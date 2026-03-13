#!/usr/bin/env python3
"""
Query Israeli Government Open Data Portal (data.gov.il)

Standalone utility for searching and querying datasets from
the Israeli government CKAN-based data portal.

Usage:
    python query_datagov.py search "schools tel aviv"
    python query_datagov.py dataset "dataset-id"
    python query_datagov.py query "resource-id" --limit 50 --filters '{"city":"Haifa"}'
    python query_datagov.py query "resource-id" --fields "field1,field2" --sort "field1 desc"
    python query_datagov.py orgs
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error

BASE_URL = "https://data.gov.il/api/3"


def api_get(endpoint: str, params: dict = None) -> dict:
    """Make a GET request to the data.gov.il CKAN API."""
    url = f"{BASE_URL}/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "israel-gov-api-skill/1.0")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("success"):
                return data.get("result", {})
            else:
                print(f"API error: {data.get('error', 'Unknown error')}", file=sys.stderr)
                sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def search_datasets(query: str, rows: int = 10) -> None:
    """Search for datasets by keyword."""
    result = api_get("action/package_search", {"q": query, "rows": rows})

    count = result.get("count", 0)
    print(f"Found {count} datasets for '{query}':\n")

    for pkg in result.get("results", []):
        name = pkg.get("title", pkg.get("name", "Untitled"))
        pkg_id = pkg.get("name", "")
        org = pkg.get("organization", {}).get("title", "Unknown")
        num_resources = len(pkg.get("resources", []))
        notes = (pkg.get("notes") or "")[:120]

        print(f"  [{pkg_id}]")
        print(f"  Title: {name}")
        print(f"  Organization: {org}")
        print(f"  Resources: {num_resources}")
        if notes:
            print(f"  Description: {notes}...")
        print()


def show_dataset(dataset_id: str) -> None:
    """Show details of a specific dataset."""
    result = api_get("action/package_show", {"id": dataset_id})

    print(f"Dataset: {result.get('title', 'Untitled')}")
    print(f"ID: {result.get('name', '')}")
    print(f"Organization: {result.get('organization', {}).get('title', 'Unknown')}")
    print(f"Last modified: {result.get('metadata_modified', 'Unknown')}")
    print(f"License: {result.get('license_title', 'Unknown')}")
    print()

    resources = result.get("resources", [])
    print(f"Resources ({len(resources)}):")
    for r in resources:
        r_name = r.get("name", r.get("description", "Unnamed"))
        r_id = r.get("id", "")
        r_format = r.get("format", "Unknown")
        r_size = r.get("size")
        datastore = r.get("datastore_active", False)

        print(f"  - {r_name}")
        print(f"    ID: {r_id}")
        print(f"    Format: {r_format}")
        if r_size:
            print(f"    Size: {r_size}")
        print(f"    Datastore queryable: {datastore}")
        print()


def query_datastore(resource_id: str, limit: int = 50, offset: int = 0,
                    filters: str = None, fields: str = None,
                    sort: str = None, q: str = None) -> None:
    """Query a datastore resource."""
    params = {
        "resource_id": resource_id,
        "limit": limit,
        "offset": offset,
    }
    if filters:
        params["filters"] = filters
    if fields:
        params["fields"] = fields
    if sort:
        params["sort"] = sort
    if q:
        params["q"] = q

    result = api_get("action/datastore_search", params)

    total = result.get("total", 0)
    records = result.get("records", [])
    result_fields = result.get("fields", [])

    print(f"Total records: {total}")
    print(f"Showing: {len(records)} (offset {offset})")
    print(f"Fields: {', '.join(f.get('id', '') for f in result_fields)}")
    print()

    for i, record in enumerate(records):
        print(f"--- Record {offset + i + 1} ---")
        for key, value in record.items():
            if key != "_id":
                print(f"  {key}: {value}")
        print()


def list_organizations() -> None:
    """List all publishing organizations."""
    result = api_get("action/organization_list", {"all_fields": True})

    print(f"Organizations ({len(result)}):\n")
    for org in result:
        if isinstance(org, dict):
            name = org.get("display_name", org.get("name", ""))
            org_id = org.get("name", "")
            count = org.get("package_count", 0)
            print(f"  {org_id}: {name} ({count} datasets)")
        else:
            print(f"  {org}")


def main():
    parser = argparse.ArgumentParser(
        description="Query Israeli Government Open Data (data.gov.il)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Search
    search_parser = subparsers.add_parser("search", help="Search datasets")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--rows", type=int, default=10, help="Number of results")

    # Dataset details
    ds_parser = subparsers.add_parser("dataset", help="Show dataset details")
    ds_parser.add_argument("id", help="Dataset ID")

    # Datastore query
    q_parser = subparsers.add_parser("query", help="Query datastore resource")
    q_parser.add_argument("resource_id", help="Resource ID")
    q_parser.add_argument("--limit", type=int, default=50, help="Result limit")
    q_parser.add_argument("--offset", type=int, default=0, help="Result offset")
    q_parser.add_argument("--filters", help='JSON filters (e.g., \'{"field":"value"}\')')
    q_parser.add_argument("--fields", help="Comma-separated field names to return")
    q_parser.add_argument("--sort", help='Sort order (e.g., "field1 desc")')
    q_parser.add_argument("-q", "--search", dest="q", help="Full-text search within resource")

    # Organizations
    subparsers.add_parser("orgs", help="List organizations")

    args = parser.parse_args()

    if args.command == "search":
        search_datasets(args.query, args.rows)
    elif args.command == "dataset":
        show_dataset(args.id)
    elif args.command == "query":
        query_datastore(args.resource_id, args.limit, args.offset,
                        args.filters, args.fields, args.sort, args.q)
    elif args.command == "orgs":
        list_organizations()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
