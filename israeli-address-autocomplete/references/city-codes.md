# Israeli CBS City Codes Reference

Major Israeli cities and their settlement codes (semel yishuv).

**Provenance.** The settlement codes in this file were verified on 2026-08-26 by enumerating
ALL rows against the full 1,310-record authoritative list published on data.gov.il by
רשות האוכלוסין וההגירה (resource_id `5c78e9fa-c2e2-4771-93ff-7f400a12f7ba`). Three codes were
wrong before that check and each was a real code belonging to a different settlement, so the
skill answered confidently wrong rather than erroring. **Never spot-check this table; enumerate
it.** The evidence gate extracts zero numeric facts from bare integer codes and cannot catch
one.

**Telephone area codes in the table are orientation only.** They were NOT verified against the
Ministry of Communications numbering plan in the 2026-08-26 cycle. They are not used for any
lookup and nothing in the skill depends on them. Verify before changing or relying on one.

## Top 30 Cities by Population

| City | Hebrew | CBS Code | District | Area Code |
|------|--------|----------|----------|-----------|
| Jerusalem | yerushalayim | 3000 | Jerusalem | 02 |
| Tel Aviv-Yafo | tel aviv-yafo | 5000 | Tel Aviv | 03 |
| Haifa | haifa | 4000 | Haifa | 04 |
| Rishon LeZion | rishon letzion | 8300 | Central | 03 |
| Petah Tikva | petach tikva | 7900 | Central | 03 |
| Ashdod | ashdod | 70 | Southern | 08 |
| Netanya | netanya | 7400 | Central | 09 |
| Beer Sheva | beer sheva | 9000 | Southern | 08 |
| Holon | holon | 6600 | Tel Aviv | 03 |
| Bnei Brak | bnei brak | 6100 | Tel Aviv | 03 |
| Ramat Gan | ramat gan | 8600 | Tel Aviv | 03 |
| Bat Yam | bat yam | 6200 | Tel Aviv | 03 |
| Rehovot | rechovot | 8400 | Central | 08 |
| Ashkelon | ashkelon | 7100 | Southern | 08 |
| Herzliya | herzliya | 6400 | Tel Aviv | 09 |
| Kfar Saba | kfar saba | 6900 | Central | 09 |
| Ra'anana | raanana | 8700 | Central | 09 |
| Modiin-Maccabim-Reut | modiin | 1200 | Central | 08 |
| Hadera | hadera | 6500 | Haifa | 04 |
| Bet Shemesh | bet shemesh | 2610 | Jerusalem | 02 |
| Lod | lod | 7000 | Central | 08 |
| Ramla | ramla | 8500 | Central | 08 |
| Nazareth | natzrat | 7300 | Northern | 04 |
| Givatayim | givatayim | 6300 | Tel Aviv | 03 |
| Eilat | eilat | 2600 | Southern | 08 |
| Tiberias | tveria | 6700 | Northern | 04 |
| Acre (Akko) | akko | 7600 | Northern | 04 |
| Nahariya | nahariya | 9100 | Northern | 04 |
| Carmiel | karmiel | 1139 | Northern | 04 |
| Afula | afula | 7700 | Northern | 04 |

## Postal Code Format
Israeli postal codes (mikud) are assigned per address and are looked up through the Israel Post lookup form; there is no official public API, so never derive a mikud yourself.
Format: XXXXXXX (7 digits, e.g. 6688310 for שדרות רוטשילד 42, תל אביב-יפו)

## Address Format
Standard: [Street] [Number], [City] [Postal Code]
Hebrew: [rechov] [mispar], [ir] [mikud]
