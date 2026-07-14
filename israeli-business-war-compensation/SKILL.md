---
name: israeli-business-war-compensation
description: "Indirect-damage business compensation calculator and filing guide for Israeli businesses, NPOs, and daycare operators hit by war. Covers Shaagat HaAri (March-April 2026) and Iron Swords (Oct 2023+). Computes eligibility (turnover decline must EXCEED 25 percent), the eligible-expenses grant per section 38lo (fixed expenses PLUS the wage part, capped, then doubled - the parts are ADDED, not compared), the doubled small-business continuity table (turnover up to 300K), the northern 100 percent tracks, and the advance schedule. Surfaces the 5/10-day chalat rule and live filing windows (to 17.08.2026). Use when a business owner, NPO admin, or daycare operator asks about נזק עקיף, מענק השתתפות בשכר, חל\"ת, מבצע שאגת הארי, or filing with the Tax Authority. Do NOT use for direct property damage (israeli-war-damage-claims), employee-side dmei avtala (israeli-unemployment-benefits-navigator), or personal reservist comp (israeli-miluim-manager)."
license: MIT
---

# Israeli Business War Compensation

## Problem

When war disrupts an Israeli business, the lost revenue, idled employees on חל"ת, and fixed costs that keep ticking can mean thousands of shekels in compensation per month - but the rules are split across two parallel frameworks (Iron Swords 2023 and Shaagat HaAri 2026), four mutually exclusive tracks, and a maze of thresholds that depend on VAT filing cadence, business location, turnover size, and employee headcount. Filing under the wrong track or missing the 25% threshold by a single percentage point forfeits the claim for that period, and the choice is usually irreversible.

## Instructions

### Step 1: Identify the framework

Two parallel frameworks operate today. Both rely on the same Property Tax & Compensation Fund Law, 1961 (חוק מס רכוש וקרן פיצויים, תשכ"א-1961), §§35–36, but each has its own hora'at sha'a (temporary order) regulations.

| Framework | Damage period | Reference baseline |
|---|---|---|
| Iron Swords (תשפ"ד-2023) | From October 7, 2023 onward | Standard same-period prior-year |
| Shaagat HaAri (March-April 2026) | March-April 2026 (תקופת הפגיעה 03-04/26). **Cash-basis filers** (בסיס מזומן, +30 payment terms): their war-period revenue is reported a VAT period later, so their comparison period may shift accordingly - confirm the exact baseline for their filing cadence on the gov.il portal. | Same period 2025 (or 2023 for evacuated north) |

**Filing windows are per-track and OPEN as of mid-2026 - do NOT quote a single "deadline".** Verify the live date on the specific track's gov.il page before promising anything; windows have been extended repeatedly.

| Shaagat HaAri track | Claim filing window |
|---|---|
| Nationwide general / small-business continuity | 17.05.2026 – **17.08.2026** |
| Cash-basis (בסיס מזומן) filers | Later window - verify the live date on the track's gov.il page |
| North red track (מסלול אדום) | to ~31.08.2026 (latest Tax Authority extension; some info pages still show 24.08) |
| North turnover / wage / agriculture tracks | to ~24.09.2026 |

Individual extensions of up to 18 months are available on request. **Do NOT confuse these with the 31.05.2026 (non-online) / 30.06.2026 (online) dates - those are the annual income-tax-report filing extension and the state-guaranteed loan application deadline, NOT the compensation-claim deadline.** A user told "the deadline was 30.06" would wrongly abandon a claim they can still file.

**Statutory anchors.** The Shaagat HaAri framework was passed in second and third readings on **4.5.2026** and published in **ספר החוקים 3525** as two parallel laws: חוק התוכנית לסיוע כלכלי (הוראת שעה) (סיוע לעסקים ולמוסדות ציבור), התשפ"ו-2026 (business-side, governs everything in this skill) and חוק התוכנית לסיוע כלכלי (הוראת שעה) (תעסוקה), התשפ"ו-2026 (employee-side, governs the chal"t dmei avtala flow, that's `israeli-unemployment-benefits-navigator`). Cite the published act, not the March 2026 draft framework, when communicating with the Tax Authority or in appeals.

**Dedicated portal for Shaagat HaAri eligible-expenses claims.** Use https://www.gov.il/he/service/claim-compensation-indirect-damage-rions-roar for the March-April 2026 indirect-damage track ("מסלול הוצאות מזכות"). This is distinct from the general Iron Swords portal (https://www.gov.il/he/service/compensation-indirect-damage) and the special-area portal (https://www.gov.il/he/service/claim-compensation-indirect-damage). Filing under the wrong portal routes to the wrong adjudication track.

Ask the user when their revenue loss occurred and route accordingly. Most live claims in 2026 still fall under Iron Swords for older damage periods.

### Step 2: Check the four-gate eligibility test

Reject early if any gate fails - the system rejects with no recourse.

| Gate | Rule | If user fails |
|---|---|---|
| Business opened by 27.02.2026 (Tax Authority notified by 28.02.2026) | HARD eligibility cliff: a business opened later cannot claim at all | Hard cliff |
| Baseline formula | Opened before 01.01.2025: standard same-period prior-year baseline. Opened after 01.01.2025: total transactions from the opening date or 01.07.2025 (whichever is later) / active months, x2 (and x12 for the base year) | Not a cliff; the formula changes |
| Annual turnover band | Between 12,000 NIS and 400,000,000 NIS | INELIGIBLE if outside band |
| Turnover decline (Shaagat HaAri) | ≥ 25% drop over the **March-April 2026** combined period vs the base period (same two months of 2025, or 2023 for evacuated north). This 25% test applies to **both** monthly and bi-monthly VAT filers - a bi-monthly filer compares the full Mar-Apr two-month report, NOT a halved 12.5% threshold. | INELIGIBLE for wage/fixed-cost track |
| Turnover decline (Iron Swords older periods) | Per the operative Iron Swords הוראת שעה for that qualifying period - check the active regulation text for the exact decline % and comparison window (do not assume the Shaagat HaAri 25% carries over). | INELIGIBLE for that period |

**Northern exception:** If the business is in an evacuated yishuv on the northern border (Galilee), compare against 2023 instead of 2025, AND the minimum decline gate is waived for the northern dedicated track.

### Step 3: Pick the highest-yield track (mutually exclusive)

A business can file under only ONE track per damage period. Run all four, recommend the highest, then apply the §38לז(ג) floor rule (Step 4).

| Track | Who qualifies | What it pays | Filing form |
|---|---|---|---|
| Red track §35 | Border-area yishuvei sfar (predefined list) | No upper cap on compensation (uncapped, proven loss) | Red-track form on gov.il/he/Departments/DynamicCollectors/compensation-tracks |
| Small business continuity grant (מענק המשכיות עסקית) | Turnover ≤ 300,000 NIS | Fixed-amount table lookup (see Step 4b) | Small-business form (separate flow) |
| Nationwide turnover/wage track | Turnover 300,000 NIS to 400M NIS, decline EXCEEDING 25% (monthly and bi-monthly alike) | (fixed expenses + wage part) x 2, capped - see Step 4. NOT "the higher of the two". A partial advance is available via the nationwide non-border advance portal | תביעת פיצויים נזק עקיף on gov.il/he/service/compensation-indirect-damage |
| Special-area track | Specific yishuvim outside the red list but designated as special | Track-specific formula | Same portal, marked as special area |

### Step 4: Compute the eligible expenses (הוצאות מזכות). The wage part and the fixed-cost part are ADDED, not compared

For the nationwide track only. **This is the single most important rule in the skill: the statute defines הוצאות מזכות as the fixed expenses PLUS the eligible wage part, and then doubles the result. It is NOT "run both tracks and take the higher".** Paying the higher of the two understates the grant for every business that has both payroll and fixed costs, which is almost all of them.

Statutory definition (§38לו, חוק התוכנית לסיוע כלכלי (הוראת שעה)(סיוע לעסקים ולמוסדות ציבור), התשפ"ו-2026):

> "הוצאות מזכות" - ההוצאות הקבועות **בתוספת** חלק השכר המזכה, והכול עד לסכום כמפורט להלן, לפי העניין, **כשהוא מוכפל ב־2**

```
declineRate  = (refTurnover - claimTurnover) / refTurnover     // must EXCEED 0.25 to qualify at all
wagePart     = form102GrossWages x declineRate                 // "חלק השכר המזכה"
fixedPart    = priorYearVatInputs / 6 x fixedCostCoefficient   // "הוצאות קבועות", see below
eligible     = min(wagePart + fixedPart, cap) x 2              // the sum AND the cap are both doubled
```

**Aggregate cap, by base-year turnover:**

| Base-year turnover | Cap before x2 | Effective payout cap |
|---|---|---|
| up to 100M NIS | 600,000 NIS | **1,200,000 NIS** |
| 100M to 300M NIS | 600,000 + 0.3% of the excess over 100M | double that |
| 300M to 400M NIS | 1,200,000 NIS | 2,400,000 NIS |

The old "aggregate ceiling of 600,000 NIS" was the PRE-doubling figure quoted as if it were the payout ceiling. For a business under 100M turnover the real ceiling is **1.2M**.

**Fixed expenses (הוצאות קבועות) are NOT the owner's rent + electricity + leasing.** The statute derives them from the VAT return:

```
fixedExpenses = (total current VAT inputs of the PREVIOUS year) / 6 x fixedCostCoefficient
```

Ask for **סך כל התשומות השוטפות בשנה הקודמת** off the VAT reports. A user who hands you monthly rent and utility bills will produce a number unrelated to what the Tax Authority computes.

**Fixed-cost coefficient (מקדם ההוצאות הקבועות)** - the general tiers plus four sector overrides:

| Case | Coefficient |
|---|---|
| Decline over 25% and up to 40% | 7% |
| Decline over 40% and up to 60% | 11% |
| Decline over 60% and up to 80% | 15% |
| Decline over 80% | 22% |
| **Fuel wholesale / retail** | **x0.35** |
| **Business under the VAT section-33 exemption** | **x0.19** |
| **קבלן ביצוע (execution contractor)** | **x0.68** |
| Director's discretionary coefficient | capped at x2 |

The statute's bands read "עולה על 25% ואינו עולה על 40%", i.e. **(low, high]**. Exactly 40% decline falls in the 7% tier, not the 11% tier.

**Per-employee cap on the wage part:**

```
perEmpCap = 13,769 x 1.25 x numberOfEligibleEmployees x declineRate
```

13,769 is the National Insurance average wage as known in March 2026 (the statute's own reference point), not 13,773. x1.25 is the employer-cost coefficient (מקדם עלות מעביד).

**Two statutory deductions from the wage base:** subtract pay for vacation days the employee used (ימי חופשה שניצל העובד), and subtract any sums Bituach Leumi reimbursed the employer for reserve duty (החזר תגמולי מילואים).

**Do not double-count חל"ת workers in the wage base.** An employee on unpaid leave earns no wages in the period and is collecting dmei avtala from Bituach Leumi (Step 5), so their salary is NOT part of the wage base for those days. Counting them in both inflates the grant and invites a clawback of the 60% advance.

**Floor rule (§38לז(ג)):** if a business on the nationwide track would receive LESS than the small-business band (b)(7) would have paid it, it is entitled to the (b)(7) amount instead. Compute both and apply the floor.

### Step 4b: Small business continuity grant table (turnover up to 300,000 NIS only)

**Every amount in the statute is PER MONTH, and the law pays double (פי 2) for the March-April 2026 period.** §38לז(ב): "זכאי לפיצויים בסכום של **פי 2** מהסכום המפורט בפסקאות שלהלן". The table below is ALREADY doubled - these are the amounts actually paid.

| Annual turnover (₪) | Over 25% to 40% | Over 40% to 60% | Over 60% to 80% | Over 80% |
|---|---|---|---|---|
| 12,000 - 50,000 | 3,728 | 3,728 | 3,728 | 3,728 |
| 50,000 - 90,000 | 6,712 | 6,712 | 6,712 | 6,712 |
| 90,000 - 120,000 | 8,950 | 8,950 | 8,950 | 8,950 |
| 120,000 - 150,000 | 5,646 | 8,469 | 13,550.40 | 16,938 |
| 150,000 - 200,000 | 6,658 | 9,987 | 15,979.20 | 19,974 |
| 200,000 - 250,000 | 8,522 | 12,783 | 20,452.80 | 25,566 |
| 250,000 - 300,000 | 9,960 | 14,940 | 23,904 | 29,880 |

The four bands above 120K scale by the statutory **damage coefficient (מקדם הנזק)**: **1** (decline over 25% to 40%), **1.5** (over 40% to 60%), **2.4** (over 60% to 80%), **3** (over 80%). The three bands up to 120K pay a flat doubled amount regardless of decline tier.

**The decline gate DOES apply to this track.** §38לז(ב) pays these amounts "ובלבד שמתקיימים לגביו התנאים הקבועים בפסקאות (2) עד (6) שבסעיף קטן (א)", and (a)(2) requires that "שיעור הירידה במחזור העסקאות שלו עולה על 25%". A business at or below 25% decline gets NOTHING on this track either. Never tell a 20%-decline business that the small-business track "does not impose the decline gate".

Notes:
- Online filing window: **17.05.2026 - 17.08.2026**; verify on https://www.gov.il/he/service/claim-compensation-indirect-damage-rions-roar before promising deadlines.
- `scripts/calc_grant.py` computes this table as well as the nationwide track.

### Step 5: Stack with reservist & employee-side benefits (additive, not exclusive)

Three additional grants stack ON TOP of the indirect-damage track:

1. **Employee חל"ת dmei avtala** (per Treasury press release 30.03.2026, finalized by Knesset 4.5.2026): employees on continuous unpaid leave get unemployment payment for ALL days from day one once they clear the bifurcated minimum, **5 consecutive days ONLY if the chal"t started 28.2.2026 or 1.3.2026**, **10 consecutive days** for any later onset (effective 5.5.2026 amendment per btl.gov.il/StateOfEmergency/ShaagatHari/Pages/halat-shaagatHari1.aspx). The employee files separately at btl.gov.il; the employer doesn't claim this directly but must hand the employee an `הסכם חל"ת` agreement signed by both parties and file Form 100 with the exact halat start and end dates. Registration with שירות התעסוקה is also required (open retroactively until 14 May 2026). First payments for the 5-day early-onset cohort landed June 2026 because the bifurcation amendment was late; for the 10-day cohort, payments began processing through April-May 2026 as employees cleared the threshold. The exact mechanics (waiting-period waiver, vacation-day deduction rules) live on the Bituach Leumi Shaagat HaAri page; direct the employee there and to `israeli-unemployment-benefits-navigator` for the active rules.
2. **Employer reservist compensation** - for each employee called up on צו 8 reserve duty, the employer receives 20% of the employee's average daily wage × reserve duty days served, paid by Bituach Leumi to the employer.
3. **Self-employed reservist grant** (for owner who served themselves, separate from this skill's main scope) - covered in `israeli-miluim-manager`.

### Step 6: Generate the filing checklist

Output a documentation pack the user must assemble before opening the gov.il filing.

**Required documents (all tracks):**
- VAT report 1301 (`דוח עוסק`) for reference period and claim period
- Profit & loss statement for the reference year
- ניהול ספרים (revenue books) for both periods
- Bank statements covering both periods
- Business registration confirmation (תעודת עוסק) showing the business opened by 27.02.2026

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

Set realistic expectations:

- **21 days** after a complete filing: 60% advance payment lands.
- **150 days**: if no decision has been issued, an ADDITIONAL 10% advance is paid (70% advanced in total). This is NOT the final determination of the balance (§38מא(ד)).
- **8 months**: if no decision is issued, the claim is automatically approved.

### Step 8: Plan for the tax bill on the grant

The grant is `פיצוי פירותי` - revenue-substituting compensation. It is taxable as ordinary business income at the recipient's marginal rate, reported on the annual return for the year of receipt. A business owner who treats it as windfall and doesn't reserve for tax can lose 30–47% of the grant to mas hachnasa surprise.

Surface this proactively. Suggest the owner top up מקדמות (advance tax payments) for the year, or apply for `פריסה` (income spreading) if the grant is large relative to typical annual income.

### Step 9: Appeals if rejected or under-paid

The live Shaagat HaAri track has its own two-stage appeals path, set by the 2026 economic-assistance law, NOT by §38ל.

| Stage | Filed with | Deadline |
|---|---|---|
| השגה (objection) | A Tax Authority employee **the Director authorised for the purpose** - NOT the officer who issued the decision (§38מז(א)(1)) | **60 days** from the decision |
| ערר (appeal) | The **ועדת ערר constituted under §21 of the Corona economic-assistance law (2020)**, sitting at the Ministry of Justice (§38מז(ב), §38מח) | **60 days** from the objection decision |

Both windows are fixed at 60 days by statute. Do not tell a claimant the day-counts "live in the operative hora'at sha'a", and do not send the objection back to the officer who issued the decision. Miss the השגה window and the ערר window slams shut too. Flag this immediately to any user with a denial or partial approval.

## Recommended MCP Servers

| MCP | Why it pairs with this skill | Install |
|---|---|---|
| `kolzchut` (All-Rights / כל-זכות) | Authoritative entitlements knowledge base; covers business compensation, reservist owner grant, חל"ת mechanics with regulator citations | `npx skills-il add skills-il/kolzchut --skill kolzchut` |

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Tax Authority press release | https://www.gov.il/he/pages/press_11032026 | Shaagat HaAri framework details, advance mechanism, 20% employer reservist comp, filing extensions |
| Tax Authority filing portal (Iron Swords nationwide) | https://www.gov.il/he/service/compensation-indirect-damage | Filing form name, registration prerequisite, contact channels |
| Tax Authority filing portal (Shaagat HaAri eligible-expenses, March-April 2026) | https://www.gov.il/he/service/claim-compensation-indirect-damage-rions-roar | Dedicated portal for the "מסלול הוצאות מזכות" Shaagat HaAri 2026 track, eligibility band 12,000-400M NIS, ≥25% decline test |
| Tax Authority nationwide advance request (Shaagat HaAri) | https://www.gov.il/he/service/request-for-dvance-dealers-shaagat-haari | Partial pre-claim advance for businesses across the country EXCEPT קו העימות border settlements. Border settlements use a separate frontier advance page (pay-advances-to-business-owners-in-frontier-roaring-lion) |
| Knesset passage announcement (4.5.2026) | https://www.gov.il/he/pages/sa040526-2 | Confirms final approval of both Shaagat HaAri assistance laws (ספר החוקים 3525) |
| Kol-Zchut: Shaagat HaAri business owner Q&A | https://www.kolzchut.org.il/he/שאלות_ותשובות_לעצמאים_ובעלי_עסקים_במהלך_המלחמה_מול_איראן_(מבצע_שאגת_הארי) | Plain-language coverage of eligibility, halat 5/10-day bifurcation, cross-references to specific regulations |
| Tax Authority track index | https://www.gov.il/he/Departments/DynamicCollectors/compensation-tracks | Track exclusivity rules, list of red-track yishuvim |
| Economic Assistance Law (Shaagat HaAri), 2026 - the operative statute | https://fs.knesset.gov.il/25/law/25_lsr_12958311.pdf | §38לו definitions, §38לז small-business table + doubling, §38מא advances, §38מז-מח appeals |
| Property Tax & Compensation Fund Law | https://www.nevo.co.il/law_html/law01/273_001.htm | Statutory definitions, §§35–36 indirect damage, §38ל ועדת ערר for indirect damage (§29 is the general property-tax appeals committee, not the indirect-damage one) |
| Bituach Leumi (Shaagat HaAri page) | https://www.btl.gov.il/About/news/Pages/hadasa2026saagathaaryiran.aspx | Bifurcated 5/10-day חל"ת rule, dmei avtala mechanics, employer reservist comp filing |
| Treasury Ministry (אגף דוברות) framework briefs | https://www.gov.il/he/departments/ministry_of_finance | 30.03.2026 "מתווה פיצויים למשק" brief: 10-day חל"ת rule, retroactive employment-service registration to 14.05.2026, NPO/daycare eligibility, northern 100% tracks |
| Kol-Zchut general business compensation | https://www.kolzchut.org.il | Plain-language entitlement entries, document checklists |
| Mako N12 framework summary | https://www.mako.co.il/news-money/2026_q1/Article-79d26c770b1ec91027.htm | Eligibility threshold (25%), turnover band 12,000–400M NIS, wage formula |

## Gotchas

1. **Track exclusivity is per damage period, not per business.** Choose the wrong track and the entire period's claim is forfeit (no reverting). Always run all four track calculations before recommending.
2. **The 25% threshold is a hard cliff, not a sliding scale.** A business at 24.9% decline gets nothing under the wage/fixed-cost track. The fixed-cost tier multipliers (7%/11%/15%/22%) only kick in once the gate is cleared. Note: under Shaagat HaAri the 25% test is the SAME for monthly and bi-monthly filers (the bi-monthly filer compares the full March-April period) - do not apply a halved 12.5% bi-monthly threshold, which was a mistaken carryover from earlier framework drafts.
3. **The wage part and the fixed-cost part are ADDED, then doubled (§38לו). They are NOT alternatives.** Paying "whichever track is higher" understates the grant for any business with both payroll and fixed costs. Within the wage part, the per-employee cap (13,769 x 1.25 x employees x declineRate) is a CEILING on the wage part, not a second additive component.
4. **Northern evacuated businesses use 2023 baseline AND have the decline floor waived** - but only on the dedicated northern track. If the agent files under the standard nationwide track, the 2023 baseline does NOT apply and the claim under-pays.
5. **The grant is taxable ordinary income.** Owners frequently spend the 60% advance and get hit by a marginal-rate tax bill (up to 47% for high earners) on the annual return. Always surface this in the output.
6. **The 8-month auto-approval rule is a floor, not a service-level commitment.** Real-world processing routinely slips. Encourage the owner to hold receipts and respond to any clarification request within 14 days to keep the timer running.

## Troubleshooting

### Issue: User's turnover decline is 20% - close to the threshold but below

The gate is statutory: the decline must EXCEED 25% (not merely reach it), and it applies to monthly and bi-monthly filers alike. **There is no fallback track for a business under the gate.** The small-business (up to 300K) track does NOT waive it: §38לז(ב) grants those amounts only "ובלבד שמתקיימים... התנאים בפסקאות (2) עד (6) שבסעיף קטן (א)", and (a)(2) is the decline test. Telling a 20%-decline business to file the small-business track sends them into a claim that cannot succeed. The one genuine avenue: cash-basis (בסיס מזומן) filers report their war-period revenue a VAT period later, so their comparison period may differ - confirm the specific baseline for their filing cadence on the gov.il portal, since a business that looks flat in March-April may still show a qualifying decline in the shifted period. If the claim is for an older Iron Swords damage period, check that regulation's own threshold.

### Issue: Employee was on חל"ת for 8 days

The Shaagat HaAri minimum is **bifurcated** (effective 5.5.2026 amendment): **5 consecutive days** if the chal"t started on 28.2.2026 or 1.3.2026 (the first two war days only); **10 consecutive days** for chal"t starting any later date. Once the applicable threshold is crossed, dmei avtala covers ALL days from day one (no waiting period). Eight days fails BOTH gates if the chal"t started after 1.3.2026 (needs 10) and would also fail the 5-day gate if not in the early-onset window. Recommend the employer extend the leave to 10 consecutive days for the general case, or fall back to standard dmei avtala rules (30-day default with five-day waiting period) if eligible. Splitting the leave (e.g., 5 days off, 2 days back, 5 days off) does NOT aggregate; each block is evaluated separately and must independently clear its applicable threshold. The 5-day early-onset cohort's first BL payments only landed June 2026 due to the late amendment, so flag the payment-timing delay to those users.

### Issue: Business opened 15.01.2025 - newer than the standard pre-01.01.2025 cohort

Eligible, but the baseline formula changes. For a business opened after 01.01.2025 the base turnover is: total transactions from the opening date (or 01.07.2025, whichever is LATER), divided by the number of active months, x2 for the two-month eligible period (and x12 for the base year). Apply the decline test against that alternate baseline. The one genuine cliff is different: the business must have OPENED by 27.02.2026 and notified the Tax Authority by 28.02.2026, or it cannot claim at all.

### Issue: User received private business interruption insurance payout

Government compensation is reduced 1:1 by amounts received from private war/BI policies (anti-double-recovery rule, §36 of the Property Tax Law). User must disclose private claims in the gov.il filing. Verify the user's specific policy language with their insurance broker; war-risk coverage varies significantly between Israeli BI products.

### Issue: Caller represents a nonprofit (עמותה / מלכ"ר), not a for-profit business

Per the Treasury brief (30.03.2026), an עמותה qualifies for the same compensation framework if at least 25% of its turnover is "income from activity" (הכנסה מפעילות). Use the standard Step 2 eligibility gates and Step 3 track routing. NPOs that fail the 25%-from-activity threshold but were nonetheless harmed by war restrictions get a separate dedicated grant program coordinated by Treasury and the Ministry of Culture & Sport (tens of millions ₪ allocated, details published separately); refer the caller to the live gov.il announcement rather than the standard indirect-damage flow.

### Issue: Caller operates a daycare (מעון יום / גן ילדים פרטי / משפחתון / מעון סמל)

Treasury (30.03.2026) maps three paths for daycare operators:
1. **Turnover-drop track** - if the daycare refunds parents for the closure period, those refunds count as a turnover decline and feed the standard wage / fixed-cost calculation in Step 4.
2. **Small-operator path** - מנהלי משפחתונים, private מטפלות, and משפחתוני סמל with annual turnover ≤ 300,000 ₪ use the Step 4b table (max ~15,000 ₪ monthly).
3. **חל"ת for staff** - placing the staff on chalat reduces the operator's wage cost AND lets the staff collect dmei avtala (10-day rule from Step 5).

The daycare may combine paths 1 and 3 (refund parents + chalat staff) but the small-operator table is its own exclusive track. Tell operators that the State cannot force them to refund parents (it's a private contract), but that the framework is sized to make the refund affordable.

### Issue: Caller is in an evacuated northern border yishuv (קו העימות צפון)

Three 100% tracks are available, mutually exclusive:
- **מסלול מחזורים (turnover track)** - compensation reflects lost profit from the full turnover decline; covers 100% of the lost profit.
- **מסלול אדום (red track)** - owner must prove specific income that would have been earned absent the war and gets full reimbursement of that proven amount.
- **מסלול חקלאות (agriculture track)** - a dedicated north sub-track for farming operations, paying 13,615 ₪ per worker employed in agricultural land in the special area (capped at 5M ₪ per farmer for the whole eligibility period); route agricultural callers here rather than the general turnover track.

Walk through the applicable tracks with the caller and pick the higher-yielding option. Salaried employees in these yishuvim get 100% of their wage (not 75%). Note: the request-for-dvance-dealers-shaagat-haari advance portal is for nationwide businesses EXCEPT קו העימות settlements, so a border business does NOT use it - border settlements have a separate frontier advance portal (pay-advances-to-business-owners-in-frontier-roaring-lion), on top of their uncapped red/turnover compensation. The north tracks have later filing windows than the nationwide track (red ~31.08.2026; turnover/wage/agriculture ~24.09.2026) - verify the live date on the track's gov.il page.

## Bundled Resources

- `references/domain-checklist.md` - coverage map for fact-check / future updates
- `references/calculator-walkthrough.md` - worked examples across all four tracks
- `references/red-track-yishuvim.md` - list of border-area yishuvim eligible for §35 red track
- `scripts/calc_grant.py` - reference implementation of the wage/fixed-cost track calculation
