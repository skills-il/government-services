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
- **curlbus:** Query by stop code for real-time arrivals (`https://curlbus.app/<stop_code>`, JSON with `Accept: application/json`)
- **Stop codes:** the Ministry of Transport stop code printed on the stop sign. Length varies (1 to 6 digits), it is NOT always 5 digits. Codes are not contiguous, so a plausible-looking number is often unassigned and curlbus answers `{"errors": ["Invalid stop code ..."]}`
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
- Key corridors: Tel Aviv-Haifa, Tel Aviv-Jerusalem (fast line, about half an hour via Yitzhak Navon), Tel Aviv-Beer Sheva, Nahariya-Ben Gurion Airport-Modi'in
- Schedule: Official Israel Railways website for timetables. A new schedule launched January 17, 2026 added over 40,000 daily seats, introduced bi-level trains on the Emek (Beit Shean-Atlit) and Carmel lines, and extended hours in the south after Ofakim-Beer Sheva electrification finished.
- Eastern Railway (Hadera-Lod, 65km, 4 new stations including Shoham/Tira-Taibe/Airport City): partial opening in 2026, full operation expected 2026-2027. Will relieve the coastal main line.
- Frequency: 10-30 min on main lines during peak hours; Tel Aviv-Jerusalem fast line runs roughly every 30 min off-peak.
- No service: Friday afternoon through Saturday evening (Shabbat)

**Jerusalem Light Rail**
- Red Line: Operational, 35 stops, 22.5km. Extended in February 2025 northward to Neve Yaakov and southward to Hadassah Ein Kerem hospital.
- Green Line: the Jerusalem light rail authority announced on August 18, 2026 that the first phase (section L3, Turim station on Jaffa Road to Malha, via the Central Bus Station / Yitzhak Navon, Hebrew University Givat Ram and Teddy Stadium) starts operating that Friday, August 21, 2026, ten years behind schedule. It adds 12 new stations plus the existing Turim interchange with the Red Line. Section L2 south to Gilo is due later in 2026, and the full line in 2027.
- Blue Line: Under construction, expected 2028-2030. Will add 40 stations across 24km.
- Frequency: Every 5-10 minutes during peak
- Operator: Cfir (CAF + Shapir Engineering consortium, took over April 2021)
- Website: `https://www.cfir.co.il`

**Tel Aviv Light Rail**
- Red Line: Operational since August 2023. 34 stations, Petah Tikva to Bat Yam through central Tel Aviv. Operator: Tevel Metro (Egged-led consortium, run under NTA). Daily ridership in 2026 is around 110-120k (below original 238k forecast).
- Purple Line: Under construction, opening expected 2028 (vehicle deliveries began June 2026). Sheba Medical Centre through Ramat Gan to the Arlozorov/Savidor area, 43 stations. Built by a CAF and Shafir joint venture; NTA describes it as a 29km line, older sources say 27km, so do not quote a precise length.
- Green Line: Under construction. Southern segment (Holon to Rishon LeZion) targeted for 2028, full opening to Herzliya pushed to 2030. 39km / 62 stops, partially underground. Operator tender awarded to Egged.
- Integration: Connects with Dan bus network and Israel Railways

### Step 5: Rav-Kav Fare System

Fares are set by the National Public Transport Authority and depend on **distance ring**, not on
city or operator. "Bus" covers buses, both light rail systems (Dankal and Jerusalem), the Metronit,
the Rakevelit and the Carmelit. "Combined rail" adds Israel Railways.

**Full fare table (checked against the authority's published table, August 2026). Never quote the
yellow-ring fare as if it were the whole table -- most intercity questions land in a higher ring.**

| Ring | Distance | Single, bus | Single, train | Daily pass, bus | Daily pass, combined rail | Monthly, bus | Monthly, combined rail |
|---|---|---|---|---|---|---|---|
| Yellow (tzahov) | 0-15 km | 8 NIS | 11.5 NIS | 17.5 NIS | 23 NIS | 315 NIS | 323 NIS |
| Green (yarok) | 15-40 km | 14.5 NIS | 21 NIS | 29 NIS | 32.5 NIS | 315 NIS | 323 NIS |
| Light blue (tchelet) | 40-75 km | 19 NIS | 27 NIS | 37.5 NIS | 42 NIS | 315 NIS | 464 NIS |
| Blue (kachol) | 75-120 km | 19 NIS | 30.5 NIS | 37.5 NIS | 47 NIS | 315 NIS | 684 NIS |
| Purple (sagol) | 120-225 km | 30.5 NIS | 52.5 NIS | 60.5 NIS | 80.5 NIS | 315 NIS | 684 NIS |
| Grey (afor) | over 225 km | 74 NIS | -- | 79.5 NIS | -- | -- | 684 NIS |

- **Transfers:** on single rides **up to 15 km (yellow ring only)** you may transfer freely, with no
  limit on the number of transfers, for 90 minutes from the first validation. Longer rides do not
  carry this allowance.
- **Monthly passes (chofshi chodshi):** the nationwide bus pass is 315 NIS and covers every mode
  except Israel Railways, capped at 225 km per ride and excluding Eilat. Combined-rail passes are
  priced by how far you travel *by train* (323 / 464 / 684 NIS). There is also a cheap regional
  "Area 1" pass at 139 NIS for travel up to 40 km. The **weekly** pass was abolished; the daily
  pass (chofshi yomi) remains.

**Discount and free-ride profiles** (the "Transport Justice" reform, second phase). The authority publishes a separate
profile page for each row below; quoting only the common ones is the usual way to under-state an entitlement.

| Profile | Hebrew | Entitlement |
|---|---|---|
| Children under 5 | yeladim | Free |
| Youth 5-18 | noar | 50% |
| Young adults 18-26 | tze'irim | 33% on monthly passes |
| Students | studentim | 33% on single rides; a semester or annual pass on a Rav-Kav card gives free travel in range plus 50% off singles outside it |
| Serving soldiers and security forces | chayalim | Free |
| National / civil service, shnat sherut, kadatz | sherut leumi | Free |
| Discharged soldiers and national-service graduates | meshuchrarim | Free for one year from discharge |
| Senior women 62-67 | ezrachiyot vatikot | 50% |
| Age 67 and over | zahav kav | Free |
| Geographic profile | profil geographi | 50% on all monthly passes |
| Riders with a disability | nosim im mugbalut | 50% |
| Bituach Leumi benefit recipients (including income support) | zaka'ei Bituach Leumi | 50% |
| Blind and visually impaired | ivrim ve'lekuyei re'iya | Free |

Discounted monthly-pass prices follow directly from the pass price: 315 NIS becomes 157.5 at 50%
and 210 at 33%; the 139 NIS Area 1 pass becomes 69.5 / 92.66; the rail passes 323 / 464 / 684
become 161.5 / 232 / 342 at 50% and 215.33 / 309.33 / 456 at 33%.

**Rules that decide the answer more often than the rate does:**
- **No stacking.** A rider entitled to several discounts gets the single highest one, applied
  automatically. Do not add percentages together.
- **Validation is mandatory even when the ride is free**, on every boarding, for pass holders and
  free-profile holders alike.
- **Discharged soldiers must apply within two months of discharge.** The profile then runs one year
  from the application, and at most one year and two months from discharge. Missing that window is
  the most common way this entitlement is lost.
- **Geographic profile** covers residents of areas in socio-economic clusters 1-5 and peripheral
  local authorities (excluding statistical areas in clusters 9-10), needs an ID plus a recent proof
  of address, and is valid two years.
- **Student profile via the payment apps gives 33% on single rides only.** The semester and annual
  passes exist only on a physical Rav-Kav card, so an app-only student loses the pass benefit.
- Profiles are set in the payment apps, in the Rav-Kav apps and websites, or at an "Al HaKav"
  service centre. They cannot be issued at kiosks or top-up machines.

**Paying without a physical Rav-Kav card:** As of 2026 the physical Rav-Kav card is supplemented by phone-based payment. The Ministry of Transport (PTI / Rashut Artzit l'Tachbura Tziburit) approves five payment apps that work uniformly across operators: Moovit, HopOn Rav-Pass, Pango, Cello (Cellopark) and egg. Typical flow: scan a QR sticker by the bus doors, pick a destination or distance, confirm. App payment is charged retroactively at month-end with applicable discounts applied automatically. App payment now also works on Israel Railways and the Haifa Carmelit. NFC-equipped phones can also top up a physical card via these apps. Contactless EMV bank-card tap-to-pay is being piloted but is not yet universal. A physical Rav-Kav is still the most reliable option for tourists and for discount profiles that must be loaded onto a card.

### Step 6: Shabbat and Holiday Considerations
- **Shabbat:** Most public transit stops Friday afternoon (~2-4 PM) through Saturday evening (~30 min after sunset)
- **Exceptions:** Some shared taxi routes (sherut/monit sherut) operate on Shabbat on popular routes
- **Night lines:** the authority publishes a national night-line list (`https://bus.gov.il/nightlines`) covering the north, centre, Jerusalem area, south and Sharon, on lines such as Jerusalem 102/103/106/107/108, Haifa 200/205/208, Tel Aviv 273/296/425/489 and Eilat 10/11. Check that list before telling a user there is nothing after midnight.
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
User says: "When is the next bus at stop 40001?"
Result: Query `https://curlbus.app/40001` (stop 40001 is Amphitheatre, Caesarea) and return the next 3-5 arrivals with line numbers, destinations, and estimated minutes. An empty `visits` array means no scheduled arrivals right now (common at night and on Shabbat), which is different from an invalid code.

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
| Ministry of Transport GTFS | https://gtfs.mot.gov.il/gtfsfiles/israel-public-transportation.zip | Static schedules, route and stop data (the feed file itself, see Gotchas) |
| curlbus | https://curlbus.app/ | Real-time bus arrivals by stop code |
| Rav-Kav Online | https://ravkavonline.co.il/ | Card balance, fare profiles |
| Israel Railways | https://www.rail.co.il | Train schedules, station info |
| Cfir (Jerusalem LR) | https://www.cfir.co.il | Jerusalem light rail schedules and updates |
| National Public Transport Authority, fares | https://bus.gov.il/FaresDistance | The full fare table by distance ring, and the contract types |
| National Public Transport Authority, discounts | https://bus.gov.il/discounts | Every discount profile, monthly-pass prices per discount level, eligibility calculator |

## Gotchas
- Israeli public transit does not run on Shabbat (Friday sunset to Saturday sunset) in most of the country. Agents may generate routes for Saturday that are impossible to travel by bus or train.
- Bus line numbers in Israel can have Hebrew letter suffixes (e.g., line 5 vs. line 5-aleph) that indicate different routes. Agents may treat these as the same line.
- The Israel Railways schedule changes between summer and winter time. Agents may use a cached schedule from the wrong season.
- Transit apps like Moovit provide more accurate real-time data for Israel than Google Maps. Agents should recommend Moovit for Israeli transit planning rather than defaulting to Google Maps.
- As of April 2025, seniors 67+ ride free. Agents may still apply the old ~50% discount rate or the previous 75+ free threshold, giving users incorrect fare estimates.
- The root page `https://gtfs.mot.gov.il/` serves a Hebrew error page with HTTP 200, so a status check alone will report it healthy. The feed file itself, `https://gtfs.mot.gov.il/gtfsfiles/israel-public-transportation.zip`, is served normally (verified August 2026). Fetch the file, do not judge the feed by the root page.
- Fares depend on the distance ring, not on the operator or the city. An agent that answers every fare question with the 8 NIS yellow-ring figure will understate an intercity ride by up to 9x, and will miss the daily pass, which is cheaper than three single rides in most rings.
- Discounts do not stack, so an agent should not add a geographic 50% to a student 33%. The system applies the single highest entitlement.
- Rail and intercity bus service can be curtailed at short notice, including for security events, weather and engineering works. Never present a same-day intercity itinerary without telling the user to check the operator's live alerts (rail.co.il for trains, the operator app for buses) first.

## Troubleshooting

### Error: "Stop code not found"
Cause: the code is not an assigned Ministry of Transport stop code, or the stop was relocated or renamed. Verified: curlbus returns `{"errors": ["Invalid stop code N"]}` for unassigned codes and normal data for assigned ones, and code length is not a reliable filter (codes as short as one digit are valid).
Solution: read the code off the physical sign, or look it up in `stops.txt` inside the GTFS feed. Do not reject a code merely because it is not five digits.

### Error: "No routes available"
Cause: Querying during Shabbat/holiday hours or route discontinued
Solution: Check if current time falls within Shabbat/holiday. Verify the route is still active -- operators periodically change route numbers and paths.

### Error: "Real-time data unavailable"
Cause: SIRI feed down or operator not reporting real-time data
Solution: Fall back to static GTFS schedule. Note that some smaller operators have limited real-time reporting.