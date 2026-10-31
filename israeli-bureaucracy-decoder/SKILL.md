---
name: israeli-bureaucracy-decoder
description: Decode confusing Israeli government letters, forms, and official documents into plain language. Use when you receive mail from the Tax Authority, Bituach Leumi, a municipality, the Population and Immigration Authority, the Land Registry, a planning committee, the Execution Office (Hotzaa LaPoal), or a court, and need to understand what it says, what action is required, and by when. Covers assessment notices, benefit and medical-committee decisions, arnona and fine notices, zoning notices, court summons and judgments, and the deadline and venue for an objection or appeal (השגה, ערר, התנגדות, ערעור). Also explains bureaucratic terms such as שומה, השגה and ערר. Do NOT use for drafting legal appeals.
license: MIT
allowed-tools: Bash(python:*) Read Edit WebFetch
compatibility: Works with all major AI coding agents
---


# Israeli Bureaucracy Decoder

## Legal notice

This is a free information tool operated by an AI model. It explains the law and the procedure and helps you organise your own documents. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by an advocate. The output is not legal advice and not a legal opinion, but a general explanation and a template only: it does not read the full file of your matter, does not check current case law, and does not examine your specific circumstances. An AI model may err, omit data, or present a wrong conclusion.

Any text this tool drafts is an automatic draft for your personal preparation only. It is not a document prepared by an advocate and must not be relied on as evidence. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Before starting proceedings, signing a document, or filing with an authority or a court, consult an advocate. All use of its output is the user's sole responsibility.


Think of this skill as your friend who works in the government. You hand them a confusing letter, they read it, and tell you: "Relax, here is what this actually means, and here is what you need to do."

## Instructions

### Step 1: Receive the document

Ask the user to paste the full text of the government document, or provide a file path to a scanned/digital document. Accept text in Hebrew, English, or a mix of both (common in official Israeli documents).

If the user provides a file path, read the file content. If it is a text file, read it directly. If the user describes the document rather than pasting it, ask clarifying questions to identify the sending body and document type.

### Step 1.5: Check the user's personal area (ezor ishi / MyGov) first

Before escalating to phone calls or office visits, ask the user whether they have already signed into the relevant personal area. Many "missing" letters are actually sitting in the user's digital inbox. The common personal-area accounts are:

- Tax Authority: the "אזור אישי ברשות המסים" link on the Tax Authority's gov.il page (`gov.il/he/departments/israel_tax_authority`), which opens `secapp.taxes.gov.il/sr-ezor-ishi`.
- Bituach Leumi: `btl.gov.il` ("אזור אישי")
- Population and Immigration Authority (PIBA): `gov.il/he/departments/population_and_immigration_authority`
- Unified government sign-in: `login.gov.il`

If a digital copy of the letter is available there, work from that copy. It is usually clearer, dated more reliably, and links to the underlying file. This is especially relevant if the paper letter is illegible, cut off, or arrived late.

### Step 2: Identify the sending body and document type

Consult `references/government-bodies-guide.md` to identify which government body sent the document. Look for:

- Letterhead or header text (e.g., "רשות המסים בישראל", "המוסד לביטוח לאומי")
- Reference numbers and their formats (each body uses different patterns)
- Official stamps, department names, or regional office identifiers
- Form numbers (e.g., "טופס 101", "טופס 1301")

Cross-reference any form numbers with `references/common-government-forms.md` to understand the form's purpose.

### Step 3: Decode the bureaucratic language

Consult `references/bureaucratic-hebrew-glossary.md` to translate official jargon into plain language. Government documents are deliberately written in dense legal Hebrew. Your job is to cut through that.

For each paragraph or section of the document:

1. Identify the key information being communicated
2. Replace bureaucratic terms with everyday language
3. Note any legal references (laws, regulations, clauses) and explain what they mean in practice
4. Flag anything that sounds threatening but is actually standard boilerplate

### Step 4: Run the document analyzer

Use the document analyzer script to extract structured information:

```bash
python scripts/document-analyzer.py --text "PASTE_DOCUMENT_TEXT_HERE"
```

Or if the text is in a file:

```bash
python scripts/document-analyzer.py --file path/to/document.txt
```

For a PDF with a text layer, extract it first with `pdftotext -layout letter.pdf letter.txt` and pass `--file letter.txt`; the script strips the invisible bidi marks that PDF extraction inserts around numbers, which otherwise hide every amount and deadline. A scanned PDF with no text layer needs OCR first.

The script extracts: sender, document type, subject, required actions, deadlines, consequences of inaction, and relevant laws. Read its NOTES block: it says when the text looked reversed or in visual order, and in that case read the amounts and dates from the original letter rather than from the script.

### Step 5: Present the decoded summary

**Before you write the summary, check kol-zchut.** Before calling the office or quoting a benefit amount, look up the relevant entry on `kolzchut.org.il` (the hyphenated `kol-zchut` spelling does not resolve) for the canonical Hebrew explanation of the right, benefit, deadline, or appeal venue mentioned in the letter. Kol-zchut is the best plain-language source for current Israeli civic rights and usually names the statute behind each rule. Use it to find the rule and to explain it simply, but the statute and the official body's own page govern: if kol-zchut disagrees with them or with the decision table below, follow the official source and tell the user about the discrepancy.

Present the decoded document in this clear format:

**Who sent this:** [Government body name in plain language]

**What this is:** [Document type in one sentence]

**What it actually says:** [Plain language summary, 2-4 sentences. No jargon.]

**What you need to do:**
1. [Action item with specific details]
2. [Action item with specific details]
(number each action clearly)

**Deadlines:**
- [Date] -- [What needs to happen by this date]
- [Date] -- [What happens if you miss this date]

**How urgent is this?**
- URGENT (red flag): if the response window is 30 days or less, there is a court date, or there is a threat of enforcement
- IMPORTANT (yellow flag): if the window is longer than 30 days, or a response is required with no stated window
- INFORMATIONAL (green flag): if no action is required, just awareness

**Next steps:**
- [Specific guidance: which office to contact, which form to fill, phone numbers if known]
- [Whether you should consult a professional (accountant, lawyer, social worker)]

### Step 6: Offer follow-up help

After presenting the summary, offer to:

1. Explain any specific section in more detail
2. Help draft a simple reply to an administrative body when one is needed (answering a document request, or asking the Tax Authority, Bituach Leumi or a municipality for instalments or an extension). For anything filed with a court, a tribunal or appeals committee, or the Execution Office registrar (including a request to cancel a demolition order, to set aside a judgment or a seizure, or to extend a court deadline), and for any objection, appeal, opposition, statement of defence or petition (השגה, ערר, התנגדות, כתב הגנה, ערעור, עתירה): list the points the user can write from, what the filing must contain, the deadline and where to file, without producing a ready-to-file document, and refer the user to a lawyer, or to legal aid (הסיוע המשפטי) where eligible. Filling in an authority's own published form can be explained field by field for the user to complete. For a request to cancel a parking or traffic fine, point the user to the `israeli-fines-fighter` skill
3. Identify related forms that might need to be filed
4. Explain what happens if the user takes no action
5. Translate the summary into the other language (Hebrew to English or vice versa)

## Decision Table: Sender + Key Term → Urgency, Window, Appeal Venue

Use this as a fast lookup when classifying urgency and pointing the user to the right escalation channel. These are typical patterns, **always verify the specific deadline written on the letter itself and against the statute or the official body's page** (kol-zchut helps locate the section), since regulations and ceilings shift.

| Sender | Key term in the letter | Urgency tier | Standard response window | Where to appeal / escalate |
|--------|------------------------|--------------|---------------------------|----------------------------|
| Tax Authority | שומה לפי מיטב השפיטה | URGENT | 30 days to file a written השגה (objection) under Section 150 of the Income Tax Ordinance | Internal השגה, then appeal to District Court (Tax Affairs) |
| Tax Authority | החלטה בהשגה (צו) | URGENT | 30 days to appeal (Income Tax Appeals Regulations, reg. 2) | District Court (Tax Affairs) |
| Tax Authority (VAT) | שומת מע"מ | URGENT | 30 days from service to file a reasoned written השגה (VAT Law s.82); if the director does not decide within a year, the השגה is deemed accepted | VAT director (מנהל), then District Court (s.83) |
| Taxes on Land (מיסוי מקרקעין) | שומת מס שבח / מס רכישה | URGENT | 30 days from delivery to file השגה (Real Estate Taxation Law s.87) | Director of Taxes on Land, then ערר to the appeals committee within 30 days (s.88) |
| Tax Authority | קנס גירעון | URGENT | Treated as an assessment, so the 30-day השגה applies | Internal השגה, then District Court |
| Tax Authority | קנס על אי הגשת דו"ח | IMPORTANT | Read the letter for the review route; do not assume the 30-day השגה applies | The assessing officer named in the letter; get professional advice |
| Bituach Leumi | דחיית תביעה | IMPORTANT | 12 months to appeal (6 months for alimony / מזונות decisions) | Beit Din L'Avoda (Labor Court) |
| Bituach Leumi | קביעת אחוזי נכות (general disability) | IMPORTANT | 60 days to file a ערר, in writing with reasons | Medical Appeals Committee, then Labor Court on points of law only (60 days) |
| Bituach Leumi | קביעת אחוזי נכות (work injury) | URGENT | 30 days to file the ערר (reasons may follow within 60) | Medical Appeals Committee, then Labor Court on points of law only (60 days) |
| Municipality | שינוי סיווג ארנונה / הודעת תשלום | IMPORTANT | 90 days to file השגה. The manager must answer within 60 days, or the השגה is deemed accepted (unless the appeals committee extended that by up to 30 days) | מנהל הארנונה |
| Municipality | תשובה להשגה על ארנונה | URGENT | 30 days to file a ערר | ועדת ערר, then administrative appeal to the Administrative Affairs Court (60 days) |
| Municipality / police | הודעת תשלום קנס (parking, by-law, traffic) | URGENT | 30 days to ask the prosecutor to cancel it; 90 days to pay or to give notice of wanting to be tried (Criminal Procedure Law s.229) | Prosecutor, or court if the user asks to be tried; see `israeli-fines-fighter` |
| Municipality | התראה לפני נקיטת הליכים | URGENT | Act immediately | Pay or arrange instalments with the collection department; to dispute the debt itself, get advice promptly, since the route depends on the debt |
| Planning Committee | הודעה על בקשה להקלה / שימוש חורג | URGENT | 15 days from publication (or from personal delivery) to object (Planning and Building Law s.149) | Local planning committee |
| Planning Committee | סירוב היתר | URGENT | 30 days from service of the refusal | District Appeals Committee (ועדת ערר) |
| Planning Committee | שומת היטל השבחה | IMPORTANT | 45 days from the assessment coming to your knowledge to file a ערר (Planning and Building Law, Third Schedule). If only the amount is disputed, ask within the same period for a decisive appraiser (שמאי מכריע) | Compensation and Betterment Levy Appeals Committee; consult a licensed appraiser |
| Planning Committee | צו הריסה מנהלי | URGENT | 15 days from service to ask the court to cancel it; filing does not stay the order | Magistrate Court, or the court for local affairs when the local committee issued it; counsel immediately |
| Hotzaa LaPoal | אזהרה (judgment file) | URGENT | 20 days to pay, arrange instalments, or ask for a payment order | The Execution Office registrar |
| Hotzaa LaPoal | אזהרה (bill or cheque / שטר file, or fixed-sum claim / תביעה על סכום קצוב file) | URGENT | 30 days to file התנגדות | Execution Office, which then transfers the case to court |
| Hotzaa LaPoal | החלטת רשם ההוצאה לפועל | URGENT | 20 days from the decision (or from service if given in your absence) to appeal, usually by leave (Execution Law s.80; regulations reg. 120) | Magistrate Court; in a family-matter file, the Family Court as of right |
| Hotzaa LaPoal | עיקול | URGENT | Immediate | Motion to release / arrangement; for payment orders, restrictions and registrar decisions see `israeli-hotzaa-lapoal-debtor` |
| Land Registry | החלטת רשם המקרקעין (e.g. a registration refused) | URGENT | 15 days from delivery (or from learning of it) to file a ערר (Land Registration Regulations reg. 74) | Registrar Supervisor (הממונה על המרשם), then District Court within 15 days (reg. 76) |
| Court | הזמנה לדין | URGENT | Per the summons | The court itself; consult a lawyer |
| Court (Magistrate) | כתב תביעה | URGENT | 60 days to file כתב הגנה (תקנות סדר הדין האזרחי תשע"ט-2018) | The same court |
| Court (Small Claims) | כתב תביעה | URGENT | 30 days to file כתב הגנה | The same court |
| Court (Small Claims) | פסק דין | URGENT | Leave to appeal within 15 days of the judgment; 30 days in proceedings opened on or after 11.4.2025 (Small Claims Regulations reg. 16). Ask when the claim was opened | District Court; see `israeli-small-claims-court` |
| Labour Court (בית הדין האזורי לעבודה) | פסק דין | URGENT | 30 days from the hearing or from service, unless another law sets a different period; some cases need leave first. The civil 60-day rule does not apply | National Labour Court |
| Court (Magistrate / District) | פסק דין | IMPORTANT | 60 days from service of the judgment (Civil Procedure Regulations reg. 137) | The next court up |
| PIBA | החלטה בעניין מעמד | URGENT | 30 days to file a ערר, counted from publication of the decision, notice of it, or learning of it, whichever is earliest | Appeals Tribunal (בית הדין לעררים), then Administrative Affairs Court (45 days) |
| PIBA | הודעה בעניין תעודת זהות / דרכון | INFORMATIONAL or IMPORTANT | Per the letter | PIBA office (book via `govisit.gov.il`) |
| Mevaker HaMedina | פנייה / החלטה | INFORMATIONAL | Per the letter | Cooperate; this is itself an escalation venue |

### Route to a dedicated skill for depth

This skill identifies the letter, the window and the venue. For the full procedure, hand off to the dedicated skill: `israeli-hotzaa-lapoal-debtor` (every Execution Office letter), `israeli-fines-fighter` (parking and traffic fines), `israeli-small-claims-court`, `israeli-tabu-extract-decoder` (Land Registry extracts), `israeli-bituach-leumi` (benefit claims), `israeli-arnona-optimizer` (arnona discounts and classification), `israeli-employee-tax-refund` (refunds on Form 135) and `israeli-vat-reporting` (VAT reports).

### Escalation ladder when standard channels fail

When the agency's internal objection / appeal has been used (or is plainly futile):

1. **Freedom of Information request** (`gov.il/he/service/freedom_of_information_submission`) if the letter cites information the user cannot otherwise access. Each public body has a designated information officer; statutory response window 30 days at most, which a public body may extend for a COMPLEX request up to 120 days, giving written reasons for the extension. A request fee of 24 NIS applies, plus an hourly handling fee from the 4th hour of work and a per-page production fee, with exemptions per the 1998 law.
2. **State Comptroller and Ombudsman** (complaint intake at `complaint.mevaker.gov.il`) for complaints about maladministration, delay, or abuse of authority by a public body. In Israel the State Comptroller and the Ombudsman (נציב תלונות הציבור) are the same office.
3. **Administrative petition** (עתירה מנהלית) to the District Court sitting as an Administrative Affairs Court, no later than 45 days from publication of the decision, notice of it, or learning of it, whichever is earliest, unless another law sets a different period; the court may extend it. For nationwide-impact or constitutional issues, the High Court of Justice (בג"ץ). Always recommend consulting a lawyer first.

## Examples

### Example 1: Tax Authority Assessment Notice

User says: "I got this letter from Reshut HaMisim and I have no idea what it means. It says something about shomah and I need to respond within 30 days?"

Actions:
1. Read the document text the user provides
2. Identify it as a "שומה" (tax assessment) from the Tax Authority, likely a "שומה לפי מיטב השפיטה" (best judgment assessment) or "שומה בהסכמה" (agreed assessment)
3. Consult the government bodies guide to understand Tax Authority assessment types
4. Consult the glossary for terms like "שומה", "השגה", "מס הכנסה", "סעיף 150"
5. Run the document analyzer to extract deadlines and required actions
6. Present a clear summary explaining that a "shomah" is essentially the Tax Authority's calculation of how much tax they think the user owes, and whether the user agrees or wants to dispute it

Result: The user understands they received a tax assessment notice. The decoder explains that "שומה לפי מיטב השפיטה" means the Tax Authority made their own calculation because the user either did not file a return or the Authority disagrees with what was filed. The user has 30 days to file a "השגה" (objection) if they disagree, or the assessment becomes final. The decoder suggests consulting a tax accountant ("רואה חשבון") before the deadline.

### Example 2: Bituach Leumi Benefit Decision

User says: "Bituach Leumi sent me a letter about my miluim claim. There are a lot of numbers and references to sections of the law. Can you tell me if they approved it?"

Actions:
1. Read the document text
2. Identify it as a decision letter from the National Insurance Institute regarding reserve duty ("מילואים") compensation
3. Consult the glossary for terms like "תגמול", "דמי מילואים", "חוק הביטוח הלאומי"
4. Look for key phrases: "אושרה" (approved), "נדחתה" (denied), "חלקית" (partial)
5. Extract the payment amount, period covered, and payment date
6. Present a clear breakdown of the decision

Result: The user learns their reserve duty claim was approved for 15 days at the minimum daily rate of 328.76 NIS (the floor effective 01.01.2026; the actual rate is usually higher and based on the reservist's income), totaling 4,931.40 NIS before tax. The letter references Section 272 of the National Insurance Law, which is the standard legal basis for the reserve duty compensation rate (within Chapter XII, "תגמולים למשרתים במילואים"), nothing unusual. No action required unless the user believes the number of days or the daily rate is incorrect, in which case they have 12 months to appeal.

### Example 3: Municipal Arnona Notice

User says: "My iriya sent something about arnona and it mentions hanacha but I can not tell if they are giving me a discount or asking for more money."

Actions:
1. Read the document text
2. Identify it as a municipal tax ("ארנונה") notice, likely about a discount ("הנחה") decision
3. Consult the glossary for "ארנונה", "הנחה", "ועדת הנחות", "סיווג נכס"
4. Look for whether the document is: an approval of a discount, a rejection, a reclassification of the property, or an annual rate update
5. Check for any payment schedule or deadline information
6. Present a clear explanation of the arnona system and what this specific notice means

Result: The user's municipality approved a 25% arnona discount based on income level ("הנחה לפי מבחן הכנסות"). The discount applies from January to December of the current year. The remaining balance is 8,400 NIS, payable in 6 bi-monthly installments. No action needed unless the user's income has changed significantly, in which case they can request a reassessment. The decoder also notes that the discount does not renew automatically and the user will need to reapply next year with updated income documentation.

### Example 4: Court Summons or Legal Notice

User says: "I got something from Beit Mishpat that looks serious. It has a date and a case number. Am I being sued?"

Actions:
1. Read the document text carefully
2. Identify the court type (Magistrate/שלום, District/מחוזי, Small Claims/תביעות קטנות, Family/משפחה, Labor/עבודה)
3. Determine the document type: summons ("הזמנה לדין"), claim ("כתב תביעה"), judgment ("פסק דין"), or notification ("הודעה")
4. Extract the case number, parties involved, hearing date, and required response
5. Flag this as URGENT and recommend immediate professional consultation

Result: The user received a summons to Small Claims Court as the defendant. Someone filed a claim against them for 12,000 NIS regarding a service dispute. The hearing is scheduled for 45 days from the letter date. The user MUST file a written defense ("כתב הגנה") within 30 days of receiving the claim, or they risk a default judgment ("פסק דין בהיעדר הגנה"). The decoder strongly recommends consulting a lawyer, though representation by a lawyer is not required in Small Claims Court.

## Bundled Resources

### Scripts
- `scripts/document-analyzer.py` -- Analyze government document text to extract structured information (sender, type, actions, deadlines, consequences). Run: `python scripts/document-analyzer.py --help`

### References
- `references/government-bodies-guide.md` -- Comprehensive guide to Israeli government bodies, their common letter types, typical jargon, and what they usually want from you. Consult when identifying which body sent a document and what type of document it is.
- `references/bureaucratic-hebrew-glossary.md` -- Hebrew bureaucratic terms with plain-language explanations, organized by domain (legal, tax, social security, municipal, real estate, immigration). Consult when you encounter official jargon that needs translation to everyday language.
- `references/common-government-forms.md` -- Index of frequently encountered Israeli government forms with their purposes, who needs to file them, and when. Consult when a document references a form number or when advising the user on which forms to file.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [Kolzchut (All-Rights)](https://agentskills.co.il/he/mcp/kolzchut) | Look up actual rights and entitlements referenced in government letters. When a document mentions a benefit, discount, or eligibility, Kolzchut provides the authoritative details. |
| [Knesset](https://agentskills.co.il/he/mcp/knesset) | Access legislative data for bills and committee information. Useful when documents reference pending legislation or regulatory changes. |

## Gotchas
- Israeli government form names change over time, and the same form may have different names in different offices. Agents may reference a form name that is no longer current.
- Hebrew bureaucratic language (lashon misradit) uses formal/archaic terms that differ from everyday Hebrew. Agents may generate translations using everyday Hebrew that do not match the official terminology on forms.
- Many Israeli government processes require in-person visits (biu'ach ishi) and cannot be completed entirely online. Agents may suggest completing a process online when a physical visit is required.
- Government office hours vary by office and by day. Agents may suggest a visit when the office is closed: check the reception hours on the office's gov.il page first.
- `gov.il` URLs are frequently restructured and individual department slugs redirect or 404. Treat direct deep links as best-effort, not authoritative. If a slug does not resolve, send the user to the `gov.il` homepage and have them search by the service name (the search bar is more stable than department paths).
- In-person visits almost always require a pre-booked appointment now. The unified gov.il booking portal is `govisit.gov.il`, which books PIBA (ID cards, passports, population registry), Ministry of Transport and court-system services. For Bituach Leumi, check `btl.gov.il` for how its branches take appointments.
- Many digital forms now require a personal **digital signature** certificate from a certification authority (גורם מאשר) recognised by the Ministry of Justice under the Electronic Signature Law, 5761-2001. Two companies are recognised: Comsign and Personal ID (gov.il notary guidance). Suggesting "just sign it digitally" is wrong if the user does not have a certificate set up.
- The same document type can run on different clocks. An execution אזהרה gives 20 days on a judgment file and 30 days to object on a bill, cheque or fixed-sum claim file; a medical-committee ערר is 60 days for general disability but 30 for a work injury. Never quote a window from the document type alone: read the period stated in the letter and check what it is counted from (service, receipt, or learning of the decision), never from the date printed at the top.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Tax Authority | https://www.gov.il/en/departments/israel_tax_authority | Tax assessment types, objection procedures, current deadlines |
| Bituach Leumi (NII) | https://www.btl.gov.il | Benefit amounts, claim forms, eligibility criteria |
| Open Law Book (Wikisource) | https://he.wikisource.org/wiki/ספר_החוקים_הפתוח | Consolidated text of laws and regulations cited in government documents |
| Kolzchut (All-Rights) | https://www.kolzchut.org.il | Plain-language explanations of rights and entitlements |
| Israeli Courts | https://www.gov.il/en/departments/the_judicial_authority | Court procedures, filing deadlines, small claims limits |
| Enforcement Authority | https://www.gov.il/he/departments/law_enforcement_and_collection_system_authority | Execution file procedures, objection deadlines |

## Troubleshooting

### Error: "I cannot identify which government body sent this"

Cause: The document may be missing a clear letterhead, or it may be from a lesser-known sub-department or regional office. Some documents come from private entities acting on behalf of government bodies (e.g., collection agencies hired by municipalities).

Solution: Look for these secondary identifiers: (1) Reference number format, as each body uses distinct patterns. (2) The legal clauses cited in the document, which point to specific laws administered by specific bodies. (3) The return address or phone number. (4) Any form numbers mentioned. If still unclear, ask the user if they have the envelope, which may have additional identifying information. Consult `references/government-bodies-guide.md` for reference number patterns.

### Error: "The document references a law or regulation I do not recognize"

Cause: Israeli bureaucratic documents frequently cite specific sections of laws ("סעיף 150 לפקודת מס הכנסה") without explaining what those sections say. There are hundreds of laws and thousands of sections.

Solution: Note the law name and section number, then explain the general domain it covers based on context. Common laws you will encounter: Income Tax Ordinance ("פקודת מס הכנסה"), National Insurance Law ("חוק הביטוח הלאומי"), VAT Law ("חוק מס ערך מוסף"), Planning and Building Law ("חוק התכנון והבנייה"), Municipal Ordinances ("צווי ארנונה"). If the specific section is critical to understanding the document, use WebFetch to look up the section text in the Open Law Book on Hebrew Wikisource (he.wikisource.org, which serves plain text) or on Nevo. The Knesset site blocks automated fetches.

### Error: "The deadline has already passed"

Cause: Many government letters still arrive by ordinary mail, so part of the response window may have elapsed before the user opens the letter. Most statutory windows run from SERVICE or RECEIPT of the letter (מיום ההמצאה / מיום הקבלה), not from the date printed on it, but a few run from the decision date or from when the person learned of it, whichever is earlier (PIBA's ערר is one).

Solution: First, check what the deadline is counted from (look for "מיום ההמצאה", "מיום הקבלה", "מיום שנודע"). Do not assume a fixed number of postal days: if the receipt date matters, ask the user when it actually arrived and whether a digital copy in the personal area is dated earlier. If the deadline has truly passed, explain the consequences and advise the user on options: (1) Some bodies allow late submissions with a reasonable explanation. (2) Courts and the Tax Authority have formal extension request procedures. (3) In some cases, the deadline is not absolute and the user can still act, just with reduced leverage. Recommend consulting a professional immediately.

### Error: "The document is partially illegible or cut off"

Cause: Scanned documents, old faxes, or photocopied letters may have missing sections, blurred text, or cut-off margins. Government offices sometimes print on both sides, and the user may have only scanned one side.

Solution: Work with what is available. Identify as many structural elements as possible (sender, reference number, date, any visible deadlines). Flag the missing sections explicitly in the summary and note what information might be in the illegible parts. Suggest the user: (1) Check if there is a second page or reverse side. (2) Contact the sending body's call center with the reference number to get the document resent or read over the phone. (3) Check their government personal area (e.g., the Tax Authority's "אזור אישי", linked from its gov.il page) where many documents are available digitally.
