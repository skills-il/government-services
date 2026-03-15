#!/usr/bin/env python3
"""
Sal Klita (Absorption Basket) Calculator

Calculates the expected sal klita amounts for new immigrants (olim)
based on family size and year. The sal klita is a financial grant
provided by Misrad HaKlita (Ministry of Absorption) to help olim
during their first months in Israel.

Note: Amounts are approximations based on published rates and may
vary. Always verify current amounts with Misrad HaKlita or at
klita.gov.il for the most up-to-date figures.

Usage:
    python scripts/sal-klita-calculator.py --family-size 1
    python scripts/sal-klita-calculator.py --family-size 4 --year 2026
    python scripts/sal-klita-calculator.py --help
"""

import argparse
import sys
from datetime import datetime


# Approximate sal klita base amounts in NIS (as of 2025/2026).
# These are estimates based on published Misrad HaKlita schedules.
# Actual amounts are updated annually and may differ.
#
# Structure: {year: {category: {airport_payment, monthly_payment, months, total}}}
# Categories: single, couple, family_small (1-2 children), family_large (3+ children)

SAL_KLITA_RATES = {
    2025: {
        "single": {
            "airport": 2500,
            "monthly": 2800,
            "months": 6,
            "rental_supplement": 0,
        },
        "couple": {
            "airport": 3700,
            "monthly": 3600,
            "months": 6,
            "final_payment": 3600,
            "rental_supplement": 0,
        },
        "family_small": {
            "airport": 4200,
            "monthly": 4000,
            "months": 6,
            "final_payment": 4000,
            "per_child_bonus": 1000,
            "rental_supplement": 0,
        },
        "family_large": {
            "airport": 4700,
            "monthly": 4400,
            "months": 6,
            "final_payment": 4400,
            "per_child_bonus": 1000,
            "rental_supplement": 0,
        },
    },
    2026: {
        "single": {
            "airport": 2600,
            "monthly": 2900,
            "months": 6,
            "rental_supplement": 0,
        },
        "couple": {
            "airport": 3850,
            "monthly": 3750,
            "months": 6,
            "final_payment": 3750,
            "rental_supplement": 0,
        },
        "family_small": {
            "airport": 4350,
            "monthly": 4150,
            "months": 6,
            "final_payment": 4150,
            "per_child_bonus": 1050,
            "rental_supplement": 0,
        },
        "family_large": {
            "airport": 4900,
            "monthly": 4600,
            "months": 6,
            "final_payment": 4600,
            "per_child_bonus": 1050,
            "rental_supplement": 0,
        },
    },
}


def get_category(family_size: int) -> str:
    """Determine the sal klita category based on family size."""
    if family_size == 1:
        return "single"
    elif family_size == 2:
        return "couple"
    elif family_size <= 4:
        return "family_small"
    else:
        return "family_large"


def get_category_label(category: str) -> str:
    """Human-readable category label."""
    labels = {
        "single": "Single Oleh",
        "couple": "Couple (no children)",
        "family_small": "Family (1-2 children)",
        "family_large": "Family (3+ children)",
    }
    return labels.get(category, category)


def get_num_children(family_size: int) -> int:
    """Calculate number of children from family size."""
    if family_size <= 2:
        return 0
    return family_size - 2


def calculate_sal_klita(family_size: int, year: int) -> dict:
    """Calculate sal klita amounts for the given family size and year."""
    category = get_category(family_size)
    num_children = get_num_children(family_size)

    # Use closest available year if exact year not in rates
    available_years = sorted(SAL_KLITA_RATES.keys())
    if year in SAL_KLITA_RATES:
        rates = SAL_KLITA_RATES[year]
    elif year > max(available_years):
        # Extrapolate from latest year with ~3% annual increase
        base_year = max(available_years)
        rates = SAL_KLITA_RATES[base_year]
        years_diff = year - base_year
        adjustment = 1.03 ** years_diff
        rates = {
            cat: {k: int(v * adjustment) if isinstance(v, (int, float)) else v
                  for k, v in cat_rates.items()}
            for cat, cat_rates in rates.items()
        }
    else:
        rates = SAL_KLITA_RATES[min(available_years)]

    cat_rates = rates[category]

    airport = cat_rates["airport"]
    monthly = cat_rates["monthly"]
    months = cat_rates["months"]
    final_payment = cat_rates.get("final_payment", 0)
    per_child_bonus = cat_rates.get("per_child_bonus", 0)

    child_bonus_total = per_child_bonus * num_children
    monthly_total = monthly * months
    total = airport + monthly_total + final_payment + child_bonus_total

    return {
        "category": category,
        "category_label": get_category_label(category),
        "family_size": family_size,
        "num_children": num_children,
        "year": year,
        "airport": airport,
        "monthly": monthly,
        "months": months,
        "final_payment": final_payment,
        "per_child_bonus": per_child_bonus,
        "child_bonus_total": child_bonus_total,
        "monthly_total": monthly_total,
        "total": total,
    }


def print_results(result: dict):
    """Print formatted sal klita calculation results."""
    print()
    print("=" * 60)
    print("  SAL KLITA (ABSORPTION BASKET) CALCULATOR")
    print(f"  Estimated amounts for {result['year']}")
    print("=" * 60)
    print()
    print(f"  Family size:    {result['family_size']} person(s)")
    print(f"  Category:       {result['category_label']}")
    if result["num_children"] > 0:
        print(f"  Children:       {result['num_children']}")
    print()
    print("  PAYMENT SCHEDULE")
    print(f"  {'-' * 50}")
    print()

    # Payment schedule table
    print(f"  {'Payment':<25} {'Amount (NIS)':>15}")
    print(f"  {'=' * 40}")
    print(f"  {'Airport (arrival)':<25} {result['airport']:>12,}")
    print()

    for month in range(1, result["months"] + 1):
        print(f"  {'Month ' + str(month):<25} {result['monthly']:>12,}")

    if result["final_payment"] > 0:
        print(f"  {'Month 7 (final)':<25} {result['final_payment']:>12,}")

    if result["child_bonus_total"] > 0:
        print()
        print(f"  {'Child bonus':<25} {result['child_bonus_total']:>12,}")
        print(f"  ({result['num_children']} children x {result['per_child_bonus']:,} NIS each)")

    print()
    print(f"  {'-' * 40}")
    print(f"  {'TOTAL ESTIMATED':<25} {result['total']:>12,} NIS")
    print(f"  {'-' * 40}")
    print()

    # Timeline
    print("  PAYMENT TIMELINE")
    print(f"  {'-' * 50}")
    print(f"  Arrival:     {result['airport']:,} NIS (cash at airport)")
    print(f"  Months 1-6:  {result['monthly']:,} NIS/month (bank transfer)")
    if result["final_payment"] > 0:
        print(f"  Month 7:     {result['final_payment']:,} NIS (final payment)")
    if result["child_bonus_total"] > 0:
        print(f"  Children:    {result['child_bonus_total']:,} NIS (added to payments)")
    print()

    # Disclaimer
    print("  IMPORTANT NOTES")
    print(f"  {'-' * 50}")
    print("  * Amounts are ESTIMATES based on published rates")
    print("  * Actual amounts are updated annually by Misrad HaKlita")
    print("  * Verify current amounts at klita.gov.il")
    print("  * Sal klita is NOT taxable income")
    print("  * Sal klita does NOT need to be repaid")
    print("  * Payments require an active Israeli bank account")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Calculate estimated sal klita (absorption basket) amounts for new olim.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --family-size 1              Single oleh, current year
  %(prog)s --family-size 2              Couple, current year
  %(prog)s --family-size 4 --year 2026  Family of 4 (2 adults + 2 children)
  %(prog)s --family-size 6              Family with 4 children

Notes:
  - Family size 1 = single oleh
  - Family size 2 = couple (no children)
  - Family size 3-4 = family with 1-2 children
  - Family size 5+ = family with 3+ children
  - Amounts are estimates; verify at klita.gov.il
        """
    )

    parser.add_argument(
        "--family-size",
        type=int,
        required=True,
        help="Total number of family members making aliyah (1=single, 2=couple, 3+=family)"
    )
    parser.add_argument(
        "--year",
        type=int,
        default=datetime.now().year,
        help=f"Year to calculate for (default: {datetime.now().year})"
    )

    args = parser.parse_args()

    if args.family_size < 1:
        print("Error: Family size must be at least 1.")
        sys.exit(1)

    if args.family_size > 15:
        print("Error: Family size seems unusually large. Maximum supported: 15.")
        sys.exit(1)

    if args.year < 2020 or args.year > 2035:
        print(f"Error: Year must be between 2020 and 2035. Got: {args.year}")
        sys.exit(1)

    result = calculate_sal_klita(args.family_size, args.year)
    print_results(result)


if __name__ == "__main__":
    main()
