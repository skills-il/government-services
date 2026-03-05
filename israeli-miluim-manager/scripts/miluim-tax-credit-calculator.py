#!/usr/bin/env python3
"""
Miluim Tax Credit Calculator

Estimates tax credits for Israeli reserve duty (miluim) based on the
number of days served in a given tax year.

The 2026 tax year uses a 4-tier credit system:
  - 10-30 days:  Standard credit (1.0 credit point)
  - 31-60 days:  Enhanced credit (1.5 credit points)
  - 61-110 days: Higher credit (2.0 credit points)
  - 110+ days:   Maximum credit (2.5 credit points)

Additionally, reservists earning below NIS 9,800/month may qualify for
a monthly supplement of approximately NIS 3,000.

Usage:
    python scripts/miluim-tax-credit-calculator.py --days 45 --monthly-income 15000
    python scripts/miluim-tax-credit-calculator.py --days 120 --monthly-income 8000
    python scripts/miluim-tax-credit-calculator.py --days 25 --monthly-income 20000

Note: Tax credit point values are approximate and based on 2026 rates.
Consult Rashut HaMisim (Tax Authority) for exact values.
"""

import argparse
import sys


# 2026 Tax Credit Point Value (approximate)
# A single credit point (nekudat zikui) is worth approximately NIS 242/month
# or NIS 2,904/year (updated annually)
CREDIT_POINT_MONTHLY = 242
CREDIT_POINT_ANNUAL = CREDIT_POINT_MONTHLY * 12

# Monthly income threshold for supplement
SUPPLEMENT_THRESHOLD = 9800
SUPPLEMENT_AMOUNT = 3000

# Credit tiers based on days served
CREDIT_TIERS = [
    {"min_days": 110, "max_days": None, "points": 2.5, "name": "Maximum", "hebrew": "מקסימלי"},
    {"min_days": 61, "max_days": 110, "points": 2.0, "name": "Higher", "hebrew": "גבוה"},
    {"min_days": 31, "max_days": 60, "points": 1.5, "name": "Enhanced", "hebrew": "מוגבר"},
    {"min_days": 10, "max_days": 30, "points": 1.0, "name": "Standard", "hebrew": "סטנדרטי"},
]


def get_credit_tier(days: int) -> dict:
    """Determine the credit tier based on days served."""
    if days < 10:
        return None

    for tier in CREDIT_TIERS:
        if tier["max_days"] is None:
            if days >= tier["min_days"]:
                return tier
        else:
            if tier["min_days"] <= days <= tier["max_days"]:
                return tier

    return None


def calculate_credits(days: int, monthly_income: float) -> dict:
    """
    Calculate tax credits and supplement eligibility.

    Returns a dictionary with all calculation details.
    """
    tier = get_credit_tier(days)

    result = {
        "days": days,
        "monthly_income": monthly_income,
        "annual_income": monthly_income * 12,
        "tier": tier,
        "credit_points": 0,
        "annual_credit_value": 0,
        "monthly_credit_value": 0,
        "supplement_eligible": False,
        "monthly_supplement": 0,
        "total_annual_benefit": 0,
    }

    if tier is None:
        return result

    result["credit_points"] = tier["points"]
    result["annual_credit_value"] = tier["points"] * CREDIT_POINT_ANNUAL
    result["monthly_credit_value"] = tier["points"] * CREDIT_POINT_MONTHLY

    # Check supplement eligibility
    if monthly_income <= SUPPLEMENT_THRESHOLD and monthly_income > 0:
        result["supplement_eligible"] = True
        # Supplement is paid per month of active service
        # Approximate: days / 30 = months of service
        service_months = days / 30.0
        result["monthly_supplement"] = SUPPLEMENT_AMOUNT
        result["total_supplement"] = SUPPLEMENT_AMOUNT * service_months
    else:
        result["total_supplement"] = 0

    result["total_annual_benefit"] = result["annual_credit_value"] + result.get("total_supplement", 0)

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
            "days served and monthly income for the 2026 tax year."
        ),
        epilog=(
            "Examples:\n"
            "  python miluim-tax-credit-calculator.py --days 45 --monthly-income 15000\n"
            "  python miluim-tax-credit-calculator.py --days 120 --monthly-income 8000\n"
            "  python miluim-tax-credit-calculator.py --days 25 --monthly-income 20000\n"
            "\n"
            "Note: Values are approximate. Consult Rashut HaMisim for exact rates."
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

    args = parser.parse_args()

    # Validate
    errors = validate_inputs(args.days, args.monthly_income)
    if errors:
        print("Input validation errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    # Calculate
    result = calculate_credits(args.days, args.monthly_income)

    # Display results
    print("\n" + "=" * 60)
    print("  Miluim Tax Credit Calculator (2026)")
    print("  מחשבון זיכוי מס מילואים (2026)")
    print("=" * 60)

    print(f"\n  Input:")
    print(f"  Days served (ימי שירות):            {result['days']}")
    print(f"  Monthly income (הכנסה חודשית):      {result['monthly_income']:,.0f} NIS")
    print(f"  Annual income (הכנסה שנתית):        {result['annual_income']:,.0f} NIS")

    # Credit tier display
    print(f"\n  Credit Tier Information:")
    print(f"  {'=' * 50}")

    if result["tier"] is None:
        print(f"  No tax credit available for {result['days']} days.")
        print(f"  Minimum qualifying days: 10")
        print(f"\n  All credit tiers:")
        for tier in reversed(CREDIT_TIERS):
            max_str = f"-{tier['max_days']}" if tier['max_days'] else "+"
            print(f"    {tier['min_days']}{max_str} days: {tier['points']} points ({tier['name']})")
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

        # Supplement check
        print(f"\n  Monthly Supplement Check:")
        print(f"  {'=' * 50}")
        print(f"  Income threshold: {SUPPLEMENT_THRESHOLD:,} NIS/month")

        if result["supplement_eligible"]:
            service_months = result["days"] / 30.0
            print(f"  Status: ELIGIBLE (income below threshold)")
            print(f"  Monthly supplement: {SUPPLEMENT_AMOUNT:,} NIS")
            print(f"  Estimated service months: {service_months:.1f}")
            print(f"  Total supplement: {result['total_supplement']:,.0f} NIS")
        else:
            if result["monthly_income"] == 0:
                print(f"  Status: NOT ELIGIBLE (no income reported)")
            else:
                print(f"  Status: NOT ELIGIBLE (income above {SUPPLEMENT_THRESHOLD:,} NIS/month)")

        # Total benefit summary
        print(f"\n  Total Estimated Annual Benefit:")
        print(f"  {'=' * 50}")
        print(f"  Tax credit:                          {result['annual_credit_value']:,.0f} NIS")
        if result["supplement_eligible"]:
            print(f"  Monthly supplement:                  {result['total_supplement']:,.0f} NIS")
        print(f"  Total benefit:                       {result['total_annual_benefit']:,.0f} NIS")

        # Next tier info
        if result["tier"]["max_days"] is not None:
            next_tier = None
            for t in CREDIT_TIERS:
                if t["min_days"] == result["tier"]["max_days"] + 1 or (
                    result["tier"]["max_days"] is not None
                    and t["min_days"] > result["tier"]["min_days"]
                    and (next_tier is None or t["min_days"] < next_tier["min_days"])
                ):
                    next_tier = t
                    break

            if next_tier:
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
    print(f"  These calculations are estimates based on approximate 2026 rates.")
    print(f"  Credit point values and tier thresholds may be adjusted by")
    print(f"  Rashut HaMisim. Consult a tax advisor or the Tax Authority")
    print(f"  for exact calculations specific to your situation.")
    print()


if __name__ == "__main__":
    main()
