#!/usr/bin/env python3
"""Estimate a monthly Bituach Leumi survivor benefit for Israel.

ESTIMATE ONLY. This is a rough, educational estimate. It is NOT an official
determination and it does NOT decide eligibility. The real amount depends on the
qualifying (akhshara) period, the exact family status, the income test, and other
factors that only Bituach Leumi checks. Always verify with the official calculator
and file a claim:
  https://www.btl.gov.il/Simulators/Pages/SherimCalc.aspx
  https://www.btl.gov.il/benefits/Survivors_%20Insurance/Pages/default.aspx

All constants are the figures published by Bituach Leumi effective 01.01.2026.
They are re-indexed every 1 January, so re-verify before relying on a number.
Every constant below is sourced and dated and matches evidence.json exactly.

Usage examples:
  python3 estimate_survivor_allowance.py --age 52 --orphans 0
  python3 estimate_survivor_allowance.py --age 45 --orphans 2 --seniority-years 20
  python3 estimate_survivor_allowance.py --age 48 --orphans 1 --work-related --wage 14000
  python3 estimate_survivor_allowance.py --age 34 --orphans 0 --exception-eligible
  python3 estimate_survivor_allowance.py --example
  python3 estimate_survivor_allowance.py --help
"""

import argparse
import sys

# --- Survivor's allowance base amounts (NIS/month), effective 01.01.2026 ---
# Source: https://www.btl.gov.il/benefits/Survivors_%20Insurance/shiuraihakizba/Pages/k.almanim.aspx
WIDOW_40_50_NO_CHILDREN = 1381   # "לאלמן/ה בגיל 50-40 בלי ילדים 1,381 ש\"ח"
WIDOW_50_PLUS_NO_CHILDREN = 1838  # "לאלמן/ה בגיל 50 ומעלה בלי ילדים 1,838 ש\"ח"
WIDOW_80_PLUS = 1941             # "לאלמן/ה בגיל 80 ומעלה 1,941 ש\"ח"
WIDOW_ONE_CHILD = 2700          # "לאלמן/ה עם ילד אחד 2,700 ש\"ח"
WIDOW_TWO_CHILDREN = 3562       # "לאלמן/ה עם שני ילדים 3,562 ש\"ח"
EACH_ADDITIONAL_CHILD = 862     # "לכל ילד נוסף 862 ש\"ח" (no cap on number of children)

# --- Seniority increment (תוספת ותק) ---
# Source: https://www.btl.gov.il/benefits/Survivors_%20Insurance/shiuraihakizba/Pages/vetek.aspx
# "2% עבור כל שנת ביטוח" since Jan 2019; "מקסימום ... 50% מהקצבה"
SENIORITY_RATE_PER_YEAR = 0.02
SENIORITY_MAX_RATE = 0.50

# --- Dependents' allowance (work-related death), effective 01.01.2026 ---
# Source: btl Work_Injury dependents "שיעורי הקצבה" page.
# Base = full (100%) work-disability pension = 75% of the deceased's determining wage.
# "קצבת נכות מעבודה מלאה מחושבת לפי 75% מהשכר"
WORK_DISABILITY_WAGE_RATE = 0.75
# "מקסימום קצבת נכות מעבודה - 39,428 ש\"ח (החל ב- 01.01.2026)"
MAX_WORK_DISABILITY_PENSION = 39428
# Widow(er) WITH children: percentages of the full work-disability pension.
DEP_WIDOW_1_CHILD = 0.80   # "אלמן/ה + ילד אחד 80%"
DEP_WIDOW_2_CHILDREN = 0.90  # "אלמן/ה + 2 ילדים 90%"
DEP_WIDOW_3PLUS_CHILDREN = 1.00  # "אלמן/ה + 3 ילדים ויותר 100%"
# Widow(er) WITHOUT children, by age.
DEP_WIDOW_40_50 = 0.40    # "50-40 שנה 40%"
DEP_WIDOW_50_PLUS = 0.60  # "50 שנה ומעלה 60%"


def estimate_ordinary(age, orphans, seniority_years, exception_eligible=False):
    """Ordinary survivor's allowance (non-work-related death)."""
    caveats = []

    if orphans >= 1:
        if orphans == 1:
            base = WIDOW_ONE_CHILD
        elif orphans == 2:
            base = WIDOW_TWO_CHILDREN
        else:
            base = WIDOW_TWO_CHILDREN + EACH_ADDITIONAL_CHILD * (orphans - 2)
        basis = "widow(er) with %d child(ren)" % orphans
    else:
        if age < 40:
            if exception_eligible:
                # Under-40 childless is NOT always a grant. A monthly allowance is paid if she is
                # pregnant with / later bears the deceased's child (then treated as a widow with a
                # child, entitled from the date of death), or, in the work-injury track, was unable
                # to support herself from work at the time of death (paid as if aged 50). Here we
                # estimate the "as if aged 50" childless base.
                base = WIDOW_50_PLUS_NO_CHILDREN
                basis = "widow(er) under 40, no children, EXCEPTION case (paid as if aged 50)"
                caveats.append(
                    "Under-40 childless EXCEPTION case: a monthly allowance is paid (not the "
                    "one-time grant) because an exception applies (pregnant with / bearing the "
                    "deceased's child, or, in the work-injury track, unable to support herself "
                    "from work). Treated as if aged 50. If she has the deceased's child, use "
                    "the orphans count instead. Verify with Bituach Leumi.")
            else:
                caveats.append(
                    "A widow(er) under 40 with no children USUALLY gets a ONE-TIME survivor grant "
                    "(menak she'erim = 36 monthly allowances) rather than a monthly allowance. "
                    "EXCEPTION: a monthly allowance is paid if she is pregnant with / later bears "
                    "the deceased's child, or (work-injury track) was unable to support herself "
                    "from work. Re-run with --exception-eligible for that monthly estimate. "
                    "Verify at btl.gov.il.")
                return None, basis_none(), caveats
        elif age < 50:
            base = WIDOW_40_50_NO_CHILDREN
            basis = "widow(er) aged 40-50, no children"
        elif age < 80:
            base = WIDOW_50_PLUS_NO_CHILDREN
            basis = "widow(er) aged 50+, no children"
        else:
            base = WIDOW_80_PLUS
            basis = "widow(er) aged 80+"

    seniority_rate = min(SENIORITY_RATE_PER_YEAR * max(seniority_years, 0), SENIORITY_MAX_RATE)
    seniority_amount = round(base * seniority_rate)
    total = base + seniority_amount

    caveats.append(
        "A widower without dependent children is subject to an income test "
        "(ceiling 7,848 NIS, minus a 2,093 NIS deduction, from 01.01.2026); the allowance "
        "may be reduced or denied. A widow is not income-tested.")
    caveats.append(
        "A widow(er) already drawing an old-age (vatik) pension is paid the old-age pension IN "
        "FULL PLUS half of the survivor's allowance. 919 NIS (from 01.01.2026) is only half of "
        "the childless-50+ base (half of 1,838); with children it is half the higher with-children "
        "rate. Check the applicable base.")
    caveats.append(
        "File the survivor's-allowance claim within 12 months of the death; later filing caps "
        "back-payment at the last 12 months.")

    breakdown = [
        ("Base (%s)" % basis, base),
        ("Seniority increment (%d%% of base, %d yrs @2%%, cap 50%%)"
         % (round(seniority_rate * 100), max(seniority_years, 0)), seniority_amount),
    ]
    return total, breakdown, caveats


def basis_none():
    return [("No monthly allowance estimated", 0)]


def estimate_work_related(age, orphans, wage):
    """Dependents' allowance (kitzvat tluyim) for a work-related death."""
    caveats = [
        "Work-related-death track (dependents' allowance). It is DISTINCT from the ordinary "
        "survivor's allowance and you cannot receive both for the same death. No income test. "
        "File form 213, not 410.",
    ]

    if orphans >= 1:
        if orphans == 1:
            rate = DEP_WIDOW_1_CHILD
        elif orphans == 2:
            rate = DEP_WIDOW_2_CHILDREN
        else:
            rate = DEP_WIDOW_3PLUS_CHILDREN
        basis = "widow(er) + %d child(ren)" % orphans
    else:
        if age < 40:
            caveats.append(
                "A widow under 40 with no children in the work-related track usually gets a "
                "one-time grant (60% x 36 of the full work-disability pension), not a monthly "
                "allowance. Verify at btl.gov.il.")
            rate = None
            basis = "widow under 40, no children"
        elif age < 50:
            rate = DEP_WIDOW_40_50
            basis = "widow(er) aged 40-50, no children"
        else:
            rate = DEP_WIDOW_50_PLUS
            basis = "widow(er) aged 50+, no children"

    if rate is None:
        return None, basis_none(), caveats

    if wage is None:
        caveats.append(
            "Applicable rate is %d%% of a full work-disability pension. Re-run with --wage "
            "<deceased monthly gross wage> to estimate an amount." % round(rate * 100))
        return None, [("Rate of full work-disability pension (%s)" % basis,
                       round(rate * 100))], caveats

    full_disability = min(wage * WORK_DISABILITY_WAGE_RATE, MAX_WORK_DISABILITY_PENSION)
    total = round(full_disability * rate)
    if wage * WORK_DISABILITY_WAGE_RATE > MAX_WORK_DISABILITY_PENSION:
        caveats.append("Wage exceeds the cap; full disability pension capped at 39,428 NIS.")

    breakdown = [
        ("Deceased monthly wage (input)", round(wage)),
        ("Full work-disability pension (75% of wage, cap 39,428)", round(full_disability)),
        ("Dependents' rate (%s): %d%%" % (basis, round(rate * 100)), 0),
    ]
    return total, breakdown, caveats


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Estimate a monthly Israeli survivor benefit (ESTIMATE ONLY).")
    p.add_argument("--age", type=int, help="Age of the surviving widow(er).")
    p.add_argument("--orphans", type=int, default=0,
                   help="Number of eligible children with the widow(er) (default 0).")
    p.add_argument("--seniority-years", type=int, default=0,
                   help="Full insurance years the deceased accrued (ordinary track only).")
    p.add_argument("--work-related", action="store_true",
                   help="Death resulted from a work accident / occupational disease.")
    p.add_argument("--wage", type=float, default=None,
                   help="Deceased monthly gross wage (needed for work-related amount).")
    p.add_argument("--exception-eligible", action="store_true",
                   help="Under-40 childless widow(er) who meets an exception (pregnant with / "
                        "bearing the deceased's child, or unable to support herself from work): "
                        "estimate a MONTHLY allowance instead of the one-time grant.")
    p.add_argument("--example", action="store_true", help="Run a worked example and exit.")
    args = p.parse_args(argv)

    if args.example:
        print("Example: widow aged 45, 2 children, deceased had 20 insurance years, "
              "non-work-related death.\n")
        args.age, args.orphans, args.seniority_years = 45, 2, 20
        args.work_related, args.wage = False, None

    if args.age is None:
        p.error("--age is required (or use --example).")

    print("=" * 64)
    print("ISRAELI SURVIVOR BENEFIT: ROUGH ESTIMATE (not an official decision)")
    print("Figures effective 01.01.2026. Verify at btl.gov.il before relying on this.")
    print("=" * 64)

    if args.work_related:
        total, breakdown, caveats = estimate_work_related(args.age, args.orphans, args.wage)
    else:
        total, breakdown, caveats = estimate_ordinary(
            args.age, args.orphans, args.seniority_years, args.exception_eligible)

    print("\nBreakdown:")
    for label, amount in breakdown:
        if amount:
            print("  %-56s %8d NIS" % (label, amount))
        else:
            print("  %s" % label)

    print()
    if total is not None:
        print("  ESTIMATED MONTHLY AMOUNT: ~%d NIS/month" % total)
    else:
        print("  No monthly amount estimated (see notes below).")

    print("\nImportant notes:")
    for c in caveats:
        print("  - %s" % c)
    print("\n  This is an estimate only. Official calculator + claim:")
    print("  https://www.btl.gov.il/Simulators/Pages/SherimCalc.aspx")
    return 0


if __name__ == "__main__":
    sys.exit(main())
