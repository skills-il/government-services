# Israeli Drug Registry Guide

Field definitions, prescription categories and the real copay structure. Registry facts here were
read from the live registry on 2026-10-28; other facts from the cited pages on 2026-08-27.

## Ministry of Health Drug Registry

- Service page: https://www.gov.il/he/service/israeli-drug-index
- Registry search UI: https://registries.health.gov.il/Medicines
- API base: `https://registries.health.gov.il/api/Medicines/`
- Leaflet and image files: `https://pharmaceuticalreg.health.gov.il/api/pharmaregistration/IsraelDrugs/<fName>`
- Public access, covers pharmaceuticals approved in Israel.

**The registry has moved (confirmed 2026-10-28).** `israeldrugs.health.gov.il` now only redirects to
`registries.health.gov.il/Medicines`, and the old POST API at
`israeldrugs.health.gov.il/GovServiceList/IDRServer/` (`SearchByName`, `GetSpecificDrug`,
`SearchByBarcode`, `SearchGeneric`, `SearchByAdv` and the lookup lists) answers 403 from CloudFront.
Nothing in this guide refers to those names any more except to say they are dead. The old
`data.health.gov.il` domain was retired earlier.

## Endpoints

Read from the network calls the new registry site makes, and each called live on 2026-10-28.

| Endpoint | Method | Input |
|----------|--------|-------|
| `GetMedicines` | POST | `{searchText, pageNumber, maxResult, sortBy, sortDirection, includeActive, includeCanceled}`; several `componentCodes` in one list are ANDed; optional `otcOnly`, `basketOnly`, `telemOnly`, `componentCodes`, `barkod`, `humanVet`, `tradeName`, `regNumber`, `manufacturerCode`, `ownerCode` |
| `GetMedicineByRegNumber` | GET | `?regNumber=` (URL-encode the spaces) |
| `GetMedicineBasketIndications` | GET | `?medicineId=` |
| `GetMedicineDocuments` | GET | `?medicineId=` |
| `GetMedicinePackages` | GET | `?medicineId=` |
| `GetMedicineAtc` | GET | `?medicineId=` |
| `GetMedicineImages` | GET | `?medicineId=` |
| `GetMedicineSites` | GET | `?medicineId=` |
| `GetComponents`, `GetTradeNames`, `GetRegNumbers`, `GetManufacturers`, `GetOwners` | GET | lookup lists, `[{key, value}]` |

**Response envelope:** `{"returnObject": ..., "statusCode": 200, "message": "Success"}`. The HTTP
status carries no signal:

- A registration number that does not exist: HTTP 200, `{"returnObject": null, "statusCode": 404, "message": "לא נמצאה תרופה"}`.
- A misspelt endpoint, or a GET sent to `GetMedicines`: HTTP 200 with an HTML page titled `Error`.
- A missing parameter: HTTP 200 with `{"ClientMessage": ..., "StatusCode": 400}` (capital S, no `returnObject`).
- The retired IDRServer API: HTTP 403 HTML from CloudFront.

Only a JSON body whose lowercase `statusCode` is 200 is an answer.

**Pagination:** `pageNumber` is zero-based, `maxResult` sets the page size, and `totalRows` gives the
full count. `acamol` has 13 active registrations, so a 10-row page is incomplete.

## Key fields

`GetMedicines` returns `returnObject.medicinesList[]`; `GetMedicineByRegNumber` returns one record of
the same shape.

| Concept | Field |
|---------|-------|
| Names | `tradeName`, `tradeNameHeb` |
| Registration number | `regNumber` |
| Internal id (for the GET endpoints) | `medicineId` |
| Active ingredient | `components[].componentDesc`, `componentCode`, `dosage` |
| Authorisation holder / manufacturer | `ownerName`, `manufacturerName` |
| Basket | `basket` (`כן` / `לא` string), `limitations`, `framework`, `dateOfInclusion` |
| Prescription | `packages[].mirsham` (1 = prescription, 0 = not), per pack |
| Price | `packages[].customerPriceWithTax`, per pack; `0` = no price listed |
| Status and dates | `canceled` (`כן` / `לא`), `regDate`, `regExpDate` (ISO dates) |
| Other | `indication`, `useInClalit`, `veterinaryUse`, `dosageFormE`, `dosageFormHeb` |

Prescription status is `packages[].mirsham`, set per PACK; the site renders `1` as
`חייב במרשם רופא`. One registration can mix both (SINUFED TABLETS `030 06 25464 00`: the 10-tablet
pack is `0`, the larger packs `1`). The `otcOnly` filter returns only registrations whose packs are
all `0`, so absence from it does NOT mean prescription-only. Specialist or hospital restriction
arrives as prose in `limitations`. There is no field called `sug mircham`.

## Prescription categories

- **GSL** (תרופות לשיווק כללי): sellable outside a pharmacy. The `telemOnly` filter on `GetMedicines` selects them; GSL can be pack- or channel-specific, so absence from that filter proves nothing.
- **OTC** (ללא מרשם): no prescription needed at a pharmacy. `mirsham: 0` on the pack.
- **Prescription** (מרשם): physician's prescription required. `mirsham: 1` on the pack.
- **Restricted** (מרשם מוגבל): specialist or hospital-only. Surfaces in `limitations`.
- **Dangerous drug** (סם מסוכן): controlled under פקודת הסמים המסוכנים, special prescription form.

Earlier versions of this guide used "sam mefakach" for the last category. The statutory term is
`סם מסוכן`.

## Health basket: entitlement is per indication

`basket: כן` is not a coverage answer for an expensive drug. `GetMedicineBasketIndications`
returns one entry per covered indication with `indication`, `includeDate`, `clinicDesc` and
`sicknessState`. Keytruda has 87 entries (2026-10-28). `framework` adds line-of-therapy and
duration conditions, and `limitations` records who may prescribe.

- An empty indication list + a general-use `limitations` (`תרופה שאושרה לשימוש כללי בקופ'ח`) means unrestricted.
- A populated indication list means entitlement exists ONLY for the listed indications.

Basket status is per registration number, not per brand. Verified 2026-10-28: `ACAMOL`
(`020 16 20534 00`) is `basket: כן` while `ACAMOL TEVA CAPLETS` and `ACAMOL FOCUS` are `basket: לא`;
`LOSEC 20 MG` is `basket: לא` while `LOSEC 20 MG RX` is `basket: כן`; all three GLUCOPHAGE XR
strengths are `basket: לא`.

The list is closed and updated annually. The binding instrument is
`צו ביטוח בריאות ממלכתי (תרופות בסל שירותי הבריאות), תשנ"ה-1995`. The effective date of a given
year's expansion is set by that year's director-general circular, so do not promise January.

## Copay: a banded percentage with a floor, set per kupah

The registry does NOT hold copay. `customerPriceWithTax` is the consumer price the registry lists
for a pack, where it lists one. A value of `0` means no price is listed: that is the normal case for
prescription packs (every Lipitor and Nexium tablet pack), so it says nothing about availability and
does not mean free. Basket terms apply only to supply through the kupah; an OTC product flagged
`basket: כן` bought at the counter is at the pharmacy's price.

Each kupah sets its own schedule and the collection rules differ between them
("סדרי הגבייה של קופות החולים אינם זהים", kolzchut/תרופות_בסל_הבריאות). Leumit's published
schedule is a worked example, dated, and must be re-read rather than quoted from here:

- No generic alternative: up to 20.80 NIS pay the consumer price; 20.80 to 156.30 pay 20.80; above 156.30 pay 15% of the price.
- A generic alternative exists: up to 20.80 pay the consumer price; above 20.80 pay 10% of the price or 20.80, whichever is HIGHER.

Chronic patients have a quarterly ceiling above which basket drugs are free. As of May 2026,
kolzchut/תקרת_תשלום_ברכישת_תרופות_לחולים_כרוניים records Clalit at 1,190 NIS per quarter and
Maccabi at 1,137 NIS per quarter, with lower ceilings for pension-age members on income support.
Separate exemption tracks exist for severe illness and other populations.

Earlier versions of this guide printed a fixed shekel-per-package copay range and a
four-tier coverage table. Both were removed: the fixed-shekel-per-package framing is not how any
kupah charges, and the tier taxonomy was not drawn from any published source.

## Off-basket routes

If an indication is not in the basket, the routes are the kupah's exceptions committee
(`ועדת חריגים לתרופות מחוץ לסל הבריאות`), a request to add the drug to the basket, and an appeal to
the National Health Insurance public complaints commissioner. A kupah is not obliged to supply an
off-basket drug. Supplementary insurance (shaban) and compassionate use are different things from
each other and from the exceptions route.

## Generic drugs

- Same active ingredient, strength and dosage form; different marketing authorisation holder.
- Find them by looking the ingredient up in `GetComponents` and calling `GetMedicines` with
  `componentCodes`, paging to `totalRows`. One substance can have several keys (DIPYRONE 2764,
  METAMIZOLE SODIUM 1679): query each key separately and merge, since several keys in one list are
  ANDed and return 0. The filter also returns combination and veterinary products; keep records
  with one entry in `components` and `veterinaryUse` of `לא`.
- Present them as a list for the pharmacist, not as substitutes, one list per ingredient. Release
  type is not recorded reliably (NEXIUM and LOSEC carry no marker; ESOMEPRAZOLE INOVAMED says
  GASTRO RESISTANT), so a missing marker never means immediate release, and a product that carries
  one (SLOW / PROLONGED RELEASE, GASTRO RESISTANT, or CR / XR / SR / OD / RETARD as a whole word in
  the name; not CRESTOR, not the famotidine brand GASTRO) is not offered in place of another by the agent; the pharmacist decides. A
  liquid's strength can read like a tablet's (TRAMARAZ drops: `100 MG`). Form spelling alone
  (FILM COATED TABLETS / COATED TABLETS / TABLETS) is not a difference.
- **Compare the actual `customerPriceWithTax` values retrieved, like for like, and say when none is listed.** Earlier versions of
  this guide said generics are cheaper by a fixed percentage band. That figure was sourced to
  nothing and is removed: single-ingredient paracetamol packages retrieved on 2026-10-28 ranged from
  5.03 to 40.24 NIS across strengths and pack sizes.
- Switching is a decision for the prescriber and the pharmacist.

## Safety routing

- Dosing, maximum daily dose, interactions: never answered by this skill. Return the CONSUMER leaflet and route to a pharmacist. `GetMedicineDocuments` mixes physician leaflets, consumer leaflets and `החמרה לעלון` amendment notices; filter on `type == "עלון לצרכן"`, take the language from `language`, else `langDesc` (both are sometimes empty, as on both current Keytruda leaflets; then open the file), skip archived `Arc*` uploads, lead with the newest leaflet(s) per language (ACAMOL `128 74 25337 08` has two Hebrew ones dated 2025-05-12) and list the older ones separately rather than dropping them, since an older leaflet can be the one for another pack or channel (ACAMOL TEVA CAPLETS `176 61 37219 99`: general-sale Hebrew 2025-12-17, pharmacy Hebrew 2025-11-24), hand over any `החמרה לעלון` / `החמרה לעלון לצרכן` notice dated on a later day than that language's current leaflet, and resolve the bare `fName` against `https://pharmaceuticalreg.health.gov.il/api/pharmaregistration/IsraelDrugs/`.
- Pregnancy and breastfeeding: route to the Israeli Teratology Information Service, which is the MoH's own referral on the drug-registry service page. The FDA's PLLR removed the A/B/C/D/X letter categories effective 30 June 2015, so that table is not reproduced anywhere in this skill.
- Adverse events: https://sideeffects.health.gov.il/ (service page https://www.gov.il/he/service/adverse_effects_reports). "Yellow Card" is the UK MHRA scheme, not Israel's.
- Recalls: https://www.gov.il/he/departments/topics/drugs-recall/govil-landing-page
