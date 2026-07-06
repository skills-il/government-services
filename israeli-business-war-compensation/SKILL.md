---
name: israeli-business-war-compensation
description: "Indirect-damage business compensation calculator and filing guide for Israeli businesses, NPOs (≥25% activity income), and daycare operators hit by war. Covers Shaagat HaAri (March-April 2026) and Iron Swords (Oct 2023+) under the Property Tax & Compensation Fund Law, 1961. Computes turnover-decline eligibility (≥25% over the March-April 2026 period, monthly and bi-monthly alike), wage grant (75% × decline × Form-102 wages × 1.25, cap 13,773 ₪ × 1.25/employee), the small-business continuity table (≤300K), 100% northern tracks (מחזורים, אדום, חקלאות), and a partial pre-claim advance. Surfaces the bifurcated 5/10-day חל\"ת rule and live per-track filing windows (to 17.08.2026). Use when a business owner, NPO admin, or daycare operator asks about נזק עקיף, מענק השתתפות בשכר, חל\"ת, מבצע שאגת הארי, או הגשה לרשות המסים. Do NOT use for direct property damage (israeli-war-damage-claims), employee-side dmei avtala (israeli-unemployment-benefits-navigator), or personal reservist comp (israeli-miluim-manager)."
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
| Business registration date | Registered before 31.12.2024 uses standard same-period prior-year baseline. Newer businesses use an alternate baseline (Jan-Feb 2025 → Mar 2025-Feb 2026; March 2025 onward → first reporting period through Feb 28, 2026) | NOT a hard cliff; baseline formula simply changes |
| Annual turnover band | Between 12,000 NIS and 400,000,000 NIS | INELIGIBLE if outside band |
| Turnover decline (Shaagat HaAri) | ≥ 25% drop over the **March-April 2026** combined period vs the base period (same two months of 2025, or 2023 for evacuated north). This 25% test applies to **both** monthly and bi-monthly VAT filers - a bi-monthly filer compares the full Mar-Apr two-month report, NOT a halved 12.5% threshold. | INELIGIBLE for wage/fixed-cost track |
| Turnover decline (Iron Swords older periods) | Per the operative Iron Swords הוראת שעה for that qualifying period - check the active regulation text for the exact decline % and comparison window (do not assume the Shaagat HaAri 25% carries over). | INELIGIBLE for that period |

**Northern exception:** If the business is in an evacuated yishuv on the northern border (Galilee), compare against 2023 instead of 2025, AND the minimum decline gate is waived for the northern dedicated track.

### Step 3: Pick the highest-yield track (mutually exclusive)

A business can file under only ONE track per damage period. Run all four and recommend the highest.

| Track | Who qualifies | What it pays | Filing form |
|---|---|---|---|
| Red track §35 | Border-area yishuvei sfar (predefined list) | No upper cap on compensation (uncapped, proven loss) | Red-track form on gov.il/he/Departments/DynamicCollectors/compensation-tracks |
| Small business continuity grant (מענק המשכיות עסקית) | Turnover ≤ 300,000 NIS | Fixed-amount table lookup (see Step 4b) | Small-business form (separate flow) |
| Nationwide turnover/wage track | Turnover 300,000 NIS to 400M NIS, declined ≥25% (monthly and bi-monthly alike) | MAX(wage track, fixed-cost track) - see Step 4; a partial advance (paid before the full claim) is available via the nationwide non-border advance portal | תביעת פיצויים נזק עקיף on gov.il/he/service/compensation-indirect-damage |
| Special-area track | Specific yishuvim outside the red list but designated as special | Track-specific formula | Same portal, marked as special area |

### Step 4: Calculate the wage track AND the fixed-cost track, take the higher

For the nationwide track only. Both branches are computed; the system pays the larger.

**Wage participation grant (per evidence.json claim wage-formula-75-percent):**

```
declineRate    = (refTurnover - claimTurnover) / refTurnover        // e.g., 0.40 for 40% drop
rawWageGrant   = 0.75 × declineRate × form102GrossWages × 1.25      // form102GrossWages = gross salaries paid per Form 102; ×1.25 = employer-cost gross-up (מקדם עלות מעביד)
perEmpCap      = 13_773 × 1.25 × numberOfEmployees × declineRate    // 13,773 = avg wage; ×1.25 = same employer-cost gross-up (≈ 17,216/employee)
wageGrant      = min(rawWageGrant, perEmpCap)
```

Input the gross salaries paid per Form 102. The formula multiplies by the 1.25 employer-cost coefficient (מקדם עלות מעביד) on BOTH the raw wage AND the per-employee cap base, so both sides are in employer-cost units. Do NOT pre-gross the input yourself, and do not cap at the bare 13,773 gross figure - either omission understates the grant by ~20%.

For businesses above 300,000 NIS turnover, each track (wage and fixed-cost) is also subject to an aggregate ceiling of 600,000 NIS per damage period.

**Do not double-count חל"ת workers in the wage base.** An employee on unpaid leave (חל"ת) earns no wages in the period and is collecting dmei avtala from Bituach Leumi (Step 5), so their salary is NOT part of `employerWageCost` for those days. Counting a חל"ת worker in both the wage-participation base and the dmei-avtala flow inflates the grant and invites a clawback of the 60% advance.

**Fixed-cost (inputs) track:** tiered multiplier × monthly fixed expenses × number of months in the reporting period.

| Decline tier | Multiplier on monthly fixed expenses |
|---|---|
| 25% – 40% | 7% |
| 40% – 60% | 11% |
| 60% – 80% | 15% |
| 80% – 100% | 22% |

Pay whichever is higher. Most labor-heavy businesses (cafés, salons, agencies) come out ahead on the wage track. Most rent-heavy / inventory-heavy businesses come out ahead on the fixed-cost track.

### Step 4b: Small business continuity grant table (turnover ≤ 300,000 NIS only)

Single monthly payment, no formula. Look up the (annual turnover band, decline tier) cell. **Post-passage authoritative values** per Kol-Zchut (updated after the law passed Knesset 4.5.2026). Pre-passage Mako/CPA-Institute figures (11-12.03.2026) were ~1.7-1.9% lower; do not quote those.

| Annual turnover (₪) | 25-40% decline | 40-60% | 60-80% | 80-100% |
|---|---|---|---|---|
| 12,000 - 50,000 | 1,864 | 1,864 | 1,864 | 1,864 |
| 50,000 - 90,000 | 3,356 | 3,356 | 3,356 | 3,356 |
| 90,000 - 120,000 | 4,475 | 4,475 | 4,475 | 4,475 |
| 120,000 - 150,000 | 2,823 | 4,234.50 | 6,775.20 | 8,469 |
| 150,000 - 200,000 | 3,329 | 4,993.50 | 7,989.60 | 9,987 |
| 200,000 - 250,000 | 4,261 | 6,391.50 | 10,226.40 | 12,783 |
| 250,000 - 300,000 | 4,980 | 7,470 | 11,952 | 14,940 |

Notes:
- All amounts are NIS, single grant for the March-April 2026 damage period.
- The bottom three turnover bands (up to 120K) pay a flat amount regardless of decline tier (post-passage rule); the four bands above 120K scale by decline tier.
- Online filing window for this track: **17.05.2026 - 17.08.2026** per the kolzchut authoritative page; verify the active dates on https://www.gov.il/he/service/claim-compensation-indirect-damage-rions-roar before promising deadlines (windows have been extended multiple times since the law passed).
- The skill's `scripts/calc_grant.py` does NOT compute this table; it covers only the wage / fixed-cost track for businesses above 300K. For small businesses, route to the gov.il portal and reference this table.

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
- Business registration confirmation (תעודת עוסק) showing pre-31.12.2024 registration

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
- **150 days**: full determination of the remaining 40%.
- **8 months**: if no decision is issued, the claim is automatically approved.

### Step 8: Plan for the tax bill on the grant

The grant is `פיצוי פירותי` - revenue-substituting compensation. It is taxable as ordinary business income at the recipient's marginal rate, reported on the annual return for the year of receipt. A business owner who treats it as windfall and doesn't reserve for tax can lose 30–47% of the grant to mas hachnasa surprise.

Surface this proactively. Suggest the owner top up מקדמות (advance tax payments) for the year, or apply for `פריסה` (income spreading) if the grant is large relative to typical annual income.

### Step 9: Appeals if rejected or under-paid

The Property Tax & Compensation Fund Law, 1961 establishes a two-stage appeals path. For INDIRECT damage compensation (the subject of this skill), the appeals committee is established under **§38ל** (Chapter 8B, the indirect-damage compensation chapter), NOT under §29 (which covers general property-tax appeals).

| Stage | Filed with |
|---|---|
| השגה (objection) | The same assessing officer (פקיד שומה) who issued the decision |
| ערר (appeal) | ועדת ערר under §38ל - independent appeals committee dedicated to indirect-damage compensation under the Property Tax Law |

Day-count windows for each stage are defined in the operative hora'at sha'a regulation rather than a fixed code rule, and they're tight (typically 30–60 days). Read the rejection letter carefully for the explicit deadline rather than relying on memory. Miss the השגה window and the ערר window slams shut too. Flag this immediately to any user with a denial or partial approval.

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
| Property Tax & Compensation Fund Law | https://www.nevo.co.il/law_html/law01/273_001.htm | Statutory definitions, §§35–36 indirect damage, §38ל ועדת ערר for indirect damage (§29 is the general property-tax appeals committee, not the indirect-damage one) |
| Bituach Leumi (Shaagat HaAri page) | https://www.btl.gov.il/About/news/Pages/hadasa2026saagathaaryiran.aspx | Bifurcated 5/10-day חל"ת rule, dmei avtala mechanics, employer reservist comp filing |
| Treasury Ministry (אגף דוברות) framework briefs | https://www.gov.il/he/departments/ministry_of_finance | 30.03.2026 "מתווה פיצויים למשק" brief: 10-day חל"ת rule, retroactive employment-service registration to 14.05.2026, NPO/daycare eligibility, northern 100% tracks |
| Kol-Zchut general business compensation | https://www.kolzchut.org.il | Plain-language entitlement entries, document checklists |
| Mako N12 framework summary | https://www.mako.co.il/news-money/2026_q1/Article-79d26c770b1ec91027.htm | Eligibility threshold (25%), turnover band 12,000–400M NIS, wage formula |

## Gotchas

1. **Track exclusivity is per damage period, not per business.** Choose the wrong track and the entire period's claim is forfeit (no reverting). Always run all four track calculations before recommending.
2. **The 25% threshold is a hard cliff, not a sliding scale.** A business at 24.9% decline gets nothing under the wage/fixed-cost track. The fixed-cost tier multipliers (7%/11%/15%/22%) only kick in once the gate is cleared. Note: under Shaagat HaAri the 25% test is the SAME for monthly and bi-monthly filers (the bi-monthly filer compares the full March-April period) - do not apply a halved 12.5% bi-monthly threshold, which was a mistaken carryover from earlier framework drafts.
3. **The wage track cap stacks two limits, not one.** Both `0.75 × declineRate × form102GrossWages × 1.25` AND `13,773 × 1.25 × employees × declineRate` apply; the grant is the LOWER of the two raw amounts (i.e., min of formula vs per-employee cap), not the sum. Computing them as additive overstates the grant by 50–100%. Both sides carry the ×1.25 employer-cost coefficient, so they are in the same units.
4. **Northern evacuated businesses use 2023 baseline AND have the decline floor waived** - but only on the dedicated northern track. If the agent files under the standard nationwide track, the 2023 baseline does NOT apply and the claim under-pays.
5. **The grant is taxable ordinary income.** Owners frequently spend the 60% advance and get hit by a marginal-rate tax bill (up to 47% for high earners) on the annual return. Always surface this in the output.
6. **The 8-month auto-approval rule is a floor, not a service-level commitment.** Real-world processing routinely slips. Encourage the owner to hold receipts and respond to any clarification request within 14 days to keep the timer running.

## Troubleshooting

### Issue: User's turnover decline is 20% - close to the threshold but below

The 25% gate is statutory and applies to monthly and bi-monthly filers alike under Shaagat HaAri (no halved bi-monthly threshold). Below it, the wage/fixed-cost track is unavailable. Two real fallbacks: (1) the small business continuity track (turnover ≤ 300,000 NIS) doesn't impose the decline gate as a formula and may still pay a fixed amount on a ≥25% declaration; (2) cash-basis (בסיס מזומן) filers report their war-period revenue a VAT period later, so their comparison period may differ - confirm the specific baseline for their filing cadence on the gov.il portal, since a business that looks flat in March-April may still show a qualifying decline in the shifted period. If the claim is for an older Iron Swords damage period, check that regulation's own threshold.

### Issue: Employee was on חל"ת for 8 days

The Shaagat HaAri minimum is **bifurcated** (effective 5.5.2026 amendment): **5 consecutive days** if the chal"t started on 28.2.2026 or 1.3.2026 (the first two war days only); **10 consecutive days** for chal"t starting any later date. Once the applicable threshold is crossed, dmei avtala covers ALL days from day one (no waiting period). Eight days fails BOTH gates if the chal"t started after 1.3.2026 (needs 10) and would also fail the 5-day gate if not in the early-onset window. Recommend the employer extend the leave to 10 consecutive days for the general case, or fall back to standard dmei avtala rules (30-day default with five-day waiting period) if eligible. Splitting the leave (e.g., 5 days off, 2 days back, 5 days off) does NOT aggregate; each block is evaluated separately and must independently clear its applicable threshold. The 5-day early-onset cohort's first BL payments only landed June 2026 due to the late amendment, so flag the payment-timing delay to those users.

### Issue: Business registered 15.01.2025 - newer than the standard pre-31.12.2024 cohort

Eligible, but the baseline period changes. For businesses opened January–February 2025, the baseline is March 2025 through February 2026 (averaged) rather than the standard same-period prior year. For businesses opened from March 1, 2025 onward, the baseline is the business's own first reporting period through February 28, 2026. Apply the 25% decline test against the alternate baseline. The business is not auto-rejected as it would be under a hard 31.12.2024 cliff.

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
