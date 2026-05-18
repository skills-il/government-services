#!/usr/bin/env python3
"""Estimate the post-discharge rent assistance for a recognized lone soldier.

Rule (hachvana SingleSolders/Rent): up to 1,000 NIS per month for up to 12
months of rent, capped at 12,000 NIS in the first year after discharge.
Two installments: first up to 6,000 NIS covers 6 months; second up to
6,000 NIS submitted within 4 months after the first period ends.

Usage:
  python post-discharge-rent-estimator.py --discharge-date 2026-03-15 --rent-start 2026-04-01 --rent-monthly 5000
"""

import argparse
import sys
from datetime import date, timedelta

MAX_MONTHLY = 1000  # NIS
MAX_MONTHS = 12
ANNUAL_CAP = 12000
FIRST_INSTALLMENT_MAX = 6000


def parse_date(s: str) -> date:
    parts = s.split("-")
    if len(parts) != 3:
        raise ValueError(f"date must be YYYY-MM-DD, got {s!r}")
    return date(int(parts[0]), int(parts[1]), int(parts[2]))


def estimate(discharge_date: date, rent_start: date, monthly_rent: int) -> dict:
    if rent_start < discharge_date:
        raise ValueError("rent-start cannot be before discharge-date")
    window_end = discharge_date + timedelta(days=365)
    if rent_start > window_end:
        return {
            "eligible": False,
            "reason": "Rent start is after the 12-month post-discharge window, not eligible",
            "discharge_date": discharge_date.isoformat(),
            "window_end": window_end.isoformat(),
        }
    months_to_year_end = (window_end - rent_start).days // 30
    eligible_months = min(MAX_MONTHS, months_to_year_end)
    per_month_subsidy = min(monthly_rent, MAX_MONTHLY)
    estimate_total = min(ANNUAL_CAP, per_month_subsidy * eligible_months)
    first = min(FIRST_INSTALLMENT_MAX, per_month_subsidy * 6)
    second = max(0, estimate_total - first)
    return {
        "eligible": True,
        "discharge_date": discharge_date.isoformat(),
        "rent_start": rent_start.isoformat(),
        "window_end": window_end.isoformat(),
        "monthly_rent_input": monthly_rent,
        "per_month_subsidy_nis": per_month_subsidy,
        "eligible_months": eligible_months,
        "estimated_total_nis": estimate_total,
        "first_installment_nis": first,
        "second_installment_nis": second,
        "note": (
            "Up to 1,000 NIS/month for up to 12 months, capped at 12,000 NIS first year. "
            "Two installments per hachvana SingleSolders/Rent. Apply via personal area at hachvana.mod.gov.il."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--discharge-date", required=True, help="YYYY-MM-DD end of mandatory service")
    parser.add_argument("--rent-start", required=True, help="YYYY-MM-DD when rental period begins")
    parser.add_argument("--rent-monthly", required=True, type=int, help="Monthly rent in NIS")
    args = parser.parse_args()

    try:
        d_date = parse_date(args.discharge_date)
        r_date = parse_date(args.rent_start)
        result = estimate(d_date, r_date, args.rent_monthly)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    if not result["eligible"]:
        print(f"NOT ELIGIBLE: {result['reason']}")
        print(f"Discharge date:    {result['discharge_date']}")
        print(f"12-month window:   ends {result['window_end']}")
        sys.exit(1)

    print("Post-discharge rent assistance estimate (hachvana):")
    print(f"  Discharge date:           {result['discharge_date']}")
    print(f"  Rent start:               {result['rent_start']}")
    print(f"  12-month window ends:     {result['window_end']}")
    print(f"  Monthly rent:             {result['monthly_rent_input']} NIS")
    print(f"  Per-month subsidy:        {result['per_month_subsidy_nis']} NIS (capped at 1,000)")
    print(f"  Eligible months:          {result['eligible_months']}")
    print(f"  Estimated total:          {result['estimated_total_nis']} NIS (annual cap 12,000)")
    print()
    print("Installments:")
    print(f"  First installment:        {result['first_installment_nis']} NIS (covers 6 months)")
    print(f"  Second installment:       {result['second_installment_nis']} NIS (within 4 months after first period ends)")
    print()
    print("Apply via the personal area at hachvana.mod.gov.il > Extra Benefits > Single Soldiers > Rent.")
    print("Required documents: signed lease, bank account authorization, declaration form.")
    print("Hotline: *5266")


if __name__ == "__main__":
    main()
