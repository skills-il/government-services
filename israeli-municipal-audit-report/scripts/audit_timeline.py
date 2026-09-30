#!/usr/bin/env python3
"""Compute the statutory deadline chain for an Israeli municipal internal audit report.

Per sections 170C(a) to 170C(e) and 170C1A(c) to (d) of the Municipalities Ordinance.
Two fallback branches lead to two different end dates, which is the most common source
of error. Each downstream clock runs from the ACTUAL date of the previous step, so pass
the actual dates as they happen; until then the script assumes each actor uses its full
period, which gives the LATEST lawful date, not the expected one.

Usage:
  python3 audit_timeline.py --audited-year 2025
  python3 audit_timeline.py --audited-year 2025 --submitted 2026-03-15
  python3 audit_timeline.py --audited-year 2025 --submitted 2026-03-15 \\
      --mayor-comments 2026-05-01 --committee-submitted 2026-06-20 --council-discussed 2026-08-10
  add --not-circulated if the mayor did not give council members copies with the comments,
  and --regional-council for a regional council.
"""
import argparse
from datetime import date


def add_months(d, n):
    y, m = divmod(d.month - 1 + n, 12)
    y += d.year
    m += 1
    day = min(d.day, [31, 29 if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0) else 28,
                      31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return date(y, m, day)


def parse(s):
    if not s:
        return None
    y, m, d = (int(x) for x in s.split("-"))
    return date(y, m, d)


def flag(actual, deadline):
    if actual is None:
        return "  (not yet happened, full period assumed)"
    return f"  actual {actual.isoformat()}" + ("  LATE" if actual > deadline else "  on time")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--audited-year", type=int, required=True,
                   help="the year the report covers")
    p.add_argument("--submitted",
                   help="actual submission to the mayor YYYY-MM-DD (defaults to the 1 April statutory latest)")
    p.add_argument("--mayor-comments",
                   help="date the committee received the mayor's comments, if it has")
    p.add_argument("--not-circulated", action="store_true",
                   help="the mayor did not give every council member a copy of the report with the comments")
    p.add_argument("--committee-submitted",
                   help="date the committee submitted its conclusions to the council, if it has")
    p.add_argument("--council-discussed",
                   help="date the council held its special discussion, if it has")
    p.add_argument("--regional-council", action="store_true",
                   help="the authority is a regional council (170C1A does not apply)")
    a = p.parse_args()

    try:
        statutory = date(a.audited_year + 1, 4, 1)
        submitted = parse(a.submitted) or statutory
        mayor = parse(a.mayor_comments)
        committee = parse(a.committee_submitted)
        council = parse(a.council_discussed)
    except ValueError as e:
        p.error(f"bad date ({e}); use YYYY-MM-DD")
    for name, d in (("--mayor-comments", mayor), ("--committee-submitted", committee),
                    ("--council-discussed", council)):
        if d and d < submitted:
            p.error(f"{name} {d.isoformat()} is before the submission date {submitted.isoformat()}")

    print(f"Audited year         : {a.audited_year}")
    print(f"Statutory latest     : {statutory.isoformat()} (1 April of the following year)")
    print(f"Submission used      : {submitted.isoformat()}"
          + ("  LATE" if submitted > statutory else ""))
    print("A copy goes to the audit committee at the same moment (170C(a)).")
    print()

    mayor_dl = add_months(submitted, 3)
    mayor_late = bool(mayor and mayor > mayor_dl)
    print("Main chain (each clock runs from the ACTUAL previous step)")
    print(f"  Mayor comments to committee + copies to council : {mayor_dl.isoformat()}  (3 months from receipt)"
          + flag(mayor, mayor_dl))

    if mayor and not mayor_late:
        committee_dl = add_months(mayor, 2)
        basis = "2 months from receiving the mayor's comments"
    elif mayor_late:
        committee_dl = add_months(submitted, 5)
        basis = "fallback A, comments came late: 5 months from delivery to the committee"
    else:
        committee_dl = add_months(submitted, 5)
        basis = "latest case: mayor's full 3 months plus 2, equal to fallback A"
    print(f"  Committee conclusions to council                 : {committee_dl.isoformat()}  ({basis})"
          + flag(committee, committee_dl))
    if council and committee and council < committee and committee <= committee_dl:
        p.error("--council-discussed is before an on-time --committee-submitted")
    if committee and mayor and committee < mayor:
        print("  NOTE: the committee submitted before the mayor's comments arrived; 170C(d) has it")
        print("        discuss the report AND the comments.")
    if committee and not mayor and committee < mayor_dl:
        print("  NOTE: the committee submitted before any mayor's comments were recorded; 170C(d)")
        print("        has it discuss the report AND the comments, unless the mayor's period lapsed.")

    fallback_b = add_months(submitted, 7)
    committee_late = bool(committee and committee > committee_dl)
    # 170C(e)(2) has two triggers: the committee missed its period, or the mayor did not
    # circulate copies. A mayor who missed the 3-month period has not circulated within it.
    not_circulated = a.not_circulated or mayor_late
    strict = None
    if committee_late or not_circulated:
        council_dl = fallback_b
        why = "committee missed its period" if committee_late else "mayor did not circulate copies"
        cbasis = f"fallback B, {why}: auditor delivers copies, 7 months from submission"
        if committee and not committee_late:
            strict = add_months(committee, 2)
    elif committee:
        council_dl = add_months(committee, 2)
        cbasis = "2 months from the committee's submission"
    else:
        council_dl = add_months(committee_dl, 2)
        cbasis = "latest case, 2 months after the committee's deadline"
    print(f"  Council special discussion                       : {council_dl.isoformat()}  ({cbasis})"
          + flag(council, council_dl))
    if strict and strict < council_dl:
        print(f"  NOTE: on a strict cumulative reading 170C(e)(1) may still bind once the committee")
        print(f"        submitted, giving {strict.isoformat()}. Aim for the earlier date.")
    print()
    print("Fallback A, mayor does not comment in time")
    print(f"  Committee acts within 5 months of delivery to it : {add_months(submitted, 5).isoformat()}")
    print("Fallback B, committee does not submit in time or mayor does not circulate copies")
    print(f"  Auditor delivers to all council members, council")
    print(f"  discusses not later than 7 months from submission: {fallback_b.isoformat()}")
    print()

    disc = council or council_dl
    if a.regional_council:
        print("Deficiency-correction team: 170C1A does not apply to a regional council.")
        print("  (A regional council still needs the State Comptroller Law 21A team for Comptroller reports.)")
    else:
        team_dl = add_months(disc, 3)
        print("Deficiency-correction team (170C1A)")
        print(f"  Team recommendations to the mayor                : {team_dl.isoformat()}  (3 months from the council discussion"
              + (")" if council else ", latest case)"))
        print(f"  Mayor's written reasons for deferring a fix      : {add_months(team_dl, 3).isoformat()}  (3 months after the recommendations, latest case)")
        print("  Team reports on implementation to the committee  : once every three months")
    print()
    pub = max(disc, committee_dl)
    print("Publication (170C(f)); breach, or breach of a permit condition, carries one year's")
    print("imprisonment (334A).")
    print("  The report, any part or its contents: not before the date set for its submission")
    print("  to the council. The statute does not define that date; the conservative earliest")
    print(f"  date is the later of the council discussion and the committee's deadline: {pub.isoformat()}"
          + ("" if council else " (council has not yet discussed it)"))
    print("  An audit finding: the second limb has no date on its face, so a finding outside the")
    print("  published report needs a permission from the auditor or the mayor, with committee approval.")
    print("  Deadlines falling on Shabbat or a holiday are not rolled forward by this script.")


if __name__ == "__main__":
    main()
