---
name: israeli-miluim-manager
description: Comprehensive guide to Israeli reserve duty (miluim) rights, compensation, tax benefits, employer obligations, IDF Aka grants, Ministry of Defense disability track, and family support. Use when a reservist, employer, or family member needs help understanding miluim entitlements, filing for Bituach Leumi compensation (tagmul nosaf, tagmul meyuchad, salary reimbursement), claiming the IDF 6.2B grants stack (Manak Mishpacha Mugdal, Manak Hashlama LeNofesh, digital wallet), recognizing service-connected injury or PTSD via Misrad HaBitachon (Aka 8944), navigating Amendment 283 combat tax credits (17 tiers, up to 4.0 credit points), Amendment 253 BL income basis fixes, Bank Israel mortgage and loan relief, student tuition refunds, or post-service employment protections (tiered 30 or 60-day dismissal ban, permanent 20% employer compensation). Do NOT use for active-duty (sherut sadir) conscription, draft deferral policy, or career military (keva) matters.
license: MIT
compatibility: Requires Claude Code or compatible AI coding agent
---


# Israeli Miluim Manager

## Instructions

### Step 1: Reserve Duty Basics

Israeli reserve duty (miluim, מילואים) is compulsory military service for citizens who have completed their regular service (sherut sadir, שירות סדיר).

| Term | Hebrew | Description |
|------|--------|-------------|
| Miluim | מילואים | Reserve duty service |
| Tsav 8 | צו 8 | Emergency call-up order |
| Tsav Kriah | צו קריאה | Routine call-up notice |
| Keva | קבע | Career military (not miluim) |
| Mashak Tash | משק ת"ש | Welfare NCO (handles hardship requests) |
| Aka | אכ"א | IDF Personnel Directorate |
| Ishur Lochem | אישור לוחם | Combat confirmation (required for Amendment 283 credit) |

**Who serves (temporary order, valid through June 30, 2027):**
- Men (non-officers) up to age 41, officers up to age 46
- Special professions (drivers, pilots, physicians) up to age 49-50
- Women in specific roles until age 38 (combat roles to equivalent male age)
- Single women without children to age 24 (age 34 in special professions)
- Exemptions: medical, religious study (hesder/yeshiva), single parents

**Call-up process:**
1. Receive Tsav Kriah or Tsav 8 via mail, phone, or IDF systems
2. Report to designated base on the specified date
3. Service: routine training (1-4 weeks/year) or extended during operations
4. On release, receive Form 3010 confirming service dates
5. Combat reservists also need Ishur Lochem for Amendment 283 tax credit tiers

### Step 2: Employment Protections

Israeli law provides strong employment protections for reservists under the Reserve Duty Compensation Law (Chok Tagmulei Miluim, חוק תגמולי מילואים) and the Military Service Law.

| Protection | Details (2026) |
|------------|----------------|
| Job preservation | Employer must hold the reservist's position during service |
| Dismissal ban (post-service, under 60 days served) | 30 days after return from service |
| Dismissal ban (post-service, 60+ days served) | 60 days after return (permanent law since 2026) |
| Dismissal ban (pre-service) | Cannot fire employee due to upcoming miluim call-up |
| Seniority | Service period counts toward seniority and tenure |
| Pension contributions | Employer must continue pension deposits during service (sechar kove'a = pre-service salary) |
| Keren hishtalmut | Employer must continue keren hishtalmut deposits during service |
| Work conditions | Must return to same role, same terms, same pay |
| 20% social contribution compensation | State compensates private employers 20% of salary for social contributions (permanent since 2026, anchored via NII Law amendment April 27, 2026) |

**Key changes for 2026:**
- The 60-day post-service protection that was a wartime temporary order has been **made permanent law** for reservists serving 60+ days. Reservists serving fewer than 60 days receive the standard 30-day protection.
- The 20% employer compensation for social contributions was applied retroactively to January 2026 and was anchored as permanent law via an amendment to the National Insurance Law approved by the Knesset plenum on April 27, 2026.
- The wartime supplementary employer compensation (for hiring temp replacements) has expired.

**Public-sector employees:** Public employers (state, local authorities, public corporations) are explicitly excluded from the 20% social-contribution refund. State employees fall under Takanon HaSherut HaTziburi (Civil Service Code) with collective agreements that may override default labor law on seniority and leave.

**Filing a complaint:**
If an employer violates these protections, the reservist can file a complaint with the Labor Court (Beit Din LaAvoda, בית דין לעבודה). Filing fee is 1% of the claim amount, minimum NIS 168 (expedited procedure 0.5% / NIS 84). Many common labor claims (wages, overtime, holiday pay, vacation pay) are exempt from filing fees.

### Step 3: Compensation Through Bituach Leumi

Bituach Leumi (ביטוח לאומי, National Insurance Institute) compensates reservists through three distinct payment tracks. Conflating them is a common cause of users believing they have been underpaid.

| Track | Hebrew | What It Is | Who Gets It |
|-------|--------|-----------|-------------|
| Salary reimbursement (**Bituach Leumi**) | תגמולי מילואים | Replaces lost income during service | All reservists; employer-mediated for employees, direct for self-employed |
| Tagmul Nosaf (**paid by the IDF, NOT BTL**) | תגמול נוסף | Annual recognition payment for any year with 10+ days of reserve duty | Paid automatically by 1 May of the following year, straight to the bank account registered with the unit |
| Tagmul Meyuchad (**paid by the IDF, NOT BTL**) | תגמול מיוחד | Special payment for **32 to 60** cumulative shamap days in a year (and for service beyond 60 days under Tzav 8) | Days served on Tzav 8 between 07.10.2023 and 31.12.2025 count toward the threshold |

**Only the salary reimbursement is a Bituach Leumi payment.** Tagmul Nosaf and Tagmul Meyuchad are IDF payments under the Reserve Service Law. Do NOT route a user to the BTL portal or *6050 for them: they are paid automatically by 1 May to the bank account registered with the unit, and discrepancies go to the **IDF miluim hotline, 1111 extension 4** (then 1 for unit-tier questions).

**Salary-reimbursement compensation basis:**

| Component | Details |
|-----------|---------|
| Income basis | Average income from 3 months before service (see Amendment 253 below for repeat reservists) |
| Maximum daily rate | NIS 1,730.33/day (NIS 51,910/month equivalent, 2026 ceiling) |
| Minimum daily rate | NIS 328.76/day (NIS 9,863/month equivalent, 2026 floor) |
| Payment timing | Employer advances salary, then claims reimbursement from Bituach Leumi |
| Self-employed | File directly with Bituach Leumi |

**Daily compensation, and the 40% supplement rule everybody gets wrong:**

```
dailyTagmul = clamp(3-month gross / 90, 328.76, 1730.33)     // the cap applies to the DAILY rate
paidDays    = serviceDays + supplement(serviceDays mod 7)     // see the remainder table below
total       = dailyTagmul x paidDays
```

**The 40% supplement is NOT paid on every day.** BTL divides the service days by 7 and pays the supplement only on the REMAINDER:

| Remainder (days mod 7) | Supplement |
|---|---|
| 0 | none |
| 1 | +0.4 day |
| 2 | +0.8 day |
| 3 | +1.2 days |
| 4 | +1.6 days |
| 5 | +2.0 days |
| 6 | **+1 day** |

BTL's own worked example: 20 days = 14 + a remainder of 6, so the reservist is paid for **21** days. And **21 days of service pays exactly 21 days** (remainder 0, no supplement at all). Multiplying every day by 1.4 overstates a 21-day call-up by 40% (11,760 instead of 8,400 at a 400/day rate). Source: btl.gov.il "סכום התגמול", חישוב תוספת 40%.

**Self-employed:** an additional 25% compensation on top of the tagmul — but **the combined daily total may never exceed the maximum tagmul** (1,730.33/day). BTL: "סכום התגמול והפיצוי יחד, לא יעלה על התגמול המקסימלי".

**Self-employed income basis:** BTL computes it from the **gross advance payments (מקדמות) you reported to BTL** for the 3 months before service, divided by 90 (the monthly advance = annual gross income / 12), and recomputes once the final tax assessment arrives. It is NOT "net income for the 3 months".

**Amendment 253 (from 01.05.2025) breaks the plain 3-month average for repeat reservists:** prior miluim pay is excluded from the next basis, a "fixed base" from the quarter before first emergency-period service is locked in, and Section 279 lets the reservist pick the more favourable basis when the gap is under 60 days. Detail in `references/bituach-leumi-filing-guide.md`.

**How to file salary reimbursement:** employees — the employer claims via the BTL employer portal (Form 501 + Form 3010) and is reimbursed within 30-60 days while the employee keeps drawing normal salary. Self-employed — **BTL usually pays automatically** from the IDF's data, with no claim at all; file a personal claim (Form 502) only if nothing has arrived within 3 weeks of discharge. Step-by-step in `references/bituach-leumi-filing-guide.md`.

**Employer refuses to pay — file Form 502, not 510:**
If the employer refuses to advance salary, the reservist files **Form 502 (תביעה אישית לתגמולי מילואים)** with Bituach Leumi and is paid directly. This is in addition to (not a replacement for) a Beit Din LaAvoda complaint against the employer.

**Do not confuse the reserve-duty forms:** **502** = the reservist's personal claim; **501** = the employer's reimbursement claim; **509** = advance request; **510** = the EMPLOYER's wage confirmation. Telling a reservist whose employer refuses to cooperate to "file Form 510" sends them to a form only that employer can complete.

**Minimum compensation top-up:**
Reservists earning below the minimum compensation floor (NIS 9,863/month in 2026) receive a top-up from Bituach Leumi to reach that floor during service months. Applied automatically.

**Tagmul Nosaf (annual recognition payment):**
Every reservist with 10+ qualifying days in a tax year receives an annual additional payment, paid by the **IDF** (not Bituach Leumi) by **1 May** of the following year, straight to the bank account registered with the unit. Separate from salary reimbursement. If it has not arrived, contact the **IDF miluim hotline at 1111 extension 4** — not *6050. If the bank account changed, update the IDF payments administrator.

**Tagmul Meyuchad (special payment) — starts at 32 days, and the daily rate is BANDED:**
Paid by the **IDF** (not BTL) to reservists who did **32 to 60** cumulative shamap days in a calendar year, and for service beyond 60 days under Tzav 8. Days served on Tzav 8 between 07.10.2023 and 31.12.2025 count toward the threshold. Telling a reservist with 32-59 days that they are not eligible costs them the whole payment.

The daily rate is **not a flat 133.33**: for 2026 it is banded by the unit's activity tier (מדרג א'+ 133 / א' 113 / ב' 86 / ג' 60 / ד' 40 / ה' 30 NIS per shamap day). Full table in `references/bituach-leumi-filing-guide.md`.

To find the unit's tier, call the IDF miluim hotline **1111, extension 4, then 1**. Commanders receive the payment for days beyond 60 as well, and age-exempt reservists (מוחרגי גיל) receive it from their FIRST shamap day. The payment is income-tax-free.

### Step 4: 2026 Tax Benefits for Combat Reservists

Amendment 283 to the Income Tax Ordinance (Section 39B), passed by the Knesset on November 19, 2025 and published in Sefer HaChukim on November 23, 2025, introduced a graduated tax credit system for **combat reservists** based on days served. These apply to tax years 2026-2027 and are managed through the Israel Tax Authority (Rashut HaMisim, רשות המסים).

**Important:** These credits apply ONLY to **combat days** (yamei lochem), starting at 30. Under 30 combat days, and non-combat service, get NO Amendment 283 credit, and there is no separate "standard reservist" point (every resident already gets 2.25 base points; the combat credit is added on top, only for 30+ confirmed combat days with ishur lochem).

| Combat Service Days Per Year | Credit Points | Annual Credit Value (NIS) |
|------------------------------|---------------|---------------------------|
| Under 30 days, or non-combat | none | 0 (no Amendment 283 credit) |
| 30-39 days | 0.50 | 1,452 |
| 40-49 days | 0.75 | 2,178 |
| 50-54 days | 1.00 | 2,904 |
| 55-59 days | 1.25 | 3,630 |
| 60-64 days | 1.50 | 4,356 |
| 65-69 days | 1.75 | 5,082 |
| 70-74 days | 2.00 | 5,808 |
| 75-79 days | 2.25 | 6,534 |
| 80-84 days | 2.50 | 7,260 |
| 85-89 days | 2.75 | 7,986 |
| 90-94 days | 3.00 | 8,712 |
| 95-99 days | 3.25 | 9,438 |
| 100-104 days | 3.50 | 10,164 |
| 105-109 days | 3.75 | 10,890 |
| 110+ days | 4.00 | 11,616 |

One credit point (nekudat zikui) = NIS 242/month = NIS 2,904/year (2026 value, frozen through 2027).

**From tax year 2028:** The minimum qualifying threshold drops from 30 days to **20 days** (20 days = 0.75 credit points, +0.25 per additional 5 days, max 4 points). Reservists planning service across 2027-2028 should account for this when projecting credits.

**How to claim tax credits:**
1. Obtain **two** confirmations from IDF (both can be downloaded from miluim.idf.il):
   - Service confirmation (ishur sherut miluim, אישור שירות מילואים) for general reservist credit
   - Combat confirmation (ishur lochem, אישור לוחם) for the Amendment 283 tier credits. The Tax Authority will reject combat tier claims without the lochem confirmation, even if service days qualify
2. Submit annual tax credit form (tofes 101, טופס 101) to employer, or file directly with Rashut HaMisim
3. Credits applied to monthly payroll deductions or as annual refund

**Combat day classification:** The unit commander (mefakedet yechida) determines combat-day classification. Reservists who believe their classification is wrong (especially for hybrid units like Yamam, GSS operational support, or specialized teams) can challenge it through the unit and the Reserve Branch.

### Step 5: IDF Aka Grants and Keren HaSiyua

Government Resolution from January 25, 2026 created a 6.2 billion NIS support package for reservists, administered by the IDF Personnel Directorate (Aka) through Keren HaSiyua LeMishartei HaMiluim (קרן הסיוע למשרתי המילואים). These grants are paid by the IDF, not by Bituach Leumi or the Tax Authority. They are the most-asked-about and most-frequently-missed benefits.

| Grant | Hebrew | Eligibility | Amount |
|-------|--------|-------------|--------|
| Manak Mishpacha Mugdal | מענק משפחה מוגדל | Reservists with 40+ days and at least one child age 14 or under | Graduated by accumulated days |
| Manak Hashlama LeNofesh | מענק השלמה לנופש | Vacation supplement | Up to NIS 4,500 |
| Manak Mishpacha LeYeled Mugbal | מענק לילד מוגבל | Parents of children with disabilities, 45+ days served | NIS 2,000 |
| Manak Ha'avarat Dira | מענק העברת דירה | Reservists who moved during/around extended service, 45+ days served | NIS 2,500 (rank-based: A+/A/B) |
| Digital Wallet | ארנק דיגיטלי | Cumulative reserve days from day 10 onward | Up to NIS 5,000 |
| Tutoring Fund (students) | קרן שיעורים פרטיים | Reservists in higher education | Up to NIS 3,000 (combat) / NIS 2,000 (rear) |

**How to claim Aka grants:**
1. Log in to miluim.idf.il (the IDF reservist portal)
2. Update personal status (married, children, location, education status under "miktzo'a ezrachi" not "haskala") so eligibility is computed correctly
3. Eligible grants appear in the "Manakim VeHatavot" tab
4. Some grants are paid automatically; others require submitting a request with supporting documents
5. Digital wallet credits accrue automatically once the reservist passes the day-10 threshold

### Step 6: Service-Connected Injury and PTSD: The Misrad HaBitachon Track

**Critical distinction:** Injuries sustained during reserve duty (physical or mental) go to the **Ministry of Defense Rehabilitation Department (Agaf HaShikum, אגף השיקום)**, NOT Bituach Leumi. Filing with the wrong agency is the single most common cause of denied claims.

| Severity | Disability Tier | Outcome |
|----------|----------------|---------|
| Minor injury (achuz nechut 1-9%) | No formal recognition | No payment |
| Moderate injury (achuz nechut 10-19%) | Recognized | One-time lump sum |
| Significant injury (achuz nechut 20%+) | Recognized | Lifetime monthly pension + medical benefits + possible mobility/housing benefits |

**PTSD and combat trauma:**
- The IDF Combat Reactions Unit (Yechidat Tguvot Krav, יחידת תגובות קרב) operates a 24/7 hotline at **8944** (from any Israeli phone). Free trauma diagnosis and treatment, no disability finding required.
- Reservists who served in combat conditions are eligible for free therapy through Keren HaSiyua even before any disability claim is filed.
- Formal recognition as a disabled IDF veteran (nechei tzahal) yields lifetime benefits and is processed by Agaf HaShikum at Misrad HaBitachon.

**How to file a disability claim:**
1. Document the injury or trauma during or immediately after service (medical records, unit reports)
2. Submit a claim through the Agaf HaShikum portal at hachvana.mod.gov.il
3. A medical committee (va'ada refuit) determines disability percentage
4. If 10%+, benefits begin; appeals route through internal MoD process and ultimately the District Court (not Beit Din LaAvoda)

**Bereavement (mishpachot shchol):** Families of fallen reservists are eligible for the same MoD pension, housing, and orphan-education benefits as families of fallen regular soldiers under Chok HaMishpachot. Contact MoD Mishpachot ShChol unit directly.

### Step 7: Self-Employed Reservists and Manak Nezek Akif

Self-employed reservists have two distinct claims, and they stack:

1. **Reserve-duty compensation (BTL).** Basis = the gross advances (מקדמות) reported to BTL for the 3 months before service, divided by 90; recomputed once the final tax assessment lands. BTL usually pays this **automatically** from IDF data — file Form 502 only if nothing arrives within 3 weeks of discharge. A 25% compensation is added on top of the tagmul, but the combined daily total may never exceed the maximum tagmul (1,730.33/day).
2. **Indirect-damage business compensation (Tax Authority).** A separate scheme with its own gates and deadlines. Route the user to `israeli-business-war-compensation` — do not attempt the calculation here.

Full self-employed filing detail: `references/bituach-leumi-filing-guide.md`.

### Step 8: Vacation Days, Spouse Protections, and Family Support

Reserve service does NOT consume vacation days, and an employer may not force a reservist to take leave for it. The reservist's spouse gets dismissal protection scaled to the reservist's own (up to 60 days post-service where the reservist served 60+ days). Family-support grants (childcare, spouse-employment assistance) run through the IDF's Keren HaSiyua, not BTL. Detail and the current grant table: `references/2026-law-changes.md`.

### Step 9: Bank Israel Relief and Practical Accommodations

Bank Israel maintains a relief framework for reservists, renewed periodically during operational periods.

| Relief | Details |
|--------|---------|
| Mortgage payment deferral | Up to 3 months interest-free |
| Consumer loan deferral | Up to NIS 100,000 |
| Business loan deferral | Up to NIS 2,000,000 |
| Overdraft discount (employees) | 1% for reservists with salary transfer at major banks |
| Overdraft for self-employed | Automatic NIS 30,000 interest-free |
| Driver's license renewal | Misrad HaRishui accommodations during service |

**How to claim:** contact bank during or after service with Form 3010; ask for sherut lakuchot miluim. Verify current terms on bankisrael.org.il.

### Step 10: Students in Higher Education

For tashpa"u (academic year 2025-26): the IDF and the Council for Higher Education (VATAT) operate a tuition refund program (Hesder Miluim VATAT). 50+ qualifying days between Oct 23, 2025 and Sep 30, 2026 = up to 100% tuition refund.

| Days Served (qualifying) | Benefit |
|--------------------------|---------|
| 30-60 days | -6 academic credit reduction (NIS"Z) |
| 61-99 days | -8 academic credit reduction |
| 100+ days | -10 academic credit reduction |
| 50+ days | Up to 100% tuition refund |
| Any qualifying service | Free tutoring up to NIS 3,000 (combat) / NIS 2,000 (rear) via Keren HaSiyua |

**How to claim:**
1. Update IDF portal status: under "miktzo'a ezrachi" (NOT "haskala") with student details and institution
2. Tuition refund flows from VATAT to the institution; the institution credits the student
3. Tutoring fund applied for through miluim.idf.il "Manakim VeHatavot" tab

## Examples

### Example 1: Employee Called Up for 45-Day Combat Reserve Duty
User says: "I received a tsav kriah for 45 days of miluim as a combat reservist. What are my rights at work?"
Actions:
1. Confirm employer must hold position and continue salary during 45-day service
2. Explain employer claims salary reimbursement from Bituach Leumi, plus 20% state compensation for social contributions
3. Note 30-day post-service dismissal protection upon return (under 60 days served), with spouse protection scaled accordingly
4. Calculate Amendment 283 tax credit eligibility: 40-49 day tier = 0.75 credit points = NIS 2,178/year (only with ishur lochem)
5. Confirm Tagmul Nosaf will be paid in May next year (annual recognition payment)
6. Note digital wallet eligibility (accrues from day 10) and check miluim.idf.il for Aka grants
Result: Employee understands full rights, employer obligations, exact tax credit value, and Aka grant access path.

### Example 2: Self-Employed Reservist Filing for Compensation
User says: "I am a freelancer and just finished 3 weeks of miluim. How do I get compensated?"
Actions:
1. Guide through Bituach Leumi personal portal login
2. Submit Form 510 with Form 3010 attached
3. Calculate expected compensation based on 3-month average income (note Amendment 253 if this is a repeat service)
4. Check if income is below NIS 9,863/month floor for automatic top-up
5. Confirm Tagmul Nosaf eligibility (any year with 10+ days = automatic payment in May)
6. Check Manak Nezek Akif filing window for the relevant period at gov.il
7. Confirm self-funded keren hishtalmut deposit if maintaining the 6-year clock
Result: Freelancer files claim, receives compensation directly from Bituach Leumi, captures Manak Nezek Akif and Tagmul Nosaf.

### Example 3: Employer Asking About Obligations
User says: "One of my employees was called up for miluim. What do I need to do?"
Actions:
1. Explain salary advance obligation during service (sechar kove'a = pre-service salary)
2. Detail pension and keren hishtalmut continuity requirements
3. Note the state reimburses 20% of salary for social contributions (private employers only; permanent since 2026, anchored by NII Law amendment April 27, 2026)
4. Explain dismissal ban: 30 days post-service for service under 60 days, 60 days for 60+ days
5. Note spouse protections: 1-hour paid absence per day during 5+ consecutive days of service, up to 8 paid leave days for spouses with a child under 14
6. Guide through Bituach Leumi employer portal for salary reimbursement
7. If the employer is public sector, note the 20% refund does not apply
Result: Employer complies with all legal obligations and claims proper reimbursement.

## Bundled Resources

### References
- `references/2026-law-changes.md` -- Detailed breakdown of all 2026 changes to reserve duty law. Covers the new permanent 20% employer compensation (anchored April 27, 2026 NII amendment), tiered dismissal protection (30/60 days), Amendment 283 tax credit tiers, Amendment 253 BL income basis fixes, Aka 6.2B grants stack from Government Resolution Jan 25, 2026, Misrad HaBitachon disability path, and expired wartime provisions. Consult when a user asks what changed in 2026, whether a wartime provision is still in effect, or how the 2026 framework differs from wartime measures.
- `references/bituach-leumi-filing-guide.md` -- Step-by-step guide for filing all three Bituach Leumi reserve duty payments (salary reimbursement, Tagmul Nosaf, Tagmul Meyuchad), plus the joint Tax Authority + Aka Manak Nezek Akif grant for self-employed. Includes Form 510 fallback for employees whose employer refuses to pay, common rejection reasons, and Amendment 253 income basis adjustments. Consult when a user needs to file a compensation claim or troubleshoot a rejected claim.

### Scripts
- `scripts/miluim-tax-credit-calculator.py` -- Estimates Amendment 283 combat tax credits for 2026-2027 based on combat days served and monthly income. Uses the 17-tier system, calculates credit points and annual credit value, flags 2028 threshold drop. Run: `python scripts/miluim-tax-credit-calculator.py --help`

## Recommended MCP Servers

| MCP | What It Adds |
|-----|--------------|
| [Kolzchut (All-Rights)](https://agentskills.co.il/he/mcp/kolzchut) | Direct access to Israel's authoritative rights and entitlements knowledge base; covers tagmul nosaf, tagmul meyuchad, miluim taxation, and all benefits referenced here |
| [Data.gov.il Advanced](https://agentskills.co.il/he/mcp/data-gov-il) | Access to Israeli government datasets including Bituach Leumi reference data; useful for cross-checking benefit amounts and eligibility tables |

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Bituach Leumi reserve duty payments | https://www.btl.gov.il/benefits/Reserve_Service/Pages/default.aspx | Current daily/monthly rates, tagmul nosaf, tagmul meyuchad |
| IDF reservist portal | https://miluim.idf.il | Aka grants, Keren HaSiyua, ishur sherut, ishur lochem, digital wallet |
| Keren HaSiyua LeMishartei HaMiluim | https://www.miluim.idf.il/articles-list/קרן-הסיוע-למשרתי-המילואים/ | Manak Mishpacha Mugdal, Manak Hashlama LeNofesh, all Aka grants |
| Misrad HaBitachon Rehabilitation | https://www.hachvana.mod.gov.il | Disability claims, PTSD recognition, lone soldier benefits |
| Manak Nezek Akif grant (gov.il) | https://www.gov.il/he/service/grant-for-reservists | Self-employed indirect-damage grant filing |
| Kolzchut combat tax credits | https://www.kolzchut.org.il/he/נקודות_זיכוי_ממס_הכנסה_ללוחמי_מילואים | Amendment 283 17-tier table, qualifying conditions |
| Knesset Amendment 283 announcement | https://main.knesset.gov.il/News/PressReleases/pages/press19112025f.aspx | Original legislation |

## Gotchas
- Reserve duty has THREE separate Bituach Leumi tracks (salary reimbursement, Tagmul Nosaf, Tagmul Meyuchad) plus IDF Aka grants and the Tax Authority Manak Nezek Akif. Agents conflate them, so users think they were paid when a track is still owed.
- Service-connected injuries and PTSD go to Misrad HaBitachon (Agaf HaShikum), NOT Bituach Leumi; filing with the wrong agency is the top cause of denied claims. Aka 8944 is the hotline; recognition via hachvana.mod.gov.il.
- Amendment 283 combat tax credit tiers require **ishur lochem** (combat confirmation), not just **ishur sherut miluim** (service confirmation). The Tax Authority will reject combat tier claims without lochem confirmation, even if the day count qualifies.
- **The 40% supplement is a REMAINDER rule, not a flat uplift.** Divide the service days by 7; only the remainder earns the supplement (remainder 0 = nothing, so 7 / 14 / 21 days earn no supplement at all; remainder 6 = +1 day). "Monthly / 30 x days" is therefore CORRECT for 21 days (12,000/mo -> 400/day -> 8,400), and multiplying every day by 1.4 overstates it by 40%. Self-employed get an ADDITIONAL 25%, but the combined daily total may never exceed the maximum tagmul (1,730.33/day). Amendment 253 also breaks the plain 3-month average for repeat reservists.
- **Tagmul Nosaf and Tagmul Meyuchad are IDF payments, not Bituach Leumi ones.** They arrive automatically by 1 May; chase them at the IDF hotline 1111 ext. 4, never at *6050. Tagmul Meyuchad starts at 32 cumulative shamap days (not 60) and its daily rate is banded by unit tier (133 / 113 / 86 / 60 / 40 / 30), not a flat 133.33.
- **Form 510 is the EMPLOYER's wage confirmation.** The reservist's personal claim is Form 502. Sending a reservist whose employer refuses to cooperate to "file 510" sends them to a form only that employer can file.
- The 20% employer social contribution refund applies to PRIVATE employers only (public sector excluded).
- Aka grants from miluim.idf.il are paid by the IDF, not Bituach Leumi or Rashut HaMisim. Reservists must update their portal status (married, children, education under "miktzo'a ezrachi") for eligibility to compute correctly.
- Manak Nezek Akif (self-employed) has short rolling filing windows; missing one forfeits the grant. It is a cash grant, not a tax deduction.
- Dismissal protection: 30 days for under-60-day service, 60 days for 60+; spouse protection scales with the tier.
- Tagmul Nosaf is paid in May of the FOLLOWING year, not at end of service. The 2028 combat-tier threshold drops from 30 to 20 days.

## Troubleshooting

### Error: "Employer refuses to advance salary during miluim"
Cause: Employer may be unaware of legal obligation, facing cash flow issues, or acting in bad faith.
Solution:
1. Cite the Reserve Duty Compensation Law requiring salary advancement
2. Remind employer that Bituach Leumi reimburses the full amount, plus 20% for social contributions (if private sector)
3. **Fallback:** File Form 510 with Bituach Leumi directly as if self-employed and receive compensation directly. This is independent of any complaint against the employer.
4. File complaint with the Labor Court (Beit Din LaAvoda). Filing fee is 1% of claim, minimum NIS 168 (many common labor claims are exempt from fees)

### Error: "Bituach Leumi rejected compensation claim"
Cause: Missing or incorrect Form 3010, income documentation gaps, BL arrears blocking payout, or filing deadline exceeded.
Solution:
1. Verify Form 3010 dates match actual service period
2. Ensure income documentation covers the 3 months before service (or longer if Amendment 253 fixed-base applies)
3. Check for BL arrears that may be offsetting the payout; resolve by paying or arranging a payment plan
4. If deadline passed, file an appeal (erur, ערעור) with Bituach Leumi within 6 months
5. Contact Bituach Leumi service center at *6050 for the specific rejection reason

### Error: "Tax Authority rejected Amendment 283 combat credit"
Cause: Submitted ishur sherut miluim (service confirmation) instead of ishur lochem (combat confirmation), or unit commander has not classified the days as combat.
Solution:
1. Download ishur lochem from miluim.idf.il (different document from ishur sherut)
2. If unit has not classified the days as combat, contact unit commander or Reserve Branch to challenge
3. Resubmit with both documents attached to Form 101 or annual filing

### Error: "Employer terminated reservist within protection period"
Cause: Employer violated post-service dismissal protection (either unaware or deliberate).
Solution:
1. Document termination date and service return date
2. Determine applicable protection period: 30 days (under 60 days served) or 60 days (60+ days served)
3. Send formal letter citing the applicable post-service protection period
4. File complaint with Labor Court; claim reinstatement and compensation
5. Filing fee is 1% of claim, minimum NIS 168 (many common labor claims are exempt from fees)

### Error: "I served combat miluim but received no Tagmul Nosaf"
Cause: Tagmul Nosaf is paid in May of the year following the qualifying year (10+ days), not at end of service.
Solution:
1. Confirm the qualifying year had 10+ reserve days
2. Wait until May of the following year, then check the BL personal portal
3. If not received by end of May, contact Bituach Leumi at *6050
4. If account/bank details changed, update them via the BL personal portal before May
