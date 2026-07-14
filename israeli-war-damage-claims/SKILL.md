---
name: israeli-war-damage-claims
description: "Guide users through filing DIRECT property damage claims from rocket attacks and hostilities in Israel (Iron Swords and Shaagat HaAri 2026): documenting damage, filing with the Tax Authority Compensation Fund, home contents insurance, assessor visits, appeals. Use when user asks about physical property damage from war, rockets, missiles, 'nezek yashir', 'mas rechush', 'keren pitzuim', war damage claim, damaged apartment, broken windows from blast, or compensation for hostility damage. Covers fast track (up to NIS 30,000), regular track, optional contents insurance, and appeals (va'adot erar). Do NOT use for indirect/economic business damage like turnover decline or wage grants (use israeli-business-war-compensation), employee unpaid-leave dmei avtala (use israeli-unemployment-benefits-navigator), personal injury (israeli-bituach-leumi), ordinary road-accident car damage (private insurance), or general home insurance (israeli-insurance-comparator)."
license: MIT
---

# Israeli War Damage Claims

## Problem

Thousands of Israelis face property damage from rocket and missile attacks. Filing compensation claims through the Tax Authority's Compensation Fund is bureaucratic and complex, with different tracks, critical deadlines, and compensation ceilings that vary by household composition. A single documentation mistake or missed deadline can result in complete forfeiture of compensation rights.

The direct-damage process here is the same across recent conflicts, Iron Swords (October 2023 onward), Operation Am K'Lavi / Rising Lion (the 12-day Iran war of June 2025, which caused widespread ballistic-missile damage to homes and prompted the Tax Authority's fast track), and Shaagat HaAri (2026).

## Instructions

### Step 1: Identify the Damage Type and Correct Track

First, determine what kind of damage the user has and which compensation track applies.

| Damage Type | Hebrew Term | Who Compensates | Track |
|---|---|---|---|
| Structural damage (walls, roof, windows, doors) | נזק למבנה | Tax Authority Compensation Fund (קרן הפיצויים) | Regular or Fast |
| Home contents (furniture, electronics, appliances) | נזק לתכולה | Tax Authority Compensation Fund (capped by household size) | Regular or Fast |
| Contents above ceiling | תכולה מעל התקרה | Optional war damage insurance (ביטוח מלחמה רשות המסים) | Insurance claim |
| Business property/equipment | נזק לעסק | Tax Authority Compensation Fund | Regular or Fast |
| Vehicle damage from war/missile | נזק לרכב | Tax Authority Compensation Fund (קרן הפיצויים), NOT car insurance (comprehensive policies exclude war) | Regular track (a Compensation Fund appraiser must approve the repair before you fix it at any garage) |
| Economic loss (lost revenue, wages) | נזק עקיף | Tax Authority (separate indirect damage track) | **Use `israeli-business-war-compensation`**, covers both Iron Swords and the Shaagat HaAri (March-April 2026) eligible-expenses track, with the wage participation grant, business continuity grant, and the 5/10-day חל"ת bifurcation |

**Key distinction:** The Compensation Fund (under the Property Tax and Compensation Fund Law, 1961) handles direct physical damage. **Indirect economic damage has a completely separate process and different deadlines**, different statute (חוק התוכנית לסיוע כלכלי (הוראת שעה) (סיוע לעסקים ולמוסדות ציבור), התשפ"ו-2026 for Shaagat HaAri; Iron Swords hora'at sha'a for that war), different portals, different forms, different appeals tracks. If the user's loss is from business turnover decline, employee wages, or fixed business costs (not physical damage to the building or contents), route to `israeli-business-war-compensation` immediately rather than continuing here.

### Step 2: Document the Damage Immediately

**Critical timing, stated precisely (regulation 5 of תקנות מס רכוש וקרן פיצויים (תשלום פיצויים) (נזק מלחמה ונזק עקיף), תשל"ג-1973):**

- **Notice of damage (הודעה על נזק): two weeks** from the day the damage occurred. Report to the Tax Authority hotline *4954 or through the online direct-damage claim.
- **The claim itself (תביעה לפיצויים)** is a SEPARATE filing. **Filing the notice does not count as filing the claim**, and this is where people lose money. The base regulation text says "תוך חודש" (one month), while the Tax Authority's operational guidance for the current operations says three months. Do not rely on the longer figure: file as early as you can, and confirm the deadline for your event on *4954.
- **Neither deadline is an automatic forfeiture.** Regulation 5(ג): "המנהל רשאי להאריך את המועדים... אם נוכח כי ישנה סיבה סבירה לכך". The extension is discretionary, and **the extension request must be filed BEFORE the deadline runs out**, not after it. Telling someone who is at day 15 that their rights are gone is wrong; telling them to ask for an extension today is right.

**Documentation checklist:**
1. Photograph all damage from multiple angles (wide shots + close-ups)
2. Photograph the overall apartment/house to show context
3. Keep damaged items in place until after the assessor visit (if going regular track)
4. Collect repair quotes from licensed professionals (at least 2 quotes recommended)
5. Save receipts for any emergency repairs already done
6. Note the exact date and time of the damage event
7. If possible, save news reports or Pikud HaOref alerts for that date as supporting evidence

**What NOT to do:**
- Do not dispose of damaged items before documenting them
- Do not start major repairs before an assessor visit (regular track)
- Do not take photos before opening the claim (fast track requires photos taken AFTER the claim is opened, from the damage site, via a link sent by SMS)

### Step 3: Choose Between Fast Track and Regular Track

| Feature | Fast Track (מסלול מהיר) | Regular Track (מסלול רגיל) |
|---|---|---|
| Maximum claim | NIS 30,000 | No ceiling for structure; contents capped by household size |
| Assessor visit | Not required | Required (appraiser visits the property) |
| Approval time | Up to 7 days from complete submission | Weeks to months |
| Documentation | Photos + price quotes uploaded online | Photos + quotes + assessor report |
| Eligibility | Individuals and businesses | Everyone |
| Limit | One claim per household per incident | One claim per household per incident |
| Invoice deadline | Must submit repair invoice within 30 days of receiving payment | Must submit repair invoice within 30 days of receiving payment |

**When to use Fast Track:**
- Total damage is under NIS 30,000
- User wants quick payment and can document damage with photos and quotes
- No complex structural damage requiring professional assessment

**When to use Regular Track:**
- Damage exceeds NIS 30,000
- Structural damage that needs professional engineering assessment
- User wants full compensation without the NIS 30,000 cap

**The fast track is opened per operation and then closed.** It was reopened on 1 March 2026 for Shaagat HaArie with a filing deadline of 28 April 2026, and the Tax Authority closed the equivalent track after the earlier operation. **Never tell a user the fast track is open without checking the current status** on the Tax Authority site or *4954; if it is closed, the regular track is the only route.

**Switching tracks:** Users who filed a regular track claim and have not yet received an assessor visit can switch to the fast track through their personal area on the Tax Authority website. The Compensation Fund may also proactively contact eligible claimants via SMS with an option to switch.

### Step 4: File the Claim Online

**Filing URL:** The claim is filed through the Tax Authority's digital services at gov.il (search for "הגשת תביעה מקוונת נזק ישיר").

**Who can file:**
- Property owner
- Person bearing restoration expenses (even if not the owner)
- Owner of damaged contents (including tenants/renters)

**Required information:**
1. Israeli ID number (Teudat Zehut)
2. Tax Authority digital services login (or create one)
3. Property address where damage occurred
4. Description of damage
5. Photos of damage (see Step 2)
6. Price quotes for repairs
7. Bank account details for compensation payment

**Fast Track specific:** After entering basic details, the system sends an SMS with a link. The user must take and upload photos FROM the damage site ONLY, and ONLY after receiving this SMS. Photos taken before opening the claim or from another location will be rejected and the claim denied.

### Step 5: Understand Compensation Ceilings for Contents

The Compensation Fund covers structural damage in full (no ceiling), but home contents compensation is capped based on household composition.

The ceilings are set by תקנות מס רכוש וקרן פיצויים (תשלום פיצויים) (חפצים ביתיים), תשל"ג-1973, are index-linked, and are re-issued on 1 January and 1 July. The table below is the **01.01.2026** column; re-check it on the Tax Authority site before quoting a figure for a later date.

**Household-contents ceilings (חפצים ביתיים), in shekels, effective 01.01.2026:**

| Category | Single person | Married couple / single parent | Each child under 18 | Each additional adult |
|---|---|---|---|---|
| Furniture (רהיטים) | 14,198 | 24,552 | 4,964 | 7,258 |
| Clothing (בגדים) | 2,366 | 4,731 | 710 | 2,366 |
| Electrical appliances and electronics (מכשירי חשמל ואלקטרוניקה) | 24,894 | 30,175 | 505 | 3,961 |
| **Other household items (חפצים ביתיים אחרים)** | 10,370 | 24,891 | 2,281 | 4,563 |
| **Total** | **51,828** | **84,349** | **8,460** | **18,148** |

**The fourth category is the one everyone forgets.** "חפצים ביתיים אחרים" is worth 24,891 to a couple, nearly as much as the furniture line. A claim that lists only furniture, appliances and clothing leaves that ceiling unused. Kitchenware, tools, linens, books and records, toys, and similar household goods belong there.

The four ceilings are **per category, not interchangeable**: unused furniture headroom does not top up an over-ceiling appliance loss.

**Not covered at all:** cash, cheques, jewellery (תכשיטים), artworks (חפצי אמנות), antiques, and similar valuables. Verbatim from the regulation's definition of a household item: "רהיטים, ביגוד, כלים, מכשירים לשימוש ביתי, ספרים ותקליטים, המצויים בבית מגוריו של אדם ואינם נכס כהגדרתו בחוק, למעט תכשיטים, חפצי אמנות ועתיקות".

### Step 6: Optional War Damage Contents Insurance

If the user's contents are worth more than the standard ceiling, the Tax Authority offers supplemental insurance.

**Key details:**
- Premium: 0.3% of the additional insured value per year
- Available since 2007, but subscriber numbers surged after October 2023
- Coverage starts immediately upon payment and runs through year-end
- No cancellation option after purchase
- This is the ONLY product in Israel that covers war damage to contents above the standard ceiling (regular home insurance excludes war damage)

**Important:** Maximum insurable values and premium amounts should be verified on the Tax Authority website, as these figures may change over time.

**How to purchase:** Online form on the Tax Authority website (search for "ביטוח תכולה רשות המסים" or "ביטוח רכוש מלחמה").

### Step 7: After Filing -- What Happens Next

**Regular Track timeline:**
1. Claim acknowledged by the Compensation Fund
2. Assessor/appraiser (שמאי) scheduled to visit the property
3. Assessor inspects damage, prepares report
4. Compensation amount determined based on assessor report
5. Payment issued
6. User must submit repair invoices within 30 days of receiving payment

**Fast Track timeline:**
1. Claim submitted with photos and quotes
2. Approval within 7 days (if documentation is complete)
3. Payment issued
4. User must submit repair invoices within 30 days of receiving payment

**For structural damage (regular track):** The user can choose between:
- Self-repair: receive compensation and hire their own contractors
- Fund-authorized repair: the Compensation Fund arranges contractors to do the work

### Step 8: Filing an Appeal (Va'adot Erar)

If the user's claim is denied or the compensation amount is too low, they can appeal.

**Appeal process:**
1. The deadline is **30 days from the day the director's decision was delivered** (regulation 11: "רשאי תוך שלושים ימים מיום שנמסרה לו ההחלטה לערור עליה לפני ועדת ערר").
2. Fill in the appeal form and email it to **`Ararim@taxes.gov.il`**.
3. The Compensation Fund submits a written response.
4. The appeal committee (ועדת ערר) hears both sides.
5. Decision issued in writing.

**The fast track costs you your appeal rights on a partial award.** If the claim was filed through the מסלול מהיר and was only PARTIALLY approved, there is no appeal to the ועדת ערר; the appeal route is open only where the claim was rejected outright. Someone with a borderline claim who wants the option to appeal a low award should think twice before taking the fast track.

**Appeal committee composition:** Two members -- a civil servant and a citizen representative, appointed by the Minister of Justice.

**Grounds for appeal:**
- Claim was wrongfully denied
- Compensation amount is too low (e.g., assessor undervalued the damage)
- Eligibility determination was incorrect
- Procedural errors in claim processing

**Further appeal:** If unsatisfied with the appeal committee decision, the claimant can request permission to appeal to the District Court (בית המשפט המחוזי).

**Legal representation:** Not required for the appeal committee, but recommended for complex or high-value cases.

## Examples

### Example 1: Apartment damaged by rocket -- fast track
User says: "A missile hit near my building, all my windows are shattered and some furniture is destroyed. The damage is probably around NIS 20,000."

Actions:
1. Confirm damage is under NIS 30,000 -- recommend Fast Track
2. Guide: notify within two weeks (*4954 or online), then file the claim itself, which is a separate submission
3. After opening claim, wait for SMS link, then photograph damage from the site
4. Upload photos + 2 repair quotes
5. Expect approval within 7 days
6. After receiving payment, submit repair invoices within 30 days

### Example 2: Major structural damage -- regular track
User says: "A rocket hit my building directly. The walls are cracked, ceiling collapsed in one room, and all contents are destroyed. I have a family of 4."

Actions:
1. Damage clearly exceeds NIS 30,000 -- recommend Regular Track
2. Document everything immediately (photos, keep damaged items in place)
3. Notify within two weeks, then file the claim (a separate submission, so do not assume the notice covered it)
4. Assessor will be scheduled to visit
5. Structure: full compensation (no ceiling). Contents for a couple with 2 children (01.01.2026): 84,349 + 2 x 8,460 = 101,269, split across the four category ceilings. Claim the "חפצים ביתיים אחרים" line too, it is worth 24,891 + 2 x 2,281.
6. If contents worth more, suggest purchasing optional insurance for future incidents

### Example 3: Appeal a denied claim
User says: "My compensation claim was approved but they gave me only NIS 15,000 when the damage was at least NIS 40,000. How do I appeal?"

Actions:
1. The appeal deadline is 30 days from delivery of the decision, so check the date on the letter first
2. Check HOW the claim was filed: if it went through the fast track and was only partially approved, there is no appeal to the ועדת ערר (that route is open only for an outright rejection)
3. Prepare a written appeal documenting why the amount is insufficient (additional quotes, photos, a private assessor's opinion)
4. Email the appeal form to Ararim@taxes.gov.il
5. Appeal committee hearing, then a written decision
6. If still unsatisfied, can escalate to District Court

## Bundled Resources

### References
- `references/compensation-ceilings.md` -- Detailed breakdown of compensation ceilings by household size and category, with current NIS amounts (2026). Consult when calculating expected compensation.
- `references/claims-process-flowchart.md` -- Step-by-step flowchart of the claims process for both fast and regular tracks. Consult when guiding users through filing.

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Tax Authority direct-damage online claim | https://www.gov.il/he/service/online-direct-damage-claim | Active claim windows and filing form |
| Tax Authority site (Mas Rechush) | https://www.gov.il/he/departments/israel_tax_authority | Current compensation ceilings, deadline notices, forms |
| Property Tax and Compensation Fund Law (1961) | https://www.nevo.co.il/law_html/law01/273_001.htm | Statute (Tekana) numbering: regulations 8/9/10/11/12 distinctions |
| Property Tax Regulations (1973) | https://www.nevo.co.il/law_html/law01/273_020.htm | Reg 8 (manager's decision), Reg 9 (corrections, 4-year window), Reg 10 (committee composition) |
| State Comptroller report on Tax Authority emergency preparedness (Jan 2026) | https://library.mevaker.gov.il/sites/DigitalLibrary/Documents/2026/Emergency/2026-Emergency-101-Tax.pdf | Process gaps and known delays |
| Kol Zchut: small-business compensation track | https://www.kolzchut.org.il/he/%D7%A4%D7%99%D7%A6%D7%95%D7%99_%D7%9C%D7%A2%D7%A1%D7%A7%D7%99%D7%9D_%D7%A7%D7%98%D7%A0%D7%99%D7%9D | Eligibility for the &lt;300K turnover track |

## Gotchas

1. **Fast Track photo trap:** Photos MUST be taken from the damage site AFTER receiving the SMS link from the Tax Authority. Photos taken before opening the claim or uploaded from another location are automatically rejected. This is the #1 reason fast track claims get denied.

2. **Notice and claim are two separate filings.** The notice of damage is due within two weeks; the claim itself is a separate form with its own deadline (the regulation says one month, current Tax Authority guidance says three). Filing the notice does NOT file the claim. Neither deadline is an automatic forfeiture: regulation 5(ג) lets the director extend both for a reasonable cause, but the extension request must be filed BEFORE the deadline passes.

3. **Contents ceiling confusion:** the ceiling varies by household size AND by category, and there are FOUR categories, not three. The forgotten one is "חפצים ביתיים אחרים" (24,891 for a couple), which is where kitchenware, tools, linens, books and toys go. A claim listing only furniture, appliances and clothing leaves that whole ceiling unclaimed. The categories are not interchangeable: unused furniture headroom does not top up an over-ceiling appliance loss.

4. **Regular home insurance does NOT cover war damage:** Commercial home insurance policies in Israel explicitly exclude war and hostility damage. Only the Tax Authority Compensation Fund (and its optional extended insurance) covers war-related property damage. Do not direct users to their regular insurance company for war damage claims.

5. **Invoice deadline after payment:** After receiving compensation, the claimant MUST submit repair invoices within 30 days. Failure to do so triggers a repayment demand. This catches many people off guard -- they receive the money but forget to send receipts after completing repairs.

## Troubleshooting

### Error: "Claim rejected -- photos not from damage site"
Cause: Fast Track requires photos taken at the damage location after the SMS link is sent. The system uses geolocation to verify.
Solution: Re-open the claim, wait for the new SMS link, go to the damage site, then take and upload fresh photos from that location.

### Error: "Missed the two-week notification deadline"
Cause: The user did not notify the Tax Authority within two weeks of the incident.
Solution: This is NOT an automatic forfeiture. Regulation 5(ג) empowers the director to extend the deadline where there is a reasonable cause ("אם נוכח כי ישנה סיבה סבירה לכך"), and mass incidents, evacuation, hospitalisation or a call-up are exactly that. File the notice and the claim now, attach the reason for the delay, and ask for the extension in the same submission. If a deadline has not yet passed, ask for the extension BEFORE it does; a request made after the fact is much weaker.

### Error: "Compensation amount seems too low"
Cause: The assessor may have undervalued the damage, or the contents ceiling was applied.
Solution: Check if the ceiling applies (contents vs structure). If undervalued, file an appeal (Step 8) with independent repair quotes or a private assessor report to support a higher amount.

### Error: "Cannot access Tax Authority digital services"
Cause: User may not have a registered account or may have login issues.
Solution: Register at the Tax Authority website with Teudat Zehut. If locked out, contact Tax Authority support at *4954 or visit a local Tax Authority office in person.