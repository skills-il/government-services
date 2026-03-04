#!/usr/bin/env python3
"""
Knesset Open Data API Client

Query the Knesset Open Data API for bills, votes, MK information,
and committee sessions.

Usage:
    python fetch_knesset.py --help
    python fetch_knesset.py bills --keyword "פרטיות" --top 10
    python fetch_knesset.py bill --id 12345
    python fetch_knesset.py members --current
    python fetch_knesset.py committees --name "מדע"
    python fetch_knesset.py votes --bill-id 12345
    python fetch_knesset.py tech-alerts --days 90
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from urllib.parse import quote

try:
    import requests
except ImportError:
    print("Error: 'requests' package required. Install with: pip install requests")
    sys.exit(1)

BASE_URL = "https://main.knesset.gov.il/Activity/Info/api/v2"

# Tech-related keywords for legislation alerts
TECH_KEYWORDS = [
    "סייבר",
    "פרטיות",
    "בינה מלאכותית",
    "טכנולוגיה",
    "מידע אישי",
    "אבטחת מידע",
    "קניין רוחני",
    "פינטק",
    "עבודה מרחוק",
    "הייטק",
    "דיגיטלי",
    "אלגוריתם",
]


def make_request(endpoint: str, params: dict = None) -> dict:
    """Make a request to the Knesset Open Data API."""
    url = f"{BASE_URL}/{endpoint}"
    headers = {"Accept": "application/json"}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def search_bills(keyword: str, top: int = 20, knesset_num: int = None, recent_days: int = None) -> dict:
    """Search for bills by keyword."""
    filters = []
    if keyword:
        filters.append(f"contains(Name,'{keyword}')")
    if knesset_num:
        filters.append(f"KnessetNum eq {knesset_num}")
    if recent_days:
        since = (datetime.now() - timedelta(days=recent_days)).strftime("%Y-%m-%dT00:00:00Z")
        filters.append(f"LastUpdatedDate ge {since}")

    params = {
        "$top": top,
        "$orderby": "LastUpdatedDate desc",
    }
    if filters:
        params["$filter"] = " and ".join(filters)

    return make_request("bills", params)


def get_bill(bill_id: int) -> dict:
    """Get details for a specific bill."""
    return make_request(f"bills({bill_id})")


def list_members(current_only: bool = True, party: str = None) -> dict:
    """List Knesset members."""
    filters = []
    if current_only:
        filters.append("IsCurrent eq true")
    if party:
        filters.append(f"contains(FactionName,'{party}')")

    params = {"$orderby": "LastName"}
    if filters:
        params["$filter"] = " and ".join(filters)

    return make_request("members", params)


def list_committees(name: str = None, knesset_num: int = None, top: int = 20) -> dict:
    """List committee sessions."""
    filters = []
    if name:
        filters.append(f"contains(TypeDesc,'{name}')")
    if knesset_num:
        filters.append(f"KnessetNum eq {knesset_num}")

    params = {
        "$top": top,
        "$orderby": "StartDate desc",
    }
    if filters:
        params["$filter"] = " and ".join(filters)

    return make_request("committees", params)


def get_votes(bill_id: int = None, session_id: int = None) -> dict:
    """Get vote details."""
    filters = []
    if bill_id:
        filters.append(f"BillID eq {bill_id}")
    if session_id:
        filters.append(f"SessionID eq {session_id}")

    params = {"$orderby": "Date desc"}
    if filters:
        params["$filter"] = " and ".join(filters)

    return make_request("votes", params)


def tech_alerts(days: int = 90, top: int = 20) -> dict:
    """Find recent tech-related legislation."""
    results = []
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")

    for keyword in TECH_KEYWORDS:
        params = {
            "$filter": f"contains(Name,'{keyword}') and LastUpdatedDate ge {since}",
            "$top": 5,
            "$orderby": "LastUpdatedDate desc",
        }
        data = make_request("bills", params)
        if "value" in data:
            for bill in data["value"]:
                bill["_matched_keyword"] = keyword
                if not any(r.get("ID") == bill.get("ID") for r in results):
                    results.append(bill)

    # Sort by date and limit
    results.sort(key=lambda x: x.get("LastUpdatedDate", ""), reverse=True)
    return {"value": results[:top], "total": len(results), "keywords_searched": TECH_KEYWORDS}


def format_output(data: dict, output_format: str = "json") -> str:
    """Format API response for display."""
    if output_format == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)

    # Simple text format
    if "error" in data:
        return f"Error: {data['error']}"

    items = data.get("value", [data] if "Name" in data else [])
    lines = []
    for item in items:
        if "Name" in item:
            status = item.get("StatusTypeDesc", "N/A")
            date = item.get("LastUpdatedDate", "N/A")
            if date and date != "N/A":
                date = date[:10]
            lines.append(f"[{status}] {item['Name']} (Updated: {date})")
        elif "FirstName" in item:
            faction = item.get("FactionName", "N/A")
            lines.append(f"{item.get('FirstName', '')} {item.get('LastName', '')} - {faction}")
        else:
            lines.append(json.dumps(item, ensure_ascii=False))
    return "\n".join(lines) if lines else "No results found."


def main():
    parser = argparse.ArgumentParser(description="Knesset Open Data API Client")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="Output format")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # bills
    bills_parser = subparsers.add_parser("bills", help="Search bills by keyword")
    bills_parser.add_argument("--keyword", "-k", required=True, help="Search keyword (Hebrew)")
    bills_parser.add_argument("--top", "-t", type=int, default=20, help="Max results")
    bills_parser.add_argument("--knesset", type=int, help="Knesset number")
    bills_parser.add_argument("--days", type=int, help="Only bills updated in last N days")

    # bill
    bill_parser = subparsers.add_parser("bill", help="Get bill details by ID")
    bill_parser.add_argument("--id", required=True, type=int, help="Bill ID")

    # members
    members_parser = subparsers.add_parser("members", help="List Knesset members")
    members_parser.add_argument("--current", action="store_true", help="Current members only")
    members_parser.add_argument("--party", help="Filter by party name (Hebrew)")

    # committees
    comm_parser = subparsers.add_parser("committees", help="List committee sessions")
    comm_parser.add_argument("--name", help="Committee name filter (Hebrew)")
    comm_parser.add_argument("--knesset", type=int, help="Knesset number")
    comm_parser.add_argument("--top", type=int, default=20, help="Max results")

    # votes
    votes_parser = subparsers.add_parser("votes", help="Get vote details")
    votes_parser.add_argument("--bill-id", type=int, help="Filter by bill ID")
    votes_parser.add_argument("--session-id", type=int, help="Filter by session ID")

    # tech-alerts
    tech_parser = subparsers.add_parser("tech-alerts", help="Find tech-related legislation")
    tech_parser.add_argument("--days", type=int, default=90, help="Lookback period in days")
    tech_parser.add_argument("--top", type=int, default=20, help="Max results")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "bills":
        result = search_bills(args.keyword, args.top, args.knesset, args.days)
    elif args.command == "bill":
        result = get_bill(args.id)
    elif args.command == "members":
        result = list_members(args.current, args.party)
    elif args.command == "committees":
        result = list_committees(args.name, args.knesset, args.top)
    elif args.command == "votes":
        result = get_votes(args.bill_id, args.session_id)
    elif args.command == "tech-alerts":
        result = tech_alerts(args.days, args.top)
    else:
        parser.print_help()
        sys.exit(1)

    print(format_output(result, args.format))


if __name__ == "__main__":
    main()
