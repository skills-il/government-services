---
name: israel-pikud-haoref
description: >-
  Integrate with Israel's Home Front Command (Pikud HaOref) real-time alert
  system — rocket alerts, earthquake warnings, and civil defense notifications.
  Use this skill when working with oref.org.il APIs, "Tzeva Adom", "Red Alert
  Israel", "פיקוד העורף", "צבע אדום", "pikud haoref", real-time alert
  monitoring, or any integration with Israel's civil defense infrastructure.
  Do NOT use for non-Israeli civil defense systems, US/UK weather alerts,
  or generic push-notification frameworks.
license: MIT
allowed-tools: 'Bash(curl:*) Bash(python:*) Bash(node:*) WebFetch'
compatibility: >-
  Code examples require network access. The official oref.org.il API geo-blocks
  non-Israeli IPs; deploy on GCP me-west1 (Tel Aviv) or use Tzofar alternative
  endpoints (no geo-blocking) for historical data.
metadata:
  author: noypearl
  version: 1.0.0
  category: government-services
  tags:
    he:
      - התרעות
      - פיקוד-העורף
      - צבע-אדום
      - טילים
      - חירום
      - ישראל
    en:
      - alerts
      - red-alert
      - israel
      - pikud-haoref
      - tzeva-adom
      - oref
      - civil-defence
  display_name:
    he: פיקוד העורף - התרעות בזמן אמת
    en: Pikud HaOref (Red Alert)
  display_description:
    he: >-
      שילוב מערכת ההתרעות של פיקוד העורף — התרעות טילים, רעידות אדמה ועדכוני
      הגנה אזרחית בזמן אמת. השתמש כאשר עובדים עם oref.org.il, "צבע אדום",
      "פיקוד העורף", "Red Alert", ובוט התרעות.
    en: >-
      Integrate with Israel's Home Front Command (Pikud HaOref) real-time alert
      system — rocket alerts, earthquake warnings, and civil defense
      notifications. Use for oref.org.il APIs, "Tzeva Adom", "Red Alert Israel",
      "פיקוד העורף", "צבע אדום", and Israeli civil defense integrations.
      Do NOT use for non-Israeli civil defense or generic push-notification
      frameworks.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - openclaw
    - antigravity
---

# Pikud HaOref Red Alert Integration

## Instructions

### Step 1: Clarify the Use Case

Ask what the user wants to build:

- **Real-time monitoring** — poll `alerts.json` every 1–2 seconds
- **Notification bot** — Telegram, Slack, Discord (most common)
- **Historical analysis** — query `AlertsHistory.json` or `GetAlarmsHistory.aspx`
- **Dashboard / map** — SSE or WebSocket relay + Leaflet.js client
- **Home Assistant** — point to `oref_alert` HACS or `RedAlert` AppDaemon
- **Location-specific alerts** — cities.json + substring match on Hebrew names

### Step 2: Address Geo-blocking Upfront

**Critical:** The official oref.org.il API may geo-block non-Israeli IPs (CDN/Akamai-based). This is the most common cause of unexpected 403 errors. Test your environment first — blocking is not always consistent for non-Israeli IPs.

**Workaround:** Deploy on GCP `me-west1` (Tel Aviv). Note: `e2-micro` is not free-tier eligible in `me-west1`, but is the cheapest Israeli-IP option.

```bash
# Deploy to GCP Tel Aviv region for an Israeli IP
gcloud compute instances create pikud-haoref \
  --zone=me-west1-a \
  --machine-type=e2-micro \
  --image-family=debian-12 \
  --image-project=debian-cloud \
  --tags=http-server

gcloud compute firewall-rules create allow-pikud-haoref \
  --allow=tcp:8000-8002 --target-tags=http-server
```

**Alternative (no geo-blocking):** Use Tzofar endpoints (`api.tzevaadom.co.il`) for historical data. Caveat: Tzofar excludes pre-alerts (cat 14) and event-concluded messages (cat 13).

### Step 3: Choose Integration Approach

- **Minimal dependencies / full control** → Raw HTTP fetch (see patterns below)
- **Node.js with city enrichment** → `pikud-haoref-api` (npm) — includes cities.json database
- **Python with callbacks** → `python-red-alert` (pip)
- **Home Assistant** → `oref_alert` HACS integration
- **AI assistant integration** → `pikud-a-oref-mcp` MCP server

---

## API Reference

### Real-time Alerts

Poll every 1–2 seconds. This is a narrow snapshot — alerts appear only while a siren is sounding (seconds to ~1 minute).

```
GET https://www.oref.org.il/warningMessages/alert/alerts.json
```

**Required headers:**
```
Referer: https://www.oref.org.il/
X-Requested-With: XMLHttpRequest
Accept: application/json
```

**Response when alert is active:**
```json
{
  "id": "134168709720000000",
  "cat": "1",
  "title": "ירי רקטות וטילים",
  "data": ["תל אביב - מרכז העיר", "רמת גן - מערב"],
  "desc": "היכנסו למרחב המוגן ושהו בו 10 דקות"
}
```

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique alert ID — use for deduplication |
| `cat` | string | Category number (see table below) |
| `title` | string | Alert type in Hebrew |
| `data` | string[] | Affected location names in Hebrew |
| `desc` | string | Protective action instructions in Hebrew |

**Response when no alert:** HTTP 200 with empty body `""` — possibly preceded by UTF-8 BOM `\uFEFF`. Always strip the BOM before attempting JSON.parse. Do NOT treat empty as an error.

**⚠️ Empty `alerts.json` does NOT mean "all clear."** Alerts vanish from this endpoint within seconds. To determine if a situation is ongoing, also check the history endpoint for a matching category 13 "event concluded" entry.

### Alert History

**Primary (recommended — more reliable under load):**
```
GET https://alerts-history.oref.org.il/Shared/Ajax/GetAlarmsHistory.aspx?lang=he&mode=1
```

**Fallback:**
```
GET https://www.oref.org.il/warningMessages/alert/History/AlertsHistory.json
```

Both are hard-capped at **3,000 records with no pagination and no date-range filtering**. During active conflicts, 3,000 records can be exhausted in under 2 hours. History `data` is a **comma-separated string**, not an array (unlike the real-time endpoint).

```json
[{
  "alertDate": "2024-10-15 14:32:00",
  "title": "ירי רקטות וטילים",
  "data": "אשדוד - א,ב,ד,ה",
  "category": 1
}]
```

All timestamps are in **Israel local time (`Asia/Jerusalem`)** — handle DST with `zoneinfo.ZoneInfo("Asia/Jerusalem")` in Python 3.9+.

### Alert Categories

```
GET https://www.oref.org.il/alerts/alertCategories.json
```

| Category | Type (Hebrew) |
|----------|--------------|
| 1 | ירי רקטות וטילים — Missiles / Rockets |
| 2 | חדירת כלי טיס עוין — Hostile aircraft intrusion |
| 3 | רעידת אדמה — Earthquake |
| 4 | צונאמי — Tsunami |
| 5 | אירוע רדיולוגי — Radiological event |
| 6 | חומרים מסוכנים — Hazardous materials |
| 7 | חדירת מחבלים — Terrorist infiltration |
| 13 | האירוע הסתיים — Event conclusion (authoritative "all clear" per location) |
| 14 | בדקות הקרובות צפויות — Pre-alert / incoming alerts warning |
| 101–107 | Drill equivalents of categories 1–7 — filter unless you want drill data |

---

## Implementation Patterns

### 1. Polling Loop — Node.js (`pikud-haoref-api`)

```javascript
// npm install pikud-haoref-api
// NOTE: Deploy on GCP me-west1 (Tel Aviv) if you get 403 geo-blocked errors

const { HaOrefClient } = require('pikud-haoref-api');

const client = new HaOrefClient({
  intervalMs: 2000,   // poll every 2 seconds
  language: 'en',    // or 'he' for Hebrew city names
});

client.on('alert', async (alert) => {
  // alert.cities — English city names resolved via cities.json
  // alert.countdown — seconds to shelter per city
  console.log(`Alert: ${alert.title} in ${alert.cities.join(', ')}`);
});

client.on('error', (err) => console.error('Poll error:', err));
client.start();
```

### 2. Polling Loop — Python (`python-red-alert`)

```python
# pip install python-red-alert
# NOTE: Deploy on GCP me-west1 (Tel Aviv) if you get 403 geo-blocked errors

from red_alert import RedAlert

ra = RedAlert(interval=2)  # poll every 2 seconds

@ra.on_alert
def handle_alert(alert):
    print(f"Alert: {alert.title} in {', '.join(alert.areas)}")

ra.start()  # blocking; use ra.start_async() with aiohttp for async
```

### 3. Raw Fetch with BOM Stripping — JavaScript

```javascript
// NOTE: Deploy on GCP me-west1 (Tel Aviv) if you get 403 geo-blocked errors

const ENDPOINT = 'https://www.oref.org.il/warningMessages/alert/alerts.json';
const HEADERS = {
  'Referer': 'https://www.oref.org.il/',
  'X-Requested-With': 'XMLHttpRequest',
  'Accept': 'application/json',
};

const seen = new Set();

async function pollAlerts() {
  try {
    const res  = await fetch(ENDPOINT, { headers: HEADERS });
    const raw  = await res.text();
    const text = raw.replace(/^\uFEFF/, '').trim(); // strip UTF-8 BOM
    if (!text || text === '[]') return;             // no active alert — not an error
    const alert = JSON.parse(text);
    if (alert.id && !seen.has(alert.id)) {
      seen.add(alert.id);
      console.log(`Alert: ${alert.title}`, alert.data);
    }
  } catch (err) {
    console.error('Poll error:', err.message);
  }
}

setInterval(pollAlerts, 2000);
pollAlerts();
```

### 4. Raw Fetch with BOM Stripping — Python

```python
import requests, json, time

# NOTE: Deploy on GCP me-west1 (Tel Aviv) if you get 403 geo-blocked errors
# For async, replace requests with aiohttp and use asyncio

ENDPOINT = 'https://www.oref.org.il/warningMessages/alert/alerts.json'
HEADERS  = {
    'Referer': 'https://www.oref.org.il/',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0',
}

seen_ids = set()

def poll():
    try:
        resp = requests.get(ENDPOINT, headers=HEADERS, timeout=5)
        text = resp.text.lstrip('\ufeff').strip()   # strip UTF-8 BOM
        if not text or text == '[]':
            return  # no active alert — not an error
        alert = json.loads(text)
        if alert.get('id') and alert['id'] not in seen_ids:
            seen_ids.add(alert['id'])
            print(f"Alert: {alert['title']} in {', '.join(alert['data'])}")
    except Exception as e:
        print(f'Poll error: {e}')

while True:
    poll()
    time.sleep(2)
```

### 5. Telegram Bot Notification

```python
import requests as rq

# NOTE: Deploy on GCP me-west1 (Tel Aviv) if you get 403 geo-blocked errors
# BOT_TOKEN and CHAT_ID should be stored in environment variables, not source code

BOT_TOKEN = "your-bot-token"   # from @BotFather
CHAT_ID   = "your-chat-id"     # channel or user chat ID

def notify_telegram(alert):
    cities = ", ".join(alert["data"])
    text   = f"🚨 {alert['title']}\n📍 {cities}\n⚠️ {alert['desc']}"
    rq.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text},
        timeout=5,
    )

# Wire into the polling loop above — replace print(...) with notify_telegram(alert)
```

For Slack (incoming webhook) and Discord (webhook), the same pattern applies — swap the `rq.post` target and payload format.

### 6. Multi-City Filtering

```python
# NOTE: Deploy on GCP me-west1 (Tel Aviv) if you get 403 geo-blocked errors

WATCHED = {
    "Tel Aviv HQ":          ["תל אביב"],
    "Haifa R&D":            ["חיפה"],
    "Beer Sheva warehouse": ["באר שבע"],
}

def on_new_alert(alert):
    affected = alert.get("data", [])
    for office, hebrew_names in WATCHED.items():
        for name in hebrew_names:
            # Substring match handles "תל אביב - מרכז העיר" when watching "תל אביב"
            if any(name in loc for loc in affected):
                notify_team(office, alert)  # your notification function
                break
```

### 7. Historical Alert Query

```python
import requests, json

# NOTE: Deploy on GCP me-west1 (Tel Aviv) if you get 403 geo-blocked errors
# GetAlarmsHistory.aspx is more reliable than AlertsHistory.json under heavy load

HISTORY_URL = (
    "https://alerts-history.oref.org.il/Shared/Ajax/GetAlarmsHistory.aspx"
    "?lang=he&mode=1"
)
HEADERS = {
    "Referer": "https://www.oref.org.il/",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json",
}

resp    = requests.get(HISTORY_URL, headers=HEADERS, timeout=10)
text    = resp.text.lstrip('\ufeff').strip()  # strip UTF-8 BOM
history = json.loads(text)                    # list of alert records

# Filter rockets (cat 1) mentioning Tel Aviv in the last ~3,000 records
rockets = [
    h for h in history
    if h.get("category") == 1 and "תל אביב" in h.get("data", "")
]
print(f"Found {len(rockets)} rocket alerts for Tel Aviv")
```

---

## Location Data — cities.json

The `pikud-haoref-api` npm package ships `cities.json`: ~1,500 Israeli locations with multi-language names, GPS coordinates, zone assignments, and time-to-shelter values.

```json
{
  "id": 511,
  "name": "אבו גוש",
  "name_en": "Abu Ghosh",
  "name_ru": "Абу Гош",
  "name_ar": "أبو غوش",
  "zone": "שפלת יהודה",
  "zone_en": "Judean Lowlands",
  "lat": 31.80686,
  "lng": 35.11038,
  "countdown": 90,
  "value": "אבו גוש"
}
```

**Key fields:**
- `countdown` — seconds to shelter (0 for Gaza-border communities, up to 90 for northern Israel). Always report this — it is life-safety critical.
- `value` — use for matching against alert `data` array entries.
- `lat` / `lng` — use for map markers and proximity queries.

**Matching strategy:** Alert location strings include sub-area suffixes (e.g., `"תל אביב - מרכז העיר"`). Use **substring match** (`"תל אביב" in loc`) rather than exact equality.

**English-to-Hebrew resolution:** Search `name_en` with fuzzy matching — `"Ashdod"`, `"Ashdod"`, `"Ashkelon"` → Hebrew `value`. Use `name_ru` / `name_ar` for Russian- and Arabic-speaking users.

---

## Community Libraries

| Language | Library | Install | Notes |
|----------|---------|---------|-------|
| Node.js | `pikud-haoref-api` | `npm install pikud-haoref-api` | Includes cities.json, English city resolution, countdown times |
| Python | `python-red-alert` | `pip install python-red-alert` | Callback-based; supports async via `aiohttp` |
| C# | `RedAlert` | NuGet | Multi-language (he/en/ru/ar) |
| Docker | `orefAlerts` | Docker Hub | Containerized poller with webhook output |
| MCP server | `pikud-a-oref-mcp` | See repo | AI assistant integration via FastAPI SSE on port 8000 |
| Home Assistant | `oref_alert` | HACS | Auto-configures from HA home location; `sensor.oref_alert` + `_time_to_shelter` entities |
| Home Assistant | `RedAlert` | AppDaemon | Script-based automations with fine-grained control |

---

## Error Handling

| Condition | Meaning | Action |
|-----------|---------|--------|
| HTTP 403 | Geo-blocked, or missing `/alert/` path segment | Deploy on GCP me-west1; verify URL includes `/alert/` segment |
| HTTP 200, empty body | No active alert | Normal state — do not raise an error |
| `\uFEFF` at start | UTF-8 BOM | Strip with `.lstrip('\ufeff')` before JSON.parse |
| Malformed JSON | Occasional history endpoint corruption under load | Retry after 2–3 seconds |
| History returns empty under load | `AlertsHistory.json` degrades during conflicts | Switch to `GetAlarmsHistory.aspx` on `alerts-history.oref.org.il` |

---

## Security Notes

- No authentication required for any endpoint — pure public read API.
- No personal data involved.
- No secrets to manage for the Pikud HaOref API itself.
- Store Telegram `BOT_TOKEN`, Slack webhook URLs, and Discord webhook URLs in environment variables — never hardcode in source.
- Rate-limit pollers to 1–2 second intervals; faster polling risks IP-level blocking.

---

## Examples

### Example 1: Telegram bot for rocket alerts
1. Address geo-blocking upfront — suggest GCP me-west1 or test from local first.
2. Use Pattern 4 (raw Python polling loop) with `on_new_alert` calling Pattern 5 (Telegram notify).
3. Filter by `alert.get("cat") == "1"` if you want rockets/missiles only.
4. Suggest storing `BOT_TOKEN` and `CHAT_ID` in `.env`.
5. Result: Bot running in Tel Aviv region, sends message on every new rocket alert.

### Example 2: "Is there an alert in Ashkelon right now?"
1. Fetch `alerts.json` and strip BOM.
2. Substring-match `"אשקלון"` against `data` array — handles sub-areas `"אשקלון - צפון"`, `"אשקלון - דרום"`.
3. Also query history and check that no cat 13 "event concluded" has been received for Ashkelon since the last cat 1–7 alert.
4. Report time-to-shelter: Ashkelon = 30 seconds (`countdown: 30` in cities.json).

### Example 3: Live alert map dashboard
1. Server-side: polling loop → fan out via SSE or WebSocket (do not have browsers hit oref.org.il directly).
2. Client-side: Leaflet.js + OpenStreetMap tiles + markers placed from cities.json `lat`/`lng`.
3. Enrich each marker tooltip with zone name (`zone_en`) and time-to-shelter (`countdown`).
4. Update markers in real time; fade or remove markers after cat 13 "event concluded" is received.

### Example 4: Home Assistant integration
1. Install `oref_alert` via HACS in the Home Assistant UI.
2. Configure with your home city — the integration auto-resolves Hebrew location names.
3. Entities: `sensor.oref_alert` (current alert state) and `sensor.oref_alert_time_to_shelter` (countdown in seconds).
4. Common automations: flash smart lights red, pause media, lock doors, announce via TTS speakers.

### Example 5: Historical alert analysis (last week)
1. Decide if you need pre-alerts (cat 14) — if yes, you must have had a continuous poller running; no retroactive source exists.
2. For actual threat alerts only: fetch `GetAlarmsHistory.aspx?lang=he&mode=1`.
3. During high-intensity periods, 3,000 records may cover only a few hours — use Tzofar archive for longer windows (see `references/alternative-data-sources.md`).
4. Normalize timestamps to `Asia/Jerusalem` timezone before grouping by day/hour.

---

## Bundled Resources

### Scripts
- `scripts/poll_alerts.py` — Command-line poller for Pikud HaOref real-time alerts. Supports filtering by city, category, and output format (plain text or JSON). Includes BOM stripping and deduplication. Run: `python scripts/poll_alerts.py --help`

### References
- `references/alternative-data-sources.md` — Tzofar (tzevaadom.co.il) API endpoints, category mapping between oref and Tzofar, community archive projects (hasadna, Meir017), and strategies for historical data beyond the 3,000-record cap. Consult when you need historical data older than a few hours or a geo-blocking-free alternative.
- `references/community-libraries.md` — Detailed guide to all community-maintained libraries: `pikud-haoref-api` (Node.js), `python-red-alert`, `RedAlert` (C#), `orefAlerts` (Docker), `pikud-a-oref-mcp` (MCP), and Home Assistant integrations. Includes install commands, API signatures, and known limitations. Consult when choosing a library or debugging library-specific behavior.

---

## Gotchas

- **UTF-8 BOM** — The real-time endpoint inconsistently emits `\uFEFF` before the JSON. Strip it with `.lstrip('\ufeff')` (Python) or `.replace(/^\uFEFF/, '')` (JS) before every JSON.parse.
- **Empty body ≠ error** — HTTP 200 with empty body means no active alert. Handle it by returning early.
- **`data` field type differs by endpoint** — Real-time: array of strings. History: single comma-separated string. Do not assume either format in shared code.
- **3,000-record history cap** — No pagination exists on either history endpoint. During March 2026 conflict, the cap was exhausted in ~97 minutes. Use Tzofar archive or a self-hosted continuous poller for longer history.
- **Category 14 pre-alerts are not retroactively available** — Tzofar excludes them entirely. The only way to have historical pre-alert data is to run your own continuous poller before the period you need.
- **Israel timezone** — All oref timestamps are in `Asia/Jerusalem` (Israel local time), not UTC. Use `zoneinfo.ZoneInfo("Asia/Jerusalem")` for DST-safe parsing in Python 3.9+.
- **Drill alerts** — Categories 101–107 are national drill equivalents of 1–7. Filter them unless you specifically want drill data.
- **URL path is case-insensitive, but `/alert/` segment is required** — `/warningMessages/alert/alerts.json` ✓ — `/warningMessages/alerts.json` → 403.
- **Multiple simultaneous alerts** — During heavy barrages, multiple alert types can be active at once. Always handle `data` as an array, not a single location.
- **Don't hammer the API** — Poll every 1–2 seconds maximum. The endpoint updates no faster than that, and excess requests risk IP-level blocks.

---

## Troubleshooting

### Error: "403 Forbidden" from oref.org.il
**Cause A:** Geo-blocking — non-Israeli IP address.
**Solution:** Deploy on GCP `me-west1` (Tel Aviv). Try from local first — blocking is not always consistent.
**Cause B:** Missing `/alert/` path segment in URL.
**Solution:** Confirm URL is `https://www.oref.org.il/warningMessages/alert/alerts.json`.

### Error: "JSON parse error" or "Unexpected token"
**Cause:** UTF-8 BOM `\uFEFF` at start of response, or occasional malformed JSON from history endpoint.
**Solution:** Strip BOM before parsing. If from history endpoint, retry after 2–3 seconds.

### Error: "History always returns empty body"
**Cause:** `AlertsHistory.json` degrades under high server load during conflicts.
**Solution:** Switch to `GetAlarmsHistory.aspx` on `alerts-history.oref.org.il` — this subdomain stays available during escalation.

### Error: "City not found in alert data"
**Cause:** Alert `data` entries include sub-area suffixes (e.g., `"תל אביב - מרכז העיר"`).
**Solution:** Use substring match rather than exact equality: `"תל אביב" in location_string`.

### Concern: "Alert disappeared from alerts.json after 10 seconds"
**Cause:** Expected — `alerts.json` is a live snapshot, not a persistent status.
**Solution:** Deduplicate by `id`. Store alerts locally as they appear. Use the history endpoint to catch anything missed between polls.

---

## Credits

API knowledge, endpoint details, BOM handling patterns, geo-blocking workarounds, and community library references are derived from the [yaniv-golan/pikud-haoref-alerts](https://github.com/yaniv-golan/pikud-haoref-alerts) Claude plugin by Yaniv Golan (MIT).
