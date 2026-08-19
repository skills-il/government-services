# Domain Coverage Checklist - israeli-business-war-compensation

Generated: 2026-04-27, refreshed 2026-04-28 against Treasury Ministry brief (30.03.2026) and CPA Institute Shaagat HaAri brief (11.03.2026). Refreshed 2026-07-06 (v3): corrected the bi-monthly decline gate to 25% (removed the erroneous 12.5%), added the cash-basis (בסיס מזומן) May-June period and the north agriculture track, replaced the single "deadline" with per-track filing windows, and synced the חל"ת rule to the bifurcated 5/10-day form. Sources: mas.gov.il, gov.il, kolzchut.org.il, btl.gov.il, knesset.gov.il, nevo.co.il

## Must cover (core)

- [x] Statutory basis (Property Tax & Compensation Fund Law, תשכ"א-1961, §§35-36) - anchor every grant calculation to a section of the underlying law. §35 defines indirect damage in border-area settlements (red track, no cap); §36 enables government regulations for nationwide indirect damage. - source: https://www.nevo.co.il/law_html/law01/273_001.htm - why core: Without this anchor, calculations are folkloric.
- [x] Iron Swords indirect-damage regulations (תקנות מס רכוש וקרן פיצויים (תשלום פיצויים) (נזק מלחמה ונזק עקיף) (חרבות ברזל) (הוראת שעה), תשפ"ד-2023) - operative regulation for damage from October 7, 2023 onward. Defines turnover-decline thresholds, wage track, fixed-cost track, 12,000-400M NIS turnover band. Filing deadlines defined per qualifying period in the regulation. - why core: nearly all live business claims in 2026 still cite it.
- [x] Shaagat HaAri (March 2026) framework - distinct hora'at sha'a, parallel to Iron Swords (different reference period, identical mechanic). - source: https://www.gov.il/he/pages/press_11032026 - why core: confusing the two frameworks causes filing under wrong regulation and rejection.
- [x] Eligibility thresholds - ≥25% decline over the March-April 2026 combined period vs the base period (same two months 2025, or 2023 for evacuated north), applied to BOTH monthly and bi-monthly filers (a bi-monthly filer compares the full two-month report; there is no halved 12.5% bi-monthly gate under Shaagat HaAri). - why core: gating eligibility check.
- [x] Cash-basis (בסיס מזומן / +30 payment-terms) filers and קבלן ביצוע - the statute FIXES their תקופת הזכאות at **May and June 2026** (§38לו); only the filing window still needs checking on the gov.il portal. The cash-basis definition is cumulative: VAT liability on receipt, bulk of receipts in the month following the transaction (or a מוסד חינוך), and a decline below 40% in the reporting period containing the התקופה הקובעת. - source: CPA briefs (poenta/amir-cpa); exact window not published on the main gov.il service page as of 2026-07-06 - why core: a whole filer class (contractors, +30-terms businesses) whose damage does not show in the March-April reports.
- [x] Eligibility - turnover band 12,000 NIS ≤ annual turnover ≤ 400M NIS, and the business must have OPENED BEFORE 01.03.2026 with the Tax Authority notified of the opening by 28.02.2026 (§38לז(א)(4)). The 31.12.2024 / 01.01.2025 date is NOT an eligibility cliff, it only selects which baseline formula applies. - why core: floor and ceiling are hard exclusions, and an off-by-one on the opening date turns away eligible claimants.
- [x] Eligible-expenses grant (§38לו) - (fixed expenses + eligible wage part), capped, THEN x2. The parts are ADDED, not compared. Wage part = wage expenses x decline rate, where wage expenses are the LOWER OF (a) 0.75 x eligible-employee wages x 1.25 and (b) 13,769 x 1.25 x eligible employees. The 0.75 is mandatory; feeding raw Form-102 gross into limb (a) overstates the wage part by 6.67%. Three claimant classes: general (1.25), מוסד ציבורי זכאי (1.325 x non-donation income ratio in both limbs), קיבוץ (1.25 over a restricted employee set). Fixed part = prior-year VAT inputs / 6 x coefficient. Effective cap 1.2M (turnover <= 100M). - why core: central deliverable.
- [x] Fixed-cost (inputs) track - tiered coefficient applied to the statutory fixed-expenses base: over 25% to 40% decline → 7%; over 40% to 60% → 11%; over 60% to 80% → 15%; over 80% → 22%. The fixed-cost part is **ADDED to** the wage part (§38לו), never compared with it. The system does NOT pay "whichever track is higher". Sector factors (fuel x0.35, VAT-s.33-exempt x0.19, קבלן ביצוע x0.68) MULTIPLY the tier rate. - why core: ignoring the fixed-cost track leaves money on the table, and treating the two parts as alternatives understates every mixed-cost claimant.
- [x] Small business fast track (turnover ≤ 300,000 NIS) - fixed-amount table lookup ("מענק המשכיות עסקית"), no formula, different filing form, exclusive of wage/fixed-cost track. Table reproduced inline in SKILL.md Step 4b (post-passage kolzchut/legislated values, ranging from 1,864 for the 12-50K band up to 14,940 for the 250-300K / 80-100%-decline cell; pre-passage press summaries quoted a lower ~1,833-14,691 range, do not use those). - source: CPA Institute Shaagat HaAri framework brief 11.03.2026, cross-referenced against Treasury Ministry brief 30.03.2026 - why core: 300k NIS is the bright-line routing threshold and the table values gate cash-flow expectations.
- [x] NPO (amuta / mlcr) eligibility - entities with ≥25% income from "activity income" (הכנסה מפעילות) qualify under the same framework as businesses. Sub-25% NPOs that were nonetheless harmed get a separate dedicated grant program coordinated by Treasury + Ministry of Culture & Sport (tens of millions ₪). - source: Treasury brief 30.03.2026 - why core: nonprofits routinely call the same hotline; routing them away to "businesses only" would forfeit eligible claims.
- [x] Daycare operators (maon yom / gan ילדים פרטי / mishpachton / maon semel) - three eligibility paths: (a) turnover-drop track if refunding parents, (b) small-operator path with ≤300K turnover via Step 4b table, (c) chalat for staff. Operators may combine paths (a) and (c). - source: Treasury brief 30.03.2026 - why core: daycare is a high-volume use case during war closures and the framework explicitly addresses it.
- [x] Northern border zone (קו עימות צפון) 100% tracks - מסלול מחזורים (100% of lost profit from full turnover decline), מסלול אדום (100% reimbursement of specifically proven lost income), and מסלול חקלאות (dedicated agriculture sub-track: 13,615 NIS per worker in agricultural land in the special area, capped 5M NIS/farmer). Mutually exclusive; pick the higher-yielding option per period. Salaried employees in evacuated yishuvim get 100% of wage. North filing windows run later than nationwide (red ~31.08.2026 per latest extension; turnover/wage/agriculture ~24.09.2026). - source: Treasury brief 30.03.2026 + gov.il track pages - why core: nationwide track at 75% under-pays northern callers by 25% if mis-routed.
- [x] חל"ת dmei avtala - **bifurcated minimum** under Shaagat HaAri (5.5.2026 amendment): **5 consecutive days** if the חל"ת began 28.2.2026 or 1.3.2026 (first two war days only), otherwise **10 consecutive days**. Once the applicable gate is crossed, dmei avtala is paid for ALL days from day one (no waiting period; aksharah reduced to 6-of-18 months). Registration with שירות התעסוקה required (retroactive to 14.05.2026). Employer must give the employee a signed הסכם חל"ת. Employee files at btl.gov.il. - why core: gating rule for the employee branch; frequently confused with the 30-day default and with the earlier flat 10-day / 14-day drafts.
- [x] Filing process - Tax Authority online portal, "תביעת פיצויים נזק עקיף" form. 60% advance after 21 days, final determination within 150 days, automatic approval after 8 months. - source: https://www.gov.il/he/service/compensation-indirect-damage - why core: business owner needs cash-flow schedule.
- [x] Northern businesses special baseline - evacuated/border northern settlements compare against 2023 (not 2025). No minimum decline % required for the dedicated northern track; covers profit losses too. - why core: skill must detect "is the business in evacuated yishuv?" and switch baseline.
- [x] Track exclusivity - eligible business may file under only ONE of: (a) red track §35, (b) special-area track, (c) nationwide turnover/wage/fixed-cost, (d) small-business continuity grant. - why core: choosing wrong track is irreversible per damage period.
- [x] Documentation requirements - VAT reports (1301/דוחות עוסק) for reference + claim periods, P&L for reference year, ניהול ספרים, bank statements, payroll records (טופס 102) for wage track, fixed-cost invoices, employee CSV with ID + הסכם חל"ת dates. - why core: this IS the filing checklist.
- [x] Tax treatment - wage/fixed-cost/turnover grant is "פיצוי פירותי" (revenue substitute), taxable as ordinary business income at marginal rate, reported on annual return. פריסה (income spreading) available in some cases. - why core: business owners frequently fail to provision for tax on the grant.
- [x] Reservist business-owner grant - separate from indirect damage; for עצמאים / בעלי שליטה called up under צו 8 reserve duty. Multiple sub-tracks exist with their own day-count thresholds and per-day multipliers; rules change with each hora'at sha'a. Refer the user to the live Kol-Zchut entry and to israeli-miluim-manager for the active calculation. - source: https://www.kolzchut.org.il/he/פיצוי_לבעלי_עסקים_ששירתו_במילואים_במלחמת_חרבות_ברזל_או_במלחמה_מול_איראן - why core: stacks WITH (not instead of) indirect-damage grant.

## Should cover (advanced / edge cases)

- [x] Self-employed (osek murshe / osek patur) - both eligible; osek patur typically funnels into small-business continuity track. - why advanced: edge case for solo practitioners.
- [x] Appeal process - two-tier: השגה to assessing officer first, then ערר to ועדת ערר. Day-count windows defined in the operative hora'at sha'a regulation rather than fixed code. - why advanced: short deadlines, easily missed; user must read the rejection letter for explicit day-counts.
- [x] Time limits - defined in the operative hora'at sha'a regulation rather than fixed code. Read the rejection letter or framework press release for specific deadlines per qualifying period. - why advanced: deadlines often missed.
- [x] Interaction with private business interruption insurance - government compensation reduced by amounts received from private war/BI policies (anti-double-recovery rule). Specific policy language varies between Israeli BI products; verify with the user's broker. - why advanced: where policy paid, government grant is offset 1:1.
- [x] Eligible business types - self-employed, exempt dealers, salaried-controlling-shareholders, corporations, nonprofits, kibbutzim. **Excluded (all 12 limbs of the "ניזוק" definition):** the State; budgeted bodies and health corporations (s.21 Budget Foundations Law); kupot cholim; public institutions that are not a מוסד ציבורי זכאי; statutory corporations; financial institutions (banks and auxiliaries, insurers, exchange members, managing companies, fund managers); dealers in real-estate rights held as trading stock; businesses with over 50% of 2024/2025 work on projects longer than a year (except קבלן ביצוע); businesses that reported closure, zero turnover for the preceding four months, or inactivity before 01.03.2026; and anyone whose occupation is agriculture. Newer businesses (registered after 31.12.2024) are eligible under alternate baseline formulas. - why advanced: rare exclusion cases need explicit handling.
- [x] Reference-period substitution - businesses with no comparable prior-year period use the alternate baseline rules defined in the framework press release (different rules for Jan-Feb 2025 vs. March 2025+ openings). - why advanced: edge case for new/seasonal businesses.
- [x] Partial pre-claim advance, two portals - the nationwide advance portal (request-for-dvance-dealers-shaagat-haari) is scoped to businesses across the country EXCEPT קו העימות settlements; border settlements use a SEPARATE frontier advance portal (pay-advances-to-business-owners-in-frontier-roaring-lion). Do not conflate the two or quote a single hard shekel cap (the amount is a percentage of assessed compensation and varies by segment). - source: gov.il service pages (both portal titles confirmed 2026-07-06) - why advanced: mislabeling the advance's population routes a border business to the wrong portal.
- [x] Employer reservist compensation - 20% of employee's average daily wage × reserve duty days, in addition to indirect-damage grants. - source: https://www.gov.il/he/pages/press_11032026 - why advanced: stacks with main grants.
- [x] Tax filing extensions (distinct from the compensation-claim window) - the annual income-tax-report deadline was extended (non-online: 31.05.2026; online: 30.06.2026) and the state-guaranteed loan application deadline is 30.06.2026. These are NOT the compensation-claim deadline (nationwide claim window runs to 17.08.2026; north to 24.09.2026). - source: https://www.gov.il/he/pages/press_11032026 - why advanced: users frequently mistake the 30.06 report/loan date for the comp deadline and abandon a still-open claim.

## Out of scope (explicit, with rationale)

- **Iron Swords (חרבות ברזל) per-period decline percentages, coefficients and filing windows
  (decided 2026-08-19: OUT OF SCOPE, deliberately).** This skill encodes the Shaagat HaAri
  figures because they sit in one published primary statute (ספר החוקים 3525) that can be read
  end to end. The Iron Swords figures do not: they live across a chain of amending
  הוראת שעה regulations, one per qualifying period from October 2023 onward, each with its own
  decline threshold, coefficient table and window, and several amended retroactively. Encoding
  a snapshot of them would produce exactly the failure this skill exists to prevent, a
  confident number attached to the wrong qualifying period, and the house rule for this skill is
  that no figure may be sourced from a blog, a press release or a CPA summary. The skill
  therefore states the MECHANISM for Iron Swords and routes the claimant to the operative
  regulation for the numbers. **Where the claimant obtains the figure:** the Tax Authority track
  index at https://www.gov.il/he/Departments/DynamicCollectors/compensation-tracks names the
  operative track and period, and the full regulation text
  (תקנות מס רכוש וקרן פיצויים (תשלום פיצויים)(נזק מלחמה ונזק עקיף)(חרבות ברזל)(הוראת שעה),
  תשפ"ד-2023, as amended) carries the decline percentage and coefficient for that period; the
  claim form itself states the window. Re-open this row if the Iron Swords orders are ever
  consolidated into a single published text, or if a checker is built for that framework.

- Direct property damage (broken windows, structure damage, vehicle damage from rocket/drone hits) - covered by Tax Authority direct-damage track. - related skill: `israeli-war-damage-claims` handles it.
- Personal/family grants for evacuated residents - accommodation grant, evacuee per-diem. Different agency (Ministry of Interior + Tefen). - related skill: `israeli-bituach-leumi` and future evacuee-specific skill handles it.
- Bituach Leumi dmei avtala employee-side claim - the employee's filing on Bituach Leumi portal. - related skill: `israeli-unemployment-benefits-navigator` handles it; this skill covers the EMPLOYER side only.
- VAT exemption / postponement during war - cash-flow relief, not a compensation grant. - related skill: `israeli-vat-reporting` (or general accounting skills) handles VAT postponement.
- Mental-health / trauma compensation for business owners - handled separately by Bituach Leumi nifgaei eivah. - related skill: `israeli-mental-health-navigator` handles trauma services.

## Authoritative sources

- https://www.nevo.co.il/law_html/law01/273_001.htm - Full text of חוק מס רכוש וקרן פיצויים תשכ"א-1961. Verify §§35, 36 (definitions, indirect damage, ועדת ערר).
- https://www.gov.il/he/pages/press_11032026 - Tax Authority press release on Shaagat HaAri framework (11.03.2026). Verify the advance mechanism, 20% employer reservist comp, filing extensions.
- https://www.gov.il/he/service/compensation-indirect-damage - Official filing portal for nationwide indirect-damage. Verify form name, registration prerequisite, contact channels.
- https://www.gov.il/he/Departments/DynamicCollectors/compensation-tracks - Tax Authority master index of indirect-damage tracks. Verify track exclusivity.
- https://www.kolzchut.org.il/he/פיצוי_לבעלי_עסקים_על_הפסדים_עקב_מלחמת_חרבות_ברזל - Plain-language entitlement entry for general business compensation.
- https://www.kolzchut.org.il/he/פיצוי_לבעלי_עסקים_ששירתו_במילואים_במלחמת_חרבות_ברזל_או_במלחמה_מול_איראן - Reservist business-owner grant.
- https://www.btl.gov.il/About/news/Pages/hadasa2026saagathaaryiran.aspx - Bituach Leumi Shaagat HaAri updates. Verify the bifurcated 5/10-day חל"ת threshold and employee-side filing flow.

## Must cover (statutory core) -- these regressed once and must be checked every cycle

Source of truth: חוק התוכנית לסיוע כלכלי (הוראת שעה)(סיוע לעסקים ולמוסדות ציבור), התשפ"ו-2026
(https://fs.knesset.gov.il/25/law/25_lsr_12958311.pdf). Do NOT source any figure in this
skill from a blog, a press release, or a CPA-firm summary; go to the statute.

- **§38לו: הוצאות מזכות = הוצאות קבועות + חלק השכר המזכה, capped, THEN x2.** The wage
  part and the fixed-cost part are ADDED. "Run both tracks, pay the higher" is WRONG and
  understates the grant for any business with both payroll and fixed costs.
- **The cap is doubled too:** 600K -> 1.2M effective (turnover <= 100M); 600K + 0.3% of the
  excess (100M-300M); 1.2M -> 2.4M (300M-400M).
- **הוצאות קבועות = prior-year total VAT inputs / 6 x coefficient**, NOT the owner's monthly
  rent/electricity/leasing.
- **Sector factors MULTIPLY the tier rate, they do NOT replace it:** fuel x0.35,
  VAT-§33-exempt x0.19, קבלן ביצוע x0.68, director's discretion capped at x2. The statute
  reads "השיעור כאמור בסיפה של אותן פסקאות משנה ... מוכפל ב־0.35". Fuel at a 50% decline is
  11% x 0.35 = 3.85%, not 35%.
- **הוצאות השכר is the LOWER OF TWO LIMBS and limb (a) carries 0.75:**
  min(0.75 x eligible-employee wages x 1.25, average wage x eligible employees x 1.25).
  The decline rate multiplies the lower-of result ONCE, afterwards. Raw Form-102 gross is
  not the wage base.
- **Three claimant classes for BOTH הוצאות השכר and הוצאות קבועות.** Wage: general (1.25);
  מוסד ציבורי זכאי (1.325 and the non-donation income ratio in both limbs); קיבוץ (1.25,
  counting non-members and members in industry/commerce/services/agriculture/tourism, excluding
  members serving the kibbutz members themselves). Fixed: general (inputs / 6 x coef);
  מוסד ציבורי זכאי (prior-year cost of services/products sold / active months x coef x 2);
  s.56 group-registered dealer (notional standalone inputs / 6 x coef).
- **תקופת הזכאות:** March-April 2026, EXCEPT a cash-basis filer and a קבלן ביצוע, for whom the
  statute fixes it at May-June 2026. The wage qualifying period stays March-April 2026 for all.
- **Bands are (low, high]:** exactly 40% decline -> the 7% tier (and damage coefficient 1).
- **§38לז(ב): the small-business (<=300K) amounts are PER MONTH and paid at x2.** The table
  in SKILL.md is the already-doubled one (3,728 / 6,712 / 8,950 / then damage-coefficient
  scaled). Quoting the statute's raw numbers halves every small business's grant.
- **The >25% decline gate applies to EVERY track, including small business** (§38לז(ב)
  incorporates (a)(2)). A business at or below 25% gets nothing. Never route it to the
  small-business track as a "fallback".
- **§38לז(ג) floor:** a nationwide-track business receiving less than the top small-business
  band gets that band's amount instead.
- **Average wage = 13,769** (the s.2(b) figure "as known in March 2026"), not 13,773.
- **Wage base deductions:** minus vacation pay used, minus BTL reserve-duty reimbursements.
- **Advances:** 60% at 21 days; an ADDITIONAL 10% at 150 days if no decision (70% total);
  deemed approval at 8 months. The 150-day milestone is NOT the final determination.
- **Appeals:** השגה 60 days to a Director-authorised employee (NOT the issuing officer);
  ערר 60 days to the ועדת ערר under §21 of the 2020 Corona economic-assistance law. Not §38ל.
- **Hard cliff:** the business must have OPENED **before 01.03.2026**, with the Tax Authority
  notified of the opening by 28.02.2026 (§38לז(א)(4)). A business opened ON 28.02.2026 is
  inside the cliff. The 01.01.2025 pivot only changes the baseline formula. The separate
  ניזוק exclusions bite too: closure reported before 01.03.2026, zero turnover in the four
  preceding months, or inactivity before 01.03.2026 (presumed if two of the last three VAT
  returns were not filed, rebuttable).
