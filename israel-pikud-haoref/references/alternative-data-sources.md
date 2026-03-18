# Alternative Data Sources

This reference covers data sources beyond the official oref.org.il endpoints — useful when you need historical data beyond the 3,000-record cap, geo-blocking workarounds, or redundant sources.

---

## Tzofar (tzevaadom.co.il)

A popular third-party alert relay. Tzofar endpoints are **not geo-blocked** — they work from any IP worldwide. Critical caveat: Tzofar **excludes pre-alerts (oref cat 14) and event-concluded messages (oref cat 13)**.

### Endpoints

**Recent alert groups (last ~50):**
```
GET https://api.tzevaadom.co.il/alerts-history
```

**Single alert group by ID:**
```
GET https://api.tzevaadom.co.il/alerts-history/id/{id}
```

**Headers:** Tzofar blocks Python's default `urllib` User-Agent with HTTP 403. Use a browser-like `User-Agent`:

```python
# OK — requests uses its own User-Agent, not blocked
import requests
resp = requests.get(url)

# OK — explicit User-Agent
import urllib.request
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

# FAILS with 403 — sends "Python-urllib/3.x"
urllib.request.urlopen(url)
```

### Historical Data via ID Iteration

There is no bulk download endpoint. Iterate alert group IDs backwards from the latest known ID:

```python
import urllib.request, json, time

def fetch_tzofar_history(start_id, min_date_unix=0, max_gap=100, delay=0.35):
    """Iterate Tzofar alert group IDs backwards for historical data.

    NOTE: Not geo-blocked — works from any IP, unlike oref.org.il

    Args:
        start_id: Highest ID to start from (get lowest id from /alerts-history).
        min_date_unix: Stop when alerts are older than this Unix timestamp.
        max_gap: Stop after this many consecutive 404s.
        delay: Seconds between requests (0.3–0.5 avoids HTTP 429 rate limits).

    Returns: List of alert group dicts, newest first.
    """
    results = []
    consecutive_404s = 0
    current_id = start_id

    while consecutive_404s < max_gap and current_id > 0:
        req = urllib.request.Request(
            f"https://api.tzevaadom.co.il/alerts-history/id/{current_id}",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                group = json.loads(resp.read())
                consecutive_404s = 0
                times = [a["time"] for a in group.get("alerts", [])]
                if times and min(times) < min_date_unix:
                    results.append(group)
                    break
                results.append(group)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                consecutive_404s += 1
                # Optimization: jump back 50 IDs after 10+ consecutive 404s
                if consecutive_404s == 10:
                    current_id -= 50
                    continue
            elif e.code == 429:
                time.sleep(2)   # back off on rate limit, retry same ID
                continue
            else:
                raise
        current_id -= 1
        time.sleep(delay)

    return results
```

**Rate limiting:** Burst requests trigger HTTP 429 after ~13 requests. Use 0.35s delay between requests — ~200 groups per ~70 seconds. IDs are mostly sequential but gaps exist (up to hundreds of consecutive 404s); the 50-ID jump optimization handles large gaps.

### Tzofar Data Model

```json
{
  "id": 5913,
  "description": null,
  "alerts": [
    {
      "time": 1772857423,
      "cities": ["תל אביב - מרכז העיר", "רמת גן - מערב"],
      "threat": 0,
      "isDrill": false
    }
  ]
}
```

- `id` — Sequential alert group ID (iterable for history).
- `alerts[].time` — Unix timestamp (UTC) — normalize to `Asia/Jerusalem` for display.
- `alerts[].cities` — Hebrew location names.
- `alerts[].threat` — Tzofar threat type (see mapping below).
- `alerts[].isDrill` — Filter `true` entries to exclude drills.
- `description` — Usually `null`.

### Threat Type Mapping (Tzofar ↔ Oref)

| Oref Category | Oref Name | Tzofar `threat` |
|--------------|-----------|-----------------|
| 1 | Missiles / Rockets | 0 |
| 2 | Hostile aircraft (UAV) | 5 |
| 3 | Earthquake | 3 |
| 4 | Tsunami | 4 |
| 5 | Radiological | 7 |
| 6 | Hazardous materials | 1 |
| 7 | Terrorist infiltration | 2 |
| 13 | Event concluded | — (not in Tzofar) |
| 14 | Pre-alert | — (not in Tzofar) |

### Timestamp Normalization (Oref ↔ Tzofar)

When combining both sources, normalize to a common timezone:

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo   # stdlib Python 3.9+

IST = ZoneInfo("Asia/Jerusalem")

def normalize_alert_time(raw, source):
    """Normalize any alert timestamp to Israel time.

    source: 'oref_history' | 'oref_aspx' | 'tzofar'
    """
    if source == "oref_history":
        # "2026-03-07 19:33:53" — space-separated, Israel local time
        return datetime.strptime(raw, "%Y-%m-%d %H:%M:%S").replace(tzinfo=IST)
    elif source == "oref_aspx":
        # "2026-03-07T19:35:00" — ISO T-separator, Israel local time
        return datetime.strptime(raw, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=IST)
    elif source == "tzofar":
        # Unix timestamp (UTC)
        return datetime.fromtimestamp(raw, tz=timezone.utc).astimezone(IST)
```

---

## Historical Data Strategy Summary

| Need | Source | Notes |
|------|--------|-------|
| Last few minutes | `alerts.json` (real-time) | Poll every 1–2 seconds |
| Last ~3,000 records (all categories) | `GetAlarmsHistory.aspx` or `AlertsHistory.json` | Hours to weeks depending on activity level |
| Last 50 alert groups (no pre-alerts/cat13) | `api.tzevaadom.co.il/alerts-history` | No geo-blocking |
| Months of history (no pre-alerts) | Iterate Tzofar IDs backwards | No geo-blocking; respect 0.35s rate-limit pacing |
| Complete history including pre-alerts | Your own continuous poller | **No retroactive source exists** — must be running before the period you need |

---

## Community Archive Projects

These projects solve the history cap problem via continuous polling and public archiving:

- **[hasadna/oref-alarms-history](https://github.com/hasadna/oref-alarms-history)** — The Public Knowledge Workshop (Israel's civic data org). Run the scraper yourself to collect.
- **[Meir017/oref-data](https://github.com/Meir017/oref-data)** — Git-based alert aggregator with downloadable `data.json`.
- **[Kaggle: Rocket Alerts dataset](https://www.kaggle.com/datasets/sab30226/rocket-alerts-in-israel-made-by-tzeva-adom)** — Downloadable historical dataset.
- **[idodov/RedAlert](https://github.com/idodov/RedAlert)** — Home Assistant integration with file-based archiving.

---

## Location Data

The `cities.json` from `eladnava/pikud-haoref-api` is the canonical city database (~1,500 locations). Tzofar's own static city files (`/static/cities.json`) returned 404 as of March 2026 — do not rely on them.
