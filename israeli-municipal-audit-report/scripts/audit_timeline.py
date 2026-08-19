#!/usr/bin/env python3
"""Compute the statutory deadline chain for an Israeli municipal internal audit report.

Per sections 170C(a) to 170C(e) of the Municipalities Ordinance. Two fallback branches
lead to two different end dates, which is the most common source of error.

Usage:
  python3 audit_timeline.py --audited-year 2025
  python3 audit_timeline.py --audited-year 2025 --submitted 2026-03-15
"""
import argparse
from datetime import date

def add_months(d, n):
    y, m = divmod(d.month - 1 + n, 12)
    y += d.year
    m += 1
    day = min(d.day, [31,29 if y%4==0 and (y%100!=0 or y%400==0) else 28,
                      31,30,31,30,31,31,30,31,30,31][m-1])
    return date(y, m, day)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--audited-year", type=int, required=True,
                   help="the year the report covers")
    p.add_argument("--submitted",
                   help="actual submission date YYYY-MM-DD (defaults to the 1 April statutory latest)")
    a = p.parse_args()

    statutory = date(a.audited_year + 1, 4, 1)
    if a.submitted:
        y, m, d = (int(x) for x in a.submitted.split("-"))
        submitted = date(y, m, d)
    else:
        submitted = statutory

    print(f"Audited year         : {a.audited_year}")
    print(f"Statutory latest     : {statutory.isoformat()} (1 April of the following year)")
    print(f"Submission used      : {submitted.isoformat()}"
          + ("  LATE" if submitted > statutory else ""))
    print()
    print("Main chain")
    print(f"  Mayor comments to committee + copies to council   : {add_months(submitted,3).isoformat()}  (3 months)")
    print(f"  Committee conclusions to council                  : {add_months(submitted,5).isoformat()}  (2 months after that)")
    print(f"  Council special discussion                        : {add_months(submitted,7).isoformat()}  (2 months after that)")
    print()
    print("Fallback A, mayor does not comment in time")
    print(f"  Committee acts within 5 months of delivery to it  : {add_months(submitted,5).isoformat()}")
    print()
    print("Fallback B, committee does not submit or mayor does not circulate")
    print(f"  Auditor delivers to all council members, council")
    print(f"  discusses not later than 7 months from submission : {add_months(submitted,7).isoformat()}")
    print()
    print("Publication of the report, any part, or any finding is prohibited")
    print("before the date set for submission to the council.")

if __name__ == "__main__":
    main()
