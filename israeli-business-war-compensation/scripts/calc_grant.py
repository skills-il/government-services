#!/usr/bin/env python3
"""Shaagat HaAri (March-April 2026) indirect-damage compensation calculator.

Implements the operative statute directly:
חוק התוכנית לסיוע כלכלי (הוראת שעה)(סיוע לעסקים ולמוסדות ציבור), התשפ"ו-2026
(Knesset: https://fs.knesset.gov.il/25/law/25_lsr_12958311.pdf)

Statutory rules this implements, each of which a naive calculator gets wrong:

  * §38לו "הוצאות מזכות" = ההוצאות הקבועות BEPLUS חלק השכר המזכה, capped, then x2.
    The wage part and the fixed-cost part are ADDED, never compared. Paying "the
    higher of the two tracks" understates the grant for any business that has both
    payroll and fixed costs, which is almost all of them.
  * The cap is 600K (base-year turnover <= 100M) / 600K + 0.3% of the excess
    (100M-300M) / 1.2M (300M-400M) -- and the cap is doubled too. The effective
    payout ceiling under 100M turnover is 1.2M, not 600K.
  * §38לו "הוצאות קבועות" = total current VAT inputs of the PREVIOUS year, / 6,
    times the fixed-cost coefficient. NOT the owner's monthly rent + utilities.
  * §38לז(ב) small-business (<=300K) amounts are PER MONTH and paid at x2, and are
    gated on the same >25% decline test as every other track.
  * §38לז(ג) floor: a nationwide-track business that would receive less than the
    top small-business band receives that amount instead.
  * Bands are (low, high]: a decline of exactly 40% sits in the 7% tier.

Run: python calc_grant.py --help
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

# ---------------------------------------------------------------- constants

# §38לו: the s.2(b) National Insurance average wage "as known in March 2026",
# i.e. the figure in force from 01.01.2026.
AVERAGE_WAGE_NIS = 13_769
EMPLOYER_COST_FACTOR = 1.25  # מקדם עלות מעביד

MIN_DECLINE = 0.25  # must be EXCEEDED, not merely reached ("עולה על 25%")
TURNOVER_FLOOR = 12_000
TURNOVER_CEILING = 400_000_000
SMALL_BUSINESS_THRESHOLD = 300_000

DOUBLING = 2  # §38לו "כשהוא מוכפל ב־2" / §38לז(ב) "פי 2"

# §38לו מקדם ההוצאות הקבועות: general tiers. Bands are (low, high].
FIXED_COST_TIERS: list[tuple[float, float, float]] = [
    (0.25, 0.40, 0.07),
    (0.40, 0.60, 0.11),
    (0.60, 0.80, 0.15),
    (0.80, 1.01, 0.22),
]

# §38לו: sector overrides that REPLACE the tiered coefficient.
SECTOR_COEFFICIENTS: dict[str, float] = {
    "fuel": 0.35,        # סחר סיטונאי/קמעונאי בדלק
    "vat-exempt": 0.19,  # עוסק פטור לפי סעיף 33 לחוק מע"מ
    "contractor": 0.68,  # קבלן ביצוע
}

# §38לז(ה) מקדם הנזק. Bands are (low, high].
DAMAGE_COEFFICIENT: list[tuple[float, float, float]] = [
    (0.25, 0.40, 1.0),
    (0.40, 0.60, 1.5),
    (0.60, 0.80, 2.4),
    (0.80, 1.01, 3.0),
]

# §38לז(ב) base amounts PER MONTH, by base-year turnover band:
# (upper_turnover, base_amount, scales_by_damage_coefficient)
SMALL_BUSINESS_BANDS: list[tuple[float, float, bool]] = [
    (50_000, 1_864, False),
    (90_000, 3_356, False),
    (120_000, 4_475, False),
    (150_000, 2_823, True),
    (200_000, 3_329, True),
    (250_000, 4_261, True),
    (300_000, 4_980, True),
]


# ---------------------------------------------------------------- helpers

def _band(value: float, table: list[tuple[float, float, float]]) -> float | None:
    """Bands are (low, high]: a decline of exactly 40% -> the 25-40 row."""
    for low, high, out in table:
        if low < value <= high:
            return out
    return None


def fixed_cost_coefficient(decline: float, sector: str | None = None) -> float | None:
    if sector:
        if sector not in SECTOR_COEFFICIENTS:
            raise ValueError(f"unknown sector {sector!r}; expected {sorted(SECTOR_COEFFICIENTS)}")
        return SECTOR_COEFFICIENTS[sector]
    return _band(decline, FIXED_COST_TIERS)


def damage_coefficient(decline: float) -> float | None:
    return _band(decline, DAMAGE_COEFFICIENT)


def eligible_expenses_cap(base_year_turnover: float) -> float:
    """§38לו: cap on eligible expenses, BEFORE the x2."""
    if base_year_turnover <= 100_000_000:
        return 600_000
    if base_year_turnover <= 300_000_000:
        return 600_000 + 0.003 * (base_year_turnover - 100_000_000)
    return 1_200_000


def small_business_grant(base_year_turnover: float, decline: float) -> float | None:
    """§38לז(ב): the amount actually paid (already doubled). None if out of band."""
    if base_year_turnover > SMALL_BUSINESS_THRESHOLD:
        return None
    coef = damage_coefficient(decline)
    if coef is None:
        return None
    for upper, amount, scales in SMALL_BUSINESS_BANDS:
        if base_year_turnover <= upper:
            return amount * (coef if scales else 1.0) * DOUBLING
    return None


# ---------------------------------------------------------------- result

@dataclass
class GrantResult:
    decline_rate: float = 0.0
    eligible: bool = False
    eligibility_reason: str = ""
    wage_part: float = 0.0
    wage_part_per_emp_cap: float = 0.0
    fixed_part: float = 0.0
    fixed_coefficient: float | None = None
    eligible_expenses: float = 0.0
    cap_before_doubling: float = 0.0
    cap_applied: bool = False
    small_business_amount: float | None = None
    floor_applied: bool = False
    total_grant: float = 0.0


# ---------------------------------------------------------------- core

def calc_grant(
    ref_turnover: float,
    claim_turnover: float,
    wages_in_period: float = 0.0,
    employees: int = 0,
    prior_year_vat_inputs: float = 0.0,
    base_year_turnover: float | None = None,
    sector: str | None = None,
    vacation_pay_in_period: float = 0.0,
    btl_miluim_reimbursement: float = 0.0,
) -> GrantResult:
    """Compute the Shaagat HaAri indirect-damage grant.

    base_year_turnover routes the small-business track and sizes the cap; it
    defaults to ref_turnover x 6 (a two-month reference period -> base year).
    """
    if ref_turnover <= 0:
        return GrantResult(eligibility_reason="Reference turnover must be positive")

    decline = (ref_turnover - claim_turnover) / ref_turnover
    if base_year_turnover is None:
        base_year_turnover = ref_turnover * 6

    # The gate must be EXCEEDED: exactly 25% does not qualify.
    if decline <= MIN_DECLINE:
        return GrantResult(
            decline_rate=decline,
            eligibility_reason=(
                f"Decline {decline:.1%} does not EXCEED the statutory 25% gate. No track "
                "is available, including the small-business track (§38לז(ב) incorporates "
                "the same >25% test through (a)(2))."
            ),
        )

    if not (TURNOVER_FLOOR <= base_year_turnover <= TURNOVER_CEILING):
        return GrantResult(
            decline_rate=decline,
            eligibility_reason=(
                f"Base-year turnover {base_year_turnover:,.0f} NIS is outside the "
                f"{TURNOVER_FLOOR:,}-{TURNOVER_CEILING:,} band"
            ),
        )

    sb = small_business_grant(base_year_turnover, decline)
    if sb is not None:
        return GrantResult(
            decline_rate=decline,
            eligible=True,
            eligibility_reason="OK (small-business continuity track, <=300K turnover)",
            small_business_amount=sb,
            total_grant=sb,
        )

    # Nationwide track: the parts are ADDED, then capped, then doubled.
    wage_base = max(0.0, wages_in_period - vacation_pay_in_period - btl_miluim_reimbursement)
    wage_part = wage_base * decline
    per_emp_cap = AVERAGE_WAGE_NIS * EMPLOYER_COST_FACTOR * employees * decline
    wage_part = min(wage_part, per_emp_cap)

    coef = fixed_cost_coefficient(decline, sector)
    fixed_part = (prior_year_vat_inputs / 6) * (coef or 0.0)

    eligible_expenses = wage_part + fixed_part
    cap = eligible_expenses_cap(base_year_turnover)
    total = min(eligible_expenses, cap) * DOUBLING

    # §38לז(ג) floor: never below what the top small-business band would have paid.
    floor = small_business_grant(SMALL_BUSINESS_THRESHOLD, decline) or 0.0
    floor_applied = total < floor
    if floor_applied:
        total = floor

    return GrantResult(
        decline_rate=decline,
        eligible=True,
        eligibility_reason="OK (nationwide track)",
        wage_part=wage_part,
        wage_part_per_emp_cap=per_emp_cap,
        fixed_part=fixed_part,
        fixed_coefficient=coef,
        eligible_expenses=eligible_expenses,
        cap_before_doubling=cap,
        cap_applied=eligible_expenses > cap,
        floor_applied=floor_applied,
        total_grant=total,
    )


# ---------------------------------------------------------------- cli

def _print_result(r: GrantResult) -> None:
    print("=== Shaagat HaAri indirect-damage compensation (March-April 2026) ===\n")
    print(f"Turnover decline:      {r.decline_rate:.1%}")
    if not r.eligible:
        print(f"NOT ELIGIBLE:          {r.eligibility_reason}")
        return
    print(f"Status:                {r.eligibility_reason}\n")

    if r.small_business_amount is not None:
        print(f"Small-business grant:  {r.small_business_amount:,.2f} NIS")
        print("  (statutory monthly amount x damage coefficient, then x2 per §38לז(ב))")
    else:
        print(f"Wage part              {r.wage_part:,.2f} NIS  "
              f"(per-employee cap {r.wage_part_per_emp_cap:,.2f})")
        coef = f"{r.fixed_coefficient:.2%}" if r.fixed_coefficient else "n/a"
        print(f"Fixed-cost part      + {r.fixed_part:,.2f} NIS  (coefficient {coef})")
        print(f"Eligible expenses    = {r.eligible_expenses:,.2f} NIS  (ADDED, not compared)")
        print(f"Cap (before x2)        {r.cap_before_doubling:,.2f} NIS"
              f"{'   <- APPLIED' if r.cap_applied else ''}")
        print(f"x2 per §38לו")
        if r.floor_applied:
            print("§38לז(ג) FLOOR APPLIED: raised to the top small-business band")

    print(f"\nTOTAL GRANT:           {r.total_grant:,.2f} NIS")
    print("\nNOTE: fixed expenses come from the PREVIOUS year's total VAT inputs / 6,")
    print("      NOT from the owner's monthly rent and utility bills.")


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--ref-turnover", type=float, required=True,
                   help="Turnover in the reference (baseline) period")
    p.add_argument("--claim-turnover", type=float, required=True,
                   help="Turnover in the eligible period (March-April 2026)")
    p.add_argument("--wages", type=float, default=0.0,
                   help="Gross wages paid in the eligible period (Form 102)")
    p.add_argument("--employees", type=int, default=0, help="Number of eligible employees")
    p.add_argument("--vat-inputs", type=float, default=0.0,
                   help="Total current VAT inputs of the PREVIOUS year (סך התשומות השוטפות)")
    p.add_argument("--base-year-turnover", type=float, default=None,
                   help="Base-year turnover (defaults to ref-turnover x 6)")
    p.add_argument("--sector", choices=sorted(SECTOR_COEFFICIENTS),
                   help="Statutory sector override for the fixed-cost coefficient")
    p.add_argument("--vacation-pay", type=float, default=0.0,
                   help="Pay for vacation days used (deducted from the wage base)")
    p.add_argument("--miluim-reimbursement", type=float, default=0.0,
                   help="Reserve-duty sums BTL reimbursed the employer (deducted from the wage base)")
    a = p.parse_args()

    _print_result(calc_grant(
        ref_turnover=a.ref_turnover,
        claim_turnover=a.claim_turnover,
        wages_in_period=a.wages,
        employees=a.employees,
        prior_year_vat_inputs=a.vat_inputs,
        base_year_turnover=a.base_year_turnover,
        sector=a.sector,
        vacation_pay_in_period=a.vacation_pay,
        btl_miluim_reimbursement=a.miluim_reimbursement,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
