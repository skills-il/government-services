---
name: israeli-discharged-soldier-navigator
description: >-
  Navigate post-discharge benefits for IDF, MAGAV, Police, SHABAS, and SLE members via the MoD Department for Discharged Soldiers (hachvana.mod.gov.il). Computes Pikadon by service tier (lochem, tomech lechima, acher), explains the 14-day deposit vs 60-day manak shichrur timelines, validates withdrawals against the 6 statutory pre-5y purposes (academic studies, vocational training, driving lessons, business, marriage, apartment purchase, rental NOT included), walks Section 39a nekudot zikui via Tofes 101 and Tofes 135 retroactive refund, and covers Iron Swords benefits for combat veterans discharged October 2023+. Use when a hayal meshuchrar, parent, or SLE completer asks about pikadon, manak shichrur, post-army benefits, nekudot zikui chayal meshuchrar, or free university for combat veterans. Do NOT use for miluim (israeli-miluim-manager), lone soldiers (israeli-lone-soldier-rights), scholarships beyond Mimadim (israeli-academic-scholarships), or mortgages (israeli-mortgage-comparator).
license: MIT
---

# Israeli Discharged Soldier Navigator

## Problem

A 21-year-old who just finished sherut chova has access to a Pikadon (personal deposit), a separate discharge grant, three years of tax credit points, and (for Iron Swords combat veterans) full university tuition. The official information is scattered across the MoD's hachvana site, kolzchut, the Income Tax Ordinance, and the Knesset full-tuition law from December 2023. Most discharged soldiers either miss benefits entirely (especially the retroactive nekudot zikui), try to use Pikadon for non-permitted purposes (rental is the most common mistake, only purchase qualifies), or fail to claim within the 5-year statutory window. This skill walks the user through eligibility, the current indexed Pikadon rates per service tier, the 6 permitted pre-5y withdrawal purposes, the Tofes 101 claim flow for credit points, and the Iron Swords expansions, with the right form numbers and the right hachvana.mod.gov.il portal flows.

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
| Any of the above, < 12 months | Eligible if discharged for health reasons OR injury during training/operational activity. Pikadon is **pro-rata** (months served × tier rate), not a full credit, the 12-month minimum is waived, not the per-month accrual rule. | Pro-rata | Pro-rata |
| Any of the above, < 12 months, voluntary exit | None | None |

> Source quote (kolzchut): "מי שהשתחררו משירות חובה בצה\"ל, במג\"ב, במשטרת ישראל, בשב\"ס, או סיימו שירות לאומי-אזרחי ששירתו לפחות 12 חודשים"

### Step 2: Compute the Pikadon Amount (2026 indexed rates)

The Pikadon accrues each month of paid service at a rate set by service type. Current 2026 indexed monthly rates from hachvana.mod.gov.il/GrantAndDeposit/DepositUpTo5:

| Service type (Hebrew) | English | NIS / month (May 2026) |
|---|---|---|
| לוחמים | Combat | 990.63 |
| תומכי לחימה | Combat support | 825.52 |
| עורפי | Rear / other | 660.42 |
| שירות לאומי-אזרחי | National-civic service (SLE) | 660.42 |
| מסלול אזרחי ביניים | Intermediate civilian track | 495.38 |
| מסלול אזרחי מפוצל | Split civilian track | 330.25 |

**Training months are reclassified, and this is the single most common over-estimate.** The MoD says so explicitly: the first **4 months** of a combat soldier's training are credited as **combat support**, and the first **2 months** of a combat-support soldier's training are credited as **other**. A combat soldier with 32 countable months therefore accrues 4 x 825.52 + 28 x 990.63, not 32 x 990.63.

**Important caps and indexing rules:**

| Rule | Detail |
|---|---|
| Male soldier accrual cap | 32 months of paid service |
| Female soldier accrual cap | 24 months of paid service |
| Beyond cap | No further Pikadon credit (unpaid extension does not accrue) |
| Index | Balance updated at start of each month per CPI (madad) |
| Type | Personal, cannot be transferred, pledged, or seized |

> Source quote (Chok Klitat Chayalim Meshuchrarim, Chapter ג): "הפקדון הוא אישי ואינו ניתן להעברה, לשעבוד או לעיקול בכל דרך שהיא"

**Always direct the user to the official calculator for the personalized total**, rates change monthly with the CPI: https://www.hachvana.mod.gov.il/GrantAndDeposit/DepositUpTo5/Pages/default.aspx (Pikadon calculator linked from the page).

Provide an order-of-magnitude estimate only when the user supplies (a) service type and (b) months served (capped at 32/24). The rates above are the MoD's May 2026 figures and are re-indexed; re-read hachvana before quoting them for a later period.

### Step 3: The Discharge Grant (Manak Shichrur)

The discharge grant is **separate** from the Pikadon. Key facts:

| Question | Answer |
|---|---|
| When paid? | 20 to 60 days from end of service |
| To where? | The same bank account that received salary during service |
| Restrictions on use? | None, "any purpose you choose" (לכל מטרה בה תבחרו) |
| Tax? | Exempt (same statute as Pikadon) |
| Per-tier amounts (May 2026, per month of service) | Combat 684.99, combat support 570.42, other (including SLE) 455.84, intermediate civilian track 342.50, split civilian track 227.92. The SAME training reclassification applies: a combat soldier's first 4 training months are paid at the combat-support rate. |
| Eligibility | 12 months of service, or less if discharged on health grounds. Lone soldiers get an advance on the grant within 14 days. |

> Source quote (hachvana GrantAndDeposit): "מענק שחרור, אשר יועבר לחשבונכם תוך 60 יום ממועד השחרור ובו תוכלו להשתמש לכל מטרה בה תבחרו"

### Step 4: Pikadon Availability and Withdrawal Window

Two distinct timelines users routinely confuse:

| Event | Window | Notes |
|---|---|---|
| Pikadon visible in personal area | Day 14 after IDF / MAGAV / Police / SHABAS discharge | "כספי הפיקדון יעמדו לרשות המשתחררים החל מהיום ה-14" |
| Pikadon visible (SLE) | Day 30 after SLE completion | Cross-check on hachvana.mod.gov.il |
| Discharge grant landed | Day 20-60 after end of service | Automatic, no application needed |
| Pre-5y window | Years 0-5, restricted to 6 statutory purposes only | See Step 5 |
| Post-5y auto-transfer | Year 5+, balance auto-transfers to bank for any use | SMS notification, ~7 business days actual credit |

If the user expected money on day 1 and there's nothing in their account: this is normal, Pikadon needs 14 days, grant needs up to 60.

### Step 5: The Six Permitted Pre-5-Year Withdrawal Purposes

Before the 5-year window closes, Pikadon can be withdrawn for these and ONLY these purposes (exact statutory wording from hachvana):

> "לימודים אקדמיים, הכשרה מקצועית, נישואין, הקמת עסק, לימודי נהיגה ורכישת דירה, בית או קרקע לבניית בית"

Numbered in the statute order quoted above:

| # | Purpose (Hebrew) | English | Typical evidence required |
|---|---|---|---|
| 1 | לימודים אקדמיים | Academic studies | Acceptance letter, tuition receipt, recognized institution **in Israel** (see the abroad rule below) |
| 2 | הכשרה מקצועית | Professional / vocational training | Course registration + payment receipt from recognized provider |
| 3 | נישואין | Marriage | Teudat Nisuin OR wedding hall contract / vendor receipts (works pre- or post-wedding within the 5y window) |
| 4 | הקמת עסק | Starting / investing in a business | Osek Patur or Osek Murshe registration + business setup expenses (equipment, lease, registration fees) |
| 5 | לימודי נהיגה | Driving lessons | Payment receipts from licensed instructor / driving school |
| 6 | רכישת דירה / בית / קרקע לבניית בית | Purchase of apartment / house / land for building | Signed purchase agreement, NOT a rental contract |

**Critical clarifications (the most common user mistakes):**

| Mistake | Reality |
|---|---|
| "I can use Pikadon to pay rent on my first apartment" | **No.** Only purchase qualifies. Rental is not a permitted purpose. Tell the user to wait for the 5-year auto-transfer if they need cash for rent, or use the discharge grant (which has no restrictions). |
| "I'll use it for my trip after the army (Big Trip)" | **No.** Travel is not a permitted purpose. The discharge grant can cover this, Pikadon cannot pre-5y. |
| "It's for my degree, but I'm studying abroad" | **No.** The Pikadon can only be realised inside Israel: "כספי הפיקדון ניתנים למימוש רק במדינת ישראל" (kolzchut, "פיקדון אישי לחיילים משוחררים ומסיימי שירות לאומי-אזרחי"). A degree abroad does not qualify, however recognized the institution is. Someone studying abroad must wait for the 5-year auto-transfer, or use the discharge grant, which has no restrictions. |
| "Can my parents withdraw it for me?" | **No.** The Pikadon is personal and non-transferable. The user must apply via their own MY VISIT account. |
| "I want to use it as collateral for a loan" | **No.** Statutorily non-pledgeable (לא ניתן לשעבוד). |

### Step 6: Tax Credit Points (Nekudot Zikui) for Discharged Soldiers

This is the single most-missed benefit. Awarded under **Pkudat Mas Hachnasa Section 39a** (סעיף 39א, note: NOT Section 11) + Chok Klitat Chayalim Meshuchrarim.

| Service population + length | Points per year | Annual benefit value (2026) | Total over 36 months |
|---|---|---|---|
| Male IDF/MAGAV/Police/SHABAS ≥ 23 months | 2 | ~5,808 NIS | **17,424 NIS** |
| Male, 12-22 months | 1 | ~2,904 NIS | **8,712 NIS** |
| Female IDF/MAGAV/Police/SHABAS ≥ 22 months | 2 | ~5,808 NIS | **17,424 NIS** |
| Female, 12-21 months | 1 | ~2,904 NIS | **8,712 NIS** |
| SLE (any gender) ≥ 24 months | 2 | ~5,808 NIS | **17,424 NIS** |
| SLE (any gender) 12-23 months | 1 | ~2,904 NIS | **8,712 NIS** |
| < 12 months | None (unless medical) |, |, |

**Mechanics:**

| Rule | Detail |
|---|---|
| Duration | 36 months, starting the month **after** the month of discharge (not the discharge month itself) |
| Per-point monthly value (2026) | 242 NIS, so 2 points = 484 NIS/month off income tax |
| Eligibility | Discharged from IDF / MAGAV / Police / SHABAS OR SLE completers. The credit reduces tax owed going forward and cannot exceed monthly liability. |
| How to claim (salaried) | Submit **Tofes 101** to employer at start of each calendar year, attach Teudat Shichrur. Credit appears on payslip under "נקודות זיכוי". |
| How to claim (self-employed) | Include credit-point claim in the personal-deductions section of the annual return (Tofes 1301) with discharge certificate attached. For prior years where the credit was missed, file an amended return (דוח מתקן), NOT Tofes 135. |
| Retroactive (salaried only) | If a salaried employer didn't apply the credit in past years: file **Tofes 135** via the Tax Authority online portal, refunds up to 6 years back. Yields cash from over-withholding plus indexation and 4% interest. |
| Multi-employer tip | If working at two employers, also file **Tofes 116 (תיאום מס)** so the second employer doesn't withhold at the full marginal rate, otherwise the credit gets "swallowed" by over-withholding. |

> Source quote (kolzchut nekudot zikui): "חיילים 23 חודשים ומעלה: 2 | חיילים בין 12 ל-23 חודשים: 1 | 36 חודשים לאחר השחרור, החל מהחודש שלאחר חודש השחרור"

If the user discharged 2-6 years ago and has been working but never claimed: route them to Tofes 135 for retroactive refund. This is real money that gets left on the table.

### Step 7: Tax Exemption of Pikadon and Grant

Both the Pikadon withdrawals AND the discharge grant are exempt from income tax under **Pkudat Mas Hachnasa Section 9(27)** (סעיף 9(27), note: NOT Section 9(7), which covers severance pay).

> Source quote (kolzchut): "מכספי הפיקדון האישי לא מנוכה מס הכנסה (פקודת מס הכנסה, סעיף 9(27))"

This means a user withdrawing the full Pikadon balance for academic studies receives the full amount, no tax. Reassure users panicking that "such a big lump sum will hit me with mas hachnasa", it does not.

### Step 8: Iron Swords (חרבות ברזל) Expanded Benefits, Mimadim 100%

**Tikkun 25 to Chok Klitat Chayalim Meshuchrarim**, approved by the Knesset on 8 Tevet 5784 (December 20, 2023), raised the Mimadim LiLimudim ("Uniform to Studies") scholarship coverage to **100% of annual undergraduate tuition** and extended the eligibility window from 3 to 5 years after discharge. Key facts:

| Aspect | Detail |
|---|---|
| Who qualifies | Lochem (combat) classification on Teudat Shichrur AND "special populations", lone soldiers, new immigrants, conscripts with children, recognized minorities. Combat-support (tomech lechima) may also qualify depending on the special-populations definition for each cohort. Verify on hachvana for the current cycle. |
| Coverage | 100% of annual undergraduate tuition (BA or MA scope per Mimadim rules). Tuition only, does NOT cover dorms, living costs, or non-academic expenses. |
| Window | Usable up to 5 years after end of service (raised from 3 years by Tikkun 25). |
| Application | Via the Education section of the personal area at hachvana.mod.gov.il (look for "ממדים ללימודים" / "Mimadim LiLimudim"). |
| Statute citation | Tikkun 25 to Chok Klitat Chayalim Meshuchrarim, approved 20 Dec 2023. Bill sponsors: MKs Katz, Dallal, Nir, Biton. |

**What this skill does NOT do:** Match the user to a specific university scholarship beyond Mimadim. For PEREACH / Adams / Rashi / Rothschild / Mimadim deep-dive, route to `israeli-academic-scholarships`.

### Step 8.5: Other High-Value Benefits, Mention-and-Route

These adjacent benefits are operationally distinct from the Pikadon + grant + Mimadim core of this skill. Mention them to the user and route to the appropriate skill or surface a link:

| Benefit | Who delivers it | Where to route |
|---|---|---|
| מענק עבודה מועדפת / נדרשת, cash grant for discharged soldiers who work 6 months full-time in defined sectors (construction, agriculture, manufacturing, hotels, gas stations, disability care) within 24 months of discharge. Single largest non-Pikadon cash benefit. | Bituach Leumi (file Tofes 1521) | `israeli-bituach-leumi` |
| Discharged-soldier unemployment (dmei avtala), up to 70 days year-1 | Bituach Leumi | `israeli-unemployment-benefits-navigator` |
| Arnona discount for discharged soldiers (typically 4 months, per municipal regulation) | Local authority | Check with arnona office |
| 2-month Bituach Leumi + health-insurance exemption post-discharge | Bituach Leumi automatic | `israeli-bituach-leumi` |
| Free public transport (1 year post-discharge) | Egged / Israel Rail | Apply on relevant transit operator portal |
| "Bahatzda" benefits card (discounts at retailers) | Independent | hachvana.mod.gov.il |
| Service-type appeal (combat vs combat-support classification) | IDF Mador Iturim | Apply via personal area or directly to Mador Iturim |
| Pikadon inheritance on death in service | MoD Mador Mishpachot Shakulot | Refer to bereavement department |

### Step 9: The hachvana.mod.gov.il Personal Area

Every flow above happens through the personal area at hachvana.mod.gov.il. The user logs in via the government Identifier (מזהה ממשלתי) or the MoD mobile app push (smart-card login is deprecated). Then they can:

| Action | Path |
|---|---|
| View Pikadon balance | Personal area > Pikadon |
| Submit a withdrawal request | Personal area > Pikadon > Submit withdrawal (select purpose + upload evidence) |
| Update bank account on file | Personal area > Settings |
| Schedule a career counselor | Personal area > Hachvana > Schedule via MY VISIT (Zoom or phone) |
| Apply for Mimadim scholarship | Personal area > Education > Mimadim |
| Download Teudat Shichrur | Personal area > Documents |

If the user can't log in: there is no manual fallback for withdrawals, they must call the department directly via the contact channels on hachvana.mod.gov.il.

### Step 10: Required Documents Checklist

Before any benefit application, the user needs:

1. **Teudat Shichrur** (discharge certificate), downloadable from MY VISIT personal area or via IDF
2. **Teudat Zehut** (Israeli ID), needed for login + every form
3. **Israeli bank account in user's name**, Pikadon will NOT pay out to a foreign account or a parent's account
4. **Purpose-specific evidence** (for pre-5y Pikadon withdrawal):
   - Studies: acceptance letter + tuition invoice
   - Vocational training: registration + receipt
   - Driving: school receipts
   - Business: Osek registration + setup expenses
   - Marriage: Teudat Nisuin OR vendor receipts
   - Apartment: signed purchase agreement
5. **Form 101 + Teudat Shichrur** for nekudot zikui (give to employer)

## Examples

### Example 1: Just discharged combat, wants Pikadon for driving lessons

User says: "I just finished my service as a lochem (32 months). Can I use my Pikadon for a driving course?"

Actions:
1. Confirm eligibility: 32 months IDF lochem → full Pikadon, capped at 32 months.
2. Estimate the amount: 4 x 825.52 (the training months, credited as combat support) plus 28 x 990.63 (combat rate, May 2026). Direct the user to the official calculator for the personalized current total.
3. Confirm purpose: driving lessons (לימודי נהיגה) is purpose #3 of the 6 permitted pre-5y purposes, YES, eligible.
4. Note timeline: Pikadon visible day 14 after discharge.
5. Documents needed: driving school payment receipts.
6. Send to: hachvana.mod.gov.il personal area > Pikadon > Submit withdrawal.

### Example 2: 3 years after discharge, wants Pikadon for rental deposit

User says: "I discharged 3 years ago, I still have money in my Pikadon, can I use it for the deposit on my first rental apartment?"

Actions:
1. Stop. Rental is **not** one of the 6 permitted pre-5y purposes. Only purchase qualifies.
2. Options to present:
   - **Option A:** Wait until year 5, at the 5-year mark, the balance auto-transfers to your bank account for any use including rent.
   - **Option B:** If user is enrolled in studies, withdraw under purpose #1 (academic studies) for tuition expenses, freeing other cash for rent.
   - **Option C:** If user is buying (not renting), purpose #6 applies, bring the signed purchase agreement.
3. Confirm timeline: 3y post-discharge means 2 more years to the auto-transfer. Suggest setting a reminder.

### Example 3: Sherut Leumi-Ezrachi completer, wants to know what she's entitled to

User says: "My daughter finished Sherut Leumi-Ezrachi 18 months ago, what is she entitled to?"

Actions:
1. Confirm eligibility: SLE 18 months ≥ 12 → eligible for Pikadon and grant.
2. Compute the Pikadon: the SLE rate is 660.42 NIS/month x 18 months. Direct the user to the official calculator for the personalized current total.
3. Discharge grant: should have already landed within 60 days of completion, verify with her bank statements; if missing, contact hachvana.
4. 6 permitted purposes apply equally.
5. Nekudot zikui: 18 months falls in the 12-22 range → 1 point/year for 36 months from month after SLE completion if she has taxable income. Submit Tofes 101 to her employer.
6. If she discharged 18 months ago and never claimed credit points: file Tofes 135 retroactive for missed months.

### Example 4: Combat veteran discharged 2024, asks about free university

User says: "I'm a lochem who discharged March 2024, I heard the Knesset passed free university?"

Actions:
1. Confirm eligibility: discharged March 2024 as lochem → eligible for Mimadim 100% tuition (raised by Tikkun 25, December 20, 2023).
2. Coverage: 100% of annual undergraduate tuition. Tuition only, does not cover dorms, living, or expenses beyond Mimadim scope.
3. Window: 5 years from end of service (extended from 3 by Tikkun 25). For a March 2024 discharge, the window runs to ~March 2029.
4. Apply via the Education section of the hachvana.mod.gov.il personal area (look for "ממדים ללימודים").
5. Suggest pairing with Pikadon: use Pikadon under purpose #1 (academic studies) for additional study-related expenses Mimadim doesn't cover.
6. Note tomech-lechima soldiers: do NOT assume exclusion, the special-populations basket may apply. Verify on hachvana for the specific cohort.
7. For scholarship matching beyond Mimadim, route to `israeli-academic-scholarships`.

### Example 5: Discharged 4 years ago, never claimed credit points

User says: "I've been working for 4 years post-discharge, but I just realized my payslip never showed nekudot zikui for chayal meshuchrar. Did I lose them?"

Actions:
1. Reassure: retroactive refunds available via **Tofes 135** for up to 6 years back.
2. Verify service length: ≥23 months male / ≥22 months female → 2 points/year for 36 months from month after discharge.
3. Compute lost benefit: total benefit value is 17,424 NIS (2 points) or 8,712 NIS (1 point) over the 36 months, realized only against actual tax liability.
4. Tell user to file Tofes 135 via Tax Authority online portal at gov.il (search "החזר מס" or "טופס 135").
5. Documents needed: Teudat Shichrur, annual salary summary for each affected year, bank account for refund.
6. After filing for retroactive: also submit Tofes 101 to current employer to start applying points going forward (if still within 36-month window from discharge, verify).

## Recommended MCP Servers

No public MCP server exists for hachvana.mod.gov.il (the MoD personal area has no public API). Withdrawal applications must go through the user's authenticated personal area in a browser.

## Reference Links

| Source | URL | What to check |
|---|---|---|
| Department for Discharged Soldiers homepage | https://www.hachvana.mod.gov.il/Pages/default.aspx | Service map, contact channels |
| Grant + Pikadon hub | https://www.hachvana.mod.gov.il/GrantAndDeposit/Pages/default.aspx | 6 purposes list, 60-day grant timeline |
| Pikadon pre-5y page (with calculator) | https://www.hachvana.mod.gov.il/GrantAndDeposit/DepositUpTo5/Pages/default.aspx | Current per-tier monthly NIS rates (change monthly), 14-day rule |
| Iron Swords benefits hub | https://www.hachvana.mod.gov.il/IronSwords/Pages/sword.aspx | Active Iron Swords expansions, Mimadim deadline |
| Chok Klitat Chayalim Meshuchrarim (full text) | https://www.nevo.co.il/law_html/law01/150_023.htm | Statutory base for Pikadon, grant, scholarship, tax credit |
| Kol Zchut: Pikadon | https://www.kolzchut.org.il/he/פיקדון_אישי_לחיילים_משוחררים_ומסיימי_שירות_לאומי-אזרחי | 6-purpose canonical list, SLE rules, medical-discharge exception |
| Kol Zchut: Nekudot Zikui | https://www.kolzchut.org.il/he/נקודות_זיכוי_ממס_הכנסה_לחיילים_משוחררים_ומסיימי_שירות_לאומי-אזרחי | Section 39a, service-length point table, Tofes 101 + Tofes 135 process |
| Wikipedia: Chok Mimadim LiLimudim | https://he.wikipedia.org/wiki/חוק_ממדים_ללימודים | Tikkun 25 (Dec 20 2023) raising Mimadim to 100% and extending the window to 5 years |
| Kol Zchut: tax refund + Form 135 | https://www.kolzchut.org.il/he/החזר_מס_הכנסה | Tofes 135 retroactive refund process for salaried employees, 6-year window, 4% interest |

## Gotchas

- **Section 39a, NOT Section 11.** Agents trained on older Israeli tax content often cite "Section 11 Pkudat Mas Hachnasa" for discharged-soldier credit points. The correct citation is **Section 39a (סעיף 39א)**. Section 11 covers basic resident points, not the post-discharge bonus.
- **Section 9(27), NOT Section 9(7).** The Pikadon tax exemption is **Section 9(27)** of the Income Tax Ordinance. Section 9(7) covers severance pay exemption, different statute, different ceiling. Don't conflate them.
- **Rental is NOT a permitted purpose.** The most common user mistake is assuming Pikadon can cover their first rental apartment deposit. Only **purchase** of an apartment / house / land qualifies. If the user wants cash for rent: route to the discharge grant (unrestricted) or wait for the 5-year auto-transfer.
- **Pikadon rates index monthly with CPI.** Any specific NIS/month figure cited (e.g. 990.63 for combat, May 2026) is the rate at the time of writing, it changes monthly. ALWAYS direct the user to the official calculator at hachvana.mod.gov.il/GrantAndDeposit/DepositUpTo5 for the personalized current total, rather than asserting a precise lump sum.
- **The 32/24 month cap is on PAID service.** A male soldier who served 36 months (some unpaid extension) still only accrues Pikadon for 32 months at the relevant tier. Female cap is 24 months. Iron Swords reservist extension beyond mandatory service does NOT add to this Pikadon, that goes under miluim, a separate skill.
- **Credit points start the month AFTER discharge.** A soldier who discharged on March 15 starts the 36-month nekudot-zikui clock from April 1, not March. The March payslip does not yet get the points.
- **Nekudot zikui forward-claim cannot exceed monthly tax liability** (via Tofes 101). If a discharged soldier in their first job has low taxable income (e.g., part-time student job), the credit reduces tax owed to zero but does not pay out negative tax going forward. The retroactive **Tofes 135** path is different: if a prior employer over-withheld in past years because they didn't apply the credit, Tofes 135 yields a cash refund of the over-withholding, plus indexation and 4% interest. So "I lost X shekels" framing is accurate for the retroactive case but not for the forward case.
- **The discharge grant lands automatically, no application needed.** If a user 60+ days post-discharge has no grant in their account, the cause is usually wrong/stale bank account on file. Direct them to update via the personal area.
- **Mimadim 100% is NOT lochem-only.** The hachvana program page explicitly covers "lochem soldiers AND special populations", special populations include lone soldiers, new immigrants, conscripts with children, and recognized minorities. Combat-support (tomech lechima) may qualify depending on the cohort's definition of the special-populations basket. Do not tell a tomech-lechima soldier they're ineligible, direct them to verify on hachvana for their specific cohort.
- **Pikadon is non-transferable, non-pledgeable, non-seizable.** A parent or sibling cannot withdraw on the user's behalf. A bank cannot use it as collateral. A court cannot seize it for debt (statutory protection per Chok Klitat Chayalim Meshuchrarim).

## Bundled Resources

### Scripts

- `scripts/pikadon-calculator.py`, Estimate the Pikadon and discharge grant amounts based on service type and months served. Indexed to 2026 Feb rates; outputs a disclaimer to verify on the official calculator. Run: `python scripts/pikadon-calculator.py --service-type lochem --months 32 --gender male`

### References

- `references/domain-checklist.md`, Canonical coverage list (Must / Should / Out-of-scope / Sources). Used by future update-skill runs to detect gaps.
- `references/six-purposes-deep-dive.md`, Detailed guidance per the 6 permitted pre-5y withdrawal purposes with required evidence.
- `references/nekudot-zikui-tables.md`, Service-length lookup table for credit points (male / female / SLE), with the Tofes 101 + Tofes 135 claim flow.

## Troubleshooting

### Error: "Pikadon not visible in personal area 20 days after discharge"
Cause: Either the discharge date hasn't been synced from IDF systems, or the personal area login is using the wrong identity (e.g., parent's account).
Solution: Verify the user logged in with their own Teudat Zehut. If still missing, contact the Department for Discharged Soldiers via the channels on hachvana.mod.gov.il, there is no manual workaround.

### Error: "Withdrawal request for apartment rental rejected"
Cause: Rental is not one of the 6 permitted pre-5y purposes. The system rejects automatically.
Solution: Either wait for the 5-year auto-transfer (use of remaining balance is unrestricted), or re-submit under purpose #6 ONLY if the user is actually purchasing (signed purchase agreement, not lease).

### Error: "Employer says nekudot zikui aren't showing on payslip even though Tofes 101 was submitted"
Cause: Payroll system delay (1 month) or missing Teudat Shichrur attachment.
Solution: Re-check the next payslip. If still missing after 2 cycles: file Tofes 135 retroactively, and have payroll re-process Tofes 101 with Teudat Shichrur attached. Don't wait, the 36-month window doesn't pause.

### Error: "Discharge grant didn't arrive after 60 days"
Cause: Bank account on file is closed, frozen, or in the wrong name (e.g., user closed their service-era account and never updated hachvana).
Solution: Log in to personal area > Settings > update bank account. The grant will be re-issued; contact the department if no follow-up SMS within 14 days.

### Error: "Mimadim scholarship rejected"
Cause: Cohort-specific eligibility rules, the "special populations" basket (lone soldiers, olim, conscripts with children, minorities) varies by academic year. A tomech-lechima soldier outside the current basket may be excluded.
Solution: Verify the current cohort eligibility on hachvana.mod.gov.il for the specific academic year. If the rejection is based on classification, appeal via Mador Iturim. If outside the basket entirely, route to `israeli-academic-scholarships` for alternative scholarships (PEREACH, Rashi, etc.).
