#!/usr/bin/env python3
"""
Query Israeli Knesset Open Data API (OData v4).

Standalone utility for querying the Knesset (Israeli Parliament) OData API for
MK information, bills, factions, plenum votes (per-MK), and the position-ID
lexicon.

Targets OData v4 at https://knesset.gov.il/OdataV4/ParliamentInfo/. The legacy
v3 endpoint at https://knesset.gov.il/Odata/ParliamentInfo.svc/ is still up
but does not expose vote tables; this script uses v4 throughout.

Usage:
    python query_knesset.py mks --knesset 25
    python query_knesset.py search-mk "נתניהו"
    python query_knesset.py bills --knesset 25 --keyword "education"
    python query_knesset.py votes --topic "תקציב"
    python query_knesset.py votes --topic "תקציב" --mk 466
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

KNESSET_BASE = "https://knesset.gov.il/OdataV4/ParliamentInfo"


def odata_get(entity: str, filters: str = "", top: int = 50,
              select: str = "", orderby: str = "") -> list:
    """Query the Knesset OData v4 API."""
    url = f"{KNESSET_BASE}/{entity}" if entity else KNESSET_BASE + "/"
    params = {}
    if entity:
        params["$top"] = str(top)
    if filters:
        params["$filter"] = filters
    if select:
        params["$select"] = select
    if orderby:
        params["$orderby"] = orderby

    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "israeli-election-data-skill/1.2")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            # OData v4 returns results in `value`.
            return data.get("value", [])
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}", file=sys.stderr)
        if e.code == 404:
            print("Entity not found. Check entity name (case-sensitive). "
                  "Common slip: 'KNS_IsraelLawClassification' returns 404, "
                  "use 'KNS_IsraelLawClassificiation' (double 'i', intentional "
                  "upstream typo).", file=sys.stderr)
        if e.code == 400:
            print("Bad request. Common slip: using v3 filter syntax. v4 uses "
                  "contains(Field,'text'), not substringof('text', Field).",
                  file=sys.stderr)
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
        faction = mk.get("FactionName", "Unknown")
        print(f"  PersonID={person_id}  Faction={faction}")


def search_mk(name: str) -> None:
    """Search for an MK by name (v4 contains)."""
    print(f"=== Searching for: {name} ===\n")

    results = odata_get(
        entity="KNS_Person",
        filters=(
            f"contains(LastName,'{name}') or "
            f"contains(FirstName,'{name}')"
        ),
        top=20,
    )

    if not results:
        print("No results found. Try Hebrew name or different spelling.")
        return

    print(f"Found {len(results)} results:\n")
    for person in results:
        # v4 PK is `Id` (legacy `PersonID` may also be present in some payloads)
        pid = person.get("Id", person.get("PersonID", ""))
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
    """Search for bills in a Knesset (v4 contains)."""
    print(f"=== Bills in {knesset_num}th Knesset matching '{keyword}' ===\n")

    filters = [f"KnessetNum eq {knesset_num}"]
    if keyword:
        filters.append(f"contains(Name,'{keyword}')")

    results = odata_get(
        entity="KNS_Bill",
        filters=" and ".join(filters),
        top=limit,
        orderby="PublicationDate desc",
    )

    if not results:
        print("No bills found. Try Hebrew keywords.")
        return

    status_map = {
        108: "In preparation for first reading",
        118: "Approved in third reading (law)",
        125: "Rejected",
    }

    print(f"Found {len(results)} bills:\n")
    for bill in results:
        bill_id = bill.get("Id", bill.get("BillID", ""))
        name = bill.get("Name", "Untitled")
        status_id = bill.get("StatusID", 0)
        status = status_map.get(status_id, f"Status {status_id}")

        print(f"  Bill #{bill_id}: {name}")
        print(f"  Status: {status}")
        print()


def search_votes(topic: str, mk_id: int, limit: int) -> None:
    """Find plenum votes by VoteTitle, optionally per-MK result.

    v4-only: KNS_PlenumVote and KNS_PlenumVoteResult are not exposed in v3.
    """
    print(f"=== Plenum votes matching '{topic}' ===\n")

    votes = odata_get(
        entity="KNS_PlenumVote",
        filters=f"contains(VoteTitle,'{topic}')",
        top=limit,
        orderby="VoteDateTime desc",
    )

    if not votes:
        print("No votes found. Try Hebrew keywords (VoteTitle is in Hebrew).")
        return

    print(f"Found {len(votes)} votes:\n")
    for vote in votes:
        vote_id = vote.get("Id", "")
        title = vote.get("VoteTitle", "(no title)")
        when = vote.get("VoteDateTime", "")
        method = vote.get("VoteMethodDesc", "")
        no_conf = vote.get("IsNoConfidenceInGov")

        print(f"  Vote #{vote_id}  {when}")
        print(f"    Title: {title}")
        if method:
            print(f"    Method: {method}")
        if no_conf:
            print("    (No-confidence motion)")

        if mk_id:
            results = odata_get(
                entity="KNS_PlenumVoteResult",
                filters=f"VoteID eq {vote_id} and MkId eq {mk_id}",
                top=1,
            )
            if results:
                r = results[0]
                outcome = r.get("ResultDesc", "(unknown)")
                first = r.get("FirstName", "")
                last = r.get("LastName", "")
                print(f"    MK {first} {last} (id={mk_id}): {outcome}")
            else:
                print(f"    MK id={mk_id}: did not vote")
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
        fid = faction.get("Id", faction.get("FactionID", ""))
        name = faction.get("Name", "Unknown")
        print(f"  [{fid}] {name}")


def list_entities() -> None:
    """List all available OData entities at the service root."""
    print("=== Available Knesset OData v4 entities ===\n")

    # In v4, GET on the service root returns a service document with entity sets.
    req = urllib.request.Request(KNESSET_BASE + "/")
    req.add_header("User-Agent", "israeli-election-data-skill/1.2")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)

    entities = data.get("value", [])
    print(f"Service exposes {len(entities)} entity sets:\n")
    for ent in entities:
        name = ent.get("name") or ent.get("url", "")
        print(f"  {name}")


def list_positions() -> None:
    """List the PositionID lexicon."""
    print("=== Knesset PositionID lexicon ===\n")

    results = odata_get(entity="KNS_Position", top=100)

    if not results:
        print("Could not retrieve positions.")
        return

    results.sort(key=lambda p: p.get("PositionID", p.get("Id", 0)))
    print(f"Found {len(results)} positions:\n")
    print(f"  {'ID':>6}  Description")
    print(f"  {'-'*6}  {'-'*40}")
    for pos in results:
        pid = pos.get("PositionID", pos.get("Id", ""))
        desc = pos.get("Description", "")
        print(f"  {pid:>6}  {desc}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Query Israeli Knesset Open Data API (OData v4). "
            "Per-MK plenum vote data is available via KNS_PlenumVote + "
            "KNS_PlenumVoteResult (v4-only)."
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

    votes_parser = subparsers.add_parser(
        "votes",
        help="Search plenum votes by topic (and optionally per-MK result)"
    )
    votes_parser.add_argument("--topic", required=True,
                              help="Substring to match in VoteTitle (Hebrew)")
    votes_parser.add_argument("--mk", type=int, default=0,
                              help="MK id to look up per-vote result")
    votes_parser.add_argument("--limit", type=int, default=10,
                              help="Number of votes to show")

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
    elif args.command == "votes":
        search_votes(args.topic, args.mk, args.limit)
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
