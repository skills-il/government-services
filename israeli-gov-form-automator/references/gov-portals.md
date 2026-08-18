# Israeli Government Portals Reference

## Main Government Portals

| Portal | URL | Description | Authentication |
|--------|-----|-------------|----------------|
| my.gov.il (Personal Area) | https://my.gov.il | Primary 2026 entry point for personal government services | gov.il account |
| gov.il (Central) | https://www.gov.il | Unified government services portal | gov.il account |
| Rashut HaMisim (Tax Authority) | https://www.misim.gov.il | Income tax, VAT, purchase tax | Personal area login |
| Tax Authority Self-Service (SHAAM) | https://secapp.taxes.gov.il/srsherutatzmi | Tax personal area self-service | Teudat Zehut + password / smart card |
| Bituach Leumi (National Insurance) | https://www.btl.gov.il | Social security benefits and claims | Personal area login |
| Rasham HaChevarot (Companies Registrar) | https://ica.justice.gov.il | Company registration and filings | Digital certificate |
| Misrad HaPnim (Interior Ministry) | https://www.gov.il/he/departments/ministry_of_interior | Population registry, ID services | gov.il account |
| Rashut HaTaagidim (Corporations Authority) | https://www.gov.il/he/departments/corporations_authority | Non-profit organizations | gov.il account |
| Israel Post Mikud Lookup | https://mypost.israelpost.co.il/zipcodesearch | Authoritative postal-code lookup | None |

Note: `my.gov.il` is the unified personal area introduced and rolled out by the National Digital Agency. Treat it as the default landing page when a user says "I want to log in to gov.il". Specific service portals (misim, btl, ica) still exist for deeper flows.

## Common Government Forms

### Tax Authority (Rashut HaMisim) Forms

| Form | Hebrew Name | Purpose | Filing Method |
|------|-------------|---------|---------------|
| Tofes 101 | טופס 101 | Employee tax coordination | Digital (mandated since 2022) / PDF fallback |
| Tofes 106 | טופס 106 | Annual salary report (employer) | Online |
| Tofes 135 | טופס 135 | Self-employed annual report | Online |
| Tofes 1301 | טופס 1301 | Individual annual tax return (Doch Shnati) | Online mandatory since 2019 for most filers (paper only for retirees / certain below-threshold filers) |
| Tofes 857 | טופס 857 | Pension fund annual report | PDF |
| Tofes 119 | טופס 119 | Tax credit request | Online |
| Tofes 161 | טופס 161 | Severance pay tax approval | PDF / Online |

Tofes 101 (digital): see `https://www.gov.il/he/service/itc-application-for-electronic-101` for the digital approval flow via employer payroll systems. PDF instructions remain as the legacy fallback.

Tofes 1301 (online mandatory): per kolzchut "הגשת דוח שנתי למס הכנסה", online submission is mandatory for most individual filers since 2019. Paper filing is allowed only for retirees (retirement age) and certain below-threshold filers; the exact income threshold is set annually, so check the current figure on the kolzchut page or the ITA annual-return instructions before relying on it.

### Bituach Leumi (National Insurance) Forms

| Form | Hebrew Name | Purpose | Filing Method |
|------|-------------|---------|---------------|
| Dmei Leida | דמי לידה | Maternity benefit claim | Online |
| Nechut | נכות | Disability claim | Online |
| Avtala | אבטלה | Unemployment benefit claim | Online |
| Pgia BaAvoda | פגיעה בעבודה | Work injury claim | Online |
| Kitzba LZikna | קצבת זקנה | Old age pension claim | Online |
| Dmei Makhala | דמי מחלה | Sick pay claim | Online |

### Companies Registrar Forms

| Form | Hebrew Name | Purpose | Filing Method |
|------|-------------|---------|---------------|
| Rishum Chevra | רישום חברה | New company registration | Online |
| Doch Shnati LaRasham | דוח שנתי לרשם | Annual company report | Online |
| Shinui Direktorim | שינוי דירקטורים | Director change notification | Online |
| Shinui Baalei Mniayot | שינוי בעלי מניות | Shareholder change | Online |
| Piruq Chevra | פירוק חברה | Company dissolution | Online / PDF |

## Authentication Methods

### gov.il Account
- Registration: https://www.gov.il/he/service/register-to-digital-services
- Methods: SMS OTP, biometric ID, digital certificate
- Session duration: approximately 20 minutes inactive timeout

### Tax Authority Personal Area (SHAAM)
- URL: https://secapp.taxes.gov.il/srsherutatzmi
- Known as SHAAM (sheirut atsmi me'ukav)
- Requires: Teudat Zehut + password, or smart-card digital signature

### Bituach Leumi Personal Area
- URL: https://www.btl.gov.il/benefits/Pages/default.aspx
- Requires: Teudat Zehut + password or gov.il SSO

### Digital Signatures (2026)
Three accepted methods:
1. **כרטיס חכם / smart card** issued by an approved provider (Comsign, PersonalID). Required for advanced misim.gov.il flows and Companies Registrar digital filings.
2. **תעודת זהות ביומטרית + סיסמה** (biometric ID + password). Primary authentication for `my.gov.il` and the gov.il personal area.
3. **חתימה דיגיטלית מאומתת** (verified digital signature) issued per the National Digital Agency standard.

Sources:
- https://www.govextra.gov.il/national-digital-agency/signature/home/
- https://www.gov.il/he/pages/digital_signature

## Date and Number Formats

| Field | Format | Example |
|-------|--------|---------|
| Date | DD/MM/YYYY | 15/03/2024 |
| Teudat Zehut | 9 digits (with leading zeros) | 012345678 |
| Phone (mobile) | 05X-XXXXXXX | 052-1234567 |
| Phone (landline) | 0X-XXXXXXX | 03-1234567 |
| Mikud (postal code) | 7 digits | 6100000 |
| Company number | 9 digits | 514567890 |
| Amuta (non-profit) number | 9 digits starting with 58 | 580123456 |
| IBAN (Israeli) | IL + 2 check + 3 bank + 3 branch + 13 account = 23 chars | IL620108000000099999999 |

For authoritative mikud lookup use Israel Post: `https://mypost.israelpost.co.il/zipcodesearch`.

## Browser Automation Notes

### General Tips
- Government sites use Hebrew (RTL), set locale to `he-IL`
- Many forms are React/Angular SPAs, wait for dynamic content
- File uploads often require specific formats (PDF, JPG) and size limits
- Digital signatures may be required for some submissions

### Common Selectors
- Gov.il forms typically use various data attributes, NOT a stable `data-testid="form-container"`. Enumerate the DOM (`page.content()` or DevTools) before assuming any selector.
- Tax Authority uses custom form components
- Bituach Leumi uses standard HTML forms with Hebrew labels

### Rate Limiting
- No official rate limits published
- Recommended: add 1-2 second delays between page navigations
- Peak hours (tax filing season March-May): expect slower responses
