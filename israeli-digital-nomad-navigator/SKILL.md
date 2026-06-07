---
name: israeli-digital-nomad-navigator
description: "End-to-end guide for Israelis choosing or living digital-nomad life abroad while keeping a foothold in Israel. Use when user asks about נוודות דיגיטלית, digital-nomad visa for an Israeli passport (Thailand DTV via Tel Aviv embassy, Spain DNV, Portugal D8, Estonia, Mexico, Costa Rica, Georgia, UAE), working remotely from abroad on tlush maskoret, foreign-client invoicing under VAT Section 30, Form 1348 residency, kupat cholim continuity, or insurance that covers remote work. Branches per employment shape (Israeli employee vs freelancer with foreign clients) and covers Form A1 totalization (20-country list, US not on it), the 2026 abolition of the 10-year reporting exemption, Section 100A exit tax, foreign tax credit, and Form 5329 disclosure of Wise/Revolut/Payoneer accounts. Do NOT use for full permanent relocation (use israeli-relocation-abroad), aliyah to Israel (use israeli-aliyah-navigator), foreign nomads coming to Israel, domestic Israeli nomading, or binding tax advice."
license: MIT
---

# Israeli Digital Nomad Navigator

## Problem

Israelis going nomad face four entangled regimes at once: per-country visa rules, Israeli tax residency that follows them across borders, kupat cholim and bituach leumi continuity rules with hard cliff edges, and the freelancer-vs-employee split that decides between a totalization certificate and a VAT Section 30 zero-rated invoice. Most nomad guides ignore the Israeli side; most Israeli-side guides assume a full relocation. Decisions made (or missed) in the first 90 days routinely cost thousands of shekels and trigger a kupat cholim waiting period on return. This skill gives a phased, branch-aware checklist so nothing falls through the cracks.

## Instructions

### Step 1: Frame the situation

Before giving guidance, capture the variables that drive every downstream decision.

| Variable | Why it matters |
|---|---|
| Stage (deciding, planning, abroad <6mo, abroad >6mo, planning return) | Determines which phase applies |
| Employment shape (Israeli employee on tlush maskoret, osek murshe with foreign clients, osek murshe with mixed clients, employee + freelance, no current income) | Drives entire compliance branch |
| Destination country | Visa, totalization, tax-treaty, FX, healthcare access |
| Intended duration (≤183 days, 6-12 months, 1-3 years, open-ended) | Triggers permanent-establishment risk for the employer and Israeli tax-residency tests |
| Family status | Drives apartment, school records, insurance, accompanying-spouse rules |
| Tax-residency intent (stay Israeli resident, plan to cut residency, undecided) | Determines whether to file Form 1348, claim foreign tax credit, or aim for toshav chozer status on return |

Once these are known, branch on employment shape. Israeli-payroll employees and foreign-client freelancers face different documents and deadlines; do not give one a checklist meant for the other.

### Step 2: Pick the destination visa

Israeli passport holders can access most digital-nomad visa programs; the right pick balances income proof against stay length and tax exposure.

**Verified 2026 options for Israeli passport holders** (full per-country detail in `references/visa-by-country-2026.md`):

| Country | Program | Monthly income proof (2026) | Validity |
|---|---|---|---|
| Thailand | DTV | ฿500,000 liquid funds for last 3 months + 6 months salary slips; 350 EUR fee at Tel Aviv embassy | 5-year multi-entry, 180 days per entry |
| Spain | DNV | €2,849/month (200% of 2026 SMI) | 1-yr abroad / 3-yr from inside |
| Portugal | D8 | €3,680/month + €11,040 savings (12× min wage) | 1-yr or 2-yr renewable for 3 |
| Estonia | Type D Digital Nomad | €4,500/month gross | 1 year |
| Croatia | Digital Nomad Residence | €3,622.50/month (raised early 2026), foreign income exempt from Croatian tax | Up to 18 months, non-renewable consecutively |
| Czech Republic | Zivno | Trade license + ~€5,500 funds | 1 year, renewable |
| Mexico | Residente Temporal | ~$4,300/month for prior 6 months OR ~$74,000 savings | 1-year, renewable up to 4 total |
| Costa Rica | Estancia para Trabajadores Remotos (the digital-nomad visa, distinct from the separate Rentista visa) | $3,000/month individual or $4,000/month family | 2 years, 180-day presence to renew |
| Georgia | Remotely from Georgia | $2,000/month or $24,000 savings; from 1 Mar 2026 paid work requires Right-to-Labour-Activity permit | 365-day visa-free + permit |
| UAE | Dubai Virtual Working Programme | $5,000/month + foreign employer (raised Apr 2026 from $3,500) | 1 year, renewable |
| Indonesia (Bali) | **BARRED** for Israelis: Israel is on Indonesia's explicit E33G remote-worker exclusion list; other routes need Jakarta calling-visa pre-approval that is not granted | n/a | n/a |

**Decision rule of thumb:**
- Income too low for Spain/Portugal → Thailand DTV, Mexico Temporal, Georgia (Bali is barred).
- Want EU residency clock running → Portugal D8 (path to citizenship in 5 years).
- Heavy Schengen 90/180 risk → pick a long-stay non-Schengen country (Thailand, Georgia) for the off-quarters.
- Israeli employee staying on Israeli payroll → pick a country in `Step 4` totalization list to avoid double bituach leumi.

**Embassy/consulate workflow:** Israeli applicants typically need a passport (≥6 months remaining, 2 blank pages), an apostilled criminal-record extract (Foreign Ministry Authentication Branch in Jerusalem or the my.gov.il e-apostille flow), income proof in original currency, and a translated accommodation proof. Check the destination embassy site for translation/notary requirements.

**Schengen ETIAS pre-authorization:** Israeli passport holders need an ETIAS pre-authorization (~€20, valid 3 years) for visa-free Schengen entry, including initial trips for the Spain DNV and Portugal D8. ETIAS launches in Q4 2026 but only becomes mandatory after a roughly 6-month grace period (around April 2027); apply at the official ETIAS portal before Schengen travel once it is live.

### Step 3: Branch A - Israeli employee on tlush maskoret working from abroad

If income comes via an Israeli employer, the employer carries half the compliance load and the employee needs different documents than a freelancer.

**Employment-contract addendum (working-from-abroad agreement):** the Israeli employment contract should be amended in writing to cover:
- Days-abroad cap (most Israeli tech firms allow 30/60/90 per year before triggering review)
- Equipment policy (company laptop crossing customs, hardware shipping)
- Data security (VPN required, no client meetings on a tourist visa)
- Sick-day reporting and time-zone overlap requirements
- Reservist call-up handling (miluim duty does not pause while abroad)
- Return obligations and what counts as "demanded return"
- Tax equalization or gross-up if the employer commits to make the employee whole on foreign tax

Without this addendum, the employee's protections under Israeli labor law are still attached (Israeli employment contracts follow the employee), but enforceability in disputes around days-abroad and equipment is weak.

**Permanent-establishment risk:** If the employee stays in one country long enough, the foreign jurisdiction can deem the Israeli employer to have a "permanent establishment" (PE) there and demand corporate tax + payroll registration. The 183-day threshold is the most common trigger but several countries are stricter (Spain treats client-facing activity as PE-creating from day 1). Practical guardrails:
- Track total days per country with calendar evidence.
- No client meetings in the foreign country, no signing authority used there.
- Do not rent commercial office space in the employer's name.
- Avoid building a local team or hiring contractors abroad.

**Bituach Leumi on Israeli payroll abroad:** continues via standard payroll deduction. If the destination is on the totalization list (Step 4), file the Israeli **Certificate of Coverage** (Israeli bilateral equivalent of EU Form A1; Israel is not in EU Regulation 883/2004) with BTL to exempt the same income from the host country's social-security charges. Note: paying bituach leumi keeps kupat cholim MEMBERSHIP active but does NOT extend coverage geographically - see Step 6.

**Section 14, keren hishtalmut, pension on Israeli payroll abroad:**
- **Section 14 of חוק פיצויי פיטורים, התשכ״ג-1963** (severance-waiver: pension contributions in lieu of separate severance) is contractual, not locational. If the contract has Section 14 and the addendum keeps the same payroll, contributions continue. Keren hishtalmut deposits also continue and the 6-year liquidity clock keeps running.
- **Caveat, Employer of Record conversion:** if the employer converts the worker to a foreign payroll entity (common for stays >6 months to cut PE risk), Israeli pension stops and the keren hishtalmut balance freezes at non-liquid status until the original 6-year clock matures; it does NOT accrue on foreign payroll. Plan around this break.

### Step 4: Branch A continued - Form A1 social-security totalization

Israel has bilateral social-security agreements with **20 countries + a limited convention with Canada (excluding Quebec)**. The list, per btl.gov.il, is:

Argentina, Austria, Belgium, Bulgaria, Czech Republic, Denmark, Finland, France, Germany, Italy, Norway, Poland, Romania, Russia, Slovakia, Sweden, Switzerland, The Netherlands, United Kingdom, Uruguay.

**The United States is NOT on this list.** Israelis working from the US on Israeli payroll cannot avoid double social-security exposure via a totalization treaty - there is none. The same applies to Spain, Portugal, Mexico, Thailand, Indonesia, Georgia, UAE, Australia, and most other popular nomad destinations. Plan the cash impact accordingly.

**For destinations that ARE on the list:** request a **Certificate of Coverage** from Bituach Leumi BEFORE departure (Israeli administrative form often referred to as "טופס בל/626" or similar; the EU Form A1 is the EU coordination equivalent - Israel is NOT in EU Regulation 883/2004 so the Israeli certificate is the bilateral instrument, not literally an A1). This is the document the foreign social-security authority demands to exempt you from local contributions. Without it, you pay both Israeli bituach leumi (via Israeli payroll) AND the foreign country's social-security charge on the same wages, then have to claim a refund years later.

### Step 5: Branch B - Israeli freelancer with foreign clients

If income comes from foreign clients (US LLC, UK Ltd, EU SARL, individual abroad), a different toolkit applies.

**VAT Section 30(a)(5) zero-rating for export of services:** services rendered to a foreign resident are zero-rated for VAT under Section 30(a)(5) of the VAT Law (2002 amendment), provided three conditions are met:
1. The recipient is a "foreign resident" for VAT-Law purposes (verified residency abroad, no Israeli presence on the engagement);
2. The services are not also provided to an Israeli resident in Israel;
3. The transaction is documented in books, including the price, payment, and currency of payment.

The Tax Authority and Israeli courts have interpreted "also provided to an Israeli resident" broadly - even ancillary benefit to an Israeli party can disqualify the zero-rating. Document the foreign-resident nature of the client (incorporation certificate, foreign address, bank account abroad) in your VAT records.

**Foreign client service agreement (bilingual EN/HE):** generate a contract that includes:
- Parties + jurisdiction + governing law (Israeli law clauses, dispute venue clause);
- IP assignment (work-for-hire vs license);
- NDA / confidentiality;
- Payment in USD/EUR with stated FX-conversion method;
- Late-payment terms (an interest rate referenced to a public benchmark);
- Termination + cure periods;
- Section 30 documentation hooks (recipient address abroad, payment from a foreign account).

**W-8BEN for US clients:** US clients withhold 30% from payments to non-US persons by default. Filing **Form W-8BEN** with the client (claiming Israeli tax residency under the US-Israel tax treaty) reduces or eliminates that withholding for many service categories. The form is filed with the client, not with the IRS, and is valid 3 years.

**VAT report cycle:** osek murshe files periodic Form 836 via שע״מ (monthly/bi-monthly per classification); zero-rate transactions go in the 0%-rate row with input VAT recoverable. Osek patur unchanged.

### Step 6: Healthcare continuity

Two distinct rules - keep them separate:

**Rule 1 (geographic): Kupat cholim does NOT cover medical care abroad.** Standard sal briut coverage ends when you board the plane, regardless of bituach leumi payment. Narrow carve-out (National Health Insurance Law + Health Regulations 5755-1995) covers only specific cases where treatment is unavailable in Israel (organ transplants, certain congenital conditions, specific tumors, cardiovascular/neurocerebral diseases) - pre-approval required. A nomad who breaks a leg in Bangkok with active membership is NOT covered. **Buy separate insurance for medical care abroad - see policy options below.**

**Rule 2 (membership/continuity):** Sec. 58 of חוק ביטוח בריאות ממלכתי sets a "תקופת המתנה" on return after a continuous absence of 2+ years: 2 months per year abroad, capped at 6 months. Continuous bituach leumi payment alone does NOT eliminate this - דמי ביטוח בריאות is a separate contribution category, and reactivation paperwork on return is required. The kupot cholim charge **דמי ויתור** to keep supplementary tiers (Mushlam, Sheli, Si, Gold) active. To minimize waiting-period risk: stay an Israeli resident, pay both bituach leumi + health-insurance components via standing order, notify the kupah of the foreign address, pay dmei vitoor on supplementary tiers, file reactivation forms within 30 days of return. Verify current minimum-payment figures on the BTL self-service portal - they change annually.

**Bituach Leumi 5-year residency presumption:** BTL treats you as Israeli resident for the first 5 years abroad by default; after 5 years you must affirmatively prove the stay is still temporary or BTL reclassifies you as non-resident. Anyone planning a continuous 5+ year stretch should check in with BTL near year 4. Also file the "הודעה על שהייה בחו״ל" form when leaving for a long stretch, or contributions accrue without health entitlement.

**Travel insurance vs nomad insurance, the work-coverage trap:** standard Israeli "ביטוח נסיעות לחו״ל" policies (Harel, Migdal, Phoenix, Clal) are written for tourist trips and routinely exclude both long-term stays AND work activity, so a nomad's claim can be denied on either ground. Two setups that DO cover remote work:
- **Israeli extended-stay policies with a working-abroad rider** (Harel, Migdal, Phoenix, Clal): verify the policy explicitly says כיסוי לעבודה מרחוק; the standard tourist tier does not.
- **International nomad policies** (SafetyWing, Genki): written for nomads and explicitly cover remote work, but are catastrophic coverage only, not kupat-cholim-style preventive care.

The right setup for most: keep paying bituach leumi (kupat cholim stays alive in Israel for visits) plus a nomad policy for acute care abroad. The two layers do not overlap.

### Step 7: Banking and currency

The default Israeli bank account is poorly suited to nomad cash flow (high FX spreads, slow international SWIFT). Build a stack instead:

| Tool | Best at | Notes |
|---|---|---|
| Wise (Account) | Multi-currency holding (USD/EUR/GBP/ILS), low FX spread, local-bank IBANs in 9+ currencies | Hold balances per currency; convert at the BOI rate ±0.4% spread |
| Payoneer | Receiving from US marketplaces (Upwork, Fiverr, Amazon) | Pulls USD into a Payoneer account; transfer to Wise or Israeli bank |
| Revolut | EU IBAN + travel card | Useful for Schengen rotations |
| Israeli foreign-currency account (Hapoalim, Leumi, Discount, Mizrahi) | Holding USD/EUR inside the Israeli banking system, official-source proof for Tax Authority | Slower and more expensive for FX, but Tax Authority accepts these statements without questions |
| Israeli credit card | Day-to-day spend abroad, kept active for gov.il portals that reject foreign cards | Enable the international-fee waiver if the issuer offers it |

**FX for tax purposes:** convert foreign-currency income to NIS at the BOI representative rate (שער יציג) on the date of receipt. An annual average rate is accepted in practice for non-business recurring income; business income uses the per-transaction rate. Keep a per-transaction NIS log; BOI exposes daily rates via boi.org.il and the BOI Exchange MCP server.

### Step 8: Tax residency - staying resident vs cutting

The most consequential decision. Tested independently of citizenship.

**Days presumption:** 183+ days in Israel in the tax year, OR 30+ days that year AND 425+ days total over that year + the two preceding. **Center-of-life test (rebuttable):** the Tax Authority weighs where the family, primary home, work, social ties, and economic interests are. The days presumption can be rebutted via center-of-life evidence in either direction.

**Treaty tie-breaker (dual residency):** when both Israel and the host country claim the user as resident (e.g. Thailand at 180+ days), the bilateral tax treaty's tie-breaker rule, not the Israeli days test alone, decides where they actually pay: permanent home, then centre of vital interests, then habitual abode, then nationality. Resolve residency through the treaty for anyone over the host-country threshold.

**Form 1348 (Residency Declaration):** if the user meets the days test but claims center of life is abroad (or vice versa), file Form 1348 with the annual return. A pre-issued Tax Authority ruling (החלטת מיסוי) prevents disputes years later - recommended for stays >2 years.

| Strategy | Fits | Implication |
|---|---|---|
| Stay an Israeli tax resident | Short nomad period (<3 years), plan to return, easy to maintain Israeli ties | Report worldwide income in Israel, claim foreign tax credit, keep kupat cholim alive |
| Cut residency (nituk toshavut) | Open-ended move, family moves with you, willing to lose Israeli ties to come back later as **toshav chozer** (6+ years out - partial benefits: 5-year exemption on passive foreign income, 1-year exemption on certain interest/dividends per ITO sec. 14) or **toshav chozer vatik** (10+ years out - full 10-year tax exemption on foreign income, same regime as olim chadashim, now subject to the 2026 reporting reform) | No Israeli tax on foreign income, but kupat cholim lapses and waiting period on return |

**Rebutting the days presumption:** Form 1348 alone is not enough; the Tax Authority requires supporting evidence (foreign rental, foreign tax-residency certificate, children's school enrollment abroad, foreign employment contract). Conversely, a primary apartment in Israel (even rented out), Israeli school enrollment, an Israeli spouse staying behind, or active Israeli business ties are anchors that routinely defeat 1348 declarations.

For stays clearly under 2-3 years, default to staying resident. Cutting residency for a planned 18-month nomad period rarely pencils out.

**Section 100A exit tax (cut residency only):** most assets are deemed sold at FMV the day before residency ceases. The taxpayer ELECTS between (a) deemed-sale + full payment now, or (b) deferral until actual realization with proration AND **interest accruing on the deferred tax** (CPI-linked + 4%). Catches non-trustee ESOP/RSUs, private-company holdings, securities. **Carved out** under sec. 100A(b1): pension funds, kupot gemel, keren hishtalmut. Trustee-track 102 options need a separate tax ruling before exit. Model Section 100A before filing nituk toshavut - the deemed-sale bill on vested startup equity can be very large.

### Step 9: Annual cycle while abroad

For Israelis who stay tax resident, the annual cycle is:

**Filing deadline (tax year 2025, filed in 2026): 30 June 2026 for online filers, 29 May 2026 for paper.** The bare statutory date is 30 April, but online filers (the vast majority) always get the extension and the ITA posts the year's deadlines on gov.il. Returns via a certified accountant get further extensions:

- **Form 1301** - the base annual income-tax return for individuals (יחיד), reporting worldwide income in NIS. This is the comprehensive form covering every income type and tax benefit.
- **Form 1322** - supplement attached to Form 1301 for capital gains from marketable securities (concentration of capital gains).
- **Form 1325** - supplement attached to Form 1301 for capital gains by tax rate (used by individuals with business or investment activity).
- **Foreign tax credit (זיכוי מס זר)** under **Sections 199-210 of the Income Tax Ordinance** (Part J, Chapter 3) and any applicable bilateral tax treaty: reduces the Israeli tax bill by foreign tax actually paid on the same income, capped at the Israeli tax rate that would have applied to that income. Israel uses an income-source basket system (dividends, business, salary, etc.) with excess credits carrying forward up to 5 years per basket. Foreign tax paid in basket A cannot offset Israeli tax on basket B income.
- **Form 5329** (foreign-income-and-assets disclosure) - Israelis required to file an annual return must complete this when triggered by ITO sec. 131A thresholds. The exact threshold varies by year and category (foreign income, foreign asset balance, trust beneficiary status); confirm the current-year figure on gov.il/en/service/itc5329b before filing. Wise, Revolut, and Payoneer accounts count as foreign accounts for this purpose; report balances and account institutions.
- **Periodic VAT report (Form 836)** for osek murshe - filed monthly or bi-monthly via the Tax Authority's שע״מ e-filing portal. Zero-rated export-of-services revenue is reported in the 0%-rate row; input VAT on related expenses is still recoverable. There is no separate annual VAT return for osek murshe - the annual income-tax filing (Form 1301 + supplements) captures the year-end picture.

**2026 reporting reform (Amendment 272), important:** the 10-year exemption from REPORTING foreign income and assets (for new olim and toshav chozer vatik) was abolished for anyone becoming an Israeli resident from 1 January 2026 onward; they must report foreign income and assets from day one. The substantive tax exemption itself stays. Pre-2026 olim keep their original 10-year window.

### Step 10: Return-to-Israel handoff

If the user is moving toward a permanent return, switch to `israeli-relocation-abroad` for the full reactivation playbook (kupat cholim, toshav-chozer vehicle import, ulpan, pension). Brief flag: returning after 2+ years abroad with continuously-paid bituach leumi resumes kupat cholim immediately; a residency gap triggers a waiting period.

**2026 returnee tax window (time-limited):** legislation passed 30 March 2026 grants veteran returning residents and olim who arrived between 5 November 2025 and 31 December 2026 a graduated 5-year exemption on Israeli-source personal-services income (cap NIS 600K for 2026, NIS 1M for 2027-28, then NIS 350K in 2029 and NIS 150K in 2030), on top of the existing 10-year foreign-income exemption (subject to the Step 9 reporting reform). A return timed into this window locks in benefits unavailable before. After 31 December 2026 the window closes and the standard toshav chozer / vatik regime applies.

## Examples

### Example 1: Tel Aviv backend engineer planning 6 months in Lisbon

User: "I'm a senior backend engineer at an Israeli startup. I want to work from Lisbon for 6 months starting June. What do I need from the Israeli side?"

Flow:
1. Branch A (employee). Destination Portugal - **NOT on Israel's totalization list**, so Form A1 will not help here.
2. Visa: Portugal D8 needs €3,680/month income proof; the user's NIS salary translates to >€4,000 → fits.
3. Employment-contract addendum: draft a written working-from-abroad agreement with the employer covering 6 months, days cap, equipment, data security, return clause.
4. Social-security exposure: because Portugal has no bilateral convention with Israel, the user is at risk of being charged Portuguese Social Security on the same wages on top of Israeli bituach leumi (deducted via the Israeli payroll). Mitigations: stay under the Portuguese local-employment threshold (typically 183 days residency), do not register the Israeli employer in Portugal, and confirm the Portuguese employer-of-record rules don't apply. Brief HR/legal early.
5. Permanent-establishment risk: 6 months is at the 183-day threshold. Avoid client meetings in Portugal, do not give the employee signing authority abroad.
6. Healthcare: keep paying bituach leumi via Israeli payroll → kupat cholim active. Buy SafetyWing or a Harel working-abroad rider for acute care in Portugal.
7. Tax residency: 6 months keeps the user Israeli tax resident (days test). No nituk toshavut.
8. Annual filing: Form 1301 (the base annual return) with full Israeli income (no foreign income to report - it's all from the Israeli employer), no special foreign-asset disclosure unless the user opens a Portuguese bank account with significant balance.

### Example 2: Osek murshe in Bangkok on Thailand DTV

User: "I'm a freelance designer in year 2 of nomading from Bangkok. My clients are all US and EU agencies. I have a Wise account with a balance well above the Form 5329 reporting threshold. What's my Israeli compliance look like?"

Flow:
1. Branch B (freelancer with foreign clients).
2. Visa: Thailand DTV - already in place. Confirm 5-year validity is intact and the 180-day-per-entry pattern is being followed.
3. VAT Section 30(a)(5) zero-rating: every invoice to US/EU clients should be a 0% VAT invoice with documentation in the VAT books (foreign address, payment from a foreign account, agreement on file).
4. W-8BEN: filed with each US client to claim US-Israel treaty benefits and reduce US withholding.
5. Annual cycle:
   - Form 1301 (the base annual return; add Form 1325 for any capital gains), reporting worldwide income in NIS at BOI שער יציג.
   - Foreign tax credit for any US withholding actually paid (typically near zero if W-8BEN is filed correctly).
   - Form 5329 disclosure for the Wise account - balance above the threshold is well above the threshold. Report balance, institution (Wise), and currency.
6. Healthcare: still paying bituach leumi - confirm kupat cholim is active. Thailand is non-treaty so dual social-security exposure was a freelancer non-issue, but verify there is no inadvertent Thai tax-residency exposure (Thailand treats 180+ days as a tax-residency trigger; the user is at the threshold).

### Example 3: 14 months in Tbilisi (Georgia), kupat cholim status uncertain

User: "I've been in Tbilisi for 14 months. I think I'm still paying bituach leumi but I'm not sure. I want to know if my kupat cholim is still active and whether I should formally cut residency."

Flow:
1. Diagnostic first: have the user log into the Bituach Leumi self-service site and confirm the last 14 months of payments. If the standing order lapsed, payments stopped, and the kupat cholim membership is at risk.
2. If payments continued: kupat cholim is active. No action needed for healthcare; buy a nomad policy for acute care in Georgia.
3. If payments lapsed: catch up immediately via the Bituach Leumi portal. The minimum-payment figure depends on whether Georgia is treaty (it is not). Partial back-payment may not fully restore continuous-coverage status; check with the kupat cholim directly.
4. Georgia 1 March 2026 update: paid work activity now generally requires the new Right to Labour Activity permit on top of the visa-free 365-day stay. Georgian regulators have signaled that fully-remote workers with no Georgian clients and no local business registration may fall outside the requirement, but this is still being clarified, so confirm against legal.ge before assuming an exemption. If the user has any Georgian footprint, walk them through the permit application first.
5. Residency-cut decision: 14 months in Georgia, no specific return date, no Israeli ties currently maintained besides bituach leumi → mid-spectrum. If the user has property in Israel, family in Israel, or plans to return within 24 months, default to staying resident. If the user is committed long-term, model the toshav chozer math: 6+ years to qualify for toshav chozer, 10+ years for toshav chozer vatik with full 10-year tax exemption. Layer the 2026 returnee tax window on top if the planned return falls before 31 Dec 2026.
6. Annual filing: Form 1301 + foreign-tax-credit math + Form 5329 if foreign accounts exceed thresholds.

## Bundled Resources

This skill includes:

- `references/visa-by-country-2026.md` - verified destination-country visa table with income thresholds, fees, validity, and Israeli embassy notes
- `references/totalization-treaties.md` - full Bituach Leumi convention list with Form A1 procedure
- `scripts/nomad-decision.py` - interactive decision tree that takes the user's situation and outputs a phased checklist

## Recommended MCP Servers

| MCP | Why pair |
|---|---|
| `boi-exchange` | Daily שער יציג rates from Bank of Israel for FX conversion in tax filings |
| `kolzchut` | Authoritative Hebrew rights articles (kupat cholim continuity rules, dmei vitoor) |
| `israel-law` | Full text of Income Tax Ordinance Section 196, VAT Law Section 30, Severance Pay Law Section 14 |
| `ben-gurion-flights` | Real-time TLV departures/arrivals for travel planning |

## Gotchas

These are agent failure modes specific to this domain:

1. **Confusing relocation with nomading.** Defaulting to `israeli-relocation-abroad` advice (cut residency, file 161, freeze pension) for a 6-month workation gives the wrong answer. Nomads typically stay tax-resident and keep paying bituach leumi. Confirm intent before applying relocation logic.
2. **Assuming USA is on the totalization list.** It is not. The 20-country list does not include the United States. Telling an Israeli employee in NYC that Form A1 will exempt them from US Social Security is wrong; there is no US-Israel totalization treaty.
3. **Quoting last year's visa-income thresholds.** Spain DNV (200% of SMI), Portugal D8 (4× minimum wage), and Estonia DNV thresholds change annually with the underlying minimum wage. Always verify the current year before committing.
4. **Treating tourist travel insurance as nomad coverage.** Standard Israeli ביטוח נסיעות לחו״ל policies (Harel/Migdal/Phoenix/Clal default tier) exclude both long-term stays AND work activity. A claim from a nomad on a tourist policy is routinely denied on either ground. Verify the policy explicitly covers working remotely.
5. **Assuming working remotely on a tourist visa is fine.** Many destinations technically prohibit any work, including remote work for foreign clients, on a tourist visa. The DTV exists precisely because Thailand wanted to legitimize this. For destinations without a nomad visa, the user is in a gray zone - flag the legal risk, do not pretend it isn't there.
6. **Forgetting the 2026 reporting-exemption reform.** Pre-2026 olim still have their 10-year exemption. Olim and toshav chozer vatik becoming resident from 1 Jan 2026 onward do NOT. Apply the right rule for the user's residency-start date.
7. **Suggesting Bali to an Israeli.** Israel is on Indonesia's explicit E33G remote-worker exclusion list, and the other Indonesian routes (B211A, KITAS, Second Home Visa) need Jakarta-level "calling visa" pre-approval that is not granted to Israelis (no diplomatic relations). Bali ranks high on generic nomad lists but is categorically barred for an Israeli passport holder, not merely hard. Flag and route to Thailand or Georgia instead.

## Reference Links

| Source | URL | What to verify |
|---|---|---|
| Royal Thai Embassy DTV portal (Israel) | https://dtv.in.th/country/israel | DTV fee, financial requirements, validity for Israeli applicants |
| Bituach Leumi - International Conventions | https://www.btl.gov.il/English%20Homepage/Benefits/International%20Conventions%20on%20Social%20Security/Pages/Existingconventions.aspx | Current totalization country list, Form A1 procedure |
| Israeli Tax Authority | https://www.gov.il/he/departments/israel_tax_authority | Form 1322/1325/1348/5329 templates and filing portal |
| Israeli VAT Section 30 commentary (Lexology) | https://www.lexology.com/library/detail.aspx?g=85650020-3448-4476-a2bc-4fc847a927f9 | Section 30(a)(5) qualification rules and case-law interpretation |
| Bank of Israel - שער יציג | https://www.boi.org.il/en/ | Daily representative-rate FX history for tax conversion |
| 2026 tax reform (Israeli foreign income) | https://cpa-dray.com/he/blog/%D7%A9%D7%99%D7%A0%D7%95%D7%99%D7%99-%D7%9E%D7%A1-2026-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%9E%D7%93%D7%A8%D7%99%D7%9A-%D7%9E%D7%A7%D7%A6%D7%95%D7%A2%D7%99-%D7%9E%D7%9C%D7%90/ | Abolition of 10-year exemption from 1 Jan 2026 |

## Troubleshooting

**"The user wants me to recommend a destination country."** Do not pick for them - ask about income level, intended duration, Schengen exposure, and whether they need totalization. The visa table in Step 2 is a decision aid, not a recommendation engine.

**"The user is asking for binding tax advice."** Refuse and route to a Roeh Cheshbon. The skill is a navigator, not a CPA. Form 1348, foreign tax credit math, and Section 30 documentation should be reviewed by a licensed advisor before filing.

**"The user already filed Form 1348 incorrectly."** Direct them to the Tax Authority's amendment process (תיקון דוח). A self-correction within 4 years of the original filing is generally allowed.

**"The destination country is not in the visa table."** The table covers the most common Israeli-nomad destinations. For others (Malta, Cyprus, Greece, Argentina, Colombia, Vietnam), instruct the user to check the destination's official immigration site and confirm the income threshold and stay validity, then apply the same compliance branches (Step 3 or 5).
