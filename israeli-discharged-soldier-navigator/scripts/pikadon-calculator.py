#!/usr/bin/env python3
"""Estimate the Pikadon and discharge grant for a recently-discharged Israeli soldier.

Rates indexed to Feb 2026 values from hachvana.mod.gov.il/GrantAndDeposit/DepositUpTo5.
THE RATES CHANGE MONTHLY WITH CPI. Always verify the personalized amount against the
official calculator before any user makes financial plans.

Usage:
  python pikadon-calculator.py --service-type lochem --months 32 --gender male
  python pikadon-calculator.py --service-type tomech-lechima --months 30 --gender male
  python pikadon-calculator.py --service-type acher --months 24 --gender female
  python pikadon-calculator.py --service-type sle --months 18 --gender female
"""

import argparse
import sys

PIKADON_RATES_FEB_2026 = {
    "lochem": 978.34,
    "tomech-lechima": 815.28,
    "acher": 652.23,
    "sle": 652.23,
}

ACCRUAL_CAP = {"male": 32, "female": 28}

NEKUDOT_ZIKUI_VALUE_PER_POINT_PER_MONTH_2026 = 242


def compute_pikadon(service_type: str, months: int, gender: str) -> dict:
    if service_type not in PIKADON_RATES_FEB_2026:
        raise ValueError(f"Unknown service-type {service_type!r}. Valid: {list(PIKADON_RATES_FEB_2026)}")
    if gender not in ACCRUAL_CAP:
        raise ValueError(f"Unknown gender {gender!r}. Valid: male, female")
    if months < 0:
        raise ValueError("months must be non-negative")

    cap = ACCRUAL_CAP[gender]
    effective_months = min(months, cap)
    rate = PIKADON_RATES_FEB_2026[service_type]
    pikadon = effective_months * rate

    # Nekudot zikui thresholds differ by service population:
    #   Male IDF/MAGAV/Police/SHABAS: ≥23 months => 2 points
    #   Female IDF/MAGAV/Police/SHABAS: ≥22 months => 2 points
    #   SLE (any gender): ≥24 months => 2 points
    if service_type == "sle":
        points_per_year = 2 if months >= 24 else (1 if months >= 12 else 0)
    elif gender == "male":
        points_per_year = 2 if months >= 23 else (1 if months >= 12 else 0)
    else:
        points_per_year = 2 if months >= 22 else (1 if months >= 12 else 0)

    monthly_credit = NEKUDOT_ZIKUI_VALUE_PER_POINT_PER_MONTH_2026 * points_per_year
    total_36_months = monthly_credit * 36

    return {
        "service_type": service_type,
        "months_input": months,
        "months_effective": effective_months,
        "cap_applied": months > cap,
        "rate_per_month_nis": rate,
        "pikadon_estimate_nis": round(pikadon, 2),
        "nekudot_zikui_points_per_year": points_per_year,
        "nekudot_zikui_monthly_credit_nis": monthly_credit,
        "nekudot_zikui_total_over_36_months_nis": total_36_months,
        "note": "Rates indexed to Feb 2026; verify on hachvana.mod.gov.il official calculator before any financial decision.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--service-type", required=True, choices=list(PIKADON_RATES_FEB_2026.keys()))
    parser.add_argument("--months", required=True, type=int, help="Months of paid service")
    parser.add_argument("--gender", required=True, choices=["male", "female"])
    args = parser.parse_args()

    try:
        result = compute_pikadon(args.service_type, args.months, args.gender)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    print("Pikadon estimate (2026 indexed rates):")
    print(f"  Service type:                       {result['service_type']}")
    print(f"  Months input / effective:           {result['months_input']} / {result['months_effective']} (cap {ACCRUAL_CAP[args.gender]} for {args.gender})")
    if result["cap_applied"]:
        print(f"  NOTE: Months exceeded cap; extra service does not accrue Pikadon")
    print(f"  Rate per month:                     {result['rate_per_month_nis']} NIS")
    print(f"  Pikadon estimate:                   {result['pikadon_estimate_nis']:,.2f} NIS")
    print()
    print("Nekudot zikui (Section 39a) over 36 months from month after discharge:")
    print(f"  Points per year:                    {result['nekudot_zikui_points_per_year']}")
    print(f"  Monthly tax credit:                 {result['nekudot_zikui_monthly_credit_nis']} NIS")
    print(f"  Total over 36 months:               {result['nekudot_zikui_total_over_36_months_nis']:,} NIS")
    print()
    print("REMINDER:")
    print("  - Pikadon rates are indexed monthly to CPI. Verify on the official calculator")
    print("    at https://www.hachvana.mod.gov.il/GrantAndDeposit/DepositUpTo5/Pages/default.aspx")
    print("  - Nekudot zikui reduce tax owed but cannot exceed liability and do not refund as cash.")
    print("  - Submit Tofes 101 to employer + Teudat Shichrur to start receiving the credit.")
    print("  - If employer never applied: file Tofes 135 retroactive (up to 6 years back).")


if __name__ == "__main__":
    main()
