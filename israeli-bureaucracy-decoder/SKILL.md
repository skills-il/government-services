---
name: israeli-bureaucracy-decoder
description: >-
  Decode confusing Israeli government letters, forms, and official documents into
  plain language. Use when you receive mail from the Tax Authority, Bituach Leumi,
  municipalities, Interior Ministry, Land Registry, courts, or any government body
  and need to understand what it says, what action is required, and by when. Covers
  assessment notices, benefit decisions, municipal levies, zoning notices, and court
  summons. Do NOT use for drafting legal appeals or providing binding legal advice.
license: MIT
allowed-tools: Bash(python:*) Read Edit WebFetch
compatibility: Works with all major AI coding agents
metadata:
  author: skills-il
  version: 1.0.1
  category: government-services
  tags:
    he:
    - בירוקרטיה
    - טפסים-ממשלתיים
    - פענוח-מסמכים
    - שפה-פשוטה
    - ציות
    en:
    - bureaucracy
    - government-forms
    - document-decoder
    - plain-language
    - compliance
  display_name:
    he: מפענח בירוקרטיה ישראלית
    en: Israeli Bureaucracy Decoder
  display_description:
    he: >-
      מפענח מכתבים ומסמכים רשמיים מגופים ממשלתיים לשפה פשוטה וברורה, כולל זיהוי פעולות
      נדרשות ומועדים אחרונים
    en: >-
      Decode confusing Israeli government letters, forms, and official documents into
      plain language. Use when you receive mail from the Tax Authority, Bituach Leumi,
      municipalities, Interior Ministry, Land Registry, courts, or any government
      body and need to understand what it says, what action is required, and by when.
      Covers assessment notices, benefit decisions, municipal levies, zoning notices,
      and court summons. Do NOT use for drafting legal appeals or providing binding
      legal advice.
  supported_agents:
  - claude-code
  - cursor
  - github-copilot
  - windsurf
  - opencode
  - codex
---


# Israeli Bureaucracy Decoder

Think of this skill as your friend who works in the government. You hand them a confusing letter, they read it, and tell you: "Relax, here is what this actually means, and here is what you need to do."

## Instructions

### Step 1: Receive the document

Ask the user to paste the full text of the government document, or provide a file path to a scanned/digital document. Accept text in Hebrew, English, or a mix of both (common in official Israeli documents).

If the user provides a file path, read the file content. If it is a text file, read it directly. If the user describes the document rather than pasting it, ask clarifying questions to identify the sending body and document type.

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

The script extracts: sender, document type, subject, required actions, deadlines, consequences of inaction, and relevant laws.

### Step 5: Present the decoded summary

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
- URGENT (red flag): if there is a deadline within 30 days, a court date, or a threat of enforcement
- IMPORTANT (yellow flag): if there is a deadline within 90 days or a required response
- INFORMATIONAL (green flag): if no action is required, just awareness

**Next steps:**
- [Specific guidance: which office to contact, which form to fill, phone numbers if known]
- [Whether you should consult a professional (accountant, lawyer, social worker)]

### Step 6: Offer follow-up help

After presenting the summary, offer to:

1. Explain any specific section in more detail
2. Help draft a response letter if one is needed
3. Identify related forms that might need to be filed
4. Explain what happens if the user takes no action
5. Translate the summary into the other language (Hebrew to English or vice versa)

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

Result: The user learns their reserve duty claim was approved for 15 days at a daily rate of 350.40 NIS, totaling 5,256 NIS before tax. Payment will arrive within 10 business days. The letter references Section 272 of the National Insurance Law, which is the standard legal basis for reserve duty compensation, nothing unusual. No action required unless the user believes the number of days or the daily rate is incorrect, in which case they have 12 months to appeal.

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

Result: The user received a summons to Small Claims Court as the defendant. Someone filed a claim against them for 12,000 NIS regarding a service dispute. The hearing is scheduled for 45 days from the letter date. The user MUST file a written defense ("כתב הגנה") at least 15 days before the hearing date, or they risk a default judgment ("פסק דין בהיעדר הגנה"). The decoder strongly recommends consulting a lawyer, though representation by a lawyer is not required in Small Claims Court.

## Bundled Resources

### Scripts
- `scripts/document-analyzer.py` -- Analyze government document text to extract structured information (sender, type, actions, deadlines, consequences). Run: `python scripts/document-analyzer.py --help`

### References
- `references/government-bodies-guide.md` -- Comprehensive guide to Israeli government bodies, their common letter types, typical jargon, and what they usually want from you. Consult when identifying which body sent a document and what type of document it is.
- `references/bureaucratic-hebrew-glossary.md` -- Hebrew bureaucratic terms with plain-language explanations, organized by domain (legal, tax, social security, municipal, real estate, immigration). Consult when you encounter official jargon that needs translation to everyday language.
- `references/common-government-forms.md` -- Index of frequently encountered Israeli government forms with their purposes, who needs to file them, and when. Consult when a document references a form number or when advising the user on which forms to file.

## Gotchas
- Israeli government form names change over time, and the same form may have different names in different offices. Agents may reference a form name that is no longer current.
- Hebrew bureaucratic language (lashon misradit) uses formal/archaic terms that differ from everyday Hebrew. Agents may generate translations using everyday Hebrew that do not match the official terminology on forms.
- Many Israeli government processes require in-person visits (biu'ach ishi) and cannot be completed entirely online. Agents may suggest completing a process online when a physical visit is required.
- Government office hours in Israel vary: some close at 12:30 PM on certain days, and most are closed on Fridays. Agents may suggest visiting offices during hours when they are closed.

## Troubleshooting

### Error: "I cannot identify which government body sent this"

Cause: The document may be missing a clear letterhead, or it may be from a lesser-known sub-department or regional office. Some documents come from private entities acting on behalf of government bodies (e.g., collection agencies hired by municipalities).

Solution: Look for these secondary identifiers: (1) Reference number format, as each body uses distinct patterns. (2) The legal clauses cited in the document, which point to specific laws administered by specific bodies. (3) The return address or phone number. (4) Any form numbers mentioned. If still unclear, ask the user if they have the envelope, which may have additional identifying information. Consult `references/government-bodies-guide.md` for reference number patterns.

### Error: "The document references a law or regulation I do not recognize"

Cause: Israeli bureaucratic documents frequently cite specific sections of laws ("סעיף 150 לפקודת מס הכנסה") without explaining what those sections say. There are hundreds of laws and thousands of sections.

Solution: Note the law name and section number, then explain the general domain it covers based on context. Common laws you will encounter: Income Tax Ordinance ("פקודת מס הכנסה"), National Insurance Law ("חוק הביטוח הלאומי"), VAT Law ("חוק מס ערך מוסף"), Planning and Building Law ("חוק התכנון והבנייה"), Municipal Ordinances ("צווי ארנונה"). If the specific section is critical to understanding the document, use WebFetch to look up the section text on the Knesset legislation database (main.knesset.gov.il) or on Israeli legal databases.

### Error: "The deadline has already passed"

Cause: Government letters in Israel are sent by regular mail, and delivery can take 5-14 days. By the time the user reads the letter, a significant portion of the response window may have elapsed. Some letters have a "deemed received" date that is several days after the actual send date.

Solution: First, check if the deadline is calculated from the send date or the receipt date (look for "מיום המשלוח" vs "מיום הקבלה"). Many deadlines in Israeli law are calculated from the "deemed receipt" date, which is typically 3-5 days after the send date. If the deadline has truly passed, explain the consequences and advise the user on options: (1) Some bodies allow late submissions with a reasonable explanation. (2) Courts and the Tax Authority have formal extension request procedures. (3) In some cases, the deadline is not absolute and the user can still act, just with reduced leverage. Recommend consulting a professional immediately.

### Error: "The document is partially illegible or cut off"

Cause: Scanned documents, old faxes, or photocopied letters may have missing sections, blurred text, or cut-off margins. Government offices sometimes print on both sides, and the user may have only scanned one side.

Solution: Work with what is available. Identify as many structural elements as possible (sender, reference number, date, any visible deadlines). Flag the missing sections explicitly in the summary and note what information might be in the illegible parts. Suggest the user: (1) Check if there is a second page or reverse side. (2) Contact the sending body's call center with the reference number to get the document resent or read over the phone. (3) Check their government portal account (e.g., the Tax Authority's "Personal Area" at mof.gov.il) where many documents are available digitally.
