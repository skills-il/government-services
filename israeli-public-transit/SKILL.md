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
| Fare estimation | Get the exact fare from the authority's route planner, Maslulan (`https://route.bus.gov.il`), then apply the rider's profile from Step 5 |
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
- **Stop codes:** the Ministry of Transport stop code printed on the stop sign. Length varies (1 to 5 digits), it is NOT always 5 digits. Codes are not contiguous, so a plausible-looking number is often unassigned and curlbus answers `{"errors": ["Invalid stop code ..."]}`
- **SIRI feed:** Ministry of Transportation real-time data
- Returns: Line number, destination, estimated minutes to arrival

### Step 4: Operator-Specific Information

**Egged (Nationwide)**
- Largest operator, serves intercity and urban routes
- App: Egged app for schedules and Rav-Kav loading
- Website: Official Egged website for schedules and route information

**Dan (Gush Dan / Tel Aviv Metro)**
- Primary urban operator for greater Tel Aviv
- Website: `https://www.dan.co.il`

**Israel Railways (Rakevet Yisrael)**
- National rail network
- Key corridors: Tel Aviv-Haifa, Tel Aviv-Jerusalem (Yitzhak Navon: about 44 min from Savidor, about 34 from HaHagana), Tel Aviv-Beer Sheva, Nahariya-Ben Gurion Airport-Modi'in
- Schedule: Official Israel Railways website for timetables. A new schedule launched January 17, 2026 added over 40,000 daily seats, introduced bi-level trains on the Emek (Beit Shean-Atlit) and Karmiel-Haifa lines, and extended hours in the south after Ofakim-Beer Sheva electrification finished.
- Eastern Railway: the northern section opened June 28, 2026, with new stations Hadera East, Shomron-Tayibe and Tira-Kochav Yair, connecting to Rosh HaAyin North, where riders change for Tel Aviv. At opening it ran Sunday to Thursday, about 06:00-21:00, two trains an hour. The southern section to Lod, with a Shoham station, is due in 2027.
- Jerusalem line: from November 14, 2026, per the Israel Railways announcement, the Jerusalem-Tel Aviv-Herzliya line continues to Netanya, Beit Yehoshua and Hadera West, giving those stations direct trains to Ben Gurion Airport and Jerusalem.
- Frequency: 10-30 min on main lines during peak hours; Jerusalem to Tel Aviv Savidor runs about 2 trains an hour for most of the day in the November 22, 2026 feed. Check the live timetable, because added trains were announced.
- No service: Friday afternoon through Saturday evening (Shabbat)

**Jerusalem Light Rail**
- Red Line: Operational, 35 stops, 22.5km. Extended in February 2025 northward to Neve Yaakov and southward to Hadassah Ein Kerem hospital.
- Green Line: the first section (L3, Malha to Turim, via Teddy Stadium, Hebrew University Givat Ram and Binyanei HaUma) opened August 21, 2026. In the Ministry feed of November 22, 2026, line 3 continues from Turim along Jaffa Road to Damascus Gate (18 stops, about every 10 minutes at morning peak), sharing the Turim to Damascus Gate stops with the Red Line. A line 4 to Gilo West appears in the same feed with a single morning trip each way, and no public opening to Gilo was confirmed as of November 23, 2026, so check before routing a rider there. The extension to Mount Scopus is due in 2027.
- Blue Line: Under construction, with opening planned around 2030. Published station counts and lengths differ, so do not quote a precise figure.
- Operator: Cfir
- Website: `https://www.cfir.co.il`

**Tel Aviv Light Rail**
- Red Line: Operational since August 2023. 34 stations, Petah Tikva to Bat Yam through central Tel Aviv. Operator: Dankal. Ridership figures are disputed: in September 2025 Globes cited about 110-120k a day from sources close to the project, while NTA's site showed 200k.
- Purple Line: Under construction, opening expected 2028 (vehicle deliveries began June 2026). Starts next to Savidor station, loops around the western city center and runs east to Sheba Medical Centre, where it splits into a branch to Kiryat Ono and Bar Ilan University and a branch through Tel Hashomer and Yehud-Monoson. Published lengths range from 27 to 29 km, so do not quote a precise length.
- Green Line: Under construction. Southern section (Rishon LeZion to south Tel Aviv) targeted for 2028, northern section to Herzliya for 2030. 39km / 62 stops, partially underground. Operator tender awarded to Egged.
- Integration: Connects with Dan bus network and Israel Railways

### Step 5: Rav-Kav Fare System

Fares are set by the National Public Transport Authority and depend on **distance ring**, not on
city or operator. "Bus" covers buses, both light rail systems (Dankal and Jerusalem), the Metronit,
the Rakevelit and the Carmelit. "Combined rail" adds Israel Railways.

**Full fare table (checked against the authority's published table, November 2026). Never quote the
yellow-ring fare as if it were the whole table -- most intercity questions land in a higher ring.**

| Ring | Distance | Single, bus | Single, train | Daily pass, bus | Daily pass, combined rail | Monthly, bus | Monthly, combined rail |
|---|---|---|---|---|---|---|---|
| Yellow (tzahov) | 0-15 km | 8 NIS | 11.5 NIS | 17.5 NIS | 23 NIS | 315 NIS | 323 NIS |
| Green (yarok) | 15-40 km | 14.5 NIS | 21 NIS | 29 NIS | 32.5 NIS | 315 NIS | 323 NIS |
| Light blue (tchelet) | 40-75 km | 19 NIS | 27 NIS | 37.5 NIS | 42 NIS | 315 NIS | 464 NIS |
| Blue (kachol) | 75-120 km | 19 NIS | 30.5 NIS | 37.5 NIS | 47 NIS | 315 NIS | 684 NIS |
| Purple (sagol) | 120-225 km | 30.5 NIS | 52.5 NIS | 60.5 NIS | 80.5 NIS | 315 NIS | 684 NIS |
| Grey (afor) | over 225 km | 74 NIS | -- | 79.5 NIS | -- | -- | 684 NIS |

**Finding the ring:** do not infer it from road or track distance, because the ring decides the price and the authority's fare pages do not state how distance is measured. Take the fare from Maslulan (`https://route.bus.gov.il`). If it cannot be checked, give both candidate rings and say which is unconfirmed.

**Pending fare update:** the price-control order sets the next update for January 25, 2027. Press reports of November 17, 2026 say the Transport Minister ordered it halted, with the funding still being settled. No new table had been published as of November 23, 2026. Quote the table above, and for any trip on or after January 25, 2027 re-check `https://bus.gov.il/FaresDistance` first. Do not quote press estimates of a new fare.

- **Transfers:** on single rides **up to 15 km (yellow ring only)** you may transfer freely, with no
  limit on the number of transfers, for 90 minutes from the first validation. The authority's page
  lists buses, light rail, Metronit and Rakevelit, and does not list Israel Railways, so confirm a
  train-to-bus transfer in Maslulan. Longer rides do not carry this allowance.
- **Monthly passes (chofshi chodshi):** the nationwide bus pass is 315 NIS and covers every mode
  except Israel Railways, capped at 225 km per ride, and trips to Eilat over 225 km are not included. Combined-rail passes are
  priced by how far you travel *by train* (323 / 464 / 684 NIS), and a train ride beyond the pass's
  rail range is paid separately. A monthly pass runs one full month
  from activation. The **weekly** pass was abolished; the daily pass (chofshi yomi) remains and
  lasts until the end of service that day, 04:00 at the latest, including night lines in range.
- **"Area 1" pass (139 NIS) is not open to everyone's route.** It covers bus rides up to 40 km only
  when **both origin and destination are inside Area 1** (the authority's examples are communities
  in the south and north), and it excludes Israel Railways. Check the locality on the area map at
  `https://bus.gov.il/Annual-Pass` before recommending it. A separate Eilat pass (up to 40 km) is
  117.79 NIS.

**Discount and free-ride profiles** (the "Transport Justice" reform, second phase). The authority publishes a separate
profile page for each row below, so check the whole table. Present these as the authority's published conditions: the authority decides eligibility on the submitted documents, so do not tell a rider they definitely qualify. The Zahav Kav and discharged-soldier pages also list service taxis (monit sherut) among the covered modes, but they do not address Shabbat sherut lines. Do not tell a rider a Shabbat sherut is free: send them to the operator or *8787 first, and tell them to carry a way to pay.

| Profile | Hebrew | Entitlement |
|---|---|---|
| Children under 5 | yeladim | Free for **one** child per accompanying adult. Each additional child pays and validates, so arrange a Youth-profile Rav-Kav (50%) at a service point before the trip. Strollers are free. On Eilat lines, a child who needs their own seat or a car seat needs a ticket bought in advance on the Youth profile |
| Youth 5-18 | noar | 50% on single rides and monthly passes, until 18 or the end of high school, whichever is later; pupils in special-education institutions until 21. Extending past 18 needs a current study confirmation |
| Young adults 18-26 | tze'irim | 33% on monthly passes, until the day before the 27th birthday |
| Students | studentim | 33% on single rides; a semester or annual pass on a Rav-Kav card gives free travel in range plus 50% off singles outside it (prices in `references/operators-and-gtfs.md`). Valid to October 14 or the end of the study confirmation, whichever is earlier |
| Soldiers in regular and career service, police, prison service | chayalim | Free, subject to the employer's rules. The page does not address reservists, so they should check IDF instructions |
| National / civil service, shnat sherut, kadatz, pre-military academy (mechina) and military boarding-school cadets | sherut leumi | Free up to 225 km, excluding Eilat and the Arava unless the rider lives or serves there or holds a suitable certificate. Requires a Rav-Kav card |
| Discharged soldiers and national-service graduates | meshuchrarim | Free for one year, within the application rule below (honorable discharge; career service of up to 5 years) |
| Senior women 62-67 | ezrachiyot vatikot | 50% on single rides, day and monthly passes. **The profile ends at 67**, so she must update to Zahav Kav to ride free |
| Age 67 and over | zahav kav | Free, from the earlier of the Hebrew or Gregorian birthday. Update with an ID, driving licence or Israeli passport, not a senior-citizen card |
| Geographic profile | profil geographi | 50% on all monthly passes |
| Riders with a disability | nosim im mugbalut | 50% on stored value, single rides and all monthly passes (the page does not list the day pass, so confirm with *8787 before quoting one), for holders of a disability certificate (teudat nacheh), or members of the IDF Disabled or hostile-action victims organizations with at least 50% medical disability |
| Bituach Leumi benefit recipients (including income support) | zaka'ei Bituach Leumi | 50% on stored value, single rides and all monthly passes (the page does not list the day pass, so confirm with *8787). Needs a confirmation from the last six months, and the profile lasts at most one year |
| Blind and visually impaired | ivrim ve'lekuyei re'iya | Free. A companion traveling with them gets 50%, paid from stored value on the profile holder's Rav-Kav (so not through an app alone), with the same origin and destination |

Discounted monthly-pass prices follow directly from the pass price: 315 NIS becomes 157.5 at 50%
and 210 at 33%; the 139 NIS Area 1 pass becomes 69.5 / 92.66; the rail passes 323 / 464 / 684
become 161.5 / 232 / 342 at 50% and 215.33 / 309.33 / 456 at 33%.

**Rules that decide the answer more often than the rate does:**
- **No stacking.** A rider holding several profiles gets the single highest discount, applied
  automatically. Do not add percentages together.
- **Validation is mandatory even when the ride is free**, on every boarding, for pass holders and
  free-profile holders alike. **On Israel Railways every rider, by card or app, validates at both
  entry and exit, even if the gate is open.** Incomplete validation can mean the maximum fare or a
  fine. On light rail, a card rider on Dan validates at the entry and exit gates, or at the platform
  machine before riding where there are no gates. In Jerusalem a card rider validates at the platform
  machine or immediately on entering the train. **An app rider selects the current station and
  validates before boarding** on both systems, and also at the exit where the station has gates. On the Rakevelit and Carmelit, validate at the entry and exit gates. A free child under 5 does not validate, and soldiers validate with the army's Zuzu app or
  by showing their military ID. A rider who believes a fine was wrong can appeal through the
  online form linked from `https://bus.gov.il/how-to-pay`.
- **Single-ride discounts on a Rav-Kav are given when loading stored value:** 100 NIS loaded becomes
  200 at 50% and 150 at 33%, and each ride then deducts the ordinary fare.
- **Discharged soldiers must apply within two months of discharge.** The profile then runs one year
  from the application, and at most one year and two months from discharge. Missing that window can
  lose the entitlement.
- **Geographic profile** covers residents of areas in socio-economic clusters 1-5 and peripheral
  local authorities (excluding statistical areas in clusters 9-10), and is valid two years. Conditions
  and proof of address apply, see `https://bus.gov.il/Geographic-Area`.
- **Student profile via the payment apps gives 33% on single rides only.** The semester and annual
  passes exist only on a physical Rav-Kav card, so an app-only student loses the pass benefit. A
  student under 27 should also compare the Young Adult profile (33% on monthly passes) and confirm
  with *8787 which profile the app will apply.
- Profiles are set in the payment apps, in the Rav-Kav apps and websites, or at an "Al HaKav"
  service centre. Two exceptions: national and civil service volunteers update only at Al HaKav, and
  soldiers, police and prison staff get their card from their employer, not from Al HaKav. New
  Rav-Kav cards cannot be issued at kiosks or top-up machines.

**No cash on board.** A rider cannot pay cash or load a card during the ride, so arrange a Rav-Kav, an app or (where available) a bank card before boarding. An anonymous Rav-Kav carries only single rides, stored value or a day pass.

**Paying without a physical Rav-Kav card:** As of 2026 the physical Rav-Kav card is supplemented by phone-based payment. The Ministry of Transport (PTI / Rashut Artzit l'Tachbura Tziburit) approves five payment apps that work uniformly across operators: Moovit, HopOn Rav-Pass, Pango, Cello (Cellopark) and egg. Typical flow: scan a QR sticker by the bus doors, pick a destination or distance, confirm. Apps charge once a month (the authority's pages give the 24th or the 25th; debit cards are charged daily), with profile discounts applied retroactively. If a day's or a month's rides add up to the day-pass or monthly-pass price, the rider pays only the pass price, so there is no need to buy a pass in advance (the student profile is the exception: in an app it gives 33% on single rides only). App payment also works on Israel Railways. On Israel Railways, generate a barcode in the app at both the entry and the exit station, even if the gates are open: skipping the exit barcode can price the trip at the maximum fare. In an app, no scan is needed when changing trains or moving between platforms, for example at Rosh HaAyin North on the Eastern Railway. On NFC phones, a physical card can be loaded through Rav-Kav Online, HopOn Rav-Pass or egg.

**Paying by bank card:** tapping a Visa or Mastercard, or a phone or watch wallet, works on selected lines only: Dan and Superbus in Gush Dan, and Egged in the Haifa-Krayot area, Jerusalem and Eilat. It buys a single ride only, with no 90-minute transfer, no combination with the light rail, and no profile discount. Do not suggest it to a rider who has a discount profile or needs a transfer. Separately, a single Israel Railways ride can be bought by credit card at the station entrance. A physical Rav-Kav is still the most reliable option for tourists and for discount profiles that must be loaded onto a card, and a new card is issued on the spot at an Al HaKav service centre.

### Step 6: Shabbat and Holiday Considerations
- **Shabbat:** Most public transit stops Friday afternoon (~2-4 PM) and restarts gradually on Saturday evening, often well after Shabbat ends. On Saturday November 28, 2026 the first train in the Ministry feed left at 19:04, over two hours after sunset. Check the actual first departure
- **Exceptions:** Some shared taxi routes (sherut/monit sherut) operate on Shabbat on popular routes
- **Night lines:** the authority publishes a national night-line list (`https://bus.gov.il/nightlines`) covering the north, centre, Jerusalem area, south and Sharon, on lines such as Jerusalem 102/103/106/107/108, Haifa 200/205/208, Tel Aviv 273/296/425/489 and Eilat 10/11. During the school year they run on Thursday and Saturday nights; in school holidays they run daily except Friday night. Check that list before telling a user there is nothing after midnight.
- **Holidays:** Reduced or no service on Jewish holidays (Rosh Hashana, Yom Kippur, etc.)
- **Yom Kippur:** No public transit nationwide (roads closed in most areas)

### Step 7: Accessibility
- The authority lists the urban bus fleet as 100% accessible; intercity coaches are only partly accessible
- Train stations and the light rail systems are step-free, with lifts or ramps
- The Ministry of Transport GTFS feed flags wheelchair accessibility per trip (`wheelchair_accessible` in `trips.txt`), not per stop or route, and operator apps plus Moovit let users filter for accessible routes and stops
- Intercity buses are only partly accessible: 45 lines, one wheelchair place, and booking at least 24 hours ahead: by 16:00 the day before on Sunday to Thursday, and by 12:30 on Friday for Saturday night or Sunday. There is no travel without a booking (`https://bus.gov.il/accessability`)
- For a specific station or stop, check the operator website or app, or the Ministry of Transport accessibility info, before travel
- Israel Railways offers an assistance service for passengers with disabilities that should be booked in advance, with 7 hours' notice recommended

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
Result: Option 1 -- Train from Tel Aviv Savidor to Jerusalem Yitzhak Navon (~44 min), then Light Rail Red Line to City Hall (~9 min), then walk (~15 min). Option 2 -- Egged bus 480 from Tel Aviv Savidor to Jerusalem Central (~44 min scheduled, longer in traffic), then bus to Old City area.

### Example 2: Real-Time Arrivals
User says: "When is the next bus at stop 40001?"
Result: Query `https://curlbus.app/40001` (stop 40001 is Amphitheatre, Caesarea) and return the next 3-5 arrivals with line numbers, destinations, and estimated minutes. An empty `visits` array means no scheduled arrivals right now (common at night and on Shabbat), which is different from an invalid code.

### Example 3: Shabbat Travel
User says: "Can I take a bus from Haifa to Tel Aviv on Saturday?"
Result: Regular bus and train service does not operate on Shabbat. Some private shared taxis (sherut) run on Shabbat but are not reliably listed, so confirm the route with the operator first. Regular service restarts gradually on Saturday evening, so check the first departure.

## Bundled Resources

### Scripts
- `scripts/check_transit.py` -- List the main Israeli transit operators with regions and websites, check real-time bus arrivals at a stop via curlbus, display Rav-Kav fare structure and discount profiles, and provide Shabbat/holiday service schedules. Supports subcommands: `operators`, `stop`, `fares`, `shabbat`. Run: `python scripts/check_transit.py --help`

### References
- `references/operators-and-gtfs.md` -- Table of the main Israeli transit operators (Egged, Dan, Kavim, Superbus, Afikim, Nateev Express, Israel Railways, light rail) with regions and websites, GTFS data source URL (gtfs.mot.gov.il), real-time data endpoints (curlbus, SIRI), Rav-Kav balance check URL, student semester and annual pass prices, and Shabbat service timing. Consult when identifying which operator runs a route, pricing a student pass, or accessing GTFS data feeds.
- `references/domain-checklist.md` -- Coverage checklist of fare products, discount profiles and payment channels, with the authority page for each. Note: Metropoline and Kavim continue to operate as separate entities despite ongoing bus reform consolidation plans.

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
| Maslulan, the authority's route planner | https://route.bus.gov.il | Exact fare and route for a specific trip |
| National Public Transport Authority, fares | https://bus.gov.il/FaresDistance | The full fare table by distance ring, and the contract types |
| National Public Transport Authority, discounts | https://bus.gov.il/discounts | Every discount profile, monthly-pass prices per discount level, eligibility calculator |

## Gotchas
- Israeli public transit does not run on Shabbat in most of the country. It stops well before sunset, from about 2-4 PM on Friday, and restarts gradually on Saturday evening, often well after Shabbat ends. Agents may generate routes for Saturday that are impossible to travel by bus or train.
- Bus line numbers in Israel can have Hebrew letter suffixes (e.g., line 5 vs. line 5-aleph) that indicate different routes. Agents may treat these as the same line.
- The Israel Railways schedule changes between summer and winter time. Agents may use a cached schedule from the wrong season.
- Since the April 25, 2025 reform, riders aged 67+ ride free. Agents may still apply older senior rules and give wrong fare estimates.
- The GTFS host's root page does not serve the feed and is not a health signal. The feed file itself, `https://gtfs.mot.gov.il/gtfsfiles/israel-public-transportation.zip`, is served normally (verified November 2026). Fetch the file, do not judge the feed by the root page.
- Fares depend on the distance ring, not on the operator or the city. An agent that answers every fare question with the 8 NIS yellow-ring figure will understate an intercity ride by up to 9x, and will miss the daily pass, which beats three single rides in every ring. For a same-day return it is already cheaper by bus from the light-blue ring up, and by train from the green ring up.
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