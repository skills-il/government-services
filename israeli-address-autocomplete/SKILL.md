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

Example: rechov Rothschild 42, Tel Aviv-Yafo, 6688312

### Step 2: Validate Components
1. **City:** Check against CBS official settlement list (~1,300 entries)
2. **Street:** Verify street exists in the city (data.gov.il street database)
3. **Number:** Validate format (number, optional apartment/entrance)
4. **Postal code:** 7 digits, verify matches the address area

### Step 3: Lookup Missing Data
- **No postal code:** Look up via Israel Post website or reference data
- **No city code:** Look up in CBS settlement code table
- **No street:** Suggest closest matching streets in the city

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
| Block / parcel (gush/helka) | גוש / חלקה | 6213 / 250 | Tabu / land registry / mas shevach. Look up on `mapi.gov.il/Pages/LotAddressLocator.aspx` or GovMap |
| Sub-parcel | תת-חלקה | 5 | Apartment-level land registry |
| Settlement code (CBS) | קוד יישוב | 5000 (Tel Aviv) | Government forms requiring canonical settlement |

Kibbutz / moshav addresses typically have no street name, just `משק [number], מושב X` or `קיבוץ X`. Form designers should handle this case explicitly.

## Examples

### Example 1: Format Address
User says: "Format this address for a form: rothschild 42 tel aviv"
Result: Hebrew: rechov Rothschild 42, Tel Aviv-Yafo | Mikud: 6688312 | CBS Code: 5000

### Example 2: Find Postal Code
User says: "What's the mikud for Herzl 10, Haifa?"
Result: 7-digit postal code with area identification

### Example 3: Batch Address Validation
User says: "I have a CSV with 500 Israeli addresses, validate and add postal codes"
Actions:
1. Parse each address into components
2. Look up CBS settlement codes
3. Resolve postal codes (mikud)
4. Flag invalid or ambiguous addresses
Result: Validated CSV with postal codes, CBS city codes, and flags for addresses needing manual review.

## Bundled Resources

### Scripts
- `scripts/lookup_address.py` - Look up CBS city codes, parse and format Israeli addresses into structured components, and list all known cities with their codes and area codes. Supports subcommands: `city`, `format`, `cities`. Run: `python scripts/lookup_address.py --help`

### References
- `references/city-codes.md` - CBS settlement codes for the top 30 Israeli cities by population, including district, Hebrew transliteration, and telephone area codes. Also covers the 7-digit postal code (mikud) format and standard address structure. Consult when resolving city names to CBS codes or validating address components.

## Gotchas
- Israeli street names exist in both Hebrew and Arabic, with different official spellings. Agents may use only the Hebrew name, missing valid Arabic variants that appear on government documents.
- Israeli city names have multiple valid transliterations (e.g., "Tel Aviv" vs "Tel-Aviv" vs "Tel Aviw"). Agents should normalize inputs before matching.
- Settlement and neighborhood boundaries in Israel are politically sensitive. Agents should avoid making assumptions about municipal boundaries, especially for areas in the West Bank or Golan Heights.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| CBS settlements directory | https://www.cbs.gov.il | Official Israeli settlement and locality codes |
| Israel Post mikud lookup | https://doar.israelpost.co.il/locatezip | Postal code (mikud) lookup web form (no documented public API; community lib `bennymeg/IsraelPostalServiceAPI`) |
| GovMap (national map) | https://www.govmap.gov.il | Address search, gush/helka (block/parcel) info, aerial imagery |
| Mapi.gov.il LotAddressLocator | https://www.mapi.gov.il/Pages/LotAddressLocator.aspx | Official block/parcel by address tool |
| data.gov.il (open datasets) | https://data.gov.il/dataset | Street and locality datasets, daily-refreshed. Search "רחובות" for street data, "ישובים" for settlements |

## Troubleshooting

### Error: "Street not found"
Cause: Spelling variation or renamed street
Solution: Try common transliteration variants. Many streets have Hebrew-only official names.

### Error: "Postal code not matching address area"
Cause: Israel Post periodically updates mikud codes, especially in new developments
Solution: Use the current Israel Post API or CBS settlement file for up-to-date postal codes. New neighborhoods may have different mikud codes than their parent city.

### Error: "City name ambiguity"
Cause: Multiple Israeli settlements share similar names (e.g., Kfar Saba vs Kfar Sava, Ramat Gan vs Ramat HaSharon)
Solution: Use CBS settlement code for unambiguous identification. Present the user with a list of matching settlements with their codes and district for disambiguation.