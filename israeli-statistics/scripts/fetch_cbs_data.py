#!/usr/bin/env python3
"""
Fetch Israeli CBS (Central Bureau of Statistics) Data

Standalone utility for querying the Israeli Central Bureau of Statistics
data through data.gov.il, including CPI, housing prices, and economic indicators.

Usage:
    python fetch_cbs_data.py cpi
    python fetch_cbs_data.py rent-calc --old-cpi 100.0 --new-cpi 103.5 --rent 5000
    python fetch_cbs_data.py search "consumer price"
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error

BASE_URL = "https://data.gov.il/api/3"


def api_get(endpoint: str, params: dict = None) -> dict:
    """Make a GET request to data.gov.il API."""
    url = f"{BASE_URL}/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "israeli-statistics-skill/1.0")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("success"):
                return data.get("result", {})
            else:
                print(f"API error: {data.get('error', 'Unknown')}", file=sys.stderr)
                sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def search_cbs_datasets(query: str) -> None:
    """Search for CBS statistical datasets."""
    result = api_get("action/package_search", {
        "q": query,
        "fq": "organization:cbs",
        "rows": 15
    })

    count = result.get("count", 0)
    datasets = result.get("results", [])

    print(f"CBS Datasets matching '{query}': {count} found\n")

    for ds in datasets:
        title = ds.get("title", "Untitled")
        ds_id = ds.get("name", "")
        modified = ds.get("metadata_modified", "Unknown")[:10]
        resources = len(ds.get("resources", []))
        notes = (ds.get("notes") or "")[:100]

        print(f"  [{ds_id}]")
        print(f"  Title: {title}")
        print(f"  Modified: {modified} | Resources: {resources}")
        if notes:
            print(f"  Notes: {notes}...")
        print()


def fetch_cpi_info() -> None:
    """Display CPI (Consumer Price Index) information and latest data."""
    print("=== Israeli Consumer Price Index (CPI / Hamadad) ===\n")

    # Search for CPI datasets
    result = api_get("action/package_search", {
        "q": "madad mchirim",
        "fq": "organization:cbs",
        "rows": 5
    })

    datasets = result.get("results", [])
    if datasets:
        print("Available CPI datasets on data.gov.il:\n")
        for ds in datasets:
            title = ds.get("title", "Untitled")
            ds_id = ds.get("name", "")
            print(f"  - {title}")
            print(f"    ID: {ds_id}")
            resources = ds.get("resources", [])
            for r in resources[:3]:
                r_id = r.get("id", "")
                r_name = r.get("name", r.get("description", ""))
                r_format = r.get("format", "")
                print(f"    Resource: {r_name} ({r_format}) - {r_id}")
            print()
    else:
        print("No CPI datasets found. Try searching manually.\n")

    print("CPI Component Weights (approximate):")
    print(f"  {'Component':<30} {'Weight'}")
    print("  " + "-" * 40)
    components = [
        ("Housing (diyur)", "~25%"),
        ("Transportation (tachburah)", "~17%"),
        ("Food (mazon)", "~16%"),
        ("Education & culture", "~8%"),
        ("Health (briut)", "~6%"),
        ("Furniture & household", "~5%"),
        ("Clothing & footwear", "~3%"),
        ("Other", "~20%"),
    ]
    for name, weight in components:
        print(f"  {name:<30} {weight}")

    print()
    print("Publication: Monthly, ~15th of following month")
    print("Source: CBS (cbs.gov.il)")


def calculate_rent_adjustment(old_cpi: float, new_cpi: float, rent: float) -> None:
    """Calculate rent adjustment based on CPI change."""
    print("=== Rent Adjustment Calculator (Madad-Linked) ===\n")

    if old_cpi <= 0:
        print("Error: Old CPI must be positive.", file=sys.stderr)
        sys.exit(1)

    change_ratio = new_cpi / old_cpi
    change_percent = (change_ratio - 1) * 100
    new_rent = rent * change_ratio
    difference = new_rent - rent

    print(f"CPI at contract signing: {old_cpi:.2f}")
    print(f"Current CPI:             {new_cpi:.2f}")
    print(f"CPI change:              {change_percent:+.2f}%")
    print()
    print(f"Original rent:           {rent:>10,.0f} NIS")
    print(f"Adjusted rent:           {new_rent:>10,.0f} NIS")
    print(f"Difference:              {difference:>+10,.0f} NIS")
    print()

    if change_percent > 0:
        print("The landlord may increase rent by the CPI change percentage")
        print("if the rental contract includes a madad adjustment clause.")
    elif change_percent < 0:
        print("The CPI has decreased. If the contract includes a madad clause,")
        print("the rent should decrease accordingly.")
    else:
        print("No change in CPI -- rent remains the same.")

    print()
    print("NOTE: Verify CPI values at cbs.gov.il. Adjustments are typically")
    print("annual, not monthly. Check your specific contract terms.")


def show_indicators() -> None:
    """Display key economic indicator summary."""
    print("=== Key Israeli Economic Indicators ===\n")
    print("Data available from CBS (cbs.gov.il):\n")

    indicators = [
        ("GDP Growth", "Quarterly", "National Accounts", "16.x"),
        ("Unemployment Rate", "Monthly", "Labor Force Survey", "12.x"),
        ("CPI / Inflation", "Monthly", "Price Statistics", "12.x"),
        ("Housing Price Index", "Quarterly", "Price Statistics", "12.x"),
        ("Building Starts", "Monthly", "Construction", "19.x"),
        ("Population", "Annual", "Population", "2.x"),
        ("Aliyah (Immigration)", "Monthly", "Migration", "4.x"),
        ("Exports", "Monthly", "Foreign Trade", "16.x"),
        ("Imports", "Monthly", "Foreign Trade", "16.x"),
        ("Average Wage", "Quarterly", "Labor", "12.x"),
    ]

    print(f"  {'Indicator':<25} {'Frequency':<12} {'Subject':<22} {'Table'}")
    print("  " + "-" * 70)
    for name, freq, subject, table in indicators:
        print(f"  {name:<25} {freq:<12} {subject:<22} {table}")

    print()
    print("Access data at: https://www.cbs.gov.il or via data.gov.il API")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Israeli CBS Statistical Data"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # CPI info
    subparsers.add_parser("cpi", help="CPI information and datasets")

    # Rent calculator
    rent_parser = subparsers.add_parser("rent-calc", help="Rent adjustment calculator")
    rent_parser.add_argument("--old-cpi", type=float, required=True,
                             help="CPI value at contract signing")
    rent_parser.add_argument("--new-cpi", type=float, required=True,
                             help="Current CPI value")
    rent_parser.add_argument("--rent", type=float, required=True,
                             help="Current monthly rent (NIS)")

    # Search
    search_parser = subparsers.add_parser("search", help="Search CBS datasets")
    search_parser.add_argument("query", help="Search query")

    # Indicators
    subparsers.add_parser("indicators", help="Key economic indicators")

    args = parser.parse_args()

    if args.command == "cpi":
        fetch_cpi_info()
    elif args.command == "rent-calc":
        calculate_rent_adjustment(args.old_cpi, args.new_cpi, args.rent)
    elif args.command == "search":
        search_cbs_datasets(args.query)
    elif args.command == "indicators":
        show_indicators()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
