#!/usr/bin/env python3
"""
Israeli Public Transit Utility

Check real-time bus arrivals, look up transit operators,
and get Rav-Kav fare information.

Usage:
    python check_transit.py operators
    python check_transit.py stop 40001
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
        "website": "https://www.kavim-t.com",
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
        "region": "Jerusalem (Red Line, Green Line opening 2026)",
        "website": "https://www.cfir.co.il",
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
            print("Stop codes are the Ministry of Transport codes on the stop sign, 1 to 6 digits.")
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
    """Display the official Rav-Kav fare table and discount profiles."""
    print("=== Rav-Kav Fare System ===\n")
    print("Source: National Public Transport Authority, https://bus.gov.il/FaresDistance")
    print("Fares depend on the distance ring, not on the city or the operator.")
    print("'Bus' covers buses, both light rail systems, Metronit, Rakevelit and Carmelit.")
    print("'Combined' adds Israel Railways.\n")

    rings = [
        ("Yellow  0-15 km", "8", "11.5", "17.5", "23", "315", "323"),
        ("Green   15-40 km", "14.5", "21", "29", "32.5", "315", "323"),
        ("L.blue  40-75 km", "19", "27", "37.5", "42", "315", "464"),
        ("Blue    75-120 km", "19", "30.5", "37.5", "47", "315", "684"),
        ("Purple  120-225 km", "30.5", "52.5", "60.5", "80.5", "315", "684"),
        ("Grey    over 225 km", "74", "-", "79.5", "-", "-", "684"),
    ]
    hdr = ("Ring", "Single bus", "Single train", "Daily bus", "Daily comb.", "Monthly bus", "Monthly comb.")
    print(f"  {hdr[0]:<20}{hdr[1]:>12}{hdr[2]:>14}{hdr[3]:>11}{hdr[4]:>13}{hdr[5]:>13}{hdr[6]:>15}")
    print("  " + "-" * 98)
    for r in rings:
        print(f"  {r[0]:<20}{r[1]:>12}{r[2]:>14}{r[3]:>11}{r[4]:>13}{r[5]:>13}{r[6]:>15}")
    print("  (all amounts in NIS)")
    print()
    print("Monthly passes: nationwide bus 315 NIS (excludes Israel Railways, Eilat, and rides over")
    print("  225 km); combined-rail 323 / 464 / 684 NIS by rail range; regional 'Area 1' 139 NIS")
    print("  (up to 40 km). The weekly pass was abolished; the daily pass remains.")
    print("Transfers: unlimited and free for 90 minutes from first validation, on single rides up")
    print("  to 15 km (yellow ring) only.")
    print()

    print("Discount and free-ride profiles (Transport Justice reform, second phase):")
    profiles = [
        ("Children under 5", "Free", "-"),
        ("Youth 5-18", "50%", "Age verification"),
        ("Young adults 18-26", "33% on monthly passes", "Age verification"),
        ("Students", "33% singles; semester/annual pass", "Study confirmation + student ID"),
        ("Soldiers / security forces", "Free", "Service ID"),
        ("National / civil service", "Free", "Service confirmation"),
        ("Discharged soldiers", "Free for 1 year", "Apply within 2 months of discharge"),
        ("Senior women 62-67", "50%", "ID"),
        ("Age 67+ (zahav kav)", "Free", "ID, zahav-kav profile"),
        ("Geographic profile", "50% on monthly passes", "ID + proof of address"),
        ("Riders with a disability", "50%", "Disability certificate"),
        ("Bituach Leumi recipients", "50%", "Benefit confirmation"),
        ("Blind / visually impaired", "Free", "Certificate"),
    ]
    print(f"  {'Profile':<30} {'Entitlement':<36} {'Requirement'}")
    print("  " + "-" * 92)
    for profile, discount, req in profiles:
        print(f"  {profile:<30} {discount:<36} {req}")

    print()
    print("No stacking: the single highest entitlement is applied automatically.")
    print("Validation is mandatory on every boarding, including free rides and pass holders.")
    print()
    print("Rav-Kav types:")
    print("  - Personal (ishi): Linked to ID, supports discount profiles")
    print("  - Anonymous (anonimi): No ID required, no discounts")
    print()
    print("Balance check: https://ravkavonline.co.il/")
    print("Discount profiles: https://bus.gov.il/discounts")


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
    stop_parser.add_argument("code", help="Ministry of Transport stop code (1-6 digits, as printed on the stop sign)")

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
