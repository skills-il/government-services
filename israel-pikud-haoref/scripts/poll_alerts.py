#!/usr/bin/env python3
"""
poll_alerts.py — Command-line poller for Pikud HaOref real-time alerts.

Polls the official oref.org.il alerts endpoint and prints new alerts to stdout.
Supports filtering by city name (Hebrew substring match) and alert category.

NOTE: The official oref.org.il API may geo-block non-Israeli IPs.
      If you receive HTTP 403, deploy on GCP me-west1 (Tel Aviv) for an Israeli IP.

Usage:
    python poll_alerts.py
    python poll_alerts.py --city "תל אביב"
    python poll_alerts.py --city "Tel Aviv" --lang en
    python poll_alerts.py --category 1
    python poll_alerts.py --output json
    python poll_alerts.py --interval 1 --city "חיפה"
    python poll_alerts.py --help

Examples:
    # Monitor all alerts, print Hebrew summary
    python poll_alerts.py

    # Monitor rocket alerts (cat 1) for Tel Aviv only
    python poll_alerts.py --category 1 --city "תל אביב"

    # Output raw JSON for piping to another tool
    python poll_alerts.py --output json | jq .data

    # Fast polling (1s) with English city search
    python poll_alerts.py --interval 1 --city "Haifa" --lang en
"""

import argparse
import json
import sys
import time
from datetime import datetime

try:
    import requests
except ImportError:
    print("ERROR: 'requests' is not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

ALERTS_URL = "https://www.oref.org.il/warningMessages/alert/alerts.json"
HEADERS = {
    "Referer": "https://www.oref.org.il/",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
}

CATEGORIES = {
    1: "Missiles / Rockets",
    2: "Hostile aircraft intrusion",
    3: "Earthquake",
    4: "Tsunami",
    5: "Radiological event",
    6: "Hazardous materials",
    7: "Terrorist infiltration",
    13: "Event concluded",
    14: "Pre-alert (incoming warnings)",
}

DRILL_CATEGORIES = {101, 102, 103, 104, 105, 106, 107}


def fetch_alert(session):
    """Fetch the current alert. Returns parsed dict or None if no active alert."""
    try:
        resp = session.get(ALERTS_URL, headers=HEADERS, timeout=5)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            raise RuntimeError(
                "HTTP 403 Forbidden — likely geo-blocked. "
                "Deploy on GCP me-west1 (Tel Aviv) for an Israeli IP."
            ) from e
        raise
    text = resp.text.lstrip("\ufeff").strip()  # strip UTF-8 BOM
    if not text or text == "[]":
        return None  # no active alert — not an error
    return json.loads(text)


def city_matches(alert, city_filter, lang):
    """Check if city_filter appears in any alert location (substring match)."""
    if not city_filter:
        return True
    locations = alert.get("data", [])
    if lang == "en":
        # English search: case-insensitive substring across the whole data array
        return any(city_filter.lower() in loc.lower() for loc in locations)
    # Hebrew search: substring match (handles "תל אביב - מרכז העיר" when searching "תל אביב")
    return any(city_filter in loc for loc in locations)


def category_matches(alert, category_filter):
    """Check if alert category matches the filter."""
    if category_filter is None:
        return True
    try:
        return int(alert.get("cat", -1)) == category_filter
    except (ValueError, TypeError):
        return False


def format_plain(alert, timestamp):
    """Format alert as a human-readable string."""
    cat_num = alert.get("cat", "?")
    try:
        cat_name = CATEGORIES.get(int(cat_num), f"Category {cat_num}")
    except (ValueError, TypeError):
        cat_name = f"Category {cat_num}"
    locations = ", ".join(alert.get("data", []))
    desc = alert.get("desc", "")
    title = alert.get("title", "")
    lines = [
        f"[{timestamp}] ALERT #{alert.get('id', 'unknown')}",
        f"  Type    : {title} ({cat_name})",
        f"  Where   : {locations}",
        f"  Action  : {desc}",
    ]
    return "\n".join(lines)


def format_json(alert, timestamp):
    """Format alert as JSON with an added timestamp field."""
    out = dict(alert)
    out["_polled_at"] = timestamp
    return json.dumps(out, ensure_ascii=False)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="poll_alerts.py",
        description=(
            "Poll Pikud HaOref real-time alerts from oref.org.il.\n"
            "NOTE: API may geo-block non-Israeli IPs — deploy on GCP me-west1 if you get 403."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python poll_alerts.py\n"
            "  python poll_alerts.py --city \"תל אביב\"\n"
            "  python poll_alerts.py --category 1 --output json\n"
            "  python poll_alerts.py --interval 1 --city \"Haifa\" --lang en\n"
            "  python poll_alerts.py --no-drills\n"
        ),
    )
    parser.add_argument(
        "--city",
        metavar="NAME",
        default=None,
        help=(
            "Filter alerts to a specific city. Hebrew substring match by default "
            "(e.g. 'תל אביב' matches 'תל אביב - מרכז העיר'). "
            "Use --lang en for case-insensitive English match."
        ),
    )
    parser.add_argument(
        "--lang",
        choices=["he", "en"],
        default="he",
        help="Language for --city matching: 'he' (Hebrew substring, default) or 'en' (English, case-insensitive).",
    )
    parser.add_argument(
        "--category",
        type=int,
        metavar="N",
        default=None,
        help=(
            "Filter by category number. "
            "1=Rockets, 2=Aircraft, 3=Earthquake, 4=Tsunami, "
            "5=Radiological, 6=HazMat, 7=Infiltration, 13=Concluded, 14=Pre-alert."
        ),
    )
    parser.add_argument(
        "--no-drills",
        action="store_true",
        default=False,
        help="Suppress drill alerts (categories 101–107).",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        metavar="SECONDS",
        help="Poll interval in seconds (default: 2.0, minimum: 1.0).",
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format: 'text' (human-readable, default) or 'json' (one JSON object per line).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        default=False,
        help="Suppress startup messages and status lines — only print alerts.",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    interval = max(1.0, args.interval)
    seen_ids = set()
    session = requests.Session()

    if not args.quiet:
        print(f"Polling {ALERTS_URL}", file=sys.stderr)
        print(f"  interval : {interval}s", file=sys.stderr)
        if args.city:
            print(f"  city     : {args.city!r} ({args.lang})", file=sys.stderr)
        if args.category is not None:
            cat_name = CATEGORIES.get(args.category, f"Category {args.category}")
            print(f"  category : {args.category} ({cat_name})", file=sys.stderr)
        if args.no_drills:
            print("  drills   : suppressed", file=sys.stderr)
        print("Press Ctrl+C to stop.\n", file=sys.stderr)

    try:
        while True:
            try:
                alert = fetch_alert(session)
            except RuntimeError as e:
                print(f"ERROR: {e}", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                if not args.quiet:
                    print(f"[poll error] {e}", file=sys.stderr)
                time.sleep(interval)
                continue

            if alert:
                alert_id = alert.get("id")

                # Deduplicate
                if alert_id and alert_id in seen_ids:
                    time.sleep(interval)
                    continue
                if alert_id:
                    seen_ids.add(alert_id)

                # Filter drills
                try:
                    cat_int = int(alert.get("cat", 0))
                except (ValueError, TypeError):
                    cat_int = 0
                if args.no_drills and cat_int in DRILL_CATEGORIES:
                    time.sleep(interval)
                    continue

                # Apply filters
                if not category_matches(alert, args.category):
                    time.sleep(interval)
                    continue
                if not city_matches(alert, args.city, args.lang):
                    time.sleep(interval)
                    continue

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if args.output == "json":
                    print(format_json(alert, timestamp), flush=True)
                else:
                    print(format_plain(alert, timestamp), flush=True)

            time.sleep(interval)

    except KeyboardInterrupt:
        if not args.quiet:
            print("\nStopped.", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
