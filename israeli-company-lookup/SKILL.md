---
name: israeli-company-lookup
description: Look up Israeli company information and understand business entity types. Use when user asks about Israeli companies, "chevra", business registration, "Rasham HaChevarot", company numbers, entity types, or needs to register a business in Israel. Covers Ltd companies, partnerships, non-profits (amuta), cooperatives, and sole proprietors. Do NOT use for non-Israeli corporate registries or stock market analysis.
license: MIT
allowed-tools: WebFetch
compatibility: Network access helpful for registrar lookups.
---

# Israeli Company Lookup

## Legal notice

This is a free information tool operated by an AI model. It retrieves records from public registers, explains what their fields mean and compares entity types in general terms, with no involvement, review or approval by a lawyer. The output is not a legal opinion and not legal due diligence. It is a presentation of information published in the register: it does not examine contracts, obligations, legal proceedings or a corporation's ability to pay, and the open register may not reflect the current position. An AI model can err, omit data or present a wrong conclusion. Any wording the tool drafts is an automatic draft for personal organization only. It is not a document prepared by a lawyer and must not be relied on as evidence. The tool is not a substitute for advice that takes into account each person's particular circumstances and needs. Before taking a proceeding, signing a document or filing with an authority or a court, consult a lawyer. Any use of the output is at the user's sole responsibility.

## Instructions

### Step 1: Identify the Need
| Request | Approach |
|---------|----------|
| Look up existing company | Search by name/number at Rasham |
| Choose entity type | Describe types by liability and registration |
| Register new business | Step-by-step guide per entity type |
| Check a counterparty | Report the register fields verbatim (Step 2b) |

### Step 2: Company Search
Search the Israel Corporations Authority (rashut hatagidim):
- URL: `https://ica.justice.gov.il/GenericCorporarionInfo/SearchCorporation?unit=8`
- Search by: Company name (Hebrew or English) or company number
- Free basic info: company number, name, type, limited/unlimited, legal status, registered address, purpose, annual-fee debts, and whether the company has been declared "in breach of law" (mufrat hok)
- Paid full extract (nesach chevra): submit at `https://ica.justice.gov.il/Request/OpenRequest?rt=CompanyExtract`. The fee is stated on the request form itself (it changes annually, so we do not reproduce it here)
- For amutot (NPOs), use GuideStar: `https://www.guidestar.org.il` (consolidated Ministry of Justice portal). A CHL"Tz is a company, so search for it as a company
- For partnerships (shutfut), use `https://ica.justice.gov.il/Request/OpenRequest?rt=PartnershipExtract`
- Report the status, sub-status and breach flag as the registrar shows them. See Step 2b.

### Step 2b: Programmatic Lookup (the route an agent can actually execute)
The ICA search page in Step 2 is a human web form. For an agent, use the Ministry of Justice's
open registrar dump on data.gov.il instead. It is free, needs no key, and covers every registered
company, not only the one you can type into a form.

- Dataset metadata: `https://data.gov.il/api/3/action/package_show?id=ica_companies`
- Companies resource id: `f004176c-b85f-4542-8901-7b3176f9a054`
- Free-text search:
  `https://data.gov.il/api/3/action/datastore_search?resource_id=f004176c-b85f-4542-8901-7b3176f9a054&q=MONDAY.COM&limit=5`
- Exact lookup by company number (URL-encode the Hebrew field name):
  `https://data.gov.il/api/3/action/datastore_search?resource_id=f004176c-b85f-4542-8901-7b3176f9a054&filters={"מספר חברה":514744887}`

Fields worth reading on each record: `מספר חברה` (company number), `שם חברה` (Hebrew name),
`שם באנגלית` (English name, often populated), `סוג תאגיד` (private / public / foreign),
`סטטוס חברה` (status), `תת סטטוס` (sub-status), `מפרה` (breach flag), `שנה אחרונה של דוח שנתי (שהוגש)` (last filed annual
report year -- a stale year is a red flag even before the company is formally flagged), and the
registered-address fields.

**Report `סטטוס חברה`, `תת סטטוס` and `מפרה` verbatim, as three separate fields.** "Active" (`פעילה`) alone is not a clean result: the same record can carry a breach flag, or a sub-status such as a strike-off or liquidation process. If you cannot interpret a value, say so and tell the user to check it at the registrar. Never conclude that a company is safe, clean or able to pay.

Confirm you are reading real data, not an error page: a successful response is JSON with
`"success": true` and a non-empty `records` array. A wrong or non-existent `resource_id` on this
host returns an S3 `AccessDenied` XML body with HTTP 403, and the human-facing
`data.gov.il/dataset/...` pages are bot-protected, so never judge this API by an HTTP status
alone. Read the body.

Two limits to tell the user: this resource is the COMPANIES register only, so partnerships,
amutot and cooperatives are not in it and need their own registry. And the dump is a periodic snapshot, not the live register, so for any
legally operative decision (signing, lending, litigating) confirm the status on the official ICA
search or a paid extract rather than relying on the dataset alone.

### Step 3: Entity Type Comparison
| Factor | Chevra Baam (Ltd) | Osek Morsheh | Amuta |
|--------|-------------------|-------------|-------|
| Liability | Limited to investment | Personal, unlimited | Limited |
| Registration | Rasham, approximately 2,559 NIS online or 3,123 NIS paper (2026; verify at ica.justice.gov.il) | Tax Authority, free | Rasham HaAmutot |
| Minimum directors | 1 | N/A | 2 board members |

Tax differs by entity type and depends on the person's facts, so this skill does not compare tax outcomes. Refer the user to an accountant or tax adviser.

Osek patur: turnover is not the only test. Some occupations and services must register as osek morsheh under the VAT Registration Regulations. Check with the Tax Authority.

### Step 4: Registration Steps (Chevra Baam -- most common)
1. Choose unique company name (check availability at Rasham)
2. Draft Articles of Association (takanon)
3. File incorporation documents at Rasham HaChevarot
4. Pay registration fee (approximately 2,559 NIS online or 3,123 NIS paper (2026; verify at ica.justice.gov.il))
5. Receive Certificate of Incorporation (teuda le-hitaagdut)
6. Register with Tax Authority for income tax and VAT
7. Open business bank account with incorporation certificate
8. Register with Bituach Leumi as employer (if hiring)

## Examples

### Example 1: Company Lookup
User says: "Look up the company Monday.com"
Result: monday.com Ltd (registrar Hebrew name "מנדיי. קום בע"מ"), Company No. 514744887, Status: `פעילה`, sub-status empty, breach flag empty, Type: Israeli public company, incorporated 13/03/2012, registered at Yitzhak Sadeh 6, Tel Aviv-Yafo. Verified via the open registrar dataset in Step 2b, not from memory: company numbers are the single most fabrication-prone field in this domain, so always resolve one before quoting it. This describes the register entry and is not a finding that the company is safe to deal with.

### Example 2: Choose Entity Type
User says: "I'm a freelance developer, what business structure should I use?"
Result: Explain Osek Morsheh and Chevra Baam in general terms using Step 3. Do not pick an entity for the user. The choice is theirs, with an accountant or lawyer.

### Example 3: Compare Entity Types
User says: "I'm starting a business in Israel, should I register as an Osek Murshe or a Chevra?"
Actions:
1. Compare entity types (Osek Patur, Osek Murshe, Ltd company) on liability and registration
Result: Side-by-side comparison table, plus the questions to raise with an accountant or lawyer. Do not pick an entity for the user.

## Bundled Resources

### Scripts
- `scripts/search_company.py` - Display Israeli business entity types (Chevra Baam, Osek Morsheh, Amuta, etc.) with side-by-side comparison of liability and registration requirements, plus step-by-step Chevra Baam incorporation instructions. Supports subcommands: `entity-types`, `compare`, `registration-steps`. Run: `python scripts/search_company.py --help`

### References
- `references/entity-types.md` - Table of Israeli business entity types with their registries and liability structures. Consult when comparing entity types.
- `references/domain-checklist.md` - Coverage contract for this skill: which registries, statuses, fees and identifiers a complete Israeli entity lookup must handle, and what is explicitly out of scope (credit scoring, litigation history, foreign registries).

## Gotchas
- A company number identifies the company at the registrar. An individual dealer is registered with the Tax Authority and is not in the companies register, so a miss on a dealer's number proves nothing.
- The registrar's name fields are not always filled. The English field (`שם באנגלית`) is inconsistently populated and often spelled differently from the trading name. An English-only search can therefore return nothing for a company that exists. Search the Hebrew name and the company number before concluding a company is not registered.
- Status, sub-status and breach flag are separate fields. An agent that stops at `פעילה` will miss a company that is flagged in breach or is in a strike-off or liquidation process.
- Israeli business types include Chevra Baam (Ltd.), Shutafut (Partnership), Amuta (NPO), and Aguda Shitufit (Cooperative). Each has different registration systems. Agents may search for a partnership in the companies file, which does not contain it.
- Amutot are not in the companies file; GuideStar (`guidestar.org.il`) is the Ministry of Justice portal for them. A CHL"Tz (public-benefit company) is a company, so look for it in the companies register.
- "Apotropos Klali" (Official Receiver) was renamed to "ha-memuneh al chadlut pira'on ve-shikum kalkali" (Insolvency and Economic Rehabilitation Commissioner) when the Insolvency and Economic Rehabilitation Law 2018 took effect on 2019-09-15. For cases opened on or after that date, the searchable docket lives at `insolvency.justice.gov.il/poshtim/main/tikim/wfrmlisttikim.aspx`. Older "psikat regel" files predating 2019 are still under the legacy Apotropos Klali system.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Companies Registrar (ICA / rashut hatagidim) | https://ica.justice.gov.il | Company search, status, filings, ownership |
| Free company snapshot | https://www.gov.il/en/service/company_extract | Basic info free; full extract paid (fee shown on the request form) |
| GuideStar (Amutot + CHL"Tz) | https://www.guidestar.org.il | Consolidated MoJ portal for NPOs and public-benefit companies |
| Partnership extract | https://ica.justice.gov.il/Request/OpenRequest?rt=PartnershipExtract | Nesach shutfut from Rasham HaShutfuyot |
| data.gov.il - ica_companies | https://data.gov.il/dataset/ica_companies | Bulk dump of companies registrar (CKAN API available) |
| Reshumot - Yalkut HaPirsumim | https://www.gov.il/he/Departments/DynamicCollectors/gazette-official | Official gazette: liquidation notices, dissolution petitions, creditor calls |
| Insolvency Commissioner (post-2019 cases) | https://insolvency.justice.gov.il/poshtim/main/tikim/wfrmlisttikim.aspx | Searchable case list under Insolvency and Economic Rehabilitation Law 2018 |
| Apotropos Klali (legacy pre-2019 files + general guardianship) | https://www.gov.il/he/departments/agor_ministry_of_justice | Older psikat regel files, kintus nechasim |
| Israel Tax Authority | https://www.gov.il/he/departments/israel_tax_authority | Verify business TIN (mispar osek) separately |
| NBCTF sanctions designations | https://nbctf.mod.gov.il/en/Minister%20Sanctions/Designation/Pages/downloads.aspx | Counter-Terrorism Law 2016 designations of sanctioned individuals and entities. A source to check before dealing with a counterparty. |
| Israel Securities Authority (ISA) licensed entities | https://www.isa.gov.il | Portfolio managers, investment advisors, marketers (public licensed list) |
| Capital Market Authority (CMA) registries | https://www.gov.il/he/departments/units/department_cma | Licensed insurers, pension funds, kupot gemel, investment houses |

## Troubleshooting

### Error: "Company not found"
Cause: Name spelling mismatch or company registered under different name
Solution: Try Hebrew name, or search by company number if available. Some companies register with English names different from their trading name.

### Error: "Company number format invalid"
Cause: Different entity types are held in different registers
Solution: Identify the entity type first, then search the matching register. Do not reject a number on its format alone.

### Error: "Entity type confusion (Osek Patur vs Osek Morsheh)"
Cause: Users confuse tax registration types with company registration types
Solution: Osek Patur/Morsheh are VAT registration types at the Tax Authority (SHAAM), not company types at the Registrar of Companies. A person can be an Osek Morsheh without registering a company. Clarify the user's actual need: business entity lookup vs. tax registration status.

### Error: "Cannot find the amuta on ica.justice.gov.il"
Cause: Amutot are in a separate register
Solution: Search on GuideStar (`https://www.guidestar.org.il`), the Ministry of Justice portal for amutot and public-benefit companies.

### Error: "User asks for beneficial owner / UBO lookup"
Cause: The open companies dataset has no owner field
Solution: The closest signals are: directors and shareholders listed on a paid full company extract, the company's filed annual report (dorech shanati), and (for public companies only) ISA disclosures on Maya at `maya.tase.co.il`.