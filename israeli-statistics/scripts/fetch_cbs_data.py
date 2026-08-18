#!/usr/bin/env python3
"""
Fetch Israeli CBS (Central Bureau of Statistics) Data

Standalone utility for querying the Israeli Central Bureau of Statistics.

Economic / price time series (CPI, housing prices, producer prices, building
input costs) come from the CBS Price Indices API at api.cbs.gov.il. That API
is the canonical source for "hamadad" data:
  - https://api.cbs.gov.il/index/catalog/catalog?format=json  (list of indices)
  - https://api.cbs.gov.il/index/data/price?id={code}&format=json  (a series)

NOTE: data.gov.il (organization "lamas") hosts a small set of CBS datasets
(census tabulations, localities, traffic accidents) but does NOT host the
CPI / GDP / unemployment time series. For those, use api.cbs.gov.il.

Usage:
    python fetch_cbs_data.py cpi
    python fetch_cbs_data.py rent-calc --old-cpi 100.0 --new-cpi 103.5 --rent 5000
    python fetch_cbs_data.py search "דירות"
    python fetch_cbs_data.py indicators
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error

# CBS Price Indices API (CPI, housing prices, producer prices, building costs).
CBS_API_BASE = "https://api.cbs.gov.il/index"

# Known index codes from the CBS catalog (mainCode values).
CPI_CODE = 120010      # מדד המחירים לצרכן - כללי (general CPI)
HOUSING_CODE = 40010   # מחירי דירות (apartment prices)


def cbs_api_get(endpoint: str, params: dict = None) -> dict:
    """Make a GET request to the CBS Price Indices API (api.cbs.gov.il)."""
    url = f"{CBS_API_BASE}/{endpoint}"
    query = dict(params or {})
    query.setdefault("format", "json")
    url += "?" + urllib.parse.urlencode(query)

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "israeli-statistics-skill/1.1")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: CBS API did not return JSON. Check the endpoint and "
              "parameters at https://api.cbs.gov.il", file=sys.stderr)
        sys.exit(1)


def search_cbs_indices(query: str) -> None:
    """Search the CBS index catalog for matching price/economic indices."""
    catalog = cbs_api_get("catalog/catalog")
    chapters = catalog.get("chapters", [])

    q = query.strip().lower()
    matches = [c for c in chapters if q in (c.get("chapterName") or "").lower()]

    print(f"CBS indices matching '{query}': {len(matches)} found\n")
    if not matches:
        print("No matching index in the catalog. The catalog covers price and")
        print("economic indices only. For census tabulations, localities, or")
        print("traffic-accident datasets, search data.gov.il (organization 'lamas').")
        return

    for c in matches:
        main_code = c.get("mainCode")
        name = c.get("chapterName", "(no name)")
        order = c.get("chapterOrder", "")
        print(f"  mainCode: {main_code}")
        print(f"  Name: {name}")
        if order:
            print(f"  Chapter order: {order}")
        if main_code:
            print(f"  Series: {CBS_API_BASE}/data/price?id={main_code}&format=json")
        print()

    print("Fetch a series with:")
    print(f"  curl '{CBS_API_BASE}/data/price?id=<mainCode>&format=json'")


def fetch_cpi_info() -> None:
    """Display CPI (Consumer Price Index) latest data from api.cbs.gov.il."""
    print("=== Israeli Consumer Price Index (CPI / Hamadad) ===\n")

    data = cbs_api_get("data/price", {"id": CPI_CODE})
    months = data.get("month", [])
    if months:
        series = months[0]
        print(f"Series: {series.get('name', 'CPI')}  (code {series.get('code', CPI_CODE)})")
        print()
        print(f"  {'Period':<14} {'Index':<10} {'Monthly %':<12} {'Annual %'}")
        print("  " + "-" * 48)
        for entry in series.get("date", [])[:6]:
            year = entry.get("year", "")
            month_desc = entry.get("monthDesc", "")
            period = f"{month_desc} {year}".strip()
            curr_base = entry.get("currBase") or {}
            value = curr_base.get("value", "")
            percent = entry.get("percent", "")
            percent_year = entry.get("percentYear", "")
            print(f"  {period:<14} {str(value):<10} {str(percent):<12} {percent_year}")
        print()
    else:
        print("No CPI data returned. Check api.cbs.gov.il.\n")

    print("CPI Component groups (weights are re-set and republished by CBS):")
    print("  housing (diyur), transportation (tachburah), food (mazon),")
    print("  education & culture, health (briut), furniture & household,")
    print("  clothing & footwear, miscellaneous")
    print("  NOTE: the API does NOT serve component weights. The catalog endpoint")
    print("  returns only chapter names and index codes. Take current weights from")
    print("  https://www.cbs.gov.il/en/Pages/Main%20Price%20Indices.aspx")
    print("  Do not quote a weight from memory.")

    print()
    print("Publication: 15th of the month at 18:30 Israel time; moved to 14:00 on")
    print("the preceding Friday / holiday eve when the 15th falls on a Friday,")
    print("Saturday, holiday, or holiday eve.")
    print("Source: CBS Price Indices API (api.cbs.gov.il), index code 120010")


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
        print("The CPI has decreased. Whether the rent actually falls depends on")
        print("the contract: many Israeli rental contracts include a floor clause")
        print("barring a drop below the base index. Read that clause before")
        print("telling anyone their rent goes down.")
    else:
        print("No change in CPI -- rent remains the same.")

    print()
    print("NOTE: Verify CPI values at api.cbs.gov.il (index code 120010) or")
    print("cbs.gov.il. Adjustments are typically annual, not monthly. Check")
    print("your specific contract terms: which index is the base index (often")
    print("the index KNOWN at signing, i.e. the previous month), whether a")
    print("floor clause bars a decrease, and whether both values share a base")
    print("period. For a disputed amount, prefer the official CBS calculator:")
    print("https://www.cbs.gov.il/en/Pages/Linkage-calculations.aspx")


def show_indicators() -> None:
    """Display key economic indicator summary."""
    print("=== Key Israeli Economic Indicators ===\n")
    print("Price indices (CPI, housing, producer prices, building costs) are")
    print("served by the CBS Price Indices API at api.cbs.gov.il.")
    print("GDP, unemployment, population, and trade series are published as")
    print("CBS tables at cbs.gov.il (not all are exposed via a public API).\n")

    indicators = [
        ("CPI / Inflation", "Monthly", "api.cbs.gov.il, code 120010"),
        ("Housing Price Index", "Monthly", "api.cbs.gov.il, code 40010"),
        ("Producer Prices (PPI)", "Monthly", "api.cbs.gov.il, code 170030"),
        ("Building input (residential)", "Monthly", "api.cbs.gov.il, code 200010"),
        ("Building input (commercial)", "Monthly", "api.cbs.gov.il, code 800010"),
        ("Paving & bridging input", "Monthly", "api.cbs.gov.il, code 240010"),
        ("Agricultural input", "Monthly", "api.cbs.gov.il, code 260010"),
        ("GDP Growth", "Quarterly", "cbs.gov.il National Accounts tables"),
        ("Unemployment Rate", "Monthly", "cbs.gov.il Labour Force Survey"),
        ("Population", "Annual", "cbs.gov.il Population tables"),
        ("Foreign Trade", "Monthly", "cbs.gov.il Foreign Trade tables"),
    ]

    print(f"  {'Indicator':<25} {'Frequency':<12} {'Source'}")
    print("  " + "-" * 70)
    for name, freq, source in indicators:
        print(f"  {name:<25} {freq:<12} {source}")

    print()
    print("Index catalog: https://api.cbs.gov.il/index/catalog/catalog?format=json")
    print("CBS portal:    https://www.cbs.gov.il")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Israeli CBS Statistical Data"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # CPI info
    subparsers.add_parser("cpi", help="CPI latest published values and component group names")

    # Rent calculator
    rent_parser = subparsers.add_parser("rent-calc", help="Rent adjustment calculator")
    rent_parser.add_argument("--old-cpi", type=float, required=True,
                             help="CPI value at contract signing")
    rent_parser.add_argument("--new-cpi", type=float, required=True,
                             help="Current CPI value")
    rent_parser.add_argument("--rent", type=float, required=True,
                             help="Current monthly rent (NIS)")

    # Search
    search_parser = subparsers.add_parser(
        "search", help="Search the CBS index catalog (price/economic indices)")
    search_parser.add_argument("query", help="Search query (Hebrew or English)")

    # Indicators
    subparsers.add_parser("indicators", help="Key economic indicators and sources")

    args = parser.parse_args()

    if args.command == "cpi":
        fetch_cpi_info()
    elif args.command == "rent-calc":
        calculate_rent_adjustment(args.old_cpi, args.new_cpi, args.rent)
    elif args.command == "search":
        search_cbs_indices(args.query)
    elif args.command == "indicators":
        show_indicators()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
