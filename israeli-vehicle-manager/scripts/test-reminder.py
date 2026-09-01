#!/usr/bin/env python3
"""
Israeli Vehicle Test Reminder

Reports how long until the next annual vehicle test (mivchan rishuy / טסט),
or how far OVERDUE the vehicle already is.

The authoritative date is the expiry printed on the vehicle licence
("בתוקף עד"). The Ministry sets and shifts that date after a late renewal,
a retest, or an ownership transfer, so it is NOT simply the anniversary of
first registration. Pass --expiry-date whenever the user can read their
licence. --reg-date is a fallback that estimates the date from the vehicle's
first registration and is explicitly labelled as an estimate in the output.

Standard library only, no third-party dependencies.

Usage:
    python3 test-reminder.py --expiry-date 2026-11-30
    python3 test-reminder.py --reg-date 2023-06-15
    python3 test-reminder.py --reg-date 2024-02-01 --vehicle-class rental
    python3 test-reminder.py --help
"""

import argparse
import sys
from datetime import date, datetime

# Test exemption for a NEW vehicle, in years from first registration.
# Only these two classes have a documented private-owner exemption.
EXEMPT_YEARS = {
    "private": 3,
    "rental": 2,   # rental / leased (rechev haskara / hachkara)
}

# Supported classes. Motorcycles, commercial vehicles, taxis, driving-school
# cars and vehicles over 3.5t have their own periodicity and exemption rules
# that this script deliberately does not model.
UNSUPPORTED_NOTE = (
    "Motorcycles, commercial vehicles over 3,500 kg, taxis, buses and\n"
    "  driving-school vehicles follow different test periodicity. Check the\n"
    "  vehicle licence and the Ministry of Transport rather than using this\n"
    "  script."
)

# Penalty bands for driving on an expired test, from SKILL.md Step 3.
PENALTY_BANDS = [
    (120, "250 NIS + 6 licence points (up to about 4 months expired)"),
    (365, "1,000 NIS + 6 licence points (about 4 months to 1 year)"),
    (None, "court summons (over 1 year), which can carry a higher fine and suspension"),
]


def add_years(d: date, years: int) -> date:
    """Add whole years, clamping 29 February to 28 February in a common year."""
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d.replace(year=d.year + years, month=2, day=28)


def years_between(start: date, end: date) -> int:
    """Whole calendar years between two dates."""
    return end.year - start.year - ((end.month, end.day) < (start.month, start.day))


def parse_iso(value: str, flag: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        sys.exit(f"Error: {flag} '{value}' is not a valid date. Use YYYY-MM-DD.")


def plural(n: int, word: str = "day") -> str:
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def penalty_for(days_overdue: int) -> str:
    for limit, text in PENALTY_BANDS:
        if limit is None or days_overdue <= limit:
            return text
    return PENALTY_BANDS[-1][1]


def from_expiry(expiry: date, today: date) -> dict:
    delta = (expiry - today).days
    return {
        "basis": "licence expiry date (authoritative)",
        "due_date": expiry,
        "days": delta,
        "overdue": delta < 0,
        "estimated": False,
    }


def from_registration(reg: date, today: date, vehicle_class: str) -> dict:
    exempt_years = EXEMPT_YEARS[vehicle_class]
    first_test = add_years(reg, exempt_years)

    if today < first_test:
        return {
            "basis": f"first registration + {exempt_years}-year new-vehicle exemption (ESTIMATE)",
            "due_date": first_test,
            "days": (first_test - today).days,
            "overdue": False,
            "estimated": True,
            "exempt": True,
        }

    # Walk annual anniversaries forward, keeping the LAST one on or before
    # today. That anniversary is the test that was most recently due, so an
    # overdue vehicle is reported as overdue instead of being rolled forward
    # to next year. The previous version of this script always rolled forward
    # and could therefore never report an overdue test at all.
    due = first_test
    while add_years(due, 1) <= today:
        due = add_years(due, 1)

    days_since = (today - due).days

    # Without the licence we cannot know whether that test was actually done.
    # Anything more than a grace window past the anniversary is treated as
    # POSSIBLY OVERDUE rather than silently reported as fine.
    if days_since > 30:
        return {
            "basis": "annual anniversary of the first-test date (ESTIMATE)",
            "due_date": due,
            "days": -days_since,
            "overdue": True,
            "presumed": True,
            "estimated": True,
            "exempt": False,
            "next_anniversary": add_years(due, 1),
        }

    return {
        "basis": "annual anniversary of the first-test date (ESTIMATE)",
        "due_date": add_years(due, 1),
        "days": (add_years(due, 1) - today).days,
        "overdue": False,
        "estimated": True,
        "exempt": False,
        "last_anniversary": due,
        "days_since_last": days_since,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Days until (or past) the next Israeli vehicle test."
    )
    parser.add_argument(
        "--expiry-date",
        help="Licence expiry printed on the vehicle licence (YYYY-MM-DD). Preferred.",
    )
    parser.add_argument(
        "--reg-date",
        help="First registration date (YYYY-MM-DD). Fallback; produces an estimate.",
    )
    parser.add_argument(
        "--vehicle-class",
        choices=sorted(EXEMPT_YEARS),
        default="private",
        help="private (3-year new-vehicle exemption) or rental (2-year). Default: private.",
    )
    parser.add_argument(
        "--today",
        help="Override today's date (YYYY-MM-DD), for testing.",
    )
    args = parser.parse_args()

    if not args.expiry_date and not args.reg_date:
        parser.error("give --expiry-date (preferred) or --reg-date")

    today = parse_iso(args.today, "--today") if args.today else date.today()

    if args.expiry_date:
        result = from_expiry(parse_iso(args.expiry_date, "--expiry-date"), today)
    else:
        reg = parse_iso(args.reg_date, "--reg-date")
        if reg > today:
            sys.exit("Error: --reg-date is in the future.")
        result = from_registration(reg, today, args.vehicle_class)
        age = years_between(reg, today)

    line = "=" * 58
    print(f"\n{line}\n  Vehicle Test Reminder\n{line}")
    print(f"  Today:             {today.isoformat()}")
    print(f"  Basis:             {result['basis']}")

    if result["overdue"]:
        overdue = -result["days"]
        if result.get("presumed"):
            print(f"  Last test due:     {result['due_date'].isoformat()}")
            print(f"  STATUS:            POSSIBLY OVERDUE by {plural(overdue)}")
            print("                     (estimated from the registration date; if that")
            print("                      test was done, the next one is due")
            print(f"                      {result['next_anniversary'].isoformat()})")
        else:
            print(f"  Licence expired:   {result['due_date'].isoformat()}")
            print(f"  STATUS:            OVERDUE by {plural(overdue)}")
        if result.get("presumed"):
            # We inferred this from the registration date, not from the licence.
            # Printing a shekel exposure here would accuse a compliant owner, so
            # say what we actually know and send them to the licence.
            print("  We cannot tell from a registration date whether that test")
            print("  was done. Read the expiry off the vehicle licence and re-run")
            print("  with --expiry-date before drawing any conclusion.")
        else:
            print(f"  Exposure:          {penalty_for(overdue)}")
            print("  There is no grace period. Even one day expired is an offence.")
        if overdue >= 120:
            print("  From about four months past expiry the renewal is handled at")
            print("  the Penalties Collection Center rather than online.")
    elif result.get("exempt"):
        print(f"  STATUS:            EXEMPT (new vehicle, {args.vehicle_class})")
        print(f"  First test due:    {result['due_date'].isoformat()}")
        print(f"  Days until:        {result['days']}")
    else:
        print(f"  Next test due:     {result['due_date'].isoformat()}")
        print(f"  Days until:        {result['days']}")
        if "days_since_last" in result:
            print(
                f"  Last anniversary:  {result['last_anniversary'].isoformat()} "
                f"({result['days_since_last']} days ago)"
            )

    if args.expiry_date and args.vehicle_class != "private":
        print("\n  Note: --vehicle-class only affects the --reg-date estimate and was")
        print("  ignored here, because the licence expiry already accounts for any")
        print("  new-vehicle exemption.")

    if not args.reg_date:
        print("\n  If the vehicle is 15 or more years old, a braking-system check at")
        print("  a licensed garage is required BEFORE the test.")

    if args.reg_date and not args.expiry_date:
        if age >= 15:
            print("  WARNING:           Vehicle is 15+ years old. A braking-system")
            print("                     check at a licensed garage is required BEFORE")
            print("                     the test.")
        print("\n  This is an ESTIMATE from the registration date. Confirm against")
        print("  the expiry printed on the vehicle licence and re-run with")
        print("  --expiry-date; the Ministry can shift that date after a late")
        print("  renewal, a retest or an ownership transfer.")

    print(f"\n  Note: {UNSUPPORTED_NOTE}")
    print(f"{line}\n")


if __name__ == "__main__":
    main()
