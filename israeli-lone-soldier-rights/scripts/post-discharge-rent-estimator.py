#!/usr/bin/env python3
"""Estimate the post-discharge rent refund for a recognized lone soldier, one lease at a time.

Rules from hachvana SingleSolders/Rent (read 2026-10-07):
- Up to 1,000 NIS per month for up to 12 rental months, up to 12,000 NIS,
  in the first year after discharge. Below 1,000 NIS the refund is the rent
  actually paid. Rent only: arnona, electricity, gas and vaad bayit are not covered.
- Registration and the declaration form are filed in the first year after discharge.
- Two payments of up to 6,000 NIS, each for at most 6 rental months. The first
  covers the first 6 months OF THE LEASE; the second is requested no later than
  4 months after that first period ends.
- A lease that started during service is reimbursed only for the months after
  discharge (hachvana: lease from 1 January, discharge 1 March, 10 months).
- If fewer than 12 months were reimbursed, a completion request for the remainder
  is made via *5266 after the second payment.
- A new lease must start within 3 months of the previous one ending.
Kol Zchut: months lived in a Beit HaChayal after discharge (up to 3) are deducted
from the rent-assistance period.

Not published, and therefore NOT modelled (the output says so):
- proration of a lease month split by a mid-month discharge (left out here);
- treatment of lease months that fall after the first anniversary of discharge.

Usage:
  python post-discharge-rent-estimator.py --discharge-date 2026-03-15 --rent-start 2026-04-01 --rent-monthly 5000 --rent-months 12
"""

import argparse
import sys
from datetime import date, timedelta

MAX_MONTHLY = 1000  # NIS
MAX_MONTHS = 12
PERIOD_MONTHS = 6
MAX_BEIT_HACHAYAL_MONTHS = 3


def parse_date(s: str) -> date:
    parts = s.split("-")
    if len(parts) != 3:
        raise ValueError(f"date must be YYYY-MM-DD, got {s!r}")
    return date(int(parts[0]), int(parts[1]), int(parts[2]))


def add_months(d: date, n: int) -> date:
    """Same day-of-month n months later, clamped to the last day of a short month."""
    y, m = divmod(d.month - 1 + n, 12)
    year, month = d.year + y, m + 1
    day = d.day
    while True:
        try:
            return date(year, month, day)
        except ValueError:
            day -= 1


def estimate(discharge_date: date, rent_start: date, monthly_rent: int, rent_months: int = None,
             beit_hachayal_months: int = 0, already_reimbursed: int = 0, filing_date: date = None) -> dict:
    if monthly_rent <= 0:
        raise ValueError("rent-monthly must be a positive number of NIS")
    if rent_months is not None and rent_months <= 0:
        raise ValueError("rent-months must be a positive number of months")
    if not 0 <= beit_hachayal_months <= MAX_BEIT_HACHAYAL_MONTHS:
        raise ValueError("beit-hachayal-months must be between 0 and 3")
    if not 0 <= already_reimbursed <= MAX_MONTHS:
        raise ValueError("months-already-reimbursed must be between 0 and 12")
    first_year_end = add_months(discharge_date, 12)
    base = {"discharge_date": discharge_date.isoformat(), "window_end": first_year_end.isoformat()}
    # The first-year rule governs the FIRST registration and declaration. A second
    # payment or a move-related declaration may legitimately be filed in year 2.
    first_request = already_reimbursed == 0
    if first_request and filing_date is not None and filing_date >= first_year_end:
        return {**base, "eligible": False,
                "reason": "Filing date is after the first year from discharge; hachvana requires registration and the declaration in that year"}
    if first_request and rent_start >= first_year_end:
        return {**base, "eligible": False,
                "reason": "The lease starts after the first year from discharge, so it cannot be registered in that year"}

    lease_months = rent_months if rent_months is not None else MAX_MONTHS
    remaining = max(0, MAX_MONTHS - beit_hachayal_months - already_reimbursed)
    in_service = split = past_anniversary = beyond_two_periods = 0
    reimbursed = {1: 0, 2: 0}
    for k in range(lease_months):
        start, end = add_months(rent_start, k), add_months(rent_start, k + 1)
        if end <= discharge_date:
            in_service += 1
            continue
        if start < discharge_date:
            split += 1  # proration not published: left out
            continue
        if k >= 2 * PERIOD_MONTHS:
            beyond_two_periods += 1
            continue
        if remaining == 0:
            continue
        if start >= first_year_end:
            past_anniversary += 1
        reimbursed[1 if k < PERIOD_MONTHS else 2] += 1
        remaining -= 1

    per_month = min(monthly_rent, MAX_MONTHLY)
    months = reimbursed[1] + reimbursed[2]
    entitlement = max(0, MAX_MONTHS - beit_hachayal_months - already_reimbursed)
    return {
        **base,
        "eligible": True,
        "rent_start": rent_start.isoformat(),
        "monthly_rent_input": monthly_rent,
        "per_month_subsidy_nis": per_month,
        "lease_months": lease_months,
        "assumed_full_lease": rent_months is None,
        "in_service_months": in_service,
        "split_months": split,
        "beit_hachayal_months": beit_hachayal_months,
        "already_reimbursed": already_reimbursed,
        "entitlement_months": entitlement,
        "eligible_months": months,
        "estimated_total_nis": per_month * months,
        "first_installment_nis": per_month * reimbursed[1],
        "first_installment_months": reimbursed[1],
        "second_installment_nis": per_month * reimbursed[2],
        "second_installment_months": reimbursed[2],
        "second_request_deadline": (add_months(rent_start, PERIOD_MONTHS + 4) - timedelta(days=1)).isoformat(),
        "lease_ends_in_window": lease_months < MAX_MONTHS,
        "last_filing_day": (first_year_end - timedelta(days=1)).isoformat(),
        "past_anniversary_months": past_anniversary,
        "beyond_two_periods": beyond_two_periods,
        "remaining_months_for_completion": max(0, entitlement - months),
        "filing_checked": filing_date is not None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--discharge-date", required=True, help="YYYY-MM-DD end of mandatory service")
    parser.add_argument("--rent-start", required=True, help="YYYY-MM-DD when the lease begins (may be before discharge)")
    parser.add_argument("--rent-monthly", required=True, type=int, help="Monthly rent in NIS")
    parser.add_argument("--rent-months", type=int, default=None,
                        help="Lease length in months, as declared. Omit to assume 12.")
    parser.add_argument("--beit-hachayal-months", type=int, default=0,
                        help="Months lived free in a Beit HaChayal after discharge (0-3); deducted from the rent period.")
    parser.add_argument("--months-already-reimbursed", type=int, default=0,
                        help="Months already refunded under an earlier lease (after a move).")
    parser.add_argument("--filing-date", default=None,
                        help="YYYY-MM-DD of the FIRST registration and declaration (checked against the first year).")
    args = parser.parse_args()

    try:
        result = estimate(parse_date(args.discharge_date), parse_date(args.rent_start), args.rent_monthly,
                          args.rent_months, args.beit_hachayal_months, args.months_already_reimbursed,
                          parse_date(args.filing_date) if args.filing_date else None)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    if not result["eligible"]:
        print(f"NOT ELIGIBLE: {result['reason']}")
        print(f"Discharge date:    {result['discharge_date']}")
        print(f"First year ends:   {result['window_end']}")
        sys.exit(1)

    r = result
    print("Post-discharge rent refund estimate for this lease (hachvana):")
    print(f"  Discharge date:            {r['discharge_date']}")
    print(f"  Lease start:               {r['rent_start']}")
    print(f"  Register and file by:      {r['last_filing_day']} (first year)"
          + ("" if r["filing_checked"] else ", pass --filing-date to check"))
    print(f"  Monthly rent:              {r['monthly_rent_input']} NIS")
    print(f"  Per-month refund:          {r['per_month_subsidy_nis']} NIS (capped at 1,000)")
    print(f"  Lease months:              {r['lease_months']}" + (" (assumed, pass --rent-months)" if r["assumed_full_lease"] else ""))
    if r["in_service_months"]:
        print(f"  Lease months in service:   {r['in_service_months']} (not refunded)")
    if r["split_months"]:
        print(f"  Month split by discharge:  {r['split_months']} (proration not published, left out; ask *5266)")
    if r["beit_hachayal_months"] or r["already_reimbursed"]:
        print(f"  Remaining entitlement:     {r['entitlement_months']} months"
              f" (12 minus {r['beit_hachayal_months']} Beit HaChayal, minus {r['already_reimbursed']} already refunded)")
    print(f"  Refunded months:           {r['eligible_months']}")
    print(f"  Estimated total:           {r['estimated_total_nis']} NIS")
    print()
    if r["entitlement_months"] == 0:
        print("  The 12-month entitlement is already used up (Beit HaChayal and earlier refunds).")
    elif r["eligible_months"] == 0:
        print("  This lease gives no refundable months under the published rules. Ask *5266.")
    elif r["already_reimbursed"]:
        print(f"  Refund for this lease:     {r['estimated_total_nis']} NIS ({r['eligible_months']} months)")
        print("  NOTE: after a move, hachvana has you upload a new declaration under the benefit year")
        print("        of your FIRST request; if you moved at the second-payment stage, it is your second")
        print("        payment, still due within 4 months of the end of the ORIGINAL first period. The new")
        print("        lease must start within 3 months of the previous one ending. Confirm on *5266.")
    elif r["first_installment_months"] == 0:
        print(f"  Refund:                    {r['second_installment_nis']} NIS, all in lease months 7-12"
              f" ({r['second_installment_months']} months)")
        print("  No first payment exists for this lease. hachvana: when the request is filed after the")
        print("  first 6 lease months have passed, file now and call *5266. The first-year registration rule still applies.")
    else:
        print(f"  First payment:             {r['first_installment_nis']} NIS"
              f" (refundable months among lease months 1-6: {r['first_installment_months']})")
        if r["second_installment_months"]:
            print(f"  Second payment:            {r['second_installment_nis']} NIS"
                  f" (lease months 7-12: {r['second_installment_months']}); request by {r['second_request_deadline']}")
    if r["past_anniversary_months"]:
        print(f"  NOTE: {r['past_anniversary_months']} of these months fall after the first anniversary of discharge.")
        print("        hachvana does not say how those are treated; confirm on *5266.")
    if r["beyond_two_periods"]:
        print(f"  NOTE: {r['beyond_two_periods']} lease month(s) past the 12th are outside the two payments.")
    if r["remaining_months_for_completion"] and r["eligible_months"]:
        print()
        print(f"  {r['remaining_months_for_completion']} month(s) of entitlement are not refunded under this estimate.")
        print("  hachvana: right after the second payment, call *5266 about a completion request (בקשת השלמה).")
        if not r["second_installment_months"]:
            print("  This lease has no second payment, so ask *5266 when to file it.")
        if r["lease_ends_in_window"]:
            print("  A following lease must start within 3 months of this one ending.")
    print()
    print("Estimate only, not a determination of entitlement. The binding decision is")
    print("hachvana (the Fund for the Absorption of Discharged Soldiers). Rent only: arnona,")
    print("electricity, gas and vaad bayit are not covered. Required document since 01.07.2026:")
    print("a declaration form signed by the soldier and the landlord. Hotline: *5266")


if __name__ == "__main__":
    main()
