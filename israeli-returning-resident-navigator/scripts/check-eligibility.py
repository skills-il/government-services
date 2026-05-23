#!/usr/bin/env python3
"""Returnee eligibility router.

Prints which of the three independent eligibility tracks (Misrad HaAliyah,
Mas Hachnasa, Bituach Leumi) the user likely qualifies for and which sources
to verify against. NO numeric tax math here, on purpose: Section 14 mechanics
live in the sister skill israeli-toshav-chozer-vatik-tax-planner.

Usage:
  python3 check-eligibility.py --years-abroad 8 --foreign-tax-resident yes \
      --israeli-citizen yes --age-at-return 35 --visited-over-4mo-any-year no \
      --emissary no --prev-returnee-assistance no [--profession other]

--profession defaults to "other" (standard 2-year track). Set to "scientist" or
"entrepreneur" for the 5-year track per gov.il "Who is a Returning Resident".
"""
from __future__ import annotations

import argparse
import sys
from textwrap import dedent

SOURCES = {
    "moia_definition": "https://www.gov.il/en/pages/returning_residents_whois",
    "moia_apply": "https://www.gov.il/he/service/application_for_recognition_as_returning_resident",
    "btl_landing": "https://www.btl.gov.il/Audience/toshavChozer/Pages/default.aspx",
    "kolzchut_dmei_bl": "https://www.kolzchut.org.il/he/%D7%93%D7%9E%D7%99_%D7%91%D7%99%D7%98%D7%95%D7%97_%D7%9C%D7%90%D7%95%D7%9E%D7%99_%D7%9C%D7%AA%D7%95%D7%A9%D7%91%D7%99%D7%9D_%D7%97%D7%95%D7%96%D7%A8%D7%99%D7%9D",
    "kolzchut_kupah": "https://www.kolzchut.org.il/he/%D7%94%D7%A6%D7%98%D7%A8%D7%A4%D7%95%D7%AA_%D7%AA%D7%95%D7%A9%D7%91_%D7%97%D7%95%D7%96%D7%A8_%D7%9C%D7%91%D7%99%D7%98%D7%95%D7%97_%D7%91%D7%A8%D7%99%D7%90%D7%95%D7%AA",
    "kolzchut_term": "https://www.kolzchut.org.il/he/%D7%AA%D7%95%D7%A9%D7%91_%D7%97%D7%95%D7%96%D7%A8",
}


def yn(value: str) -> bool:
    v = value.strip().lower()
    if v in {"yes", "y", "true", "1", "ken", "כן"}:
        return True
    if v in {"no", "n", "false", "0", "lo", "לא"}:
        return False
    raise argparse.ArgumentTypeError(f"expected yes/no, got: {value}")


def moia_track(args: argparse.Namespace) -> str:
    reasons: list[str] = []
    # Scientists and entrepreneurs need 5 years, not 2 (gov.il source).
    if args.profession in {"scientist", "entrepreneur"}:
        required_years = 5
        track_label = f"{args.profession} track (5-year threshold)"
    else:
        required_years = 2
        track_label = "standard track (2-year threshold)"
    if not args.israeli_citizen:
        reasons.append("not an Israeli citizen")
    if args.age_at_return < 17:
        reasons.append("under age 17 at return")
    if args.years_abroad < required_years:
        reasons.append(
            f"only {args.years_abroad} years abroad ({track_label} needs ≥ {required_years})"
        )
    if args.visited_over_4mo_any_year:
        # Visits-test window: 2y standard, 3y entrepreneur, 5y scientist (gov.il source).
        if args.profession == "scientist":
            window_label = "5 years (scientist track)"
        elif args.profession == "entrepreneur":
            window_label = "3 years (entrepreneur track)"
        else:
            window_label = "2 years (standard track)"
        reasons.append(f"visited Israel > 4 months in a year during the visits window ({window_label})")
    if args.emissary:
        reasons.append("served abroad as an emissary (5-year cooldown applies)")
    if args.prev_returnee_assistance:
        reasons.append(
            "previously received returnee assistance; 10-year cooldown applies "
            "AND return must follow 6+ years abroad"
        )

    if reasons:
        body = "\n    - ".join(reasons)
        return (
            "Misrad HaAliyah V'HaKlita certificate: LIKELY NOT eligible - reasons:\n    - "
            + body
            + f"\n  Verify: {SOURCES['moia_definition']}"
        )
    return (
        "Misrad HaAliyah V'HaKlita certificate: LIKELY eligible.\n"
        f"  Apply: {SOURCES['moia_apply']}\n"
        "  Window: 24 months from date of return for ministry services.\n"
        f"  Source: {SOURCES['moia_definition']}"
    )


def mas_hachnasa_track(args: argparse.Namespace) -> str:
    if not args.foreign_tax_resident:
        return (
            "Mas Hachnasa returnee benefits: NOT available - you were not a foreign tax resident.\n"
            f"  Source: {SOURCES['kolzchut_term']}"
        )
    if args.years_abroad >= 10:
        bracket = "תושב חוזר ותיק (≥ 10 years) - full Section 14 ten-year exemption basket"
    elif args.years_abroad >= 6:
        bracket = (
            "תושב חוזר רגיל (6-9 years) - partial: 5-year exemption on foreign passive income from "
            "assets bought while abroad, 10-year exemption on capital gains on those assets"
        )
    else:
        return (
            f"Mas Hachnasa returnee benefits: NOT available - only {args.years_abroad} years abroad "
            "(need ≥ 6 for partial, ≥ 10 for vatik).\n"
            f"  Source: {SOURCES['kolzchut_term']}"
        )
    return (
        f"Mas Hachnasa track: {bracket}\n"
        "  HAND OFF the tax math to israeli-toshav-chozer-vatik-tax-planner (Form 1348, Section 14 mechanics).\n"
        f"  Source: {SOURCES['kolzchut_term']}\n"
        "  Note (2026): vatik basket retains tax exemption but now requires full reporting to Mas Hachnasa for returns on or after 01.01.2026."
    )


def bl_track(args: argparse.Namespace) -> str:
    # Waiting period: 1 month per year abroad, MIN 2 months, MAX 6 (kolzchut kupah source).
    waiting_months = min(6, max(2, args.years_abroad))
    pidyon_2026 = "16,860 NIS (one shot, or up to 6 installments)"
    return dedent(
        f"""
        Bituach Leumi: file Form 628 ("שאלון לקביעת תושבות לתושב חוזר") at any BL branch
        or via the online personal area. BL decides residency by center of life, not by year count.
          Likely health-services waiting period: ~{waiting_months} month(s) (1 month per year abroad, min 2, max 6).
          Pidyon (redemption) in 2026: {pidyon_2026}.
          Source: {SOURCES['kolzchut_dmei_bl']}
          Source: {SOURCES['kolzchut_kupah']}
          BL phone: *6050 (Israel) or +972-8-936-9669 (from abroad, Hebrew/English/Russian, Sun-Thu 8:00-15:00).
          NOT available on day one: maternity allowance, dmei avtala (unemployment), employer insolvency.
        """
    ).strip()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--years-abroad", type=int, required=True, help="Continuous years of residence abroad")
    p.add_argument("--foreign-tax-resident", type=yn, required=True, help="Were you a foreign tax resident? yes/no")
    p.add_argument("--israeli-citizen", type=yn, default=True, help="Israeli citizen? yes/no (default yes)")
    p.add_argument("--age-at-return", type=int, default=18, help="Age at date of return")
    p.add_argument(
        "--visited-over-4mo-any-year",
        type=yn,
        default=False,
        help="During the last 2 years abroad, did you visit Israel > 4 months in any single year?",
    )
    p.add_argument("--emissary", type=yn, default=False, help="Served abroad as State/WZO/Jewish Agency/JNF/UJA/Israel Bonds emissary? yes/no")
    p.add_argument(
        "--prev-returnee-assistance",
        type=yn,
        default=False,
        help="Did you previously receive returnee assistance from Misrad HaAliyah? yes/no",
    )
    p.add_argument(
        "--profession",
        choices=["scientist", "entrepreneur", "other"],
        default="other",
        help=(
            "Special tracks: 'scientist' or 'entrepreneur' use the 5-year residence "
            "threshold (gov.il source). Default 'other' uses the standard 2-year threshold."
        ),
    )
    args = p.parse_args(argv)

    print(f"Inputs: years_abroad={args.years_abroad}, foreign_tax_resident={args.foreign_tax_resident}, "
          f"citizen={args.israeli_citizen}, age_at_return={args.age_at_return}, profession={args.profession}\n")

    print("Branch 1 - Misrad HaAliyah V'HaKlita")
    print(f"  {moia_track(args)}\n")

    print("Branch 2 - Mas Hachnasa (tax)")
    print(f"  {mas_hachnasa_track(args)}\n")

    print("Branch 3 - Bituach Leumi")
    print(f"  {bl_track(args)}\n")

    print("Reminder: this is a routing aid, not legal or tax advice. Verify every threshold against the cited sources before relying on it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
