# Israeli Transit Operators and GTFS Reference

## Operators

| Operator | Hebrew | Modes | Region | Website |
|----------|--------|-------|--------|---------|
| Egged | eged | Bus | Nationwide | egged.co.il |
| Dan | dan | Bus | Gush Dan | dan.co.il |
| Metropoline | metropolin | Bus | Central | metropoline.com |
| Kavim | kavim | Bus | Central/Jerusalem | kavim-t.com |
| Superbus | superbus | Bus | Central/South | superbus.co.il |
| Electra Afikim | elektra afikim | Bus | Center/South/Judea-Samaria/Dan | electra-afikim.co.il |
| Nateev Express | nativ express | Bus | Negev | nateevexpress.com |
| Israel Railways | rakevet yisrael | Train | National | rail.co.il |
| Jerusalem LR | harakevet hakala | Light Rail | Jerusalem | cfir.co.il |
| Tel Aviv LR | harakevet hakala | Light Rail | Tel Aviv | nta.co.il |

## GTFS Data
- Source: Ministry of Transportation
- Feed file: https://gtfs.mot.gov.il/gtfsfiles/israel-public-transportation.zip (this is the URL to fetch)
- Note: the site root https://gtfs.mot.gov.il/ returns a Hebrew error page with HTTP 200. That does not mean the feed is down; fetch the file itself.
- Format: GTFS static + GTFS-realtime
- Update: Daily
- Stop codes live in stops.txt. They are 1 to 6 digits, not uniformly 5.

## Real-Time Data
- curlbus: https://curlbus.app/{STOP_CODE}
- SIRI: Ministry of Transportation real-time feed

## Rav-Kav
- Balance: https://ravkavonline.co.il/
- Types: Personal (ishi), Anonymous (anonimi)
- Transfer: unlimited free transfers within 90 minutes of the first validation, on single rides up to 15 km (yellow ring) only
- Official fare table: https://bus.gov.il/FaresDistance
- Official discount profiles: https://bus.gov.il/discounts

## Shabbat
- Service stops: Friday ~2-4 PM
- Service resumes: Saturday ~30 min after sunset
- Yom Kippur: No transit nationwide
