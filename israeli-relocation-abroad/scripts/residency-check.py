#!/usr/bin/env python3
"""Israeli tax residency quick check.

Walks through the days test and basic center-of-life questions, outputs
a status recommendation. Not a legal opinion -- always verify with a
qualified accountant (yo'etz mas) or consider requesting a formal ruling
from the Tax Authority.

Usage:
    python residency-check.py --days_this_year 120 --days_prev1 200 \\
        --days_prev2 180 --family_in_israel no --home_in_israel yes
"""
from __future__ import annotations

import argparse


def days_test(days_this_year: int, days_prev1: int, days_prev2: int) -> tuple[bool, str]:
    """Return (presumed_resident, reason)."""
    if days_this_year >= 183:
        return True, f"183-day rule triggered: {days_this_year} days in Israel this year"
    total_3y = days_this_year + days_prev1 + days_prev2
    if days_this_year >= 30 and total_3y >= 425:
        return True, f"30+425 rule triggered: {days_this_year} days this year + {total_3y} total over 3 years"
    return False, f"Days test not triggered: {days_this_year} this year, {total_3y} total over 3 years"


def center_of_life_score(args: argparse.Namespace) -> tuple[int, list[str]]:
    """Score center of life 0-5 toward Israel. Higher = more ties to Israel."""
    score = 0
    reasons = []
    if args.family_in_israel == "yes":
        score += 2
        reasons.append("Spouse and/or minor children in Israel (+2)")
    if args.home_in_israel == "yes":
        score += 1
        reasons.append("Owns or leases home in Israel (+1)")
    if args.employer in ("israeli", "israeli_parent_of_foreign_entity"):
        score += 1
        reasons.append("Employer is Israeli or Israeli-connected (+1)")
    if args.bank_accounts_main == "israeli":
        score += 1
        reasons.append("Primary bank accounts are Israeli (+1)")
    return score, reasons


def recommend(presumed: bool, col_score: int) -> str:
    if presumed and col_score >= 3:
        return (
            "LIKELY ISRAELI TAX RESIDENT. Days test triggered AND center of life leans Israel. "
            "Plan to file Israeli tax return and report worldwide income. Bituach Leumi continues."
        )
    if presumed and col_score < 3:
        return (
            "AMBIGUOUS. Days test triggered but center of life leans abroad. "
            "File Form 1348 (Residency Declaration) with your annual return to contest the presumption. "
            "Consider requesting a Tax Authority ruling. Consult an accountant before acting."
        )
    if not presumed and col_score >= 3:
        return (
            "AMBIGUOUS. Days test not triggered but center of life leans Israel. "
            "The Tax Authority may still consider you a resident based on ties. "
            "Document your situation carefully and consult an accountant."
        )
    return (
        "LIKELY NOT AN ISRAELI TAX RESIDENT. Neither the days test nor center of life points to Israel. "
        "Stop Bituach Leumi payments formally if you want to cut residency, or keep paying to preserve kupat cholim. "
        "Verify before the next tax year with an accountant."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days_this_year", type=int, required=True, help="Days physically in Israel this tax year")
    parser.add_argument("--days_prev1", type=int, default=0, help="Days in Israel last year")
    parser.add_argument("--days_prev2", type=int, default=0, help="Days in Israel 2 years ago")
    parser.add_argument("--family_in_israel", choices=["yes", "no"], default="no")
    parser.add_argument("--home_in_israel", choices=["yes", "no"], default="no")
    parser.add_argument(
        "--employer",
        choices=["israeli", "foreign", "self_employed", "israeli_parent_of_foreign_entity", "none"],
        default="foreign",
    )
    parser.add_argument("--bank_accounts_main", choices=["israeli", "foreign"], default="foreign")
    args = parser.parse_args()

    presumed, days_reason = days_test(args.days_this_year, args.days_prev1, args.days_prev2)
    col_score, col_reasons = center_of_life_score(args)

    print("=" * 60)
    print("Israeli Tax Residency Check")
    print("=" * 60)
    print()
    print("Days Test:")
    print(f"  {days_reason}")
    print(f"  Presumed resident by days test: {'YES' if presumed else 'NO'}")
    print()
    print("Center of Life Indicators:")
    for r in col_reasons:
        print(f"  {r}")
    print(f"  Center-of-life score toward Israel: {col_score} / 5")
    print()
    print("Recommendation:")
    print(f"  {recommend(presumed, col_score)}")
    print()
    print(
        "IMPORTANT: This script is a guidance tool only. Israeli tax residency is a fact-based "
        "determination by the Tax Authority. For any real decision, consult a qualified Israeli "
        "accountant (yo'etz mas) and consider a formal ruling (Pre-Ruling) from Rashut HaMisim."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
