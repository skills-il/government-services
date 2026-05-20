#!/usr/bin/env python3
"""
Query Israeli Knesset Open Data API (OData v3).

Standalone utility for querying the Knesset (Israeli Parliament) OData API
for MK information, bills, factions, and the position-ID lexicon.

Per-MK plenum vote data is NOT available in the public OData service
(KNS_VoteMain and KNS_VoteDetail return 404). For votes, use
https://github.com/hasadna/knesset-data instead.

Usage:
    python query_knesset.py mks --knesset 25
    python query_knesset.py search-mk "Netanyahu"
    python query_knesset.py bills --knesset 25 --keyword "education"
    python query_knesset.py factions --knesset 25
    python query_knesset.py entities
    python query_knesset.py positions
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error

KNESSET_BASE = "https://knesset.gov.il/Odata/ParliamentInfo.svc"


def odata_get(entity: str, filters: str = "", top: int = 50,
              select: str = "") -> list:
    """Query the Knesset OData API."""
    url = f"{KNESSET_BASE}/{entity}" if entity else KNESSET_BASE + "/"
    params = {"$format": "json"}
    if entity:
        params["$top"] = str(top)

    if filters:
        params["$filter"] = filters
    if select:
        params["$select"] = select

    url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "israeli-election-data-skill/1.1")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            # OData v3 returns results in d.results or value
            if "value" in data:
                return data["value"]
            elif "d" in data:
                return data["d"].get("results", [])
            return []
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}", file=sys.stderr)
        if e.code == 404:
            print("Entity not found. Check entity name (case-sensitive).",
                  file=sys.stderr)
            print("Note: KNS_VoteMain and KNS_VoteDetail are NOT exposed "
                  "via the public OData service.", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def get_mks(knesset_num: int) -> None:
    """Get all MKs for a Knesset session (PositionID 43=male, 61=female)."""
    print(f"=== Members of the {knesset_num}th Knesset ===\n")

    results = odata_get(
        entity="KNS_PersonToPosition",
        filters=(
            f"KnessetNum eq {knesset_num} and "
            f"(PositionID eq 43 or PositionID eq 61)"
        ),
        top=120,
    )

    if not results:
        print("No MKs found. Check Knesset number.")
        return

    print(f"Found {len(results)} MK records:\n")
    for mk in results:
        person_id = mk.get("PersonID", "")
        name = f"{mk.get('FirstName', '')} {mk.get('LastName', '')}".strip()
        faction = mk.get("FactionName", "Unknown")
        print(f"  [{person_id}] {name} - {faction}")


def search_mk(name: str) -> None:
    """Search for an MK by name."""
    print(f"=== Searching for: {name} ===\n")

    results = odata_get(
        entity="KNS_Person",
        filters=(
            f"substringof('{name}', LastName) or "
            f"substringof('{name}', FirstName)"
        ),
        top=20,
    )

    if not results:
        print("No results found. Try Hebrew name or different spelling.")
        return

    print(f"Found {len(results)} results:\n")
    for person in results:
        pid = person.get("PersonID", "")
        first = person.get("FirstName", "")
        last = person.get("LastName", "")
        email = person.get("Email", "")
        gender = person.get("GenderDesc", "")

        print(f"  [{pid}] {first} {last}")
        if gender:
            print(f"    Gender: {gender}")
        if email:
            print(f"    Email: {email}")
        print()


def search_bills(knesset_num: int, keyword: str, limit: int) -> None:
    """Search for bills in a Knesset."""
    print(f"=== Bills in {knesset_num}th Knesset matching '{keyword}' ===\n")

    filters = [f"KnessetNum eq {knesset_num}"]
    if keyword:
        filters.append(f"substringof('{keyword}', Name)")

    results = odata_get(
        entity="KNS_Bill",
        filters=" and ".join(filters),
        top=limit,
    )

    if not results:
        print("No bills found. Try Hebrew keywords.")
        return

    status_map = {
        108: "In preparation for first reading",
        118: "Approved in third reading (law)",
        120: "Pending continuity discussion",
        125: "Rejected",
    }

    print(f"Found {len(results)} bills:\n")
    for bill in results:
        bill_id = bill.get("BillID", "")
        name = bill.get("Name", "Untitled")
        status_id = bill.get("StatusID", 0)
        status = status_map.get(status_id, f"Status {status_id}")

        print(f"  Bill #{bill_id}: {name}")
        print(f"  Status: {status}")
        print()


def get_factions(knesset_num: int) -> None:
    """Get all factions in a Knesset session."""
    print(f"=== Factions in the {knesset_num}th Knesset ===\n")

    results = odata_get(
        entity="KNS_Faction",
        filters=f"KnessetNum eq {knesset_num}",
        top=50,
    )

    if not results:
        print("No factions found.")
        return

    print(f"Found {len(results)} factions:\n")
    for faction in results:
        fid = faction.get("FactionID", "")
        name = faction.get("Name", "Unknown")
        print(f"  [{fid}] {name}")


def list_entities() -> None:
    """List all available OData entities at the service root."""
    print("=== Available Knesset OData entities ===\n")

    req = urllib.request.Request(KNESSET_BASE + "/?$format=json")
    req.add_header("User-Agent", "israeli-election-data-skill/1.1")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)

    entities = data.get("value", [])
    print(f"Service exposes {len(entities)} entities:\n")
    for ent in entities:
        print(f"  {ent.get('name', '')}")


def list_positions() -> None:
    """List the PositionID lexicon (used for filtering KNS_PersonToPosition)."""
    print("=== Knesset PositionID lexicon ===\n")

    results = odata_get(entity="KNS_Position", top=100)

    if not results:
        print("Could not retrieve positions.")
        return

    # Sort by PositionID
    results.sort(key=lambda p: p.get("PositionID", 0))
    print(f"Found {len(results)} positions:\n")
    print(f"  {'ID':>6}  Description")
    print(f"  {'-'*6}  {'-'*40}")
    for pos in results:
        pid = pos.get("PositionID", "")
        desc = pos.get("Description", "")
        print(f"  {pid:>6}  {desc}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Query Israeli Knesset Open Data API (OData v3). "
            "Per-MK vote data is not exposed publicly; use hasadna/knesset-data."
        )
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    mks_parser = subparsers.add_parser("mks", help="List MKs for a Knesset")
    mks_parser.add_argument("--knesset", type=int, default=25,
                            help="Knesset number (default: 25)")

    smk_parser = subparsers.add_parser("search-mk", help="Search MK by name")
    smk_parser.add_argument("name", help="Name to search (Hebrew or English)")

    bills_parser = subparsers.add_parser("bills", help="Search bills")
    bills_parser.add_argument("--knesset", type=int, default=25,
                              help="Knesset number")
    bills_parser.add_argument("--keyword", default="",
                              help="Search keyword (Hebrew works best)")
    bills_parser.add_argument("--limit", type=int, default=20,
                              help="Number of results")

    fac_parser = subparsers.add_parser("factions", help="List factions")
    fac_parser.add_argument("--knesset", type=int, default=25,
                            help="Knesset number")

    subparsers.add_parser("entities",
                          help="List all available OData entities")

    subparsers.add_parser("positions",
                          help="List the PositionID lexicon")

    args = parser.parse_args()

    if args.command == "mks":
        get_mks(args.knesset)
    elif args.command == "search-mk":
        search_mk(args.name)
    elif args.command == "bills":
        search_bills(args.knesset, args.keyword, args.limit)
    elif args.command == "factions":
        get_factions(args.knesset)
    elif args.command == "entities":
        list_entities()
    elif args.command == "positions":
        list_positions()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
