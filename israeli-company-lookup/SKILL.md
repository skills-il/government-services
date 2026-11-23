---
name: israeli-company-lookup
description: Register information, not due diligence. Look up Israeli companies and other registered entities, read what a registrar record means, and understand business entity types. Use when a user wants to check a supplier, contractor, borrower or investor before paying or signing, gives a company number (ח.פ.) or pastes a registrar row, gets an empty registry result, is choosing between entity types, asks about "chevra", business registration, "Rasham HaChevarot", or needs to register a business in Israel. Covers Ltd companies, partnerships, non-profits (amuta), cooperatives, and sole proprietors. Prevents reading "active" alone as a clean result. Do NOT use for non-Israeli corporate registries or stock market analysis.
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
| Register new business | Step 4 for a company. A dealer opens files with the Tax Authority |
| Check a counterparty | Report the register fields verbatim (Step 2b), then Step 2c |

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
The ICA search page in Step 2 is a human web form. For an agent, use the open registers on
data.gov.il. They are free and need no key. Use the number's prefix as a first guess at the register:

| Prefix | Entity | Resource id | Number field | Status field |
|--------|--------|-------------|--------------|--------------|
| 51, 52, 56 (foreign) | Companies, including CHL"Tz | `f004176c-b85f-4542-8901-7b3176f9a054` | `מספר חברה` | `סטטוס חברה` |
| 53, 54, 55 | Partnerships | `139aa193-fabb-4f6b-a71b-0bb40fd73eb2` | `מספר שותפות` | `סטטוס תאגיד` |
| 58 | Amutot | `be5b7935-3922-45d4-9638-08871b17ec95` | `מספר עמותה` | `סטטוס עמותה` |
| 57 | Cooperatives | `cad6bb66-5560-4cf4-a39c-92518f3f18ef` | `Identity` | `StatusDesc` |

A number outside these prefixes may belong to an individual dealer, who is not in these registers. If a number returns nothing, try the other registers before saying it is not registered. A miss proves nothing about whether the business is real.

- Free-text search:
  `https://data.gov.il/api/3/action/datastore_search?resource_id=f004176c-b85f-4542-8901-7b3176f9a054&q=MONDAY.COM&limit=5`
- Exact lookup by number (URL-encode the Hebrew field name):
  `https://data.gov.il/api/3/action/datastore_search?resource_id=f004176c-b85f-4542-8901-7b3176f9a054&filters={"מספר חברה":514744887}`

**Report every field below verbatim. In every register, show a value not listed here as it appears, say it must be checked at the registrar, and never guess its meaning or read it as clean.**

**1. `סטטוס חברה`**

| Value | Reading |
|-------|---------|
| `פעילה` | Registered and active. Keep reading the next fields |
| `פעילה זמנית` | Temporarily active |
| `בפרוק מרצון`, `בפרוק ע~י בימ~ש` | In voluntary or court liquidation |
| `פעילה/בפירוק - הליך פשרה או הסדר/פירוק זמני`, `פעילה/בפירוק - בכינוס נכסים` | In an arrangement, provisional liquidation or receivership |
| `מחוקה`, `מחוסלת מרצון`, `חיסול ע~י בימ~ש`, `מחוסלת עקב מיזוג`, `נגרעה מהמרשם` | Struck off, dissolved, merged away or removed from the register |

**2. `מפרה`**, a separate field. Empty means no marking. `התראה` is the registrar's warning, with 30 days to cure. `מפרה` means registered as a company in breach under Companies Law s.362א, for unpaid fees or, for a private or foreign non-reporting company, a missed annual report. It is not proof of insolvency. While it stands, the registrar may refuse to register a charge on the company's assets.

**3. `תת סטטוס`**, which can overturn an "active" reading. Split on `;`, trim, and report each value:

| Value | Reading |
|-------|---------|
| `פעילה` | Adds nothing |
| `בהליכי מחיקה` | Being struck off |
| `בפרוק מרצון בהליך מזורז` | Fast-track voluntary liquidation |
| `תצהיר כושר פירעון` | Directors declared the company can pay its debts within 12 months, ahead of a voluntary liquidation (s.342כה) |
| `צו לפתיחת הליכים`, `צו לפתיחת הליכים - תאגיד בשיקום` | Insolvency order, the second with rehabilitation |
| `הוגשה בקשת מיזוג - מיועדת להתמזג` | Will merge away |
| `הוגשה בקשת מיזוג - מיועדת לקלוט` | Will absorb another company |
| `בקשת נושים בהחייאה`, `בקשת חברה בהחייאה`, `הוגשה בקשה להחייאה` | Restoration requested |

**4. `שנה אחרונה של דוח שנתי (שהוגש)`.** A company that is not a reporting corporation files once a year (s.141), so a year older than the previous calendar year deserves a question. An empty field is normal for a new company and a question for an older one. Neither proves a breach. The type field does not show whether a company is a reporting corporation, so check Maya for public and bond companies.

**Recent registrar events** for a company or partnership: resource `28780ab5-3ef1-44c7-8377-da82c0aa6781`, filter on `מספר תאגיד`, event type in `סוג בקשה`. This file holds **only the last 12 months** and omits some changes even within them, including current-year fee payments and externally sourced information shown on the extract. So no row does NOT mean no charge, attachment or proceeding. Read the whole response and confirm the rows read equal `total`. If it is cut off, page with `limit` and `offset`, serially with a delay. If you still cannot read every row, report the events file as not fully checked, never as "no flag". The full list of charges is on the paid extract.

- Charges: group by `מזהה השיעבוד` and read by date. `רישום שעבוד` or `עדכון שעבוד` shows a charge exists, even if it was registered before the window. `סילוק שעבוד` removes it. `ביטול סילוק שעבוד` cancels the removal, so the charge is open again.
- If the latest events on a charge share a date, or an update follows a removal, report the charge as **unclear** and send the user to the registrar. Never call it discharged.
- Report these as items to verify: `משפטי כללי / תגובה לבית משפט- הערה לנסח` (a court note, whose content the file does not state), `צו לפתיחת הליכים`, `הוספה/עדכון הליך פשרה או הסדר`, `הוספה/עדכון/הסרה של צו עיקול` (may record a removal), `הוספה/עדכון צו להקפאת הליכים`, `כינוס נכסים`, `תאגיד בשיקום`, and any event containing `פירוק`, `חיסול`, `גריעה`, `החייא` or `ביטול אישור`. Show any other event type verbatim and do not read it as clean. `ביטול פירוק` and `ביטול תהליך הקפאת הליכים/כינוס נכסים/פירוק זמני` record a reversal.

**Other registers carry less.**

- Partnerships have no breach, sub-status or annual-report field. `פעילה` is live and `פעילה זמנית` is temporary. `בפרוק מרצון` and `בפרוק ע~י בימ~ש` are in liquidation. `מחוקה`, `שותפות מחוקה מרצון`, `שותפות מחוקה על ידי בית משפט`, `פורקה מרצון`, `פורקה ע~י בימ~ש`, `מחוסלת מרצון`, `מחוסלת עקב מיזוג` and `חיסול ע~י בימ~ש` have ended. Use the paid extract to identify the general partners.
- Amutot: `רשומה` and `פעילה` are live, and `בתהליכי רישום` is not yet registered. `בהליכי פירוק מרצון`, `בפרוק מרצון`, `בפרוק ע~י בימ~ש`, `ניתן צו פירוק על ידי בית משפט`, `הוגשה בקשת פירוק לבית משפט`, `פירוק זמני`, `כונס נכסים` and `החייאה` are warnings. `נמחקה`, `מחוקה`, `פורקה מרצון`, `מחוסלת מרצון`, `חיסול עקב מיזוג` and `מחוסלת עקב מיזוג` have ended.
- Amuta proper-management certificate: resource `cb12ac14-7429-4268-bc03-460f48157858`, filter on `מספר עמותה`. Read every row whose `שנת האישור` is the current year, with its `תאריך עדכון אחרון של רשומה` (DD/MM/YYYY), since a year can hold several rows. If all rows hold one value, report it. If they hold more than one value, show every row with its date, report the certificate as **unclear**, and send the user to the registrar. Call it granted only when every row that year is `נחתם אישור`. If no row exists for the current year, say so and draw no conclusion. Values: `נחתם אישור` is granted. `בטיפול`, `ממתין להשלמות` and `בבדיקה מקצועית` are in process. `אין אישור` is none, which is not illegality. `מסורב` and `מבוטל` are refused and cancelled.
- Cooperatives show `פעילה`, `בפירוק` or `סגורה`. The file can include test rows.

Raw names replace the Hebrew gershayim with `~` (`בע~מ`, `חל~צ`). Search with `~` or without the suffix.

Confirm you are reading real data: a successful response is JSON with `"success": true`. A number that is absent returns `"success": true` with `total: 0`, meaning "not in this register". A wrong `resource_id` returns an HTML 404 page, so read the body rather than trusting a status code.

These files are snapshots, not the live register. For a legally operative decision (signing, lending, litigating), confirm on the official ICA search or a paid extract.

### Step 2c: Before Paying or Signing
A record shows that an entity with this number exists. It does not show that the person in front of the user represents it. Tell the user to:

1. Match the number and legal name on the contract and invoice to the register. A different address or trading name is only a prompt to look closer, never a red flag on its own.
2. Confirm the bank account is held in the entity's name.
3. Confirm signing authority separately, since the open register has no signatory field. An unauthorized act may not bind the company (s.56). For a material sum, ask the company's lawyer or accountant for a signing-rights confirmation.

Report in the form "no flag found in X; not checked: Y". Never conclude that a company is clean, safe to contract with, or able to pay.

### Step 3: Entity Type Comparison
| Factor | Chevra Baam (Ltd) | Osek Morsheh | Amuta |
|--------|-------------------|-------------|-------|
| Liability | Limited, with exceptions | Personal, unlimited | Limited |
| Registration | Rasham, approximately 2,559 NIS online or 3,123 NIS paper (2026; verify at ica.justice.gov.il) | Tax Authority, free | Rasham HaAmutot |
| Minimum directors | 1 | N/A | 2 board members |

Limited liability has limits: a court may attribute company debt to a shareholder in exceptional cases (Companies Law s.6), and a personal guarantee binds the person who gave it.

Tax differs by entity type and depends on the person's facts, so this skill does not compare tax outcomes. Refer the user to an accountant or tax adviser.

Osek patur: turnover is not the only test. VAT Registration Regulations r.13 requires listed professions, and people whose occupation is providing the services listed in VAT Regulations r.6א, to register as osek morsheh regardless of turnover, for those services only. Separate rules can apply to someone whose main income is salary, pension or allowance. Read the regulation or ask the VAT office before treating an occupation as eligible. Do not state which status applies to this user.

### Step 4: Registration Steps (Chevra Baam -- most common)
1. Choose unique company name (check availability at Rasham)
2. Prepare Articles of Association (takanon). Refer tailored drafting to a lawyer
3. File incorporation documents at Rasham HaChevarot
4. Pay registration fee (approximately 2,559 NIS online or 3,123 NIS paper (2026; verify at ica.justice.gov.il))
5. Receive Certificate of Incorporation (teuda le-hitaagdut)
6. Register with Tax Authority for income tax and VAT
7. Open business bank account with incorporation certificate
8. Register with Bituach Leumi as employer if the company will have employees

## Examples

### Example 1: Company Lookup
User says: "Look up the company Monday.com"
Result: monday.com Ltd (registrar Hebrew name "מנדיי. קום בע~מ"), Company No. 514744887, Status: `פעילה`, sub-status empty, breach flag empty, Type: Israeli public company, incorporated 13/03/2012, registered at Yitzhak Sadeh 6, Tel Aviv-Yafo. Verified via the open registrar dataset in Step 2b, not from memory: company numbers are the single most fabrication-prone field in this domain, so always resolve one before quoting it. This describes the register entry and is not a finding that the company is safe to deal with.

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
- Israeli business types include Chevra Baam (Ltd.), Shutafut (Partnership), Amuta (NPO), and Aguda Shitufit (Cooperative). Each has different registration systems. Agents may search for a partnership in the companies file, which does not contain it. Use the partnerships resource in Step 2b.
- Amutot have their own register in Step 2b; GuideStar (`guidestar.org.il`) is the Ministry of Justice portal for them. A CHL"Tz (public-benefit company) is a company, so look for it in the companies register.
- The Official Receiver function passed to the Insolvency and Economic Rehabilitation Commissioner (ha-memuneh) under the Insolvency and Economic Rehabilitation Law 2018. The Administrator General (Apotropos Klali) is a separate office. Searchable case list: `insolvency.justice.gov.il/poshtim/main/tikim/wfrmlisttikim.aspx`.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Companies Registrar (ICA / rashut hatagidim) | https://ica.justice.gov.il | Company search, status, filings, ownership |
| Free company snapshot | https://www.gov.il/en/service/company_extract | Basic info free; full extract paid (fee shown on the request form) |
| GuideStar (Amutot + CHL"Tz) | https://www.guidestar.org.il | Consolidated MoJ portal for NPOs and public-benefit companies |
| Partnership extract | https://ica.justice.gov.il/Request/OpenRequest?rt=PartnershipExtract | Nesach shutfut from Rasham HaShutfuyot |
| data.gov.il - companies register API | https://data.gov.il/api/3/action/package_show?id=ica_companies | Dataset metadata and last refresh |
| Reshumot - Yalkut HaPirsumim | https://www.gov.il/he/Departments/DynamicCollectors/gazette-official | Official gazette: liquidation notices, dissolution petitions, creditor calls |
| Insolvency Commissioner (formerly Official Receiver) | https://insolvency.justice.gov.il/poshtim/main/tikim/wfrmlisttikim.aspx | Searchable case list |
| Administrator General (Apotropos Klali) | https://www.gov.il/he/departments/agor_ministry_of_justice | Separate office for guardianship and inheritance matters |
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
Solution: Use the prefix table in Step 2b as a first guess, then try the other registers. Do not reject a number on its format alone.

### Error: "Entity type confusion (Osek Patur vs Osek Morsheh)"
Cause: Users confuse tax registration types with company registration types
Solution: Osek Patur/Morsheh are VAT registration types at the Tax Authority (SHAAM), not company types at the Registrar of Companies. A person can be an Osek Morsheh without registering a company. Clarify the user's actual need: business entity lookup vs. tax registration status.

### Error: "Cannot find the amuta on ica.justice.gov.il"
Cause: Amutot are in a separate register
Solution: Query the amutot resource in Step 2b, or search GuideStar (`https://www.guidestar.org.il`), the Ministry of Justice portal for amutot and public-benefit companies.

### Error: "User asks for beneficial owner / UBO lookup"
Cause: The open companies dataset has no owner field
Solution: The closest signals are: directors and shareholders listed on a paid full company extract, the company's filed annual report (doch shnati), and (for public companies only) ISA disclosures on Maya at `maya.tase.co.il`.