#!/usr/bin/env python3
"""Estimate the post-discharge rent assistance for a recognized lone soldier.

Rule (hachvana SingleSolders/Rent): up to 1,000 NIS per month for up to 12
months of rent, capped at 12,000 NIS in the first year after discharge.
If the actual rent is below 1,000 NIS/month the reimbursement is the amount
actually paid, not the cap.
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


def estimate(discharge_date: date, rent_start: date, monthly_rent: int, rent_months: int = None) -> dict:
    if rent_start < discharge_date:
        raise ValueError("rent-start cannot be before discharge-date")
    if monthly_rent <= 0:
        raise ValueError("rent-monthly must be a positive number of NIS")
    if rent_months is not None and rent_months <= 0:
        raise ValueError("rent-months must be a positive number of months")
    window_end = discharge_date + timedelta(days=365)
    if rent_start > window_end:
        return {
            "eligible": False,
            "reason": "Rent start is after the 12-month post-discharge window, not eligible",
            "discharge_date": discharge_date.isoformat(),
            "window_end": window_end.isoformat(),
        }
    # Count whole CALENDAR months between rent_start and the end of the window.
    # A 30-day approximation silently loses a month on most real date pairs.
    months_to_year_end = (window_end.year - rent_start.year) * 12 + (window_end.month - rent_start.month)
    if window_end.day < rent_start.day:
        months_to_year_end -= 1
    months_to_year_end = max(0, months_to_year_end)
    eligible_months = min(MAX_MONTHS, months_to_year_end)
    # Only months actually paid under the lease can be reimbursed. Without a
    # lease length the estimate is an upper bound, not an entitlement.
    if rent_months is not None:
        eligible_months = min(eligible_months, rent_months)
    per_month_subsidy = min(monthly_rent, MAX_MONTHLY)
    estimate_total = min(ANNUAL_CAP, per_month_subsidy * eligible_months)
    # Installments can never exceed what is actually claimable: the first payment
    # covers at most 6 eligible rental months AND at most the whole estimate.
    first = min(FIRST_INSTALLMENT_MAX, per_month_subsidy * min(6, eligible_months), estimate_total)
    second = max(0, estimate_total - first)
    return {
        "eligible": True,
        "discharge_date": discharge_date.isoformat(),
        "rent_start": rent_start.isoformat(),
        "window_end": window_end.isoformat(),
        "monthly_rent_input": monthly_rent,
        "per_month_subsidy_nis": per_month_subsidy,
        "eligible_months": eligible_months,
        "assumed_full_window": rent_months is None,
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
    parser.add_argument(
        "--rent-months",
        type=int,
        default=None,
        help="Number of rental months actually paid (from the lease). Omit to assume the lease runs to the end of the window.",
    )
    args = parser.parse_args()

    try:
        d_date = parse_date(args.discharge_date)
        r_date = parse_date(args.rent_start)
        result = estimate(d_date, r_date, args.rent_monthly, args.rent_months)
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
    if result.get("assumed_full_window"):
        print("  NOTE: no --rent-months given, so this assumes the lease runs to the end of")
        print("        the window. With a shorter lease the real figure is lower.")
    print()
    print("Estimate only, not a determination of entitlement. The binding decision is the")
    print("Fund for the Absorption of Discharged Soldiers via hachvana. Verify on *5266.")
    print()
    print("Installments:")
    print(f"  First installment:        {result['first_installment_nis']} NIS (covers 6 months)")
    print(f"  Second installment:       {result['second_installment_nis']} NIS (within 4 months after first period ends)")
    print()
    print("Apply via the personal area at hachvana.mod.gov.il > Extra Benefits > Single Soldiers > Rent.")
    print("Required document (as of 01.07.2026): a declaration form signed by soldier + landlord; bank details are updated separately in the personal area. Keep the signed lease on hand for review.")
    print(
        "Model: this counts rental months that fall inside the first year after discharge, "
        "matching hachvana's wording (up to 12,000 NIS 'בשנה הראשונה לשחרור'). Registration "
        "must also happen in that first year. If the lease straddles the year boundary, "
        "confirm the treatment on *5266 rather than relying on this estimate."
    )
    print("Hotline: *5266")


if __name__ == "__main__":
    main()
