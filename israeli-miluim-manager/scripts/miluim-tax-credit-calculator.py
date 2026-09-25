#!/usr/bin/env python3
"""
Miluim Tax Credit Calculator

Estimates tax credits for Israeli combat reserve duty (miluim) based on
the number of combat service days in a given tax year.

Amendment 283 to the Income Tax Ordinance (Section 39B), effective
January 1, 2026, introduced a 15-tier graduated credit system for
combat reservists (lochamim) for tax years 2026-2027:

  - Under 30 days, or non-combat: no Amendment 283 credit (0)
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

From tax year 2028 (that is, for combat service in 2027 onward) the
permanent rule in Section 39B(a)(1)-(2) applies instead: 20+ days = 0.75
points, plus 0.25 per additional 5 days beyond 20, capped at 4 points
(reached at 85 days). The table is selected by the SERVICE year: service
in year Y is credited in tax year Y+1. Service in 2024 or earlier earns no
Section 39B credit, because the section first applies to tax year 2026.

IMPORTANT: These tiers apply to COMBAT service days only. Non-combat
reserve service does NOT qualify for an Amendment 283 credit (0). The universal 2.25
resident credit points apply to everyone regardless of service.

Separately, Bituach Leumi never pays reserve tagmul below its daily floor
(NIS 328.76/day in 2026, about NIS 9,863/month), so a low earner's daily
tagmul is lifted to the floor. This script does NOT estimate reserve pay itself.

Usage:
    python scripts/miluim-tax-credit-calculator.py --days 45 --monthly-income 15000
    python scripts/miluim-tax-credit-calculator.py --days 120 --monthly-income 8000
    python scripts/miluim-tax-credit-calculator.py --days 25 --monthly-income 20000
    python scripts/miluim-tax-credit-calculator.py --days 25 --monthly-income 20000 --service-year 2027

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
# Lower minimum for a working youth (נער עובד): 25% of the average wage / 30
MIN_COMPENSATION_DAILY_WORKING_YOUTH = 114.73

# Amendment 283 combat credit tiers (Section 39B)
# Temporary table: tax years 2026-2027 (service 2025-2026), minimum 30 days
# From tax year 2028 (service 2027+) the permanent 20-day rule applies instead
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

# Permanent rule, Section 39B(a)(1)-(2), from tax year 2028 (service year 2027+):
# 20+ days = 0.75 point, +0.25 per additional 5 days beyond 20, capped at 4.
PERMANENT_MIN_DAYS = 20
PERMANENT_BASE_POINTS = 0.75
MAX_POINTS = 4.0

# Service years whose credit falls in a tax year covered by the 2026-2027
# temporary table (service 2025 -> tax 2026, service 2026 -> tax 2027).
TEMPORARY_SERVICE_YEARS = (2025, 2026)
FIRST_SERVICE_YEAR = 2025  # Section 39B first applies to tax year 2026

# No Amendment 283 credit for non-combat or under 30 combat days (the credit starts at 30
# combat days; the universal 2.25 resident points are separate and not modeled here).
STANDARD_CREDIT_POINTS = 0.0


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


def permanent_rule_tier(days: int) -> dict:
    """Section 39B permanent rule (tax year 2028 onward, i.e. service year 2027+)."""
    if days < PERMANENT_MIN_DAYS:
        return None
    extra_blocks = (days - PERMANENT_MIN_DAYS) // 5
    points = min(MAX_POINTS, PERMANENT_BASE_POINTS + 0.25 * extra_blocks)
    if points >= MAX_POINTS:
        return {"min_days": 85, "max_days": None, "points": MAX_POINTS,
                "name": "Maximum (permanent rule)", "hebrew": "מקסימלי (הסדר הקבע)"}
    low = PERMANENT_MIN_DAYS + 5 * extra_blocks
    return {"min_days": low, "max_days": low + 4, "points": points,
            "name": "Permanent rule", "hebrew": "הסדר הקבע"}


def calculate_credits(days: int, monthly_income: float, is_combat: bool = True,
                      service_year: int = 2026) -> dict:
    """
    Calculate tax credits and compensation eligibility.

    Returns a dictionary with all calculation details.
    """
    result = {
        "days": days,
        "monthly_income": monthly_income,
        "annual_income": monthly_income * 12,
        "is_combat": is_combat,
        "service_year": service_year,
        "tax_year": service_year + 1,
        "rule": None,
        "tier": None,
        "credit_points": STANDARD_CREDIT_POINTS,
        "annual_credit_value": STANDARD_CREDIT_POINTS * CREDIT_POINT_ANNUAL,
        "monthly_credit_value": STANDARD_CREDIT_POINTS * CREDIT_POINT_MONTHLY,
        "below_compensation_floor": False,
        "estimated_monthly_topup": 0,
        "total_annual_benefit": STANDARD_CREDIT_POINTS * CREDIT_POINT_ANNUAL,
    }

    if service_year < FIRST_SERVICE_YEAR:
        result["rule"] = "none"
    elif service_year in TEMPORARY_SERVICE_YEARS:
        result["rule"] = "temporary"
    else:
        result["rule"] = "permanent"

    tier = None
    if is_combat and result["rule"] == "temporary" and days >= 30:
        tier = get_combat_credit_tier(days)
    elif is_combat and result["rule"] == "permanent":
        tier = permanent_rule_tier(days)
    if tier:
        result["tier"] = tier
        result["credit_points"] = tier["points"]
        result["annual_credit_value"] = tier["points"] * CREDIT_POINT_ANNUAL
        result["monthly_credit_value"] = tier["points"] * CREDIT_POINT_MONTHLY

    # Flag, do NOT quantify, the tagmul floor.
    # The floor is on the DAILY TAGMUL, not a monthly income top-up. BTL applies it
    # to every basis ("לא פחות ממינימום = 328.76 ש"ח ליום" for monthly, daily and
    # hourly employees alike), so a working low earner is lifted to it, and someone
    # not working gets it directly. See references/btl-payment-rules.md section 1.
    # An earlier version multiplied the gap by the service months and added the
    # product to the credit value. That produced a shekel figure that does not exist,
    # and summed a next-tax-year credit with a this-year pay estimate. Removed.
    if monthly_income == 0:
        result["no_income"] = True
        result["floor_note"] = (
            "No reported income: someone not working (including a student) is paid the "
            "daily floor directly. This script does not estimate reserve pay."
        )
    elif monthly_income < MIN_COMPENSATION_MONTHLY:
        result["below_compensation_floor"] = True
        result["floor_note"] = (
            "Reported income is below the tagmul floor, so BTL would pay the daily "
            "tagmul at the floor rather than at the lower wage basis. This script does "
            "not estimate reserve pay. See references/btl-payment-rules.md section 1."
        )

    # Deliberately no combined total: the Amendment 283 credit lands in the tax year
    # AFTER the service year, while reserve pay is paid during or shortly after the
    # service. Summing them into one headline figure misrepresents both.
    result["annual_credit_value_note"] = (
        "Credit applies in the tax year following the service year."
    )

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
            "combat days served and monthly income. Uses the 15-tier Amendment 283 "
            "temporary table (Section 39B) for service in 2025-2026, and the "
            "permanent 20-day rule for service from 2027."
        ),
        epilog=(
            "Examples:\n"
            "  python miluim-tax-credit-calculator.py --days 45 --monthly-income 15000\n"
            "  python miluim-tax-credit-calculator.py --days 120 --monthly-income 8000\n"
            "  python miluim-tax-credit-calculator.py --days 25 --monthly-income 20000\n"
            "  python miluim-tax-credit-calculator.py --days 60 --monthly-income 12000 --non-combat\n"
            "  python miluim-tax-credit-calculator.py --days 25 --monthly-income 15000 --service-year 2027\n"
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
        help="Number of combat reserve days served in the service year (see --service-year)",
    )
    parser.add_argument(
        "--monthly-income",
        type=float,
        required=True,
        help="Average monthly gross income in NIS",
    )
    parser.add_argument(
        "--service-year",
        type=int,
        default=2026,
        help=(
            "Calendar year in which the combat days were served (default 2026). "
            "The credit lands in the FOLLOWING tax year. 2025-2026 use the "
            "30-day temporary table; 2027 onward use the permanent 20-day rule; "
            "2024 or earlier earn no Section 39B credit."
        ),
    )
    parser.add_argument(
        "--non-combat",
        action="store_true",
        help="Flag for non-combat reserve service (no Amendment 283 credit: 0 points)",
    )

    args = parser.parse_args()
    is_combat = not args.non_combat

    # Validate
    errors = validate_inputs(args.days, args.monthly_income)
    if args.service_year < 2000 or args.service_year > 2100:
        errors.append("Service year must be a calendar year such as 2026.")
    if errors:
        print("Input validation errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    # Calculate
    result = calculate_credits(args.days, args.monthly_income, is_combat, args.service_year)

    # Display results
    print("\n" + "=" * 60)
    print("  Miluim Tax Credit Calculator")
    print("  מחשבון זיכוי מס מילואים")
    print("  Amendment 283 / תיקון 283")
    print("=" * 60)

    print(f"\n  Input:")
    print(f"  Days served (ימי שירות):            {result['days']}")
    print(f"  Service year (שנת השירות):          {result['service_year']}")
    print(f"  Credited in tax year (שנת הזיכוי):  {result['tax_year']}")
    print(f"  Service type (סוג שירות):           {'Combat (לוחם)' if is_combat else 'Non-combat (לא לוחם)'}")
    print(f"  Monthly income (הכנסה חודשית):      {result['monthly_income']:,.0f} NIS")
    print(f"  Annual income (הכנסה שנתית):        {result['annual_income']:,.0f} NIS")

    # Credit tier display
    print(f"\n  Credit Tier Information:")
    print(f"  {'=' * 50}")

    if result["rule"] == "none":
        print(f"  Service in {result['service_year']} earns NO Section 39B credit:")
        print(f"  the section first applies to tax year 2026 (service in 2025).")
    elif not is_combat:
        print(f"  Non-combat service: standard credit of {STANDARD_CREDIT_POINTS} point(s)")
        print(f"  Annual credit value: {STANDARD_CREDIT_POINTS * CREDIT_POINT_ANNUAL:,.0f} NIS")
    elif result["tier"] is None and result["rule"] == "permanent":
        print(f"  Combat days: {result['days']}")
        print(f"  Below the 20-day threshold of the permanent rule (service 2027+)")
    elif result["tier"] is None:
        print(f"  Combat days: {result['days']}")
        if result["days"] < 30:
            print(f"  Below 30-day threshold of the temporary table (service 2025-2026)")
            print(f"  No Section 39B credit (there is no 'standard reservist' point)")
            print(f"  Note: for service from 2027 (tax year 2028) the threshold is 20 days")
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
    if result["tax_year"] >= 2028:
        print(f"  NOTE: {CREDIT_POINT_ANNUAL:,} is the value frozen for 2024-2027. The")
        print(f"        tax-year {result['tax_year']} point value is not yet published, so")
        print(f"        the shekel figures below are an estimate at the 2027 value.")
    print(f"  Annual credit value: {result['annual_credit_value']:,.0f} NIS")
    print(f"  Monthly credit value: {result['monthly_credit_value']:,.0f} NIS")

    # Tagmul floor: flag only, never quantify.
    print(f"\n  Reserve-Pay Floor (informational, NOT calculated here):")
    print(f"  {'=' * 50}")
    print(f"  Bituach Leumi daily floor: {MIN_COMPENSATION_DAILY} NIS/day ({MIN_COMPENSATION_MONTHLY:,} NIS/month)")
    if result.get("no_income"):
        print(f"  No income reported. Someone not working, including a student, is")
        print(f"  paid the floor of {MIN_COMPENSATION_DAILY} NIS/day directly.")
    elif result["below_compensation_floor"]:
        print(f"  Reported income is below that floor. BTL pays the daily tagmul")
        print(f"  at no less than the floor, for employees and the self-employed alike,")
        print(f"  so the wage-based figure is lifted to {MIN_COMPENSATION_DAILY} NIS/day.")
        print(f"  Exceptions that use a DIFFERENT basis (stopped work or left keva within")
        print(f"  60 days, unemployment benefit above the floor) are in")
        print(f"  references/btl-payment-rules.md section 1. This script does NOT estimate reserve pay.")
    else:
        print(f"  Reported income is at or above the floor.")
    print(f"  (A working youth, נער עובד, has a lower minimum of {MIN_COMPENSATION_DAILY_WORKING_YOUTH} NIS/day.)")

    # Amendment 283 credit only. Deliberately NOT summed with reserve pay:
    # the credit lands in the tax year AFTER the service year, whereas reserve
    # pay arrives during or shortly after the service. They are not commensurable.
    print(f"\n  Amendment 283 Credit (this is the ONLY figure this script computes):")
    print(f"  {'=' * 50}")
    print(f"  Annual credit value:                 {result['annual_credit_value']:,.0f} NIS")
    print(f"  Applies in the tax year AFTER the service year.")

    # Next tier info (combat only)
    if (is_combat and result["rule"] == "temporary" and result["tier"] is not None
            and result["tier"]["max_days"] is not None):
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
    print(f"  NOTE: the credit is given in the tax year AFTER the service year.")
    print(f"        Service in {result['service_year']} credits in {result['tax_year']}.")
    print(f"  1. Obtain BOTH the service confirmation (ishur sherut miluim)")
    print(f"     AND the combat confirmation (ishur lochem) from the IDF.")
    print(f"     A claim without the ishur lochem is rejected.")
    print(f"  2. Submit Form 101 (tofes 101, part het section 16) to employer")
    print(f"     OR file directly with Rashut HaMisim (Tax Authority)")
    print(f"  3. Credits applied to monthly payroll or as annual refund")
    print(f"  4. Self-employed: claim through annual tax filing")

    print(f"\n  DISCLAIMER (הערה חשובה):")
    print(f"  These calculations are estimates at the 2026 point value (frozen")
    print(f"  through 2027). Combat credit tiers apply ONLY to combat service")
    print(f"  days (yamei lochem) under Amendment 283 (Section 39B).")
    print("  Non-combat reserve service earns NO Amendment 283 credit (0 points).")
    print(f"  Consult a tax advisor or Rashut HaMisim for exact calculations.")
    print()


if __name__ == "__main__":
    main()
