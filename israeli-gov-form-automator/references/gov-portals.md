# Israeli Government Portals Reference

## Main Government Portals

| Portal | URL | Description | Login system |
|--------|-----|-------------|--------------|
| my.gov.il (Personal Area) | https://my.gov.il | Personal area for services on national identification | National identification |
| gov.il (Central) | https://www.gov.il | Unified government services and form pages | National identification for identified services |
| Tax Authority department page | https://www.gov.il/he/departments/israel_tax_authority | Forms, guides, link to the personal area | None needed to read |
| Tax Authority personal area | https://secapp.taxes.gov.il/sr-ezor-ishi | Annual return, tax coordination, refunds | The Tax Authority's own login (not national identification as of May 2025) |
| Bituach Leumi personal service | https://ps.btl.gov.il | Claims, documents, status | Bituach Leumi's own login: ID number + one-time code to the registered mobile |
| Companies Registrar online (תאגידים ברשת) | https://ica.justice.gov.il/IcaSite | Online company registration ("רישום חברה בקליק") | National identification (online company registration) |
| Misrad HaPnim (Interior Ministry) | https://www.gov.il/he/departments/ministry_of_interior | Population registry, ID services | National identification |
| Rashut HaTaagidim (Corporations Authority) | https://www.gov.il/he/departments/israeli_corporations_authority | Companies, non-profits, fees | National identification |
| Israel Post Mikud Lookup | https://mypost.israelpost.co.il/zipcodesearch | Postal-code lookup (bot-protected, open in a real browser) | None |

`www.misim.gov.il` now only redirects to the Tax Authority site. The bare `ica.justice.gov.il` root is not the online-services entry; use `/IcaSite`.

## Common Government Forms

### Tax Authority (Rashut HaMisim) Forms

| Form | Hebrew Name | Purpose | Who fills it |
|------|-------------|---------|--------------|
| Tofes 101 | טופס 101 | Employee card and request for tax relief | Employee, handed to the employer or pension payer |
| Tofes 106 | טופס 106 | Annual salary summary | Issued by the employer to the employee |
| Tofes 119 | טופס 119 | Tax benefit for completing an academic degree or vocational certificate | The graduate; attached to the 101 given to the employer, or via online tax coordination |
| Tofes 135 | טופס 135 | Short annual return, used to request a refund for previous years (up to 6 years) | The individual |
| Tofes 1301 | טופס 1301 | Annual return for individuals and business owners who are not a company | Obliged filers, including the self-employed |
| Tofes 857 | טופס 857 | Annual certificate of tax withheld at source from payments for services or assets | Issued by the payer to the supplier |
| Tofes 867 | טופס 867 | Bank certificate of tax withheld on deposits and securities | Issued by the bank |
| Tofes 161 | טופס 161 | Employer notice of an employee's retirement or departure (new 161 mandatory since 1 January 2024) | The employer |

Tofes 101 electronic: Tax Authority rules PERMIT an employer to produce 101 electronically through an approved system, as a substitute for the manual form; it is not mandatory. `https://www.gov.il/he/service/itc-application-for-electronic-101` is the approval route for software houses and employers building such a system, not a filing route for employees.

Annual return: the gov.il 2025 annual-return page offers full online submission from 2019 onward, and allows manual submission for those above retirement age, those with low income, and those not obliged to file who request a refund. Tax year 2025 deadlines: non-online obliged filers by 29.5.2026, online obliged filers by 30.6.2026 (both passed; a late obliged filer still files, and the next year's dates are on the same gov.il page).

### Bituach Leumi (National Insurance) Forms

Claim types the user may ask to fill (check the claim form itself for the route and the documents it requires):

| Claim | Hebrew Name | Purpose |
|-------|-------------|---------|
| Dmei Leida | דמי לידה | Maternity pay (often automatic, see SKILL.md Step 6) |
| Nechut | נכות | Disability claim |
| Avtala | אבטלה | Unemployment benefit claim |
| Pgia BaAvoda | פגיעה בעבודה | Work injury claim |
| Kitzba LZikna | קצבת זקנה | Old age pension claim |

Ordinary sick pay (דמי מחלה) is paid by the employer, not claimed from Bituach Leumi.

### Companies Registrar Forms

| Form | Hebrew Name | Purpose |
|------|-------------|---------|
| Rishum Chevra | רישום חברה | New company registration (online "רישום חברה בקליק" through national identification) |
| Doch Shnati LaRasham | דוח שנתי לרשם | Annual company report |
| Shinui Direktorim | שינוי דירקטורים | Director change notification |
| Shinui Baalei Mniayot | שינוי בעלי מניות | Shareholder change |
| Piruq Chevra | פירוק חברה | Company dissolution |

For filings other than registration, check the Corporations Authority service page for the current filing route.

## Authentication Methods

### National identification (gov.il, my.gov.il, Companies Registrar online registration)
- Login: ID number, the chosen password, and a one-time code sent each time by SMS or voice call
- Since May 2025: passwordless login on a mobile phone with the phone's biometrics (passkey)
- A biometric ID card is one way to register, at a station with a card reader
- Identified services are personal under the gov.il terms of use (family members acting with consent excepted)

### Tax Authority personal area
- URL: https://secapp.taxes.gov.il/sr-ezor-ishi
- Its own identification system; as of May 2025 not connected to national identification, with "dual identification" planned by the end of 2026

### Bituach Leumi personal service
- URL: https://ps.btl.gov.il
- Its own identification system: ID number + secret code sent to the mobile number on record

### Electronic signatures
- gov.il forms that take an electronic signature use a smart card or token holding a certificate from an authorised certification authority (in Israel: Comsign and PersonalID), plus a card reader and signing software
- Logging in is not signing. When a form asks for a signature, the user performs it. In online company registration the filer enters through national identification and each shareholder and director then approves online from an email link
- Source: https://www.gov.il/he/pages/digital_signature

## Date and Number Formats

| Field | Format | Example |
|-------|--------|---------|
| Date | DD/MM/YYYY | 15/03/2024 |
| Teudat Zehut | 9 digits (with leading zeros) | 012345678 |
| Phone (mobile) | 05X-XXXXXXX (10 digits) | 052-1234567 |
| Phone (geographic landline) | 0A-NXX-XXXX (9 digits, A = 2/3/4/8/9, N = 2-9) | 03-6123456 |
| Phone (national 07X) | 07P-NXX-XXXX (10 digits, P = 2-9) | 077-2345678 |
| Mikud (postal code) | 7 digits | 6100000 |
| IBAN (Israeli) | IL + 2 check + 3 bank + 3 branch + 13 account = 23 chars | IL620108000000099999999 |

For mikud lookup use Israel Post: `https://mypost.israelpost.co.il/zipcodesearch`.

## Browser Automation Notes

### General Tips
- Government sites use Hebrew (RTL), set locale to `he-IL`
- Many forms are React/Angular SPAs, wait for dynamic content
- File uploads often require specific formats (PDF, JPG) and size limits
- Digital signatures may be required for some submissions; the user performs them

### Common Selectors
- Gov.il forms typically use various data attributes, NOT a stable `data-testid="form-container"`. Enumerate the DOM (`page.content()` or DevTools) before assuming any selector.
- Tax Authority uses custom form components
- Bituach Leumi uses standard HTML forms with Hebrew labels

### Pace and presence
- No official rate limits published. The user stays present for the whole personal-area session (login, CAPTCHA, final confirmation)
- Expect slower responses around annual-return deadlines
