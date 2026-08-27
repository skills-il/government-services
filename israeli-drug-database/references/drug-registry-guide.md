# Israeli Drug Registry Guide

Field definitions, prescription categories and the real copay structure. Everything here was read
from the live registry or from a cited page on 2026-08-27.

## Ministry of Health Drug Registry

- Service page: https://www.gov.il/he/service/israeli-drug-index
- Registry search UI: https://israeldrugs.health.gov.il/
- API base: `https://israeldrugs.health.gov.il/GovServiceList/IDRServer/` (POST, JSON)
- Public access, covers pharmaceuticals approved in Israel.
- The old `data.health.gov.il` domain is no longer resolvable.

## Endpoints

Read from the registry app's own client, `/scripts/services/serverConnection.js`.

| Endpoint | Payload |
|----------|---------|
| `SearchByName` | `{val, prescription, healthServices, pageIndex, orderBy}` |
| `GetSpecificDrug` | `{dragRegNum}` |
| `SearchByBarcode` | `{barcode, prescription}` |
| `SearchGeneric` | `{val, name, matanId, packageId, atcId, pageIndex, orderBy}` |
| `SearchByAdv` | advanced filters including `isGSL`, `veterinary`, `cytotoxic`, `healthServices` |
| `SearchBySymptom`, `GetBySymptom`, `GetFastSearchPopularSymptoms` | symptom-driven search |
| `GetAtcList`, `GetMatanList`, `GetPackageList` | `{}`, lookup lists |

`SearchGenericByDragRegNum` and `SearchByPackageBarcode` are NOT endpoints. Both return the
server's generic HTML error page: the same 3,438-byte page a deliberately fabricated path returns,
differing only in an incident number (`מספר תקלה`), so compare shape and length, not a hash.

**Status codes carry no signal here.** A fabricated path answers HTTP 200 with an HTML error page;
a real endpoint under load answers HTTP 502 with a maintenance page. Only a body that parses as
JSON is an answer. A wrong PARAMETER name produces the same HTML error page as a wrong path.

**Pagination:** 10 results per page, with a `pages` count on each result.

## Key fields, per endpoint

The two main endpoints return different schemas. Do not carry a field name across.

| Concept | `SearchByName` results[] | `GetSpecificDrug` |
|---------|--------------------------|-------------------|
| Names | `dragHebName`, `dragEnName` | same |
| Registration number | `dragRegNum` | same |
| Active ingredient | `activeComponents[].componentName`, `activeComponentsCompareName` | `activeMetirals[].ingredientsDesc` + `dosage` |
| Authorisation holder | `dragRegOwner` | `regOwnerName`, `manufacturers[]` |
| Prescription | `prescription` | `isPrescription` (unreliable, see below) |
| Price | `customerPrice` (string), `packagesPrices[]` | `maxPrice` (number) |
| Basket | `health` | `health`, `salList[]`, `frameworkOfInclusion`, `indicationIncludedInTheBasket`, `limitations`, `dateOfInclusion` |
| ATC | not returned | `atc[]` (`atc4Code`, `atc5Code`) |
| Leaflet | not returned | `brochure[]` |
| Dates | `dragRegDate` | `regDate`, `regExpDate` (epoch milliseconds) |
| Other | `barcodes` (a single string), `indications`, `iscanceled` | `dragIndication`, `useInClalit`, `iscanceled` |

There is no field called `sug mircham`. Restriction arrives as the boolean `prescription` on
`SearchByName` and as prose in `limitations` on `GetSpecificDrug`.

**`isPrescription` on `GetSpecificDrug` contradicts `SearchByName`.** For Keytruda
(`154 38 34448 00`), `SearchByName` returns `prescription: true` and `GetSpecificDrug` returns
`isPrescription: false`. Take prescription status from `SearchByName` only.

## Prescription categories

- **GSL** (תכשיר שניתן למכור שלא בבית מרקחת): sellable outside a pharmacy. Exposed as `isGSL` on `SearchByAdv`.
- **OTC** (ללא מרשם): no prescription needed at a pharmacy. `prescription: false`.
- **Prescription** (מרשם): physician's prescription required. `prescription: true`.
- **Restricted** (מרשם מוגבל): specialist or hospital-only. Surfaces in `limitations`.
- **Dangerous drug** (סם מסוכן): controlled under פקודת הסמים המסוכנים, special prescription form.

Earlier versions of this guide used "sam mefakach" for the last category. The statutory term is
`סם מסוכן`.

## Health basket: entitlement is per indication

`health: true` is not a coverage answer for an expensive drug. `GetSpecificDrug` returns
`salList[]`, one entry per covered indication with `indication`, `include_date`, `clinic_desc` and
`sickness_state`. Keytruda has 101 entries. `frameworkOfInclusion` adds line-of-therapy and
duration conditions, and `limitations` records who may prescribe.

- Empty `salList` + a general-use `limitations` (`תרופה שאושרה לשימוש כללי בקופ'ח`) means unrestricted.
- A populated `salList` means entitlement exists ONLY for the listed indications.

Basket status is per registration number, not per brand. Verified 2026-08-27: `ACAMOL` is
`health: true` while `ACAMOL TEVA CAPLETS` and `ACAMOL FOCUS` are `health: false`; `LOSEC 20 MG` is
`health: false` while `LOSEC 20 MG RX` is `health: true`; all three GLUCOPHAGE XR strengths are
`health: false`.

The list is closed and updated annually. The binding instrument is
`צו ביטוח בריאות ממלכתי (תרופות בסל שירותי הבריאות), תשנ"ה-1995`. The effective date of a given
year's expansion is set by that year's director-general circular, so do not promise January.

## Copay: a banded percentage with a floor, set per kupah

The registry does NOT hold copay. `customerPrice` / `maxPrice` is the regulated maximum CONSUMER
PRICE, a ceiling on what a pharmacy may charge. A value of `0` means the product is not on the
retail price list (typically hospital-administered), not that it is free.

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
- Find them with `SearchByName` on the ingredient, matching `activeComponentsCompareName` exactly,
  paging to the `pages` count.
- **Compare the actual `customerPrice` values retrieved.** Earlier versions of this guide said
  generics are cheaper by a fixed percentage band. That figure was sourced to nothing and is removed:
  real paracetamol registrations returned on one page ranged from 12.10 to 28.60 NIS.
- Switching is a decision for the prescriber and the pharmacist.

## Safety routing

- Dosing, maximum daily dose, interactions: never answered by this skill. Return the CONSUMER leaflet and route to a pharmacist. `brochure[]` is dominated by `החמרה לעלון` amendment notices; filter on `type == "עלון לצרכן"`, take the newest, pick the language from `lng`, and resolve the bare filename against `https://mohpublic.health.gov.il/IsraelDrugs/`.
- Pregnancy and breastfeeding: route to the Israeli Teratology Information Service, which is the MoH's own referral on the drug-registry service page. The FDA's PLLR removed the A/B/C/D/X letter categories effective 30 June 2015, so that table is not reproduced anywhere in this skill.
- Adverse events: https://sideeffects.health.gov.il/ (service page https://www.gov.il/he/service/adverse_effects_reports). "Yellow Card" is the UK MHRA scheme, not Israel's.
- Recalls and warnings: https://www.gov.il/he/departments/topics/drugs-recall/govil-landing-page
