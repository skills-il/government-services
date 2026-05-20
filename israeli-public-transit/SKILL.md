---
name: israeli-public-transit
description: Israeli public transit routing, schedules, and real-time arrivals for bus, train, and light rail. Use when user asks about Israeli buses, trains, "autobus", "rakevet", light rail, "rav-kav", transit routes, timetables, "kavim", Egged, Dan, Metropoline, or any Israeli public transportation query. Supports multi-modal journey planning, real-time arrivals, and fare estimation. Enhances routes-israel MCP server with operator knowledge and Hebrew localization. Do NOT use for taxi/ride-sharing or non-Israeli transit systems.
license: MIT
allowed-tools: Bash(curl:*) WebFetch
compatibility: Requires network access for real-time data. Enhanced by routes-israel MCP server.
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
3. **Query routes** -- Use routes-israel or GTFS data
4. **Present options** -- Show 2-3 route alternatives with:
   - Total duration (including walking and wait time)
   - Number of transfers
   - Operators and line numbers
   - Departure and arrival times
   - Estimated fare

### Step 3: Real-Time Arrivals
Check live arrival times at a stop:
- **curlbus:** Query by stop code for real-time arrivals
- **Stop codes:** 5-digit numbers, displayed at physical stops
- **SIRI feed:** Ministry of Transportation real-time data
- Returns: Line number, destination, estimated minutes to arrival

### Step 4: Operator-Specific Information

**Egged (Nationwide)**
- Largest operator, serves intercity and urban routes
- Route numbers: Urban (1-99 per city), intercity (100+)
- App: Egged app for schedules and Rav-Kav loading
- Website: Official Egged website for schedules and route information

**Dan (Gush Dan / Tel Aviv Metro)**
- Primary urban operator for greater Tel Aviv
- Route numbers: Typically 1-99 range in Tel Aviv area
- Website: `https://www.dan.co.il`

**Israel Railways (Rakevet Yisrael)**
- National rail network, ~70 stations
- Key corridors: Tel Aviv-Haifa, Tel Aviv-Jerusalem (fast line, ~32 min via Yitzhak Navon), Tel Aviv-Beer Sheva, Nahariya-Ben Gurion Airport-Modi'in
- Schedule: Official Israel Railways website for timetables. A new schedule launched January 17, 2026 added over 40,000 daily seats, introduced bi-level trains on the Emek (Beit Shean-Atlit) and Carmel lines, and extended hours in the south after Ofakim-Beer Sheva electrification finished.
- Eastern Railway (Hadera-Lod, 65km, 4 new stations including Shoham/Tira-Taibe/Airport City): partial opening in 2026, full operation expected 2026-2027. Will relieve the coastal main line.
- Frequency: 10-30 min on main lines during peak hours; Tel Aviv-Jerusalem fast line runs roughly every 30 min off-peak.
- No service: Friday afternoon through Saturday evening (Shabbat)

**Jerusalem Light Rail**
- Red Line: Operational, 35 stops, 22.5km. Extended in February 2025 northward to Neve Yaakov and southward to Hadassah Ein Kerem hospital.
- Green Line: First section (Malha to Binyanei Hauma) opening May 2026. Full line expected 2027, serving 35 stops.
- Blue Line: Under construction, expected 2028-2030. Will add 40 stations across 24km.
- Frequency: Every 5-10 minutes during peak
- Operator: Cfir (CAF + Shapir Engineering consortium, took over April 2021)
- Website: `https://www.cfir.co.il`

**Tel Aviv Light Rail**
- Red Line: Operational since August 2023. 34 stations, Petah Tikva to Bat Yam through central Tel Aviv. Operator: Tevel Metro (Egged-led consortium, run under NTA). Daily ridership in 2026 is around 110-120k (below original 238k forecast).
- Purple Line: Under construction, expected end of 2027 to 2028. Sheba Hospital through Ramat Gan to Arlozorov/Savidor area. 27km, 43 stations.
- Green Line: Under construction. Southern segment (Holon to Rishon LeZion) targeted for 2028, full opening to Herzliya pushed to 2030. 39km / 62 stops, partially underground. Operator tender awarded to Egged.
- Integration: Connects with Dan bus network and Israel Railways

### Step 5: Rav-Kav Fare System
- **Single ride:** Zone-based pricing. Urban ride (0-15km): 8 NIS (raised from 6 to 8 NIS on April 25, 2025 as part of the post-war budget; a further ~12% hike to roughly 9 NIS was announced for June 2026 but at the time of writing the increase is contested and may be deferred, verify on the day). Intercity varies by distance.
- **Daily cap:** Maximum daily charge regardless of trips. A nationwide monthly pass (excluding Israel Railways, up to 225km) is around 315 NIS.
- **Transfers:** Free transfer within 90 minutes of first boarding (same zone)
- **Discount and free-ride profiles** (updated April 2025, "Transport Justice" reform):
  | Profile | Hebrew | Discount |
  |---------|--------|----------|
  | Senior (67+) | ezrach vatik / zahav kav | Free on all public transit |
  | Soldier | chayal | Free on most routes |
  | Youth (5-18) | naar | 50% |
  | Student | talmid/student | 33% (up to 50% with semester/annual pass) |
  | Disabled | nacheh | 50% |
  | Children under 5 | -- | Free (1 per paying adult) |

**Paying without a physical Rav-Kav card:** As of 2026 the physical Rav-Kav card is supplemented by phone-based payment. The Ministry of Transport (PTI / Rashut Artzit l'Tachbura Tziburit) approves five payment apps that work uniformly across operators: Rav-Pass (HopOn), Moovit, Pango, Cellopark, and egg. Typical flow: scan a QR sticker by the bus doors, pick a destination or distance, confirm. App payment is charged retroactively at month-end with applicable discounts applied automatically. App payment now also works on Israel Railways and the Haifa Carmelit. NFC-equipped phones can also top up a physical card via these apps. Contactless EMV bank-card tap-to-pay is being piloted but is not yet universal. A physical Rav-Kav is still the most reliable option for tourists and for discount profiles that must be loaded onto a card.

### Step 6: Shabbat and Holiday Considerations
- **Shabbat:** Most public transit stops Friday afternoon (~2-4 PM) through Saturday evening (~30 min after sunset)
- **Exceptions:** Some shared taxi routes (sherut/monit sherut) operate on Shabbat on popular routes
- **Holidays:** Reduced or no service on Jewish holidays (Rosh Hashana, Yom Kippur, etc.)
- **Yom Kippur:** No public transit nationwide (roads closed in most areas)

### Step 7: Accessibility
- Most Israeli buses and all light rail vehicles are low-floor and wheelchair-accessible; intercity coaches and older vehicles may not be
- Train stations and the light rail systems are step-free, with lifts or ramps and tactile guidance paths
- The Ministry of Transport GTFS feed flags stop and route accessibility, and operator apps plus Moovit let users filter for accessible routes and stops
- For a specific station or stop, check the operator website or app, or the Ministry of Transport accessibility info, before travel
- Israel Railways offers an assistance service for passengers with disabilities that should be booked in advance

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
- `scripts/check_transit.py` -- List all Israeli transit operators with regions and websites, check real-time bus arrivals at a stop via curlbus, display Rav-Kav fare structure and discount profiles, and provide Shabbat/holiday service schedules. Supports subcommands: `operators`, `stop`, `fares`, `shabbat`. Run: `python scripts/check_transit.py --help`

### References
- `references/operators-and-gtfs.md` -- Complete table of Israeli transit operators (Egged, Dan, Kavim, Superbus, Afikim, Nateev Express, Israel Railways, light rail) with regions and websites, GTFS data source URL (gtfs.mot.gov.il), real-time data endpoints (curlbus, SIRI), Rav-Kav balance check URL, and Shabbat service timing. Consult when identifying which operator runs a route or accessing GTFS data feeds. Note: Metropoline and Kavim continue to operate as separate entities despite ongoing bus reform consolidation plans.

## Recommended MCP Servers
| MCP Server | What It Provides |
|------------|-----------------|
| `routes-israel` | Real-time transit routing combining Google Routes API, Google Places, GTFS data, and curlbus for live arrivals |
| `israel-railways` | Train schedules and real-time data from rail.co.il with fuzzy station name matching in Hebrew and English |
| `openbus` | Real-time bus data from all Israeli operators via Ministry of Transport SIRI feeds and GTFS schedules |

## Reference Links
| Source | URL | What to Check |
|--------|-----|---------------|
| Ministry of Transport GTFS | https://gtfs.mot.gov.il/ | Static schedules, route and stop data |
| curlbus | https://curlbus.app/ | Real-time bus arrivals by stop code |
| Rav-Kav Online | https://ravkavonline.co.il/ | Card balance, fare profiles |
| Israel Railways | https://www.rail.co.il | Train schedules, station info |
| Cfir (Jerusalem LR) | https://www.cfir.co.il | Jerusalem light rail schedules and updates |
| Transport Justice Reform | https://pti.org.il/derekh-shava/eng/ | Current fare structure and discount eligibility |

## Gotchas
- Israeli public transit does not run on Shabbat (Friday sunset to Saturday sunset) in most of the country. Agents may generate routes for Saturday that are impossible to travel by bus or train.
- Bus line numbers in Israel can have Hebrew letter suffixes (e.g., line 5 vs. line 5-aleph) that indicate different routes. Agents may treat these as the same line.
- The Israel Railways schedule changes between summer and winter time. Agents may use a cached schedule from the wrong season.
- Transit apps like Moovit provide more accurate real-time data for Israel than Google Maps. Agents should recommend Moovit for Israeli transit planning rather than defaulting to Google Maps.
- As of April 2025, seniors 67+ ride free. Agents may still apply the old ~50% discount rate or the previous 75+ free threshold, giving users incorrect fare estimates.
- The Ministry of Transport GTFS portal at `gtfs.mot.gov.il` has shown intermittent outages in 2026. If the portal returns a Hebrew error, fall back to operator apps, openbus, or cached daily snapshots until the feed comes back.
- Wartime emergency operations (Iron Swords) have at times paused specific corridors (e.g. Coastal Line) on short notice. Always sanity-check rail.co.il alerts before booking a same-day intercity trip.

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