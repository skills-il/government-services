#!/usr/bin/env python3
"""
Query Israeli Knesset Open Data API

Standalone utility for querying the Knesset (Israeli Parliament) OData API
for MK information, voting records, bills, and faction data.

Usage:
    python query_knesset.py mks --knesset 25
    python query_knesset.py search-mk "Netanyahu"
    python query_knesset.py votes --knesset 25 --limit 10
    python query_knesset.py vote-detail --vote-id 12345
    python query_knesset.py bills --knesset 25 --keyword "education"
    python query_knesset.py factions --knesset 25
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
    url = f"{KNESSET_BASE}/{entity}"
    params = {"$format": "json", "$top": str(top)}

    if filters:
        params["$filter"] = filters
    if select:
        params["$select"] = select

    url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "israeli-election-data-skill/1.0")
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
            print("Entity not found. Check entity name (case-sensitive).", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def get_mks(knesset_num: int) -> None:
    """Get all MKs for a Knesset session."""
    print(f"=== Members of the {knesset_num}th Knesset ===\n")

    results = odata_get(
        entity="KNS_PersonToPosition",
        filters=f"KnessetNum eq {knesset_num} and PositionID eq 54",
        top=120
    )

    if not results:
        print("No MKs found. Check Knesset number.")
        return

    print(f"Found {len(results)} MKs:\n")
    for mk in results:
        person_id = mk.get("PersonID", "")
        name = f"{mk.get('FirstName', '')} {mk.get('LastName', '')}".strip()
        faction = mk.get("FactionName", "Unknown")
        print(f"  [{person_id}] {name} - {faction}")


def search_mk(name: str) -> None:
    """Search for an MK by name."""
    print(f"=== Searching for MK: {name} ===\n")

    results = odata_get(
        entity="KNS_Person",
        filters=f"substringof('{name}', LastName) or substringof('{name}', FirstName)",
        top=20
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


def get_votes(knesset_num: int, limit: int) -> None:
    """Get recent votes in a Knesset session."""
    print(f"=== Votes in the {knesset_num}th Knesset ===\n")

    results = odata_get(
        entity="KNS_VoteMain",
        filters=f"KnessetNum eq {knesset_num}",
        top=limit
    )

    if not results:
        print("No votes found.")
        return

    print(f"Showing {len(results)} votes:\n")
    for vote in results:
        vote_id = vote.get("VoteID", "")
        topic = vote.get("TopicText", "No topic")
        accepted = vote.get("AcceptedText", "")
        session_id = vote.get("SessionID", "")

        print(f"  Vote #{vote_id} (Session {session_id})")
        print(f"  Topic: {topic}")
        if accepted:
            print(f"  Result: {accepted}")
        print()


def get_vote_detail(vote_id: int) -> None:
    """Get individual MK votes for a specific vote."""
    print(f"=== Vote #{vote_id} Details ===\n")

    results = odata_get(
        entity="KNS_VoteDetail",
        filters=f"VoteID eq {vote_id}",
        top=120
    )

    if not results:
        print("No vote details found.")
        return

    vote_map = {1: "For", 2: "Against", 3: "Abstain", 4: "Absent"}
    counts = {"For": 0, "Against": 0, "Abstain": 0, "Absent": 0}

    for detail in results:
        value = detail.get("VoteValue", 0)
        vote_text = vote_map.get(value, "Unknown")
        counts[vote_text] = counts.get(vote_text, 0) + 1

    print("Summary:")
    for k, v in counts.items():
        bar = "#" * v
        print(f"  {k:>8}: {v:>3} {bar}")
    print()

    # Group by vote value
    for vote_text in ["For", "Against", "Abstain"]:
        vote_val = [k for k, v in vote_map.items() if v == vote_text][0]
        members = [d for d in results if d.get("VoteValue") == vote_val]
        if members:
            print(f"{vote_text} ({len(members)}):")
            for m in members:
                name = f"{m.get('FirstName', '')} {m.get('LastName', '')}".strip()
                faction = m.get("FactionName", "")
                print(f"  - {name} ({faction})")
            print()


def search_bills(knesset_num: int, keyword: str, limit: int) -> None:
    """Search for bills in the Knesset."""
    print(f"=== Bills in {knesset_num}th Knesset matching '{keyword}' ===\n")

    filters = [f"KnessetNum eq {knesset_num}"]
    if keyword:
        filters.append(f"substringof('{keyword}', Name)")

    results = odata_get(
        entity="KNS_Bill",
        filters=" and ".join(filters),
        top=limit
    )

    if not results:
        print("No bills found. Try Hebrew keywords.")
        return

    status_map = {
        108: "In preparation",
        118: "First reading approved",
        120: "Approved (law)",
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
        top=50
    )

    if not results:
        print("No factions found.")
        return

    print(f"Found {len(results)} factions:\n")
    for faction in results:
        fid = faction.get("FactionID", "")
        name = faction.get("Name", "Unknown")
        print(f"  [{fid}] {name}")


def main():
    parser = argparse.ArgumentParser(
        description="Query Israeli Knesset Open Data API"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # MKs
    mks_parser = subparsers.add_parser("mks", help="List MKs")
    mks_parser.add_argument("--knesset", type=int, default=25,
                            help="Knesset number (default: 25)")

    # Search MK
    smk_parser = subparsers.add_parser("search-mk", help="Search MK by name")
    smk_parser.add_argument("name", help="Name to search")

    # Votes
    votes_parser = subparsers.add_parser("votes", help="Get votes")
    votes_parser.add_argument("--knesset", type=int, default=25,
                              help="Knesset number")
    votes_parser.add_argument("--limit", type=int, default=10,
                              help="Number of results")

    # Vote detail
    vd_parser = subparsers.add_parser("vote-detail", help="Get vote details")
    vd_parser.add_argument("--vote-id", type=int, required=True,
                           help="Vote ID")

    # Bills
    bills_parser = subparsers.add_parser("bills", help="Search bills")
    bills_parser.add_argument("--knesset", type=int, default=25,
                              help="Knesset number")
    bills_parser.add_argument("--keyword", default="",
                              help="Search keyword")
    bills_parser.add_argument("--limit", type=int, default=20,
                              help="Number of results")

    # Factions
    fac_parser = subparsers.add_parser("factions", help="List factions")
    fac_parser.add_argument("--knesset", type=int, default=25,
                            help="Knesset number")

    args = parser.parse_args()

    if args.command == "mks":
        get_mks(args.knesset)
    elif args.command == "search-mk":
        search_mk(args.name)
    elif args.command == "votes":
        get_votes(args.knesset, args.limit)
    elif args.command == "vote-detail":
        get_vote_detail(args.vote_id)
    elif args.command == "bills":
        search_bills(args.knesset, args.keyword, args.limit)
    elif args.command == "factions":
        get_factions(args.knesset)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
