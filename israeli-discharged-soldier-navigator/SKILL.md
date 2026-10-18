---
name: israeli-discharged-soldier-navigator
description: >-
  Navigate post-discharge benefits for IDF, MAGAV, Police, SHABAS, and SLE members via the MoD Department for Discharged Soldiers and Reservists (hachvana.mod.gov.il). Computes Pikadon and manak shichrur by service tier (lochem, tomech lechima, acher), checks withdrawals against the 6 permitted pre-5y purposes (studies, vocational training, driving lessons, business, marriage, apartment purchase; rental NOT included), walks Section 39a nekudot zikui via Tofes 101 and Tofes 135, and covers Mimadim 100% tuition plus the Department's own periphery scholarships. Use when a hayal meshuchrar, parent, or SLE completer asks about pikadon, manak shichrur, post-army benefits, nekudot zikui chayal meshuchrar, or free university for combat veterans. Do NOT use for miluim (israeli-miluim-manager), lone soldiers (israeli-lone-soldier-rights), third-party scholarships (israeli-academic-scholarships), or mortgages (israeli-mortgage-comparator).
license: MIT
---

# Israeli Discharged Soldier Navigator

## Legal notice

This is a free information tool operated by an AI model. It explains the rules and calculates from the figures you enter, but it does not examine your full circumstances and does not constitute advice. All of its outputs are produced automatically, with no involvement, review, or approval by an authorised representative of any of the bodies named below, and an AI model may err, omit data, or present a wrong conclusion. Eligibility, the amount, and the service classification are determined solely by the paying authority: the MoD Department for Discharged Soldiers and Reservists and its Fund for the Pikadon, the grant, Mimadim and the scholarships and programmes it runs; the Tax Authority for credit points; the National Insurance Institute for the required-work grant and unemployment benefit; and, for any other benefit mentioned, the body that grants it. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and all use of its output is the user's sole responsibility.


## Problem

A 21-year-old who just finished sherut chova has a Pikadon, a separate discharge grant, three years of tax credit points, a right to return to their pre-draft employer, and, for combat veterans, full university tuition. Each has its own deadline running from discharge. Most miss retroactive nekudot zikui, try to spend the Pikadon on rent, or let a window close.

## Instructions

### Step 1: Establish Eligibility

The Pikadon and discharge grant are governed by **Chok Klitat Chayalim Meshuchrarim, 5754-1994** (חוק קליטת חיילים משוחררים). The eligibility table:

| Service type | Minimum service | Pikadon? | Grant? |
|---|---|---|---|
| IDF mandatory (sherut chova) | 12 months | Yes | Yes |
| MAGAV (Border Police) | 12 months | Yes | Yes |
| Israel Police | 12 months | Yes | Yes |
| SHABAS (Prison Service) | 12 months | Yes | Yes |
| Sherut Leumi-Ezrachi (SLE) | 12 months | Yes (acher tier) | Yes |
| Any of the above, < 12 months, health discharge | Minimum waived, but the accrual rule is not: Pikadon is **pro-rata** (months served x tier rate) | Pro-rata | Pro-rata |
| IDF/MAGAV/Police/SHABAS soldier discharged for a training or operational injury (Head of Manpower determination, s.10A(b)) | Deemed FULL compulsory service (estimated at the 32/24 cap; a shorter obligation gives less); appeal to the Chief of Staff | Full | Full |
| Any of the above, < 12 months, voluntary exit | None | None |

> Source quote (kolzchut): "מי שהשתחררו משירות חובה בצה\"ל, במג\"ב, במשטרת ישראל, בשב\"ס, או סיימו שירות לאומי-אזרחי ושירתו לפחות 12 חודשים"

### Step 2: Compute the Pikadon Amount (2026 indexed rates)

The Pikadon accrues per month of regular service at a rate set by service type, excluding statutorily non-counted periods ("ללא תקופות בלתי נמנות"). **Unpaid service (SHLAT, hesder yeshiva periods) counts too**: s.11(a) credits "כל חודשי השירות הסדיר" and trims SHLAT only beyond the cap, and the grant page says SHLAT "יכול להשלים את תקופת הזכאות ל-32 חודשים". The tier applied to SHLAT months is not published, so confirm the figure in the personal area. Current rates from hachvana:

| Service type | English | NIS/month (August 2026) |
|---|---|---|
| לוחמים | Combat | 1,000.08 |
| תומכי לחימה | Combat support | 833.40 |
| עורפי | Rear / other | 666.72 |
| שירות לאומי-אזרחי | National-civic service (SLE) | 666.72 |
| מסלול אזרחי ביניים | Intermediate civilian track | 500.10 |
| מסלול אזרחי מפוצל | Split civilian track | 333.40 |

**Training months are reclassified DOWN, and this is the single most common over-estimate.** The MoD states it explicitly: a combat soldier's first **4** training months are credited as combat support, and a combat-support soldier's first **2** are credited as other. So 32 combat months accrue 4 x 833.40 + 28 x 1,000.08, not 32 x 1,000.08. Only the first four downgrade: training beyond four months counts as combat. A lochem or tomech lechima wounded in training or operations who moves role keeps the higher rate for the whole service.

**Caps and indexing:** hachvana publishes the operative caps as **32 months of service for a man and 24 for a woman** ("עד 32 חודשים לחייל ו-24 חודשים לחיילת"), and service beyond the cap adds nothing. **Flag the female figure rather than asserting it flatly:** s.11(a) as amended by Amendment 16 of 2014 reads "32 חודשים לחייל ו-28 חודשים לחיילת", and the commencement of the female figure is tied to regulations under s.16א(ד). Use 24, since that is what the paying authority publishes, but tell a woman who served more than 24 months to confirm her own cap with the Department before planning around it. The balance is re-indexed to the CPI at the start of each month, and it is personal, non-transferable, non-pledgeable, and non-seizable.

> Source quote (Chok Klitat Chayalim Meshuchrarim, Chapter ג): "הפקדון הוא אישי ואינו ניתן להעברה, לשעבוד או לעיקול בכל דרך שהיא"

**Always send the user to the official calculator for the personal total** at https://www.hachvana.mod.gov.il/GrantAndDeposit/DepositUpTo5/Pages/default.aspx. Give an order-of-magnitude estimate only when they supply service type and months served (capped at 32/24). These are the MoD's August 2026 figures (they were 990.63 for combat in May) and are re-indexed periodically; re-read hachvana before quoting them for a later period.

### Step 3: The Discharge Grant (Manak Shichrur)

The discharge grant is **separate** from the Pikadon. Key facts:

| Question | Answer |
|---|---|
| When, and to where | 20 to 60 days from end of service, to the account that received salary during service |
| Restrictions | None, "לכל מטרה בה תבחרו". Exempt from tax under s.9(27) (Step 7). SHLAT counts toward it as in Step 2 |
| Per-month amounts (August 2026) | Combat 691.53, combat support 575.86, **other including SLE** 460.19, intermediate civilian 345.77, split civilian 230.10. Note this is **five** tiers, not six: the grant merges orfi and SLE into one row. The training reclassification applies here too |
| Eligibility | 12 months, or less on health grounds. Lone soldiers get an advance within 14 days |

> Source quote (hachvana GrantAndDeposit): "מענק שחרור, אשר יועבר לחשבונכם תוך 60 יום ממועד השחרור ובו תוכלו להשתמש לכל מטרה בה תבחרו"

### Step 4: Pikadon Availability and Withdrawal Window

| Event | Window |
|---|---|
| Pikadon usable | From day **14** after end of chova OR national-civic service (hachvana: "החל מהיום ה-14 מסיום שירות החובה או השירות הלאומי-אזרחי"). Kol Zchut still says day 30 for SLE, so an SLE completer should not escalate before day 30 |
| Discharge grant landed | Day 20-60 after end of service, automatic |
| Pre-5y window | Years 0-5, restricted to the 6 purposes in Step 5 |
| Post-5y auto-transfer | To the account on file "בתוך עד 60 ימי עסקים" of the 5-year mark, automatic for service ending after 01.01.2014 (Kol Zchut). A stale account gets an SMS to update it, with cash at a post office (up to 10,000 NIS) or, for a foreign-only account, email pikadon_5@mod.gov.il; no SMS by day 50, call *5266. Pikadon 2000 balances: Step 8.5 |
| Bank account not located | The Fund makes contact, then **120 days** to redeem (s.19(b)(1)) |
| Forfeiture | At **5.5 years** the balance goes to the Additional Assistance Fund (s.19(c)), reclaimable for a further **4.5 years** (s.19(c1)), so the outer deadline is 10 years. A residue of 50 NIS or less goes to the Treasury (s.19(d)) |
| Early release at 3 years | A lochem who served 3 more keva years as lochem or tomech lechima and committed to another may draw the balance at 3 years (s.19(b)(2)), on request within 2.5 years |

**Ask when sherut CHOVA ended, never when they left the army.** Every clock above runs from it: "משרתי קבע נחשבים חיילים משוחררים במשך 5 שנים מתום שירות החובה שלהם". Someone who signed three years of keva is at year six from chova, so the window has closed and the balance has transferred, or is in the forfeiture path if the account was stale.

Nothing in the account on day 1 is normal: the service data reaches the personal area about a week after discharge, the Pikadon is usable from day 14, the grant takes up to 60.

### Step 5: The Six Permitted Pre-5-Year Withdrawal Purposes

**The restricted-purpose Pikadon window is 5 years for EVERYONE** (s.19(a)). The well-known "10 years for active reservists and lone soldiers" rule is s.19(a1)(1), and it attaches to the **s.7(a) and s.7A benefits** (the Additional Assistance Fund for a mechina, a vocational institution and a living allowance; and the Higher-Education Encouragement Fund for study in priority areas), **not to the Pikadon**. It was added by Amendment 19 of 12.07.2017 and re-enacted by Amendment 24 of 2022, so it is not an Iron Swords measure. Never tell a reservist or lone soldier their Pikadon purposes stay open for 10 years.

> Source quote (Chok Klitat Chayalim Meshuchrarim, Section 19(a1)): "חייל מילואים פעיל וחייל משוחרר בודד יהיו רשאים לממש את הזכאויות לפי סעיפים 7(א) ו-7א בתקופת עשר השנים הראשונות שלאחר סיום השירות הסדיר"

Before it closes, the Pikadon may be withdrawn for these and ONLY these (hachvana's wording):

> "לימודים אקדמיים, הכשרה מקצועית, נישואין, הקמת עסק, לימודי נהיגה ורכישת דירה, בית או קרקע לבניית בית"

Four sit in the statute (s.12 bagrut/mechina/psychometric, s.13 academic, s.14 vocational, s.18 business); marriage and driving lessons were added to the Schedule by order under s.18א, which lets the Minister add more. Treat it as the current Schedule, not a permanently closed list. Numbered as quoted:

| # | Purpose (Hebrew) | English |
|---|---|---|
| 1 | לימודים אקדמיים | Academic studies. **s.12 makes this wider than a degree**: bagrut completion, a mechina and psychometric preparation each qualify. But the Fund pays a mechina FIRST, outside the Pikadon (Step 8.4), so the Pikadon is the fallback only for someone it turns down |
| 2 | הכשרה מקצועית | Vocational training. Check the Department's course subsidy first (near-full for combat veterans) |
| 3 | נישואין | Marriage |
| 4 | הקמת עסק | Starting or investing in a business |
| 5 | לימודי נהיגה | Driving lessons |
| 6 | רכישת דירה / בית / קרקע לבניית בית | Purchase of an apartment, house, or land to build on |

**The Fund pays the provider, not the soldier.** For studies, training and a mechina it "תשלם את סכומי ההשתתפות בשכר הלימוד במישרין למוסדות" (s.15(a)); for an apartment it "תעביר את סכום ההשתתפות ישירות למוכר דירת המגורים" (s.17(b)). An approved request settles a bill, it does not put cash in the user's account. Never describe purposes 1, 2 or 6 as money they will receive.

`references/six-purposes-deep-dive.md` has the evidence each purpose needs and the five refusals users argue with: rent (only purchase qualifies), the post-army trip, a degree abroad (Israel only, "כספי הפיקדון ניתנים למימוש רק במדינת ישראל", however recognised the institution), a parent withdrawing for them, and loan collateral.

### Step 6: Tax Credit Points (Nekudot Zikui) for Discharged Soldiers

The most-missed benefit. Awarded under **Pkudat Mas Hachnasa Section 39a** (not Section 11).

State these as thresholds, never as ranges: the source table is inconsistent about which band the boundary month falls in.

| Threshold reached | Points per year | Annual value (2026) | Total over 36 months |
|---|---|---|---|
| Male IDF/MAGAV/Police/SHABAS **≥ 23 months**; female **≥ 22**; SLE and both civilian tracks **≥ 24** | 2 | 5,808 NIS | **17,424 NIS** |
| Otherwise, **≥ 12 months** in any of those populations | 1 | 2,904 NIS | **8,712 NIS** |
| < 12 months | None, EXCEPT an early medical discharge, deemed to have completed 12 months | 1 | 8,712 NIS |

It is prorated across calendar years (so years 1 and 4 are partial) and stacks on the ordinary resident credit points.

**Three populations the month-count alone gets wrong, all set out in `references/nekudot-zikui-tables.md`, which you must read before answering any of them:** a **keva** soldier (the 36 months run from the end of CHOVA and the points are claimable while still serving, so a keva leaver typically has 13 months left, not 36); a **hesder / SHLAT** soldier (the threshold is measured over total service from enlistment, and SHLAT counts toward the Pikadon and grant too, up to the cap); and an **early medical discharge** under 12 months (deemed to have completed 12).

**Mechanics** (full detail in the reference file): 36 months from the month **after** discharge, 242 NIS per point per month in 2026. Salaried: **Tofes 101** to the employer each January with the Teudat Shichrur. Self-employed: the ordinary annual return, not Tofes 135. Missed years: **Tofes 135**, 6 years back from the end of each tax year, plus indexation and 4% interest. Mid-year start or two employers: **Tofes 116**, or the credit is swallowed by over-withholding.

> Source quote (kolzchut): "חיילים 23 חודשים ומעלה 2 ... 36 חודשים לאחר השחרור, החל מהחודש שלאחר חודש השחרור"

Discharged 2 to 6 years ago and never claimed: Tofes 135.

### Step 7: Tax Exemption of Pikadon and Grant

Pikadon withdrawals and the discharge grant are both exempt from income tax under **Pkudat Mas Hachnasa Section 9(27)**, which exempts "כספים שקיבלה הקרן או שקיבל חייל משוחרר לפי חוק קליטת חיילים משוחררים" (not 9(7), which is severance).

> Source quote (kolzchut): "מכספי הפיקדון האישי לא מנוכה מס הכנסה", with the legal basis listed as "פקודת מס הכנסה - סעיף 9(27)"

### Step 8: Mimadim LiLimudim, 100% Tuition

**Mimadim LiLimudim** funds **100% of the CHE university tuition**. **`references/mimadim-scholarship.md` carries the full terms; read it before answering on eligibility or amounts.** The essentials:

| Aspect | Detail |
|---|---|
| Who qualifies | Two tracks. (1) Combat soldiers with a **"shichrur bekavod-zahav"** certificate. (2) "Special populations" with a **"shichrur bekavod"** certificate: tashmash horim, parents who received family payments, lone soldiers, minorities, Arab / Druze / Circassian dischargees, olim. Combat support is not a track on its own but is not excluded either, so verify the cohort. |
| Coverage | First degree or an arts certificate; the eligibility section and the combat-veterans page also list a second degree, so have the user confirm their cohort. 100% of CHE tuition, capped at that ceiling (**12,017 NIS, תשפ"ו**). Annual refund of up to 85% (10,214.45 at the ceiling), the accrued 15% (1,802.5) released in the final year. 3 study years, 4 for engineering, medicine (doctor) or architecture. Tuition only. |
| Window | 5 years from discharge, +1 for bagrut / mechina / psychometric, +2 for a year or more of continuous keva, +3 for both. Statute and website measure it differently, see the reference file. |
| Other scholarships | Charvot Barzel: not in the same academic year, and the ORDER changes the total; its terms are not published by the Department, route to the IDF Assistance Fund, 1111 ext 4. Private scholarships stack freely; government scholarships offset it. |
| Application | Education section of the personal area; confirm the bank details first. The תשפ"ו cycle closes **31.10.26** (extended), read off the Mimadim page and NOT the Iron Swords page, which still shows an expired 2025 date. No תשפ"ז cycle is published yet. |

**The "free university law" users mention is Mimadim itself**: s.7A1 of the Absorption Law (Amendment 24 of 2022, rewritten by Amendment 25 of December 2023), paid by the Department. It is not limited to those discharged after October 2023, and there is no separate Iron Swords tuition law. Third-party scholarships (PEREACH, Adams, Rashi, Rothschild) route to `israeli-academic-scholarships`.

### Step 8.4: The Department's Own Programmes (check before spending the Pikadon)

The Department pays several benefits outside the Pikadon. **`references/department-programs.md` has the terms; read it before answering.** In brief:

- **Mechina and bagrut completion**: the Fund pays first, "הסיוע אינו מוענק על חשבון הפיקדון". Full tuition automatically for gold-honour combat veterans (living allowance means-tested), full tuition plus living allowance for lone soldiers, olim, Ethiopian-Israeli, minority, Haredi and tashmash dischargees, and means-tested help for everyone else within 5 years. Register through the mechina office.
- **Scholarships 45** (periphery residents, first BA year, up to 12,017) **and 46** (periphery residents who are Fund-financed mechina graduates, up to 6,008.5) close registration **31.10.2026**; **44** (periphery institution) needs no registration; the technician scholarship is 90% via the college. 44, 45 and 46 do not stack, and 46 does not stack with Mimadim.
- **Combat veterans, including Swords of Iron**: Tochnit Amit (free therapy, sport and mental-health care via an MoD app), near-full vocational-course funding, Lochamim LeHitech. No war-specific Pikadon or grant top-up for conscripts was found as of 18.10.2026.
- The donor-funded "משפיעים בלימודים" living-cost scholarship's last cycle has closed.

### Step 8.5: Other High-Value Benefits, Mention-and-Route

Delivered by other bodies: surface, then route. **`references/adjacent-benefits.md` holds the conditions that decide each one; read it before answering, because several disqualify the typical 21-year-old outright.**

- **מענק עבודה נדרשת**, 11,461 NIS (2026), 6 full months in a defined sector within 24 months, Tofes 1521, taxable, claim within **42 months**. → `israeli-bituach-leumi`
- **Dmei avtala**, max 70 days if unemployment starts in year 1. → `israeli-unemployment-benefits-navigator`
- **Arnona exemption**, up to 4 months, not automatic, not while living with parents.
- **2-month BL and health exemption**, automatic, only while not working and non-work income at most 688 NIS/month (2026).
- **Free public transport for a year**, lost unless the Rav-Kav profile is loaded **within 60 days**.
- **תוספת משכנתא**, +1% per service month, joint cap 46% / 65%. → `israeli-mortgage-comparator`
- **פיקדון 2000**, dormant balances (service ended after 01.01.1995 or began before 31.12.2000).
- **Free Ministry of Justice legal aid**, and the **"Bahatzda" card**.
- **Service data wrong** (type or length): IDF soldiers go to the IDF "שער לעתיד" directorate, WhatsApp 03-7374789 or atid@digital.idf.il; SLE completers to the National-Civic Service Authority or *5266. The Department cannot reclassify service.
- **Pikadon inheritance**, for a death during service OR after discharge; the heirs apply to the Department.
- **Injury or mental-health condition from compulsory service**: recognition is the MoD Rehabilitation Division (אגף השיקום, shikum.mod.gov.il), not this skill and not `israeli-miluim-manager`; file early and route to `israeli-mental-health-navigator` for support.


### Step 8.6: Right to Return to the Pre-Draft Employer (45-day window)

**Chok Chayalim Meshuchrarim (Hachzara LaAvoda), 5709-1949**: a "permanent employee", or someone with **6 continuous months** there before conscription who did not take severance, may return to the pre-draft employer, which must employ them for **6 months** on the same terms. **The written request must be made between 15 days before discharge and 30 days after**; miss that 45-day window and the right lapses silently. A refusal goes to a **ועדת תעסוקה** (s.21), appealable to the regional labour court within 20 days; Ministry of Justice legal aid helps. Details: `references/adjacent-benefits.md`.

### Step 9: The hachvana.mod.gov.il Personal Area

Everything above runs through the personal area (האזור האישי) at hachvana.mod.gov.il: balance, withdrawals and evidence uploads, the bank account, scholarships, and the Teudat Shichrur. Do not assert a login method. There is no manual fallback for withdrawals, so a user who cannot log in must call the Department on *5266. A changed bank account must be updated there first; approval arrives by SMS within 48 hours.

### Step 10: Required Documents Checklist

Before any application: the **Teudat Shichrur** (from the personal area or the IDF), the **Teudat Zehut**, an **Israeli bank account in the user's own name** for withdrawals (not a parent's; after year 5 a foreign-only account uses the email route in Step 4), the IDF digital wallet ("הארנק הצה"לי") confirmations of gold-honour or lone-soldier status, the purpose-specific evidence from Step 5 for a pre-5y withdrawal, and Tofes 101 plus the Teudat Shichrur for the employer.

## Examples

### Example 1: Just discharged combat, wants Pikadon for driving lessons

"I just finished as a lochem (32 months). Can I use my Pikadon for a driving course?"

1. Eligible: 32 months IDF lochem, at the male cap.
2. Estimate: 4 x 833.40 (training months, at the combat-support rate) plus 28 x 1,000.08. Send him to the official calculator for the live total.
3. Driving lessons are purpose #5, so yes. Evidence: driving-school receipts.
4. Pikadon visible day 14.
5. Apply in the personal area under Pikadon.

### Example 2: 3 years after discharge, wants Pikadon for a rental deposit

"I discharged 3 years ago and still have money in my Pikadon. Can I use it for the deposit on my first rental?"

1. No. Rental is not one of the six purposes; only purchase qualifies.
2. Options: wait for the year-5 auto-transfer, which is unrestricted; or, if enrolled in studies, use purpose #1 for tuition (paid to the institution) and free up other cash; or, if actually buying, purpose #6 with a signed agreement.
3. Two years to the auto-transfer. Tell him to check the bank account on file NOW: a stale one at year 5 starts the 120-day clock and then the 5.5-year forfeiture.

### Example 3: Sherut Leumi-Ezrachi completer, 18 months

"My daughter just finished 18 months of Sherut Leumi-Ezrachi. What is she entitled to?"

1. Eligible: over the 12-month minimum. Pikadon at the SLE rate of 666.72 x 18; official calculator for the live total.
2. hachvana now says the Pikadon is usable from day 14 for SLE too (Kol Zchut still says 30). The grant arrives within 60 days of completion; if it has not landed by then, the bank account on file is the usual cause.
3. Credit points: 18 months is under the SLE 24-month threshold, so 1 point/year for 36 months from the month after completion, if she has taxable income. Tofes 101 to her employer, Tofes 135 for any missed year.
4. Her restricted window runs 5 years from completion. Check the bank account on file today.

### Example 4: Combat veteran discharged 2024, asks about free university

"I'm a lochem who discharged March 2024. I heard the Knesset passed free university?"

1. What he heard about is Mimadim, the s.7A1 fund, not a new Iron Swords law and not tied to his discharge date. It funds 100% of the CHE tuition if his certificate is "shichrur bekavod-zahav". Capped at 12,017 NIS (תשפ"ו), refunded at 85% annually with the 15% released in the final year.
2. Window: 5 years from discharge, so to roughly March 2029, with the extensions in `references/mimadim-scholarship.md`. The current cycle closes 31.10.26.
3. If he also qualifies for the Charvot Barzel scholarship, he cannot realise both in one academic year, and the order changes the total. Have him check first.
4. Do NOT tell him to draw the Pikadon for "what Mimadim doesn't cover": Mimadim already meets the tuition, and a mechina is paid by the Fund for a gold-honour lochem without touching the Pikadon (Step 8.4). Mention Tochnit Amit too.
5. A tomech-lechima asking the same question is not automatically excluded; send him to verify his cohort.

## Recommended MCP Servers

No public MCP server exists for hachvana.mod.gov.il; the personal area has no public API, so withdrawals go through the user's authenticated browser session.

## Reference Links

| Source | URL | What to check |
|---|---|---|
| Department homepage | https://www.hachvana.mod.gov.il/Pages/default.aspx | Contact channels |
| Grant hub | https://www.hachvana.mod.gov.il/GrantAndDeposit/Pages/default.aspx | 6 purposes, 60-day grant timeline |
| Grant amounts | https://www.hachvana.mod.gov.il/GrantAndDeposit/Pages/Grant.aspx | Per-tier grant NIS rates |
| Pikadon pre-5y (with calculator) | https://www.hachvana.mod.gov.il/GrantAndDeposit/DepositUpTo5/Pages/default.aspx | Per-tier monthly rates (re-indexed monthly), 14-day rule |
| Chok Klitat Chayalim Meshuchrarim | https://www.nevo.co.il/law_html/law01/150_023.htm | Sections 7, 7A, 7A1, 19: windows, forfeiture, early release |
| Kol Zchut: Pikadon | https://www.kolzchut.org.il/he/פיקדון_אישי_לחיילים_משוחררים_ומסיימי_שירות_לאומי-אזרחי | 6 purposes, Israel-only rule, SLE wording (older than hachvana) |
| Kol Zchut: Nekudot Zikui | https://www.kolzchut.org.il/he/נקודות_זיכוי_ממס_הכנסה_לחיילים_משוחררים_ומסיימי_שירות_לאומי-אזרחי | Section 39a thresholds, 2026 point value, Tofes 101 / 135 |
| Kol Zchut: return to work | https://www.kolzchut.org.il/he/חזרה_לעבודה_של_חייל_משוחרר | The 45-day request window, 6-month employer duty |
| Kol Zchut: rights index | https://www.kolzchut.org.il/he/זכויות_חיילים_משוחררים_ומסיימי_שירות_לאומי-אזרחי | The full entitlement taxonomy, to spot anything new |
| Mimadim LiLimudim | https://www.hachvana.mod.gov.il/MainEducation/HachvanaScholarship/Pages/UniformToStudies.aspx | Tuition ceiling, 85/15 split, window extensions, cycle deadline |
| Department scholarships | https://www.hachvana.mod.gov.il/MainEducation/HachvanaScholarship/Pages/default.aspx | 44 / 45 / 46 / living-cost terms and deadlines |
| Combat veterans | https://www.hachvana.mod.gov.il/ExtraBenefits/Pages/combat.aspx | Tochnit Amit, mechina, vocational funding |
| Pikadon after 5 years | https://www.hachvana.mod.gov.il/GrantAndDeposit/DepositAfter5/Pages/default.aspx | Auto-transfer timing, stale-account path |
| Kol Zchut: tax refund + Form 135 | https://www.kolzchut.org.il/he/החזר_מס_הכנסה | 6-year window from end of tax year, indexation + 4% interest |

## Gotchas

- **The 10-year window is NOT the Pikadon window.** Section 19(a1) gives active reservists and lone soldiers ten years for the Section 7(a) and 7A study-fund benefits. The Pikadon's restricted-purpose window is five years for everyone, and the balance leaves the Fund at 5.5 years.
- **A stale bank account can forfeit the Pikadon, not just delay it.** At year 5 the balance transfers to the account on file. If the Fund cannot locate it there are 120 days from its contact; at 5.5 years it goes to the Additional Assistance Fund with 4.5 years to reclaim.
- **Two citations agents get wrong.** Credit points are **Section 39a**, not Section 11. The Pikadon and grant exemption is **Section 9(27)**, not 9(7).
- **Pikadon rates are re-indexed**, so any figure here (1,000.08 combat, August 2026) is an order-of-magnitude anchor. Send the user to the official calculator.
- **SHLAT counts.** A hesder or SHLAT soldier accrues Pikadon and grant on total service up to the 32/24 cap (s.11(a)) and is thresholded on total service for credit points. Counting paid months alone can halve all three.
- **The Fund pays a mechina before the Pikadon does.** Never send a lochem, lone soldier or oleh to spend the Pikadon on a mechina the Fund would fund.
- **Forward credit cannot exceed monthly tax liability; the retroactive path can pay cash.** Tofes 101 reduces tax owed to zero and no further, so "I lost X shekels" is wrong for the forward case. Tofes 135 refunds real over-withholding plus indexation and 4% interest, 6 years back from the END of each tax year, one request per year.
- **Mimadim is not lochem-only, and its deadlines are not on the Iron Swords page.** The special-populations track runs off a "shichrur bekavod" certificate. The Iron Swords page still shows an expired 2025 date; the live תשפ"ו cycle closes 31.10.26, as do scholarships 45 and 46.
- **Pikadon is non-transferable, non-pledgeable, non-seizable**, and the Department warns that a withdrawal needs no paid intermediary: never hand anyone the personal-area password.

## Bundled Resources

### Scripts

- `scripts/pikadon-calculator.py`, estimates the Pikadon and grant from service type and months served at the August 2026 rates, with the training reclassification applied. It returns zero under 12 months unless `--medical-discharge` (pro-rata, deemed 12 for credit points) or `--injury-discharge` (deemed full service, s.10A(b)) is passed. `--total-service-months` adds SHLAT to the Pikadon, grant and credit-point counts, capped at 32/24. Run: `python scripts/pikadon-calculator.py --service-type lochem --months 32 --gender male`

### References

- `references/adjacent-benefits.md`, the conditions behind every Step 8.5 row (required-work grant, avtala, arnona, BL exemption, Rav-Kav, mortgage supplement, Pikadon 2000, legal aid).
- `references/mimadim-scholarship.md`, full Mimadim terms: eligibility tracks, the 85/15 mechanics and ceiling, window extensions, the Charvot Barzel interaction.
- `references/department-programs.md`, the Department's mechina funding, scholarships 44 / 45 / 46, technician and living-cost scholarships, and combat-veteran programmes, with stacking rules and deadlines.
- `references/six-purposes-deep-dive.md`, evidence required per permitted withdrawal purpose.
- `references/nekudot-zikui-tables.md`, credit-point thresholds and the Tofes 101 / 135 flow.
- `references/domain-checklist.md`, coverage list used by future update runs.

## Troubleshooting

### Error: "Pikadon not visible in the personal area 20 days after discharge"
Cause: the Department itself says data appears about a week after discharge, later when the IDF or the SLE authority reports late; a wrong-identity login is the other likely cause (not confirmed). An SLE completer is best given until day 30 (Kol Zchut's figure), and a keva leaver may be years past the window rather than days early.
Solution: confirm they logged in with their own Teudat Zehut, and confirm when CHOVA ended. Then call *5266; if the service data itself is wrong, write to "שער לעתיד". There is no manual workaround.

### Error: "Withdrawal request for apartment rental rejected"
Cause: rental is not one of the 6 permitted purposes, so the rejection is automatic and correct.
Solution: wait for the year-5 auto-transfer, which is unrestricted, or re-submit under purpose #6 only if they are genuinely purchasing (signed agreement, not a lease).

### Error: "Nekudot zikui not on the payslip even though Tofes 101 was submitted"
Cause: usually a one-month payroll lag or a missing Teudat Shichrur attachment.
Solution: check the next payslip; if still missing after two cycles, have payroll re-process Tofes 101 with the certificate and file Tofes 135 for the months already lost. The 36-month window does not pause.

### Error: "Discharge grant did not arrive after 60 days"
Cause: almost always the bank account on file, closed, frozen, or in the wrong name after the user left their service-era account.
Solution: update the bank account in the personal area (SMS approval within 48 hours). The same stale account is what triggers the Pikadon forfeiture clock at year 5, so fix it once and it fixes both.

### Error: "Mimadim scholarship rejected"
Cause: usually the certificate type. The gold-honour track is combat-only, and the special-populations basket attaches to a "shichrur bekavod" certificate.
Solution: check the cohort terms for that academic year. If the rejection turns on service classification, that is an IDF question, not a Department one: write to "שער לעתיד" (WhatsApp 03-7374789, atid@digital.idf.il), which the Mimadim page also gives for a scholarship missing from the personal area. If outside the basket entirely, route to `israeli-academic-scholarships` for alternative scholarships (PEREACH, Rashi, etc.).
