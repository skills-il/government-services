---
name: israeli-aliyah-navigator
description: Comprehensive guide for new immigrants (olim) to Israel covering the full aliyah journey from pre-arrival to settlement. Use when user asks about "aliyah to Israel", "sal klita", "absorption basket", "misrad haklita", "klitat aliyah", "teudat oleh", "ulpan enrollment", "oleh chadash rights", "tax benefits for olim", or "driver's license conversion in Israel". Covers Misrad HaKlita processes, sal klita tracking, Ulpan, housing, banking, Bituach Leumi, tax exemptions, license conversion, and professional recognition. Do NOT use for general Israeli bureaucracy unrelated to immigration (use israeli-gov-services instead) or tourist visa questions.
license: MIT
allowed-tools: Bash(python:*)
compatibility: No special requirements. Works with Claude Code, Cursor, Windsurf.
---

# Israeli Aliyah Navigator

## Instructions

### Step 1: Assess the Oleh's Situation

Before providing guidance, ask about: **stage** (pre-arrival / first week / first month / first year / beyond, determines relevant steps), **family status** (single / couple / family with children, affects sal klita amount and housing), **country of origin** (USA, Russia, France, Ethiopia, etc., affects license conversion and professional recognition), **profession** (determines licensing path), **Jewish Agency involvement** (Nefesh B'Nefesh for English-speaking countries), and **Hebrew level** (determines Ulpan recommendation).

Based on responses, generate a personalized checklist using:

```bash
python scripts/aliyah-checklist.py --stage <stage> --family <status> --country <country> --profession <profession>
```

### Step 2: Pre-Arrival Checklist

Guide the user through pre-arrival requirements:

**Jewish Agency and Consulate Process:**
1. Open a file with the Jewish Agency for Israel (Sochnut)
2. Schedule an appointment at the Israeli consulate
3. Choose your visa path: **Oleh visa** (immediate aliyah under the Law of Return, full benefits) or **A1 temporary residence** (1-year renewable trial, no aliyah benefits, no military obligation). A1 holders can switch to oleh status later via Shinui Ma'amad (see Step 2b). See `references/aliyah-additional-procedures.md` for the comparison table.
4. Receive **Ishur Chok HaShvut** (Confirmation of Eligibility under the Law of Return), the formal letter the Jewish Agency issues once your file passes review. Bring the original to the consulate and present it on arrival.
5. Gather required documents:
   - Proof of Jewish identity (birth certificate, parents' ketubah, letter from rabbi)
   - Valid passport, recommended at least 2 years remaining validity; dual-citizen olim bring all passports and coordinate with the Jewish Agency on which to use
   - Marriage certificate (if applicable). Effective Sept 30 2024, the certificate must show the applicant's pre-marriage civil status (single / divorced / widowed). Any prior marriages also need supporting divorce or death certificates with apostille.
   - Children's birth certificates (if applicable)
   - Police clearance / Certificate of Good Conduct from country of birth, every country of continuous residence over 1 year after age 14, and every country of current citizenship. Effective Nov 2024, applicants doing Shinui Ma'amad (status change to oleh from inside Israel) must also present background checks from every country they lived in for 6+ months.
   - Professional diplomas and transcripts (apostilled)
   - Medical records and vaccination history. Bring 3 months' worth of any regular medication and complete vaccination cards (required for children's school enrollment).
   - Apostille requirement: every public-record document (birth, marriage, divorce, background check, academic diploma) must carry an apostille from the issuing country's Hague Convention authority. Non-Hague countries require consular legalisation instead.
   - **Converts (giyur):** in addition to the standard list, provide 4 letters: rabbi's letter on pre-conversion preparation, rabbi's letter on communal participation, external Beit Din letter (if applicable), and a personal letter from the applicant. All dated, ink-signed, and stamped. **Reform / Conservative converts:** Misrad HaPnim accepts the conversion for aliyah but the Israeli Rabbanut does NOT for marriage/divorce/burial; consult ITIM (itim.org.il) before marriage decisions. See `references/aliyah-additional-procedures.md`.
   - **Edge-case applicants** (special-needs adults aged 21+, adopted children, families bringing pets) follow modified document and process tracks. See `references/aliyah-additional-procedures.md` for the per-case requirements before assuming the standard flow applies.

**Nefesh B'Nefesh (for English-speaking countries):**
- Free aliyah assistance for olim from USA, Canada, and UK
- Flight subsidies and group flights
- Pre-aliyah employment guidance
- Airport welcome and first-day assistance
- Website: nbn.org.il

**Before Departure:**
- Notify banks about international transfers
- Obtain certified translations of key documents (Hebrew or English)
- Research health insurance options (kupat cholim selection)
- Consider shipping personal belongings (tax-free container for olim)
- Download Israeli banking apps and government service apps

### Step 2b: Shinui Ma'amad (Aliyah from within Israel)

If the applicant is already inside Israel on a tourist, A1, student, work, or family-reunification visa, they apply for status change to oleh chadash via Misrad HaPnim (Population and Immigration Authority), not at Ben Gurion arrival. **Step 3 below does NOT apply to this path**: the Teudat Oleh and initial sal klita are issued at Misrad HaPnim and Misrad HaKlita branches inside Israel.

From November 2024, Shinui Ma'amad applicants must present background checks from every country they lived in for 6+ months (broader than the standard rule). Document set is otherwise the standard aliyah list from Step 2. See `references/aliyah-additional-procedures.md`.

### Step 3: Arrival and First-Week Essentials

**At Ben Gurion Airport:**
1. Proceed to the Ministry of Absorption (Misrad HaKlita) desk at arrivals
2. Receive Teudat Oleh (oleh certificate), valid for identification until Teudat Zehut is issued
3. Receive initial sal klita cash payment
4. Receive a free SIM card with starter credit
5. If arriving via Nefesh B'Nefesh group flight, representatives will be present

**First-Week Priority Actions:**

| Priority | Task | Where | Documents Needed |
|----------|------|-------|-----------------|
| Day 1-2 | Register at Misrad HaPnim (Interior Ministry) | Local branch | Teudat Oleh, passport, photos |
| Day 1-2 | Receive Teudat Zehut (Israeli ID) | Misrad HaPnim | Automatic after registration |
| Day 1-3 | Open bank account | Any major bank branch | Teudat Oleh/Zehut, passport |
| Day 1-3 | Register with a kupat cholim (HMO) | Clalit, Maccabi, Meuhedet, or Leumit | Teudat Zehut |
| Day 1-7 | Register at Bituach Leumi (National Insurance) | Local branch or online | Teudat Zehut |
| Day 1-7 | Get Israeli phone number | Any carrier store | Teudat Zehut |
| Day 1-7 | Open a MyGov account (gov.il Ezor Ishi Ezrach) | gov.il portal | Teudat Zehut + Israeli SIM for SMS verification |
| Week 1 (families with children 3-18) | Enroll children in gan / beit sefer | Local municipality education department | Teudat Zehut + birth certificate; Misrad HaChinuch oleh program (Sela) provides absorption classes + free tutoring |
| Week 1-2 | Register for Ulpan | Misrad HaKlita or local municipality | Teudat Oleh |

**Refund of pre-aliyah government payments:** olim sometimes pay government fees (passport processing, document apostille, consular fees) before they hold a Teudat Oleh. Some are reimbursable by Misrad HaKlita against original receipts; file the request at the absorbing branch within the first year. See `references/aliyah-additional-procedures.md`.

### Step 4: Sal Klita (Absorption Basket)

The sal klita is a financial grant provided by Misrad HaKlita to help olim during their first months.

**Eligibility:**
- All olim who arrived under the Law of Return
- Must register with Misrad HaKlita within the first year
- Paid in monthly installments to the oleh's Israeli bank account

**Payment schedule:** lump sum at airport, monthly installments for months 1-6, and a final payment in month 7 for couples and families (singles end at month 6). Amounts are updated annually by Misrad HaKlita; calculate estimates:

```bash
python scripts/sal-klita-calculator.py --family-size <number> --year <year>
```

**Tracking Payments:**
- Log in to the Misrad HaKlita personal area (ezor ishi) at klita.gov.il
- Check bank account for monthly deposits
- Contact Misrad HaKlita branch if a payment is delayed beyond the expected date
- Keep Teudat Oleh and bank details updated

**Important notes:** Sal klita is not taxable income, does not need to be repaid, varies by family composition, and is linked to cost-of-living adjustments. Olim who delay opening a bank account may experience delayed payments.

### Step 5: Ulpan (Hebrew Language Program)

**Free Ulpan for Olim:**
- Every oleh is entitled to a free 500-hour Hebrew course (Ulpan Aleph)
- Must begin within 18 months of aliyah date
- Attendance requirement: 80% minimum; missing more days can drop the oleh from the subsidized track
- Second subsidized course (e.g., Ulpan Bet) available within 10 years of aliyah; only one of the two courses can be at a private/recognized institution, the rest must be at a Misrad HaKlita-recognized public ulpan
- Registration through Misrad HaKlita or local municipality

**Ulpan options:** Morning Ulpan (boker, Sun-Thu 8-13, 5 months, full-time learners); Evening Ulpan (erev, Sun-Thu 17-20, 10 months, working olim); Kibbutz Ulpan (immersive, 5 months, ages 18-35); Online Ulpan (flexible, for remote workers and parents); Private Ulpan (paid, custom schedule, for profession-specific vocab).

**Levels:** Aleph (א׳, beginners, free), Bet (ב׳, intermediate, sometimes subsidized), Gimel (ג׳, advanced, usually paid), Dalet+ (ד׳+, academic/professional).

### Step 6: Housing for Olim

**Finding a rental:** Yad2 (yad2.co.il) is the primary Israeli classifieds site; city-specific Facebook groups (e.g., "Secret Tel Aviv") supplement. Real-estate agents (metavchei nadlan) typically charge one month's rent. Mercazei klita (absorption centers) provide temporary housing.

**Rental requirements:** guarantees (arevut) of typically 3 months' rent via bank guarantee or guarantors, post-dated checks (chekim dechuyim) for monthly rent, arnona (municipal tax), vaad bayit (building maintenance fee).

**Oleh housing benefits:** arnona discount up to 90% for the first 12 months, means-tested rental assistance from Misrad HaKlita, temporary housing at mercazei klita, reduced mas rechisha (purchase tax) on first property. See `references/tax-benefits-olim.md` for the mas rechisha oleh brackets.

**Buying property:** lawyer (orech din) required for all real estate transactions, tabu (land registry) registration, mortgage (mashkanta) available with oleh benefits from Israeli banks.

### Step 7: Banking for Olim

**Opening a Bank Account:**

Major Israeli banks:

Major Israeli banks for olim: Bank Leumi (large network, English staff in major cities), Bank Hapoalim (largest, dedicated oleh programs), Bank Discount (digital-friendly, competitive for young olim), Bank Mizrahi-Tefahot (strong mortgage department), Bank Mercantile (smaller, more personal service).

**Required Documents:**
- Teudat Zehut or Teudat Oleh
- Passport
- Proof of address (rental contract or utility bill)
- Proof of income or employment letter (if available)

**Banking considerations:** open the account as early as possible (sal klita requires an Israeli account). Request online banking + English app if needed. For large transfers use dedicated services (Wise, OFP) over bank rates. Chekim (checks) are still common for rent. Set up standing orders (horaat keva) for arnona, vaad bayit, utilities. Foreign income has the 10-year exemption (Step 8).

**Bringing money declaration:** cash and bearer instruments brought into Israel must be declared at customs if the total exceeds the threshold (NIS 50,000 standard, higher for first-time-entry olim per ITA guidance). Verify current threshold before traveling. See `references/aliyah-additional-procedures.md`.

### Step 8: Tax Benefits for Olim

Israel offers significant tax benefits for new immigrants under Section 14 of the Income Tax Ordinance.

**10-Year Foreign Income Exemption:**
- Olim are exempt from Israeli tax on foreign-source income for 10 years from aliyah date
- Covers: foreign pensions, rental income abroad, dividends, capital gains from foreign assets
- **Important (2026 change):** Olim arriving from January 1, 2026 onwards must report all worldwide income and assets, even if the income is tax-exempt. The reporting exemption was abolished while the tax exemption remains
- Olim who arrived before January 1, 2026 retain both the tax exemption and the reporting exemption
- Applies to both olim chadashim (new immigrants) and toshavim chozrim vatikim (veteran returning residents, 10+ years abroad)

**Tax credit points (nekudot zikui):** 3 additional points for months 1-18, 2 for months 19-30, 1 for months 31-42 (3.5 years total). Apply automatically when the employer is notified via Form 101. Each point reduces monthly tax by approximately NIS 235. Cumulative benefit roughly NIS 30,000-50,000 over 3.5 years. See `references/tax-benefits-olim.md` for the full schedule.

**Additional tax benefits:** reduced customs duties on importing personal belongings (including a vehicle, within time limits), tax-free container shipment of household goods, potential VAT exemption on certain purchases (first car, appliances) within eligibility windows.

**New-oleh Israeli-source income exemption (2026 incentive window):**

A new tax incentive grants olim and toshavim chozrim vatikim who establish Israeli residency between **November 5, 2025 and December 31, 2026** a tiered exemption on **Israeli-source earned income** (employment salary and self-employment only, NOT passive income), on top of the standard 10-year foreign-income exemption.

| Tax year | Exemption ceiling on earned Israeli-source income |
|---|---|
| 2026 | up to NIS 600,000 |
| 2027 | up to NIS 1,000,000 |
| 2028 | up to NIS 1,000,000 |
| 2029 | up to NIS 350,000 |
| 2030 | up to NIS 150,000 |

- **Related-party cap:** when working for a related party (own company, family business), the exemption is capped at NIS 140,000 per year for all years 2026-2030.
- **75-day residency requirement:** eligibility is lost if you spend fewer than 75 days in Israel during 2028 or 2029, or cease being an Israeli tax resident in those years.
- **Earned income only:** rental, interest, dividends do NOT qualify. The standard Section 14 ten-year foreign-income exemption remains intact.
- Olim arriving outside the November 5, 2025 - December 31, 2026 window do NOT receive this incentive, only the standard Section 14 benefits.

Source: Shivat Zion 501000361627 (Tax Reform 2026).

**Acclimatization Year and the tax clock:**

Returning Israelis can elect a one-year "Acclimatization Year" (shnat hatzharat tochnit) before the Section 14 ten-year clock starts. New olim (under the Law of Return) do NOT have this election; their 10-year clock starts on the aliyah date as recorded on the Teudat Oleh. The Acclimatization Year is a returning-resident tool, NOT an oleh tool, and confusing the two leads to wrong residency-start advice. For toshav chozer cases, route the user to `israeli-toshav-chozer-vatik-tax-planner`.

**Buying a car with olim benefits (3-year window):** olim can purchase a car in Israel with reduced purchase-tax benefits within 3 years of aliyah. One car per family, M1 passenger class. The car cannot be sold within 4 years of registration without paying back the discount. See `references/aliyah-additional-procedures.md` for conditions.

**Capital declaration / asset cap on sal klita (2025/2026):**

Sal klita applicants must now submit a capital declaration (הצהרת הון). Reported assets above NIS 500,000 reduce or deny eligibility. Applicants below the threshold receive a +10% top-up. Confirm the current threshold + top-up at klita.gov.il before applying, since these figures are subject to budget-cycle adjustment.

**Bituach Leumi US-Social-Security coordination:** olim from the US who continue paying US Social Security contributions may be eligible for limited exemption from corresponding Bituach Leumi contributions under the US-Israel totalization arrangement. Specific duration and eligibility depend on the totalization agreement scope and recent BL/SSA amendments. Verify directly with Bituach Leumi (*6050) and the SSA international office before relying on this; cite the current rule, not historical specifics.

**Reporting:** Israeli-source income is reported normally from day one. File an annual tax return (doch shnati) if income exceeds the filing threshold or if 2026-onwards reporting rules apply. Consult `references/tax-benefits-olim.md` for the full exemption rules and thresholds. For complex cases (significant foreign assets, businesses abroad), consult a yo'etz mas specializing in olim; Rashut HaMisim has a dedicated olim department.

### Step 9: Bituach Leumi (National Insurance)

**Registration:**
- All olim must register with Bituach Leumi (National Insurance Institute)
- Registration can be done at a local branch or online at btl.gov.il
- Registration triggers health insurance coverage via kupat cholim

**Benefits eligibility timeline:** Health insurance (bituach briut) is immediate via kupat cholim registration. Child allowances (kitzvat yeladim) are immediate for children under 18. Maternity grant (maanat leidah) requires a qualifying period of residency. Unemployment (dmei avtalah) requires 12 months of employment. Disability (nechut) is immediate for severe cases pending assessment. Old-age pension (kitzba) is based on years of residency and contributions, at standard retirement age.

**Health insurance (kupat cholim):** choose one of four HMOs (Clalit, Maccabi, Meuhedet, Leumit). Basic coverage (sal briut) is universal by law and funded through Bituach Leumi contributions, but you must actively register with your chosen kupat. Supplementary insurance (bituach mashlim) is optional. Switching is allowed in transfer periods (typically twice a year).

**Payments:** Bituach Leumi contributions are deducted from salary for employees; self-employed (atzmai) pay monthly directly. Olim not yet employed should verify their contribution status to maintain coverage.

**Child Savings Plan (Chisachon LeKol Yeled):** Bituach Leumi automatically opens a savings plan for every child up to age 18, funded by monthly state deposits. For olim parents the plan is opened once the child has a Teudat Zehut. Parents can optionally double the deposit by adding their own contribution and choose between a bank account (default for under-21 months) or a kupat gemel. Activate via the Bituach Leumi personal area in the first month. See `references/aliyah-additional-procedures.md`.

### Step 10: Driver's License Conversion

Conversion is based on driving experience, not country of origin (the country-based system was replaced in August 2017).

| Driving Experience | Process |
|---|---|
| 5+ years consecutive | Administrative conversion only (medical certificate + documents, no tests) |
| 2-5 years | Short practical test (mivchan shlita); no theory test |
| Less than 2 years | Full theory + practical testing, typically ~28 lessons |

**Conversion window:** 5 years from aliyah date. The foreign license itself stays valid in Israel for up to 1 year from your last entry to Israel, with the clock resetting if you spend 6+ months continuously abroad. After 5 years without converting, you complete a full Israeli licensing process regardless of prior experience.

See `references/driver-license-conversion.md` for the full per-tier procedure, required documents, theory-test languages, and common rejection reasons.

### Step 11: Professional License Recognition

Professional recognition (hakarat miktzoa) varies by field. The general path is: apostille all academic documents, get certified Hebrew translations, submit to the relevant recognizing body, complete any required exams or supplementary training, and receive an Israeli professional license (rishyon miktzoi).

| Field | Recognizing body | Typical timeline |
|---|---|---|
| Medical (physician, dentist, nurse, pharmacist, psychologist) | Misrad HaBriut (Ministry of Health) | 1-2 years for physicians (credential review + Hebrew exam + stazh) |
| Engineering | MAHAT or the relevant engineering union | Months; pre-approval from abroad possible |
| Law | Israel Bar Association | 2-3 years (Hebrew bar exam + stazh) |
| Accounting | Council of CPAs (moetzet roei cheshbon) | Months; "New Oleh Accountant" streamlined track for 2+ years experience |
| Teaching | Misrad HaChinuch (Ministry of Education) | Months; Hebrew at Ulpan Bet+ required |

See `references/professional-recognition.md` for the per-field detailed process, exam requirements, recent reforms, and common rejection causes. Consult `references/aliyah-timeline-guide.md` for a month-by-month timeline of the full first year.

### Step 11b: IDF Draft, Lone Soldier, Teudat Ma'avar

Young olim are subject to Israeli military service: men ages 18-22 and women ages 18-20 receive a Tzav Rishon (first draft notice) from IDF Meitav after Misrad HaPnim registration completes. Deferrals (dechiyat sherut) are available for academic study, yeshiva, or new-oleh adjustment (up to 1 year).

**Chayal Boded (Lone Soldier):** olim who serve without parents resident in Israel get a named legal status with concrete benefits: salary supplement, one paid month off per year to visit family abroad, IDF-covered flight, dedicated counseling at Mador HaBoded, housing subsidy, and a Misrad HaBitachon end-of-service grant. Request status explicitly at induction.

**Teudat Ma'avar vs Darkon:** olim do NOT receive a full Israeli passport (Darkon) immediately. They get a Teudat Ma'avar (one-year travel document) until residency intent is demonstrated (typically 1 year + fees). Some countries do not accept it; plan international travel accordingly. See `references/aliyah-additional-procedures.md` for IDF deferrals, exemption tracks, and travel-document specifics.

### Step 12: Alternate Aliyah Statuses (Route the User Correctly)

Not every aliyah is a standard Oleh Chadash under the Law of Return. Five named statuses sit alongside the main track. Recognize which one applies before quoting Sal Klita figures or document lists, because the eligibility rules, document set, and benefit basket all differ.

| Status | Who qualifies | Key differences vs. standard oleh | Primary authority |
|---|---|---|---|
| **Ezrach Oleh** (Child of an Israeli) | Born outside Israel to a parent who held Israeli citizenship at the time of your birth | Requires proof of residence outside Israel for the past 7 years and a 7-year table of entries and exits to/from Israel. Benefit basket is similar to oleh chadash but processed under a separate file at the Jewish Agency / Misrad HaPnim. | Jewish Agency (from abroad) or Misrad HaPnim (within Israel) |
| **Katin Chozer** (Returning Minor) | Born in Israel or immigrated as a child, departed before age 14 | Applicants under 30 also need parental documentation: parents' declaration, work proof for the past 5 years, parents' entry/exit records, and proof parents resided abroad during the applicant's ages 14-18. | Jewish Agency (from abroad) or Misrad HaPnim (within Israel) |
| **Aliyah BaShenit** (Second-time Aliyah) | Previously held Israeli citizenship, formally renounced it, now wishes to resettle in Israel | Not automatically classified as Oleh Chadash; eligibility is reviewed case-by-case by Misrad HaPnim, Bituach Leumi, Misrad HaKlita, and Rashut HaMisim *independently*. May qualify for some immigrant benefits, but do NOT promise a full Sal Klita basket without ministry confirmation. | Jewish Agency (if abroad) + Ministry of Interior (if in Israel) |
| **Aliyah BeNifrad** (Split Aliyah) | Family unit (spouse, children under 21) making aliyah at different times within less than one year | Sal Klita is calculated per family unit, NOT per individual. The first arriving group receives the bulk of the family allocation; the later-arriving members receive only the remainder. Recommend arriving within a few weeks if timing is flexible. | Jewish Agency + Misrad HaKlita |
| **ARLI** (Renouncing Aliyah within 3 months) | Oleh over 18 who decides post-arrival that they do not want Israeli citizenship | Must declare in person at Misrad HaPnim within 3 months of aliyah date. Critical for olim from countries that prohibit dual citizenship and want to preserve their original passport. One parent can declare for the family with both spouses' consent. Reversible within the 3-month window. | Misrad HaPnim |

**Verify citizenship-status before any change** (marriage, divorce, birth, foreign naturalization, ARLI declaration). Check the Misrad HaPnim "Citizenship Status" page in the MyGov personal account. Out-of-date records can cause Bituach Leumi benefit suspensions or wrong IDF service-obligation calculations. Discrepancies are reported with supporting apostilled documentation.

For Toshav Chozer (returning Israeli citizen who left and is coming back, distinct from Oleh) and the in-depth Section 14 / 10-year tax exemption for Toshav Chozer Vatik, route the user to `israeli-returning-resident-navigator` and `israeli-toshav-chozer-vatik-tax-planner` respectively. Toshav Chozer is NOT a status under the Law of Return and does NOT receive the full oleh Sal Klita.

If the user has already received a Toshav Chozer certificate from Misrad HaAliyah V'HaKlita, that is a returnee certificate, not an oleh one; reroute and stop quoting oleh figures.

## Examples

### Example 1: Pre-Arrival Planning for a Family from the USA

User says: "We're a family of 4 making aliyah from the US next month. What do we need to prepare?"

Actions:
1. Run `python scripts/aliyah-checklist.py --stage pre-arrival --family family --country usa --profession tech`
2. Generate pre-arrival document checklist for family (Step 2)
3. Highlight Nefesh B'Nefesh services for US olim
4. Calculate estimated sal klita: `python scripts/sal-klita-calculator.py --family-size 4`
5. Recommend morning Ulpan for non-working spouse, evening for working spouse
6. Advise on school enrollment for children through Misrad HaChinuch

Result: Complete pre-arrival action plan with timelines, document checklist, and estimated financial support.

### Example 2: Professional License Conversion for a Doctor

User says: "I'm a physician from France, how do I get my medical license recognized in Israel?"

Actions:
1. Identify profession as medical (Step 11, Misrad HaBriut)
2. Outline the credential review process for EU-trained physicians
3. Explain Hebrew medical terminology exam requirement
4. Detail the internship (stazh) requirement at an Israeli hospital
5. Recommend relevant Ulpan with medical vocabulary focus
6. Reference the professional recognition guide in references/

Result: Step-by-step medical license recognition path with expected timeline (typically 1-2 years).

### Example 3: Understanding Sal Klita Payments

User says: "I made aliyah 2 months ago and haven't received my second sal klita payment. What should I do?"

Actions:
1. Verify the user opened an Israeli bank account and shared details with Misrad HaKlita
2. Check expected payment schedule (Step 4)
3. Calculate expected amount: `python scripts/sal-klita-calculator.py --family-size 1`
4. Advise checking the Misrad HaKlita personal area (ezor ishi) online
5. Recommend contacting the local Misrad HaKlita branch with Teudat Oleh and bank details
6. Note common causes of delay: incorrect bank details, incomplete registration

Result: Clear troubleshooting path for delayed sal klita payment with contact instructions.

### Example 4: Tax Planning for an Oleh with Foreign Assets

User says: "I have rental income from an apartment in London. Do I need to pay Israeli tax on it?"

Actions:
1. Explain the 10-year foreign income exemption (Step 8)
2. Confirm UK rental income falls under exempt foreign-source income
3. Clarify that no Israeli reporting is required for exempt foreign income
4. Advise on UK tax obligations (still apply regardless of Israeli residency)
5. Recommend consulting a dual-qualified tax advisor for complex situations
6. Reference `references/tax-benefits-olim.md` for detailed exemption rules

Result: Clear answer that UK rental income is exempt from Israeli tax for 10 years, with guidance on UK obligations.

## Bundled Resources

### Scripts
- `scripts/aliyah-checklist.py` -- Interactive checklist generator based on the oleh's situation (stage, family status, country of origin, profession). Produces a prioritized to-do list with deadlines. Run: `python scripts/aliyah-checklist.py --help`
- `scripts/sal-klita-calculator.py` -- Calculate expected sal klita (absorption basket) amounts based on family size and year. Shows payment schedule and total expected amount. Run: `python scripts/sal-klita-calculator.py --help`

### References
- `references/aliyah-timeline-guide.md` -- Month-by-month guide for the first year in Israel. Covers each phase from arrival through settlement with key milestones and deadlines. Consult when building a long-term plan for a new oleh.
- `references/tax-benefits-olim.md` -- Detailed guide to oleh tax exemptions and benefits including the 10-year foreign income exemption, tax credit points, customs benefits, and reporting requirements. Consult when advising on tax-related questions.
- `references/aliyah-additional-procedures.md` -- A1 vs Oleh visa comparison, Shinui Ma'amad procedure, converts (giyur) letter set, Aliyah BeNifrad, edge-case applicants (special-needs adults 21+, adopted children, pets), MyGov account setup, refund of pre-aliyah payments, Bringing Money customs declaration, buying a car with olim benefits, Child Savings Plan, citizenship-status verification.
- `references/driver-license-conversion.md` -- Full per-tier procedure for converting a foreign driver's license, theory-test languages, common rejection reasons. Consult when the user asks about license conversion details beyond the high-level path in Step 10.
- `references/professional-recognition.md` -- Per-field detail for medical, engineering, law, accounting, and teaching credential recognition; recent reforms; common rejection causes. Consult when the user asks about a specific profession's licensing path.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [kolzchut-mcp](https://agentskills.co.il/he/mcps/government-services/kolzchut-mcp) | Real-time fetch of rights articles from Kolzchut (the authoritative Israeli rights knowledge base). Use `kolzchut_search_rights` for "סל קליטה" / "הטבות מס לעולים" / "ביטוח לאומי עולים" / "דיור עולים" to get current-year NIS figures and eligibility rules. Fall back to the static guidance in this skill when the MCP is not installed. |

## Gotchas
- Aliyah benefits (sal klita) amounts change annually and differ by family size, age, and country of origin. Agents may quote outdated figures from previous years.
- The Ministry of Aliyah and Integration (Misrad HaKlita) and the Jewish Agency (Sochnut) handle different parts of the aliyah process. Agents may direct users to the wrong organization.
- Olim (new immigrants) receive extra tax credit points (neku'dot zikui) for 3.5 years, not permanently. Agents may fail to mention the expiration of these benefits.
- Professional license recognition in Israel can take months to years depending on the profession (doctors, lawyers, engineers each have different processes). Agents may underestimate the timeline for practicing a licensed profession after aliyah.

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Misrad HaAliyah V'HaKlita (Ministry of Aliyah and Integration) | https://www.gov.il/en/departments/ministry_of_aliyah_and_integration | Current Sal Klita amounts, Ulpan program list, returning-resident eligibility |
| Klita.gov.il personal area (ezor ishi) | https://www.klita.gov.il/ | Sal Klita payment status, rights and forms for olim |
| Kolzchut (Kol-Zchut) - Olim and returning residents | https://www.kolzchut.org.il/he/עולים_ותושבים_חוזרים | Authoritative rights pages with statute citations, current-year NIS amounts |
| Nefesh B'Nefesh (English-speaking olim) | https://www.nbn.org.il/ | Flight subsidies, rights summaries, pre-aliyah employment guidance |
| Jewish Agency (Sochnut) | https://www.jewishagency.org/aliyah/ | File opening, document upload, eligibility verification |
| Shivat Zion knowledge base (EN/HE plain-English explainers) | https://shivatzion-support.freshdesk.com/en/support/solutions/501000214842 | Apostille per country, background-check authorities by country, document checklist, alternate-status overviews (Ezrach Oleh, Katin Chozer, Aliyah BaShenit, ARLI) |
| Bituach Leumi | https://www.btl.gov.il/ | Registration, benefit eligibility timelines for new residents |
| Israel Tax Authority (Rashut HaMisim) - Olim department | https://www.gov.il/en/departments/israel_tax_authority | Section 14 exemption details, reporting obligations |

## Troubleshooting

### Error: "Sal klita payment not received"
Cause: Incomplete bank registration, incorrect account details, or delay in Misrad HaKlita processing.
Solution: Verify bank account is active and details were provided to Misrad HaKlita. Check the personal area (ezor ishi) at klita.gov.il. Visit local Misrad HaKlita branch with Teudat Oleh and bank statement.

### Error: "Professional license application rejected"
Cause: Missing documents, documents not apostilled, or insufficient Hebrew translations.
Solution: Ensure all academic documents have an apostille from the country of origin. Provide certified Hebrew translations. Contact the specific licensing body for their exact document requirements. Some professions require additional Israeli exams.

### Error: "Foreign driver's license expired before conversion completed"
Cause: Conversion process not started within the 1-year validity window.
Solution: The conversion window is **5 years from aliyah date**. The 1-year clock applies separately to the foreign license itself (counting from your last entry to Israel; resets after 6+ months abroad). Within 5 years of aliyah, you can still convert per the experience-based tiers. Past 5 years, you must complete the full Israeli licensing process (theory + practical). Contact the local licensing office (misrad harishui) for options.

### Error: "Kupat cholim registration issues"
Cause: Bituach Leumi registration incomplete or not processed.
Solution: First verify Bituach Leumi registration is complete. Bring Teudat Zehut to the chosen kupat cholim branch. Registration should be processed within 1-2 business days. If issues persist, contact Bituach Leumi at *6050.
