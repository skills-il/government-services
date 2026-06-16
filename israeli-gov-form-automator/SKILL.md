---
name: israeli-gov-form-automator
description: Automate Israeli government form filling via Playwright browser automation and PDF population. Prevents hours of manual form filling and data entry errors on government portals. Use when user asks about filling government forms, "tofes" (form), "milui tfasim" (form filling), "gov.il" portal submissions, online form submission, Rashut HaMisim (Tax Authority) filings, Bituach Leumi (National Insurance) claims, or Rasham HaChevarot (Companies Registrar) documents. Validates Teudat Zehut (ID numbers) with check digit, Israeli phone numbers (+972), and Hebrew address fields. Supports Doch Shnati (annual tax report), maternity grant claims, and company registration forms. Do NOT use for classified or security-clearance government systems.
license: MIT
allowed-tools: Bash(python:*) Bash(pip:*) WebFetch
compatibility: "Requires Python 3.9+, Playwright for browser automation, and network access to gov.il portals. Optional: pikepdf or pypdf for PDF form filling."
---

# Israeli Government Form Automator

## Instructions

### Step 1: Identify the Form and Portal

Ask the user which government form or process they need to automate:

| Portal | URL | Common Forms | Hebrew |
|--------|-----|-------------|--------|
| my.gov.il Personal Area (primary 2026 entry) | https://my.gov.il | All authenticated personal services | האזור האישי |
| gov.il Services | https://www.gov.il | General government forms | שירותי ממשלה |
| Rashut HaMisim (Tax Authority) | https://www.misim.gov.il | Doch Shnati, Mas Hachnasa, Nikui Mas | רשות המסים |
| Tax Authority Self-Service (SHAAM) | https://secapp.taxes.gov.il/srsherutatzmi | Personal tax area | שירות עצמי |
| Bituach Leumi (National Insurance) | https://www.btl.gov.il | Maternity, disability, unemployment claims | ביטוח לאומי |
| Rasham HaChevarot (Companies Registrar) | https://ica.justice.gov.il | Company registration, annual reports | רשם החברות |
| Misrad HaPnim (Interior Ministry) | https://www.gov.il/he/departments/ministry_of_interior | Teudat Zehut updates, address changes | משרד הפנים |

Note: `my.gov.il` is the primary 2026 entry point for individual users. Deeper service-specific flows still live on the dedicated portals above.

Clarify:
- **Which form?** (form number or name, e.g., Tofes 101, Tofes 106)
- **Online or PDF?** (browser-based portal or downloadable PDF)
- **User data available?** (Teudat Zehut, address, employer details)

### Step 2: Validate Israeli-Specific Fields

Before filling any form, validate all Israeli-format data:

**Teudat Zehut (ID Number) Validation:**
The Israeli ID is 9 digits with a check digit (Luhn variant):
```python
def validate_tz(id_number: str) -> bool:
    """Validate Israeli Teudat Zehut number."""
    id_str = id_number.zfill(9)
    if len(id_str) != 9 or not id_str.isdigit():
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

**Israeli Phone Number Formats:**
| Format | Example | Notes |
|--------|---------|-------|
| Mobile | 05X-XXXXXXX | Currently-allocated prefixes: 050, 051, 052, 053, 054, 055, 058 (plus some 059 MVNO blocks). The bundled validator checks 05X mobile format, not the carrier; number portability means a prefix never identifies the current carrier, and the allocated set shifts over time (057 was retired in 2014; 056 is a Palestinian-territories prefix) |
| Landline | 0X-XXXXXXX | Area codes: 02 (Jerusalem), 03 (Tel Aviv), 04 (Haifa), 08 (South), 09 (Sharon) |
| International | +972-5X-XXXXXXX | Drop leading 0, add +972 |

**Israeli Address Format:**
```
{street_name} {house_number}, {apartment} (optional)
{city_name}, {mikud (postal code - 7 digits)}
```

For authoritative mikud lookup use Israel Post: `https://mypost.israelpost.co.il/zipcodesearch`. Always verify mikud matches the city before submitting, mismatches are a top rejection reason.

**Hebrew-only vs English-allowed fields:** Most Israeli government forms require Hebrew text. Exceptions where English (or Latin) input is allowed or required:

| Context | Allowed input |
|---------|---------------|
| Passport / foreign-citizen forms (names) | English (must match passport) |
| Company name proposals at רשם החברות | Hebrew primary, optional English transliteration |
| IBAN / bank account references | Latin characters (IL + digits) |
| Email and URLs | Latin |

When in doubt, mirror the casing and script of the user's official document (Teudat Zehut, passport, company certificate).

### Step 3: Set Up Browser Automation (Online Forms)

Install and configure Playwright for Hebrew RTL government portals:

```bash
pip install playwright
playwright install chromium
```

**Key patterns for gov.il portals:**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(locale="he-IL")
    page = context.new_page()
    # Note: Replace with specific service URL as needed
    page.goto("https://www.gov.il/he/")

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

### Step 4: Fill PDF Forms (Offline Forms)

For downloadable government PDFs with fillable fields:

```python
# Option 1: pikepdf (recommended)
import pikepdf

pdf = pikepdf.open("tofes_101.pdf")
pdf.pages[0]["/Annots"]  # Inspect form field names

# Option 2: pypdf (the maintained successor to PyPDF2, which is deprecated)
from pypdf import PdfReader, PdfWriter

reader = PdfReader("tofes_101.pdf")
fields = reader.get_fields()  # MANDATORY: enumerate before guessing names
writer = PdfWriter()
writer.append(reader)
writer.update_page_form_field_values(
    writer.pages[0],
    {"shem_prati": "ישראל", "shem_mishpacha": "ישראלי"}
)
```

Always run `reader.get_fields()` first. Field names differ between form versions and between ministries, never assume a name from a previous run.

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

### Step 5: Handle Common Government Form Patterns

**Tofes 101 (Employee Tax Coordination):**
Since 2022 the form is mandated digital via employer payroll systems and the רשות המסים digital approval flow (טופס 101 מקוון). PDF flow exists but is a legacy fallback. Digital flow: `https://www.gov.il/he/service/itc-application-for-electronic-101`.

**Tofes 1301 / Doch Shnati (Individual Annual Tax Return):**
Online submission is mandatory since 2019 for most filers. Paper submission is allowed only for retirees and certain below-threshold filers. Source: kolzchut "הגשת דוח שנתי למס הכנסה".

1. Navigate to Rashut HaMisim personal area
2. Required fields: income sources (mekorot hachnasa), deductions (nikuyim), credits (zikuyim)
3. Attach digital slips (tofes 106, tofes 857)
4. Date format: always DD/MM/YYYY

**Bituach Leumi Claims:**
1. Navigate to btl.gov.il personal area
2. Identify claim type (maternity/dme'i leida, disability/nechut, unemployment/avtala)
3. Upload supporting documents (medical certificates, employment letters)
4. Track claim status via personal dashboard

**Companies Registrar Filings:**
1. Navigate to https://ica.justice.gov.il
2. Required: company number (mispar chevra), authorized signatory details
3. Annual report (doch shnati la-rasham) filing
4. Director/shareholder change notifications

### Step 6: Common Rejection Reasons

Audit the filled form against these common rejection causes before submitting:

| Rejection cause | Fix |
|-----------------|-----|
| Teudat Zehut has leading zero stripped (e.g., 12345678 instead of 012345678) | Re-pad to 9 digits with leading zeros |
| Mikud does not match city | Re-verify via Israel Post lookup |
| Hebrew name spelling does not match Misrad HaPnim records | Use the exact spelling from the user's Teudat Zehut booklet |
| Wrong year on Tofes 106 (using current calendar year instead of tax year) | Confirm the tax year the report covers |
| Signature placed on the wrong page or in the wrong field | Re-check the signature placement before upload |
| Photo / scan upload wrong format or resolution | Verify allowed formats (PDF/JPG) and minimum DPI |

### Step 7: Digital Signatures (2026 landscape)

Three accepted methods on Israeli government portals:

1. **כרטיס חכם (smart card)** issued by Comsign or PersonalID. Required for advanced misim.gov.il flows and some Companies Registrar submissions.
2. **תעודת זהות ביומטרית + סיסמה** (biometric ID + password). Primary authentication for `my.gov.il` and the gov.il personal area.
3. **חתימה דיגיטלית מאומתת** (verified digital signature) per the National Digital Agency standard.

Agents cannot programmatically sign forms, the user must complete the signing step interactively. Sources: `https://www.govextra.gov.il/national-digital-agency/signature/home/`, `https://www.gov.il/he/pages/digital_signature`.

### Step 8: Submit and Verify

After filling the form:
1. **Screenshot before submit**, capture the filled form for user review
2. **Validate all required fields**, government forms reject partial submissions
3. **Save confirmation number** (mispar ishur), always displayed after successful submission
4. **Download receipt PDF** when available
5. **Note processing timeline**, most government services specify expected response time

### Step 9: Error Recovery

Common issues with government portals:
- **Session timeout**: Gov.il sessions expire after approximately 20 minutes of inactivity
- **CAPTCHA**: Some forms require manual CAPTCHA solving; pause and ask user
- **Certificate errors**: Government portals may use Israeli CA certificates
- **Peak hours**: Tax Authority portal is slow during filing season (March-May)

## Examples

### Example 1: Fill Tax Form 101
User says: "I need to fill Tofes 101 for my new employee"
Actions:
1. Check whether the employer is on a payroll system that supports the digital Tofes 101 approval flow (preferred since 2022). Fall back to PDF only if not.
2. Validate employee Teudat Zehut
3. Fill personal details, tax bracket, credits (nekudot zikui)
4. Generate filled PDF for employer signature (legacy fallback only)
Result: Completed Tofes 101 ready for digital approval or PDF submission

### Example 2: Submit Bituach Leumi Maternity Claim
User says: "Help me file a maternity benefit claim with Bituach Leumi"
Actions:
1. Navigate to btl.gov.il maternity (dme'i leida) section
2. Validate eligibility: employment period, salary data
3. Fill claim form with personal and employer details, validate IBAN for the refund account
4. Upload required documents (employment confirmation, hospital discharge)
Result: Submitted claim with tracking number for follow-up

### Example 3: Register New Company
User says: "I want to register a new Chevra Ba'am (Ltd company)"
Actions:
1. Navigate to Companies Registrar portal (https://ica.justice.gov.il)
2. Fill company name proposals (3 options required)
3. Enter founder details, share capital, articles of association
4. Calculate and note registration fees
Result: Submission confirmation with expected registration timeline

### Example 4: Update Personal Details at Misrad HaPnim
User says: "I moved apartments and need to update my address"
Actions:
1. Navigate to gov.il address change service
2. Validate new address format (street, city, mikud via Israel Post lookup)
3. Fill change-of-address form with old and new addresses
4. Submit with required identification
Result: Address change request submitted with confirmation number

## Bundled Resources

### Scripts
- `scripts/fill_form.py`, helper to validate Israeli form fields (Teudat Zehut, phone, address, IBAN) and populate common government form data structures. Run: `python scripts/fill_form.py --help`

### References
- `references/gov-portals.md`, comprehensive list of Israeli government portal URLs, form types, and field naming conventions. Consult when identifying the correct portal or form for a given task.

## Gotchas
- Israeli government forms require Hebrew text input in specific fields. Agents may generate English-only form data, which will be rejected by government systems.
- Teudat Zehut (Israeli ID) numbers have 9 digits with a Luhn-variant check digit. Agents may generate random 9-digit numbers that fail the check-digit validation, and `000000000` passes Luhn but is a placeholder, not a real ID.
- Many government forms require a date of birth in both Hebrew calendar (luach ivri) and Gregorian formats. Agents typically only provide the Gregorian date.
- Digital signatures on Israeli government forms use the gov.il identity verification system. Agents cannot programmatically sign forms without going through the user's gov.il authentication.
- Selectors on gov.il portals are not stable across services. Never reuse a selector from a previous portal, enumerate the DOM first.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| my.gov.il personal area | https://my.gov.il | Primary 2026 entry point |
| Gov.il main portal | https://www.gov.il | Form listings, service index, authentication entry |
| Israel Tax Authority services | https://www.gov.il/he/departments/israel_tax_authority | Tax forms, online submission portals |
| Tax Authority self-service (SHAAM) | https://secapp.taxes.gov.il/srsherutatzmi | Personal tax area |
| Bituach Leumi (NII) | https://www.btl.gov.il | NII forms, claim submission, personal account |
| Companies Registrar (ICA) | https://ica.justice.gov.il | Company filings and updates |
| National Digital Agency, signatures | https://www.govextra.gov.il/national-digital-agency/signature/home/ | Approved digital-signature methods |
| Digital signature policy | https://www.gov.il/he/pages/digital_signature | National standard |
| Israel Post mikud lookup | https://mypost.israelpost.co.il/zipcodesearch | Authoritative postal-code source |
| Playwright docs | https://playwright.dev | RTL context, form automation, waits |

## Troubleshooting

### Error: "Session expired" on gov.il
Cause: Government portal sessions time out after prolonged inactivity
Solution: Re-authenticate and resume from the last saved step. Save partial progress frequently.

### Error: "Invalid Teudat Zehut"
Cause: ID number fails check digit validation, or is a placeholder like `000000000`
Solution: Run `validate_tz()` before submission. Ensure 9 digits with leading zeros if needed.

### Error: "Hebrew text displays incorrectly in PDF"
Cause: PDF library does not support RTL text or Hebrew fonts
Solution: Use pikepdf with embedded Hebrew fonts. Ensure the PDF template already has Hebrew font resources.

### Error: "Form field not found"
Cause: Government PDFs change field names between versions
Solution: List all fields with `reader.get_fields()` first, then match by inspecting field labels.
