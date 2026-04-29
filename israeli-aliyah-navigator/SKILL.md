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

Before providing guidance, determine the user's current stage and circumstances. Ask about:

| Factor | Options | Impact on Guidance |
|--------|---------|-------------------|
| Stage | Pre-arrival, first week, first month, first year, beyond | Determines which steps are relevant |
| Family status | Single, couple, family with children | Affects sal klita amount and housing |
| Country of origin | USA, Russia, France, Ethiopia, other | Affects license conversion, professional recognition |
| Profession | Medical, engineering, law, accounting, teaching, tech, other | Determines professional licensing path |
| Jewish Agency involvement | Yes, no, Nefesh B'Nefesh | Affects available support channels |
| Hebrew level | None, basic, intermediate, advanced | Determines Ulpan recommendation |

Based on responses, generate a personalized checklist using:

```bash
python scripts/aliyah-checklist.py --stage <stage> --family <status> --country <country> --profession <profession>
```

### Step 2: Pre-Arrival Checklist

Guide the user through pre-arrival requirements:

**Jewish Agency and Consulate Process:**
1. Open a file with the Jewish Agency for Israel (Sochnut)
2. Schedule an appointment at the Israeli consulate
3. Obtain an aliyah visa (if required based on country)
4. Gather required documents:
   - Proof of Jewish identity (birth certificate, parents' ketubah, letter from rabbi)
   - Valid passport (minimum 6 months validity)
   - Marriage certificate (if applicable)
   - Children's birth certificates (if applicable)
   - Police clearance from country of origin
   - Professional diplomas and transcripts (apostilled)
   - Medical records and vaccination history

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
| Week 1-2 | Register for Ulpan | Misrad HaKlita or local municipality | Teudat Oleh |

### Step 4: Sal Klita (Absorption Basket)

The sal klita is a financial grant provided by Misrad HaKlita to help olim during their first months.

**Eligibility:**
- All olim who arrived under the Law of Return
- Must register with Misrad HaKlita within the first year
- Paid in monthly installments to the oleh's Israeli bank account

**Payment Schedule:**

| Installment | Singles | Couples | Family (1-2 children) | Family (3+ children) |
|-------------|---------|---------|----------------------|---------------------|
| At airport | Lump sum | Lump sum | Lump sum | Lump sum |
| Months 1-6 | Monthly | Monthly | Monthly | Monthly |
| Month 7 | N/A | Final payment | Final payment | Final payment |

Exact amounts are updated annually by Misrad HaKlita. Calculate estimated amounts:

```bash
python scripts/sal-klita-calculator.py --family-size <number> --year <year>
```

**Tracking Payments:**
- Log in to the Misrad HaKlita personal area (ezor ishi) at klita.gov.il
- Check bank account for monthly deposits
- Contact Misrad HaKlita branch if a payment is delayed beyond the expected date
- Keep Teudat Oleh and bank details updated

**Important Notes:**
- Sal klita is not taxable income
- The grant does not need to be repaid
- Olim who delay opening a bank account may experience delayed payments
- Amounts vary by family composition and are linked to cost of living adjustments

### Step 5: Ulpan (Hebrew Language Program)

**Free Ulpan for Olim:**
- Every oleh is entitled to a free 500-hour Hebrew course (Ulpan Aleph)
- Must begin within 18 months of aliyah date
- Registration through Misrad HaKlita or local municipality

**Ulpan Options:**

| Type | Schedule | Duration | Best For |
|------|----------|----------|----------|
| Morning Ulpan (boker) | Sun-Thu, 8:00-13:00 | 5 months | Full-time learners |
| Evening Ulpan (erev) | Sun-Thu, 17:00-20:00 | 10 months | Working olim |
| Kibbutz Ulpan | Immersive, live on kibbutz | 5 months | Young singles, ages 18-35 |
| Online Ulpan | Flexible schedule | Varies | Remote workers, parents |
| Private Ulpan (paid) | Custom schedule | Custom | Professionals needing specific vocab |

**Levels:**

| Level | Hebrew Name | Description |
|-------|-------------|-------------|
| Aleph | אולפן א׳ | Complete beginners, free for all olim |
| Bet | אולפן ב׳ | Intermediate, sometimes subsidized |
| Gimel | אולפן ג׳ | Advanced, usually paid |
| Dalet+ | אולפן ד׳+ | Academic/professional level |

**Survival Hebrew for Bureaucracy:**
- Teudat Zehut (teudat zehut) = ID card
- Tofes (tofes) = form
- Misrad (misrad) = office
- Tor (tor) = queue/appointment
- Asmachta (asmachta) = reference number
- Ishur (ishur) = approval/confirmation
- Bakasha (bakasha) = request/application

### Step 6: Housing for Olim

**Rental Process:**

1. **Finding an Apartment:**
   - Yad2 (yad2.co.il), the primary Israeli classifieds site
   - Facebook groups (e.g., "Secret Tel Aviv", city-specific groups)
   - Real estate agents (metavchei nadlan), typically charge one month's rent
   - Absorption centers (mercazei klita) for temporary housing

2. **Rental Requirements:**
   - Guarantees (arevut): typically 3 months' rent via bank guarantee or guarantors
   - Post-dated checks (chekim dechuyim) for monthly rent, common practice in Israel
   - Arnona (municipal tax): olim receive significant discounts (up to 90% in year one)
   - Vaad bayit (building maintenance fee): monthly payment to building committee

3. **Oleh Housing Benefits:**
   - Arnona discount: up to 90% reduction for the first 12 months
   - Rental assistance from Misrad HaKlita (means-tested, for eligible olim)
   - Temporary housing at mercazei klita (absorption centers)
   - Mortgage benefits: reduced mas rechisha (purchase tax) for first apartment

**Buying Property:**
- Mas rechisha (purchase tax) discount for olim on first property
- Tabu (land registry) registration process
- Lawyer (orech din) required for all real estate transactions
- Mortgage (mashkanta) available from Israeli banks with oleh benefits

### Step 7: Banking for Olim

**Opening a Bank Account:**

Major Israeli banks:

| Bank | Hebrew Name | Notes for Olim |
|------|-------------|---------------|
| Bank Leumi | בנק לאומי | Large branch network, English-speaking staff in major cities |
| Bank Hapoalim | בנק הפועלים | Largest bank, oleh programs available |
| Bank Discount | בנק דיסקונט | Digital-friendly, competitive for young olim |
| Bank Mizrahi-Tefahot | בנק מזרחי-טפחות | Strong mortgage department |
| Bank Mercantile | בנק מרכנתיל | Smaller, sometimes more personal service |

**Required Documents:**
- Teudat Zehut or Teudat Oleh
- Passport
- Proof of address (rental contract or utility bill)
- Proof of income or employment letter (if available)

**Important Banking Considerations:**
- Open account as soon as possible (sal klita payments require an Israeli bank account)
- Request online banking access and an app in English if needed
- Currency conversion: use dedicated services (e.g., Wise, OFP) for large transfers rather than bank exchange rates
- Foreign income: olim have a 10-year exemption on reporting foreign income (see Step 8)
- Chekim (checks) are still widely used in Israel for rent and certain payments
- Standing orders (horaat keva) for recurring payments (arnona, vaad bayit, utilities)

### Step 8: Tax Benefits for Olim

Israel offers significant tax benefits for new immigrants under Section 14 of the Income Tax Ordinance.

**10-Year Foreign Income Exemption:**
- Olim are exempt from Israeli tax on foreign-source income for 10 years from aliyah date
- Covers: foreign pensions, rental income abroad, dividends, capital gains from foreign assets
- **Important (2026 change):** Olim arriving from January 1, 2026 onwards must report all worldwide income and assets, even if the income is tax-exempt. The reporting exemption was abolished while the tax exemption remains
- Olim who arrived before January 1, 2026 retain both the tax exemption and the reporting exemption
- Applies to both olim chadashim (new immigrants) and toshavim chozrim vatikim (veteran returning residents, 10+ years abroad)

**Income Tax Benefits (Mas Hachnasa):**

| Benefit | Duration | Details |
|---------|----------|---------|
| Tax credit points (nekudot zikui) | 3.5 years | Additional credit points reducing tax liability |
| Foreign income exemption | 10 years | No tax on foreign-source income |
| Foreign pension exemption | 10 years | Foreign pensions not taxable |
| Capital gains exemption | 10 years | Gains from foreign assets exempt |

**Additional Tax Benefits:**
- Reduced customs duties on importing personal belongings (including a vehicle, within time limits)
- Tax-free container shipment of household goods
- Potential VAT exemption on certain purchases (first car, appliances) within eligibility windows

**2026 New-Oleh Israeli-Source Income Exemption (special incentive window):**

A new tax incentive enacted late 2025 grants olim and toshavim chozrim vatikim who establish Israeli residency between **November 5, 2025 and December 31, 2026** a tiered exemption on **Israeli-source earned income**, on top of the standard 10-year foreign-income exemption.

- The exemption applies to active (earned) Israeli-source income up to an annual NIS ceiling that ramps up over the first years of residency, then steps down.
- Public sources (Gornitzky, BSH CPA, Knesset MMM memo) cite slightly different schedules; verify against the final Knesset-passed text and ITA circulars before quoting specific NIS ceilings to a user.
- The 2028-2029 portion of the benefit may carry a minimum-days-in-Israel residency condition (~75 days/year per published memos). Verify before quoting.
- A separate per-family-member NIS cap (~140K) applies in addition to the primary ceiling.
- Olim arriving outside the November 5, 2025 - December 31, 2026 window do NOT receive this incentive — only the standard Section 14 benefits.

**Capital declaration / asset cap on sal klita (2025/2026):**

Sal klita applicants must now submit a capital declaration (הצהרת הון). Reported assets above NIS 500,000 reduce or deny eligibility. Applicants below the threshold receive a +10% top-up. Confirm the current threshold + top-up at klita.gov.il before applying — these figures are subject to budget-cycle adjustment.

**Bituach Leumi US-Social-Security exemption (Feb 2026 amendment):**

New olim from the United States who continue paying US Social Security contributions can be exempt from corresponding Bituach Leumi contributions for up to 5 years. Verify eligibility, the totalization-agreement scope, and any required proof-of-payment documentation with Bituach Leumi (*6050) before relying on this.

**Reporting Requirements:**
- Israeli-source income must be reported normally from day one
- File annual tax return (doch shnati) if total income exceeds the filing threshold
- Consult `references/tax-benefits-olim.md` for detailed exemption rules and thresholds

**Professional Advice:**
- Consider consulting a tax advisor (yo'etz mas) specializing in olim
- Relevant for olim with significant foreign assets, businesses abroad, or complex income sources
- The Israel Tax Authority (Rashut HaMisim) has an olim department for questions

### Step 9: Bituach Leumi (National Insurance)

**Registration:**
- All olim must register with Bituach Leumi (National Insurance Institute)
- Registration can be done at a local branch or online at btl.gov.il
- Registration triggers health insurance coverage via kupat cholim

**Benefits Eligibility Timeline:**

| Benefit | Eligibility | Notes |
|---------|-------------|-------|
| Health insurance (bituach briut) | Immediate | Via kupat cholim registration |
| Child allowances (kitzvat yeladim) | Immediate | For children under 18 |
| Maternity grant (maanat leidah) | After qualifying period | Based on months of residency |
| Unemployment (dmei avtalah) | After 12 months of employment | Standard eligibility rules apply |
| Disability (nechut) | Immediate for severe cases | Assessment required |
| Old-age pension (kitzba) | Standard retirement age | Based on years of residency and contributions |

**Health Insurance (Kupat Cholim):**
- Choose one of four HMOs: Clalit, Maccabi, Meuhedet, Leumit
- Basic coverage (sal briut) is universal by law and funded through national insurance contributions, but you must actively register with your chosen kupat cholim
- Supplementary insurance (bituach mashlim) available for additional coverage
- Can switch kupat cholim during transfer periods (typically twice a year)

**Payments:**
- Bituach Leumi contributions deducted from salary for employed olim
- Self-employed (atzmai) must make monthly payments directly
- Olim not yet employed should verify their contribution status to maintain coverage

### Step 10: Driver's License Conversion

The process for converting a foreign driver's license is primarily based on driving experience, not country of origin.

**Experience-Based Tiers:**

| Driving Experience | Process | Notes |
|-------------------|---------|-------|
| 5+ years consecutive | Administrative conversion only (no tests) | Applies to licenses from USA, Canada, UK, EU, Australia, South Africa, and other recognized countries |
| 2-5 years | Short practical test (mivchan shlita) | No theory test required |
| Less than 2 years | Full testing (theory + practical) | May need driving lessons |

**Conversion Process (5+ Years Experience):**
1. Obtain a medical fitness certificate (ishur refui) from a licensed physician
2. Submit application at a licensing office (misrad harishui) with:
   - Valid foreign license (with certified Hebrew translation)
   - Teudat Zehut
   - Medical certificate
   - Passport photos
3. Receive Israeli license (usually within 2-4 weeks)
4. Foreign license remains valid for up to 1 year from last entry to Israel (resets after 6+ months abroad). The conversion window itself is 5 years from aliyah date.

**Conversion Process (2-5 Years Experience):**
1. Same documents as above
2. Pass a short practical driving test (mivchan shlita)
3. No theory test required
4. Schedule at any testing center (via misrad harishui website)

**Conversion Process (Less Than 2 Years):**
1. Take driving lessons at a licensed school (beit sefer lenehiga)
2. Pass theory test (available in Hebrew, English, Russian, Arabic, Amharic, French)
3. Pass practical driving test
4. Theory test covers Israeli-specific road rules and signage

**Temporary Driving:**
- Foreign license valid for up to 1 year from your **last entry to Israel** (clock resets if you spend 6+ months abroad).
- The full conversion window is **5 years from aliyah date** (not 1 year). After 5 years without conversion you must complete a full Israeli licensing process (theory + practical).
- Must carry both foreign license and Teudat Oleh/Zehut while driving.
- Start conversion early to avoid gaps in driving eligibility.

### Step 11: Professional License Recognition

Professional recognition (hakarat miktzoa) varies significantly by field.

**Medical Professions (Misrad HaBriut):**

| Profession | Recognizing Body | Typical Process |
|-----------|-----------------|-----------------|
| Physician (rofe) | Ministry of Health | Credential review, Hebrew exam, internship |
| Dentist (rofe shinayim) | Ministry of Health | Credential review, licensing exam |
| Nurse (achot) | Ministry of Health | Credential review, Hebrew exam |
| Pharmacist (rokach) | Ministry of Health | Credential review, licensing exam |
| Psychologist (psicholog) | Ministry of Health | Credential review, supervised practice |

**Engineering (MAHAT):**
- Apply through MAHAT (Center for Technological Education) or the relevant engineering union
- Submit academic transcripts and professional experience documentation
- Some specializations require an equivalency exam
- Recent reform: professional engineering licenses can now be approved from abroad before making aliyah, allowing immediate work upon arrival

**Law (Israel Bar Association):**
- Foreign law degrees are NOT automatically recognized
- Must pass Israeli Bar exams (in Hebrew)
- Internship (stazh) required at an Israeli law firm
- Process typically takes 2-3 years

**Accounting (CPA):**
- Foreign CPA/CA qualifications require Israeli CPA exam
- Exam administered by the Council of CPAs (moetzet roei cheshbon)
- Some subjects may be exempted based on prior qualifications
- Must demonstrate proficiency in Israeli tax law and accounting standards
- New: "New Oleh Accountant" license available for olim with 2+ years professional experience (streamlined process)

**Teaching:**
- Apply through Misrad HaChinuch (Ministry of Education)
- Teaching credentials evaluated for equivalency
- Hebrew proficiency required (typically Ulpan Bet or higher)
- May require additional Israeli pedagogical training

**General Process for All Professions:**
1. Obtain apostille on all academic documents from country of origin
2. Certified Hebrew translation of all documents
3. Submit to the relevant recognizing body
4. Undergo evaluation (weeks to months depending on profession)
5. Complete any required exams or supplementary training
6. Receive Israeli professional license (rishyon miktzoi)

Consult `references/aliyah-timeline-guide.md` for a month-by-month timeline of the full first year.

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

## MCP Integration (Optional)

If the `kolzchut-mcp` server is available, use it to fetch **real-time, up-to-date** rights information from Kolzchut (All-Rights / כל-זכות), Israel's authoritative rights knowledge base. This supplements the static guidance in this skill with current data.

### Available Kolzchut MCP Tools

| Tool | When to Use |
|------|-------------|
| `kolzchut_search_rights` | Search for specific rights articles (e.g., "הטבות מס לעולים", "סל קליטה") |
| `kolzchut_get_article` | Read the full content of a rights article by exact title |
| `kolzchut_get_article_sections` | Get section headings before reading a long article |
| `kolzchut_get_article_section` | Read a specific section of an article |
| `kolzchut_list_category_members` | Browse all articles in "עולים ותושבים חוזרים" category |

### When to Use the MCP

- **Sal klita amounts**: Search "סל קליטה" for current-year payment schedules
- **Tax benefits**: Get the article "הטבות מס לעולים" for up-to-date tax information
- **Bituach Leumi**: Search "ביטוח לאומי עולים" for current eligibility rules
- **Housing rights**: Search "דיור עולים" for current rental assistance programs
- **Professional recognition**: Search the specific profession for current licensing requirements

### Example Workflow

1. User asks about sal klita for a family of 4
2. Use this skill's Step 4 for general guidance and structure
3. Call `kolzchut_search_rights` with query "סל קליטה" for current amounts
4. Call `kolzchut_get_article` on the relevant result for detailed breakdown
5. Combine static guidance with real-time data for the most accurate answer

**Note:** If kolzchut-mcp is not installed, all guidance in this skill remains fully functional without it.

## Gotchas
- Aliyah benefits (sal klita) amounts change annually and differ by family size, age, and country of origin. Agents may quote outdated figures from previous years.
- The Ministry of Aliyah and Integration (Misrad HaKlita) and the Jewish Agency (Sochnut) handle different parts of the aliyah process. Agents may direct users to the wrong organization.
- Olim (new immigrants) receive extra tax credit points (neku'dot zikui) for 3.5 years, not permanently. Agents may fail to mention the expiration of these benefits.
- Professional license recognition in Israel can take months to years depending on the profession (doctors, lawyers, engineers each have different processes). Agents may underestimate the timeline for practicing a licensed profession after aliyah.

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
