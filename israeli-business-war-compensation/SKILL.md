---
name: israeli-business-war-compensation
description: "Not tax advice. Filing orientation for Israeli war indirect-damage compensation for businesses, NPOs, and daycare operators, covering Shaagat HaAri (March-April 2026) and Iron Swords (Oct 2023+). Explains the tracks, eligibility gates, the chalat rule, and the document checklist. Does not calculate a grant or confirm a deadline: amounts and dates here may be wrong, so it sends users to the Tax Authority simulator and official claim pages. Use when a business owner, NPO admin, or daycare operator asks about נזק עקיף, מענק השתתפות בשכר, חל\"ת, מבצע שאגת הארי, or filing with the Tax Authority. Do NOT use for direct property damage (israeli-war-damage-claims), employee-side dmei avtala (israeli-unemployment-benefits-navigator), or personal reservist comp (israeli-miluim-manager)."
license: MIT
---

# Israeli Business War Compensation

## Legal notice

This is a free information tool operated by an AI model. It explains the rules, but it does not examine your full circumstances and does not constitute tax advice. All of its outputs are produced automatically, with no involvement, review, or approval by a tax adviser or accountant, and an AI model may err, omit data, or present a wrong conclusion. The binding computation is the Tax Authority's and responsibility for reporting is yours. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and all use of its output is the user's sole responsibility.

**Amounts and dates in this skill may be wrong. Versions 1.4.0 to 1.6.0 usually showed twice the correct amount. Do not rely on them.** Use the Tax Authority simulator and its official claim pages. If you already filed, check with the Tax Authority before changing or cancelling anything.

## Problem

When war disrupts an Israeli business, the rules for compensation for lost revenue, idled employees on חל"ת, and fixed costs are split across two parallel frameworks (Iron Swords 2023 and Shaagat HaAri 2026), four mutually exclusive tracks, and a maze of thresholds that depend on VAT filing cadence, business location, turnover size, and employee headcount. Filing under the wrong track or missing the 25% threshold by a single percentage point forfeits the claim for that period, and the choice is usually irreversible.

## Instructions

Agent instruction: never state a grant amount, or a filing, payment, objection or appeal deadline, from this skill, from memory or from an earlier version. Send the user to the simulator in the Tax Authority's online claim system and to the official page for their track.

### Step 1: Identify the framework

Two parallel frameworks operate today. Both rely on the same Property Tax & Compensation Fund Law, 1961 (חוק מס רכוש וקרן פיצויים, תשכ"א-1961), §§35-36, but each has its own hora'at sha'a (temporary order) regulations.

| Framework | Damage period | Reference baseline |
|---|---|---|
| Iron Swords (תשפ"ד-2023) | From October 7, 2023 onward | Standard same-period prior-year |
| Shaagat HaAri (March-April 2026) | March-April 2026 (תקופת הפגיעה 03-04/26) for an ordinary claimant. **Cash-basis filers (עוסק המדווח על בסיס מזומן) and קבלן ביצוע: the statute FIXES their qualifying period (תקופת הזכאות) at May and June 2026**, it does not merely "shift" it. | Same period 2025 (or 2023 for evacuated north) |

**The qualifying period is statutory, not portal guidance (§38לו, "תקופת הזכאות"), and has exactly two rows:**

| Claimant | תקופת הזכאות |
|---|---|
| Any claimant that is not a cash-basis filer | **March and April 2026** |
| עוסק המדווח על בסיס מזומן, and קבלן ביצוע | **May and June 2026** |

"עוסק המדווח על בסיס מזומן" has three cumulative conditions: VAT liability on receipt of consideration (Chapter F of the VAT Law); the bulk of ongoing receipts arriving in the month FOLLOWING the transaction, or the claimant being a מוסד חינוך; and a turnover decline **below 40%** in the reporting period containing the התקופה הקובעת. Meeting the first two but declining 40% or more leaves the claimant on March-April. The wage qualifying period stays March-April 2026 for everyone, and the התקופה הקובעת is 01.03.2026 to 30.04.2026 throughout.

**Filing windows are per-track. Do not quote a deadline from this skill.** Check the current date on the specific track's official gov.il page.

**Statutory anchors.** The Shaagat HaAri framework was passed in second and third readings on **4.5.2026** and published in **ספר החוקים 3525** as two parallel laws: חוק התוכנית לסיוע כלכלי (הוראת שעה) (סיוע לעסקים ולמוסדות ציבור), התשפ"ו-2026 (business-side, governs everything in this skill) and חוק התוכנית לסיוע כלכלי (הוראת שעה) (תעסוקה), התשפ"ו-2026 (employee-side, governs the chal"t dmei avtala flow, that's `israeli-unemployment-benefits-navigator`). Cite the published act, not the March 2026 draft framework, when communicating with the Tax Authority or in appeals.

**Dedicated portal for Shaagat HaAri eligible-expenses claims.** Use https://www.gov.il/he/service/claim-compensation-indirect-damage-rions-roar for the March-April 2026 indirect-damage track. It is distinct from the general Iron Swords portal and the special-area portal (both in Step 6); filing under the wrong portal routes to the wrong adjudication track.

Ask the user when their revenue loss occurred and route accordingly. Most live claims in 2026 still fall under Iron Swords for older damage periods.

### Step 2: Check the four-gate eligibility test

Reject early if any gate fails - the system rejects with no recourse.

| Gate | Rule | If user fails |
|---|---|---|
| Business opened BEFORE 01.03.2026, and the Tax Authority notified of the opening by 28.02.2026 (§38לז(א)(4)) | HARD eligibility cliff. A business opened ON 28.02.2026 is INSIDE the cliff, not outside it: the statute's line is "לפני יום 1 במרץ 2026". Separately, a claimant is excluded if its business was not active before 01.03.2026 (presumed inactive if it failed to file two of its last three VAT returns, rebuttable), if it reported closing before that date, or if it reported zero turnover for the four preceding months. | Hard cliff |
| Baseline formula | Opened before 01.01.2025: standard same-period prior-year baseline. Opened after 01.01.2025: total transactions from the opening date or 01.07.2025 (whichever is later) / active months, x2 (and x12 for the base year) | Not a cliff; the formula changes |
| Annual turnover band | Between 12,000 NIS and 400,000,000 NIS | INELIGIBLE if outside band |
| Turnover decline (Shaagat HaAri) | ≥ 25% drop over the **March-April 2026** combined period vs the base period (same two months of 2025, or 2023 for evacuated north). This 25% test applies to **both** monthly and bi-monthly VAT filers - a bi-monthly filer compares the full Mar-Apr two-month report, NOT a halved 12.5% threshold. | INELIGIBLE for wage/fixed-cost track |
| Turnover decline (Iron Swords older periods) | Per the operative Iron Swords הוראת שעה for that qualifying period - check the active regulation text for the exact decline % and comparison window (do not assume the Shaagat HaAri 25% carries over). | INELIGIBLE for that period |

**Excluded claimant classes (definition of "ניזוק", 12 limbs).** Screen BEFORE running any track: a business in one of these gets nothing even with a qualifying decline. The State; budgeted bodies and health corporations (s.21 Budget Foundations Law); kupot cholim; public institutions that are not a מוסד ציבורי זכאי; statutory corporations; financial institutions (banks and auxiliaries, insurers, exchange members, managing companies, fund managers); dealers in real-estate rights held as trading stock; businesses with over 50% of 2024 or 2025 work on projects running over a year (except a קבלן ביצוע); businesses that reported closure, zero turnover for the preceding four months, or inactivity before 01.03.2026; and **anyone whose occupation is agriculture** (farmers route to the dedicated agriculture track, not Step 4). Full list in `references/domain-checklist.md`.

**Northern exception:** If the business is in an evacuated yishuv on the northern border (Galilee), compare against 2023 instead of 2025, AND the minimum decline gate is waived for the northern dedicated track.

### Step 3: Pick the track (mutually exclusive)

A business can file under only ONE track per damage period. Compare the tracks in the Tax Authority simulator.

| Track | Who qualifies | What it pays | Filing form |
|---|---|---|---|
| Red track §35 | Border-area yishuvei sfar (predefined list) | Use the Tax Authority simulator | Red-track form on gov.il/he/Departments/DynamicCollectors/compensation-tracks |
| Small business continuity grant (מענק המשכיות עסקית) | Turnover ≤ 300,000 NIS | Use the Tax Authority simulator | Small-business form (separate flow) |
| Nationwide turnover/wage track | Turnover 300,000 NIS to 400M NIS, decline EXCEEDING 25% (monthly and bi-monthly alike) | Use the Tax Authority simulator. A partial advance is available via the nationwide non-border advance portal | תביעת פיצויים נזק עקיף on gov.il/he/service/compensation-indirect-damage |
| Special-area track | Specific yishuvim outside the red list but designated as special | Use the Tax Authority simulator | Same portal, marked as special area |

### Step 4: Get the amount from the Tax Authority simulator

This skill does not calculate a grant amount. Send the user to the simulator in the Tax Authority's online claim system. `scripts/calc_grant.py` prints no amount and points to the simulator.

### Step 5: Stack with reservist & employee-side benefits (additive, not exclusive)

Three additional grants stack ON TOP of the indirect-damage track:

1. **Employee חל"ת dmei avtala** (Treasury 30.03.2026, finalized by Knesset 4.5.2026): employees on continuous unpaid leave are paid for ALL days from day one once they clear a bifurcated minimum, **5 consecutive days only if the חל"ת started 28.2.2026 or 1.3.2026**, **10 consecutive days** for any later onset (5.5.2026 amendment). The employee files at btl.gov.il; the employer hands over a signed `הסכם חל"ת` and files Form 100 with exact start and end dates, and שירות התעסוקה registration is required. For payment timing, waiting-period and vacation-day mechanics, check the Bituach Leumi Shaagat HaAri page and `israeli-unemployment-benefits-navigator`.
2. **Employer reservist compensation** - check the amount and conditions with Bituach Leumi.
3. **Self-employed reservist grant** (for owner who served themselves, separate from this skill's main scope) - covered in `israeli-miluim-manager`.

### Step 6: Generate the filing checklist

Output a documentation pack the user must assemble before opening the gov.il filing.

**Required documents (all tracks):**
- VAT report 1301 (`דוח עוסק`) for reference period and claim period
- Profit & loss statement for the reference year
- ניהול ספרים (revenue books) for both periods
- Bank statements covering both periods
- Business registration confirmation (תעודת עוסק) showing the business opened before 01.03.2026 and was notified to the Tax Authority by 28.02.2026

**Wage track only:**
- Form 102 (`טופס 102`) - payroll declaration for claim-period months
- Employee CSV: ID, name, gross monthly wage in claim period
- For each employee placed on חל"ת: signed `הסכם חל"ת` with start/end dates

**Fixed-cost track only:**
- Invoices or contracts for: rent, electricity, leasing, recurring SaaS, communications

**Submission:**
- Tax Authority online portal for Shaagat HaAri eligible-expenses track (March-April 2026): gov.il/he/service/claim-compensation-indirect-damage-rions-roar
- Tax Authority online portal for Iron Swords general nationwide track: gov.il/he/service/compensation-indirect-damage
- Tax Authority special-area portal (north / specific yishuvim): gov.il/he/service/claim-compensation-indirect-damage
- Advance request, nationwide (businesses across the country EXCEPT קו העימות border settlements): gov.il/he/service/request-for-dvance-dealers-shaagat-haari
- Advance request, border settlements (יישובי ספר / קו העימות): gov.il/he/service/pay-advances-to-business-owners-in-frontier-roaring-lion
- Hotline: *4954 (Tax Authority)
- Email: nezekakif@taxes.gov.il

### Step 7: Communicate the cash-flow schedule

Do not promise a payment date, an advance percentage, or approval if no decision is issued. Check the official claim page and follow up with the Tax Authority in writing.

### Step 8: Plan for the tax bill on the grant

The grant is `פיצוי פירותי` - revenue-substituting compensation. It is taxable as ordinary business income at the recipient's marginal rate, reported on the annual return for the year of receipt. A business owner who treats it as windfall and doesn't reserve for tax can lose 30-47% of the grant to mas hachnasa surprise.

Surface this proactively. Suggest the owner top up מקדמות (advance tax payments) for the year, or apply for `פריסה` (income spreading) if the grant is large relative to typical annual income.

### Step 9: Appeals if rejected or under-paid

Do not state an objection or appeal deadline, or an appeal route, from this skill. Read the decision letter and the official page for the track immediately, and check with the Tax Authority. Flag this immediately to any user with a denial or partial approval.

## Recommended MCP Servers

| MCP | Why it pairs with this skill | Install |
|---|---|---|
| `kolzchut` (All-Rights / כל-זכות) | Authoritative entitlements knowledge base; covers business compensation, reservist owner grant, חל"ת mechanics with regulator citations | `npx skills-il add skills-il/kolzchut --skill kolzchut` |

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Tax Authority filing portal (Iron Swords nationwide) | https://www.gov.il/he/service/compensation-indirect-damage | Filing form name, registration prerequisite, contact channels |
| Tax Authority filing portal (Shaagat HaAri eligible-expenses, March-April 2026) | https://www.gov.il/he/service/claim-compensation-indirect-damage-rions-roar | Dedicated portal for the "מסלול הוצאות מזכות" Shaagat HaAri 2026 track, eligibility band 12,000-400M NIS, ≥25% decline test |
| Tax Authority nationwide advance request (Shaagat HaAri) | https://www.gov.il/he/service/request-for-dvance-dealers-shaagat-haari | Partial pre-claim advance for businesses across the country EXCEPT קו העימות border settlements. Border settlements use a separate frontier advance page (pay-advances-to-business-owners-in-frontier-roaring-lion) |
| Knesset passage announcement (4.5.2026) | https://www.gov.il/he/pages/sa040526-2 | Confirms final approval of both Shaagat HaAri assistance laws (ספר החוקים 3525) |
| Kol-Zchut: Shaagat HaAri business owner Q&A | https://www.kolzchut.org.il/he/שאלות_ותשובות_לעצמאים_ובעלי_עסקים_במהלך_המלחמה_מול_איראן_(מבצע_שאגת_הארי) | Plain-language coverage of eligibility, halat 5/10-day bifurcation, cross-references to specific regulations |
| Tax Authority track index | https://www.gov.il/he/Departments/DynamicCollectors/compensation-tracks | Track exclusivity rules |
| Economic Assistance Law (Shaagat HaAri), 2026 - the operative statute | https://fs.knesset.gov.il/25/law/25_lsr_12958311.pdf | §38לו definitions, §38לז small business, §38מא advances, §38מז-מח appeals |
| Property Tax & Compensation Fund Law | https://www.nevo.co.il/law_html/law01/273_001.htm | Statutory definitions, §§35-36 indirect damage, §38ל ועדת ערר for indirect damage (§29 is the general property-tax appeals committee, not the indirect-damage one) |
| Bituach Leumi (Shaagat HaAri page) | https://www.btl.gov.il/About/news/Pages/hadasa2026saagathaaryiran.aspx | Bifurcated 5/10-day חל"ת rule, dmei avtala mechanics, employer reservist comp filing |
| Treasury Ministry (אגף דוברות) framework briefs | https://www.gov.il/he/departments/ministry_of_finance | 30.03.2026 "מתווה פיצויים למשק" brief |

## Gotchas

1. **Track exclusivity is per damage period, not per business.** Choose the wrong track and the entire period's claim is forfeit (no reverting). Compare the tracks in the Tax Authority simulator.
2. **The 25% threshold is a hard cliff, not a sliding scale.** A business at 24.9% decline gets nothing under the wage/fixed-cost track. Note: under Shaagat HaAri the 25% test is the SAME for monthly and bi-monthly filers (the bi-monthly filer compares the full March-April period) - do not apply a halved 12.5% bi-monthly threshold, which was a mistaken carryover from earlier framework drafts.
3. **Northern evacuated businesses use 2023 baseline AND have the decline floor waived** - but only on the dedicated northern track. If the agent files under the standard nationwide track, the 2023 baseline does NOT apply and the claim under-pays.
4. **The grant is taxable ordinary income.** Owners frequently spend an advance and get hit by a marginal-rate tax bill (up to 47% for high earners) on the annual return. Always surface this in the output.

## Troubleshooting

### Issue: User's turnover decline is 20% - close to the threshold but below

The gate is statutory: the decline must EXCEED 25% (not merely reach it), and it applies to monthly and bi-monthly filers alike. **There is no fallback track for a business under the gate.** The small-business (up to 300K) track does NOT waive it: §38לז(ב) grants those amounts only "ובלבד שמתקיימים... התנאים בפסקאות (2) עד (6) שבסעיף קטן (א)", and (a)(2) is the decline test. Telling a 20%-decline business to file the small-business track sends them into a claim that cannot succeed. The one genuine avenue: if the claimant is a cash-basis filer (עוסק המדווח על בסיס מזומן) or a קבלן ביצוע, its statutory qualifying period is **May and June 2026**, not March-April, so a business that looks flat in March-April may still show a qualifying decline over May-June. Check the three cumulative conditions of the cash-basis definition first, in particular that the decline in the reporting period containing March-April was below 40%. If the claim is for an older Iron Swords damage period, check that regulation's own threshold.

### Issue: Employee was on חל"ת for 8 days

The Shaagat HaAri minimum is **bifurcated** (effective 5.5.2026 amendment): **5 consecutive days** if the chal"t started on 28.2.2026 or 1.3.2026 (the first two war days only); **10 consecutive days** for chal"t starting any later date. Once the applicable threshold is crossed, dmei avtala covers ALL days from day one (no waiting period). Eight days fails BOTH gates if the chal"t started after 1.3.2026 (needs 10) and would also fail the 5-day gate if not in the early-onset window. Recommend the employer extend the leave to 10 consecutive days for the general case, or fall back to standard dmei avtala rules (30-day default with five-day waiting period) if eligible. Splitting the leave (e.g., 5 days off, 2 days back, 5 days off) does NOT aggregate; each block is evaluated separately and must independently clear its applicable threshold.

### Issue: Business opened 15.01.2025 - newer than the standard pre-01.01.2025 cohort

Eligible, but the baseline formula changes. For a business opened after 01.01.2025 the base turnover is: total transactions from the opening date (or 01.07.2025, whichever is LATER), divided by the number of active months, x2 for the two-month eligible period (and x12 for the base year). Apply the decline test against that alternate baseline. The one genuine cliff is different: the business must have OPENED before 01.03.2026 and notified the Tax Authority of the opening by 28.02.2026, or it cannot claim at all. A business opened on 28.02.2026 still clears that cliff.

### Issue: User received private business interruption insurance payout

User must disclose private claims in the gov.il filing. Verify the user's specific policy language with their insurance broker; war-risk coverage varies significantly between Israeli BI products.

### Issue: Caller represents a nonprofit (עמותה / מלכ"ר), not a for-profit business

Per the Treasury brief (30.03.2026), an עמותה qualifies for the same compensation framework if at least 25% of its turnover is "income from activity" (הכנסה מפעילות). Use the standard Step 2 eligibility gates and Step 3 track routing. NPOs that fail the 25%-from-activity threshold but were nonetheless harmed by war restrictions get a separate dedicated grant program coordinated by Treasury and the Ministry of Culture & Sport; refer the caller to the live gov.il announcement rather than the standard indirect-damage flow.

### Issue: Caller operates a daycare (מעון יום / גן ילדים פרטי / משפחתון / מעון סמל)

Three paths exist: the turnover-drop track (parent refunds count as a turnover decline), the small-operator path (turnover up to 300,000 NIS), and חל"ת for staff. Paths 1 and 3 combine; the small-operator path is exclusive. Full detail, including what the State can and cannot require of the operator, is in `references/claimant-paths.md`.

### Issue: Caller is in an evacuated northern border yishuv (קו העימות צפון)

Three mutually exclusive tracks: מסלול מחזורים, מסלול אדום, and מסלול חקלאות. Compare the applicable ones in the Tax Authority simulator. A border business does NOT use the nationwide advance portal; it has its own frontier portal.

## Bundled Resources

- `references/domain-checklist.md` - pointer to the earlier coverage map
- `references/red-track-yishuvim.md` - list of border-area yishuvim eligible for §35 red track
- `scripts/calc_grant.py` - prints no amount and points to the Tax Authority simulator
