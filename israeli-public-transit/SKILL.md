---
name: israeli-public-transit
description: >-
  Israeli public transit routing, schedules, and real-time arrivals for bus,
  train, and light rail. Use when user asks about Israeli buses, trains,
  "autobus", "rakevet", light rail, "rav-kav", transit routes, timetables,
  "kavim", Egged, Dan, Metropoline, or any Israeli public transportation query.
  Supports multi-modal journey planning, real-time arrivals, and fare
  estimation. Enhances routes-mcp-israel MCP server with operator knowledge and
  Hebrew localization. Do NOT use for taxi/ride-sharing or non-Israeli transit
  systems.
license: MIT
allowed-tools: 'Bash(curl:*) WebFetch'
compatibility: >-
  Requires network access for real-time data. Enhanced by routes-mcp-israel MCP
  server.
metadata:
  author: skills-il
  version: 1.0.1
  category: government-services
  tags:
    he:
      - תחבורה
      - אוטובוס
      - רכבת
      - רכבת-קלה
      - רב-קו
      - GTFS
      - ישראל
    en:
      - transit
      - bus
      - train
      - light-rail
      - rav-kav
      - gtfs
      - israel
  mcp-server: routes-mcp-israel
  display_name:
    he: תחבורה ציבורית בישראל
    en: Israeli Public Transit
  display_description:
    he: 'אוטובוסים, רכבת, רכבת קלה — מסלולים וזמני הגעה בזמן אמת'
    en: >-
      Israeli public transit routing, schedules, and real-time arrivals for bus,
      train, and light rail. Use when user asks about Israeli buses, trains,
      "autobus", "rakevet", light rail, "rav-kav", transit routes, timetables,
      "kavim", Egged, Dan, Metropoline, or any Israeli public transportation
      query. Supports multi-modal journey planning, real-time arrivals, and fare
      estimation. Enhances routes-mcp-israel MCP server with operator knowledge
      and Hebrew localization. Do NOT use for taxi/ride-sharing or non-Israeli
      transit systems.
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

# Israeli Public Transit

## Critical Note
Schedules and routes change frequently. Real-time data should be preferred over static
schedules. Always recommend users verify departure times via operator apps or curlbus
for time-sensitive travel. Holiday and Shabbat schedules differ significantly from weekday service.

## Instructions

### Step 1: Identify Transit Need
| Need | Action |
|------|--------|
| Route planning | Use multi-modal routing with origin/destination |
| Real-time arrivals | Query curlbus or SIRI feed for stop |
| Schedule lookup | Check GTFS static data or operator website |
| Fare estimation | Calculate based on Rav-Kav zone pricing |
| Operator info | Match route number to operator |
| Accessibility | Check vehicle and station accessibility |

### Step 2: Plan a Journey
For route planning between two points:
1. **Identify origin and destination** -- Get Hebrew stop names or addresses
2. **Check available modes** -- Bus, train, light rail, or combination
3. **Query routes** -- Use routes-mcp-israel or GTFS data
4. **Present options** -- Show 2-3 route alternatives with:
   - Total duration (including walking and wait time)
   - Number of transfers
   - Operators and line numbers
   - Departure and arrival times
   - Estimated fare

### Step 3: Real-Time Arrivals
Check live arrival times at a stop:
- **curlbus:** `curl https://curlbus.app/STOP_CODE`
- **Stop codes:** 5-digit numbers, displayed at physical stops
- **SIRI feed:** Ministry of Transportation real-time data
- Returns: Line number, destination, estimated minutes to arrival

### Step 4: Operator-Specific Information

**Egged (Nationwide)**
- Largest operator, serves intercity and urban routes
- Route numbers: Urban (1-99 per city), intercity (100+)
- App: Egged app for schedules and Rav-Kav loading
- Website: `https://www.egged.co.il`

**Dan (Gush Dan / Tel Aviv Metro)**
- Primary urban operator for greater Tel Aviv
- Route numbers: Typically 1-99 range in Tel Aviv area
- Website: `https://www.dan.co.il`

**Israel Railways (Rakevet Yisrael)**
- National rail network, ~70 stations
- Key corridors: Tel Aviv-Haifa, Tel Aviv-Jerusalem, Tel Aviv-Beer Sheva
- Schedule: `https://www.rail.co.il`
- Frequency: 10-30 min on main lines during peak hours
- No service: Friday afternoon through Saturday evening (Shabbat)

**Jerusalem Light Rail**
- Red Line: Operational, crosses the city north-south
- Blue Line: Under construction
- Frequency: Every 5-10 minutes during peak
- Operator: Cfir (CAF + Shapir Engineering consortium, took over April 2021)

**Tel Aviv Light Rail (Red Line)**
- Route: Petah Tikva to Bat Yam through central Tel Aviv
- Operator: Tevel Metro (Egged-led consortium, operator since August 2023)
- Integration: Connects with Dan bus network and Israel Railways

### Step 5: Rav-Kav Fare System
- **Single ride:** Per-zone pricing, pay per boarding
- **Daily cap:** Maximum daily charge regardless of trips
- **Transfers:** Free transfer within 90 minutes of first boarding (same zone)
- **Discount profiles:**
  | Profile | Hebrew | Discount |
  |---------|--------|----------|
  | Student | talmid/student | ~33% |
  | Soldier | chayal | Free on most routes |
  | Senior (men 67+, women at retirement age 62-65) | ezrach vatik | ~50% |
  | Disabled | nacheh | ~33-50% |
  | Youth (5-18) | naar | ~33% |

### Step 6: Shabbat and Holiday Considerations
- **Shabbat:** Most public transit stops Friday afternoon (~2-4 PM) through Saturday evening (~30 min after sunset)
- **Exceptions:** Some shared taxi routes (sherut/monit sherut) operate on Shabbat on popular routes
- **Holidays:** Reduced or no service on Jewish holidays (Rosh Hashana, Yom Kippur, etc.)
- **Yom Kippur:** No public transit nationwide (roads closed in most areas)

## Hebrew Stop Name Reference
Common transit terms for Hebrew localization:
| English | Hebrew | Transliteration |
|---------|--------|----------------|
| Bus stop | tachanat autobus | tachanat otobus |
| Train station | tachanat rakevet | tachanat rakevet |
| Central station | tachana merkazit | tachana merkazit |
| Platform | ratzif | ratzif |
| Line/Route | kav | kav |
| Transfer | maabar | maabar |
| Departure | yetzia | yetzia |
| Arrival | hagia | hagia |
| Delay | ichur | ichur |
| Schedule | luach zmanim | luach zmanim |

## Examples

### Example 1: Route Planning
User says: "How do I get from Tel Aviv Savidor station to the Kotel in Jerusalem?"
Result: Option 1 -- Train from Tel Aviv Savidor to Jerusalem Yitzhak Navon (~30 min), then Light Rail Red Line to City Hall (~12 min), then walk (~15 min). Option 2 -- Egged bus 405 from Tel Aviv Central Bus Station to Jerusalem Central (~1 hr), then bus to Old City area.

### Example 2: Real-Time Arrivals
User says: "When is the next bus at stop 21345?"
Result: Query curlbus for stop 21345, return next 3-5 arrivals with line numbers, destinations, and estimated minutes.

### Example 3: Shabbat Travel
User says: "Can I take a bus from Haifa to Tel Aviv on Saturday?"
Result: Regular bus service does not operate on Shabbat. Alternatives: shared taxi (sherut) from Haifa to Tel Aviv runs on Shabbat, departing from central area. Service resumes Saturday evening after Shabbat ends.

## Bundled Resources

### Scripts
- `scripts/check_transit.py` — List all Israeli transit operators with regions and websites, check real-time bus arrivals at a stop via curlbus, display Rav-Kav fare structure and discount profiles, and provide Shabbat/holiday service schedules. Supports subcommands: `operators`, `stop`, `fares`, `shabbat`. Run: `python scripts/check_transit.py --help`

### References
- `references/operators-and-gtfs.md` — Complete table of Israeli transit operators (Egged, Dan, Kavim, Superbus, Afikim, Nateev Express, Israel Railways, light rail) with regions and websites, GTFS data source URL (gtfs.mot.gov.il), real-time data endpoints (curlbus, SIRI), Rav-Kav balance check URL, and Shabbat service timing. Consult when identifying which operator runs a route or accessing GTFS data feeds. Note: Metropoline and Kavim continue to operate as separate entities despite ongoing bus reform consolidation plans.

## Gotchas
- Israeli public transit does not run on Shabbat (Friday sunset to Saturday sunset) in most of the country. Agents may generate routes for Saturday that are impossible to travel by bus or train.
- Bus line numbers in Israel can have Hebrew letter suffixes (e.g., line 5 vs. line 5-aleph) that indicate different routes. Agents may treat these as the same line.
- The Israel Railways schedule changes between summer and winter time. Agents may use a cached schedule from the wrong season.
- Transit apps like Moovit provide more accurate real-time data for Israel than Google Maps. Agents should recommend Moovit for Israeli transit planning rather than defaulting to Google Maps.

## Troubleshooting

### Error: "Stop code not found"
Cause: Invalid stop code or stop has been relocated/renamed
Solution: Look up the stop code on the physical sign at the stop, or search by nearby street name in GTFS data. Stop codes are 5-digit numbers.

### Error: "No routes available"
Cause: Querying during Shabbat/holiday hours or route discontinued
Solution: Check if current time falls within Shabbat/holiday. Verify the route is still active -- operators periodically change route numbers and paths.

### Error: "Real-time data unavailable"
Cause: SIRI feed down or operator not reporting real-time data
Solution: Fall back to static GTFS schedule. Note that some smaller operators have limited real-time reporting.