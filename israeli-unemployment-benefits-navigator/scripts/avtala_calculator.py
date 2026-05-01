#!/usr/bin/env python3
"""Israeli unemployment benefits (dmei avtala) calculator for 2026.

Takes age, dependents, and 6-month salary history and returns:
- Eligibility check (standard 12-of-18 or Shaagat HaArie 6-of-18 chal"t track)
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
import sys
from dataclasses import dataclass

# 2026 figures (verify on btl.gov.il for the current year)
DAILY_CEILING_FIRST_125 = 550.76
DAILY_CEILING_AFTER_125 = 367.17
WAGE_DIVISOR = 150
BL_MONTHLY_DEDUCTION = 48
HEALTH_TAX_RATE = 0.031  # ~3.1% mas briut on benefit, approximate
DEFAULT_QUAL_MONTHS_STANDARD = 12
DEFAULT_QUAL_MONTHS_EMERGENCY = 6

# Progressive brackets: (upper_bound, rate_under_28, rate_28_plus)
BRACKETS = [
    (207.50, 0.60, 0.80),
    (311.00, 0.40, 0.50),
    (415.00, 0.35, 0.45),
    (float("inf"), 0.25, 0.30),
]


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


TERMINATION_REASONS = {
    "laid-off": 0,
    "fired": 0,
    "redundant": 0,
    "bankruptcy": 0,
    "chalat": 0,
    "end-of-contract": 0,
    "resigned": 90,
    "resigned-justified": 0,
    "refused-offer": 90,
}


def check_eligibility(
    is_resident: bool,
    age: int,
    qualifying_months: int,
    registered_within_3_months: bool,
    emergency_chalat: bool = False,
) -> EligibilityResult:
    if not is_resident:
        return EligibilityResult(False, "Not an Israeli resident")
    if age < 20:
        return EligibilityResult(False, "Below minimum age (20)")
    if age >= 67:
        return EligibilityResult(False, "Above maximum age (67); see kiztavat zikna")
    required = DEFAULT_QUAL_MONTHS_EMERGENCY if emergency_chalat else DEFAULT_QUAL_MONTHS_STANDARD
    track = "Shaagat HaArie chal\"t emergency track" if emergency_chalat else "standard track"
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
) -> int:
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


def project_total_entitlement(daily_uncapped: float, max_days: int) -> tuple[float, bool]:
    """Project total gross over full entitlement with the day-126 ceiling drop.

    Returns (total_gross, ceiling_applied_anywhere).
    """
    front_days = min(max_days, 125)
    tail_days = max(0, max_days - 125)
    front_capped = min(daily_uncapped, DAILY_CEILING_FIRST_125)
    tail_capped = min(daily_uncapped, DAILY_CEILING_AFTER_125)
    ceiling_applied = (
        daily_uncapped > DAILY_CEILING_FIRST_125
        or (tail_days > 0 and daily_uncapped > DAILY_CEILING_AFTER_125)
    )
    total = (front_capped * front_days) + (tail_capped * tail_days)
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
) -> tuple[EligibilityResult, BenefitResult | None]:
    eligibility = check_eligibility(
        is_resident, age, qualifying_months, registered_within_3_months, emergency_chalat
    )
    if not eligibility.eligible:
        return eligibility, None

    daily_uncapped = calculate_daily_benefit_uncapped(monthly_gross_salary, age)
    daily_gross = round(min(daily_uncapped, DAILY_CEILING_FIRST_125), 2)
    ceiling_applied_first_125 = daily_uncapped > DAILY_CEILING_FIRST_125

    max_days = calculate_max_days(age, dependents, is_female, born_1960_or_later)
    wait_days = TERMINATION_REASONS.get(termination_reason, 0)
    monthly_gross = round(daily_gross * 25, 2)

    total_gross, ceiling_anywhere = project_total_entitlement(daily_uncapped, max_days)
    daily_net, monthly_net = estimate_net(daily_gross, monthly_gross)

    notes: list[str] = []
    if ceiling_applied_first_125:
        notes.append(f"Day-1 daily ceiling applied (₪{DAILY_CEILING_FIRST_125} for first 125 days)")
    if max_days > 125:
        notes.append(
            f"Day-126 ceiling drops to ₪{DAILY_CEILING_AFTER_125}; total over {max_days} days reflects this drop"
        )
    if wait_days:
        notes.append(
            f"Waiting period: {wait_days} calendar days. Clock starts on REGISTRATION date, not last workday"
        )
    if emergency_chalat:
        notes.append("Shaagat HaArie chal\"t track applied (6-of-18 akhshara, day-1 payment)")
    notes.append(f"BL deduction: ₪{BL_MONTHLY_DEDUCTION}/month. Net estimates are approximate")
    notes.append("Approx 'monthly' assumes 25 working days; BL pays per reporting weeks (4 or 5/month)")
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
    if b.waiting_period_days:
        lines.append(f"Waiting period:                 {b.waiting_period_days:>10} days")
    lines.append("")
    lines.append("Notes:")
    for n in b.notes:
        lines.append(f"  - {n}")
    lines.append("")
    lines.append("All net figures are estimates. Real net depends on full-year income, credits,")
    lines.append("and rounding. Verify with kolzchut.org.il and btl.gov.il before acting.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Israeli unemployment benefits calculator")
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
        "--emergency-chalat",
        action="store_true",
        help="Shaagat HaArie chal\"t track (6-of-18 akhshara, defining period 28 Feb to 14 May 2026)",
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
    )
    print(format_output(e, b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
