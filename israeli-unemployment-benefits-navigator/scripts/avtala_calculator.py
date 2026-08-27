#!/usr/bin/env python3
"""Israeli unemployment benefits (dmei avtala) calculator for 2026.

Takes age, dependents, and 6-month salary history and returns:
- Eligibility check (standard 12-of-18; the Shaagat HaAri 6-of-18 chal"t track is a CLOSED
  window and is refused unless --chalat-start falls on or before 2026-05-14. A further
  3-of-18 tier applied to special populations inside that same window; pass the real
  month count via --qualifying-months for those cases.)
- Daily and monthly gross benefit amount
- Estimated net (after BL deduction, health tax, marginal income tax)
- Maximum benefit days based on age + dependents
- Total entitlement gross over the full duration (with day-126 ceiling drop)
- Waiting period warning based on termination reason

Usage:
    python avtala_calculator.py --age 32 --dependents 2 --salary 15000 --reason laid-off --qualifying-months 14
    python avtala_calculator.py --age 30 --salary 12000 --emergency-chalat --qualifying-months 8
    python avtala_calculator.py --example
    python avtala_calculator.py --help

All amounts in ILS (shekels). All rates effective 01.01.2026 and linked to inflation;
they re-link in January 2027. Verify against btl.gov.il/benefits/Unemployment/Pages/hisuv.aspx
for the current year before relying on the figures.

Source: btl.gov.il, kolzchut.org.il
"""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass

# 2026 figures (verify on btl.gov.il for the current year)
DAILY_CEILING_FIRST_125 = 550.76
DAILY_CEILING_AFTER_125 = 367.17
# From day 176, ONLY on the women's 300-day track and ONLY for ages 57 to 60.
# Women aged 60 to 67 on the same 300-day track have NO such cap.
# Source: btl.gov.il/benefits/Unemployment/Pages/zecoyot-nasim.aspx
DAILY_CEILING_AFTER_175_WOMEN_57_60 = 201.03
# Statutory minimum daily benefit for a discharged soldier.
DISCHARGED_SOLDIER_MIN_DAILY = 144.62
DISCHARGED_SOLDIER_MAX_DAYS = 70
# Repeat claimant (mobtal chozer = 2 or more claims in the last 4 years) under 40:
# once 100% of the entitlement days are used up, the daily maximum drops to this.
REPEAT_CLAIMANT_UNDER_40_DAILY_CEILING = 468.15
REPEAT_CLAIMANT_UNDER_40_DAYS_CAP = 1.80  # 180% of max days across 4 years
WAGE_DIVISOR = 150
BL_MONTHLY_DEDUCTION = 48
HEALTH_TAX_RATE = 0.031  # UNVERIFIED approximation. BTL publishes no rate for the health component on dmei avtala; it states only that health insurance is deducted "according to the amount of the benefit".
DEFAULT_QUAL_MONTHS_STANDARD = 12
DEFAULT_QUAL_MONTHS_EMERGENCY = 6
# Shaagat HaAri emergency chal"t window. Defining period 28.2.2026 to 14.4.2026,
# extendable by ministerial order only to 14.5.2026. CLOSED thereafter: any leave or
# job loss starting after this date falls under the standard 12-of-18 rule.
EMERGENCY_WINDOW_START = "2026-02-28"
EMERGENCY_WINDOW_END = "2026-05-14"

# The basic daily amount for computing benefits (הסכום היומי הבסיסי), 415 ILS from 01.01.2026.
# BL publishes the bracket boundaries as FRACTIONS of this amount, not as shekel figures, and
# its own worked example on hisuv.aspx is still built on an older basic amount. Derive, never copy.
BASIC_DAILY_AMOUNT = 415.00

# Progressive brackets: (upper_bound, rate_under_28, rate_28_plus).
# Boundaries are half, three quarters, the full basic amount, and 5x the basic amount.
# Nothing above 5x the basic daily amount is counted at all.
BRACKETS = [
    (BASIC_DAILY_AMOUNT * 0.50, 0.60, 0.80),   # 207.50
    (BASIC_DAILY_AMOUNT * 0.75, 0.40, 0.50),   # 311.25
    (BASIC_DAILY_AMOUNT, 0.35, 0.45),          # 415.00
    (BASIC_DAILY_AMOUNT * 5, 0.25, 0.30),      # 2,075.00
]

# No benefit is paid for the first 5 unemployment days in each 4 consecutive months of
# attendance, counted from the first attendance. These days are NOT deducted from the quota.
# Source: btl.gov.il/benefits/Unemployment/Pages/pay.aspx
UNPAID_DAYS_PER_BLOCK = 5
ATTENDANCE_MONTHS_PER_BLOCK = 4
DAYS_PER_ATTENDANCE_MONTH = 25


@dataclass
class EligibilityResult:
    eligible: bool
    reason: str | None


@dataclass
class BenefitResult:
    daily_gross: float
    monthly_gross_approx: float
    daily_net_estimate: float
    monthly_net_estimate: float
    max_days: int
    waiting_period_days: int
    total_gross_full_entitlement: float
    ceiling_applied: bool
    notes: list[str]
    daily_uncapped: float = 0.0
    tail_ceiling: float = DAILY_CEILING_AFTER_125


TERMINATION_REASONS = {
    "laid-off": 0,
    "fired": 0,
    "redundant": 0,
    "bankruptcy": 0,
    "chalat-employer": 0,
    "chalat-employee": None,      # None = a full disqualification, not a wait
    "end-of-contract": 0,
    "resigned": 90,
    "resigned-justified": 0,
    "retired-employer-initiated": 0,
    "retired-voluntary": 90,      # incl. a woman retiring voluntarily after 62
    "teacher-shabbaton": None,    # not available for work, so not entitled
    "refused-offer": 90,
}

# Refusing a suitable job, training, hishtalmut or hasava miktzoit costs BOTH a 90-day
# non-payment period AND a permanent 30-day cut in the quota, every time it happens.
# Source: btl.gov.il/benefits/Unemployment/Pages/pay.aspx
REFUSED_OFFER_DAYS_DEDUCTED = 30

# A vocational-training participant with fewer than 12 years of schooling whose own maximum
# is under 138 days is paid for up to 138 days.
# Source: btl.gov.il/benefits/Unemployment/Pages/tkufat_zakaut.aspx
TRAINING_LOW_SCHOOLING_FLOOR_DAYS = 138

# Reasons that are a DISQUALIFICATION rather than a delay, with the message to print.
DISQUALIFYING_REASONS = {
    "chalat-employee": (
        'Unpaid leave taken on the EMPLOYEE\'s own initiative carries no entitlement at all, '
        'however justified the leave was: "מי שיצא לחל"ת מיוזמתו (גם אם החל"ת מוצדק) - לא יהיה '
        'זכאי לדמי אבטלה". Only employer-initiated chal"t of at least 30 days qualifies, and '
        'remaining vacation days are set off before payment starts.'
    ),
    "teacher-shabbaton": (
        "A teacher on a shnat shabbaton is not entitled for that period, because they may not "
        "work more than a third of a post and so are not available for work offered to them."
    ),
}


# Populations that are outside the unemployment branch entirely, however many salaried
# months they have. Source: btl.gov.il/benefits/Unemployment/Pages/zakaut.aspx
NOT_INSURED = {
    "osek": "A self-employed person (osek) is not insured for unemployment.",
    "controlling-shareholder": (
        "A controlling shareholder in a closely-held company (בעל שליטה בחברת מעטים) is NOT "
        "entitled to unemployment benefit even when employed there as a salaried employee and "
        "contributions were paid: \"בעל שליטה בחברת מעטים - לא זכאי לדמי אבטלה גם אם הוא עובד "
        "בה כשכיר\". This is the most-missed refusal in the whole scheme."
    ),
    "kibbutz-member": (
        "A member of a kibbutz or a cooperative moshav is not insured, unless they work as an "
        "employee outside the collective."
    ),
    "in-service": (
        "A soldier in regular service, and anyone serving in national or civil service, is not "
        "insured for the duration of that service."
    ),
    "student-not-employed": (
        "A student or yeshiva student who is not working as a salaried employee is not insured."
    ),
}


def check_eligibility(
    is_resident: bool,
    age: int,
    qualifying_months: int,
    registered_within_3_months: bool,
    emergency_chalat: bool = False,
    not_insured: str | None = None,
) -> EligibilityResult:
    # Run the exclusion gate FIRST. A claimant in one of these groups can have 12 clean
    # salaried months and still have no entitlement, so checking months first would print a
    # confident false positive.
    if not_insured:
        return EligibilityResult(False, "NOT INSURED for unemployment. " + NOT_INSURED[not_insured])
    if not is_resident:
        return EligibilityResult(False, "Not an Israeli resident")
    if age < 20:
        return EligibilityResult(
            False,
            "Under 20: not entitled under the standard rules, but this is NOT an automatic bar. "
            "A closed exception list applies (discharged from regular IDF service other than for "
            "serious misconduct; completed 24 months of national/civil service, or a bat sherut who "
            "served at least 6 months and married within 30 days of stopping; exempted or deferred by "
            "the IDF on health, family, education, settlement or national-economy grounds; sole "
            "breadwinner of the family, or supporting a child). A na'ar from age 15 also has a "
            "separate grant track. Check references/eligibility-rules.md before telling the user no."
        )
    if age >= 67:
        return EligibilityResult(False, "Age 67 or above: not entitled to avtala; claim kitzvat zikna instead")
    required = DEFAULT_QUAL_MONTHS_EMERGENCY if emergency_chalat else DEFAULT_QUAL_MONTHS_STANDARD
    track = "Shaagat HaAri chal\"t emergency track [CLOSED WINDOW]" if emergency_chalat else "standard track"
    if qualifying_months < required:
        return EligibilityResult(
            False,
            f"Qualifying period not met ({track}): need {required} salaried months out of last 18, you have {qualifying_months}",
        )
    if not registered_within_3_months:
        return EligibilityResult(
            True,
            "Eligible, but registered outside 3-month window. Lookback shifts to registration date; consider filing a hekel mizvad waiver if delay was due to hospitalization, miluim, or emergency abroad",
        )
    return EligibilityResult(True, None)


def calculate_daily_benefit_uncapped(monthly_gross_salary: float, age: int) -> float:
    """Returns daily benefit before applying any ceiling."""
    average_daily = (monthly_gross_salary * 6) / WAGE_DIVISOR
    is_28_plus = age >= 28
    daily = 0.0
    prev_upper = 0.0
    for upper, rate_young, rate_old in BRACKETS:
        rate = rate_old if is_28_plus else rate_young
        if average_daily <= prev_upper:
            break
        taxable = min(average_daily, upper) - prev_upper
        daily += taxable * rate
        prev_upper = upper
        if average_daily <= upper:
            break
    return daily


def estimate_net(daily_gross: float, monthly_gross: float) -> tuple[float, float]:
    """Rough net estimation. Real net depends on full-year income and tax credits."""
    bl_per_day = BL_MONTHLY_DEDUCTION / 25
    health_per_day = daily_gross * HEALTH_TAX_RATE
    if daily_gross > 500:
        income_tax_rate = 0.10
    elif daily_gross > 400:
        income_tax_rate = 0.05
    else:
        income_tax_rate = 0.0
    income_tax_per_day = daily_gross * income_tax_rate
    daily_net = max(0.0, daily_gross - bl_per_day - health_per_day - income_tax_per_day)
    monthly_net = max(0.0, monthly_gross - BL_MONTHLY_DEDUCTION - (monthly_gross * HEALTH_TAX_RATE) - (monthly_gross * income_tax_rate))
    return round(daily_net, 2), round(monthly_net, 2)


def calculate_max_days(
    age: int,
    dependents: int,
    is_female: bool,
    born_1960_or_later: bool,
    discharged_soldier_first_year: bool = False,
    vocational_training_under_12_years_schooling: bool = False,
) -> int:
    if discharged_soldier_first_year:
        base = DISCHARGED_SOLDIER_MAX_DAYS
        # A trainee with fewer than 12 years of schooling whose own maximum is under 138 days
        # is paid for up to 138. Without this a low-schooling dischargee is quoted 70.
        if vocational_training_under_12_years_schooling and base < TRAINING_LOW_SCHOOLING_FLOOR_DAYS:
            return TRAINING_LOW_SCHOOLING_FLOOR_DAYS
        return base
    if 57 <= age < 67 and is_female and born_1960_or_later:
        return 300
    if age >= 45:
        return 175
    if 35 <= age < 45:
        return 175 if dependents >= 3 else 138
    if 28 <= age < 35:
        return 138 if dependents >= 3 else 100
    if 25 <= age < 28:
        return 138 if dependents >= 3 else 67
    if 20 <= age < 25:
        return 138 if dependents >= 3 else 50
    return 0


def project_total_entitlement(
    daily_uncapped: float,
    max_days: int,
    women_57_60_track: bool = False,
) -> tuple[float, bool]:
    """Project total gross over the full entitlement, applying every ceiling in turn.

    Days 1-125:   550.76
    Days 126-175: 367.17
    Days 176+:    201.03, but ONLY for a woman aged 57 to 60 on the 300-day track.
                  A woman aged 60 to 67 on the same track keeps the 367.17 ceiling,
                  and understating her tail by using 201.03 costs her (367.17 - 201.03) for each of the 125
                  days from day 176, up to 20,767.50 NIS at the ceiling.

    Returns (total_gross, ceiling_applied_anywhere).
    """
    d1 = min(max_days, 125)
    d2 = max(0, min(max_days, 175) - 125)
    d3 = max(0, max_days - 175)

    c1 = min(daily_uncapped, DAILY_CEILING_FIRST_125)
    c2 = min(daily_uncapped, DAILY_CEILING_AFTER_125)
    tail_ceiling = (
        DAILY_CEILING_AFTER_175_WOMEN_57_60 if women_57_60_track else DAILY_CEILING_AFTER_125
    )
    c3 = min(daily_uncapped, tail_ceiling)

    ceiling_applied = (
        daily_uncapped > DAILY_CEILING_FIRST_125
        or (d2 > 0 and daily_uncapped > DAILY_CEILING_AFTER_125)
        or (d3 > 0 and daily_uncapped > tail_ceiling)
    )
    total = (c1 * d1) + (c2 * d2) + (c3 * d3)
    return round(total, 2), ceiling_applied


def calculate(
    age: int,
    dependents: int,
    monthly_gross_salary: float,
    qualifying_months: int,
    is_resident: bool = True,
    registered_within_3_months: bool = True,
    termination_reason: str = "laid-off",
    is_female: bool = False,
    born_1960_or_later: bool = False,
    emergency_chalat: bool = False,
    discharged_soldier_first_year: bool = False,
    repeat_claimant: bool = False,
    not_insured: str | None = None,
    vocational_training_under_12_years_schooling: bool = False,
) -> tuple[EligibilityResult, BenefitResult | None]:
    eligibility = check_eligibility(
        is_resident, age, qualifying_months, registered_within_3_months, emergency_chalat,
        not_insured,
    )
    if not eligibility.eligible:
        return eligibility, None

    # A disqualifying reason is not a waiting period. Refuse the whole projection rather
    # than printing a number that implies entitlement.
    if termination_reason in DISQUALIFYING_REASONS:
        return EligibilityResult(False, DISQUALIFYING_REASONS[termination_reason]), None

    daily_uncapped = calculate_daily_benefit_uncapped(monthly_gross_salary, age)
    if discharged_soldier_first_year:
        daily_uncapped = max(daily_uncapped, DISCHARGED_SOLDIER_MIN_DAILY)
    daily_gross = round(min(daily_uncapped, DAILY_CEILING_FIRST_125), 2)
    ceiling_applied_first_125 = daily_uncapped > DAILY_CEILING_FIRST_125

    max_days = calculate_max_days(
        age, dependents, is_female, born_1960_or_later, discharged_soldier_first_year,
        vocational_training_under_12_years_schooling,
    )
    women_57_60_track = (
        is_female and born_1960_or_later and 57 <= age < 60 and max_days > 175
    )
    # Refusing a suitable offer permanently removes 30 days from the quota, on top of the
    # 90-day non-payment period. Apply it to max_days BEFORE projecting the total.
    if termination_reason == "refused-offer":
        max_days = max(0, max_days - REFUSED_OFFER_DAYS_DEDUCTED)

    # A repeat claimant under 40 who has already used 100% of their days gets 80% of the
    # entitlement on the next claim, capped at a lower daily maximum. Apply both.
    repeat_under_40 = repeat_claimant and age < 40
    if repeat_under_40:
        max_days = int(max_days * (REPEAT_CLAIMANT_UNDER_40_DAYS_CAP - 1.0))
        if daily_gross > REPEAT_CLAIMANT_UNDER_40_DAILY_CEILING:
            daily_gross = REPEAT_CLAIMANT_UNDER_40_DAILY_CEILING
            daily_uncapped = min(daily_uncapped, REPEAT_CLAIMANT_UNDER_40_DAILY_CEILING)

    wait_days = TERMINATION_REASONS.get(termination_reason) or 0
    monthly_gross = round(daily_gross * DAYS_PER_ATTENDANCE_MONTH, 2)

    total_gross, ceiling_anywhere = project_total_entitlement(
        daily_uncapped, max_days, women_57_60_track
    )
    daily_net, monthly_net = estimate_net(daily_gross, monthly_gross)

    notes: list[str] = []
    if discharged_soldier_first_year:
        notes.append(
            f"Discharged soldier, first year after release: max {DISCHARGED_SOLDIER_MAX_DAYS} benefit days, "
            f"and the daily benefit never falls below the statutory minimum of {DISCHARGED_SOLDIER_MIN_DAILY} ILS. "
            "Up to 6 months of regular service count toward the qualifying period."
        )
    if women_57_60_track:
        notes.append(
            f"Woman 57-60 on the 300-day track: from day 176 the daily maximum is "
            f"{DAILY_CEILING_AFTER_175_WOMEN_57_60} ILS. A woman aged 60-67 on the same track does NOT "
            "have this cap; do not apply it to her."
        )
    elif is_female and born_1960_or_later and 60 <= age < 67 and max_days > 175:
        notes.append(
            "Woman 60-67 on the 300-day track: the 201.03 day-176 cap does NOT apply to her. "
            f"Her tail keeps the {DAILY_CEILING_AFTER_125} ILS ceiling."
        )
    if repeat_claimant:
        if age < 40:
            notes.append(
                f"Repeat claimant (2 or more claims in 4 years) under 40: total days across all claims in "
                f"the 4-year window are capped at {int(REPEAT_CLAIMANT_UNDER_40_DAYS_CAP * 100)}% of the maximum. "
            f"The days and the daily ceiling above ALREADY reflect the second-claim position "
            f"(80% of the days, capped at {REPEAT_CLAIMANT_UNDER_40_DAILY_CEILING} ILS a day). "
            f"If this is still the FIRST claim of the 4-year window, rerun without --repeat-claimant."
            )
        else:
            notes.append(
                "Repeat claimant aged 40+: no cap on the AMOUNT. If unemployment was paid in the 11 months "
                "before this claim, each month's days are reduced by the days already paid in the preceding "
                "11 months (a rolling window); otherwise the entitlement is the same as a first claim."
            )
    if termination_reason == "refused-offer":
        notes.append(
            f"Refusing a suitable offer costs TWO penalties: no benefit for 90 days from the "
            f"refusal, every time it happens, AND {REFUSED_OFFER_DAYS_DEDUCTED} days permanently "
            f"removed from the quota. The days above already reflect the 30-day cut. Two published "
            f"exceptions apply on the women's 300-day track, see SKILL.md Step 7"
        )
    if ceiling_applied_first_125:
        notes.append(f"Day-1 daily ceiling applied (₪{DAILY_CEILING_FIRST_125} for first 125 days)")
    if max_days > 125:
        notes.append(
            f"Day-126 ceiling drops to ₪{DAILY_CEILING_AFTER_125}; total over {max_days} days reflects this drop"
        )
    if wait_days:
        notes.append(
            f"Waiting period: {wait_days} calendar days, counted from the DAY WORK CEASED "
            f"(מיום הפסקת העבודה), not from the registration date. Register immediately anyway"
        )
        notes.append(
            "The wait delays the start; it does NOT reduce the maximum number of days"
        )
    if emergency_chalat:
        notes.append("Shaagat HaArie chal\"t track applied (6-of-18 akhshara, day-1 payment)")
    notes.append(
        "First 5 unemployment days in EACH 4 consecutive attendance months are not paid, and are "
        "not deducted from the quota. They cut the cash, not the entitlement"
    )
    notes.append(f"BL deduction: ₪{BL_MONTHLY_DEDUCTION}/month. Net estimates are approximate")
    notes.append(
        "Approx 'monthly' uses 25 days as a conservative baseline. BL actually pays for the "
        "'possible work days' in each calendar month, which EXCLUDE Shabbat, so a real month is "
        "usually around 26 payable days. Treat the monthly figure as approximate either way"
    )
    notes.append("Figures effective 01.01.2026; verify on btl.gov.il for current year")

    return eligibility, BenefitResult(
        daily_gross=daily_gross,
        monthly_gross_approx=monthly_gross,
        daily_net_estimate=daily_net,
        monthly_net_estimate=monthly_net,
        max_days=max_days,
        waiting_period_days=wait_days,
        total_gross_full_entitlement=total_gross,
        ceiling_applied=ceiling_anywhere,
        notes=notes,
        daily_uncapped=daily_uncapped,
        tail_ceiling=(
            DAILY_CEILING_AFTER_175_WOMEN_57_60 if women_57_60_track else DAILY_CEILING_AFTER_125
        ),
    )


def format_output(e: EligibilityResult, b: BenefitResult | None) -> str:
    lines = []
    lines.append("=" * 64)
    lines.append("Israeli Unemployment Benefits Calculator (2026)")
    lines.append("=" * 64)
    lines.append("")
    if not e.eligible:
        lines.append(f"[NOT ELIGIBLE] {e.reason}")
        return "\n".join(lines)
    lines.append("[ELIGIBLE]")
    if e.reason:
        lines.append(f"  Note: {e.reason}")
    lines.append("")
    assert b is not None
    lines.append(f"Daily gross benefit:            {b.daily_gross:>10.2f} ILS")
    lines.append(f"Daily net (estimate):           {b.daily_net_estimate:>10.2f} ILS")
    lines.append(f"Approx monthly gross (25d):     {b.monthly_gross_approx:>10.2f} ILS")
    lines.append(f"Approx monthly net (estimate):  {b.monthly_net_estimate:>10.2f} ILS")
    lines.append(f"Maximum benefit days:           {b.max_days:>10}")
    lines.append(f"Total gross (full entitlement): {b.total_gross_full_entitlement:>10.2f} ILS")
    # The first 5 unemployment days in each 4 consecutive attendance months are never paid,
    # and are NOT deducted from the quota. Show the cash effect explicitly, because a
    # projection that omits it overstates the first month and every fourth month after.
    attendance_months = b.max_days / DAYS_PER_ATTENDANCE_MONTH
    blocks = max(1, math.ceil(attendance_months / ATTENDANCE_MONTHS_PER_BLOCK))
    unpaid_days = blocks * UNPAID_DAYS_PER_BLOCK
    # Price each block at the ceiling that actually governs the days it falls on. Block n
    # starts at benefit day (n-1) * 4 attendance months, so a later block can sit past day
    # 125 or past day 176, where the daily maximum is lower. Valuing every block at the
    # day-1 rate overstates the deduction for a ceiling-hitting long entitlement.
    unpaid_value = 0.0
    for n in range(blocks):
        block_start_day = n * ATTENDANCE_MONTHS_PER_BLOCK * DAYS_PER_ATTENDANCE_MONTH + 1
        if block_start_day > 175:
            ceiling = b.tail_ceiling
        elif block_start_day > 125:
            ceiling = DAILY_CEILING_AFTER_125
        else:
            ceiling = DAILY_CEILING_FIRST_125
        unpaid_value += UNPAID_DAYS_PER_BLOCK * min(b.daily_uncapped, ceiling)
    unpaid_value = round(unpaid_value, 2)
    lines.append(f"  less unpaid first-5-day blocks: {unpaid_value:>10.2f} ILS  ({blocks} x 5 days)")
    lines.append(f"Total gross after those blocks: {b.total_gross_full_entitlement - unpaid_value:>10.2f} ILS")
    lines.append(f"First month gross (25d - 5d):   {(b.daily_gross * 20):>10.2f} ILS")
    if b.waiting_period_days:
        lines.append(f"Waiting period:                 {b.waiting_period_days:>10} days")
    lines.append("")
    lines.append("Notes:")
    for n in b.notes:
        lines.append(f"  - {n}")
    lines.append("")
    lines.append("NET CAVEAT: Bituach Leumi publishes no percentage for the health component on")
    lines.append("dmei avtala (only 'ודמי ביטוח בריאות לפי סכום דמי האבטלה'), so the health element of")
    lines.append("every net figure above is an approximation, not a published rate.")
    lines.append("")
    lines.append("All net figures are estimates. Real net depends on full-year income, credits,")
    lines.append("and rounding. Verify with kolzchut.org.il and btl.gov.il before acting.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Israeli unemployment benefits calculator")
    parser.add_argument(
        "--chalat-start",
        help="Chal\"t start date YYYY-MM-DD. Required with --emergency-chalat; the emergency track is refused if it is after 2026-05-14.",
    )
    parser.add_argument("--age", type=int, help="Age in years")
    parser.add_argument("--dependents", type=int, default=0, help="Number of dependents (spouse + children)")
    parser.add_argument("--salary", type=float, help="Average monthly gross salary ILS")
    parser.add_argument(
        "--qualifying-months",
        type=int,
        help="Months of salaried work in last 18 (REQUIRED for accurate eligibility check)",
    )
    parser.add_argument(
        "--reason",
        choices=sorted(TERMINATION_REASONS.keys()),
        default="laid-off",
        help="Reason for unemployment",
    )
    parser.add_argument("--non-resident", action="store_true", help="Not an Israeli resident")
    parser.add_argument("--late-registration", action="store_true", help="Registered after 3 months")
    parser.add_argument("--female", action="store_true", help="For women aged 57-67 special track")
    parser.add_argument("--born-after-1960", action="store_true", help="For women 57-67 special track")
    parser.add_argument(
        "--discharged-soldier",
        action="store_true",
        help="Unemployment starting in the first year after release from regular service "
        "(max 70 days, statutory daily minimum 144.62)",
    )
    parser.add_argument(
        "--not-insured",
        choices=sorted(NOT_INSURED.keys()),
        default=None,
        help="Claimant is in a population outside the unemployment branch entirely. Checked "
             "BEFORE the qualifying period, because these claimants can have 12 clean salaried "
             "months and still be refused.",
    )
    parser.add_argument(
        "--training-under-12-years-schooling",
        action="store_true",
        help="Claimant is in Employment Service vocational training with fewer than 12 years of "
             "schooling. Raises a sub-138-day entitlement to 138 days.",
    )
    parser.add_argument(
        "--repeat-claimant",
        action="store_true",
        help="Filed 2 or more unemployment claims in the last 4 years (mobtal chozer)",
    )
    parser.add_argument(
        "--emergency-chalat",
        action="store_true",
        help="Shaagat HaAri chal\"t track (6-of-18 akhshara). CLOSED WINDOW: only valid when --chalat-start is on or before 2026-05-14",
    )
    parser.add_argument("--example", action="store_true", help="Run with a worked example")
    args = parser.parse_args()

    if args.example:
        print("Example: 32-year-old with 2 dependents, 15,000 ILS/month, laid off, 14 qualifying months")
        print("")
        e, b = calculate(
            age=32,
            dependents=2,
            monthly_gross_salary=15000.0,
            qualifying_months=14,
        )
        print(format_output(e, b))
        return 0

    if args.emergency_chalat:
        if not args.chalat_start:
            print(
                "Error: --emergency-chalat requires --chalat-start YYYY-MM-DD. The Shaagat HaAri\n"
                f"window ran {EMERGENCY_WINDOW_START} to {EMERGENCY_WINDOW_END} and is CLOSED; the 6-of-18\n"
                "qualifying period cannot be applied without confirming the leave fell inside it.",
                file=sys.stderr,
            )
            return 1
        if not (EMERGENCY_WINDOW_START <= args.chalat_start <= EMERGENCY_WINDOW_END):
            print(
                f"Error: chal\"t start {args.chalat_start} is outside the Shaagat HaAri window "
                f"({EMERGENCY_WINDOW_START} to {EMERGENCY_WINDOW_END}).\n"
                "That window is CLOSED. The standard 12-of-18 qualifying period applies; rerun without "
                "--emergency-chalat.",
                file=sys.stderr,
            )
            return 1

    if args.age is None or args.salary is None:
        parser.print_help()
        print("\nError: --age and --salary are required (or use --example)", file=sys.stderr)
        return 1

    if args.qualifying_months is None:
        default_qual = DEFAULT_QUAL_MONTHS_EMERGENCY if args.emergency_chalat else DEFAULT_QUAL_MONTHS_STANDARD
        print(
            f"Warning: --qualifying-months not supplied; assuming exactly the minimum ({default_qual}). "
            "Pass the real value for an accurate eligibility check.",
            file=sys.stderr,
        )
        qualifying_months = default_qual
    else:
        qualifying_months = args.qualifying_months

    e, b = calculate(
        age=args.age,
        dependents=args.dependents,
        monthly_gross_salary=args.salary,
        qualifying_months=qualifying_months,
        is_resident=not args.non_resident,
        registered_within_3_months=not args.late_registration,
        termination_reason=args.reason,
        is_female=args.female,
        born_1960_or_later=args.born_after_1960,
        emergency_chalat=args.emergency_chalat,
        discharged_soldier_first_year=args.discharged_soldier,
        repeat_claimant=args.repeat_claimant,
        not_insured=args.not_insured,
        vocational_training_under_12_years_schooling=args.training_under_12_years_schooling,
    )
    print(format_output(e, b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
