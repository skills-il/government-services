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
import ssl
import urllib.request
import urllib.parse
import urllib.error

# A python.org build on macOS ships without a populated CA store, so urllib
# cannot verify data.gov.il's certificate and every call dies with an opaque
# CERTIFICATE_VERIFY_FAILED. curl on the same machine works, which is what makes
# it confusing. Prefer certifi's bundle when it is installed.
try:
    import certifi

    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CTX = None

BASE_URL = "https://data.gov.il/api/3"


def api_get(endpoint: str, params: dict = None) -> dict:
    """Make a GET request to the data.gov.il CKAN API."""
    url = f"{BASE_URL}/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "israel-gov-api-skill/1.4.0")

    try:
        with urllib.request.urlopen(req, timeout=30, context=_SSL_CTX) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("success"):
                return data.get("result", {})
            else:
                print(f"API error: {data.get('error', 'Unknown error')}", file=sys.stderr)
                sys.exit(1)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(
                "HTTP 404 with an HTML body. The request never reached the SQL "
                "or datastore layer, and this generic error page has three "
                "possible causes:\n"
                "  1. the WAF matched an injection-signature substring in your "
                "SQL (`count(`, `1=1`, `UNION`). Use sum(1) instead of "
                "count(*), or take a row count from datastore_search's total.\n"
                "  2. the resource_id does not exist. Re-resolve it with "
                "`dataset <slug>`; resource IDs rotate.\n"
                "  3. the action name is wrong.\n"
                "Disambiguate by running a known-good query on the same "
                "resource: sql 'SELECT * FROM \"<resource_id>\" LIMIT 1'.\n"
                "A genuine SQL error looks different: JSON with HTTP 409 and a "
                "psycopg2 message.",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"HTTP error {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        if isinstance(e.reason, ssl.SSLCertVerificationError):
            print(
                "SSL certificate verification failed. This is a local CA-store "
                "problem, not a data.gov.il outage (curl on this machine will "
                "work). Fix it with one of:\n"
                "  pip install certifi\n"
                "  /Applications/Python\\ 3.x/Install\\ Certificates.command   "
                "(macOS python.org builds)\n"
                "  export SSL_CERT_FILE=$(python3 -c 'import certifi; "
                "print(certifi.where())')",
                file=sys.stderr,
            )
            sys.exit(1)
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


def run_sql(sql: str, as_json: bool = False) -> None:
    """Run a SQL query via datastore_search_sql.

    This is the only route to real keyset paging (WHERE _id > N ORDER BY _id)
    and to aggregation. Note that the WAF rejects SQL containing `count(`,
    `1=1` or `UNION` with an HTML 404 rather than a JSON error; use `sum(1)`
    in place of `count(*)`.
    """
    result = api_get("action/datastore_search_sql", {"sql": sql})
    records = result.get("records", [])
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"Rows: {len(records)}")
    print()
    for i, record in enumerate(records):
        print(f"--- Row {i + 1} ---")
        for key, value in record.items():
            if key == "_full_text":
                continue
            print(f"  {key}: {value}")
        print()


def query_datastore(resource_id: str, limit: int = 50, offset: int = 0,
                    filters: str = None, fields: str = None,
                    sort: str = None, q: str = None,
                    records_format: str = None, as_json: bool = False) -> None:
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
    if records_format:
        params["records_format"] = records_format

    result = api_get("action/datastore_search", params)

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    total = result.get("total", 0)
    records = result.get("records", [])
    result_fields = result.get("fields", [])

    print(f"Total records: {total}")
    if isinstance(records, list):
        print(f"Showing: {len(records)} (offset {offset})")
    print(f"Fields: {', '.join(f.get('id', '') for f in result_fields)}")
    print()

    if not isinstance(records, list):
        # records_format=csv/tsv returns a single headerless string. The column
        # names live only in result["fields"], in order, so print them first or
        # the Hebrew columns silently misalign.
        print(",".join(f.get("id", "") for f in result_fields))
        print(records)
        return

    for i, record in enumerate(records):
        print(f"--- Record {offset + i + 1} ---")
        for key, value in record.items():
            # _id is kept: it is what you need for keyset paging
            # (WHERE _id > <last _id>) via the `sql` subcommand.
            if key == "_full_text":
                continue
            print(f"  {key}: {value}")
        print()


def list_organizations() -> None:
    """List all publishing organizations."""
    result = api_get("action/organization_list", {"all_fields": True})

    print(f"Organizations ({len(result)}):\n")
    for org in result:
        if isinstance(org, dict):
            # data.gov.il returns `title` and `resources_count`; it does NOT
            # return CKAN's `display_name` or `package_count` (both come back
            # null), which is why an earlier version printed the slug twice and
            # "(0 datasets)" for every organization.
            org_id = org.get("name", "")
            name = org.get("display_name") or org.get("title") or org_id
            count = org.get("package_count")
            if count is None:
                count = org.get("resources_count")
            suffix = f" ({count} resources)" if count is not None else ""
            print(f"  {org_id}: {name}{suffix}")
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

    q_parser.add_argument("--records-format", dest="records_format",
                          choices=["objects", "lists", "csv", "tsv"],
                          help="Response record shape (csv/tsv are headerless; "
                               "the header is printed from result.fields)")
    q_parser.add_argument("--json", dest="as_json", action="store_true",
                          help="Emit the raw CKAN result as JSON, for chaining")

    # SQL
    sql_parser = subparsers.add_parser(
        "sql", help="Run SQL via datastore_search_sql (keyset paging, aggregation)")
    sql_parser.add_argument("sql", help='SQL, e.g. \'SELECT * FROM "<resource_id>" LIMIT 5\'')
    sql_parser.add_argument("--json", dest="as_json", action="store_true",
                            help="Emit the raw CKAN result as JSON")

    # Organizations
    subparsers.add_parser("orgs", help="List organizations")

    args = parser.parse_args()

    if args.command == "search":
        search_datasets(args.query, args.rows)
    elif args.command == "dataset":
        show_dataset(args.id)
    elif args.command == "query":
        query_datastore(args.resource_id, args.limit, args.offset,
                        args.filters, args.fields, args.sort, args.q,
                        args.records_format, args.as_json)
    elif args.command == "sql":
        run_sql(args.sql, args.as_json)
    elif args.command == "orgs":
        list_organizations()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
