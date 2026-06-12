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
  - Days 1 to 125: capped at 550.76 NIS/day in 2026 (average wage 13,769 ÷ 25 working days).
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
- **15 paid + up to 11 unpaid = 26 weeks total:** Under the Women's Employment Law (חוק עבודת נשים), employees may extend up to 11 additional unpaid weeks for a total of 26 weeks; only the first 15 are BTL-paid.
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
- **Daily cap (2026):** 1,730.33 NIS/day (max insurable income 51,910 ÷ 30). Daily minimum: 328.76 NIS/day.
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

Bituach Leumi runs ~85 numbered claim forms (טפסים) across the 13 programs above. The full catalog with form numbers, Hebrew names, who files each, and notes is in **`references/forms.md`** (organized by program: maternity, child allowance, old-age, survivors, unemployment, disability, work injury, vocational rehab, miluim, income support, alimony, employer bankruptcy, burial, long-term care, mobility, hostile-action victims, treaty / abroad, self-employed contributions, representation, general-purpose).

Most claims are filed digitally through the personal area at **https://ps.btl.gov.il**, where the form-PDF is auto-generated from the wizard. PDF originals live at **https://www.btl.gov.il/טפסים-ואישורים** under per-program subfolders.

> **Form 900 is NOT a benefit claim.** It is the general "Personal Details Update" form (הודעה על עדכון פרטים אישיים) used by anyone already receiving a benefit to change their address, marital status, or bank account.
>
> **Form 100 in BTL** is the opt-out from employer-outreach, NOT an employer report. The actual employer attachment to a 1500 unemployment claim is form **1514**. The "100" most accountants reference is a Tax Authority payslip-summary form, not a BTL form.

### Most-used forms

| Need | Form | Filed by |
|---|---|---|
| Maternity allowance | 355 (or 356 with birth grant) | Mother |
| Old-age pension | 480 | Resident at retirement age |
| Unemployment | 1500 + employer 1514 | Laid-off employee + employer |
| Work injury (initial) | 211 | Injured worker |
| General disability | 7801 | Disabled adult |
| Reserve duty (personal) | 502 / employer 501 | Reservist / employer |
| Long-term care | 2600 | Elderly resident |
| Income support | 5619 | Low-income resident |
| Survivors | 410 | Widow/widower/orphan |
| Mobility (step 1 to MoH) | 8220 → 8200 | Mobility-limited person |
| Hostile-action victims | 580 (+ 595/596 for hostage families) | Injured / family |
| Court-ordered alimony collection | 5400 | Alimony recipient |
| Wages after employer bankruptcy | 5305 | Employee |
| Vocational rehabilitation | 270 | Disabled / work-injured / survivor / terror victim |
| Annual life certificate (abroad) | 10420 | Pension recipient living abroad |
| Authorize a representative | 70 | Insured person |
| Update address / bank / marital status | 900 | Existing beneficiary |
| Self-employed file open | 6101 | New עצמאי |

For any form not listed above, see `references/forms.md` for the complete catalog or search at https://www.btl.gov.il/טפסים-ואישורים/FormSearch/Pages/default.aspx.

## Contribution Rates (2026)

NI is collected on income up to a monthly cap, with two brackets:

- **Bracket boundary (60% of average wage):** 7,703 NIS/month.
- **Maximum insurable income (תקרה):** 51,910 NIS/month.

| Payer | Bracket 1 (up to 7,703) | Bracket 2 (7,703 to 51,910) |
|---|---|---|
| Employee (deducted from salary) | 1.04% NI + 3.23% health = **4.27%** | 7.0% NI + 5.17% health = **12.17%** |
| Employer (in addition to wage) | 4.51% | 7.60% |
| Self-employed | 4.47% NI + 3.23% health = **7.7%** | 12.83% NI + 5.17% health = **18.0%** |

> **Amendment 252 (תיקון 252):** the 2026 rate increases above are set by Amendment 252 to the National Insurance Law, enacted 2025-01-14. Rates are CPI-indexed for 2026 through 2028 and switch to wage indexation from 2029.

Self-employed pay both shares (employee + employer-equivalent) and cannot claim unemployment. They can claim every other benefit. Verify rates against the live BTL pages (`btl.gov.il/Insurance/.../rates.aspx`) at filing time, rates can shift mid-year on amendment.

#### Employee Rates Vary by Age and Pension Status (2026)

The 4.27% / 12.17% above is ONLY the standard employee aged 18 to retirement. The amount actually deducted from an employee's salary changes with age and old-age-pension status. Applying the standard rate to a minor or a working pensioner is a common and material error (it over-charges them by the whole deduction).

| Employee category | Employee deduction, reduced (up to 7,703) | Employee deduction, full (7,703 to 51,910) |
|---|---|---|
| Aged 18 to retirement age (standard) | 1.04% NI + 3.23% health = **4.27%** | 7.0% NI + 5.17% health = **12.17%** |
| Under 18 | **0%** (employer pays 0.61% / 2.12%, employee nothing) | **0%** |
| Receiving old-age pension (kitzbat azrach vatik), any age | **0%** (employer still pays 0.61% / 2.12%) | **0%** |
| Reached retirement age, under 70, NOT yet receiving old-age pension (men 67-70) | 0.61% NI + 3.23% health = **3.93%** | 4.86% NI + 5.17% health = **10.03%** |
| Woman between her retirement age and 67, NOT receiving old-age pension | **3.95%** | **10.24%** |
| Recipient of work-injury or general-disability pension (75%+/100%, with annual BTL confirmation) | 0% NI + 3.23% health = **3.23%** (health only, NI exempt) | 0% NI + 5.17% health = **5.17%** |
| Soldier in regular service, organ donor, treaty-country foreign resident | 1.04% NI only (health exempt) | 7.0% NI only |

- The employer share (4.51% / 7.60%) does NOT change with the employee's age, only the employee deduction does (and for under-18 / pensioner the employer keeps paying its reduced 0.61% / 2.12%).
- Recently-naturalized residents (first became resident over age 62) and controlling shareholders of a closely-held company (ba'al shlita) have their own slightly different rows, verify on the live page.
- Source: `btl.gov.il/Insurance/Rates/Pages/לעובדים שכירים.aspx` (employee rate table, 2026 figures effective 01.01.2026; rates unchanged from 2025 per the BTL 2026 circular).

#### Self-Employed Rates Also Vary by Age and Pension Status

The 7.7% / 18% above is the STANDARD self-employed rate (aged 18 to retirement, not receiving old-age pension). Like employees, a self-employed person who is a minor, who receives an old-age pension, or who reached retirement age pays a reduced National Insurance rate (the health component continues). Do not apply the flat 7.7% / 18% to a self-employed pensioner. Verify the exact reduced rate for the specific age and pension status on `btl.gov.il/Insurance/Rates/Pages/לעצמאים.aspx`.

#### Multiple Employers and Coordination (Te'um Dmei Bituach)

Each employer applies the reduced-rate bracket (the lower 4.27% up to 7,703) to the salary IT pays. An employee with two or more employers (or salary plus an early pension) therefore gets the reduced bracket applied more than once and is over-deducted. The rule: the secondary employer (and an early-pension payer) must deduct at the FULL rate (12.17%) from the first shekel, UNLESS the employee files a coordination request (te'um dmei bituach). File te'um through the secondary employer, or claim a refund from BTL for the over-deducted amount after year-end. This is one of the most common over-payments for people with a second job or a gig plus a salary.

#### Household-Help Employers (Ma'asik Oved Meshek Bayit)

A private individual who employs a domestic worker (cleaner, nanny, caregiver, gardener) is a household employer and must register with BTL and pay contributions on the worker's wage, reported and paid quarterly (not through a monthly payslip system). For a domestic worker aged 18 to retirement (2026): the employer pays **6.05%** National Insurance (0% health on the employer side) and the worker's share is **2.8%** (1.8% NI + 1% health), total **8.85%** of the wage. For a domestic worker under 18 or receiving an old-age pension, the employer pays a reduced **3.6%**. Register once via the BTL household-employer service. Source: `btl.gov.il/Insurance/Rates/Pages/עובד משק בית.aspx`.

### Non-Working Residents and Non-Work (Passive) Income (2026)

A working-age resident (18 to retirement age) who is NOT salaried, NOT self-employed, and NOT an exempt non-working spouse still owes NI and health insurance on their own account. The base table below applies to that person only. Read the exemptions and the coordination rule that follow, because they change the answer for several common cases (getting them wrong is the most frequent error here).

| Situation (base case: own account, no work income) | Monthly charge (2026) |
|---|---|
| Not working, no income | **Minimum 266 NIS/month** (143 NIS NI + 123 NIS health) |
| Non-work (passive) income up to 3,442 NIS/month | Exempt from the rate, but the 266 minimum still applies |
| Non-work income 3,442 to 7,703 NIS (reduced tier) | 6.92% NI + 5.17% health = **12.09%** on the amount above 3,442 |
| Non-work income 7,703 to 51,910 NIS (full tier) | 7.0% NI + 5.17% health = **12.17%** |

"Non-work income" (הכנסה שלא מעבודה) means passive income such as rent, dividends, and interest. The first 3,442 NIS/month is exempt; rates apply only to the amount above it. The 266 NIS minimum applies as a floor, so a non-working resident pays the greater of the passive-income calculation or 266 NIS/month. BTL sends a quarterly advance-payment book (pinkas mikdamot) for non-employees.

**Exemptions and exceptions (these OVERRIDE the base table, do not apply the table to these people):**

| Who | Treatment |
|---|---|
| Non-working spouse (עקרת בית, or a non-working partner of an insured resident, including common-law and same-sex marriage) | **Fully exempt, pays 0** NI and health on their own account. Granted automatically in most cases; otherwise reported via Form 673 (spouse-exemption declaration) or the Form 6101 multi-year declaration. Lumping this person under the 266 minimum is the single most common mistake. |
| Old-age pension recipient / past retirement age | Special treatment, NOT the flat table. For benefit recipients, non-work income up to **688 NIS/month (2026)** is exempt, and the NI portion generally does not apply to a pensioner's income (health may still apply). Verify the exact split with BTL before quoting a number. |
| Person with BOTH work income (salary or self-employment) AND passive income | The 3,442 NIS exemption does NOT stack on top of work income. Work income consumes the exemption, so passive income is charged separately (often from the first shekel for higher earners). This is a coordination calculation, do not treat passive income as exempt just because it is below 3,442. |
| New immigrant (oleh) in the early residency window, full-time student, or resident working abroad for a foreign employer | Special rules apply (oleh reductions, bilateral social-security treaty coordination for a foreign employer). Treat as a separate case, not the base table. |

- Under-18s are not separately liable; coverage is through the household.
- The 266 minimum and the 3,442 / 688 thresholds are average-wage-indexed and update each January and July.
- Source: `btl.gov.il/Insurance/National Insurance/Pages/מי פטור מתשלום דמי ביטוח לאומי.aspx` (exemptions), `btl.gov.il/Insurance/National Insurance/type_list/NotWorking/Pages/ScomNotWorking.aspx` (minimum), `btl.gov.il/Insurance/Rates` (non-working and non-work-income), and kolzchut "פטור מתשלום דמי ביטוח לאומי", 2026 figures effective 01.01.2026.

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
3. Calculation: last 3 months average daily wage (gross divided by 90), capped at 1,730.33 NIS/day, minimum 328.76 NIS/day.
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
- Self-employed pay both the employee and employer shares of NI (7.7% reduced bracket and 18.0% full bracket in 2026, per Amendment 252). Agents may calculate only the employee share, underestimating the obligation by ~2x.
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
