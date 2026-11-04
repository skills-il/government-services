# Domain checklist: israeli-gov-form-automator

Scope: an agent helping a user fill and submit Israeli government forms (online portals and fillable PDFs) for the Tax Authority, Bituach Leumi, the Companies Registrar, and gov.il services. Built 2026-11-03 from a Bituach Leumi / bureaucracy-navigator coverage audit and primary-source research (sources below).

## Must cover (core)

- Who fills each form and who receives it (101 by the employee to the employer; 106, 857, 867 issued by others; 161 by the employer). Source: Kol Zchut טופס 101 / טופס 106; gov.il notice-of-retirement.
- Annual return route: obliged filer (1301) vs refund request for previous years (135, up to 6 years), with the tax-year deadlines. Source: gov.il annual-return 2025 page; gov.il itc116 page.
- Form 101 deadlines (7 days from start or first salary, 1 January, 7 days from a change; possible annual exemption for pensioners 70+ and allowance recipients) and attachments (ID + appendix); Form 119 attached to the 101. Source: Kol Zchut טופס 101; gov.il itc119.
- Electronic 101 is permitted through an approved system, not mandatory. Source: ITA circular 12.1.2026.
- Manual (paper) annual-return routes: above retirement age, low income, non-obliged refund seekers. Source: gov.il annual-return 2025 page.
- Identified services are personal; family-member exception; password secrecy. Source: gov.il terms of use.
- Agent never handles password or OTP, never submits/signs/pays without per-submission confirmation, never ticks a declaration, never solves a CAPTCHA. (structural: how the agent behaves, backed by the terms-of-use entry)
- Login systems per portal: national identification (password + SMS/voice OTP, passkey since May 2025); Tax Authority and Bituach Leumi run their own. Source: Kol Zchut national identification page; State Comptroller report May 2026.
- Logging in is not signing; signature by smart card or token from an authorised CA. Source: gov.il digital_signature page.
- Maternity pay: automatic-payment cases (none after a home birth), online claim only after birth, 12-month filing limit, employer confirmation of the 10 months before stopping work. Source: Kol Zchut דמי לידה.
- Company registration online (national identification, online approval by each party), name proposals (three under the 2017 manual; the current click guide states no number), 2026 fees. Source: gov.il registration-online and its guide PDF; Registrar 2017 manual; Corporations Authority 2026 fee table.
- Field validation: Teudat Zehut check digit, phone formats per the numbering plan (05X and 07X are 10 digits, geographic 9), mikud 7 digits, IBAN mod-97. Source: Ministry of Communications numbering plan Feb 2023; Wikipedia postal codes.
- PDF filling with pypdf: enumerate fields, write the file, check Hebrew appearance visually. (structural, tested locally with pypdf 6.12)

## Should cover (advanced)

- Bituach Leumi form numbers and per-claim attachment lists (deferred: the skill tells the agent to read them from the claim form itself).
- Employer reporting (102, 126, 856) for small-business users (deferred to a future cycle; logged in optimization-log).
- Offline and assisted routes when automation fails (covered: public-inquiries system for paper tax returns, service centres; specific hotline numbers deferred).
- Bank account for payments: use the account the claim form asks for (Kol Zchut notes maternity pay goes to the account given at the hospital on a first birth, or the child-allowance account).

## Out of scope (explicit)

- Deciding what to claim (credit points, refund eligibility, tax coordination amounts): routed to `israeli-employee-tax-refund` and `israeli-tax-coordination`. Rationale: this skill fills forms. Reviewed 2026-11-03: users do ask, and the skill routes them rather than staying silent.
- Building approved electronic-101 payroll systems (a software-house approval process). Reviewed 2026-11-03.
- Classified or security-clearance systems.
- Municipal (arnona) and court e-filing systems.
- VAT periodic reporting flows.

## Authoritative sources

- https://www.gov.il/he/pages/terms_of_use
- https://www.gov.il/he/service/reporting-and-payment-2025-annual-tax-report-for-individuals
- https://www.kolzchut.org.il/he/%D7%98%D7%95%D7%A4%D7%A1_101
- https://www.kolzchut.org.il/he/%D7%93%D7%9E%D7%99_%D7%9C%D7%99%D7%93%D7%94
- https://library.mevaker.gov.il/sites/DigitalLibrary/Documents/2026/2026-05-Cyber/2026-05-Cyber-101.pdf
- https://www.gov.il/he/service/registration-online
- https://www.gov.il/BlobFolder/policy/number_policy/en/The_numbering_plan-02-2023.pdf
