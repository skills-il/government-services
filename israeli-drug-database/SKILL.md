---
name: israeli-drug-database
description: Query the Israeli pharmaceutical database for drug information, health basket coverage, generic alternatives, and pricing. Use when user asks about Israeli medications, "trufot", drug names, "sal briut" drug coverage, generic drugs, drug prices in Israel, prescription requirements, or medication safety info. Enhances the israel-drugs MCP server with health basket context and patient-facing guidance. Do NOT use for medical advice, dosage recommendations, or diagnosis. Do NOT use for non-Israeli drug registries.
license: MIT
allowed-tools: Bash(python:*) Bash(curl:*) WebFetch
compatibility: >-
  Searching the registry is a POST, which WebFetch cannot issue, so a shell (curl or the bundled
  script) is needed to search by name or ingredient. The per-drug detail endpoints are plain GETs,
  so an agent with only WebFetch can still read a record when it already has the registration
  number. Without either, the skill still explains the basket mechanism, the copay structure and
  the prescription categories, but it must then say it could not query the registry rather than
  answering from memory.
---

# Israeli Drug Database

## Critical Note
This skill provides DRUG INFORMATION ONLY, not medical advice.

**Hard refusal rules. These are not style guidance.**

- **Never state a dose, a maximum daily dose, or a dosing schedule**, even one you read in a
  leaflet. Return the consumer leaflet itself (from `GetMedicineDocuments`) and send the user to a
  pharmacist.
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
| Health basket status | Check sal briut coverage and the per-indication list |
| Generic alternatives | List registered products with the same active ingredient, for the pharmacist |
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
| Prescription type | mirsham | Per PACK, not per registration: `packages[].mirsham` is `1` (prescription) or `0` (no prescription). Further restriction arrives as prose in `limitations` |

**The registry has moved (confirmed 2026-10-28).** The old site `israeldrugs.health.gov.il` now only redirects
to `https://registries.health.gov.il/Medicines`, and its old POST API under
`/GovServiceList/IDRServer/` (`SearchByName`, `GetSpecificDrug` and the rest) answers **403** from
CloudFront. Any instructions, scripts or MCP servers that still call those endpoint names are
broken. The current backend is `https://registries.health.gov.il/api/Medicines/`. The endpoint
names and payloads below were read from the new registry app's own network calls and each was
called live on 2026-10-28.

| Endpoint | Method | Input |
|----------|--------|-------|
| `GetMedicines` | POST | `{searchText, pageNumber, maxResult, sortBy, sortDirection, includeActive, includeCanceled}` plus optional filters `otcOnly`, `basketOnly`, `telemOnly`, `componentCodes`, `barkod`, `humanVet`. Several codes in one `componentCodes` list are ANDed (products containing all of them) |
| `GetMedicineByRegNumber` | GET | `?regNumber=020%2016%2020534%2000` (spaces URL-encoded) |
| `GetMedicineBasketIndications` | GET | `?medicineId=<id>` |
| `GetMedicineDocuments` | GET | `?medicineId=<id>`, the leaflets |
| `GetMedicinePackages` | GET | `?medicineId=<id>`, packs and prices |
| `GetMedicineAtc` | GET | `?medicineId=<id>` |
| `GetMedicineImages` | GET | `?medicineId=<id>` |
| `GetComponents` | GET | the active-ingredient lookup list, `[{key, value}]` |

`medicineId` is a number returned by `GetMedicines` and `GetMedicineByRegNumber`. It is not the
registration number.

**Every answer is wrapped:** `{"returnObject": ..., "statusCode": 200, "message": "Success"}`. Assert
on the inner `statusCode`, not on HTTP: an unknown registration number, a misspelt endpoint, a wrong
method and a missing parameter all answer **HTTP 200** (the exact shapes are in
`references/drug-registry-guide.md`). The retired `israeldrugs.health.gov.il` API is the one that
answers 403.

**One record schema across endpoints.** `GetMedicines` returns `returnObject.medicinesList[]` plus
`totalRows`; `GetMedicineByRegNumber` returns one record of the same shape. The full field list is
in `references/drug-registry-guide.md`. The ones that matter most: `regNumber`, `medicineId` (for
the GET endpoints), `components[]`, `basket` (the string `כן` / `לא`), `limitations`, `framework`,
and per pack `packages[].mirsham` and `packages[].customerPriceWithTax`.

**Prescription status is per pack.** Read `packages[].mirsham` on every package: `1` means a
prescription is required for that pack, `0` means it is not. The registry's own site renders `1` as
`חייב במרשם רופא`. One registration can mix both: `SINUFED TABLETS` (`030 06 25464 00`) sells its
10-tablet pack without a prescription and its larger packs on prescription only. So report status
per pack size, and say "some packs need a prescription" for a mixed registration rather than
picking one answer.

**Do not use the `otcOnly` filter to label a registration prescription-only.** It returns only
registrations whose packs are all `mirsham: 0`, so a mixed registration like SINUFED TABLETS is
absent from it and would be wrongly called prescription-only. Where packs are uniform the two
agree: Keytruda (`154 38 34448 00`) is `mirsham: 1` on its pack and absent from the OTC set.

**Results are paginated.** `pageNumber` is zero-based and `maxResult` sets the page size (the site
uses 10). `totalRows` is the full count. `acamol` returns 13 active registrations, so a single
10-row page silently drops three. Page until you have `totalRows` rows before making any
completeness claim.

**A price of `0` means "no price listed", nothing more.** `customerPriceWithTax` is `0` for most
prescription packs, including every Lipitor and Nexium tablet pack, which are dispensed in
community pharmacies every day. It does not mean free, and it does not mean the product is not
sold at retail. Where a price is listed it is the consumer price the registry carries for that
pack, which is not the user's copay.

Treat this as an undocumented public backend: cache results and do not bulk-scrape.

### Step 3: Health Basket Coverage

**Being "in the basket" is not a yes/no answer for most expensive drugs. It is per indication.**
This is the single most consequential thing to get right here. The registry returns far more than
the `basket` flag:

- `GetMedicineBasketIndications` -- one entry per basket-covered indication, each with
  `indication`, `includeDate`, `clinicDesc` and `sicknessState`. **Keytruda has 87 entries**
  (2026-10-28).
- `framework` -- the conditions of entitlement in prose, including line-of-therapy and duration
  limits.
- `limitations` -- who may prescribe. Acamol: `תרופה שאושרה לשימוש כללי בקופ'ח`. Keytruda:
  `תרופה מוגבלת לרישום ע'י רופא מומחה או הגבלה אחרת`.
- `dateOfInclusion`.

So: **an empty indication list plus a general-use `limitations` means unrestricted. A populated
list means entitlement exists ONLY for the listed indications.** Answering "yes, it is in the
basket" from `basket: כן` alone will tell a patient whose indication is not on that list that they
are covered when they are not. Read the list, say how many indications it holds, and tell the user
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

**Price is not copay.** `customerPriceWithTax` is the consumer price the registry lists for a
pack, where it lists one. A basket-covered drug supplied through the kupah is priced by the kupah's
copay schedule instead. **Basket terms apply only to supply through the kupah.** Many OTC
registrations are flagged `basket: כן` (Acamol, Optalgin), but a purchase at the counter is at the
pharmacy's price; do not let a user infer that the basket flag makes their counter purchase
subsidised. The registry's own tooltip on the basket filter adds
that the kupah is not obliged to supply the drug under that trade name and may substitute another
with the same active ingredients.

**Freshness.** The basket list is closed and updated annually. The legally binding instrument is
`צו ביטוח בריאות ממלכתי (תרופות בסל שירותי הבריאות), תשנ"ה-1995`, not a web page: Kol Zchut states
`רשימת התרופות הנכללות בסל היא רשימה סגורה שמתעדכנת כל שנה`. Do not promise that the update lands
in January; the effective date of a given year's expansion is set by the director-general circular
for that year. Confirm against the current order.

### Step 4: Generic Alternatives
To find generic alternatives:
1. Identify the active ingredient (chomer peeil) of the brand-name drug from
   `components[].componentDesc` (Acamol returns `PARACETAMOL`).
2. Look the ingredient up in `GetComponents` (PARACETAMOL is key `3172`) and call `GetMedicines`
   with `"componentCodes": [<key>]`. That matches on the ingredient code, where a free-text
   `searchText` also matches names. **Page to `totalRows`**, or your list is silently truncated.
3. **The same substance can have more than one ingredient entry.** DIPYRONE (`2764`) and METAMIZOLE
   SODIUM (`1679`) are separate keys, and searching only the first misses DIPYRONE KALCEKS. Query
   each synonym or salt as its own call and merge: putting both codes in one `componentCodes` list
   returns 0, because the codes are ANDed.
4. The component filter also returns combination products and **veterinary products** (14 of the 39
   amoxicillin hits on 2026-10-28). Keep records with exactly one entry in `components` and
   `veterinaryUse` of `לא`.
5. **Present the result as a list of registered products with the same ingredient, not as a list
   of substitutes.** Show each product's route, form and strength as the registry gives them, keep
   different ingredients in separate lists (esomeprazole is not pantoprazole), and leave the
   substitution decision to the pharmacist. Three traps:
   - **Release type is not recorded reliably.** Proton-pump inhibitors are gastro-resistant, yet
     NEXIUM and LOSEC carry no marker while ESOMEPRAZOLE INOVAMED says `GASTRO RESISTANT TABLETS`.
     So never call a product "immediate release" because no marker is shown, and do not yourself
     offer a product that DOES carry a marker (`SLOW RELEASE`, `PROLONGED RELEASE`, `GASTRO RESISTANT`, or
     `CR` / `XR` / `SR` / `OD` / `RETARD` as a whole word in the name) in place of another; whether it
     can substitute is the pharmacist's decision. TEGRETOL
     CR is not TEGRETOL; PENTASA and RAFASSAL, or TRAMADEX OD and TRAMAL RETARD, differ in mechanism
     or dosing interval. Match whole words: not CRESTOR, and GASTRO is a famotidine brand.
   - **A liquid's strength can read like a tablet's:** TRAMARAZ drops list `100 MG` (it is per ml).
   - **Form spelling alone is not a difference:** LIPITOR is `FILM COATED TABLETS`, TORVA is
     `COATED TABLETS` and LITORVA is `TABLETS`, all atorvastatin by mouth.
6. **Compare the actual `customerPriceWithTax` values you retrieved, pack size against pack size.**
   Prices are often not listed for prescription packs (every atorvastatin pack, for example); then
   say so and send the user to the pharmacist for the price. Do not quote a percentage saving: the
   single-ingredient paracetamol packs retrieved on 2026-10-28 were listed from 5.03 to 40.24 NIS
   across strengths and pack sizes.

**Basket and prescription status are per registration number, not per brand.** Verified live on
2026-10-28: `LOSEC 20 MG` is `mirsham: 0` and `basket: לא` while `LOSEC 20 MG RX` is `mirsham: 1`
and `basket: כן`. `ACAMOL` (`020 16 20534 00`) is `basket: כן` but `ACAMOL TEVA CAPLETS` and
`ACAMOL FOCUS` are `basket: לא`. All three GLUCOPHAGE XR strengths are `basket: לא`. Never answer
for a brand; answer for a `regNumber` and say which one.

**Common Israeli generics.** All six brands below were confirmed registered and not cancelled on
2026-10-28, with the ingredients shown. Use this to recognise a name, never to answer basket,
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
service rather than repeating a contraindication yourself. Note also that `OPTALGIN TEVA`
(`160 24 34798 00`) is prescription-only, but it is a solution for injection; the oral Optalgin
registrations are not prescription-only.

### Step 5: Drug Safety Information
Provide safety context (NOT medical advice):

**The leaflet is the thing you hand over instead of an answer, so get the right one.**
`GetMedicineDocuments` returns physician leaflets, consumer leaflets and leaflet AMENDMENT notices
(`החמרה לעלון`, `החמרה לעלון לצרכן`). Three rules:

- **The consumer leaflet is `type == "עלון לצרכן"`.** Take the language from `language`
  (`עברית` / `אנגלית` / `ערבית` / `רוסית`), falling back to `langDesc`. Both are sometimes empty
  (both current Keytruda leaflets): then open the file before telling the user its language.
- **Skip archived uploads** (`fName` starting `Arc`, for example a 2015 leaflet still attached to
  NUROFEN TABLETS 200 MG).
- **Lead with the newest leaflet in each language, but do not discard the older ones.** An older
  leaflet may be superseded, or may be the leaflet for a different pack or sales channel: ACAMOL
  TEVA CAPLETS `176 61 37219 99` has a general-sale Hebrew leaflet from 2025-12-17 and a pharmacy
  Hebrew leaflet from 2025-11-24, and both are in force. List older leaflets separately, say they may
  be superseded or for another pack, and have the user check the product name and channel against
  their pack, or ask the pharmacist. A leaflet with no language is compared against the newest
  leaflet of any language.
- **There can be more than one current leaflet in the same language.** ACAMOL `128 74 25337 08`
  has two Hebrew consumer leaflets dated 2025-05-12, which can differ by pack or sales channel. List
  both and have the user match the leaflet to the pack in their hand; never silently pick one.
- **An amendment notice dated after a language's current leaflet must be handed over too.** For
  ACAMOL `020 16 20534 00` a `החמרה לעלון` dated 2025-09-11 postdates the Hebrew consumer leaflet
  (2025-05-12), so the leaflet may not yet contain that safety change. Give both, and say so.
  Compare per language and by calendar day: a notice uploaded the same day as its leaflet is part of
  that upload, not a later change.
  Physician-leaflet amendments (`החמרה לעלון לרופא`) are not for this.

`fName` is a bare filename, not a link: resolve it against
`https://pharmaceuticalreg.health.gov.il/api/pharmaregistration/IsraelDrugs/<fName>`, which is the
host the new registry site itself uses. Some registrations publish no consumer leaflet at all; then
say so and send the user to the pharmacist.

**Patient information leaflet (alon la-tzarchan):**
- Published in the registry and inside the drug packaging, but not every registration has one
  online
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
the Israeli Teratology Information Service and to their physician. Give them the consumer leaflet
if they want to read the labelling themselves.

**Recall and safety alerts:**
- MoH publishes drug safety alerts and recalls on `gov.il` (the Pharmaceutical Division)
- Adverse-event (side-effect) reports go to the MoH reporting form at **https://sideeffects.health.gov.il/**, with the service page at https://www.gov.il/he/service/adverse_effects_reports (`דיווח על תופעות לוואי ואירועים חריגים הקשורים בתרופות`). The relevant MoH unit is `המחלקה לניהול סיכונים ומידע תרופתי`. ("Yellow Card" is the UK MHRA scheme, not Israel's, do not use that term for Israel.)
- Drug recalls are collected at https://www.gov.il/he/departments/topics/drugs-recall/govil-landing-page (the gov.il recall topic page for medicines), alongside marketing-discontinuation notices.

### Step 6: Prescription Status
Israeli prescription categories:
| Type | Hebrew | Meaning |
|------|--------|---------|
| GSL | תרופות לשיווק כללי | Sellable outside a pharmacy. The registry's `telemOnly` filter, labelled `תרופות לשיווק כללי (GSL)`, selects them. GSL can be a property of one pack or channel, so absence from that filter does not prove a product is never on general sale |
| OTC | ללא מרשם | Available without prescription at a pharmacy. `mirsham: 0` on the pack |
| Prescription | מרשם | Requires a physician's prescription. `mirsham: 1` on the pack |
| Restricted | מרשם מוגבל | Specialist prescription or hospital-only. Surfaces in `limitations` |
| Dangerous drug | **סם מסוכן** | Controlled under `פקודת הסמים המסוכנים`, special prescription form |

The last row is `סם מסוכן`, the statutory term used in the Dangerous Drugs Ordinance. Earlier
versions of this skill said `sam mefakach`, which is not the term the Ministry uses.

The registry's field is `mirsham`, per pack; there is no `sug mircham` field. Specialist or hospital
restriction arrives as prose in `limitations`.

## Examples

### Example 1: Drug Lookup
User says: "Tell me about Acamol"

POST to `https://registries.health.gov.il/api/Medicines/GetMedicines` with
`{"searchText":"acamol","pageNumber":0,"maxResult":100,"sortBy":"tradeNameHeb","sortDirection":"asc","includeActive":true,"includeCanceled":false}`,
and read `packages[].mirsham` for each pack. Answer from what came back, naming the registration
number.

Result: "Acamol", registration number `020 16 20534 00`, is paracetamol 500 mg in tablet form,
marketing authorisation held by TEVA ISRAEL LTD. Its packs need no prescription, and the 20-tablet
pack is listed at 14.12 NIS. The registration is flagged as in the health basket, which matters
only when it is supplied through your kupah; at the counter you pay the pharmacy's price. Note that
"Acamol" covers 13 active registrations and they differ: `ACAMOL TEVA CAPLETS` and `ACAMOL FOCUS`
are NOT in the basket, and `COD-ACAMOL 15/325` is prescription-only (codeine status is per
registration: `COD ACAMOL 10/500` is not). For how much to take, read the leaflet or ask
your pharmacist. This skill does not give doses.

### Example 2: Generic Alternative
User says: "Is there a cheaper alternative to Lipitor?"

Look up Lipitor, take its ingredient (ATORVASTATIN), find its key in `GetComponents`, call
`GetMedicines` with `componentCodes`, page to `totalRows`, keep human single-ingredient products, and
list them with route, form and strength.

Result: the registered oral atorvastatin products at each strength (at 20 mg: LIPITOR, TORVA,
LITORVA and ATORVA-DEX, whose form names differ only in spelling), each with its registration
number, its holder and its own basket flag, presented as the list to take to the pharmacist, plus the note that
basket status differs between registrations so it must be read per product. The registry lists no
consumer price for these prescription packs, so say that plainly and send the user to their
pharmacist or kupah for the actual cost, rather than implying the products are unavailable. No
percentage saving is quoted. Switching brand to generic is a decision for the prescriber and the
pharmacist.

### Example 3: Health Basket Check
User says: "Is Keytruda covered by kupat cholim?"

This is the case where a yes/no answer is actively harmful. Call `GetMedicineByRegNumber` with
`154 38 34448 00`, then `GetMedicineBasketIndications` with its `medicineId`, and read the list,
`framework` and `limitations`.

Result: Keytruda (pembrolizumab, ATC L01FF02) is in the basket, but entitlement is defined per
indication and the registry lists 87 of them, each with its own conditions, and `framework` adds
line-of-therapy and duration limits (for example the adjuvant melanoma entry caps treatment at one
year and allows only one checkpoint inhibitor during the illness). `limitations` records that it
may be prescribed only by a specialist. So the honest answer is: it depends entirely on your
specific diagnosis and treatment line, which only your oncologist can match against that list. If
your indication is not on it, the route is the kupah's **exceptions committee**
(`ועדת חריגים לתרופות מחוץ לסל הבריאות`) or a request to add the drug to the basket, and there is an
appeal to the National Health Insurance public complaints commissioner. Note that supplementary
insurance (shaban) and compassionate use are different things from each other and from the
exceptions route, and a kupah is not obliged to supply an off-basket drug.

## Bundled Resources

### Scripts
- `scripts/lookup_drug.py` - Queries the LIVE registry at `registries.health.gov.il`. Subcommands: `search` (by name, with OTC / Rx / mixed read from each pack's `mirsham`), `drug` (by registration number: per-pack prescription status and price, the basket indication list, the newest consumer leaflets per language plus the older ones labelled as such, and any later amendment notice), `generics` (by one or more ingredient names, one query per code, one section per ingredient, human single-ingredient products with route, form, strength and any release marker the registry states; a list for the pharmacist, not a list of substitutes), `prescription-types` (the five statutory categories). It refuses to print doses, and it treats a non-JSON body or an inner `statusCode` other than 200 as a failure rather than an answer. Versions before 1.4.0 called the retired `israeldrugs.health.gov.il` API and no longer work. Run: `python scripts/lookup_drug.py --help`

### References
- `references/drug-registry-guide.md` - The current endpoints with methods and inputs, the record fields, per-pack prescription status, the five Israeli prescription categories (GSL, OTC, prescription, restricted, `סם מסוכן`), the real banded copay structure with the quarterly ceilings, the per-indication basket mechanics, the off-basket routes, and generic-switching guidance. Consult when interpreting registry fields or explaining coverage to users.

## Recommended MCP Servers

| MCP Server | What it adds | Link |
|------------|--------------|------|
| israel-drugs | Semantic wrappers over the MoH registry (`discover_drug_by_name`, `get_comprehensive_drug_info`, `explore_generic_alternatives`, `find_drugs_for_symptom` and others) | https://agentskills.co.il/he/mcp/israel-drugs |

**As of 2026-10-28 this MCP is broken.** Its default API base is still the retired
`https://israeldrugs.health.gov.il/GovServiceList/IDRServer`, which now answers 403, so its tools
fail until its maintainer moves it to the new registry. Use the bundled script or the endpoints in
Step 2 instead, and if an MCP tool errors, say the registry could not be queried through it rather
than answering from memory.

**Pairing rule.** That MCP advertises dosage and administration information among its features. This
skill's refusal rules still apply when it is present: having a tool that will return a dose is not
permission to state one. Use it to retrieve registry data, and route dosing, interaction and
pregnancy questions to a pharmacist or physician exactly as Step 5 requires. Never use it, or the
registry, to suggest which medicine to take for the user's own symptoms: that is a choice of
treatment for a physician or pharmacist.

## Gotchas
- Israeli drug registration uses local brand names that differ from international names. The same active ingredient may have different trade names in Israel vs. the US or Europe. Agents may use international brand names that Israeli pharmacies will not recognize.
- The Israeli drug formulary (sal habri'ut) determines which medications are subsidized. Agents may recommend a medication without checking if it is in the sal, leading to unexpected out-of-pocket costs.
- Drug prices in Israel are regulated by the Ministry of Health. The maximum retail price (mechir mufchach) is fixed and different from US or European prices. Agents should not use international drug pricing.
- Israeli prescriptions use the metric system exclusively. Agents may convert dosages from imperial measurements or use non-standard abbreviations.
- **Old endpoint names are dead, not slow.** `SearchByName`, `GetSpecificDrug` and the rest of `/GovServiceList/IDRServer/` answer 403 (confirmed 2026-10-28). Retrying them will not help; switch to `registries.health.gov.il/api/Medicines/`.
- **HTTP 200 is not success.** A missing registration comes back as HTTP 200 with an inner `statusCode: 404`, and a misspelt endpoint as HTTP 200 with an HTML error page. Read the inner code.
- **Basket and prescription status vary between registrations of the same brand name, and prescription status varies between packs of one registration.** Answer for a registration number and, for prescription status, for a pack size.
- **Do not call a registration prescription-only because it is missing from the `otcOnly` filter.** Mixed-pack registrations are missing from it too. Read `mirsham`.
- **One page is a page, not an answer.** Page to `totalRows` before claiming a list is complete.
- **`basket: כן` on an expensive drug is not a coverage answer.** Read the indication list; entitlement is per indication.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israeli drug index (service page) | https://www.gov.il/he/service/israeli-drug-index | Primary gov.il entry point for the national drug registry |
| Drug registry search UI | https://registries.health.gov.il/Medicines | Live search by trade name, active ingredient, or registration number (replaces israeldrugs.health.gov.il) |
| Ministry of Health - Pharma | https://www.gov.il/he/departments/units/pharmaceuticals/govil-landing-page | Pharmaceuticals Division landing page, registry entry points |
| Health basket drugs (Kol Zchut) | https://www.kolzchut.org.il/he/תרופות_בסל_הבריאות | That the list is closed and annual, that the binding instrument is the order, and that kupot copay rules differ |
| Chronic-patient payment ceiling (Kol Zchut) | https://www.kolzchut.org.il/he/תקרת_תשלום_ברכישת_תרופות_לחולים_כרוניים | Current quarterly ceilings per kupah, above which basket drugs are free |
| Off-basket routes (Kol Zchut) | https://www.kolzchut.org.il/he/סל_הבריאות | Exceptions committee, request to add a drug to the basket, and the appeal route |
| Adverse-event reporting (MoH) | https://sideeffects.health.gov.il/ | The Israeli side-effect reporting form. NOT the UK Yellow Card |
| Drug warnings and recalls (MoH) | https://www.gov.il/he/departments/topics/drugs-recall/govil-landing-page | Safety alerts, recalls, marketing-discontinuation notices |
| Drug registry API | https://registries.health.gov.il/api/Medicines/GetComponents | The live JSON API (this GET returns the ingredient list). Endpoints: GetMedicines (POST), GetMedicineByRegNumber, GetMedicineBasketIndications, GetMedicineDocuments, GetMedicinePackages, GetMedicineAtc, GetComponents |
| ATC / WHO drug classification | https://www.whocc.no/atc_ddd_index/ | International ATC codes for cross-referencing active ingredients |

## Troubleshooting

### Error: "Drug not found in registry"
Cause: Drug may be registered under different name, or not registered in Israel
Solution: Try searching by active ingredient instead of brand name. Some international brands are marketed under different names in Israel. Check if the drug is registered at all -- not all drugs approved abroad are registered in Israel. For a registration-number lookup, an inner `statusCode: 404` with `לא נמצאה תרופה` means that exact number is not registered: check the spacing (`020 16 20534 00`) before concluding anything.

### Error: "Health basket status unclear"
Cause: Almost always because `basket` was read as a yes/no when the entitlement is per indication.
Solution: Call `GetMedicineBasketIndications` and read the list, plus `framework` and `limitations` on the record. Report how many indications are listed and that the user's own diagnosis decides it. For an indication not on the list, the route is the kupah's exceptions committee, not supplementary insurance.

### Error: "403" or an HTML page instead of JSON
Cause: Verified 2026-10-28. A 403 ("The distribution supports only cachable requests") means the call went to the retired `israeldrugs.health.gov.il/GovServiceList/IDRServer/` API. An HTML page titled `Error` under HTTP 200 means the new host received a misspelt endpoint name or the wrong method (for example a GET to `GetMedicines`, which only accepts POST).
Solution: Use `https://registries.health.gov.il/api/Medicines/` with the names and methods in the Step 2 table. Do not tell the user the registry is down on the strength of a 403 from the old host: it is retired, not down.

### Error: "Price information unavailable" or the price is 0
Cause: `customerPriceWithTax` of `0` means the registry lists no price for that pack. Verified 2026-10-28 that this is the normal case for prescription packs (every Lipitor and Nexium tablet pack), so it is not evidence that the drug is hospital-only, unavailable or free.
Solution: Read `packages[]` from `GetMedicines` or `GetMedicinePackages`. If no pack has a price, say the registry does not list one and send the user to the pharmacist or their kupah for the cost. Never present a listed price as the amount the user will pay: that is the copay, which the registry does not hold.
