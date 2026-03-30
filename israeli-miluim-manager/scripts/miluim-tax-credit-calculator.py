#!/usr/bin/env python3
"""
Miluim Tax Credit Calculator

Estimates tax credits for Israeli combat reserve duty (miluim) based on
the number of combat service days in a given tax year.

Amendment 283 to the Income Tax Ordinance (Section 39B), effective
January 1, 2026, introduced a 17-tier graduated credit system for
combat reservists (lochamim) for tax years 2026-2027:

  - Under 30 days: Standard credit (1.0 credit point)
  - 30-39 days:  0.50 credit points
  - 40-49 days:  0.75 credit points
  - 50-54 days:  1.00 credit points
  - 55-59 days:  1.25 credit points
  - 60-64 days:  1.50 credit points
  - 65-69 days:  1.75 credit points
  - 70-74 days:  2.00 credit points
  - 75-79 days:  2.25 credit points
  - 80-84 days:  2.50 credit points
  - 85-89 days:  2.75 credit points
  - 90-94 days:  3.00 credit points
  - 95-99 days:  3.25 credit points
  - 100-104 days: 3.50 credit points
  - 105-109 days: 3.75 credit points
  - 110+ days:   4.00 credit points

IMPORTANT: These tiers apply to COMBAT service days only. Non-combat
reserve service qualifies for the standard 1.0 credit point.

Additionally, reservists earning below NIS 9,863/month receive a
top-up from Bituach Leumi to reach that minimum compensation floor.

Usage:
    python scripts/miluim-tax-credit-calculator.py --days 45 --monthly-income 15000
    python scripts/miluim-tax-credit-calculator.py --days 120 --monthly-income 8000
    python scripts/miluim-tax-credit-calculator.py --days 25 --monthly-income 20000

Note: Tax credit point values are based on 2026 rates (frozen through
2027). Consult Rashut HaMisim (Tax Authority) for exact values.
"""

import argparse
import sys


# 2026 Tax Credit Point Value (frozen through 2027)
# A single credit point (nekudat zikui) is worth NIS 242/month
# or NIS 2,904/year
CREDIT_POINT_MONTHLY = 242
CREDIT_POINT_ANNUAL = CREDIT_POINT_MONTHLY * 12

# Minimum compensation floor (Bituach Leumi)
MIN_COMPENSATION_DAILY = 328.76
MIN_COMPENSATION_MONTHLY = 9863

# Amendment 283 combat credit tiers (Section 39B)
# For tax years 2026-2027, minimum qualifying days is 30
# From 2028, minimum drops to 20 days
COMBAT_CREDIT_TIERS = [
    {"min_days": 110, "max_days": None, "points": 4.00, "name": "Maximum", "hebrew": "מקסימלי"},
    {"min_days": 105, "max_days": 109, "points": 3.75, "name": "Tier 15", "hebrew": "דרגה 15"},
    {"min_days": 100, "max_days": 104, "points": 3.50, "name": "Tier 14", "hebrew": "דרגה 14"},
    {"min_days": 95, "max_days": 99, "points": 3.25, "name": "Tier 13", "hebrew": "דרגה 13"},
    {"min_days": 90, "max_days": 94, "points": 3.00, "name": "Tier 12", "hebrew": "דרגה 12"},
    {"min_days": 85, "max_days": 89, "points": 2.75, "name": "Tier 11", "hebrew": "דרגה 11"},
    {"min_days": 80, "max_days": 84, "points": 2.50, "name": "Tier 10", "hebrew": "דרגה 10"},
    {"min_days": 75, "max_days": 79, "points": 2.25, "name": "Tier 9", "hebrew": "דרגה 9"},
    {"min_days": 70, "max_days": 74, "points": 2.00, "name": "Tier 8", "hebrew": "דרגה 8"},
    {"min_days": 65, "max_days": 69, "points": 1.75, "name": "Tier 7", "hebrew": "דרגה 7"},
    {"min_days": 60, "max_days": 64, "points": 1.50, "name": "Tier 6", "hebrew": "דרגה 6"},
    {"min_days": 55, "max_days": 59, "points": 1.25, "name": "Tier 5", "hebrew": "דרגה 5"},
    {"min_days": 50, "max_days": 54, "points": 1.00, "name": "Tier 4", "hebrew": "דרגה 4"},
    {"min_days": 40, "max_days": 49, "points": 0.75, "name": "Tier 3", "hebrew": "דרגה 3"},
    {"min_days": 30, "max_days": 39, "points": 0.50, "name": "Tier 2", "hebrew": "דרגה 2"},
]

# Standard credit for non-combat or under 30 combat days
STANDARD_CREDIT_POINTS = 1.0


def get_combat_credit_tier(days: int) -> dict:
    """Determine the combat credit tier based on days served."""
    for tier in COMBAT_CREDIT_TIERS:
        if tier["max_days"] is None:
            if days >= tier["min_days"]:
                return tier
        else:
            if tier["min_days"] <= days <= tier["max_days"]:
                return tier
    return None


def calculate_credits(days: int, monthly_income: float, is_combat: bool = True) -> dict:
    """
    Calculate tax credits and compensation eligibility.

    Returns a dictionary with all calculation details.
    """
    result = {
        "days": days,
        "monthly_income": monthly_income,
        "annual_income": monthly_income * 12,
        "is_combat": is_combat,
        "tier": None,
        "credit_points": STANDARD_CREDIT_POINTS,
        "annual_credit_value": STANDARD_CREDIT_POINTS * CREDIT_POINT_ANNUAL,
        "monthly_credit_value": STANDARD_CREDIT_POINTS * CREDIT_POINT_MONTHLY,
        "below_compensation_floor": False,
        "estimated_monthly_topup": 0,
        "total_annual_benefit": STANDARD_CREDIT_POINTS * CREDIT_POINT_ANNUAL,
    }

    if is_combat and days >= 30:
        tier = get_combat_credit_tier(days)
        if tier:
            result["tier"] = tier
            result["credit_points"] = tier["points"]
            result["annual_credit_value"] = tier["points"] * CREDIT_POINT_ANNUAL
            result["monthly_credit_value"] = tier["points"] * CREDIT_POINT_MONTHLY

    # Check minimum compensation floor
    if 0 < monthly_income < MIN_COMPENSATION_MONTHLY:
        result["below_compensation_floor"] = True
        result["estimated_monthly_topup"] = MIN_COMPENSATION_MONTHLY - monthly_income

    service_months = days / 30.0
    total_topup = result["estimated_monthly_topup"] * service_months if result["below_compensation_floor"] else 0
    result["total_annual_benefit"] = result["annual_credit_value"] + total_topup

    return result


def validate_inputs(days: int, monthly_income: float) -> list:
    """Validate input values and return list of error messages."""
    errors = []
    if days < 0:
        errors.append("Days served must be a non-negative number.")
    if days > 365:
        errors.append("Days served cannot exceed 365 in a single year.")
    if monthly_income < 0:
        errors.append("Monthly income must be a non-negative number.")
    return errors


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Calculate estimated miluim (reserve duty) tax credits based on "
            "combat days served and monthly income for the 2026-2027 tax years. "
            "Uses the 17-tier Amendment 283 system (Section 39B)."
        ),
        epilog=(
            "Examples:\n"
            "  python miluim-tax-credit-calculator.py --days 45 --monthly-income 15000\n"
            "  python miluim-tax-credit-calculator.py --days 120 --monthly-income 8000\n"
            "  python miluim-tax-credit-calculator.py --days 25 --monthly-income 20000\n"
            "  python miluim-tax-credit-calculator.py --days 60 --monthly-income 12000 --non-combat\n"
            "\n"
            "Note: Values are approximate. Consult Rashut HaMisim for exact rates.\n"
            "Combat credit tiers apply only to combat service days (yamei lochem)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--days",
        type=int,
        required=True,
        help="Number of reserve duty days served in the tax year",
    )
    parser.add_argument(
        "--monthly-income",
        type=float,
        required=True,
        help="Average monthly gross income in NIS",
    )
    parser.add_argument(
        "--non-combat",
        action="store_true",
        help="Flag for non-combat reserve service (standard 1.0 credit point)",
    )

    args = parser.parse_args()
    is_combat = not args.non_combat

    # Validate
    errors = validate_inputs(args.days, args.monthly_income)
    if errors:
        print("Input validation errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    # Calculate
    result = calculate_credits(args.days, args.monthly_income, is_combat)

    # Display results
    print("\n" + "=" * 60)
    print("  Miluim Tax Credit Calculator (2026-2027)")
    print("  מחשבון זיכוי מס מילואים (2026-2027)")
    print("  Amendment 283 / תיקון 283")
    print("=" * 60)

    print(f"\n  Input:")
    print(f"  Days served (ימי שירות):            {result['days']}")
    print(f"  Service type (סוג שירות):           {'Combat (לוחם)' if is_combat else 'Non-combat (לא לוחם)'}")
    print(f"  Monthly income (הכנסה חודשית):      {result['monthly_income']:,.0f} NIS")
    print(f"  Annual income (הכנסה שנתית):        {result['annual_income']:,.0f} NIS")

    # Credit tier display
    print(f"\n  Credit Tier Information:")
    print(f"  {'=' * 50}")

    if not is_combat:
        print(f"  Non-combat service: standard credit of {STANDARD_CREDIT_POINTS} point(s)")
        print(f"  Annual credit value: {STANDARD_CREDIT_POINTS * CREDIT_POINT_ANNUAL:,.0f} NIS")
    elif result["tier"] is None:
        print(f"  Combat days: {result['days']}")
        if result["days"] < 30:
            print(f"  Below 30-day threshold for combat credit tiers (2026-2027)")
            print(f"  Standard credit of {STANDARD_CREDIT_POINTS} point(s) applies")
            print(f"  Note: From 2028, threshold drops to 20 days")
        print(f"\n  All combat credit tiers (Amendment 283):")
        for tier in reversed(COMBAT_CREDIT_TIERS):
            max_str = f"-{tier['max_days']}" if tier['max_days'] else "+"
            print(f"    {tier['min_days']}{max_str} days: {tier['points']} points")
    else:
        tier = result["tier"]
        max_str = f"-{tier['max_days']}" if tier['max_days'] else "+"
        print(f"  Your tier: {tier['name']} ({tier['hebrew']})")
        print(f"  Days range: {tier['min_days']}{max_str}")
        print(f"  Credit points (nekudot zikui): {tier['points']}")

    print(f"\n  Tax Credit Calculation:")
    print(f"  {'=' * 50}")
    print(f"  Credit points: {result['credit_points']}")
    print(f"  Point value (monthly): {CREDIT_POINT_MONTHLY} NIS")
    print(f"  Point value (annual): {CREDIT_POINT_ANNUAL:,} NIS")
    print(f"  Annual credit value: {result['annual_credit_value']:,.0f} NIS")
    print(f"  Monthly credit value: {result['monthly_credit_value']:,.0f} NIS")

    # Compensation floor check
    print(f"\n  Minimum Compensation Check:")
    print(f"  {'=' * 50}")
    print(f"  Bituach Leumi floor: {MIN_COMPENSATION_MONTHLY:,} NIS/month ({MIN_COMPENSATION_DAILY} NIS/day)")

    if result["below_compensation_floor"]:
        service_months = result["days"] / 30.0
        print(f"  Status: BELOW FLOOR (income below {MIN_COMPENSATION_MONTHLY:,} NIS/month)")
        print(f"  Estimated monthly top-up: {result['estimated_monthly_topup']:,.0f} NIS")
        print(f"  Estimated service months: {service_months:.1f}")
        print(f"  Total estimated top-up: {result['estimated_monthly_topup'] * service_months:,.0f} NIS")
    elif result["monthly_income"] == 0:
        print(f"  Status: NO INCOME (full floor amount applies)")
    else:
        print(f"  Status: ABOVE FLOOR (no top-up needed)")

    # Total benefit summary
    print(f"\n  Total Estimated Annual Benefit:")
    print(f"  {'=' * 50}")
    print(f"  Tax credit:                          {result['annual_credit_value']:,.0f} NIS")
    if result["below_compensation_floor"]:
        service_months = result["days"] / 30.0
        total_topup = result["estimated_monthly_topup"] * service_months
        print(f"  Compensation top-up:                 {total_topup:,.0f} NIS")
    print(f"  Total benefit:                       {result['total_annual_benefit']:,.0f} NIS")

    # Next tier info (combat only)
    if is_combat and result["tier"] is not None and result["tier"]["max_days"] is not None:
        current_idx = COMBAT_CREDIT_TIERS.index(result["tier"])
        if current_idx > 0:
            next_tier = COMBAT_CREDIT_TIERS[current_idx - 1]
            additional_days = next_tier["min_days"] - result["days"]
            if additional_days > 0:
                additional_value = (next_tier["points"] - result["credit_points"]) * CREDIT_POINT_ANNUAL
                print(f"\n  Next Tier ({next_tier['name']}):")
                print(f"  {'=' * 50}")
                print(f"  {additional_days} more days needed to reach {next_tier['min_days']}-day tier")
                print(f"  Additional annual credit: +{additional_value:,.0f} NIS")

    # How to claim
    print(f"\n  How to Claim:")
    print(f"  {'=' * 50}")
    print(f"  1. Obtain service confirmation (ishur sherut miluim) from IDF")
    print(f"  2. Submit Form 101 (tofes 101) to employer")
    print(f"     OR file directly with Rashut HaMisim (Tax Authority)")
    print(f"  3. Credits applied to monthly payroll or as annual refund")
    print(f"  4. Self-employed: claim through annual tax filing")

    print(f"\n  DISCLAIMER (הערה חשובה):")
    print(f"  These calculations are estimates based on 2026 rates (frozen")
    print(f"  through 2027). Combat credit tiers apply ONLY to combat service")
    print(f"  days (yamei lochem) under Amendment 283 (Section 39B).")
    print(f"  Non-combat reserve service qualifies for standard 1.0 credit point.")
    print(f"  Consult a tax advisor or Rashut HaMisim for exact calculations.")
    print()


if __name__ == "__main__":
    main()
