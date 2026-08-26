---
name: israeli-address-autocomplete
description: Format, validate, and geocode Israeli addresses including postal code (mikud) lookup and CBS city code resolution. Use when user asks about Israeli addresses, "ktovet", postal codes, "mikud", city codes, or needs to format addresses for Israeli forms and systems. Supports Hebrew address formatting and Hebrew-English transliteration. Do NOT use for non-Israeli addresses.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Network access helpful for postal code and geocoding lookups.
---

# Israeli Address Autocomplete

## Instructions

### Step 1: Parse Address Components
Israeli address format: `[Street Name] [Number], [City], [Postal Code]`
Hebrew: `[rechov] [mispar], [ir], [mikud]`

Example: rechov Rothschild 42, Tel Aviv-Yafo, 6688310

**Ask which address the form wants before formatting anything.** Israel has two different
addresses for the same person and they are frequently not the same:

| | מען (registered address) | Delivery address |
|---|---|---|
| What it is | The address recorded in the population registry, printed on the teudat zehut appendix (ספח) | Wherever post actually reaches the person |
| Who controls it | The Interior Ministry. It changes only by filing a change-of-address notice | Israel Post routing, plus whatever the person tells a company |
| Who asks for it | Interior Ministry, Bituach Leumi, the tax authority, courts, voter registration, municipal arnona | Couriers, retailers, banks for statements |

A well-formed, correctly-geocoded, correct-mikud address is still the **wrong answer** to a
Bituach Leumi form that asks for the מען. This skill formats and validates addresses; it cannot
read the population registry. When a government form is involved, say so and tell the user to
take the address from the ספח, and that if the two have diverged the fix is filing a
change-of-address notice with the Interior Ministry, not reformatting the address.

### Step 2: Validate Components
1. **City:** Check against the official settlement list (1,310 entries). Query it from the data.gov.il CKAN datastore, see Step 3.
2. **Street:** Verify the street exists in that city (data.gov.il street dataset)
3. **Number:** Validate format (number, optional apartment/entrance)
4. **Postal code:** look it up per address on the Israel Post form; verify it matches the address area

**Check whether the locality is divided into streets BEFORE you ask for a street.**
Israel Post marks each locality as divided or not. A locality that is NOT divided, which covers
most kibbutzim and moshavim and many Arab localities, has **one locality-wide mikud** and no
street-level postal codes at all. Asking for a street name there is wrong by construction, and
a street-level lookup will return an empty result that looks like a missing address rather than
a category error. Israel Post publishes the list of localities with no delivery address or
mixed delivery at <https://doar.israelpost.co.il/content/no-address>.

### Step 3: Lookup Missing Data

**Settlements and streets: the data.gov.il CKAN datastore is a real keyless public API.** Use
it rather than the HTML catalogue, which no longer exists. Both datasets are published by
רשות האוכלוסין וההגירה (the Population and Immigration Authority), and the code column
`סמל_ישוב` is the same semel yishuv used on government forms.

| Need | Call |
|---|---|
| Resolve a settlement name to its code | `GET https://data.gov.il/api/3/action/datastore_search?resource_id=5c78e9fa-c2e2-4771-93ff-7f400a12f7ba&q=<name>` (1,310 records; fields `סמל_ישוב`, `שם_ישוב`, `שם_נפה`) |
| Check a street exists in a settlement | `GET https://data.gov.il/api/3/action/datastore_search?resource_id=9ad3862c-8391-4b2f-84a4-2d4c68625f4b&q=<street>` (fields `סמל_ישוב`, `שם_ישוב`, `סמל_רחוב`, `שם_רחוב`) |
| Discover other datasets | `GET https://data.gov.il/api/3/action/package_search?q=<term>` |

A bad `resource_id` returns an HTML error page rather than JSON, so parse the response as JSON
and treat a parse failure as a bad request, not as an empty result set.

**Postal code (mikud): there is no keyless public API.** The Israel Post site is backed by a
JSON API on `apimftprd.israelpost.co.il` that requires a subscription key the site injects;
called without one it returns HTTP 401 `Access denied due to missing subscription key`. Do not
scrape that key. The supported route is the web form at
<https://doar.israelpost.co.il/locatezip>, which resolves in three steps: locality, then street
within that locality, then house number. **Do not use `bennymeg/IsraelPostalServiceAPI` for
mikud**, that library is a shipping-price calculator, not an address-to-mikud lookup.

- **No street:** Suggest closest matching streets from the street dataset above.

**Three id spaces that are NOT interchangeable.** Feeding one where another is expected returns
an empty result with no error, which reads as "address not found":

| Id | Example, Tel Aviv-Yafo | Where it is used |
|---|---|---|
| Settlement code (semel yishuv) | 5000 | Government forms, the data.gov.il datasets, this skill's tables |
| Israel Post internal city id | 1212 | Only inside the Israel Post lookup form |
| Street code (semel rechov) | per street | data.gov.il street dataset |
| Israel Post internal street id | per street | Only inside the Israel Post lookup form |

### Step 4: Format Output
Provide address in:
- Hebrew (official format)
- English transliteration
- Structured data (JSON with components separated)

## Major City Codes Reference
| City | Hebrew | CBS Code | Area Code |
|------|--------|----------|-----------|
| Jerusalem | yerushalayim | 3000 | 02 |
| Tel Aviv-Yafo | tel aviv-yafo | 5000 | 03 |
| Haifa | haifa | 4000 | 04 |
| Rishon LeZion | rishon letzion | 8300 | 03 |
| Petah Tikva | petach tikva | 7900 | 03 |
| Ashdod | ashdod | 70 | 08 |
| Netanya | netanya | 7400 | 09 |
| Beer Sheva | beer sheva | 9000 | 08 |
| Holon | holon | 6600 | 03 |
| Bnei Brak | bnei brak | 6100 | 03 |

## Granular Components Israeli forms typically expect

Israeli address forms (Bit, Pelephone, Bituach Leumi, banks) often split a single address into separate fields beyond street + number + city:

| Field | Hebrew | Example | When required |
|-------|--------|---------|---------------|
| Apartment number | מספר דירה | 5 | Multi-unit buildings, virtually always |
| Floor | קומה | 3 | Common, especially Bituach Leumi and gov forms |
| Entrance | כניסה | א | Tel Aviv / Bnei Brak / dense neighborhoods |
| PO Box | ת.ד. | 1234 | Moshavim, government correspondence |
| Block / parcel (gush/helka) | גוש / חלקה | 6213 / 250 | Tabu / land registry / mas shevach. Look up on `gov.il/apps/mapi/parcel_address/parcel_address.html` (Survey of Israel "block-parcel by address") or GovMap |
| Sub-parcel | תת-חלקה | 5 | Apartment-level land registry |
| Settlement code (semel yishuv) | סמל יישוב | 5000 (Tel Aviv-Yafo) | Government forms requiring a canonical settlement. Not the same as Israel Post's internal city id |

Kibbutz / moshav addresses typically have no street name, just `משק [number], מושב X` or `קיבוץ X`. Form designers should handle this case explicitly.

## Examples

### Example 1: Format Address
User says: "Format this address for a form: rothschild 42 tel aviv"
Result: Hebrew: rechov Rothschild 42, Tel Aviv-Yafo | Mikud: 6688310 (from the Israel Post form) | Settlement code: 5000

### Example 2: Find Postal Code
User says: "What's the mikud for Herzl 10, Haifa?"
Result: 7-digit postal code with area identification

### Example 3: Batch Address Validation

User says: "I have a CSV with 500 Israeli addresses, validate and add postal codes"

**Say the hard part first: the mikud half cannot be automated.** Settlement codes and street
validation can, against the CKAN datastore. Mikud cannot: the only source is a key-gated API
whose key must not be scraped, and the web form is one interactive address at a time. Do not
promise a mikud column, and never generate one by pattern or by copying a neighbouring row.

Actions:
1. Parse each address into components
2. Resolve settlement codes against the settlements dataset (automatable)
3. Verify each street exists in its locality against the streets dataset (automatable)
4. Detect localities with no named streets and mark them as locality-wide addresses rather
   than as errors
5. Flag ambiguous localities, and leave the mikud column EMPTY with a per-row reason
6. Tell the user how many rows would need manual mikud lookup, so they can decide whether it
   is worth doing

Result: A CSV with settlement codes, street-validation status, and per-row flags. The mikud
column is deliberately empty, with the count of rows needing manual lookup stated up front.

## Bundled Resources

### Scripts
- `scripts/lookup_address.py` - Look up CBS city codes, parse and format Israeli addresses into structured components, and list all known cities with their codes and area codes. Supports subcommands: `city`, `format`, `cities`. Run: `python scripts/lookup_address.py --help`

### References
- `references/city-codes.md` - CBS settlement codes for the top 30 Israeli cities by population, including district, Hebrew transliteration, and telephone area codes. Also covers the 7-digit postal code (mikud) format and standard address structure. Consult when resolving city names to CBS codes or validating address components.

## Gotchas

- **Every `שם_ישוב` value in the CKAN datasets carries trailing whitespace** (`"אבו גוש "`).
  All 1,310 of 1,310 rows. An exact-match join on the raw field silently returns nothing.
  Strip before comparing.
- **Two localities can share one Latin name on different settlement codes.** The Bedouin
  (שבט) and (יישוב) pairs do exactly this: `ABU QUREINAT` is both אבו קורינאת (שבט) 968 and
  אבו קרינאת (יישוב) 1342, and the Hebrew spellings differ too (קורינאת against קרינאת).
  `KHAWALED` is 986 and 1321; `TARABIN AS-SANI` is 970 and 1346. Matching on the Latin name,
  or on a fuzzy Hebrew match, returns whichever row came first and produces the domain's
  signature failure: a real code belonging to a different settlement. Disambiguate on
  `סמל_ישוב`, and surface both options to the user rather than picking.
- **The dataset's Latin name field `שם_ישוב_לועזי` is hard-truncated at 20 characters**
  (`MODI'IN-MAKKABBIM-RE`, `ASHDOT YA'AQOV(ME'UH`) and is empty on some rows including
  חברון 3400 and סנסנה 3777. Never use it as a join key.
- **Every locality has a self-row in the streets dataset** with `סמל_רחוב = 9000` whose
  `שם_רחוב` is the locality name: exactly 1,310 such rows out of 63,571. Listing streets for a
  locality will otherwise offer the locality's own name as a street. A locality whose ONLY
  street row is this sentinel has no named streets at all, which is a machine-readable test
  for the non-divided case that works at CSV scale, unlike the Israel Post HTML list.
- **When the registry datasets and Israel Post disagree, they are different authorities and
  neither is simply right.** רשות האוכלוסין וההגירה owns the settlement and street lists that
  government forms are validated against; Israel Post owns the mikud and the divided or
  non-divided status. Use the registry for a form's locality and street fields, use Israel Post
  for the mikud, and surface the conflict to the user rather than silently choosing.
- Israeli street names exist in both Hebrew and Arabic, with different official spellings. Agents may use only the Hebrew name, missing valid Arabic variants that appear on government documents.
- Israeli city names have multiple valid transliterations (e.g., "Tel Aviv" vs "Tel-Aviv" vs "Tel Aviw"). Agents should normalize inputs before matching.
- Settlement and neighborhood boundaries in Israel are politically sensitive. Agents should avoid making assumptions about municipal boundaries, especially for areas in the West Bank or Golan Heights.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| CBS | https://www.cbs.gov.il | Statistical publications that use the semel yishuv. Note the machine-readable settlement dataset itself is published on data.gov.il by רשות האוכלוסין וההגירה, not by the CBS |
| Israel Post mikud lookup | https://doar.israelpost.co.il/locatezip | Postal code (mikud) lookup web form, the supported route. The site's backing JSON API requires a subscription key and returns HTTP 401 without one, so there is no keyless public mikud-by-address API. Do NOT use `bennymeg/IsraelPostalServiceAPI` for mikud, that library is a shipping-price calculator |
| Israel Post, localities with no delivery address | https://doar.israelpost.co.il/content/no-address | Authoritative list of localities that are not divided into streets and carry a single locality-wide mikud |
| GovMap (national map) | https://www.govmap.gov.il | Address search, gush/helka (block/parcel) info, aerial imagery |
| GovMap developer docs | https://api.govmap.gov.il/docs/intro | Documentation site, NOT a callable endpoint. GovMap is a JavaScript SDK (`govmap.api.js`), and its search endpoint requires an API key that is bound to an approved domain, so it cannot be called from a CLI or a server-side agent. Treat it as a browser-only option |
| Survey of Israel block/parcel by address | https://www.gov.il/apps/mapi/parcel_address/parcel_address.html | Official gush/helka by address tool (the old mapi.gov.il/Pages/LotAddressLocator.aspx path was retired) |
| data.gov.il CKAN API | https://data.gov.il/api/3/action/package_search | Keyless public API for the street and locality datasets. The former HTML catalogue path `data.gov.il/datasets` now returns HTTP 404 |

## Troubleshooting

### Error: "Street not found"
Cause: Spelling variation or renamed street
Solution: Try common transliteration variants. Many streets have Hebrew-only official names.

### Error: "Postal code not matching address area"
Cause: Israel Post periodically updates mikud codes, especially in new developments. Verified: this is a real cause. Not verified as a cause, so do not assert it: a stale cached mikud in a third-party dataset.
Solution: Re-resolve the mikud on the Israel Post form rather than from any cached list. New neighbourhoods may have different mikud codes than their parent city.

### Error: "Street not found, but the locality exists"
Cause: The locality is not divided into streets. Most kibbutzim and moshavim and many Arab localities have a single locality-wide mikud and no street-level codes, so a street lookup there returns empty rather than erroring.
Solution: Check the locality against <https://doar.israelpost.co.il/content/no-address> before treating an empty street result as a bad address. Format the address as `משק [number], [locality]` or just the locality, and use the locality-wide mikud.

### Error: "City name ambiguity"
Cause: Multiple Israeli settlements share similar names (e.g., Kfar Saba vs Kfar Sava, Ramat Gan vs Ramat HaSharon)
Solution: Use CBS settlement code for unambiguous identification. Present the user with a list of matching settlements with their codes and district for disambiguation.