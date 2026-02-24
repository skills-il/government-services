#!/usr/bin/env python3
"""
Israeli Address Lookup and Validation

Standalone utility for formatting, validating, and looking up
Israeli addresses, postal codes (mikud), and CBS city codes.

Usage:
    python lookup_address.py city "Tel Aviv"
    python lookup_address.py format "Rothschild 42, Tel Aviv"
    python lookup_address.py cities
"""

import argparse
import json
import sys

# CBS city codes for major Israeli cities
CITY_CODES = {
    "jerusalem": {"code": 3000, "hebrew": "yerushalayim", "area_code": "02"},
    "tel aviv-yafo": {"code": 5000, "hebrew": "tel aviv-yafo", "area_code": "03"},
    "tel aviv": {"code": 5000, "hebrew": "tel aviv-yafo", "area_code": "03"},
    "haifa": {"code": 4000, "hebrew": "haifa", "area_code": "04"},
    "rishon lezion": {"code": 8300, "hebrew": "rishon letzion", "area_code": "03"},
    "petah tikva": {"code": 7900, "hebrew": "petach tikva", "area_code": "03"},
    "ashdod": {"code": 70, "hebrew": "ashdod", "area_code": "08"},
    "netanya": {"code": 7400, "hebrew": "netanya", "area_code": "09"},
    "beer sheva": {"code": 9000, "hebrew": "beer sheva", "area_code": "08"},
    "beersheba": {"code": 9000, "hebrew": "beer sheva", "area_code": "08"},
    "holon": {"code": 6600, "hebrew": "holon", "area_code": "03"},
    "bnei brak": {"code": 6100, "hebrew": "bnei brak", "area_code": "03"},
    "ramat gan": {"code": 8600, "hebrew": "ramat gan", "area_code": "03"},
    "bat yam": {"code": 6200, "hebrew": "bat yam", "area_code": "03"},
    "rehovot": {"code": 8400, "hebrew": "rechovot", "area_code": "08"},
    "ashkelon": {"code": 7100, "hebrew": "ashkelon", "area_code": "08"},
    "herzliya": {"code": 6400, "hebrew": "herzliya", "area_code": "09"},
    "kfar saba": {"code": 6900, "hebrew": "kfar saba", "area_code": "09"},
    "raanana": {"code": 8700, "hebrew": "raanana", "area_code": "09"},
    "modiin": {"code": 1200, "hebrew": "modiin-maccabim-reut", "area_code": "08"},
    "nazareth": {"code": 7300, "hebrew": "natzrat", "area_code": "04"},
    "lod": {"code": 7000, "hebrew": "lod", "area_code": "08"},
    "ramla": {"code": 8500, "hebrew": "ramla", "area_code": "08"},
    "eilat": {"code": 2600, "hebrew": "eilat", "area_code": "08"},
    "tiberias": {"code": 6700, "hebrew": "tveria", "area_code": "04"},
    "acre": {"code": 4100, "hebrew": "akko", "area_code": "04"},
    "akko": {"code": 4100, "hebrew": "akko", "area_code": "04"},
    "nahariya": {"code": 7500, "hebrew": "nahariya", "area_code": "04"},
    "givatayim": {"code": 6300, "hebrew": "givatayim", "area_code": "03"},
}


def lookup_city(name: str) -> None:
    """Look up a city's CBS code and details."""
    normalized = name.lower().strip()
    city = CITY_CODES.get(normalized)

    if city:
        print(f"City: {name}")
        print(f"CBS Code: {city['code']}")
        print(f"Hebrew: {city['hebrew']}")
        print(f"Area Code: {city['area_code']}")
    else:
        # Try partial match
        matches = [
            (k, v) for k, v in CITY_CODES.items()
            if normalized in k or k in normalized
        ]
        if matches:
            print(f"No exact match for '{name}'. Possible matches:")
            for k, v in matches:
                print(f"  {k}: CBS Code {v['code']}, Area Code {v['area_code']}")
        else:
            print(f"City '{name}' not found in reference data.")
            print("Try using the Hebrew transliteration or check data.gov.il for the full settlement list.")


def format_address(address: str) -> None:
    """Parse and format an Israeli address."""
    parts = [p.strip() for p in address.replace(",", " ").split()]

    # Try to identify city from the address parts
    city_found = None
    street_parts = []
    number = None

    for i, part in enumerate(parts):
        # Check if this part is a number (street number)
        if part.isdigit() and not number:
            number = part
            continue

        # Check if remaining parts form a city name
        remaining = " ".join(parts[i:]).lower()
        for city_name in CITY_CODES:
            if remaining.startswith(city_name) or city_name.startswith(remaining):
                city_found = city_name
                break

        if city_found:
            break
        street_parts.append(part)

    street = " ".join(street_parts)

    print("Parsed Address Components:")
    print(f"  Street: {street or 'Not identified'}")
    print(f"  Number: {number or 'Not found'}")
    print(f"  City: {city_found or 'Not identified'}")

    if city_found and city_found in CITY_CODES:
        city_info = CITY_CODES[city_found]
        print(f"  CBS Code: {city_info['code']}")
        print(f"  Area Code: {city_info['area_code']}")

    print()
    if street and number and city_found:
        print("Formatted address:")
        print(f"  English: {street.title()} {number}, {city_found.title()}")
        print(f"  For forms: Street={street.title()}, Number={number}, City={city_found.title()}")
    else:
        print("Could not fully format. Please provide: Street Name + Number + City")


def list_cities() -> None:
    """List all known cities with CBS codes."""
    print(f"Known Israeli cities ({len(CITY_CODES)}):\n")
    print(f"{'City':<25} {'CBS Code':<10} {'Area Code':<10} {'Hebrew'}")
    print("-" * 70)
    for name, info in sorted(CITY_CODES.items(), key=lambda x: x[1]["code"]):
        print(f"{name:<25} {info['code']:<10} {info['area_code']:<10} {info['hebrew']}")


def main():
    parser = argparse.ArgumentParser(
        description="Israeli Address Lookup and Validation"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # City lookup
    city_parser = subparsers.add_parser("city", help="Look up city by name")
    city_parser.add_argument("name", help="City name")

    # Format address
    fmt_parser = subparsers.add_parser("format", help="Format an address")
    fmt_parser.add_argument("address", help="Address string to format")

    # List cities
    subparsers.add_parser("cities", help="List all known cities")

    args = parser.parse_args()

    if args.command == "city":
        lookup_city(args.name)
    elif args.command == "format":
        format_address(args.address)
    elif args.command == "cities":
        list_cities()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
