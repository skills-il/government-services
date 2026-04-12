#!/usr/bin/env python3
"""Israeli unemployment benefits (dmei avtala) calculator for 2026.

Takes age, dependents, and 6-month salary history and returns:
- Eligibility check
- Daily and monthly gross benefit amount
- Maximum benefit days based on age + dependents
- Waiting period warning based on termination reason

Usage:
    python avtala_calculator.py --age 32 --dependents 2 --salary 15000 --reason laid-off
    python avtala_calculator.py --example
    python avtala_calculator.py --help

All amounts in ILS (shekels). All rates current for 2026.
Source: btl.gov.il, kolzchut.org.il
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

DAILY_CEILING_FIRST_125 = 550.76
DAILY_CEILING_AFTER_125 = 367.17
WAGE_DIVISOR = 150
BL_MONTHLY_DEDUCTION = 32

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
    max_days: int
    waiting_period_days: int
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
) -> EligibilityResult:
    if not is_resident:
        return EligibilityResult(False, "Not an Israeli resident")
    if age < 20:
        return EligibilityResult(False, "Below minimum age (20)")
    if age >= 67:
        return EligibilityResult(False, "Above maximum age (67); see kiztavat zikna")
    if qualifying_months < 12:
        return EligibilityResult(
            False,
            f"Qualifying period not met: need 12 salaried months out of last 18, you have {qualifying_months}",
        )
    if not registered_within_3_months:
        return EligibilityResult(
            True,
            "Eligible, but registered outside 3-month window — 18-month lookback shifts to registration date",
        )
    return EligibilityResult(True, None)


def calculate_daily_benefit(monthly_gross_salary: float, age: int) -> tuple[float, bool]:
    """Returns (daily_gross_benefit, ceiling_applied)."""
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
    ceiling_applied = False
    if daily > DAILY_CEILING_FIRST_125:
        daily = DAILY_CEILING_FIRST_125
        ceiling_applied = True
    return round(daily, 2), ceiling_applied


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


def calculate(
    age: int,
    dependents: int,
    monthly_gross_salary: float,
    is_resident: bool = True,
    qualifying_months: int = 12,
    registered_within_3_months: bool = True,
    termination_reason: str = "laid-off",
    is_female: bool = False,
    born_1960_or_later: bool = False,
) -> tuple[EligibilityResult, BenefitResult | None]:
    eligibility = check_eligibility(
        is_resident, age, qualifying_months, registered_within_3_months
    )
    if not eligibility.eligible:
        return eligibility, None

    daily_gross, ceiling = calculate_daily_benefit(monthly_gross_salary, age)
    max_days = calculate_max_days(age, dependents, is_female, born_1960_or_later)
    wait_days = TERMINATION_REASONS.get(termination_reason, 0)
    monthly_gross = daily_gross * 25

    notes: list[str] = []
    if ceiling:
        notes.append(f"Daily ceiling applied ({DAILY_CEILING_FIRST_125} for first 125 days)")
    if wait_days:
        notes.append(f"Waiting period: {wait_days} days before first payment")
    notes.append(
        f"Day 126+ ceiling is {DAILY_CEILING_AFTER_125}, which may apply if unemployment exceeds 125 days"
    )
    notes.append(f"Bituach Leumi monthly deduction: {BL_MONTHLY_DEDUCTION} ILS")

    return eligibility, BenefitResult(
        daily_gross=daily_gross,
        monthly_gross_approx=round(monthly_gross, 2),
        max_days=max_days,
        waiting_period_days=wait_days,
        ceiling_applied=ceiling,
        notes=notes,
    )


def format_output(e: EligibilityResult, b: BenefitResult | None) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append("Israeli Unemployment Benefits Calculator (2026)")
    lines.append("=" * 60)
    lines.append("")
    if not e.eligible:
        lines.append(f"[NOT ELIGIBLE] {e.reason}")
        return "\n".join(lines)
    lines.append("[ELIGIBLE]")
    if e.reason:
        lines.append(f"  Note: {e.reason}")
    lines.append("")
    assert b is not None
    lines.append(f"Daily gross benefit:       {b.daily_gross:>10.2f} ILS")
    lines.append(f"Monthly gross (approx):    {b.monthly_gross_approx:>10.2f} ILS")
    lines.append(f"Maximum benefit days:      {b.max_days:>10}")
    if b.waiting_period_days:
        lines.append(f"Waiting period:            {b.waiting_period_days:>10} days")
    lines.append("")
    lines.append("Notes:")
    for n in b.notes:
        lines.append(f"  - {n}")
    lines.append("")
    lines.append("All figures before income tax, BL, and health tax deductions.")
    lines.append("Verify at kolzchut.org.il and btl.gov.il before acting.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Israeli unemployment benefits calculator")
    parser.add_argument("--age", type=int, help="Age in years")
    parser.add_argument("--dependents", type=int, default=0, help="Number of dependents (spouse + children)")
    parser.add_argument("--salary", type=float, help="Average monthly gross salary ILS")
    parser.add_argument("--qualifying-months", type=int, default=12, help="Months of salaried work in last 18")
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
    parser.add_argument("--example", action="store_true", help="Run with a worked example")
    args = parser.parse_args()

    if args.example:
        print("Example: 32-year-old with 2 dependents, 15,000 ILS/month, laid off")
        print("")
        e, b = calculate(age=32, dependents=2, monthly_gross_salary=15000.0)
        print(format_output(e, b))
        return 0

    if args.age is None or args.salary is None:
        parser.print_help()
        print("\nError: --age and --salary are required (or use --example)", file=sys.stderr)
        return 1

    e, b = calculate(
        age=args.age,
        dependents=args.dependents,
        monthly_gross_salary=args.salary,
        is_resident=not args.non_resident,
        qualifying_months=args.qualifying_months,
        registered_within_3_months=not args.late_registration,
        termination_reason=args.reason,
        is_female=args.female,
        born_1960_or_later=args.born_after_1960,
    )
    print(format_output(e, b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
