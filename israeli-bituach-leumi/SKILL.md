---
name: israeli-bituach-leumi
description: Navigate Israeli National Insurance (Bituach Leumi) benefits, eligibility, contributions, and claim forms (טפסים). Use when user asks about "bituach leumi", national insurance, retirement pension (kitzbat zikna), unemployment (dmei avtala), maternity leave (dmei leida), child allowance (kitzbat yeladim), disability (nechut), work injury, reserve duty (miluim), survivors pension, long-term care (siyud), income support (havtachat hachnasa), birth grant (ma'anak leida), savings-for-every-child, alimony (mezonot), personal-accident benefit (dmei te'una), vocational rehabilitation, burial and death grants, or NI contribution rates and who pays them (employee, self-employed, non-worker, early pensioner, household-help employer, unpaid leave / chalat). Includes form numbers (Form 900, 355, 480, 1500, 211, 7801, 2201, etc.) for filing each claim. Do NOT use for private insurance or health fund (kupat cholim) questions.
license: MIT
allowed-tools: Bash(python:*)
compatibility: No network required. Works with Claude Code, Claude.ai, Cursor.
---

# Israeli Bituach Leumi (National Insurance)

## Critical Note
Bituach Leumi rules are complex. Amounts update **once a year, on 1 January**, plus an adjustment only if a cost-of-living supplement is paid. Individual tables can also be reissued mid-year (the long-term-care income test AND cash amounts changed on 1 April 2026), so check the specific benefit page rather than trusting an update calendar. Always tell users to verify their case at btl.gov.il, the personal area at https://ps.btl.gov.il, or *6050. Amounts here follow the January 2026 benefits circular (`btl.gov.il/Publications/benefits_update/Documents/hozerkizba2026.pdf`) and contributions circular 1522.

## Instructions

### Step 1: Identify the Benefit Program
Map the user's situation to the correct program. The 13 main programs are listed in `references/benefit-programs.md`.

### Step 2: Check Eligibility
Each program has its own qualifying period; the full table is in `references/benefit-programs.md` under "Qualifying Periods". Key factors: residency status (תושב, with special rules for new immigrants), age, employment history (תקופת אכשרה), income (some benefits are means-tested), medical condition, and family status.

### Step 3: Estimate Benefit Amount
Use `scripts/calculate_benefits.py` for old-age pension, unemployment, maternity, child allowance, miluim, and birth-grant estimates (2026 rates).

### Step 4: File the Claim
Identify the form (`## Forms`) and the filing channel (`## Digital Channels`). Most claims are filed through the personal area at https://ps.btl.gov.il, which auto-generates the form-PDF.

### Step 5: Track and Appeal
Three appeal tracks (medical, non-medical, labor court). See `## Appeals` for deadlines and the right venue per decision type.

## Key Programs Detail

All amounts are **2026 official rates** (effective 01.01.2026 unless a different date is noted).

### Old Age Pension (Kitzbat Zikna)
- **Retirement age (גיל פרישה):** Men **67**. Women **62 to 65, by BIRTH YEAR**. Age 65 applies only to women born **1970 or later**, NOT to everyone born after 1960. Telling a woman born in 1962 to wait until 65 costs her two years of pension.
 Anchors: 62 up to birth-year 1959, 62y4m for 1960, 63 for 1962, 63y6m for 1964, 64 for 1966, 65 from 1970. Full year-by-year table in `references/benefit-programs.md`; confirm with the official calculator at btl.gov.il/benefits/old_age/Pages/RetirementCalculation.aspx.
- **Absolute eligibility age:** 70 for everyone; paid regardless of income.
- **Income test (retirement age to 70), work income, 2026:** a **graduated test, not an on/off switch**. Never tell a working pensioner their pension is "suspended" just because they have a salary.
  - No spouse: full below **10,113 NIS/month**; **partial** from 10,113 to **14,402**; none above 14,402. With a spouse: full below **13,484**; partial to **20,082**; none above 20,082.
  - Pension income (Israeli or foreign) is **not** counted. Passive income is tested separately. Any year withheld for income earns the **+5% deferral supplement** later.
- **Qualifying period:** 60 to 144 months of NI contributions (varies by age at immigration).
- **Basic amount (2026):** single 1,838 NIS; single aged 80+ 1,941 NIS; couple 2,762 NIS (single rate + 924 spouse increment); couple where the claimant is 80+ 2,865 NIS. Child supplements raise it further (single + 1 child 2,419; couple + 1 child 3,343; single + 2 or more 3,000; couple + 2 or more 3,924).
- **Supplements:** seniority (**+2% of the basic pension per full insured year, counted from year ONE**, not from year 11; BTL's example: 15 years = +30%; capped at 50%, reached at 25 years, so most pensioners reach ~2,757 NIS single), deferral (+5% per deferred year to 70, **compounded on the seniority-inflated pension**), children (581 NIS each, max 2), and income supplement for low-income pensioners.
- **Claim form:** **480** (תביעה לקצבת אזרח ותיק - זקנה). File at https://ps.btl.gov.il.

### Unemployment (Dmei Avtala)
- **Eligibility:** 12 of the last 18 months as a salaried employee, ended by termination not resignation.
- **Resignation penalty:** 90-day disqualification unless for justified cause (הרעת תנאים, relocation following a spouse, family care). The 5-day waiting period applies only to terminations.
- **Duration (2026):** set by age AND by dependants, where "dependants" means **3 or more dependent family members** (spouse, including same-sex, plus children), not "any dependants". Up to 25: 50 days (138 with 3+). 25-28: 67 (138). 28-35: 100 (138). 35-45: 138 (175). **45 and over: 175 unconditionally.** **Women aged 57 to 67 born in 1960 or later get 300 days**, usable over 18 months instead of 12; never quote them a 175-day ceiling. Two sub-bands: **ages 57 to 60** also have the daily benefit capped at **201.03 NIS from day 176** (and vocational training pays 100% but no more than 201.03/day; refusing training in the first 175 days costs a 90-day disqualification plus 30 days off the entitlement, leaving 270). Ages 60 to 67 get the 300 days without that day-176 cap. Discharged soldiers get 70 days in their first year. Full table in `references/benefit-programs.md`.
- **Amount:** Sliding scale tied to the average wage, capped at:
  - The replacement rate itself is capped by AGE: **60% of the wage under 28, 80% from 28**, degressive above ~5,000 NIS/month. BTL publishes two separate tables; applying the 28+ one to a 22-year-old overstates the benefit by a third.
  - Days 1 to 125: capped at 550.76 NIS/day in 2026. Days 126 onward: capped at 367.17 NIS/day (a claimant below the cap keeps their own lower rate, the 367.17 is not a floor).
- **Claim form:** **1500** (תביעה לדמי אבטלה) plus employer attachment **1514** (אישור המעסיק על תקופת ההעסקה והשכר).

### Maternity, Birth, and Parental Leave
- **Birth grant (ma'anak leida) 2026:** First child 2,103 NIS; second 946 NIS; third+ 631 NIS. Multiple births are banded: **twins 10,514 NIS, triplets 15,771 NIS, plus 5,257 NIS for each additional baby**. Paid as a one-time grant per birth. Hospitals normally file automatically when the mother provides her bank details on admission.
- **Maternity allowance (dmei leida) eligibility:** full 15 weeks with 10 of the last 14 (or 15 of the last 22) months as an employee or self-employed; a reduced 8 weeks with 6 of 14 (or 10 of 22).
- **Duration extras:** +3 weeks for multiple births; an extension if the newborn is hospitalized 15+ days; an equivalent for adoptive mothers. Under the Women's Employment Law an employee may add up to 11 unpaid weeks (26 total), only the first 15 BTL-paid.
- **Daily cap (2026):** 1,752.33 NIS/day. Calculation base: last 3 months ÷ 90 OR last 6 months ÷ 180, whichever is higher.
- **Father / partner (gimlat horim le'av):** 1 dedicated week; remaining weeks can be split between the parents.
- **Pregnancy preservation (shmirat herayon):** separate benefit when a doctor certifies the work environment is hazardous. Form 330 + medical certificate 331.
- **Claim forms:** mother **355**; father **354**, **360** (partner-week split); birth grant + maternity together **356**.

### Child Allowance (Kitzbat Yeladim)
- **Eligibility:** all Israeli residents with children under 18, usually automatic from the hospital report. Paid around the 20th monthly to the registered parent.
- **Amounts (2026, per child per month):** 1st child 173 NIS; 2nd to 4th 219 NIS each; 5th onward 173 NIS each.
- **Manual filing (rare):** form **5025**, only when not auto-registered (birth abroad, parent transfer, custody change).
- **Savings-for-every-child:** BTL auto-deposits 58 NIS/month per child until 18; parents may match from the child allowance (116 NIS total). Released at 18, or 21 with a bonus.

### General Disability (Nechut Klalit)
- **Distinct from work injury (nechut me'avoda)**: different program, different forms.
- **Eligibility:** resident aged 18 to retirement age whose condition reduces earning capacity by 60%, 65%, 74%, or 75-100%. Requires 12 months of NI residency before the disability.
- **Monthly amounts (2026):** full (75-100%) 4,711 NIS; 74% 3,211; 65% 2,894; 60% 2,718.
- **Family supplements are BANDED BY DEGREE, not flat.** Spouse: 1,518 / 1,123 / 987 / 911 NIS at 75-100% / 74% / 65% / 60%. Each child (max 2): 1,214 / 898 / 789 / 728 NIS on the same degrees. The spouse supplement also requires spouse gross income up to 7,848 NIS/month and no other benefit. Quoting the full-degree figure to a 60% claimant overstates by ~31%.
- **Special services (SHRM):** four tiers (2026): 50% = 1,943; 112% = 4,501; 188% = 7,181; 235% = 9,126 NIS. Supplements: ventilated at 188%+ adds 10,774; two caregivers adds 7,182 (neither pays with the 235% rate, nor with each other); a child under 3 adds 1,215 per child (max 2).
- **Disabled child (yeled nacheh): FIVE levels; 3,820 is the middle one, NOT the ceiling.** 1,943 / 3,820 / 4,501 / 7,181 / 9,126 NIS at 50 / 100 / 112 / 188 / 235%. Ventilated adds 10,774, but at 235% the child is paid the 188% rate (7,181) PLUS the supplement, not 9,126 + 10,774; two caregivers adds 7,182 on the same rule and cannot combine with the ventilated one. **A family with 2+ disabled children gets every child's rate raised by 50%.** Never tell a parent 3,820 is the maximum.
- **Claim forms:** **7801** (general disability claim), **7849** (special services), **7821** (disabled child).

### Work Injury (Pgi'at Avoda)
- **Eligibility:** Any worker injured on the job or commuting, covered from day 1 (no qualifying period). Self-employed must be registered with BTL before the injury.
- **Injury pay (dmei pgi'a):** 75% of the last 3 months' average wage for up to 91 days, capped at 1,314.25 NIS/day (2026). After 91 days a medical committee sets a permanent-disability degree (lump sum or pension).
- **Claim forms:** **211** (initial injury-pay claim, the "tofes 211"), **200** (permanent disability degree), **250** / **283** (medical-treatment authorization, employee / self-employed), **284** (employer declaration).

### Reserve Duty (Miluim)
- **Eligibility:** Any IDF reservist, covered from day 1. Claim window: 7 years from end of service.
- **Daily amount:** 100% of the last 3 months' average daily wage (gross ÷ 90; self-employed: prior-year assessment ÷ 90), capped at 1,730.33 NIS/day (2026, = 51,910 ÷ 30), minimum 328.76 NIS/day.
- **Annual bonus tiers (Iron Swords-era):** additional grants scale with cumulative reserve days per year. The tier table changes often, so look up the current one at btl.gov.il rather than quoting a figure.
- **Salaried employees:** Employer pays salary as usual; BTL refunds the employer via form 501. The employee receives the full salary.
- **Self-employed and sub-cap salaried:** File personal claim form **502**. Form **509** for advance payment.

### Long-term Care (Siyud)
- **Eligibility:** resident at retirement age needing substantial help with daily functions (washing, dressing, eating, mobility at home, continence), or constant supervision for medical reasons (assessed separately). Six dependence levels.
- **Income test (effective 1 April 2026):** graduated, with a 50%-reduced middle band. Single: full benefit up to 13,769 NIS/month, 50%-reduced from 13,769 to 20,654, none above 20,654. Couple: full up to 20,654, 50%-reduced to 30,980, none above 30,980. Income is measured over the 3 months before the claim; if BOTH spouses are care-dependent their incomes are summed and halved, and each is tested as a single.
- **Cash amounts (effective 1 April 2026):** a recipient may take part or all of the benefit in cash instead of care services. The maximum depends on the level AND on whether a foreign or Israeli caregiver is employed: level 1, 1,705 NIS either way; level 6, 6,448 NIS (foreign caregiver) or 7,440 NIS (Israeli caregiver). Full six-level table in `references/benefit-programs.md`. Do NOT quote the January-2026 figures, these were reissued on 1 April 2026.
- **Foreign caregiver (metapel zar):** interacts with the Population Authority permit, and the cash benefit can supplement the caregiver's wage.
- **Claim form:** **2600**; form **2655** to elect cash instead of services. Related skill: `israeli-elder-care-navigator` (assisted living, nursing homes).

### Income Support (Havtachat Hachnasa)
- **Eligibility:** Low-income residents who pass an asset test (no second home, car and savings below thresholds) and, if under 55, comply with the שירות התעסוקה employment test.
- **Monthly amounts (2026) vary by AGE and by FAMILY COMPOSITION. Never quote a single flat figure**, and never quote the single rate to a parent. Ages 25-54: single 2,076; couple 2,855; couple + 1 child 3,115; couple + 2 or more 3,478; single parent + 1 child 3,478; single parent + 2 or more **4,049**. Age 55 to retirement: single 2,596; couple 3,893; single parent + 2 or more 5,289. Ages 20-24: the register/exempt split applies only to a single (1,661 / 2,076) and a couple (2,284 / 2,855); the family rows are the same as the 25-54 band (couple + 1 child 3,115; couple + 2 or more 3,478; single parent + 1 child 3,478; single parent + 2 or more 4,049). A 22-year-old single parent of two gets 4,049, not 1,661. Above retirement age it equals the old-age pension with income supplement. Women born 1.1.1960 to 31.12.1964 get an extra 825 NIS/month from 62 to retirement age. Full table in `references/benefit-programs.md`.
- **Interactions:** not paid alongside unemployment; combines with old-age and disability supplements.
- **Claim form:** **5619** (תביעה לגמלת הבטחת הכנסה). Form **5521** for employer attachment if the claimant works part-time.

### Survivors Pension (Sheerim)
- **Eligibility:** Widow/widower of an insured person who had 12 months of NI in the last 18, OR 24 of the last 60, OR 60 months total. A widow qualifies at 40+, or with children, or with reduced earning capacity.
- **Monthly amount (2026) is banded by age and children, and these are BASE amounts: BTL pays a seniority supplement (and, for orphans, a subsistence supplement) ON TOP, so each figure is a floor, not the final answer.** Do NOT quote a flat 1,838. Widow/widower aged 40-50 with no children: **1,381 NIS**. Aged 50+ with no children: 1,838 NIS. Aged 80+: 1,941 NIS. With 1 child: 2,700 NIS. With 2 children: 3,562 NIS, plus 862 NIS for each additional child. A widow/widower who also draws an old-age pension and is entitled to half a survivors pension gets 919 NIS.

- **A widow/widower under 40 with no children gets NO monthly pension, but is not left with nothing:** a one-time **survivors grant (מענק שאירים)** worth **36 monthly survivors pensions** is paid instead. It also goes to a widower whose income later rises above the maximum, or whose child stops qualifying. A widower who was married to a non-working spouse (עקרת בית) is not entitled to the grant. Never tell such a claimant they have no claim.
- **The 12-month filing window is a RETROACTIVITY cap, not a forfeiture.** File within 12 months of the death to be paid from the date of death. Filing later does NOT destroy the entitlement: the pension is still granted, but back-payment is limited to 12 months. Never tell a late claimant they lost the pension.
- **Claim forms:** **410** (survivors pension claim), **416** (death grant + pension balance), **2910** (orphan maintenance).

### Mobility Allowance (Niyadut)
Two steps: form **8220** to the Ministry of Health (medical committee sets the % limitation), THEN form **8200** to BTL. Covers a loan for an accessible vehicle plus a monthly subsidy. Joint program with משרד התחבורה.

### Hostile-action Victims (Nifgaei Pe'ulot Eiva)
State-funded (not contribution-funded). Form **580** for recognition, **581** for the disability degree, **582** for the family of the deceased, **577** for psychological-injury intake.

### Employer Bankruptcy (Pshitat Regel shel Ma'asik)
BTL pays unpaid wages, severance, and unused vacation when the employer becomes insolvent, with its own caps. File once a court has issued the bankruptcy or liquidation order.

## Forms (טפסים)

BTL runs ~85 numbered claim forms. The full catalog is in **`references/forms.md`**. Most claims are filed through the personal area at **https://ps.btl.gov.il**, which auto-generates the form-PDF; PDF originals live under https://www.btl.gov.il/טפסים%20ואישורים.

> **Form 900 is NOT a benefit claim.** It is the "Personal Details Update" form (הודעה על עדכון פרטים אישיים), used by an existing beneficiary to change an address, marital status, or bank account.
>
> **Form 100 in BTL** is the opt-out from employer outreach, NOT an employer report. The 1500's employer attachment is form **1514**. The "100" accountants mean is a Tax Authority payslip summary.

### Most-used forms

| Need | Form | Filed by |
|---|---|---|
| Maternity allowance | 355 (or 356 with birth grant) | Mother |
| Old-age pension | 480 | Resident at retirement age |
| Unemployment | 1500 + employer 1514 | Laid-off employee + employer |
| Work injury (initial) | 211 | Injured worker |
| General disability | 7801 | Disabled adult |
| Reserve duty (personal) | 502 / employer 501 | Reservist / employer |
| Income support | 5619 | Low-income resident |
| Personal accident (non-work) | 2201 | Injured resident |
| Update address / bank / marital status | 900 | Existing beneficiary |

For any form not listed above, see `references/forms.md` for the complete catalog or search at https://www.btl.gov.il/טפסים%20ואישורים/FormSearch/Pages/default.aspx.

## Contribution Rates (2026)

NI is collected on income up to a monthly cap, in two brackets. **Full per-category tables (every age / pension / status row, the NI-health split, controlling shareholders, naturalized-over-62, household help, non-worker exemptions) are in `references/contribution-rates.md`. Read it before quoting a rate for anyone who is not a standard working-age employee.**

- **Reduced-collection step (מדרגת גביה מופחתת):** 7,703 NIS/month. **This is a statutory amount, NOT a percentage of the average wage.** The law fixes a base of 7,522 NIS, updated each 1 January by the **CPI** for 2026 to 2028, and by the average wage only from 2029. Do NOT recompute it as "60% of the average wage": that gives 8,261 and is wrong (7,703 is 56% of the 13,769 average wage). Use the published figure.
- **Maximum insurable income for contributions (תקרה):** 51,910 NIS/month.
- **Benefit ceiling (a different number):** 52,570 NIS/month (5 x the 10,514 basic amount). Contributions cap at 51,910, benefits at 52,570.
- **Average wage (§2, for benefits):** 13,769 NIS/month.

Standard working-age rates:

| Payer | Bracket 1 (up to 7,703) | Bracket 2 (7,703 to 51,910) |
|---|---|---|
| Employee (deducted from salary) | 1.04% NI + 3.23% health = **4.27%** | 7.0% NI + 5.17% health = **12.17%** |
| Employer (in addition to wage) | 4.51% | 7.60% |
| Self-employed | 4.47% NI + 3.23% health = **7.7%** | 12.83% NI + 5.17% health = **18.0%** |

> **Amendment 252 (תיקון 252):** the 2026 rates were set by Amendment 252, enacted 2025-01-14. Rates are CPI-indexed for 2026 through 2028 and switch to wage indexation from 2029.

Self-employed pay both shares and cannot claim unemployment; they can claim every other benefit.

### The rate depends on WHO is paying and WHO they are

The table above is the standard working-age case only. Applying it to anyone else is a material error. Totals per category (2026):

| Who | Reduced bracket | Full bracket |
|---|---|---|
| Employee, 18 to retirement age | 4.27% | 12.17% |
| Employee under 18, or on an old-age pension | **0%** (employer still pays 0.61% / 2.12%) | **0%** |
| Employee 67 to 70, not yet on a pension | 3.93% | 10.03% |
| Employee on a work-injury or disability pension | 3.23% (health only) | 5.17% |
| Self-employed, 18 to retirement age | 7.7% | 18.0% |
| Self-employed under 18 or on an old-age pension | 0.26% NI (pensioner health: flat 237 NIS/month off the pension) | 0.78% NI |
| Self-employed past retirement age, not on a pension | 6.92% | 15.79% |
| Early-pension recipient (pension payer withholds) | 4.25% | 11.96% |
| Non-working resident, no income | Minimum 266 NIS/month | -- |
| Household-help employer (on the worker's wage) | 6.05% employer + 2.8% worker = 8.85% | -- |

A woman between her retirement age and 67 who is not drawing a pension pays 3.95% / 10.24%. Controlling shareholders (בעל שליטה) and people naturalized after age 62 have their own lower rows. All of it is in `references/contribution-rates.md`.

### Multiple Employers and Coordination (Te'um Dmei Bituach)

Each employer applies the reduced bracket to the salary IT pays, so someone with two employers (or a salary plus an early pension) gets the reduced bracket twice and is over-deducted. The secondary employer (and an early-pension payer) must deduct at the FULL rate from the first shekel UNLESS the employee files a coordination request (te'um dmei bituach), through the secondary employer or as a refund claim after year-end. One of the most common over-payments for anyone with a second job or a gig plus a salary.

### Unpaid Leave (Chalat) and Non-Workers

- **Unpaid leave:** the **employer** pays contributions for the first 2 months (and may deduct them from the employee's wage). **From the 3rd month** a person not working as an employee or self-employed pays the non-worker minimum of **266 NIS/month** themselves; if they draw unemployment, BTL deducts it from the benefit. Gaps here break the qualifying period for later claims.
- **Non-working residents** owe a minimum of 266 NIS/month, and pay 12.09% / 12.17% on passive income above a 3,442 NIS/month exemption. **A non-working spouse (עקרת בית) is fully exempt and pays 0**, which is the single most common mistake here. Pensioners and people with both work and passive income are separate cases. Full table and exemptions: `references/contribution-rates.md`.

## Other Programs (Beyond the 13 Main Ones)

Real entitlements people miss. Route here when the question fits none of the 13 above. Eligibility in `references/benefit-programs.md`, forms in `references/forms.md`.

- **Alimony (mezonot), 5400** — a court alimony judgment the ex-partner is not paying: BTL pays, then collects from the debtor.
- **Personal-accident benefit (dmei te'una), 2201** — injured at home / on holiday / in leisure and unable to function, up to 90 days. NOT work or road accidents. Widely unknown, so it goes unclaimed.
- **Vocational rehabilitation, 270** — retraining and a stipend when earning capacity drops, or for a widow/widower.
- **Burial grant (460, exceptional cases)** and **death grant (416)** — the latter a one-off to the family of someone drawing an old-age, survivors, disability, or work-injury pension.
- **Study grant, discharged-soldier preferred-work grant, volunteer injury** — see the reference.

Do NOT confuse **ma'anak avoda (מענק עבודה, the EITC)** with a BTL grant: it is paid by the **Tax Authority**. **Sick pay** is paid by the **employer**, not BTL.

## Status, Obligations, and Debt

Every benefit runs through insured-resident status and a clean contributions record. This layer silently disqualifies people. Detail in `references/benefit-programs.md`.

- **Residency (toshavut) is the gateway.** Benefits belong to Israeli *residents*, not citizens as such. A long stay abroad can end residency; olim and returning residents need it restored. If the user lives abroad, just arrived, or works abroad for a foreign employer, residency is the first question, not the benefit.
- **Contribution gaps break claims.** An unpaid stretch (chalat past month 2, a non-working period, an unregistered self-employed period) can fail the qualifying period years later. Check the record in the personal area first. If the EMPLOYER never paid, the employee usually keeps the benefit: BTL pays and pursues the employer, and can pay a discretionary equity grant (form 20).
- **BTL debt is enforceable** but can be contested and settled, so never advise ignoring a demand. Overpaid benefits are clawed back from future payments. **Certificates are self-service** at https://ps.btl.gov.il.

## Digital Channels

1. **Personal area (preferred):** https://ps.btl.gov.il, most claims have full digital flows and certificates; the form-PDF is auto-generated from the wizard.
2. **Online forms portal:** https://www.btl.gov.il/טפסים%20ואישורים/tfasimMkuvanim/Pages/default.aspx, submit a filled PDF without logging in.
3. **Document upload:** https://b2b.btl.gov.il/BTL.ILG.Payments/DocumentsForm.aspx, for attachments to an open claim.
4. **MyBTL app** (iOS/Android). **Phone:** *6050 (WhatsApp same number; press 9 for English).
6. **Combined unemployment + employment-service form:** https://www.taasuka.gov.il/applicants/sharedform/, registers with שירות התעסוקה and files the 1500 in one step.
7. **Branch service:** book online, walk-ins are limited. Branch list at https://www.btl.gov.il/snifim.

## Appeals

| Decision type | Venue | Statutory deadline |
|---|---|---|
| Medical (disability degree, ADL test) | ועדה רפואית לעררים (medical appeals committee) | 60 days from decision |
| Non-medical eligibility / amounts | ועדת ערר (internal review) | 60 days |
| Final decisions (post-appeal) | בית הדין האזורי לעבודה (regional labor court) | 12 months from decision |

Free legal aid: הסיוע המשפטי, for low-income claimants.

## Examples

### Example 1: Maternity Leave
User says: "I'm pregnant and want to know about maternity leave benefits."
1. Confirm employment duration to determine 15 weeks vs 8.
2. Calculate the daily benefit with `python scripts/calculate_benefits.py maternity --salary X --months-employed Y` (capped at 1,752.33 NIS/day in 2026).
3. Mention the birth grant (2,103 NIS first child; 10,514 for twins) and the partner-week split, then direct to form 355 (or 356 combined) via ps.btl.gov.il.

### Example 2: Filing a Disability Claim
User says: "I have a chronic illness, how do I file a disability claim?"
1. Distinguish general disability (nechut klalit) from work-related (nechut me'avoda): different programs, forms, and funding.
2. File form 7801 at the personal area. The medical committee sets the incapacity degree (60% / 65% / 74% / 75-100%), paying 2,718 / 2,894 / 3,211 / 4,711 NIS per month in 2026.
3. If daily personal-care help is needed, also file 7849 for special services (SHRM).
4. Appeals: medical committee within 60 days for the degree; internal review for eligibility; labor court within 12 months.

## Bundled Resources

### Scripts
- `scripts/calculate_benefits.py`, estimate Bituach Leumi benefit amounts for old age pension, unemployment, maternity, child allowance, miluim, and birth grant. All hardcoded amounts reflect 2026 official rates. Subcommands: `pension`, `unemployment`, `maternity`, `child-allowance`, `miluim`, `birth-grant`. Run: `python scripts/calculate_benefits.py --help`.

### References
- `references/benefit-programs.md`, complete program catalog: 13 programs, 2026 rate table, qualifying-period table, contribution-rate tables, appeal deadlines, contact channels, claim-form quick lookup.
- `references/forms.md`, the full ~85-form catalog organized by program, with Hebrew names, who files each, and notes.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [pikud-haoref](https://agentskills.co.il/he/mcp/pikud-haoref) | Real-time emergency alerts (relevant for nifgaei pe'ulot eiva claims). |

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| January 2026 benefits circular (PDF) | https://www.btl.gov.il/Publications/benefits_update/Documents/hozerkizba2026.pdf | Every benefit amount for the year |
| Circular index (next year lands here) | https://www.btl.gov.il/Publications/benefits_update/Pages/default.aspx | Newer editions |
| Contribution rates hub | https://www.btl.gov.il/Insurance/Rates/Pages/default.aspx | Rates per payer type |
| Personal area (filing) | https://ps.btl.gov.il | Claims, forms, certificates |
| Retirement-age calculator | https://www.btl.gov.il/benefits/old_age/Pages/RetirementCalculation.aspx | Per-cohort retirement age |
| kolzchut BTL hub | https://www.kolzchut.org.il/he/המוסד_לביטוח_לאומי | Plain-Hebrew explanations |

Individual benefit pages carry the CURRENT table (including mid-year reissues). Check the benefit's own page before quoting an amount.

## Gotchas
- **7,703 is NOT 60% of the average wage.** It is a statutory amount (base 7,522, CPI-indexed each January through 2028). Deriving it as 0.6 x 13,769 gives 8,261 and mis-computes every payslip.
- The contributions ceiling (51,910) and the benefit ceiling (52,570) are different numbers. Swapping them skews maternity and injury calculations.
- Employee, self-employed, non-worker and early-pension recipients are four DIFFERENT rate tables (an early pensioner: 4.25% / 11.96%; a self-employed pensioner: 0.26% / 0.78% NI, not 7.7% / 18%).
- Self-employed pay both shares (7.7% / 18.0%) and get NO unemployment.
- **Income tests are graduated bands, not cliffs.** A single pensioner keeps the FULL pension below 10,113 NIS of work income, a partial pension to 14,402, and loses it only above (with a spouse: 13,484 / 20,082); pension income is not counted. Siyud has a 50%-reduced middle band.
- **Survivors amounts are banded.** A childless widow/widower aged 40-50 gets 1,381 NIS, not 1,838. Under 40 with no children there is no monthly pension but a one-time survivors grant, so never say "you get nothing". The 12-month window caps retroactivity, it does not forfeit the pension.
- **Income support is banded by age** (single: 1,661 at 20-24 registering, 2,076 at 25-54, 2,596 from 55). Quoting the lowest figure to a 30-year-old makes an eligible person conclude they do not qualify.
- Amounts are reissued on **1 January**, not twice a year, but a single table can be reissued mid-year (the siyud income test AND cash amounts changed on 1 April 2026). Check the benefit's own page.
- The forms path uses a SPACE, not a hyphen: `btl.gov.il/טפסים ואישורים/...` (%20). The hyphenated URL 404s.
- Women's retirement age is **65 only from birth-year 1970**. A woman born 1962 retires at 63, born 1966 at 64. Quoting 65 to all of them costs real pension years.
- **Almost every amount here is BANDED, so ask what it varies by before quoting it.** Disability supplements vary by degree (spouse 1,518 down to 911), the disabled-child allowance has five levels (1,943 to 9,126, so 3,820 is NOT the ceiling), income support varies by age AND family composition, survivors by age AND children, siyud cash by level AND caregiver nationality. Quoting the headline figure to someone in a different band is this domain's most common and most costly error.
- "Ma'anak avoda" (EITC) is a Tax Authority grant, and sick pay comes from the employer. Neither is BTL.

## Troubleshooting

### Error: "Not enough qualifying months"
Cause: insufficient contribution history (תקופת אכשרה).
Solution: check the per-program qualifying-period table in `references/benefit-programs.md`. Military service, maternity leave and miluim count as qualifying months. Olim have special rules; for old-age the 60-month minimum can be waived via מענק מותנה.

### Error: "Benefit amounts don't match expected values"
Cause: BTL reissues benefit amounts each 1 January, and individual tables are sometimes reissued mid-year (the long-term-care income test was reissued effective 1 April 2026).
Solution: Verify against the current benefits circular at https://www.btl.gov.il/Publications/benefits_update/Pages/default.aspx (the January 2026 edition is `Documents/hozerkizba2026.pdf`), against the specific benefit page, or via *6050. Amounts in this skill follow the January 2026 circular.

### Error: "Form not found at the URL I tried"
Cause: the forms path uses a SPACE, not a hyphen. The hyphenated form 404s; the live path is `btl.gov.il/טפסים ואישורים/...` (encoded `%20`).
Solution: use the form-search at https://www.btl.gov.il/טפסים%20ואישורים/FormSearch/Pages/default.aspx. PDF originals are at `btl.gov.il/טפסים%20ואישורים/Documents/T<form-number>.pdf` (e.g. `T355.pdf`).

### Error: "I resigned and was denied unemployment"
Cause: Voluntary resignation triggers a 90-day disqualification.
Solution: If the resignation was for justified cause (relocation following spouse, family-care, hazardous-conditions, deterioration of work conditions, fixed-term contract end), file an appeal with form 7810 within 60 days. Document the cause carefully.
