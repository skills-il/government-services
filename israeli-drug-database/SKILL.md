---
name: israeli-drug-database
description: Query the Israeli pharmaceutical database for drug information, health basket coverage, generic alternatives, and pricing. Use when user asks about Israeli medications, "trufot", drug names, "sal briut" drug coverage, generic drugs, drug prices in Israel, prescription requirements, or medication safety info. Enhances the israel-drugs MCP server with health basket context and patient-facing guidance. Do NOT use for medical advice, dosage recommendations, or diagnosis. Do NOT use for non-Israeli drug registries.
license: MIT
allowed-tools: Bash(python:*) Bash(curl:*) WebFetch
compatibility: >-
  The registry API is POST-only, which WebFetch cannot issue on its own, so a shell (curl) or the
  israel-drugs MCP server is needed for live lookups. Without either, the skill still explains the
  basket mechanism, the copay structure and the prescription categories, but it must then say it
  could not query the registry rather than answering from memory.
---

# Israeli Drug Database

## Critical Note
This skill provides DRUG INFORMATION ONLY, not medical advice.

**Hard refusal rules. These are not style guidance.**

- **Never state a dose, a maximum daily dose, or a dosing schedule**, even one you read in a
  leaflet. Return the leaflet itself (the `brochure[]` entry from `GetSpecificDrug`) and send the
  user to a pharmacist.
- **Never answer a drug-interaction question.** Cross-referencing two active ingredients is a
  clinical judgement. Name the question and route it to a pharmacist.
- **Never state whether a drug is safe in pregnancy or breastfeeding.** Route to the Israeli
  Teratology Information Service, which is the MoH's own referral for this question.
- **Never state prescription status, basket status or price from memory or from a table in this
  skill.** Query the registry for the specific product, and say which registration number you
  answered for.
- Where a claim cannot be verified from the registry or the leaflet, say so and direct the user to
  a pharmacist or physician. Do not guess and do not interpolate.

Drug coverage and pricing change. Copay is set by the user's kupat cholim, not by this skill and
not by the registry.

## Instructions

### Step 1: Identify Drug Query Type
| Query | Action |
|-------|--------|
| Drug lookup | Search registry by name or ingredient |
| Health basket status | Check sal briut coverage tier |
| Generic alternatives | Find equivalent generics by active ingredient |
| Drug pricing | Look up regulated maximum price |
| Safety info | Return the consumer leaflet and route the question. Do NOT answer doses, interactions or pregnancy safety |
| Prescription status | Check if OTC or prescription required |

### Step 2: Drug Lookup
Search the MoH drug registry:
- **By trade name:** Search Hebrew or English brand name (e.g., "Acamol", "Optalgin")
- **By generic/active ingredient:** Search by active substance (e.g., "paracetamol", "dipyrone")
- **By registration number:** Direct lookup by mispar rishum

**Key fields returned:**
| Field | Hebrew | Description |
|-------|--------|-------------|
| Trade name | shem miskhari | Brand name as marketed |
| Generic name | shem bilti muskam / shem generi | International nonproprietary name (INN) |
| Active ingredient | chomer peeil | Active substance and strength |
| Dosage form | tzurat matan | Tablet, capsule, injection, etc. |
| Manufacturer | yatzran | Company holding marketing authorization |
| ATC code | kod ATC | WHO anatomical therapeutic chemical code |
| Registration status | matzav rishum | Active, suspended, or cancelled |
| Prescription type | (no such field) | Returned as the boolean `prescription` on `SearchByName`, and as prose in `limitations` on `GetSpecificDrug`. There is no `sug mircham` field |

**The live registry API.** The canonical machine-readable source is the MoH Israel Drug Registry
backend at `israeldrugs.health.gov.il/GovServiceList/IDRServer/`. All calls are **POST** with
`Content-Type: application/json`. The endpoint names and payload shapes below were read from the
registry app's own client (`/scripts/services/serverConnection.js`) and each was called live on
2026-08-27.

| Endpoint | Payload |
|----------|---------|
| `SearchByName` | `{val, prescription, healthServices, pageIndex, orderBy}` |
| `GetSpecificDrug` | `{dragRegNum}` |
| `SearchByBarcode` | `{barcode, prescription}` |
| `SearchGeneric` | `{val, name, matanId, packageId, atcId, pageIndex, orderBy}` |
| `SearchByAdv` | advanced filters, including `isGSL`, `veterinary`, `cytotoxic`, `healthServices` |
| `GetAtcList` / `GetMatanList` / `GetPackageList` | `{}`, return the ATC, route-of-administration and package-type lookup lists |

**Two endpoint names in earlier versions of this skill do not exist.** `SearchGenericByDragRegNum`
and `SearchByPackageBarcode` both return the server's generic HTML error page: the same 3,438-byte
page a deliberately fabricated path returns, differing only in an incident number
(`מספר תקלה`). Use `SearchGeneric` and `SearchByBarcode`.

**Status codes carry no signal on this host.** A fabricated path answers **HTTP 200** with an HTML
error page; a real endpoint under load answers **HTTP 502** with a maintenance page. Assert on the
BODY: a successful call returns `Content-Type: application/json`. Anything that does not parse as
JSON is a failure, whatever the status line says. Sending a wrong parameter name (an older version
of this skill documented `prefix` on `SearchByName`) also returns the HTML error page rather than a
validation message.

**The two main endpoints return DIFFERENT schemas.** Do not carry a field name across.

| | `SearchByName` results[] | `GetSpecificDrug` |
|---|---|---|
| Name | `dragHebName`, `dragEnName` | same |
| Reg. number | `dragRegNum` (e.g. `020 16 20534 00`) | same |
| Ingredient | `activeComponents[].componentName`, `activeComponentsCompareName` | `activeMetirals[].ingredientsDesc` + `dosage` |
| Marketing authorisation holder | `dragRegOwner` | `regOwnerName`, `manufacturers[]` |
| Prescription | `prescription` | `isPrescription` (**see the warning below**) |
| Price | `customerPrice` (string), `packagesPrices[]` | `maxPrice` (number) |
| Basket | `health` (boolean) | `health`, plus `salList[]`, `frameworkOfInclusion`, `indicationIncludedInTheBasket`, `limitations`, `dateOfInclusion` |
| ATC | not returned | `atc[]` with `atc4Code`/`atc5Code` |
| Leaflet | not returned | `brochure[]` |
| Other | `barcodes` (a single string, not a list), `indications`, `iscanceled` | `dragIndication`, `useInClalit`, `regDate`, `regExpDate`, `iscanceled` |

**Never take prescription status from `GetSpecificDrug`.** The two endpoints disagree. For Keytruda
(`154 38 34448 00`) `SearchByName` returns `prescription: true` while `GetSpecificDrug` returns
`isPrescription: false`, which would report an intravenous oncology biologic as available without a
prescription. Use `SearchByName`, and still tell the user to confirm with the pharmacy.

**Results are paginated, 10 per page.** Each result carries a `pages` count. `acamol` returns 10
results across 2 pages. An agent that reads only page one and says "these are all the products" is
wrong; loop `pageIndex` to the `pages` count before making any completeness claim.

**A `customerPrice` of `"0"` does not mean free.** It means the product is not on the retail price
list, which is the normal case for hospital-administered drugs. Keytruda returns `"0"`.

Treat this as an undocumented public backend: cache results and do not bulk-scrape.

### Step 3: Health Basket Coverage

**Being "in the basket" is not a yes/no answer for most expensive drugs. It is per indication.**
This is the single most consequential thing to get right here. `GetSpecificDrug` returns far more
than the `health` boolean:

- `salList[]` -- one entry per basket-covered indication, each with `indication`, `include_date`,
  `clinic_desc` and `sickness_state`. **Keytruda has 101 entries.**
- `frameworkOfInclusion` -- the conditions of entitlement in prose, including line-of-therapy and
  duration limits.
- `limitations` -- who may prescribe. Acamol: `תרופה שאושרה לשימוש כללי בקופ'ח`. Keytruda:
  `תרופה מוגבלת לרישום ע'י רופא מומחה או הגבלה אחרת`.
- `indicationIncludedInTheBasket`, `dateOfInclusion`.

So: **empty `salList` plus a general-use `limitations` means unrestricted. A populated `salList`
means entitlement exists ONLY for the listed indications.** Answering "yes, it is in the basket"
from `health: true` alone will tell a patient whose indication is not on that list that they are
covered when they are not. Read the list, say how many indications it holds, and tell the user
their entitlement depends on their own diagnosis, which only their physician can match.

**Copay: the registry does not know it, and there is no single national number.** Each kupah sets
its own schedule under the National Health Insurance Law, and Kol Zchut records that the collection
rules differ between them ("סדרי הגבייה של קופות החולים אינם זהים"). The structure is a **banded
percentage with a floor**, not a fixed shekel amount per package. Leumit's published schedule is a
worked example (read the current one, this is dated):

- No generic alternative: up to 20.80 NIS, pay the consumer price; between 20.80 and 156.30, pay
  20.80; above 156.30, pay 15% of the price.
- A generic alternative exists: up to 20.80, pay the consumer price; above 20.80, pay **10% of the
  price or 20.80, whichever is higher**.

There is also a **quarterly ceiling** for chronic patients, above which the drugs are free. As of
May 2026 Kol Zchut records Clalit at 1,190 NIS per quarter and Maccabi at 1,137 NIS per quarter,
with lower ceilings for pension-age members receiving income support. Separate exemption tracks
exist for severe illness and other populations.

Never quote a copay figure of your own. Give the mechanism, then send the user to their own kupah's
schedule.

**Price is not copay.** `customerPrice` / `maxPrice` is the **regulated maximum consumer price**, a
ceiling on what a pharmacy may charge. A basket-covered drug bought through a kupah is priced by the
kupah's copay schedule instead.

**Freshness.** The basket list is closed and updated annually. The legally binding instrument is
`צו ביטוח בריאות ממלכתי (תרופות בסל שירותי הבריאות), תשנ"ה-1995`, not a web page: Kol Zchut states
`רשימת התרופות הנכללות בסל היא רשימה סגורה שמתעדכנת כל שנה`. Do not promise that the update lands
in January; the effective date of a given year's expansion is set by the director-general circular
for that year. Confirm against the current order.

### Step 4: Generic Alternatives
To find generic alternatives:
1. Identify the active ingredient (chomer peeil) of the brand-name drug
2. Call `SearchByName` with the ingredient and match on `activeComponentsCompareName`, which is
   the exact-match ingredient field (Acamol returns `PARACETAMOL`). **Loop `pageIndex` to the
   `pages` count**, or your list is silently truncated at 10.
3. Filter out `iscanceled: true` products.
4. Compare same ingredient, same strength, same dosage form, different `dragRegOwner`.
5. **Compare the actual `customerPrice` values you retrieved.** Do not quote a percentage saving.
   Real paracetamol products returned on one page ranged from 12.10 to 28.60 NIS, so a single
   headline figure would have been wrong in both directions.

`SearchGeneric` also exists, but it needs `matanId` / `packageId` / `atcId` values taken from
`GetMatanList` / `GetPackageList` / `GetAtcList`, and returns an empty list when they do not line
up. The ingredient-match route above is the reliable one.

**Basket and prescription status are per registration number, not per brand.** Verified live on
2026-08-27: `LOSEC 20 MG` is `prescription: false, health: false` while `LOSEC 20 MG RX` is
`prescription: true, health: true`. `ACAMOL` is `health: true` but `ACAMOL TEVA CAPLETS` and
`ACAMOL FOCUS` are `health: false`. All three GLUCOPHAGE XR strengths are `health: false`. Never
answer for a brand; answer for a `dragRegNum` and say which one.

**Common Israeli generics.** All six brands below were confirmed registered and not cancelled on
2026-08-27, with the ingredients shown. Use this to recognise a name, never to answer basket,
prescription or price questions: those are per registration number and must be queried.
| Brand Name | Generic Name | Active Ingredient |
|------------|-------------|-------------------|
| Acamol | Paracetamol generics | Paracetamol |
| Optalgin | Dipyrone generics | Dipyrone (metamizole) |
| Ibufen | Ibuprofen generics | Ibuprofen |
| Losec | Omeprazole generics | Omeprazole |
| Lipitor | Atorvastatin generics | Atorvastatin |
| Norvasc | Amlodipine generics | Amlodipine |

**Dipyrone (Optalgin) needs a caveat.** It is sold over the counter in Israel, but it is restricted
elsewhere: in 2018 the EMA reviewed metamizole-containing medicines and recommended harmonising the
maximum daily dose and the contraindications in pregnancy and breastfeeding, noting the medicine
"may occasionally cause severe side effects, such as effects on the blood", with a binding
Commission decision in March 2019. If a user compares Israeli practice to another country, say
that the status genuinely differs. Route any pregnancy or breastfeeding question to the teratology
service rather than repeating a contraindication yourself. Note also that not every Optalgin
registration is OTC: `OPTALGIN TEVA` returns `prescription: true`.

### Step 5: Drug Safety Information
Provide safety context (NOT medical advice):

**The leaflet is the thing you hand over instead of an answer, so get the right one.**
`GetSpecificDrug` returns `brochure[]`, but that array is dominated by `החמרה לעלון` entries, which
are leaflet AMENDMENT notices, not the leaflet. For one product `brochure[0]` is an amendment from
2017 while the actual consumer leaflet is from 2026. Filter on `type == "עלון לצרכן"`, pick the
newest, and choose the language the user is reading in (`lng` is `עברית` / `אנגלית` / `ערבית`).
The `url` is a bare filename, not a link: resolve it against
`https://mohpublic.health.gov.il/IsraelDrugs/<filename>`.

**Patient information leaflet (alon la-tzarchan):**
- Available in Hebrew for all registered drugs
- Published on MoH website and inside drug packaging
- Contains: Indications, contraindications, side effects, dosage

**Drug interactions: do not answer, route.**

Do not cross-reference active ingredients yourself. Deciding whether two medicines interact, and
whether it matters for this patient, is a clinical judgement that depends on dose, indication,
renal and hepatic function and everything else the person is taking. State the question back
clearly, name the products and their active ingredients so the user can repeat them accurately,
give them the consumer leaflets, and send them to a pharmacist, who can run a full interaction
check against their actual medication list.

**Pregnancy and breastfeeding: do not answer, route.**

This skill deliberately does NOT carry the A/B/C/D/X letter table. The FDA's Pregnancy and
Lactation Labeling Rule removed those categories: "The PLLR removes pregnancy letter categories --
A, B, C, D and X", with the labelling changes effective 30 June 2015 and phased in for older
approvals (OTC labelling was never in scope). Reproducing a retired five-row lookup table next to a
footnote saying it is legacy invites exactly the failure this skill exists to prevent: an agent
answering "category C" to "can I take this while pregnant".

The Ministry of Health's own drug-registry service page routes this question to a named national
service: `לגבי נטילת תרופות בזמן היריון, יש לפנות למרכז הארצי לייעוץ טרטולוגי`. Send the user to
the Israeli Teratology Information Service and to their physician. Give them the leaflet from
`brochure[]` if they want to read the labelling themselves.

**Recall and safety alerts:**
- MoH publishes drug safety alerts and recalls on `gov.il` (the Pharmaceutical Division)
- Adverse-event (side-effect) reports go to the MoH reporting form at **https://sideeffects.health.gov.il/**, with the service page at https://www.gov.il/he/service/adverse_effects_reports (`דיווח על תופעות לוואי ואירועים חריגים הקשורים בתרופות`). The relevant MoH unit is `המחלקה לניהול סיכונים ומידע תרופתי`. ("Yellow Card" is the UK MHRA scheme, not Israel's, do not use that term for Israel.)
- Recalls and drug warnings are collected at https://www.gov.il/he/departments/topics/drugs-recall/govil-landing-page (`אזהרות בנושא תרופות`), alongside marketing-discontinuation notices.

### Step 6: Prescription Status
Israeli prescription categories:
| Type | Hebrew | Meaning |
|------|--------|---------|
| GSL | תכשיר שניתן למכור שלא בבית מרקחת | Sellable outside a pharmacy. The registry exposes this as the `isGSL` filter on `SearchByAdv` |
| OTC | ללא מרשם | Available without prescription at a pharmacy. `prescription: false` on `SearchByName` |
| Prescription | מרשם | Requires a physician's prescription. `prescription: true` |
| Restricted | מרשם מוגבל | Specialist prescription or hospital-only |
| Dangerous drug | **סם מסוכן** | Controlled under `פקודת הסמים המסוכנים`, special prescription form |

The last row is `סם מסוכן`, the statutory term used in the Dangerous Drugs Ordinance. Earlier
versions of this skill said `sam mefakach`, which is not the term the Ministry uses.

Note that the per-drug restriction does not arrive in any field called `sug mircham`. What the API
actually returns is the boolean `prescription` on `SearchByName` and the prose `limitations` on
`GetSpecificDrug`.

## Examples

### Example 1: Drug Lookup
User says: "Tell me about Acamol"

Call `SearchByName` with `{"val":"acamol","prescription":false,"healthServices":false,"pageIndex":1,"orderBy":0}`. Answer from what came back, naming the registration number.

Result: "Acamol", registration number `020 16 20534 00`, is paracetamol 500 mg in tablet form,
marketing authorisation held by TEVA ISRAEL LTD. That registration is not prescription-only and is
flagged as in the health basket, at a regulated maximum consumer price of 14.12 NIS. Note that
"Acamol" covers several registrations and they differ: `ACAMOL TEVA CAPLETS` and `ACAMOL FOCUS` are
NOT flagged as in the basket. What you actually pay is your kupah's copay, not this price. For how
much to take, read the leaflet or ask your pharmacist. This skill does not give doses.

### Example 2: Generic Alternative
User says: "Is there a cheaper alternative to Lipitor?"

Look up Lipitor, take its `activeComponentsCompareName` (atorvastatin), search that, page through to
the `pages` count, drop `iscanceled` products, and compare the `customerPrice` values you actually
retrieved.

Result: an itemized list of the registered atorvastatin products at the same strength and dosage
form, each with its registration number, its holder, its regulated price, and its own basket flag,
plus the note that basket status differs between registrations so it must be read per product. No
percentage saving is quoted. Switching brand to generic is a decision for the prescriber and the
pharmacist.

### Example 3: Health Basket Check
User says: "Is Keytruda covered by kupat cholim?"

This is the case where a yes/no answer is actively harmful. Call `GetSpecificDrug` with
`154 38 34448 00` and read `salList`, `frameworkOfInclusion` and `limitations`.

Result: Keytruda (pembrolizumab, ATC L01FF02) is in the basket, but entitlement is defined per
indication and the registry lists 101 of them, each with its own conditions, and
`frameworkOfInclusion` adds line-of-therapy and duration limits (for example the adjuvant melanoma
entry caps treatment at one year and allows only one checkpoint inhibitor during the illness).
`limitations` records that it may be prescribed only by a specialist. So the honest answer is: it
depends entirely on your specific diagnosis and treatment line, which only your oncologist can
match against that list. If your indication is not on it, the route is the kupah's **exceptions
committee** (`ועדת חריגים לתרופות מחוץ לסל הבריאות`) or a request to add the drug to the basket,
and there is an appeal to the National Health Insurance public complaints commissioner. Note that
supplementary insurance (shaban) and compassionate use are different things from each other and
from the exceptions route, and a kupah is not obliged to supply an off-basket drug.

## Bundled Resources

### Scripts
- `scripts/lookup_drug.py` - Queries the LIVE registry. Subcommands: `search` (by name), `drug` (by registration number, including the basket indication list), `generics` (by ingredient, paging to completion), `prescription-types` (the five statutory categories). It refuses to print doses, and it distinguishes the HTML error page and the 502 maintenance page from a real JSON answer. Earlier versions shipped a frozen table of brands with hardcoded dose, prescription and basket values; that table was removed because it was verifiably wrong (it claimed Glucophage was in the basket when all three registrations return `health: false`) and because basket and prescription status are per registration number and cannot be represented per brand. Run: `python scripts/lookup_drug.py --help`

### References
- `references/drug-registry-guide.md` - Registry field definitions split per endpoint, the endpoint list with payloads, the five Israeli prescription categories (GSL, OTC, prescription, restricted, `סם מסוכן`), the real banded copay structure with the quarterly ceilings, the per-indication basket mechanics, the off-basket routes, and generic-switching guidance. Consult when interpreting registry fields or explaining coverage to users.

## Recommended MCP Servers

| MCP Server | What it adds | Link |
|------------|--------------|------|
| israel-drugs | Semantic wrappers over the MoH registry (`discover_drug_by_name`, `get_comprehensive_drug_info`, `explore_generic_alternatives`, `find_drugs_for_symptom` and others). They are not one-to-one with the endpoints in Step 2 | https://agentskills.co.il/he/mcp/israel-drugs |

**Pairing rule.** That MCP advertises dosage and administration information among its features. This
skill's refusal rules still apply when it is present: having a tool that will return a dose is not
permission to state one. Use it to retrieve registry data, and route dosing, interaction and
pregnancy questions to a pharmacist or physician exactly as Step 5 requires.

## Gotchas
- Israeli drug registration uses local brand names that differ from international names. The same active ingredient may have different trade names in Israel vs. the US or Europe. Agents may use international brand names that Israeli pharmacies will not recognize.
- The Israeli drug formulary (sal habri'ut) determines which medications are subsidized. Agents may recommend a medication without checking if it is in the sal, leading to unexpected out-of-pocket costs.
- Drug prices in Israel are regulated by the Ministry of Health. The maximum retail price (mechir mufchach) is fixed and different from US or European prices. Agents should not use international drug pricing.
- Israeli prescriptions use the metric system exclusively. Agents may convert dosages from imperial measurements or use non-standard abbreviations.
- **A 200-response from this API can be a failure.** A fabricated endpoint path returns HTTP 200 with an HTML error page, and a real endpoint under load returns HTTP 502 with a maintenance page. Only a body that parses as JSON is a real answer.
- **Basket and prescription status vary between registrations of the same brand name.** Answering for "Losec" or "Acamol" rather than for a registration number will be wrong for some of them.
- **Ten results is a page, not an answer.** Loop `pageIndex` to the `pages` count before claiming a list is complete.
- **`health: true` on an expensive drug is not a coverage answer.** Read `salList`; entitlement is per indication.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israeli drug index (service page) | https://www.gov.il/he/service/israeli-drug-index | Primary gov.il entry point for the national drug registry |
| Drug registry search UI | https://israeldrugs.health.gov.il/ | Live search by trade name, active ingredient, or registration number |
| Ministry of Health - Pharma | https://www.gov.il/he/departments/units/pharmaceuticals/govil-landing-page | Pharmaceuticals Division landing page, registry entry points |
| Health basket drugs (Kol Zchut) | https://www.kolzchut.org.il/he/תרופות_בסל_הבריאות | That the list is closed and annual, that the binding instrument is the order, and that kupot copay rules differ |
| Chronic-patient payment ceiling (Kol Zchut) | https://www.kolzchut.org.il/he/תקרת_תשלום_ברכישת_תרופות_לחולים_כרוניים | Current quarterly ceilings per kupah, above which basket drugs are free |
| Off-basket routes (Kol Zchut) | https://www.kolzchut.org.il/he/סל_הבריאות | Exceptions committee, request to add a drug to the basket, and the appeal route |
| Adverse-event reporting (MoH) | https://sideeffects.health.gov.il/ | The Israeli side-effect reporting form. NOT the UK Yellow Card |
| Drug warnings and recalls (MoH) | https://www.gov.il/he/departments/topics/drugs-recall/govil-landing-page | Safety alerts, recalls, marketing-discontinuation notices |
| Drug registry API (IDRServer) | https://israeldrugs.health.gov.il/GovServiceList/IDRServer/SearchByName | The live JSON API. POST only. Real endpoints: SearchByName, GetSpecificDrug, SearchByBarcode, SearchGeneric, SearchByAdv, GetAtcList, GetMatanList, GetPackageList |
| ATC / WHO drug classification | https://www.whocc.no/atc_ddd_index/ | International ATC codes for cross-referencing active ingredients |

## Troubleshooting

### Error: "Drug not found in registry"
Cause: Drug may be registered under different name, or not registered in Israel
Solution: Try searching by active ingredient instead of brand name. Some international brands are marketed under different names in Israel. Check if the drug is registered at all -- not all drugs approved abroad are registered in Israel.

### Error: "Health basket status unclear"
Cause: Almost always because `health` was read as a yes/no when the entitlement is per indication.
Solution: Call `GetSpecificDrug` and read `salList`, `frameworkOfInclusion` and `limitations`. Report how many indications are listed and that the user's own diagnosis decides it. For an indication not on the list, the route is the kupah's exceptions committee, not supplementary insurance.

### Error: "The API returned 200 but I cannot parse it"
Cause: Either the endpoint name or a parameter name is wrong, or the service is in maintenance.
Solution: Check the name against the endpoint table in Step 2, and check the payload keys (`SearchByName` takes `prescription` and `healthServices`, not `prefix`). A fabricated path and a wrong parameter both return the same HTML error page under a 200. A 502 with a maintenance image is the service being down; retry later rather than changing your call.

### Error: "Price information unavailable" or the price is 0
Cause: `customerPrice` of `"0"` means the product is not on the retail price list, typically because it is hospital-administered. It does not mean free.
Solution: Query `SearchByName` for `customerPrice` / `packagesPrices[]` or `GetSpecificDrug` for `maxPrice`. If it is `0`, say the drug is not sold at retail and that cost is handled through the kupah. Never present a regulated price as the amount the user will pay: that is the copay, which the registry does not hold.