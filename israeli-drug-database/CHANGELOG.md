# Changelog

## 1.4.0 (2026-10-28)

The Ministry of Health moved the drug registry (confirmed 2026-10-28). Every registry call in 1.3.x is dead.

### Fixed

- **The registry moved to `registries.health.gov.il/Medicines`.** `israeldrugs.health.gov.il` now
  only redirects there, and the old POST API at `/GovServiceList/IDRServer/` (`SearchByName`,
  `GetSpecificDrug` and the rest) answers 403 from CloudFront. Step 2, the examples, the reference
  guide and the script were rewritten against the new API: `GetMedicines` (POST) plus GET endpoints
  for the record, basket indications, documents, packages, ATC and the ingredient list. Every
  endpoint, field and error shape was called live on 2026-10-28.
- **Prescription status is read per PACK from `packages[].mirsham`.** One registration can sell
  some pack sizes without a prescription and others only on prescription (SINUFED TABLETS), so the
  skill reports status per pack and never infers "prescription-only" from absence in the `otcOnly`
  filter.
- **A price of 0 means "no price listed".** It is 0 for most prescription packs, so the old
  "not sold at retail / hospital-only" reading was wrong and is removed.
- **Leaflets:** the newest consumer leaflets per language come first (there can be two), older
  ones are listed separately because they can belong to another pack or sales channel, archived
  uploads are skipped, and an amendment notice dated after a language's newest leaflet is handed
  over with it.
- **Generics:** veterinary products are excluded, ingredient synonyms (DIPYRONE / METAMIZOLE SODIUM)
  are queried separately, and the result is a per-ingredient list for the pharmacist, not a list
  of substitutes. Release markers are shown only where the registry states them, matched as whole
  words; a missing marker is never read as immediate release, because the registry records release
  type inconsistently.
- **Basket flag on OTC products:** basket terms apply only to supply through the kupah, not to a
  counter purchase.
- The recall page is no longer given a name it does not carry.
- **Leaflets now resolve against `pharmaceuticalreg.health.gov.il`,** the file host the new
  registry site uses.
- **Error handling rewritten.** On the new host a missing registration, a misspelt endpoint and a
  wrong method all answer HTTP 200, so the script checks the inner `statusCode` instead.
- **`scripts/lookup_drug.py` rewritten** for the new API.

### Updated figures

- Keytruda basket indications: 87 (was 101 under the old API).
- `acamol`: 13 active registrations.
- Listed single-ingredient paracetamol package prices: 5.03 to 40.24 NIS.

### Notes

- The recommended `israel-drugs` MCP still calls the retired API and is marked as broken until its
  maintainer updates it.

## 1.3.1 (2026-08-27)

- Narrows the declared tool privileges from a bare `Bash` to `Bash(python:*) Bash(curl:*)`, which is
  what the skill actually needs (run the bundled script, POST to the registry) and matches the
  convention used across this repo. 1.3.0 had corrected the previously wrong `WebFetch`-only
  declaration, since WebFetch cannot issue the POST requests the registry requires, but declared
  more than necessary in doing so.

## 1.3.0 (2026-08-27)

Every API claim in this release was verified by calling the endpoint live, with a deliberately
fabricated path as a negative control.

### Corrected

- **Two documented endpoints do not exist.** `SearchGenericByDragRegNum` and
  `SearchByPackageBarcode` return the server's generic HTML error page, the same page a fabricated
  path returns. The real names are `SearchGeneric` and `SearchByBarcode`.
- **`SearchByName`'s payload was wrong.** It takes `val`, `prescription`, `healthServices`,
  `pageIndex` and `orderBy`. The documented `prefix` parameter makes the call fail.
- **`SearchByName` and `GetSpecificDrug` return different schemas.** The single field table was
  replaced with one per endpoint. Field names cannot be carried across.
- **"The registry returns only whether a drug is in the basket" was wrong**, and dangerously so.
  `GetSpecificDrug` returns per-indication entitlement: Keytruda has 101 `salList` entries, plus
  `frameworkOfInclusion` conditions and a `limitations` string. Answering "yes, it is covered" from
  the boolean alone tells a patient whose indication is not on that list that they are covered.
- **"sam mefakach"** corrected to `סם מסוכן`, the statutory term, and a GSL row added.

### Removed

- **The copay tier table and the "generic 10-20 NIS / brand 30-50 NIS" ranges.** No kupah charges a
  fixed amount per package. The real structure is a banded percentage with a floor, set per kupah,
  with quarterly ceilings for chronic patients and separate exemption tracks. The mechanism and a
  dated worked example replace the invented figures.
- **The pregnancy A/B/C/D/X table**, from both language files and the script. The FDA's PLLR removed
  those categories effective 30 June 2015. Pregnancy and breastfeeding questions now route to the
  Israeli Teratology Information Service, which is the Ministry of Health's own referral.
- **"Generics are typically 40-60% cheaper."** Sourced to nothing. Real paracetamol registrations on
  one page spanned 12.10 to 28.60 NIS, so no single figure describes the market. Compare the prices
  actually retrieved.
- **The script's frozen table of brands** with hardcoded dose, prescription and basket values. It
  was verifiably wrong against the live registry, and basket and prescription status belong to a
  registration number rather than a brand name.

### Added

- **Hard refusal rules**: never state a dose, an interaction, a pregnancy conclusion, or any status
  from memory. Where a claim cannot be verified, say so and route to a pharmacist or physician.
- **The prescription-status contradiction**: `GetSpecificDrug.isPrescription` disagrees with
  `SearchByName.prescription` for real products, and would report an intravenous oncology biologic
  as available without a prescription.
- **Pagination**: results come 10 to a page with a `pages` count. Ten results is a page, not an
  answer.
- **How to reach the right leaflet.** `brochure[]` is dominated by amendment notices; the consumer
  leaflet is `type == "עלון לצרכן"`, and the `url` is a bare filename that resolves against
  `https://mohpublic.health.gov.il/IsraelDrugs/`.
- Status codes carry no signal on this host: a fabricated path answers 200 with HTML and a live
  endpoint under load answers 502. Assert on the body parsing as JSON.
- The adverse-event reporting portal, the recall collection, and the off-basket routes (exceptions
  committee, request to add to the basket, appeal), replacing the previous supplementary-insurance
  framing.
- A caveat that dipyrone is OTC in Israel but restricted elsewhere.

### Script

Rewritten to query the live registry: `search`, `drug`, `generics`, `prescription-types`. It pages
to completion, refuses on any non-JSON body, distinguishes the maintenance page from an error page,
diagnoses local TLS failures rather than blaming the service, and never prints a dose.

## 1.2.0

- Earlier release. See optimization-log.json.
