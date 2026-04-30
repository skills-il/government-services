---
name: israeli-bituach-leumi
description: Navigate Israeli National Insurance (Bituach Leumi) benefits, eligibility, contributions, and claim forms (טפסים). Use when user asks about "bituach leumi", national insurance, retirement pension (kitzbat zikna), unemployment (dmei avtala), maternity leave (dmei leida), child allowance (kitzbat yeladim), disability (nechut), work injury, reserve duty (miluim), survivors pension, long-term care (siyud), income support (havtachat hachnasa), birth grant (ma'anak leida), savings-for-every-child, or NI contribution rates. Includes form numbers (Form 900, 355, 480, 1500, 211, 7801, etc.) for filing each claim. Do NOT use for private insurance or health fund (kupat cholim) questions.
license: MIT
allowed-tools: Bash(python:*)
compatibility: No network required. Works with Claude Code, Claude.ai, Cursor.
---

# Israeli Bituach Leumi (National Insurance)

## Critical Note
Bituach Leumi rules are complex and amounts update twice a year (January and July) tied to the average wage. Always direct users to verify their specific case at btl.gov.il, the personal area at https://ps.btl.gov.il, or by calling *6050. Amounts in this skill reflect the official 2026 rate announcement (`btl.gov.il/About/news/Pages/hadasaidkonkitzva2026.aspx`).

## Instructions

### Step 1: Identify the Benefit Program
Map the user's situation to the correct program. The 13 main programs are listed in `references/benefit-programs.md`.

### Step 2: Check Eligibility
Each program has its own qualifying period. The full table is in `references/benefit-programs.md` under "Qualifying Periods". Key factors:
- Residency status (תושב vs. non-resident; new immigrants have special rules)
- Age (retirement, work, minor)
- Employment history (qualifying period, called תקופת אכשרה)
- Income level (some benefits are means-tested)
- Medical condition (for disability, long-term care, work injury)
- Marital and family status

### Step 3: Estimate Benefit Amount
Use `scripts/calculate_benefits.py` for old-age pension, unemployment, maternity, child allowance, miluim, and birth grant estimates. All hardcoded amounts reflect 2026 rates.

### Step 4: File the Claim
Identify the correct form (see `## Forms` below) and the right filing channel (see `## Digital Channels`). Most claims are now filed digitally through the personal area at https://ps.btl.gov.il, with the form-PDF auto-generated from the wizard.

### Step 5: Track and Appeal
Three appeal tracks exist (medical, non-medical, labor court). See `## Appeals` below for the deadlines and the right venue per decision type.

## Key Programs Detail

All amounts are **2026 official rates**. Rates update January 1 and July 1.

### Old Age Pension (Kitzbat Zikna)
- **Retirement age (גיל פרישה):** Men 67. Women 62 to 65, depending on birth-month cohort. The Knesset passed תיקון מס' 7 in 2021 that resumed raising women's retirement age starting June 2022, by 4 months/year. Final age 65 is reached for women born after April 1960; full schedule completes around 2032. Use the official BTL retirement-age calculator at btl.gov.il/benefits/old_age/Pages/RetirementCalculation.aspx.
- **Absolute eligibility age (גיל הזכאות המוחלטת):** 70 for everyone. Pension is paid regardless of income.
- **Income test (between retirement age and 70):** Single ~7,827 NIS/month; couple ~10,436 NIS/month. Above the threshold the pension is suspended until age 70.
- **Qualifying period:** 60 to 144 months of NI contributions (varies by age at immigration).
- **Basic amount (2026):**
  - Single: 1,838 NIS/month up to age 80; 1,941 NIS/month from age 80.
  - Couple: 2,762 NIS/month (spouse increment 924 NIS).
- **Seniority supplement (תוספת ותק):** +2% per year starting from year 11 of contributions, capped at 50% (25 years). Most pensioners receive the full 50%, bringing the typical single-rate to ~2,757 NIS/month.
- **Deferral bonus:** +5% per year of deferred claiming, paid up to age 70.
- **Income supplement (השלמת הכנסה):** Additional payment for low-income pensioners.
- **Claim form:** **480** (תביעה לקצבת אזרח ותיק - זקנה). File at https://ps.btl.gov.il.

### Unemployment (Dmei Avtala)
- **Eligibility:** 12 of last 18 months as a salaried employee; service ended due to termination, not resignation.
- **Resignation penalty:** 90-day disqualification for voluntary resignation, unless quitting for justified cause (הרעת תנאים, relocation following spouse, family-care). The standard "5-day waiting period" only applies to terminations.
- **Duration:** 50 to 175 days, depending on age and dependents.
- **Amount:** Sliding scale tied to the average wage, capped at:
  - Days 1 to 125: full daily average wage = ~1,101.50 NIS/day in 2026.
  - Days 126 onward: 2/3 of daily average wage = 367.17 NIS/day in 2026.
- **Combined registration:** The single shared workflow at https://www.taasuka.gov.il/applicants/sharedform/ registers with שירות התעסוקה and files the BL claim in one step.
- **Claim form:** **1500** (תביעה לדמי אבטלה) plus employer attachment **1514** (אישור המעסיק על תקופת ההעסקה והשכר).

### Maternity, Birth, and Parental Leave
- **Birth grant (ma'anak leida) 2026:** First child 2,103 NIS; second 946 NIS; third+ 631 NIS; **twins 10,514 NIS**. Paid as a one-time grant per birth. Hospitals normally file automatically when the mother provides her bank details on admission.
- **Hospitalization grant (ma'anak ishpuz):** Paid directly to the hospital for the delivery.
- **Maternity allowance (dmei leida) eligibility:**
  - Full 15 weeks: 10 of last 14 OR 15 of last 22 months as employee or self-employed.
  - Reduced 8 weeks: 6 of last 14 OR 10 of last 22 months.
- **Maternity duration extras:** +3 weeks for multiple births. Hospitalization extension if newborn is hospitalized 15+ days. Adoptive mothers receive an equivalent (גמלה לאם מאמצת).
- **Daily cap (2026):** 1,752.33 NIS/day. Calculation base: last 3 months ÷ 90 OR last 6 months ÷ 180, whichever is higher.
- **Father / partner (gimlat horim le'av):** 1 week dedicated; the remaining weeks can be split between parents.
- **Pregnancy preservation (shmirat herayon):** Separate benefit if a doctor certifies the work environment is hazardous. Form 330 + medical certificate 331.
- **Claim forms:** Mother, **355** (תביעה לדמי לידה); father, **354** (תביעה לתשלום גמלת הורים לאב), **360** (partner-week split). Birth grant + maternity together, **356**.

### Child Allowance (Kitzbat Yeladim)
- **Eligibility:** All Israeli residents with children under 18; usually automatic from hospital report.
- **Amounts (2026, per child per month):**
  - 1st child: 173 NIS.
  - 2nd, 3rd, 4th child: 219 NIS each.
  - 5th child onward: 173 NIS each.
- **Payment date:** Around the 20th of each month, paid to the registered parent.
- **Manual filing (rare):** Form **5025** (תביעה אישית לקצבת ילדים), only when not auto-registered (birth abroad, parent transfer, custody change).
- **Savings-for-every-child (חיסכון לכל ילד):** 58 NIS/month per child auto-deposited by BTL until age 18. Parents may match from the child allowance for 116 NIS total. Released at 18 (or 21 with bonus).

### General Disability (Nechut Klalit)
- **Distinct from work injury (nechut me'avoda)**: different program, different forms.
- **Eligibility:** Resident aged 18 to retirement age with medical incapacity reducing earning capacity by 60%, 65%, 74%, or 75-100%. Requires 12 months of NI residency before disability.
- **Monthly amounts (2026):**
  - 75% to 100% incapacity (full): 4,711 NIS.
  - 74%: 3,211 NIS.
  - 65%: 2,894 NIS.
  - 60%: 2,718 NIS.
- **Family supplements:** Spouse +1,518 NIS; children +1,214 NIS up to 2 children.
- **Special services (sherutim meyuchadim, SHRM):** For the severely disabled who need daily personal care. Tiers from 50% rate (1,943 NIS) to 235% rate (9,126 NIS). Caregiver supplement up to 10,774 NIS/month.
- **Disabled child (yeled nacheh):** Up to 3,820 NIS for a 100%-disabled child plus caregiver supplement.
- **Claim forms:** **7801** (general disability claim), **7849** (special services), **7821** (disabled child).

### Work Injury (Pgi'at Avoda)
- **Eligibility:** Any worker injured on the job or commuting; covered from day 1 of employment (no qualifying period). Self-employed must be registered with BTL before the injury.
- **Injury pay (dmei pgi'a):** 75% of last 3 months average wage, paid for up to 91 days.
- **Daily cap (2026):** 1,314.25 NIS/day.
- **Permanent disability (after 91 days):** Determined by medical committee; lump-sum or pension based on disability percentage.
- **Claim forms:** **211** (initial injury-pay claim and notification, the "tofes 211" most people refer to), **200** (permanent disability degree), **250** (medical-treatment authorization for employees), **283** (same for self-employed), **284** (employer declaration).
- **Common confusion:** "Form 100" is NOT a BTL employer report for unemployment. Form 100 in BTL is the opt-out from employer outreach. The actual employer attachment to a 1500 unemployment claim is form 1514. The "100" most accountants refer to is a Tax Authority payslip-summary form, not a BTL form.

### Reserve Duty (Miluim)
- **Eligibility:** Any IDF reservist; covered from day 1 (no qualifying period). Claim window: 7 years from end of service.
- **Daily amount:** 100% of last 3 months' average daily wage (gross ÷ 90), or for self-employed, prior-year tax assessment ÷ 90.
- **Daily cap (2026):** 1,752.33 NIS/day. Daily minimum: 328.76 NIS/day.
- **Annual bonus tiers (Iron Swords-era):** Enhanced rates for cumulative miluim days/year, ~2,000 to ~10,000+ NIS depending on tier.
- **Salaried employees:** Employer pays salary as usual; BTL refunds the employer via form 501. The employee receives the full salary.
- **Self-employed and sub-cap salaried:** File personal claim form **502**. Form **509** for advance payment.

### Long-term Care (Siyud)
- **Eligibility:** Resident at retirement age who fails the ADL dependence test (mivchan ADL: washing, dressing, eating, mobility, toileting, continence). Six dependence levels (2.5-3 points = level 1, 9.5+ points = level 6).
- **Income test (2026):** Single < 12,536 NIS/month; couple < 18,804 NIS/month for full benefit. Reduced for higher incomes.
- **Cash amounts (2026):** Level 1, 1,659 NIS; Level 6, 7,238 NIS. Recipients can elect cash payment OR care services delivered by approved providers.
- **Foreign caregiver (metapel zar):** Interaction with the Population Authority's permit; the cash benefit can supplement the caregiver's wage.
- **Claim form:** **2600** (תביעה לגמלת סיעוד). Form **2655** to elect cash-instead-of-services.
- **Related skill:** `israeli-elder-care-navigator` covers the broader elder-care system including assisted living and nursing homes.

### Income Support (Havtachat Hachnasa)
- **Eligibility:** Low-income residents who pass an asset test (no second home, car value below threshold, savings below threshold) AND, if under 55, comply with the שירות התעסוקה employment test.
- **Monthly amounts (2026):** From 1,661 NIS (single under 25) to 5,289 NIS (single parent 55+ with 2+ children).
- **Interactions:** Not paid alongside unemployment. Combines with old-age (השלמת הכנסה לקצבת זיקנה) and disability supplements.
- **Claim form:** **5619** (תביעה לגמלת הבטחת הכנסה). Form **5521** for employer attachment if the claimant works part-time.

### Survivors Pension (Sheerim)
- **Eligibility:** Widow/widower of a deceased insured person. Deceased must have had 12 months NI in the last 18 OR 60 months total. Widow eligible at 40+, or with children, or with reduced earning capacity.
- **Monthly amount (2026):** ~1,838 NIS base (matches old-age single rate). Plus orphan supplement per child.
- **Filing window:** Within 12 months of death.
- **Claim forms:** **410** (survivors pension claim), **416** (death grant + pension balance), **2910** (orphan maintenance).

### Mobility Allowance (Niyadut)
- **Two-step process:** Form **8220** to the Ministry of Health (medical committee determines % limitation), THEN form **8200** to BTL for the benefit.
- **Components:** Loan to purchase an accessible vehicle, monthly subsidy. Joint program with משרד התחבורה.

### Hostile-action Victims (Nifgaei Pe'ulot Eiva)
- **Funding:** State (not contribution-funded). Especially relevant post-October 2023.
- **Recognition:** Form **580** (initial recognition + claim), then **581** for disability-degree determination, **582** for family of deceased, **577** for psychological injury intake.

### Employer Bankruptcy (Pshitat Regel shel Ma'asik)
BTL pays unpaid wages, severance, and unused vacation when the employer goes insolvent. Distinct program with its own caps. File once a court has issued the bankruptcy or liquidation order.

## Forms (טפסים)

Bituach Leumi forms are numbered by program. Most can now be filed digitally through the personal area at **https://ps.btl.gov.il** (login with Israeli ID + password or one-time SMS code). PDF originals live at **https://www.btl.gov.il/טפסים-ואישורים** under per-program subfolders.

> **Form 900 is NOT a benefit claim.** It is the general "Personal Details Update" form (הודעה על עדכון פרטים אישיים) used by anyone already receiving a benefit to change their address, marital status, or bank account. The actual program-specific claim forms are listed below.

### Maternity, parental leave, birth grants

| Form | Hebrew name | Filed by | Notes |
|---|---|---|---|
| 355 | תביעה לתשלום דמי לידה ליולדת | Mother (employee or self-employed) | Main maternity-pay claim |
| 356 | תביעה לתשלום מענק לידה ודמי לידה לאם | Mother | Birth grant + maternity pay combined |
| 300 | תביעה למענק לידה ולמענק אשפוז | Mother / hospital | Hospital normally files automatically |
| 302 | תביעה לתשלום מענק לאב | Father | Birth grant for father |
| 354 | תביעה לתשלום גמלת הורים לאב | Father | Parental-leave pay for father |
| 360 | תביעה לתשלום דמי לידה לאב המחליף את בת/בן הזוג | Father | Partner-week split / paternity replacement |
| 330 | תביעה לתשלום גמלה לשמירת הריון | Pregnant employee | Hazardous-pregnancy benefit. Pair with 331 |
| 331 | אישור רפואי לגמלת שמירת הריון | Doctor | Companion to 330 |
| 368 | תביעה להארכה או פיצול דמי לידה | Mother / parents | Extension or splitting between parents |
| 381 | בקשה לשימור ותחזוק העסק במהלך תקופת לידה | Self-employed mother | Business-continuity grant |

### Child allowance and child savings

| Form | Hebrew name | Filed by | Notes |
|---|---|---|---|
| (auto) | (no form, hospital-reported) | Hospital | Births in Israel are reported automatically; provide bank details at the hospital |
| 5025 | תביעה אישית לקצבת ילדים | Parent / guardian | Only when not auto-registered (birth abroad, custody change) |

### Old-age pension and death

| Form | Hebrew name | Filed by | Notes |
|---|---|---|---|
| 480 | תביעה לקצבת אזרח ותיק - זקנה | Resident at retirement age | Main claim |
| 434 | תביעה למענק מעבר בגין העלאת גיל הפרישה | Affected age cohort | Transition grant |
| 484 | תביעה לתוספת עבור בן/בת זוג | Pensioner | Spouse increment |
| 430 | תביעה להשלמת הכנסה למקבל קצבאות אזרח ותיק ושאירים | Low-income pensioner | Income supplement |
| 4501 | תביעה לגמלה מיוחדת לאזרח ותיק | Non-insured immigrant past retirement age | Special benefit |
| 481 | בקשה למענק מיוחד לבני 67+ | Working pensioner | Special grant for 67+ |

### Survivors

| Form | Hebrew name | Filed by | Notes |
|---|---|---|---|
| 410 | תביעה לקצבת שאירים | Widow / widower / orphan | Main survivors claim. File within 12 months of death |
| 416 | תביעה לתשלום מענק פטירה ו/או יתרת קצבה | Heirs | Death grant + pension balance |
| 2910 | תביעה לדמי מחיה בעד יתום | Orphan / guardian | Orphan maintenance |
| 412 | הצהרת הכנסות שאירים | Survivor | Income declaration |

### Unemployment

| Form | Hebrew name | Filed by | Notes |
|---|---|---|---|
| 1500 | תביעה לדמי אבטלה | Laid-off employee | Main claim. Use the joint workflow at taasuka.gov.il/applicants/sharedform |
| 1514 | אישור המעסיק על תקופת ההעסקה והשכר | Employer | Required attachment to 1500 |
| 1517 | תביעה למענק למובטל העובד בשכר נמוך | Low-wage worker | Supplement |

### General disability and special services

| Form | Hebrew name | Filed by | Notes |
|---|---|---|---|
| 7801 | תביעה לקצבת נכות כללית | Disabled adult under retirement age | Main claim |
| 7849 | תביעה לקצבת שירותים מיוחדים | Severely disabled adult | Attendance allowance |
| 7821 | תביעה לגמלה לילד נכה | Parent of disabled child | Disabled-child benefit |
| 7842 | בקשה לבדיקה מחדש עקב החמרת מצב | Existing recipient | Reassessment |
| 7810 | כתב ערר על החלטת המוסד | Claimant | Appeal |
| 3296 | בקשה לתשלום תוספת תלויים | Recipient | Dependants increment |

### Work injury

| Form | Hebrew name | Filed by | Notes |
|---|---|---|---|
| 211 | תביעה לתשלום דמי פגיעה והודעה על פגיעה בעבודה | Injured employee | Initial injury-pay claim, the most common BL form |
| 200 | תביעה לקביעת דרגת נכות מעבודה | Injured employee | Permanent disability claim (after 91-day dmei pgi'a period) |
| 250 | טופס למתן טיפול רפואי לנפגע בעבודה - שכיר | Employee | Authorization slip for clinic / hospital |
| 283 | אישור למתן טיפול רפואי - עצמאי | Self-employed | Same as 250 for self-employed |
| 284 | הצהרת המעסיק על פגיעה בעבודה | Employer | Employer declaration |
| 202 | תביעה להכרה במחלת מקצוע | Worker | Occupational-disease recognition |
| 213 | תביעה לתשלום גמלה לבני משפחה של מי שנפטר מפגיעה בעבודה | Dependants | Dependants pension after fatal injury |

### Reserve duty (miluim)

| Form | Hebrew name | Filed by | Notes |
|---|---|---|---|
| 502 | תביעה אישית לתגמולי מילואים | Reservist (self-employed or below cap) | Personal claim |
| 501 | תביעת מעסיק להחזרת תגמולי מילואים | Employer | Employer-refund claim |
| 509 | בקשה לתשלום מקדמה על חשבון תגמולי מילואים | Reservist | Advance payment |
| 510 | אישור המעסיק על עבודה ושכר | Employer | Salary confirmation |

### Income support

| Form | Hebrew name | Filed by | Notes |
|---|---|---|---|
| 5619 | תביעה לגמלת הבטחת הכנסה | Low-income resident | Main claim |
| 5624 | בקשה לחידוש הזכאות | Returning claimant | Renewal |
| 5521 | טופס למילוי על ידי מעסיק לתובעי הבטחת הכנסה | Employer | Employer attachment |
| 5612 / 5613 | הצהרה לתובע/ת החי/ה בנפרד מבן/בת הזוג | Separated claimant | Separation declaration |

### Long-term care

| Form | Hebrew name | Filed by | Notes |
|---|---|---|---|
| 2600 | תביעה לגמלת סיעוד | Elderly resident | Main claim |
| 2655 | גמלת סיעוד בכסף במקום שירותים | Recipient with dedicated caregiver | Cash-instead-of-services election |
| 2620 | בקשה לבדיקה מחדש עקב טענת החמרה | Recipient | Reassessment |
| 2670 | הצהרה לקביעת מעמד בודד | Single applicant | Single-status declaration |
| 2604 | אישור על מגורים במוסד / בית אבות | Institution | Institutional residence confirmation |

### Mobility

| Form | Hebrew name | Filed by | Notes |
|---|---|---|---|
| 8220 | טופס לקביעת מוגבלות בניידות | Mobility-limited resident | Filed with Ministry of Health first (medical committee) |
| 8200 | תביעה להטבות על פי הסכם הניידות | Approved claimant | Filed with BTL after MoH determination |

### Hostile-action victims

| Form | Hebrew name | Filed by | Notes |
|---|---|---|---|
| 580 | הודעה על פגיעה בפעולות איבה ותביעה להכרה כנפגע | Injured / family | Initial recognition + claim |
| 581 | בקשה לקביעת דרגת נכות ולתשלום תגמול נכות | Recognized victim | Disability-degree determination |
| 582 | תביעה לתגמולים למשפחות הנספים | Family of deceased victim | Family compensation |
| 571 | בקשה לתגמול טיפול רפואי | Recognized victim | Medical-treatment compensation |
| 577 | תשאול נפגע הטוען לפגיעה נפשית | Victim claiming psychological injury | PTSD / mental injury intake |

### Insurance contributions (self-employed)

| Form | Hebrew name | Filed by | Notes |
|---|---|---|---|
| 6101 | דין וחשבון רב שנתי | Self-employed / non-working resident | Opens collection file, sets advance payments. Required when starting as עצמאי |
| 672 | בקשה לתיקון מקדמות | Self-employed | Adjust monthly advances (up to 4 times per year) |
| 6131 | הצהרת עיסוקים | Resident changing employment status | Status update |
| 627 / 628 | שאלון לקביעת תושבות | Resident temporarily abroad / returning | Residency determination |
| 673 | הצהרת בני/בנות זוג | Non-working spouse | Spouse-exemption declaration |

### General-purpose forms (every program uses these)

| Form | Hebrew name | Use | Notes |
|---|---|---|---|
| 900 | הודעה על עדכון פרטים אישיים | Update address, marital status, bank account | NOT a claim form, for existing beneficiaries |
| 715 | בקשה להעברת כספים | Reroute payment | |
| 88 | כתב הסכמה והתחייבות לקבלת גמלה | Beneficiary commitment | When benefit paid via third party |
| 17 | כתב ויתור לחברות הביטוח | Privacy waiver to private insurers | |
| 20 | בקשה להענקה מטעמי צדק | Equity grant request | When statutory entitlement is denied but hardship exists |
| 910 | פנייה לוועדת תביעות | Claims committee referral | Internal-appeal channel |
| 851 | בקשה לקבלת מידע לפי חוק חופש המידע | FOI request | |

## Contribution Rates (2026)

NI is collected on income up to a monthly cap, with two brackets:

- **Bracket boundary (60% of average wage):** 7,703 NIS/month.
- **Maximum insurable income (תקרה):** 51,910 NIS/month.

| Payer | Bracket 1 (up to 7,703) | Bracket 2 (7,703 to 51,910) |
|---|---|---|
| Employee (deducted from salary) | 0.4% NI + 3.1% health = **3.5%** | 7.0% NI + 5.0% health = **12.0%** |
| Employer (in addition to wage) | 3.55% | 7.60% |
| Self-employed | 2.87% NI + 5.17% health = **8.04%** | 12.83% NI + 5.0% health = **17.83%** |

Self-employed pay both shares (employee + employer-equivalent) and cannot claim unemployment. They can claim every other benefit. Verify rates against the live BTL pages (`btl.gov.il/Insurance/.../rates.aspx`) at filing time, rates can shift mid-year on amendment.

## Digital Channels

1. **Personal area (preferred):** https://ps.btl.gov.il, most claims have full digital flows; the form-PDF is auto-generated from the wizard.
2. **Online forms portal:** https://www.btl.gov.il/טפסים-ואישורים/tfasimMkuvanim/Pages/default.aspx, submit a filled PDF without logging in.
3. **Document upload to caseworker:** https://b2b.btl.gov.il/BTL.ILG.Payments/DocumentsForm.aspx, for attachments to an open claim.
4. **MyBTL mobile app:** iOS and Android. Most-used flow: download "ishur mekabel kitzba" (benefit-recipient certificate).
5. **Phone:** *6050 (also has WhatsApp at the same number).
6. **Combined unemployment + employment service form:** https://www.taasuka.gov.il/applicants/sharedform/, single workflow that registers with שירות התעסוקה and files the BL 1500 in one step.
7. **Branch service:** Appointments must be booked online; walk-ins are limited. Branch list at https://www.btl.gov.il/snifim. English-language assistance available; press 9 on *6050.

## Appeals

| Decision type | Venue | Statutory deadline |
|---|---|---|
| Medical (disability degree, ADL test) | ועדה רפואית לעררים (medical appeals committee) | 60 days from decision |
| Non-medical eligibility / amounts | ועדת ערר (internal review) | 60 days |
| Final decisions (post-appeal) | בית הדין האזורי לעבודה (regional labor court) | 12 months from decision |

Free legal aid is available through הסיוע המשפטי (Ministry of Justice) for low-income claimants.

## Examples

### Example 1: Maternity Leave
User says: "I'm pregnant and want to know about maternity leave benefits."
1. Confirm employment duration to determine 15 weeks vs 8 weeks.
2. Calculate daily benefit using `python scripts/calculate_benefits.py maternity --salary X --months-employed Y` (capped at 1,752.33 NIS/day in 2026).
3. Mention birth grant (2,103 NIS first child; 10,514 for twins) and the partner-week split.
4. Direct to filing: form 355 (or 356 combined) via the personal area at ps.btl.gov.il.

### Example 2: Retirement Planning
User says: "When can I start getting pension from Bituach Leumi?"
1. If the user is a man, retirement age is 67. If a woman, retirement age depends on birth-month cohort (currently 62 to 65; the schedule is being raised by 4 months/year since 2022). Use the official calculator at btl.gov.il/benefits/old_age/Pages/RetirementCalculation.aspx.
2. Explain the income test between retirement age and 70.
3. Quote the basic 2026 amount (1,838 NIS single, 1,941 from age 80, 2,762 couple). Note that most pensioners get the +50% seniority supplement, bringing the effective single rate to ~2,757 NIS.
4. Direct to form 480 (תביעה לקצבת אזרח ותיק).

### Example 3: Reserve Duty Compensation
User says: "I did 30 days of miluim, how much will Bituach Leumi pay me?"
1. If the user is a salaried employee, the employer pays the salary as usual; BTL refunds the employer via form 501. The user receives full salary, no separate BTL payment.
2. If the user is self-employed or paid below the cap, file a personal claim using form 502.
3. Calculation: last 3 months average daily wage (gross divided by 90), capped at 1,752.33 NIS/day, minimum 328.76 NIS/day.
4. Add the Iron Swords annual bonus tier if cumulative days for the year exceed 10.
5. Mention the 7-year claim window from end of service.

### Example 4: Filing a Disability Claim
User says: "I have a chronic illness, how do I file a disability claim?"
1. Distinguish general disability (nechut klalit) from work-related (nechut me'avoda), different programs, different forms, different funding sources.
2. For general disability: file form 7801 (under retirement age) at the personal area.
3. The medical committee determines incapacity percentage (60%, 65%, 74%, or 75-100%). The 2026 monthly amounts are 2,718 / 2,894 / 3,211 / 4,711 NIS respectively.
4. If the user needs daily personal-care assistance, also file form 7849 for special services (SHRM).
5. Appeal track: medical committee within 60 days for the disability percentage; internal review for eligibility decisions; labor court within 12 months for final challenges.

## Bundled Resources

### Scripts
- `scripts/calculate_benefits.py`, estimate Bituach Leumi benefit amounts for old age pension, unemployment, maternity, child allowance, miluim, and birth grant. All hardcoded amounts reflect 2026 official rates. Subcommands: `pension`, `unemployment`, `maternity`, `child-allowance`, `miluim`, `birth-grant`. Run: `python scripts/calculate_benefits.py --help`.

### References
- `references/benefit-programs.md`, complete program catalog: 13 programs, 2026 rate table, qualifying-period table, contribution-rate tables, appeal deadlines, contact channels, claim-form quick lookup.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [pikud-haoref](https://agentskills.co.il/he/mcp/pikud-haoref) | Real-time emergency alerts (relevant for nifgaei pe'ulot eiva claims). |

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| BTL 2026 rate announcement | https://www.btl.gov.il/About/news/Pages/hadasaidkonkitzva2026.aspx | Annual benefit amounts |
| Personal area (filing) | https://ps.btl.gov.il | Claim status, forms |
| Forms portal | https://www.btl.gov.il/טפסים-ואישורים | All form PDFs |
| Retirement-age calculator | https://www.btl.gov.il/benefits/old_age/Pages/RetirementCalculation.aspx | Per-cohort retirement age |
| Self-employed contribution rates | https://www.btl.gov.il/Insurance/National%20Insurance/type_list/Self_Employed/Pages/rates.aspx | Live rate verification |
| kolzchut BTL hub | https://www.kolzchut.org.il/he/המוסד_לביטוח_לאומי | Plain-Hebrew explanations |
| Joint unemployment + employment-service form | https://www.taasuka.gov.il/applicants/sharedform/ | Combined 1500 + שירות התעסוקה |

## Gotchas
- BTL contribution rates have two brackets: a reduced rate up to 60% of the average wage (7,703 NIS in 2026), and the normal rate above it. Agents almost always apply a single flat rate.
- Self-employed pay both the employee and employer shares of NI (8.04% and 17.83% in 2026). Agents may calculate only the employee share, underestimating the obligation by ~2x.
- Self-employed are NOT eligible for unemployment (dmei avtala), only שכירים are. This is a common user expectation that fails.
- Form 900 is the personal-details update form, NOT a benefit claim. Users frequently search "form 900" expecting it to be a maternity or other benefit form.
- "Form 100" in BTL context is the opt-out from employer outreach, NOT an employer report. The actual employer attachment to a 1500 unemployment claim is form 1514. The "100" non-BTL form most accountants reference is a Tax Authority payslip-summary form.
- Resignation triggers a 90-day disqualification from unemployment unless quitting for justified cause (relocation, family-care, deterioration of conditions). The standard "5-day waiting period" only applies to terminations.
- Mobility (niyadut) is a two-step process: medical determination at the Ministry of Health (form 8220), THEN BTL benefit (form 8200). Filing only one of them is a common mistake.
- Women's retirement age is NOT yet 65 across the board. The 2021 amendment resumed the gradual increase from 62; women's actual retirement age in 2026 depends on birth-month cohort (62 to 65). Use the official calculator.
- The average wage (sachir memutza) used for benefit calculations is updated twice a year (January and July) by the CBS. Outdated figures will cause rate calculations to drift.
- Old-age pension has an income test between retirement age and 70. Above ~7,827 NIS/month single income, the pension is suspended until age 70. Agents quote the basic amount unconditionally.

## Troubleshooting

### Error: "Not enough qualifying months"
Cause: Insufficient contribution history (תקופת אכשרה).
Solution: Check the per-program qualifying-period table in `references/benefit-programs.md`. Some periods (military service, maternity leave, miluim) count as qualifying months. New immigrants (olim) have special rules; for old-age, the 60-month minimum can be waived via מענק מותנה.

### Error: "Benefit amounts don't match expected values"
Cause: BTL updates benefit amounts twice a year (January and July) tied to the average wage.
Solution: Verify current amounts at https://www.btl.gov.il/About/news/Pages/hadasaidkonkitzva2026.aspx or via *6050. Amounts in this skill reflect the official 2026 announcement; check the live page for mid-year revisions.

### Error: "Form not found at the URL I tried"
Cause: BTL form pages are organized in per-program subfolders under `btl.gov.il/טפסים-ואישורים/forms/<program>_forms/Pages/`.
Solution: Use the master form-search at https://www.btl.gov.il/טפסים-ואישורים/FormSearch/Pages/default.aspx. PDF originals are at `btl.gov.il/טפסים-ואישורים/Documents/t<form-number>.pdf` (e.g. `t355.pdf`).

### Error: "I resigned and was denied unemployment"
Cause: Voluntary resignation triggers a 90-day disqualification.
Solution: If the resignation was for justified cause (relocation following spouse, family-care, hazardous-conditions, deterioration of work conditions, fixed-term contract end), file an appeal with form 7810 within 60 days. Document the cause carefully.
