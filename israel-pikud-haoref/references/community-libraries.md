# Community Libraries Reference

All community-maintained libraries for integrating with the Pikud HaOref alert system. Consult this file when choosing a library, looking up API signatures, or debugging library-specific behavior.

---

## Node.js — `pikud-haoref-api`

**Install:** `npm install pikud-haoref-api`
**Repo:** https://github.com/eladnava/pikud-haoref-api
**Maintainer:** Eladnava
**Stars:** ~200+

### What it provides
- EventEmitter-based polling client with configurable interval
- cities.json database (~1,500 locations) bundled — English city names, Hebrew names, GPS coordinates, zone assignments, time-to-shelter (`countdown` in seconds)
- Automatic BOM stripping and deduplication
- Language selection (`he` / `en` / `ru` / `ar`) for city name output

### API

```javascript
const { HaOrefClient } = require('pikud-haoref-api');

const client = new HaOrefClient({
  intervalMs: 2000,   // poll interval (ms) — recommended: 1000–2000
  language: 'en',    // city name language in events: 'he' | 'en' | 'ru' | 'ar'
});

client.on('alert', (alert) => {
  alert.id         // string — unique alert ID
  alert.title      // string — alert type in Hebrew
  alert.data       // string[] — raw Hebrew location names from API
  alert.cities     // object[] — enriched city objects from cities.json
  alert.countdown  // number — shortest time-to-shelter across affected cities (seconds)
  alert.desc       // string — protective instructions
  alert.cat        // string — category number
});

client.on('error', (err) => { /* handle */ });
client.start();
client.stop();
```

### cities.json structure

Available at `node_modules/pikud-haoref-api/cities.json` or https://github.com/eladnava/pikud-haoref-api/blob/master/cities.json:

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

### Known limitations
- Geo-blocking: uses the same oref.org.il endpoint — deploy on GCP me-west1 if you get 403
- cities.json may lag behind new settlements added by Pikud HaOref
- No built-in support for historical queries — use raw `requests` for that

---

## Python — `python-red-alert`

**Install:** `pip install python-red-alert`
**PyPI:** https://pypi.org/project/python-red-alert/

### What it provides
- Callback-based polling with `@ra.on_alert` decorator
- Sync (blocking) and async modes
- Basic city name resolution

### API

```python
from red_alert import RedAlert

ra = RedAlert(interval=2)  # poll interval in seconds

@ra.on_alert
def handle(alert):
    alert.title    # str — Hebrew alert type
    alert.areas    # list[str] — affected location names
    alert.cat      # str — category number

ra.start()           # blocking
ra.start_async()     # returns coroutine — use with asyncio / aiohttp
ra.stop()
```

### Known limitations
- Does not bundle cities.json — no countdown times or GPS coordinates
- For city enrichment, download cities.json from the `pikud-haoref-api` npm package separately

---

## C# — `RedAlert`

**Install:** NuGet: `Install-Package RedAlert`
**Repo:** https://github.com/idodov/RedAlert

### What it provides
- Multi-language support: Hebrew, English, Russian, Arabic
- Polling client with event-based callback
- cities.json bundled as embedded resource
- Home Assistant file-based archiving integration

### API

```csharp
var client = new RedAlertClient(language: Language.English);
client.OnAlert += (alert) => {
    Console.WriteLine($"{alert.Title}: {string.Join(", ", alert.Locations)}");
    Console.WriteLine($"Time to shelter: {alert.Countdown}s");
};
client.Start();
```

### Known limitations
- Same geo-blocking applies — needs Israeli IP for real-time endpoint
- Less actively maintained than the Node.js library

---

## Docker — `orefAlerts`

**Docker Hub:** `orefAlerts`

### What it provides
- Containerized poller — no host language dependency
- Webhook output on new alert (configurable URL + payload)
- Deployable directly to GCP me-west1 Cloud Run or a VM

### Usage

```bash
docker run -e WEBHOOK_URL=https://your-hook/endpoint orefAlerts
```

Environment variables:
- `WEBHOOK_URL` — POST destination for each new alert (JSON body)
- `POLL_INTERVAL` — seconds between polls (default: 2)
- `CITY_FILTER` — optional Hebrew city substring filter

### Known limitations
- No cities.json enrichment (countdown, GPS)
- Webhook payload format is fixed — for custom formatting, use the Node.js or Python library

---

## MCP Server — `pikud-a-oref-mcp`

**Purpose:** Exposes the Pikud HaOref alert stream as an MCP (Model Context Protocol) server for AI assistant integration (Claude, Cursor, etc.).

### What it provides
- FastAPI server with SSE endpoint at `/api/alerts-stream` (port 8000)
- Polls oref.org.il once, fans out to multiple SSE clients — prevents hammering the official endpoint
- REST endpoint `/api/current-alert` for polling clients
- MCP tool definitions for AI assistants to query live alerts

### Architecture

```
oref.org.il ← polls every 2s ← pikud-a-oref-mcp (port 8000)
                                        │
                     ┌──────────────────┤
                     │                  │
              AI assistant          browser client
              (Claude/Cursor)       (EventSource)
```

### Known limitations
- Must be deployed on an Israeli IP (GCP me-west1) — inherits the same geo-blocking
- Server must be running before the AI session starts
- MCP tool definitions may require re-registration if the server restarts

---

## Home Assistant — `oref_alert` (HACS)

**Install:** HACS → Integrations → search "oref alert"
**Repo:** https://github.com/amitfin/oref_alert

### What it provides
- Auto-configures from HA's configured home location
- Creates sensors: `sensor.oref_alert`, `sensor.oref_alert_time_to_shelter`
- Multiple entity types: binary sensor, text sensor, countdown timer
- Uses both oref.org.il and Tzofar as data sources

### Entities

| Entity | Type | Value |
|--------|------|-------|
| `sensor.oref_alert` | string | Alert title, or `"no alert"` |
| `sensor.oref_alert_time_to_shelter` | number | Seconds, or `null` |
| `binary_sensor.oref_alert` | bool | `True` if active alert |

### Common automation patterns

```yaml
# Flash lights red on alert
automation:
  trigger:
    platform: state
    entity_id: binary_sensor.oref_alert
    to: "on"
  action:
    service: light.turn_on
    data:
      entity_id: light.living_room
      color_name: red
      flash: long
```

### Known limitations
- Monitors only the HA home location by default — configure additional areas via the integration settings
- Time-to-shelter is for the configured home location only, not other affected cities

---

## Home Assistant — `RedAlert` (AppDaemon)

**Install:** AppDaemon add-on + copy `redAlerts.py`
**Repo:** https://github.com/idodov/RedAlert (AppDaemon version)

### What it provides
- More scriptable than HACS — arbitrary Python logic in callbacks
- Multi-location monitoring in a single app
- Custom notification routing per city

### Usage

```python
import appdaemon.plugins.hass.hassapi as hass

class RedAlerts(hass.Hass):
    def initialize(self):
        self.listen_state(self.on_alert, "sensor.oref_alert")

    def on_alert(self, entity, attribute, old, new, kwargs):
        if new != "no alert":
            self.call_service("notify/mobile_app", message=new)
```

### Known limitations
- Requires AppDaemon — more setup than HACS integration
- AppDaemon version and HACS version should not both be active simultaneously
