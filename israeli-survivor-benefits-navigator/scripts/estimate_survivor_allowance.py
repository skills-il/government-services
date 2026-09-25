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
Section numbers refer to the National Insurance Law [Consolidated Version], 1995.

Usage examples:
  python3 estimate_survivor_allowance.py --age 52 --orphans 0
  python3 estimate_survivor_allowance.py --age 45 --orphans 2 --seniority-years 20
  python3 estimate_survivor_allowance.py --age 45 --child-aged-out
  python3 estimate_survivor_allowance.py --age 34 --posthumous-child
  python3 estimate_survivor_allowance.py --orphans 2 --orphans-alone no-parent-or-abroad
  python3 estimate_survivor_allowance.py --age 48 --orphans 1 --work-related --wage 14000
  python3 estimate_survivor_allowance.py --age 34 --work-related --wage 12000 --unable-to-support
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
# s.256A: from age 80 an addition is paid ON TOP of the allowance, with or without
# children. Its size is the published 80+ row minus the 50+ row.
AGE_80_ADDITION = WIDOW_80_PLUS - WIDOW_50_PLUS_NO_CHILDREN  # 103

# --- Orphans paid in their own right (no entitled widow(er)), effective 01.01.2026 ---
# Source: https://www.btl.gov.il/benefits/Survivors_%20Insurance/shiuraihakizba/Pages/k.yatom.aspx
ORPHAN_SINGLE = 1142        # "סכום הקצבה לילד יחיד - 1,142 ש\"ח"
ORPHAN_EACH_OF_SEVERAL = 862  # "סכום הקצבה כשיש יותר מילד אחד - 862 ש\"ח"
# s.252(c)(2): no surviving parent, or the parent lives abroad permanently: 11% of the
# basic amount FOR EACH child, i.e. the single-child rate 1,142 per child.
ORPHAN_NO_PARENT_EACH = 1142

# --- Seniority increment (תוספת ותק), s.257 ---
# Source: https://www.btl.gov.il/benefits/Survivors_%20Insurance/shiuraihakizba/Pages/vetek.aspx
# "2% עבור כל שנת ביטוח" since Jan 2019; "מקסימום ... 50% מהקצבה"
SENIORITY_RATE_PER_YEAR = 0.02
SENIORITY_MAX_RATE = 0.50

# --- Dependents' allowance (work-related death), effective 01.01.2026 ---
# Source: btl Work_Injury dependents "שיעורי הקצבה" page; NI Law s.130-134.
# Base = full (100%) work-disability pension = 75% of the deceased's determining wage.
# "קצבת נכות מעבודה מלאה מחושבת לפי 75% מהשכר"
WORK_DISABILITY_WAGE_RATE = 0.75
# "מקסימום קצבת נכות מעבודה - 39,428 ש\"ח (החל ב- 01.01.2026)"
MAX_WORK_DISABILITY_PENSION = 39428
# Widow(er) WITH children: percentages of the full work-disability pension (s.132(5)).
DEP_WIDOW_1_CHILD = 0.80   # "אלמן/ה + ילד אחד 80%"
DEP_WIDOW_2_CHILDREN = 0.90  # "אלמן/ה + 2 ילדים 90%"
DEP_WIDOW_3PLUS_CHILDREN = 1.00  # "אלמן/ה + 3 ילדים ויותר 100%"
# Widow(er) WITHOUT children, by age (s.132(1), (2)).
DEP_WIDOW_40_50 = 0.40    # "50-40 שנה 40%"
DEP_WIDOW_50_PLUS = 0.60  # "50 שנה ומעלה 60%"
# Under-40 childless widow: one-time grant of 60% x 36 (s.133(a)).
DEP_GRANT_MONTHS = 36
# Orphans on their own (s.132(6)).
DEP_ORPHANS_ALONE = {1: 0.60, 2: 0.80, 3: 0.90}  # 4 or more: 100%
# Survivor grant (s.255(a)): 36 allowances at the s.252(a)(1) rate, i.e. the 50+ row.
SURVIVOR_GRANT_MONTHS = 36

SENIORITY_CAVEAT = (
    "Seniority (s.257) counts only years in which the deceased was an INSURED WORKER "
    "(employee or self-employed) AND contributions were paid; years as a non-working "
    "spouse do not count, and no increment is paid while contributions are in arrears. "
    "Enter only those years.")


def seniority(years):
    rate = min(SENIORITY_RATE_PER_YEAR * years, SENIORITY_MAX_RATE)
    return rate


def estimate_orphans_alone(orphans, seniority_years, parent_status):
    """Orphans paid in their own right (no entitled widow(er))."""
    caveats = [SENIORITY_CAVEAT]
    if parent_status == "no-parent-or-abroad":
        base = ORPHAN_NO_PARENT_EACH * orphans
        basis = "%d orphan(s), no surviving parent or the parent lives abroad (1,142 each)" % orphans
        caveats.append(
            "An orphan of BOTH parents is entitled from EACH parent separately (if both were "
            "insured), which BTL publishes as 2,284 per child. Run once per deceased parent.")
    else:
        if orphans == 1:
            base = ORPHAN_SINGLE
        else:
            base = ORPHAN_EACH_OF_SEVERAL * orphans
        basis = ("%d orphan(s) with a parent in Israel who is not entitled "
                 "(1,142 for one child, 862 each for more)" % orphans)
    rate = seniority(seniority_years)
    amount = round(base * rate)
    caveats.append(
        "The orphan subsistence allowance (dmei michya, 946 a month when no survivor's "
        "allowance is paid to a parent) may be due ON TOP for a studying orphan; claim on form 2910.")
    breakdown = [("Base (%s)" % basis, base),
                 ("Seniority increment (%d%% of base)" % round(rate * 100), amount)]
    return base + amount, breakdown, caveats


def estimate_ordinary(age, orphans, seniority_years, widower, child_aged_out,
                      posthumous_child):
    """Ordinary survivor's allowance (non-work-related death)."""
    caveats = [SENIORITY_CAVEAT]
    rate = seniority(seniority_years)

    if posthumous_child and orphans == 0:
        # s.260(1): a widow who bears the deceased's child after his death is entitled to the
        # allowance from the date of death, as a widow with a child; a grant already paid is
        # set off against it.
        orphans = 1
        caveats.append(
            "Posthumous child (s.260(1)): once the child is born she is paid as a widow with a "
            "child, from the date of death, and any survivor grant already paid is set off. "
            "Confirm the rate for the months before the birth with Bituach Leumi.")

    if orphans >= 1:
        if orphans == 1:
            base = WIDOW_ONE_CHILD
        elif orphans == 2:
            base = WIDOW_TWO_CHILDREN
        else:
            base = WIDOW_TWO_CHILDREN + EACH_ADDITIONAL_CHILD * (orphans - 2)
        basis = "widow(er) with %d child(ren)" % orphans
        if age >= 80:
            base += AGE_80_ADDITION
            basis += ", plus the age-80 addition (s.256A)"
    elif child_aged_out and not widower:
        # s.256: a widow who had a child with her who is no longer with her is paid as if 50.
        base = WIDOW_80_PLUS if age >= 80 else WIDOW_50_PLUS_NO_CHILDREN
        basis = "widow whose child has left the definition, paid as if aged 50 (s.256)"
    else:
        if child_aged_out and widower:
            caveats.append(
                "The 'paid as if aged 50' rule for a child who has aged out (s.256) applies to a "
                "widow only; it was not applied.")
        if age < 40:
            grant_base = WIDOW_50_PLUS_NO_CHILDREN * SURVIVOR_GRANT_MONTHS
            grant = round(grant_base * (1 + rate))
            caveats.append(
                "Under 40 with no children: no monthly allowance. A ONE-TIME survivor grant is "
                "paid instead: 36 x 1,838 = %s NIS, plus the seniority increment (s.255(a), "
                "s.257), so about %s NIS here. It is 36 times the 1,838 rate, not 1,381. If a child "
                "of the deceased is born after the death, re-run with --posthumous-child."
                % (format(grant_base, ","), format(grant, ",")))
            if not widower:
                caveats.append(
                    "A widow who had a child with her at the death who has since aged out is paid "
                    "monthly instead: re-run with --child-aged-out.")
            return None, [("One-time survivor grant (not monthly)", grant)], caveats
        elif age < 50:
            base = WIDOW_40_50_NO_CHILDREN
            basis = "widow(er) aged 40-50, no children"
        elif age < 80:
            base = WIDOW_50_PLUS_NO_CHILDREN
            basis = "widow(er) aged 50+, no children"
        else:
            base = WIDOW_80_PLUS
            basis = "widow(er) aged 80+"

    seniority_amount = round(base * rate)
    total = base + seniority_amount

    if widower and orphans == 0:
        caveats.append(
            "A widower with no child who counts as an orphan is income-tested (ceiling 7,848 "
            "NIS a month, after a 2,093 NIS deduction from work, pension or retirement income, "
            "from 01.01.2026); above it he is paid a grant, not this allowance. A widower with "
            "such a child is not income-tested.")
    caveats.append(
        "This is the BASE allowance. A family with little other income may instead be paid "
        "the allowance WITH the income supplement, 4,375 to 8,563 NIS a month by age band and "
        "family composition (from 01.01.2026), claimed on form 430. Check that first.")
    caveats.append(
        "A widow(er) already drawing an old-age (vatik) pension is paid the old-age pension IN "
        "FULL PLUS half of the survivor's allowance. 919 NIS (from 01.01.2026) is only half of "
        "the childless-50+ base; with children it is half the higher with-children rate.")
    caveats.append(
        "File the survivor's-allowance claim within 12 months of the death; later filing caps "
        "back-payment at the last 12 months. An appeal to the regional labour court must be "
        "filed within 12 months of receiving the written decision.")
    caveats.append(
        "A survivor entitled to another National Insurance allowance that is not the old-age "
        "pension (general disability, work-disability, dependents') must CHOOSE one, not both. "
        "The children keep the survivor's allowance either way.")

    breakdown = [
        ("Base (%s)" % basis, base),
        ("Seniority increment (%d%% of base, %d yrs @2%%, cap 50%%)"
         % (round(rate * 100), seniority_years), seniority_amount),
    ]
    return total, breakdown, caveats


def estimate_work_related(age, orphans, wage, widower, unable_to_support, child_aged_out,
                          pregnant, widower_income_within_ceiling):
    """Dependents' allowance (kitzvat tluyim) for a work-related death, s.130-134."""
    caveats = [
        "Work-related-death track (dependents' allowance). It is DISTINCT from the ordinary "
        "survivor's allowance and you cannot receive both for the same death. File form 213, "
        "not 410.",
    ]

    if widower and orphans == 0 and not unable_to_support and not widower_income_within_ceiling:
        # s.130(a)(5): a husband is a dependant only while a child is with him, or he cannot
        # support himself, or his income is within Table 9.
        caveats.append(
            "A widower with no child is a dependant only if he cannot support himself, or his "
            "income is within the Table 9 ceiling (s.130(a)(5)). Neither was indicated, so no "
            "allowance is estimated. Re-run with --unable-to-support or "
            "--widower-income-within-ceiling if one applies.")
        return None, basis_none(), caveats

    if orphans >= 1:
        if orphans == 1:
            rate = DEP_WIDOW_1_CHILD
        elif orphans == 2:
            rate = DEP_WIDOW_2_CHILDREN
        else:
            rate = DEP_WIDOW_3PLUS_CHILDREN
        basis = "widow(er) + %d child(ren)" % orphans
    elif pregnant and not widower:
        rate = DEP_WIDOW_50_PLUS
        basis = "widow pregnant at the death: 60% until the birth"
        caveats.append("After the birth the rate becomes 80% (widow with one child).")
    elif unable_to_support:
        # s.132(3) and s.134: unable to support herself from work shortly before the death or
        # within a year of it: paid as if aged 50, at any age; a grant already paid is set off.
        rate = DEP_WIDOW_50_PLUS
        basis = "widow(er) unable to support herself, paid as if aged 50 (s.132(3), s.134)"
        caveats.append(
            "Applies when she could not support herself from work shortly before the death or "
            "within one year of it, and only while that lasts. A one-time grant already paid is "
            "set off against the allowance.")
    elif child_aged_out and not widower:
        rate = DEP_WIDOW_50_PLUS
        basis = "widow whose child is no longer with her, paid as if aged 50 (s.132(4))"
    else:
        if child_aged_out and widower:
            caveats.append(
                "The aged-out-child rule (s.132(4)) applies to a widow only; not applied.")
        if age < 40:
            rate = None
            basis = "under 40, no children"
        elif age < 50:
            rate = DEP_WIDOW_40_50
            basis = "widow(er) aged 40-50, no children"
        else:
            rate = DEP_WIDOW_50_PLUS
            basis = "widow(er) aged 50+, no children"
        if age < 50:
            caveats.append(
                "Paid 60% instead (not 40% or the grant) if she could not support herself from "
                "work around the death (--unable-to-support), if a widow had a child with her "
                "who has since aged out (--child-aged-out), or if she was pregnant at the death "
                "(--pregnant).")

    if wage is None:
        if rate is None:
            caveats.append(
                "Under 40 with no children: a one-time grant of 60% x 36 of the full "
                "work-disability pension (s.133(a)). Re-run with --wage to size it.")
            return None, basis_none(), caveats
        caveats.append(
            "Applicable rate is %d%% of a full work-disability pension. Re-run with --wage "
            "<deceased monthly gross wage> to estimate an amount." % round(rate * 100))
        return None, [("Rate of full work-disability pension (%s): %d%%"
                       % (basis, round(rate * 100)), 0)], caveats

    full_disability = min(wage * WORK_DISABILITY_WAGE_RATE, MAX_WORK_DISABILITY_PENSION)
    if wage * WORK_DISABILITY_WAGE_RATE > MAX_WORK_DISABILITY_PENSION:
        caveats.append("Wage exceeds the cap; full disability pension capped at 39,428 NIS.")

    if rate is None:
        grant = round(full_disability * DEP_WIDOW_50_PLUS * DEP_GRANT_MONTHS)
        caveats.append(
            "Under 40 with no children: no monthly allowance but a ONE-TIME grant of 60% x 36 of "
            "the full work-disability pension (s.133(a)).")
        return None, [("Full work-disability pension (75% of wage, cap 39,428)",
                       round(full_disability)),
                      ("One-time grant (60% x 36, not monthly)", grant)], caveats

    total = round(full_disability * rate)
    breakdown = [
        ("Deceased monthly wage (input)", round(wage)),
        ("Full work-disability pension (75% of wage, cap 39,428)", round(full_disability)),
        ("Dependents' rate (%s): %d%%" % (basis, round(rate * 100)), 0),
    ]
    return total, breakdown, caveats


def estimate_work_orphans_alone(orphans, wage):
    """Dependents' allowance for orphans on their own, s.132(6)."""
    caveats = ["Work-related-death track, orphans on their own (s.132(6)). File form 213."]
    rate = DEP_ORPHANS_ALONE.get(orphans, 1.00)
    if wage is None:
        return None, [("Rate of full work-disability pension (%d orphan(s)): %d%%"
                       % (orphans, round(rate * 100)), 0)], caveats
    full_disability = min(wage * WORK_DISABILITY_WAGE_RATE, MAX_WORK_DISABILITY_PENSION)
    return round(full_disability * rate), [
        ("Full work-disability pension (75% of wage, cap 39,428)", round(full_disability)),
        ("Orphans-alone rate (%d orphan(s)): %d%%" % (orphans, round(rate * 100)), 0)], caveats


def basis_none():
    return [("No monthly allowance estimated", 0)]


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Estimate a monthly Israeli survivor benefit (ESTIMATE ONLY).")
    p.add_argument("--age", type=int, help="Age of the surviving widow(er).")
    p.add_argument("--widower", action="store_true",
                   help="The survivor is a widower (default: widow). Several rules apply to "
                        "widows only, and a widower has an income test.")
    p.add_argument("--orphans", type=int, default=0,
                   help="Number of eligible children with the widow(er) (default 0).")
    p.add_argument("--orphans-alone", choices=["parent-in-israel", "no-parent-or-abroad"],
                   help="Orphans paid in their own right (no entitled widow(er)): the surviving "
                        "parent is in Israel but not entitled, or there is no surviving parent "
                        "or the parent lives abroad permanently. --age is then not needed.")
    p.add_argument("--seniority-years", type=int, default=0,
                   help="Years the deceased was an INSURED WORKER with contributions paid "
                        "(ordinary track only; see s.257).")
    p.add_argument("--child-aged-out", action="store_true",
                   help="A widow had an entitled child with her at the death who is no longer "
                        "with her (paid as if aged 50; widows only).")
    p.add_argument("--posthumous-child", action="store_true",
                   help="Ordinary track: the widow is pregnant with, or bore, the deceased's child "
                        "after his death (s.260(1)).")
    p.add_argument("--work-related", action="store_true",
                   help="Death resulted from a work accident / occupational disease.")
    p.add_argument("--wage", type=float, default=None,
                   help="Deceased monthly gross wage (work-related track).")
    p.add_argument("--unable-to-support", action="store_true",
                   help="Work track: the survivor could not support herself from work shortly "
                        "before the death or within a year of it (s.132(3), s.134).")
    p.add_argument("--pregnant", action="store_true",
                   help="Work track: the widow was pregnant at the death.")
    p.add_argument("--widower-income-within-ceiling", action="store_true",
                   help="Work track: a childless widower whose income is within the Table 9 "
                        "ceiling (s.130(a)(5)).")
    p.add_argument("--example", action="store_true", help="Run a worked example and exit.")
    args = p.parse_args(argv)

    if args.example:
        print("Example: widow aged 45, 2 children, deceased had 20 insured working years, "
              "non-work-related death.\n")
        args.age, args.orphans, args.seniority_years = 45, 2, 20
        args.work_related, args.wage = False, None

    if args.orphans < 0 or args.seniority_years < 0:
        p.error("--orphans and --seniority-years cannot be negative.")
    if args.wage is not None and args.wage <= 0:
        p.error("--wage must be a positive monthly amount.")
    if args.orphans_alone:
        if args.orphans < 1:
            p.error("--orphans-alone needs --orphans 1 or more.")
    else:
        if args.age is None:
            p.error("--age is required (or use --example, or --orphans-alone).")
        if not 16 <= args.age <= 120:
            p.error("--age must be between 16 and 120.")

    notes = []
    if args.work_related and args.seniority_years:
        notes.append("--seniority-years is ignored in the work-related track (no seniority "
                     "increment there).")
    if not args.work_related and args.wage is not None:
        notes.append("--wage is ignored in the ordinary track (the allowance is not wage-based).")
    if not args.work_related and (args.unable_to_support or args.pregnant
                                  or args.widower_income_within_ceiling):
        notes.append("--unable-to-support / --pregnant / --widower-income-within-ceiling apply "
                     "only to the work-related track. In the ordinary track, inability to work "
                     "does not create a monthly allowance under 40; a posthumous child does "
                     "(--posthumous-child).")
    if args.work_related and args.posthumous_child:
        notes.append("In the work-related track use --pregnant (60% until the birth, then 80%).")

    print("=" * 64)
    print("ISRAELI SURVIVOR BENEFIT: ROUGH ESTIMATE (not an official decision)")
    print("Figures effective 01.01.2026. Verify at btl.gov.il before relying on this.")
    print("=" * 64)

    if args.work_related and args.orphans_alone:
        total, breakdown, caveats = estimate_work_orphans_alone(args.orphans, args.wage)
    elif args.work_related:
        total, breakdown, caveats = estimate_work_related(
            args.age, args.orphans, args.wage, args.widower, args.unable_to_support,
            args.child_aged_out, args.pregnant, args.widower_income_within_ceiling)
    elif args.orphans_alone:
        total, breakdown, caveats = estimate_orphans_alone(
            args.orphans, args.seniority_years, args.orphans_alone)
    else:
        total, breakdown, caveats = estimate_ordinary(
            args.age, args.orphans, args.seniority_years, args.widower,
            args.child_aged_out, args.posthumous_child)

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
    for c in notes + caveats:
        print("  - %s" % c)
    print("\n  This is an estimate only. Official calculator + claim:")
    print("  https://www.btl.gov.il/Simulators/Pages/SherimCalc.aspx")
    return 0


if __name__ == "__main__":
    sys.exit(main())
