# Israeli Transit Operators and GTFS Reference

## Operators

| Operator | Hebrew | Modes | Region | Website |
|----------|--------|-------|--------|---------|
| Egged | eged | Bus | Nationwide | egged.co.il |
| Dan | dan | Bus | Gush Dan | dan.co.il |
| Metropoline | metropolin | Bus | Central, Sharon, Beer Sheva and Arad | metropoline.com |
| Kavim | kavim | Bus | Central/Jerusalem | kavim-t.com |
| Superbus | superbus | Bus | Jerusalem, the valleys (Emek) and Gush Dan | superbus.co.il |
| Electra Afikim | elektra afikim | Bus | Center/South/Judea-Samaria/Dan | electra-afikim.co.il |
| Nateev Express | nativ express | Bus | North (Safed, Nahariya, Haifa, Acre) | nateevexpress.com |
| Israel Railways | rakevet yisrael | Train | National | rail.co.il |
| Jerusalem LR | harakevet hakala | Light Rail | Jerusalem | cfir.co.il |
| Tel Aviv LR | harakevet hakala | Light Rail | Tel Aviv | nta.co.il |

This lists the main operators only. The authority runs about 40 and publishes all of them with phone numbers at https://bus.gov.il/operators. The national information line is *8787.

## GTFS Data
- Source: Ministry of Transportation
- Feed file: https://gtfs.mot.gov.il/gtfsfiles/israel-public-transportation.zip (this is the URL to fetch)
- Note: the site root does not serve the feed and is not a health signal. Fetch the file itself.
- Format: GTFS static (ZIP). Real-time data is separate (SIRI, below)
- Stop codes live in stops.txt. They are 1 to 5 digits, not uniformly 5.

## Real-Time Data
- curlbus: https://curlbus.app/{STOP_CODE}
- SIRI: Ministry of Transportation real-time feed

## Rav-Kav
- Balance: https://ravkavonline.co.il/
- Types: Personal (ishi), Anonymous (anonimi)
- Transfer: unlimited free transfers within 90 minutes of the first validation, on single rides up to 15 km (yellow ring) only
- Official fare table: https://bus.gov.il/FaresDistance
- Official discount profiles: https://bus.gov.il/discounts

## Student period passes, academic year 2026-27 (NIS)

Rav-Kav card only. Source: https://bus.gov.il/Student-Pass

| Pass | Monthly | Semester A (15/10/26 to 28/02/27) | Semester B (23/02/27 to 31/07/27) | Annual (15/10/26 to 14/10/27) |
|---|---|---|---|---|
| National, bus | 315 | 779.50 | 866.50 | 1,890 |
| National + rail, 40 km | 323 | 799.50 | 888.50 | 1,938 |
| National + rail, 75 km | 464 | 1,148.50 | 1,276 | 2,784 |
| National + rail, unlimited | 684 | 1,693 | 1,881 | 4,104 |
| Area 1 (40 km) | 139 | 344 | 382.50 | 834 |
| Eilat (up to 40 km) | 117.79 | 291.53 | 323.92 | 706.74 |

## Shabbat
- Service stops: Friday ~2-4 PM
- Service restarts gradually on Saturday evening, often well after Shabbat ends. Check the first departure
- Yom Kippur: No transit nationwide
