---
name: israeli-business-war-compensation
description: "Indirect-damage business compensation calculator and filing guide for Israeli businesses, NPOs (≥25% activity income), and daycare operators hit by war. Covers Shaagat HaAri (March-April 2026) and Iron Swords (Oct 2023+) under the Property Tax & Compensation Fund Law, 1961. Computes turnover-decline eligibility (25% monthly / 12.5% bi-monthly), wage grant (75% × decline × wages, capped at 13,773 ₪ × employees × decline), small-business continuity table for ≤300K NIS turnover (1,833-14,691 ₪ per period), 100% northern-border tracks (מחזורים, אדום), and the 100,000 ₪ red-track advance. Surfaces the 10-day חל\"ת rule (per Treasury 30.03.2026 brief). Use when a business owner, NPO admin, or daycare operator asks about נזק עקיף, מענק השתתפות בשכר, חל\"ת, מבצע שאגת הארי, או הגשה לרשות המסים על אובדן הכנסות מהמלחמה. Do NOT use for direct property damage (use israeli-war-damage-claims), employee-side dmei avtala (israeli-unemployment-benefits-navigator), or personal reservist comp (israeli-miluim-manager)."
license: MIT
---

# Israeli Business War Compensation

## Problem

When war disrupts an Israeli business, the lost revenue, idled employees on חל"ת, and fixed costs that keep ticking can mean thousands of shekels in compensation per month - but the rules are split across two parallel frameworks (Iron Swords 2023 and Shaagat HaAri 2026), four mutually exclusive tracks, and a maze of thresholds that depend on VAT filing cadence, business location, turnover size, and employee headcount. Filing under the wrong track or missing a 25% / 12.5% threshold by a single percentage point forfeits the claim for that period, and the choice is usually irreversible.

## Instructions

### Step 1: Identify the framework

Two parallel frameworks operate today. Both rely on the same Property Tax & Compensation Fund Law, 1961 (חוק מס רכוש וקרן פיצויים, תשכ"א-1961), §§35–36, but each has its own hora'at sha'a (temporary order) regulations.

| Framework | Damage period | Filing deadline | Reference baseline |
|---|---|---|---|
| Iron Swords (תשפ"ד-2023) | From October 7, 2023 onward | Per qualifying period (regulation defines it; check the active regulation text) | Standard same-period prior-year |
| Shaagat HaAri (March 2026) | March-April 2026 (תקופת הפגיעה 03-04/26) | Online: 30.06.2026; non-online: 31.05.2026 | Same period 2025 (or 2023 for evacuated north) |

Ask the user when their revenue loss occurred and route accordingly. Most live claims in 2026 still fall under Iron Swords for older damage periods.

### Step 2: Check the four-gate eligibility test

Reject early if any gate fails - the system rejects with no recourse.

| Gate | Rule | If user fails |
|---|---|---|
| Business registration date | Registered before 31.12.2024 uses standard same-period prior-year baseline. Newer businesses use an alternate baseline (Jan-Feb 2025 → Mar 2025-Feb 2026; March 2025 onward → first reporting period through Feb 28, 2026) | NOT a hard cliff; baseline formula simply changes |
| Annual turnover band | Between 12,000 NIS and 400,000,000 NIS | INELIGIBLE if outside band |
| Turnover decline (monthly VAT filer) | ≥ 25% drop, March 2026 vs March 2025 | INELIGIBLE for wage/fixed-cost track |
| Turnover decline (bi-monthly VAT filer) | ≥ 12.5% drop, Mar–Apr 2026 vs Mar–Apr 2025 | INELIGIBLE for wage/fixed-cost track |

**Northern exception:** If the business is in an evacuated yishuv on the northern border (Galilee), compare against 2023 instead of 2025, AND the minimum decline gate is waived for the northern dedicated track.

### Step 3: Pick the highest-yield track (mutually exclusive)

A business can file under only ONE track per damage period. Run all four and recommend the highest.

| Track | Who qualifies | What it pays | Filing form |
|---|---|---|---|
| Red track §35 | Border-area yishuvei sfar (predefined list) | No upper cap; up to 100,000 NIS advance available | Red-track form on gov.il/he/Departments/DynamicCollectors/compensation-tracks |
| Small business continuity grant (מענק המשכיות עסקית) | Turnover ≤ 300,000 NIS | Fixed-amount table lookup (see Step 4b) | Small-business form (separate flow) |
| Nationwide turnover/wage track | Turnover 300,000 NIS to 400M NIS, declined ≥25% (or 12.5% bi-monthly) | MAX(wage track, fixed-cost track) - see Step 4 | תביעת פיצויים נזק עקיף on gov.il/he/service/compensation-indirect-damage |
| Special-area track | Specific yishuvim outside the red list but designated as special | Track-specific formula | Same portal, marked as special area |

### Step 4: Calculate the wage track AND the fixed-cost track, take the higher

For the nationwide track only. Both branches are computed; the system pays the larger.

**Wage participation grant (per evidence.json claim wage-grant-formula):**

```
declineRate    = (refTurnover - claimTurnover) / refTurnover      // e.g., 0.40 for 40% drop
rawWageGrant   = 0.75 × declineRate × actualWagesInClaimPeriod
perEmpCap      = 13_773 × numberOfEmployees × declineRate          // 13,773 NIS = average wage in economy
wageGrant      = min(rawWageGrant, perEmpCap)
```

**Fixed-cost (inputs) track:** tiered multiplier × monthly fixed expenses × number of months in the reporting period.

| Decline tier | Multiplier on monthly fixed expenses |
|---|---|
| 25% – 40% | 7% |
| 40% – 60% | 11% |
| 60% – 80% | 15% |
| 80% – 100% | 22% |

Pay whichever is higher. Most labor-heavy businesses (cafés, salons, agencies) come out ahead on the wage track. Most rent-heavy / inventory-heavy businesses come out ahead on the fixed-cost track.

### Step 4b: Small business continuity grant table (turnover ≤ 300,000 NIS only)

Single monthly payment, no formula. Look up the (annual turnover band, decline tier) cell. Source: CPA Institute Shaagat HaAri framework brief, 11.03.2026.

| Annual turnover (₪) | 25-40% decline | 40-60% | 60-80% | 80-100% |
|---|---|---|---|---|
| 12,000 - 50,000 | not eligible | 1,833 | 1,833 | 1,833 |
| 50,000 - 90,000 | not eligible | 3,300 | 3,300 | 3,300 |
| 90,000 - 120,000 | not eligible | 4,400 | 4,400 | 4,400 |
| 120,000 - 150,000 | 2,776 | 4,164 | 6,662 | 8,328 |
| 150,000 - 200,000 | 3,273 | 4,910 | 7,855 | 9,819 |
| 200,000 - 250,000 | 4,190 | 6,285 | 10,056 | 12,570 |
| 250,000 - 300,000 | 4,897 | 7,346 | 11,752 | 14,691 |

Notes:
- All amounts are NIS, single grant for the March-April 2026 damage period.
- The 25-40% column is empty for sub-120K turnover bands (no entitlement under that decline tier).
- Early filing window for businesses in the 25-40% decline tier closed 31.03.2026; check whether your client's filing path is still open before promising the lower tier.
- The skill's `scripts/calc_grant.py` does NOT compute this table; it covers only the wage / fixed-cost track for businesses above 300K. For small businesses, route to the gov.il small-business form and reference this table.

### Step 5: Stack with reservist & employee-side benefits (additive, not exclusive)

Three additional grants stack ON TOP of the indirect-damage track:

1. **Employee חל"ת dmei avtala** (per Treasury press release, 30.03.2026): employees on continuous unpaid leave for ≥ 10 days get unemployment payment for ALL days from day one. The employee files separately at btl.gov.il; the employer doesn't claim this directly but must hand the employee an `הסכם חל"ת` agreement signed by both parties. Registration with שירות התעסוקה is also required (open retroactively until 14 May 2026). Bituach Leumi processed first dmei avtala payments in April 2026 once the law passed Knesset. The exact dmei avtala mechanics under the operative hora'at sha'a (waiting-period waiver, vacation-day deduction rules) live on the Bituach Leumi Shaagat HaAri page; direct the employee there for the active rules.
2. **Employer reservist compensation** - for each employee called up on צו 8 reserve duty, the employer receives 20% of the employee's average daily wage × reserve duty days served, paid by Bituach Leumi to the employer.
3. **Self-employed reservist grant** (for owner who served themselves, separate from this skill's main scope) - covered in `israeli-miluim-manager`.

### Step 6: Generate the filing checklist

Output a documentation pack the user must assemble before opening the gov.il filing.

**Required documents (all tracks):**
- VAT report 1301 (`דוח עוסק`) for reference period and claim period
- Profit & loss statement for the reference year
- ניהול ספרים (revenue books) for both periods
- Bank statements covering both periods
- Business registration confirmation (תעודת עוסק) showing pre-31.12.2024 registration

**Wage track only:**
- Form 102 (`טופס 102`) - payroll declaration for claim-period months
- Employee CSV: ID, name, gross monthly wage in claim period
- For each employee placed on חל"ת: signed `הסכם חל"ת` with start/end dates

**Fixed-cost track only:**
- Invoices or contracts for: rent, electricity, leasing, recurring SaaS, communications

**Submission:**
- Tax Authority online portal: gov.il/he/service/compensation-indirect-damage
- Hotline: *4954 (Tax Authority)
- Email: nezekakif@taxes.gov.il

### Step 7: Communicate the cash-flow schedule

Set realistic expectations:

- **21 days** after a complete filing: 60% advance payment lands.
- **150 days**: full determination of the remaining 40%.
- **8 months**: if no decision is issued, the claim is automatically approved.

### Step 8: Plan for the tax bill on the grant

The grant is `פיצוי פירותי` - revenue-substituting compensation. It is taxable as ordinary business income at the recipient's marginal rate, reported on the annual return for the year of receipt. A business owner who treats it as windfall and doesn't reserve for tax can lose 30–47% of the grant to mas hachnasa surprise.

Surface this proactively. Suggest the owner top up מקדמות (advance tax payments) for the year, or apply for `פריסה` (income spreading) if the grant is large relative to typical annual income.

### Step 9: Appeals if rejected or under-paid

The Property Tax & Compensation Fund Law, 1961 establishes a two-stage appeals path:

| Stage | Filed with |
|---|---|
| השגה (objection) | The same assessing officer (פקיד שומה) who issued the decision |
| ערר (appeal) | ועדת ערר - independent appeals committee under the law's appeals chapter |

Day-count windows for each stage are defined in the operative hora'at sha'a regulation rather than a fixed code rule, and they're tight (typically 30–60 days). Read the rejection letter carefully for the explicit deadline rather than relying on memory. Miss the השגה window and the ערר window slams shut too. Flag this immediately to any user with a denial or partial approval.

## Recommended MCP Servers

| MCP | Why it pairs with this skill | Install |
|---|---|---|
| `kolzchut` (All-Rights / כל-זכות) | Authoritative entitlements knowledge base; covers business compensation, reservist owner grant, חל"ת mechanics with regulator citations | `npx skills-il add skills-il/kolzchut --skill kolzchut` |

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Tax Authority press release | https://www.gov.il/he/pages/press_11032026 | Shaagat HaAri framework details, red-track 100,000 NIS advance, 20% employer reservist comp, filing extensions |
| Tax Authority filing portal | https://www.gov.il/he/service/compensation-indirect-damage | Filing form name, registration prerequisite, contact channels |
| Tax Authority track index | https://www.gov.il/he/Departments/DynamicCollectors/compensation-tracks | Track exclusivity rules, list of red-track yishuvim |
| Property Tax & Compensation Fund Law | https://www.nevo.co.il/law_html/law01/273_001.htm | Statutory definitions, §§35–36 indirect damage, §15 ועדת ערר |
| Bituach Leumi (Shaagat HaAri page) | https://www.btl.gov.il/About/news/Pages/hadasa2026saagathaaryiran.aspx | חל"ת 10-day rule (per Treasury 30.03.2026 framework brief), dmei avtala mechanics, employer reservist comp filing |
| Treasury Ministry (אגף דוברות) framework briefs | https://www.gov.il/he/departments/ministry_of_finance | 30.03.2026 "מתווה פיצויים למשק" brief: 10-day חל"ת rule, retroactive employment-service registration to 14.05.2026, NPO/daycare eligibility, northern 100% tracks |
| Kol-Zchut general business compensation | https://www.kolzchut.org.il | Plain-language entitlement entries, document checklists |
| Mako N12 framework summary | https://www.mako.co.il/news-money/2026_q1/Article-79d26c770b1ec91027.htm | Eligibility thresholds (25% / 12.5%), turnover band 12,000–400M NIS, wage formula |

## Gotchas

1. **Track exclusivity is per damage period, not per business.** Choose the wrong track and the entire period's claim is forfeit (no reverting). Always run all four track calculations before recommending.
2. **The 25% / 12.5% threshold is a hard cliff, not a sliding scale.** A business at 24.9% decline gets nothing under the wage/fixed-cost track. The fixed-cost tier multipliers (7%/11%/15%/22%) only kick in once the gate is cleared.
3. **The wage track cap stacks two limits, not one.** Both `0.75 × declineRate × wages` AND `13,773 × employees × declineRate` apply; the grant is the LOWER of the two raw amounts (i.e., min of formula vs per-employee cap), not the sum. Computing them as additive overstates the grant by 50–100%.
4. **Northern evacuated businesses use 2023 baseline AND have the decline floor waived** - but only on the dedicated northern track. If the agent files under the standard nationwide track, the 2023 baseline does NOT apply and the claim under-pays.
5. **The grant is taxable ordinary income.** Owners frequently spend the 60% advance and get hit by a marginal-rate tax bill (up to 47% for high earners) on the annual return. Always surface this in the output.
6. **The 8-month auto-approval rule is a floor, not a service-level commitment.** Real-world processing routinely slips. Encourage the owner to hold receipts and respond to any clarification request within 14 days to keep the timer running.

## Troubleshooting

### Issue: User's turnover decline is 20% - close to the threshold but below

The 25% / 12.5% gate is statutory. Below it, the wage/fixed-cost track is unavailable. The main fallback is to check whether the bi-monthly filing path applies (lower 12.5% threshold) - many businesses are bi-monthly VAT filers without realizing it. If still below threshold, the small business continuity track (turnover ≤ 300,000 NIS) doesn't impose this gate at all and may still pay.

### Issue: Employee was on חל"ת for 8 days

Per the Treasury Ministry brief (30.03.2026), the Shaagat HaAri minimum is **10 consecutive days**, not 14, and once the threshold is crossed dmei avtala covers ALL days from day one (no waiting period). Eight days fails the gate; recommend the employer extend the leave to 10 consecutive days, or fall back to standard dmei avtala rules (30-day default with five-day waiting period) if eligible. Splitting the leave (e.g., 5 days off, 2 days back, 5 days off) does NOT aggregate; each block is evaluated separately and must independently clear 10 consecutive days.

### Issue: Business registered 15.01.2025 - newer than the standard pre-31.12.2024 cohort

Eligible, but the baseline period changes. For businesses opened January–February 2025, the baseline is March 2025 through February 2026 (averaged) rather than the standard same-period prior year. For businesses opened from March 1, 2025 onward, the baseline is the business's own first reporting period through February 28, 2026. Apply the 25% / 12.5% decline test against the alternate baseline. The business is not auto-rejected as it would be under a hard 31.12.2024 cliff.

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

Two 100% tracks are available, mutually exclusive:
- **מסלול מחזורים (turnover track)** - compensation reflects lost profit from the full turnover decline; covers 100% of the lost profit.
- **מסלול אדום (red track)** - owner must prove specific income that would have been earned absent the war and gets full reimbursement of that proven amount.

Walk through both with the caller and pick the higher-yielding option. Salaried employees in these yishuvim get 100% of their wage (not 75%). The red-track 100,000 ₪ advance still applies for cash-flow.

## Bundled Resources

- `references/domain-checklist.md` - coverage map for fact-check / future updates
- `references/calculator-walkthrough.md` - worked examples across all four tracks
- `references/red-track-yishuvim.md` - list of border-area yishuvim eligible for §35 red track
- `scripts/calc_grant.py` - reference implementation of the wage/fixed-cost track calculation
