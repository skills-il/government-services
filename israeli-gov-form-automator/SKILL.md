---
name: israeli-gov-form-automator
description: Automate Israeli government form filling via Playwright browser automation and PDF population. Prevents data-entry errors and rejected submissions on government portals. Use when user asks about filling government forms, "tofes" (form), "milui tfasim" (form filling), "gov.il" portal submissions, online form submission, Rashut HaMisim (Tax Authority) filings, Bituach Leumi (National Insurance) claims, or Rasham HaChevarot (Companies Registrar) documents. Validates Teudat Zehut (ID numbers) with check digit, Israeli phone numbers (+972), and Hebrew address fields. Supports Doch Shnati (annual tax report), maternity pay claims, and company registration forms. Do NOT use for deciding benefit or refund entitlement (use israeli-bituach-leumi or israeli-employee-tax-refund), explaining an official letter (use israeli-bureaucracy-decoder), arnona objections, or classified government systems.
license: MIT
allowed-tools: Bash(python:*) Bash(pip:*) WebFetch
compatibility: "Requires Python 3.9+, Playwright for browser automation, and network access to gov.il portals. Optional: pikepdf or pypdf for PDF form filling."
---

# Israeli Government Form Automator

## Legal notice

This is a free information tool operated by an AI model. It helps you organise and complete forms for government authorities. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by an advocate, tax adviser, or accountant. The output is not legal, tax, or other professional advice. An AI model may err, omit data, or present a wrong conclusion.

A form submitted to an authority is a document whose contents are your responsibility, and incorrect details in it can carry liability. Check every field before filing, and do not file a form whose contents you do not understand. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and all use of its output is the user's sole responsibility.


## Instructions

### Step 1: Identify the Form, Its Role, and the Portal

Before touching a browser, settle four questions: which form, who fills it, who receives it, and whether it needs filing at all. Many requests that sound like "fill form X" are really "ask someone else for form X" or "nothing to file, it is paid automatically".

**Who fills what (Tax Authority forms):**

| Form | What it is | Who fills it | Who receives it |
|------|-----------|--------------|-----------------|
| טופס 101 | Employee card and request for tax relief (כרטיס עובד) | The employee or pensioner | The employer or pension payer, never the Tax Authority |
| טופס 106 | Annual summary of the year's salary | Issued BY the employer | The employee. Never fill it yourself; ask the employer |
| טופס 119 | Tax benefit for completing an academic degree or vocational certificate | The graduate | Attached to the 101 given to the employer (who applies it in payroll), or claimed through online tax coordination |
| טופס 135 | Short annual return (דין וחשבון שנתי מקוצר), used to request a tax refund for previous years (up to 6 years) | The individual | Tax Authority |
| טופס 1301 | Annual return for individuals and business owners who are not a company | Obliged filers, including the self-employed | Tax Authority |
| טופס 857 | Annual certificate of tax withheld at source from payments for services or assets | Issued BY the payer to the supplier | The supplier, who uses it in the annual return |
| טופס 867 | Bank or financial-institution certificate of tax withheld on deposits and securities | Issued BY the bank | The account holder |
| טופס 161 | Employer notice of an employee's retirement or departure | The employer, via the new 161 (mandatory since 1 January 2024) | Tax Authority |

**Annual return: obligation or refund?** A salaried person with no filing obligation who wants money back for previous years (up to 6) files a refund request on Form 135; an obliged filer (for example a self-employed person) files 1301. Ask which applies before choosing a form. If the user does not know, route the question to `israeli-employee-tax-refund` or `israeli-tax-coordination` (benefit questions to `israeli-bituach-leumi`); this skill fills forms, it does not decide what to claim.

**Portals:**

| Portal | URL | Login system |
|--------|-----|--------------|
| gov.il services and form pages | https://www.gov.il | National identification for identified services |
| my.gov.il personal area | https://my.gov.il | National identification |
| Tax Authority department page | https://www.gov.il/he/departments/israel_tax_authority | Links to the personal area |
| Tax Authority personal area | https://secapp.taxes.gov.il/sr-ezor-ishi | The Tax Authority's OWN login, not national identification |
| Bituach Leumi personal service | https://ps.btl.gov.il | Bituach Leumi's OWN login (ID number + one-time code to the registered mobile) |
| Companies Registrar online (תאגידים ברשת) | https://ica.justice.gov.il/IcaSite | National identification (online company registration) |
| Interior Ministry | https://www.gov.il/he/departments/ministry_of_interior | National identification |

`www.misim.gov.il` is now only a redirect to the Tax Authority site; do not navigate to it as a portal. As of May 2025 the Tax Authority was not connected to national identification and announced "dual identification" by the end of 2026, so expect its login screen to change during 2026 and re-check before scripting it.

Clarify with the user:
- **Which form, which tax year?** Field layouts change every year
- **Online or PDF?** Download official PDFs only from the issuing body's own gov.il form page, never from a third-party site
- **Whose form is it?** See Step 2 before acting for anyone other than the user

### Step 2: Ground Rules for an Agent on a Government Portal

These are hard rules, not suggestions:

1. **Identified services are personal.** The gov.il terms of use state that using the identification system for identified services is personal, and that use by another person in the user's name breaches the terms and may in some circumstances be a criminal offence. The one exception is a family member (spouse, parent, child, sibling) acting with the user's consent. An agent filing for a non-family third party (an employer for an employee, an accountant for a client) must stop and route to that party's representative channel instead.
2. **Never receive, store, or type the user's password or one-time code.** Launch a visible browser (`headless=False`) and let the user log in themselves. The terms of use require the user to keep the password secret and not hand it to another.
3. **Never submit, sign, or pay without an explicit confirmation for THIS submission**, given after the user has seen the filled form (screenshot or the open browser window).
4. **Never tick a declaration box** ("I declare the details are correct") for the user, and never invent a value the user did not supply. Leave the field empty and ask.
5. **Never solve a CAPTCHA or pass it to a solving service.** Pause and hand control to the user.
6. **Do not keep personal data after the session.** Delete scraped pages, filled PDFs, and screenshots containing ID numbers, bank details, or medical documents once the user has saved what they need.

### Step 3: Validate Israeli-Specific Fields

Before filling any form, validate all Israeli-format data:

**Teudat Zehut (ID Number) Validation:**
The Israeli ID is 9 digits with a check digit (Luhn variant):
```python
import re

def validate_tz(id_number: str) -> bool:
    """Validate Israeli Teudat Zehut number."""
    id_str = id_number.strip().zfill(9)
    # ASCII digits only: str.isdigit() also accepts full-width digits
    if not re.fullmatch(r"[0-9]{9}", id_str):
        return False
    if id_str == "000000000":
        return False  # passes Luhn but is a placeholder, not a real ID
    total = 0
    for i, digit in enumerate(id_str):
        val = int(digit) * (1 + (i % 2))
        if val > 9:
            val -= 9
        total += val
    return total % 10 == 0
```

**Israeli Phone Number Formats** (Ministry of Communications numbering plan):

| Type | Pattern | Notes |
|------|---------|-------|
| Mobile | 05X-XXXXXXX (10 digits) | The bundled validator checks the 05X mobile format, not the carrier or whether the prefix is allocated; number portability means a prefix never identifies the current carrier |
| Geographic landline | 0A-NXX-XXXX (9 digits) | A is 2 (Jerusalem), 3 (Tel Aviv), 4 (Haifa and the north), 8 (Shfela and the south), 9 (Sharon); the local number's first digit N is 2-9 |
| National (07X) | 07P-NXX-XXXX (10 digits) | P is 2-9 (072 to 079); widely used by VoIP and cable landlines. A 9-digit validator wrongly rejects these |
| International | +972-5X-XXXXXXX | Drop leading 0, add +972 |

**Israeli Address Format:**
```
{street_name} {house_number}, {apartment} (optional)
{city_name}, {mikud (postal code - 7 digits)}
```

For mikud lookup use Israel Post: `https://mypost.israelpost.co.il/zipcodesearch`. The page is bot-protected and could not be machine-read on 2026-11-03, so open it in the user's own browser; if it does not load, use the mikud search on israelpost.co.il. Many identified services take the address from the population registry, so check what the portal already shows before typing a new one.

**Hebrew-only vs English-allowed fields:** Most Israeli government forms require Hebrew text. Exceptions where English (or Latin) input is allowed or required:

| Context | Allowed input |
|---------|---------------|
| Passport / foreign-citizen forms (names) | English (must match passport) |
| Company name proposals at רשם החברות | Hebrew primary, optional English transliteration |
| IBAN / bank account references | Latin characters (IL + digits) |
| Email and URLs | Latin |

When in doubt, mirror the casing and script of the user's official document (Teudat Zehut, passport, company certificate).

### Step 4: Set Up Browser Automation (Online Forms)

Install and configure Playwright for Hebrew RTL government portals:

```bash
pip install playwright
playwright install chromium
```

**Key patterns for gov.il portals:**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # the user logs in here, not the agent
    context = browser.new_context(locale="he-IL")
    page = context.new_page()
    page.goto("https://my.gov.il")

    # Pause until the user has logged in themselves (Step 2, rule 2).
    input("Log in in the browser window, then press Enter here...")

    # IMPORTANT: selectors are NOT stable across gov.il portals.
    # Do not assume [data-testid="form-container"]. Enumerate the DOM
    # first (page.content() or DevTools) and discover the actual
    # selector for each portal before relying on it.
    page.wait_for_selector("form, [role='main']", timeout=15000)

    # Fill RTL text fields
    page.fill('input[name="firstName"]', "ישראל")
    page.fill('input[name="lastName"]', "ישראלי")
    page.fill('input[name="idNumber"]', "123456782")

    # Handle date pickers (DD/MM/YYYY format in Israel)
    page.fill('input[name="birthDate"]', "15/03/1990")

    # Handle dropdowns with Hebrew options
    page.select_option('select[name="city"]', label="תל אביב-יפו")
```

### Step 5: Fill PDF Forms (Offline Forms)

For downloadable government PDFs with fillable fields, use pypdf (the maintained successor to PyPDF2, which is deprecated):

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("tofes_101.pdf")
fields = reader.get_fields()  # MANDATORY: enumerate before guessing names
print(list(fields))

writer = PdfWriter()
writer.append(reader)
writer.update_page_form_field_values(
    writer.pages[0],
    {"shem_prati": "ישראל", "shem_mishpacha": "ישראלי"}
)
writer.write("tofes_101_filled.pdf")  # without this nothing is saved
```

Always run `reader.get_fields()` first. Field names differ between form versions and between ministries, never assume a name from a previous run. pikepdf can inspect the same AcroForm at a lower level (`pdf.Root.AcroForm`), but pypdf is the path tested here.

**Hebrew values and appearance streams:** with pypdf 6.x, filling a field whose font lacks Hebrew glyphs prints "contains characters not supported by font encoding". The value itself is stored correctly and the writer sets NeedAppearances so the viewer redraws it, but the pre-drawn appearance can show garbage. Open the filled file in a real PDF viewer and check every Hebrew field visually before the user uploads it, and do not flatten the form.

**Common PDF field naming conventions in government forms:**

| Field Purpose | Transliteration | Pure English | Pure Hebrew |
|--------------|----------------|--------------|-------------|
| First name | shem_prati, shem_praty | first_name, firstName | שם_פרטי |
| Last name | shem_mishpacha, shem_mishpaha | last_name, lastName | שם_משפחה |
| ID number | mispar_zehut, tz | id_number, idNumber | מספר_זהות, ת״ז |
| Date of birth | taarich_leida | birth_date, dob | תאריך_לידה |
| Address | ktovet, rechov | address, street | כתובת, רחוב |
| City | yishuv, ir | city | יישוב, עיר |
| Phone | telefon, nayad | phone, mobile | טלפון, נייד |
| Employer | maasik | employer | מעסיק |

### Step 6: Handle Common Government Form Patterns

**Tofes 101 (employee card):**
The employee fills and signs it and hands it, with the supporting documents, to the employer or pension payer: within 7 days of starting work or of the first salary (whichever is earlier), at the start of every tax year (1 January), and within 7 days of any change in details. Pensioners aged 70 and over and recipients of various allowances may be exempt from refiling every year if their income did not change; check the Tax Authority conditions before telling them to refile. A degree or vocational-certificate benefit (Form 119) is attached to this 101. The employee declares facts (children, residence, studies, other income); the employer's payroll converts them into credit points, so do not type a credit-point number into a 101.
An electronic 101 is PERMITTED, not mandatory: Tax Authority rules let an employer produce 101 electronically, as a substitute for the manual form, through an approved system. The gov.il page `https://www.gov.il/he/service/itc-application-for-electronic-101` is for software houses and employers seeking that system approval, not a filing route for employees.

**Annual return (1301 or 135):**
The gov.il 2025 annual-return page offers full online submission from 2019 onward, and allows manual (paper) submission for those above retirement age, those with low income, and those not obliged to file who are requesting a refund.

Deadlines for tax year 2025: obliged filers of a non-online return by 29.5.2026, obliged online filers by 30.6.2026. These have passed; an obliged filer who missed them still files now, and the agent re-checks the gov.il page for the next tax year's dates. Those exempt from online filing can submit the page's PDF forms through the public-inquiries system (מערכת פניות הציבור).

1. Log in to the Tax Authority personal area (the user logs in; see Step 2)
2. Required data: income sources (mekorot hachnasa), deductions (nikuyim), credits (zikuyim)
3. Keep 106, 857, and 867 to hand; their figures are typed into the return's fields, with uploads where the system asks for them
4. Date format: always DD/MM/YYYY

**Bituach Leumi claims:**
1. **First check whether a claim is needed at all.** Except after a home birth, maternity pay (דמי לידה) is paid automatically, with no claim, to a self-employed mother, to an employee whose employer has an arrangement with Bituach Leumi and files for her, to a woman who received the pregnancy-preservation benefit up to the birth, and to one who received unemployment pay up to a month before the birth. A home birth always needs a claim. The claim must be filed no later than 12 months from the first day of entitlement, and the online form can be filled only after the birth. Each employer confirms, inside the form, her months of work and salary for the 10 months before she stopped working (one form per employer).
2. Log in to the Bituach Leumi personal service (ps.btl.gov.il); this is Bituach Leumi's own login, not national identification
3. Identify the claim type and the documents that type requires, from the claim form itself
4. Track the claim in the personal area

**Companies Registrar filings:**
1. Online company registration ("רישום חברה בקליק") runs on תאגידים ברשת, entered through national identification; the articles and the shareholders' and directors' declarations are then approved online by each party, with no lawyer-verified scans
2. Prepare more than one Hebrew name proposal: the Registrar's 2017 online-registration manual (smart-card route) required three in order of priority, and the current click-service guide does not state a number, so follow what the form asks
3. Fees (2026 Corporations Authority table): online registration NIS 2,559 (reduced), regular registration NIS 3,123; there is also an annual fee every year after registration, so tell the owner
4. For the annual report and director or shareholder changes, check the Corporations Authority service page for the current filing route

### Step 7: Common Rejection Reasons

Audit the filled form against these before submitting:

| Problem | Fix |
|---------|-----|
| Teudat Zehut has leading zero stripped (e.g., 12345678 instead of 012345678) | Re-pad to 9 digits with leading zeros |
| Mikud does not match the street and city | Re-check in the Israel Post lookup |
| Hebrew name spelling does not match Misrad HaPnim records | Use the exact spelling from the user's Teudat Zehut |
| Form for the wrong tax year (for example a previous year's 101 or return) | Download the current year's form from the issuing body's page |
| Signature placed on the wrong page or in the wrong field | Re-check the signature placement before upload |
| Upload in the wrong format or unreadable | Check the formats and size the upload screen states |

### Step 8: Identification and Signatures

Logging in and signing are different things.

**Logging in (identification):**
- **National identification (gov.il, my.gov.il, Companies Registrar online registration):** ID number, the chosen password, and a one-time code sent each time by SMS or voice call. Since May 2025 the user can also log in on a mobile phone with the phone's biometrics, with no password and no code (passkey). A biometric ID card is one of the ways to register, at a station with a card reader.
- **Tax Authority personal area:** its own login system (see Step 1).
- **Bituach Leumi:** its own system; a registered user logs in with ID number and a secret code sent to the mobile number on record.

**Signing:** gov.il forms that take a certificate-based electronic signature use a smart card or token holding a certificate from an authorised certification authority (in Israel: Comsign and PersonalID), plus a card reader and signing software. Online company registration is different: the filer enters through national identification, and each shareholder and director then approves (signs) online from an email link; check the approval screen for how they identify. When a form asks for a signature, agents cannot provide it: the user completes any signing step interactively.

### Step 9: Submit and Verify

After filling the form:
1. **Screenshot before submit** and get the user's explicit go-ahead (Step 2, rule 3)
2. **Validate all required fields**, government forms reject partial submissions
3. **Save the confirmation number** (mispar ishur) shown after submission
4. **Download the receipt PDF** when available
5. **Note where to track status**: the personal area of the same portal

### Step 10: Error Recovery

- **Automation is not working, or the user has no login**: fall back to the human routes, such as the public-inquiries system for paper tax returns, or the agency's service centre
- **Session timeout**: portals log the user out after inactivity, and the limit varies by portal. Save progress where the portal allows it and hand login back to the user
- **CAPTCHA**: pause and hand control to the user (Step 2, rule 5)
- **Login screen changed**: identification systems are changing during 2026; re-enumerate the page rather than replaying an old script
- **Peak load**: the Tax Authority site is slower around annual-return deadlines

## Examples

### Example 1: Fill Tofes 101 at a New Job
User says: "I started a new job and HR asked me for a Tofes 101"
Actions:
1. Confirm the user is the employee (the 101 is theirs to fill) and which tax year
2. Ask whether the employer uses an electronic 101 system; if so the user fills it there. Otherwise download the current year's 101 from the Tax Authority form page
3. Validate the Teudat Zehut, then fill personal details and the factual declarations (children, residence, studies, other employer); no credit-point number
4. Save the filled PDF, have the user check every Hebrew field visually, sign, and hand it to the employer within 7 days, with the ID and its appendix
Result: A filled 101 ready for the user's signature, plus a note that a second employer may need tax coordination (route to `israeli-tax-coordination`)

### Example 2: Bituach Leumi Maternity Pay
User says: "Help me file a maternity benefit claim with Bituach Leumi"
Actions:
1. Ask whether the birth was at home (then a claim is always needed), and otherwise whether she is self-employed, whether her employer files for her, whether she received pregnancy-preservation benefit up to the birth, or unemployment pay up to a month before the birth; if any applies, payment is automatic and nothing needs filing
2. Otherwise, after the birth, the user logs in to ps.btl.gov.il herself
3. Fill the claim form with her details; each employer confirms its own section (work months and salary for the 10 months before she stopped working); validate the IBAN of the account the form asks for; file within 12 months of entitlement
4. Upload only the documents the form asks for, then screenshot and get her confirmation before submitting
Result: Either "no claim needed, payment is automatic", or a submitted claim with a confirmation number

### Example 3: Register a New Company Online
User says: "I want to register a new Chevra Ba'am (Ltd company)"
Actions:
1. The user enters תאגידים ברשת (https://ica.justice.gov.il/IcaSite) through national identification
2. Prepare Hebrew name proposals in priority order (see Step 6)
3. Enter founder, director, and share details; each shareholder and director then approves online from their own email link
4. Note the 2026 online registration fee (NIS 2,559) and the recurring annual fee
Result: Submitted registration awaiting every party's online approval

### Example 4: Update Personal Details at Misrad HaPnim
User says: "I moved apartments and need to update my address"
Actions:
1. The user opens the gov.il address-change service and logs in with national identification
2. Validate the new address format (street, city, mikud via Israel Post lookup)
3. Fill the change-of-address form; screenshot and confirm with the user
4. Submit and save the confirmation; remind the user that other bodies (for example the municipality) may need their own update
Result: Address change request submitted with confirmation number

## Bundled Resources

### Scripts
- `scripts/fill_form.py`, validates Israeli form fields (Teudat Zehut, phone per the numbering plan, address, IBAN) and prints field templates for common forms, marking which forms the user fills and which are issued by someone else. Run: `python scripts/fill_form.py --help`

### References
- `references/gov-portals.md`, Israeli government portal URLs, login systems, form roles, and field formats. Consult when identifying the correct portal or form for a given task.

## Gotchas
- Agents treat every form as something the user fills. 106, 857, and 867 are issued by the employer, payer, or bank; an agent that "fills" one is fabricating someone else's figures.
- Agents route a self-employed person to Form 135 or a refund seeker to 1301. Settle "obliged to file or requesting a refund" first.
- Agents assume the Tax Authority and Bituach Leumi use the gov.il login. Both run their own identification systems.
- Teudat Zehut numbers have 9 digits with a Luhn-variant check digit. Agents may generate random 9-digit numbers that fail the check, and `000000000` passes Luhn but is a placeholder, not a real ID.
- Selectors on gov.il portals are not stable across services. Never reuse a selector from a previous portal, enumerate the DOM first.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| gov.il terms of use | https://www.gov.il/he/pages/terms_of_use | Identified services are personal; password secrecy |
| Annual return 2025 (1301, 135) | https://www.gov.il/he/service/reporting-and-payment-2025-annual-tax-report-for-individuals | Online and manual filing routes, current forms |
| Kol Zchut, Form 101 | https://www.kolzchut.org.il/he/%D7%98%D7%95%D7%A4%D7%A1_101 | Who fills it, deadlines, attachments |
| Kol Zchut, maternity pay | https://www.kolzchut.org.il/he/%D7%93%D7%9E%D7%99_%D7%9C%D7%99%D7%93%D7%94 | Automatic payment cases, online claim |
| Tax Authority | https://www.gov.il/he/departments/israel_tax_authority | Personal-area link, forms |
| Company registration online | https://www.gov.il/he/service/registration-online | רישום חברה בקליק |
| Digital signature procedure | https://www.gov.il/he/pages/digital_signature | Smart card or token signing |
| Numbering plan (Ministry of Communications) | https://www.gov.il/BlobFolder/policy/number_policy/en/The_numbering_plan-02-2023.pdf | Phone number formats |
| Playwright docs | https://playwright.dev | RTL context, form automation, waits |

## Troubleshooting

### Error: "Session expired" on gov.il
Cause: Government portal sessions time out after inactivity (no published limit; it varies by portal)
Solution: Hand login back to the user and resume from the last saved step.

### Error: "Invalid Teudat Zehut"
Cause: ID number fails check digit validation, or is a placeholder like `000000000`
Solution: Run `validate_tz()` before submission. Ensure 9 digits with leading zeros if needed.

### Error: "Hebrew text displays incorrectly in PDF"
Cause: The field's font has no Hebrew glyphs, so the appearance pypdf draws is wrong even though the stored value is right (verified with pypdf 6.12 on a test form)
Solution: Open the file in a PDF viewer, which redraws fields from the stored value; check visually; do not flatten. Prefer the official form, whose fields usually carry a Hebrew font.

### Error: "Form field not found"
Cause: Government PDFs change field names between versions
Solution: List all fields with `reader.get_fields()` first, then match by inspecting field labels.

### Error: phone number rejected by the validator
Cause: Before v1.3.0 the bundled validator accepted only 9-digit landlines, so every 10-digit 07X number failed
Solution: Use the current script; 07X numbers are 10 digits under the numbering plan.
