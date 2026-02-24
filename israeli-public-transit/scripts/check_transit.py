#!/usr/bin/env python3
"""
Israeli Public Transit Utility

Check real-time bus arrivals, look up transit operators,
and get Rav-Kav fare information.

Usage:
    python check_transit.py operators
    python check_transit.py stop 21345
    python check_transit.py fares
    python check_transit.py shabbat
"""

import argparse
import json
import sys
import urllib.request
import urllib.error


OPERATORS = {
    "egged": {
        "name": "Egged",
        "hebrew": "eged",
        "modes": ["Bus", "Express"],
        "region": "Nationwide (largest operator)",
        "website": "https://www.egged.co.il",
    },
    "dan": {
        "name": "Dan",
        "hebrew": "dan",
        "modes": ["Bus"],
        "region": "Gush Dan (Tel Aviv metro)",
        "website": "https://www.dan.co.il",
    },
    "metropoline": {
        "name": "Metropoline",
        "hebrew": "metropolin",
        "modes": ["Bus"],
        "region": "Central Israel, Sharon",
        "website": "https://www.metropoline.com",
    },
    "kavim": {
        "name": "Kavim",
        "hebrew": "kavim",
        "modes": ["Bus"],
        "region": "Central Israel, Jerusalem area",
        "website": "https://www.kavim-t.co.il",
    },
    "superbus": {
        "name": "Superbus",
        "hebrew": "superbus",
        "modes": ["Bus"],
        "region": "Central and Southern Israel",
        "website": "https://www.superbus.co.il",
    },
    "israel_railways": {
        "name": "Israel Railways",
        "hebrew": "rakevet yisrael",
        "modes": ["Train"],
        "region": "National rail network (~70 stations)",
        "website": "https://www.rail.co.il",
    },
    "jerusalem_lr": {
        "name": "Jerusalem Light Rail",
        "hebrew": "harakevet hakala yerushalayim",
        "modes": ["Light Rail"],
        "region": "Jerusalem (Red Line)",
        "website": "https://citypass.co.il",
    },
    "tel_aviv_lr": {
        "name": "Tel Aviv Light Rail",
        "hebrew": "harakevet hakala tel aviv",
        "modes": ["Light Rail"],
        "region": "Tel Aviv (Red Line, Petah Tikva to Bat Yam)",
        "website": "https://www.nta.co.il",
    },
}


def show_operators() -> None:
    """Display all Israeli transit operators."""
    print("=== Israeli Transit Operators ===\n")

    for key, info in OPERATORS.items():
        print(f"  {info['name']} ({info['hebrew']})")
        print(f"    Modes: {', '.join(info['modes'])}")
        print(f"    Region: {info['region']}")
        print(f"    Website: {info['website']}")
        print()


def check_stop(stop_code: str) -> None:
    """Check real-time arrivals at a bus stop using curlbus."""
    print(f"=== Real-Time Arrivals at Stop {stop_code} ===\n")

    url = f"https://curlbus.app/{stop_code}"

    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "israeli-transit-skill/1.0")
        req.add_header("Accept", "text/plain")

        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read().decode("utf-8")
            print(data)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Stop {stop_code} not found.")
            print("Stop codes are typically 5-digit numbers displayed at the physical stop.")
        else:
            print(f"HTTP error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}")
        print("curlbus.app may be temporarily unavailable.")
    except Exception as e:
        print(f"Error: {e}")

    print()
    print(f"Direct link: https://curlbus.app/{stop_code}")
    print("Alternative: Check operator apps (Egged, Dan, Moovit)")


def show_fares() -> None:
    """Display Rav-Kav fare information."""
    print("=== Rav-Kav Fare System ===\n")

    print("Fare structure:")
    print("  - Single ride: Per-zone pricing, pay per boarding")
    print("  - Daily cap: Maximum daily charge regardless of trips")
    print("  - Transfers: Free within 90 minutes of first boarding (same zone)")
    print()

    print("Discount profiles:")
    profiles = [
        ("Student (talmid)", "~33%", "Valid student card required"),
        ("Soldier (chayal)", "Free on most routes", "Active IDF service"),
        ("Senior 67+ (ezrach vatik)", "~50%", "Age verification"),
        ("Disabled (nacheh)", "~33-50%", "Disability certificate"),
        ("Youth 5-18 (naar)", "~33%", "Age verification"),
    ]

    print(f"  {'Profile':<30} {'Discount':<25} {'Requirement'}")
    print("  " + "-" * 70)
    for profile, discount, req in profiles:
        print(f"  {profile:<30} {discount:<25} {req}")

    print()
    print("Rav-Kav types:")
    print("  - Personal (ishi): Linked to ID, supports discount profiles")
    print("  - Anonymous (anonimi): No ID required, no discounts")
    print()
    print("Balance check: https://ravkavonline.co.il/")


def show_shabbat_info() -> None:
    """Display Shabbat transit information."""
    print("=== Shabbat and Holiday Transit Information ===\n")

    print("Regular Shabbat:")
    print("  - Most public transit STOPS Friday afternoon (~2-4 PM)")
    print("  - Service RESUMES Saturday evening (~30 min after sunset)")
    print()
    print("Shabbat alternatives:")
    print("  - Shared taxi (sherut/monit sherut) on popular routes")
    print("  - Private taxi (monit)")
    print("  - Ride-sharing services")
    print()
    print("Jewish holidays:")
    print("  - Rosh Hashana: No service (2 days)")
    print("  - Yom Kippur: NO transit nationwide (roads closed)")
    print("  - Sukkot: Reduced service")
    print("  - Pesach: Reduced service")
    print("  - Other holidays: Check operator announcements")
    print()
    print("NOTE: Some municipalities have begun operating limited")
    print("Shabbat bus service on specific routes.")


def main():
    parser = argparse.ArgumentParser(
        description="Israeli Public Transit Utility"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("operators", help="List transit operators")

    stop_parser = subparsers.add_parser("stop", help="Check arrivals at stop")
    stop_parser.add_argument("code", help="Stop code (5-digit number)")

    subparsers.add_parser("fares", help="Rav-Kav fare information")
    subparsers.add_parser("shabbat", help="Shabbat transit info")

    args = parser.parse_args()

    if args.command == "operators":
        show_operators()
    elif args.command == "stop":
        check_stop(args.code)
    elif args.command == "fares":
        show_fares()
    elif args.command == "shabbat":
        show_shabbat_info()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
