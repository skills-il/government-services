---
name: israeli-returning-resident-customs-vehicle
description: >-
  Customs and vehicle-import planner for Israelis returning home (תושב חוזר / toshav chozer).
  Use when a user asks about "מכס לתושב חוזר", "יבוא רכב לתושב חוזר", "כמה משלוחים מותר",
  "חלון 9 חודשים", "כמה טלוויזיות מותר", "כדאי לייבא את הרכב", the 6-year hold on duty-free
  items, the 48-months-from-manufacture vehicle window, the customs file (תיק זכאות במכס),
  or how returnee customs differ from olim. Disambiguates returnees from olim (returnees
  get 2 shipments and 1 unit per appliance type, NOT the oleh 3-shipment basket) and warns
  there is no purchase-tax exemption on vehicles, only an extended age window.
  Do NOT use for the process navigator (use israeli-returning-resident-navigator), Section 14
  tax math (use israeli-toshav-chozer-vatik-tax-planner), oleh chadash customs (use
  israeli-aliyah-customs-shipment-planner), people LEAVING Israel (use israeli-relocation-abroad),
  or binding advice (refer to a licensed customs broker / סוכן מכס).
license: MIT
---

# Israeli Returning Resident Customs and Vehicle Planner

## Problem

Returnees routinely lose money on the trip back. They miss the 9-month customs window, conflate their 2-shipment basket with the oleh 3-shipment basket, ship 4 TVs when only 3 are duty-free, sell a paid-off car abroad because they assume returnees pay full tax (they do, but with a wider age window so the car might still be worth shipping), or ship a car expecting a purchase-tax break that does not exist. AI agents make this worse: training data conflates olim and returnees because both flows live under "personal import" at Meches. This skill produces a per-shipment declaration draft, a ship-vs-sell vehicle worksheet, and a windows timeline so the user does not learn the rules by paying for a mistake.

## Instructions

### Step 1: Confirm customs status before quoting any number

Customs definitions are NOT the same as Misrad HaAliyah definitions. Ask:

- **Returning resident (תושב חוזר) for customs**: Israeli resident, abroad **2 years or more**, returning permanently. Also covers second-time olim and entrants the Israel Tax Authority specifically classifies as returnees.
- **Returning student (סטודנט חוזר)**: Israeli resident abroad **18+ months** who studied full-time **2 consecutive academic years** at a recognized institution, or earned a degree. Must return within **6 months of finishing studies / receiving the degree** or the student status lapses.
- **There is no "vatik (10-year)" customs basket.** The 6-year and 10-year vatik thresholds live in income-tax world (Section 14). Meches only knows "returnee". If the user has been abroad 12 years, they get the same customs basket as a 2-year returnee. The tax-planner sister skill handles the 10-year math.
- **Year-of-absence rule**: each year of absence counts even if the user visited Israel up to **4 cumulative months** in that year (gov.il chapter 9). Exceed 4 months in a single absence-year and that year does NOT count toward the 2-year (returnee) or 18-month (student) threshold. Surface this explicitly because returnees with regular Israel visits often misread the rule as "no visits allowed."
- **Permanent-return entry vs. tourist visit**: many returnees fly in on a tourist visa first, leave, then return permanently months later. The 9-month customs clock anchors to the **permanent-return entry** (the trip where the user actually re-establishes Israeli residency), NOT to an earlier tourist visit. Ask the user which trip is the permanent move; that is D in the timeline.
- If the user has been abroad less than 2 years (or less than 18 months as a student), they are NOT a returnee for customs and the regular Israeli-resident personal-import rules apply. Stop and hand off.

The Misrad HaAliyah תעודת תושב חוזר is helpful but NOT required to open the customs file. The customs file is opened on a separate Meches form. If the user is still chasing the certificate, they can start the customs file in parallel.

### Step 2: The household-shipment basket (returnees, NOT olim)

| Item | Returnee cap (per family) |
|---|---|
| Number of shipments | **2 shipments** (NOT 3 like olim) |
| Window to receive shipments | **9 months from date of physical entry** to Israel, NOT extendable |
| TV sets | up to **3** total |
| Personal computers | up to **3** total |
| Other electrical / electronic appliances | **1 per type** (1 fridge, 1 dishwasher, 1 washer, 1 dryer, 1 oven, 1 microwave, etc.) |
| Major furniture items | **1 per type** (1 sofa set, 1 dining set, etc.; "type" is interpreted liberally by clerks) |
| Hold period | items must remain in returnee's personal use in Israel for at least **6 years**; selling, transferring, or destroying inside the window triggers tax payback + possible criminal probe |
| Re-claim of same item type | only after returnee has spent **6 years in Israel** since the prior duty-free release of that item type |
| Spousal anti-stacking | cannot re-claim what spouse already released duty-free unless 6 years passed AND user was not the spouse at time of prior release |

A single household item brought on entry day as accompanying luggage (carry-on / checked baggage) does NOT count as one of the 2 shipments, it is duty-free at the airport but must be declared on the red channel.

A mail package containing household goods DOES count as one of the 2 shipments. Clothing-only mail packages are exempt if they arrive within 30 days before entry, on the day of entry, or within 3 months after entry.

**Save money: consolidate.** Meches counts shipments by Bill of Lading, not by physical move. If a returnee originally planned two separate liftvans, a freight forwarder can consolidate them into a single container with one Bill of Lading and that counts as ONE shipment, freeing the second slot for a later post-arrival package. Many returnees save $4-7k by consolidating; ask the broker / forwarder about combining lifts before booking.

**Inheritance items shipped from abroad** travel under their own customs basket (linked to inheritance / מס ירושה documentation), NOT the 2-shipment household quota, provided the items are properly documented as inherited property at clearance. If the user is bringing furniture or items inherited from a parent abroad, surface this as a separate flow and refer to a customs broker for the inheritance-channel paperwork.

### Step 3: Accompanying-luggage allowance (separate from the 2 shipments)

On entry day, every entrant aged 2+ may bring duty-free:

- Clothing, footwear, personal toiletries, customary travel quantities
- Other items up to a per-entrant value cap (currently quoted as **$200 USD equivalent**, with the NIS equivalent set periodically by the takanot , verify the live NIS figure on the gov.il customs guide chapter 3 at answer time, since gov.il publishes the cap in NIS). The cap is per entrant, not poolable across family members. Above the cap the user pays tax on the FULL value of the item, not just the excess.
- Within the per-entrant cap: mixed food up to 3 kg total, no single food type over 1 kg.
- Entrants aged 18+: up to 1 liter spirit + 2 liters wine + 250 ml alcohol perfumes + 250 g tobacco / 200 cigarettes.

If the user has anything beyond the personal allowance, they must use the red channel ("מסלול אדום") and declare.

**Tools of the trade** (כלי עבודה מהסוג הנישא ביד) and **business machines** (מכשירים ומכונות לעסק) travel under their own gov.il chapters, separate from the household basket. A returnee in trades (electrician, hairdresser, photographer, dentist, contractor) can bring professional hand tools and certain business equipment under different conditions, often duty-free, without consuming a household-shipment slot. Surface this as a one-line pointer to the broker if the user mentions a profession that ships tools.

**Restricted-permit items** require a separate import permit from the relevant ministry BEFORE the shipment arrives, on top of any customs benefit. Most-confiscated categories at Ashdod (gov.il chapter "פריטים, שהתנאי ליבוא שלהם הוא אישור הרשות המוסמכת"): drones (Misrad HaTikshoret + RSHTOT), communications gear / baby monitors / signal-emitting devices (Misrad HaTikshoret, 03-5198282), plants and seeds (Misrad HaChaklaut, 03-9681587), pets (Misrad HaChaklaut Veterinary, 03-9485461), weapons and weapon parts (Misrad LeBitachon Pnim, 077-2324444), lasers (Misrad HaKalkala), electric scooters and e-bikes (Misrad HaTachbura import unit). Tell the user to check the gov.il "מחשבון ליבוא אישי" calculator for the specific item BEFORE shipping.

**Pets**: not a customs-benefit topic per se, but every returnee asks. Misrad HaChaklaut import permit + microchip + rabies titer typically 90+ days before flight. Refer the user to the veterinary services unit for the latest checklist.

### Step 4: Vehicle import, the math that surprises most returnees

Returnees do NOT get a purchase-tax / VAT / customs-duty exemption on a personally-imported vehicle. The ONLY benefit is an extended age window:

| Eligibility | Vehicle age cap from manufacture date |
|---|---|
| Regular Israeli resident, personal import | **24 months** |
| Returning resident or returning student | **48 months** |

Other conditions: vehicle must be a make/model approved by Misrad HaTachbura, current model year or one of the 4 previous model years, driver must hold a valid Israeli license for that vehicle category, age 17+ on entry day. The vehicle must be imported within **9 months from permanent-return entry**.

**The vehicle 9-month window is a DIFFERENT window** from the 2-shipment household 9-month window. Both run from D, but they are separate procedural clocks governed by separate takanot (the customs takanot for household goods vs. the מס קניה / Misrad HaTachbura takanot for vehicles). A returnee who blew the household window may still have a live vehicle window and vice versa. Treat them as independent in any timeline you produce.

**Per-family vehicle quota (operational)**: gov.il and kolzchut do not publish a hard cap, but customs broker practice treats the returnee benefit as **one personally-imported vehicle per eligible returnee**. A couple where both spouses qualify can in principle import two vehicles in the 9-month window. Verify with the local Meches office and Misrad HaTachbura before ordering a second vehicle.

**12-month bealut-transfer restriction**: Misrad HaTachbura imposes a 12-month hold on every personally-imported vehicle, returnee or not. Source: gov.il [יבוא אישי של כלי רכב](https://www.gov.il/he/pages/personal_import_of_vehicles): "על רכב המיובא ביבוא אישי מוטלת מגבלת העברת בעלות למשך 12 חודשים." A separate procedure (Nahal 416) exists for applying to remove the restriction earlier in justified cases. Plan to keep the vehicle at least 12 months; the broker can advise on Nahal 416 if circumstances change.

After clearance and Misrad HaRishui registration, a tax refund based on equipment level can sometimes be claimed at Meches ("החזר על הפרש המסים בהתאם לרמת האבזור"). This is downstream and non-trivial, refer the user to a customs broker.

**The ship-vs-sell decision** almost always pencils to "sell abroad and buy locally" because the returnee pays full Israeli tax. Per gov.il personal_import_of_vehicles_guide chapter 3 (updated 15.01.2026), the combined customs + purchase tax + VAT lands at roughly **116% of CIF** for passenger cars from FTA-origin (USA, EU, Canada, UK, Korea, etc.), **131% of CIF** for non-FTA origin, **75-87%** for EVs, and **103-117%** for collector cars. Hybrids depend on the specific green-tax pollution grade. Shipping makes sense when (a) the car is paid off and the user is emotionally attached, (b) the model is rare in Israel, or (c) the user is moving from a high-spec North-American market and the Israeli equivalent is meaningfully more expensive. Run `scripts/vehicle-decision.py` to get the worksheet.

### Step 5: Open the customs entitlement file (תיק זכאות)

1. Online: file the form via [gov.il, בקשת זכאות לפטור לתושבים חוזרים](https://www.gov.il/he/service/request-for-entitlement-exemption-for-returning-resident-student). The system opens the file automatically. No physical visit needed in the happy path.
2. If the auto-approval fails, visit a Meches office (find list at [gov.il customs guide](https://www.gov.il/he/pages/customs-guide-for-returning-residents), section "רשימת משרדי המכס") with:
   - Israeli ID + passport (yours)
   - Israeli ID + passport (spouse, if applicable)
   - תעודת תושב חוזר from Misrad HaAliyah, if you have it
3. Returning students: bring institutional certification (2 years full-time enrollment, or degree certificate).
4. On entry the customs officer may require a bond / deposit equal to 6 months of the applicable taxes. The deposit is refunded if the entitlement file is approved within 9 months. Plan for short-term cash-flow impact.

The returnee CAN start the file even before the תעודת תושב חוזר is issued; Meches has its own determination process. Sources of confusion: some Meches branches will ask for the certificate, others accept the online auto-approval. If a clerk demands the certificate, the returnee can either (a) wait for Misrad HaAliyah, or (b) escalate via the **Rashut HaMisim 1299 hotline** (the Israel Tax Authority's main service line, which routes customs questions internally). For vehicle-specific Misrad HaTachbura status issues (import permit, type approval, bealut-restriction Nahal 416), use **\*4515** (Misrad HaTachbura import unit, listed on the gov.il יבוא אישי של כלי רכב page).

### Step 6: Currency on the body (anti-money-laundering)

Section 9 of the Anti-Money-Laundering Law requires declaration on entry / exit if total value exceeds:

- **50,000 NIS** equivalent at air / sea borders
- **12,000 NIS** equivalent at land borders

Family members traveling together cannot pool to skirt the cap, each entrant declares independently if they personally carry above the threshold. Joint family ownership above threshold must be declared even if each individual carries less. Failure to declare triggers seizure, potential fine, or criminal indictment with up to 6 months imprisonment.

### Step 7: Build the timeline

Hand the user `references/customs-timeline.md` or compute it inline. Anchor everything to **D = date of permanent-return physical entry to Israel** (NOT a prior tourist visit, NOT date of certificate issue, NOT date of leaving the foreign country):

- D + 0: arrival; declare on red channel anything over personal allowance; declare currency if applicable; pay any required bond.
- D + 0 to D + 30: open online entitlement file at gov.il if not already done.
- D + 0 to D + 9 months (household clock): first household shipment must arrive AND clear customs.
- D + 0 to D + 9 months (household clock): second household shipment (if needed) must arrive AND clear customs.
- D + 0 to D + 9 months (separate vehicle clock under מס קניה / Misrad HaTachbura takanot): any personally-imported vehicle must arrive AND clear customs.
- D + clearance of vehicle to clearance + 12 months: Misrad HaTachbura bealut-transfer restriction (do not sell / transfer the vehicle without Nahal 416 application).
- D + 0 to D + 6 years: household-goods hold period, none of the duty-free items may be sold, transferred, or destroyed without paying back the tax + interest.
- D + 6 years onward: re-claim window opens for items the returnee already released duty-free.

### Step 8: When to hand off

- Process / kupat cholim / Form 628 / driver's license → `israeli-returning-resident-navigator`.
- Section 14 10-year tax exemption math / Form 1348 → `israeli-toshav-chozer-vatik-tax-planner`.
- Oleh chadash 3-shipment basket / sal-klita customs link → `israeli-aliyah-customs-shipment-planner` (planned).
- People still abroad planning to leave Israel → `israeli-relocation-abroad`.
- Actual filing of the customs declaration, HS codes, equipment-level vehicle refund, dispute with a customs commissioner → licensed customs broker (סוכן מכס). This skill is a planning aid, not a substitute for a broker.

## Examples

### Example 1: Two-shipment family with one TV too many

> User: "אני חוזרת אחרי 7 שנים בסיליקון ואלי, יש לי בעל וילד. אנחנו מתכננים לשלוח 4 טלוויזיות (סלון, חדר שינה, חדר עבודה, חדר ילדים), מקרר, מייבש, מקפיא נפרד, שני מחשבים שולחניים, ולפטופ אחד. כמה משלוחים? מה לזרוק?"

Response framework:
1. Returnee customs status: yes (7 years > 2 years), but does NOT change the basket.
2. Shipments: 2 max. Plan accordingly.
3. Cap: 3 TVs (so the 4th is taxable, either sell, leave in storage abroad, or pay tax on entry).
4. Cap: 1 fridge OK. 1 dryer OK. **Separate freezer is a second appliance of the same "refrigeration" type**, flag this as a clerk-judgment item; the user should ask Meches in writing before shipping. If counted separately as "freezer" it may be allowed as 1 of its type.
5. Computers: 2 desktops + 1 laptop = 3 PCs total. Right at the cap. OK.
6. Send the user to the gov.il online entitlement form before shipping.

### Example 2: Ship the car or sell it?

> User: "יש לי טויוטה הייבריד 2023 עם 40 אלף מייל. שיוויה בארה״ב כ-28 אלף דולר. עלות משלוח לישראל כ-3,500 דולר. כדאי לשלוח?"

Response framework:
1. Eligibility for the 48-month window: 2023 car in mid-2026 = ~30 months from manufacture, well inside 48 months. Vehicle is eligible for personal import.
2. **No purchase-tax exemption.** Per gov.il personal_import_of_vehicles_guide chapter 3, the combined customs + purchase tax + VAT (with VAT at 18% from 2025-01-01) lands at ~116% of CIF for hybrids from FTA-origin like Japan or the USA, exact green-tax adjustment depending on the specific model's pollution grade. Verify exact rate with a customs broker.
3. Run the worksheet (`scripts/vehicle-decision.py`) with the user's numbers. Typically: CIF ≈ $28,000 + $3,500 = $31,500; combined Israeli tax ≈ $31,500 × 1.0 to 1.15 (hybrid band) ≈ $31,500-$36,000; total landed ≈ $63,000-$67,500 + ~$1,200 broker / registration fees. Local Toyota hybrid equivalent ~$50,000. The ship option loses by $13,000-$17,000 in the typical case. Shipping wins only when the model is unavailable locally or the local trim is meaningfully lower.
4. Surface: Misrad HaTachbura imposes a 12-month bealut-transfer restriction on every personally-imported vehicle (gov.il, "מגבלת העברת בעלות למשך 12 חודשים"). Plan to keep the vehicle at least 12 months. A separate procedure (Nahal 416) handles early-release applications.

### Example 3: 6-year hold trap

> User: "חזרתי לפני 4 שנים, פתחתי תיק זכאות וייבאתי מקרר ומכונת כביסה בפטור. עכשיו אני רוצה לעבור דירה ולקנות מקרר חדש בארץ. צריך לשלם משהו?"

Response framework:
1. Selling/transferring the duty-free fridge inside the 6-year hold triggers tax payback. Confirm: did the user sell the original fridge, give it away, or just stop using it?
2. If user keeps the original fridge in personal use (e.g., moves it to the new home), no problem, they're free to ALSO buy a new fridge at full Israeli tax. The hold rule is about the duty-free unit, not about owning multiple.
3. If user sold or gave it away: tax payback applies, calculated on the original duty-free fridge's value at the time of release, plus interest. Refer to Meches to compute the exact amount.
4. The re-claim window (importing another duty-free fridge) opens at year 6 from D, not from the date of selling the original.

## Bundled Resources

- `references/domain-checklist.md`: authoritative sources, must-cover and should-cover facts, last-verified dates.
- `references/vehicle-import-benefit.md`: eligibility, age window, lack of purchase-tax exemption, kolzchut + gov.il citations, ship-vs-sell economic guide.
- `references/household-shipment-rules.md`: 2-shipment basket, 9-month window, item-by-item caps, 6-year hold, spousal anti-stacking.
- `references/customs-timeline.md`: day-by-day from entry to year 6.
- `scripts/vehicle-decision.py`: reads user inputs (car value, shipping quote, equivalent local price) and prints a side-by-side decision worksheet.

## Recommended MCP Servers

None directly applicable. The customs Tax Authority does not expose an MCP / API. Users with Meches / customs questions should call **1299** (Rashut HaMisim main service line). For vehicle-specific Misrad HaTachbura questions (import permit, type approval, bealut-restriction Nahal 416) use **\*4515** (import unit). For Misrad HaAliyah questions about the תעודת תושב חוזר use **\*2994**. Or visit a Meches office in person.

## Gotchas

1. **Returnees are NOT olim.** The single most common mistake: assuming the oleh 3-shipment basket applies. It does not. Returnees get 2 shipments. Period.
2. **No purchase-tax exemption on vehicles for returnees.** Stop quoting "tax-free car import", it does not exist for returnees. Combined customs + purchase tax + VAT lands at roughly 116% of CIF for FTA-origin passenger cars, 131% for non-FTA, 75-87% for EVs, per gov.il personal_import_of_vehicles_guide chapter 3. The 48-month age window is the only benefit.
3. **Vehicle 12-month bealut-transfer restriction.** Misrad HaTachbura imposes a 12-month ownership-transfer hold on every personally-imported vehicle (gov.il, "מגבלת העברת בעלות למשך 12 חודשים"). Plan to keep the vehicle at least 12 months; Nahal 416 is the early-release procedure.
4. **Vehicle 9-month window ≠ household 9-month window.** They are independent procedural clocks (vehicles run under מס קניה / Misrad HaTachbura takanot, household runs under customs takanot). Both start at D, but missing one does not affect the other. Treat them as two separate deadlines.
5. **Permanent-return entry, not tourist visit, anchors D.** A returnee who flew in on a tourist visa for a 2-week trip, then went back abroad and came home permanently 4 months later, anchors the 9-month clock to the PERMANENT-return entry. Surface this with the user before computing D.
6. **9-month clock starts on entry, not on certificate issue.** Returnees who chase the Misrad HaAliyah certificate first sometimes burn 4 months before realizing the customs clock has been running since wheels-down.
7. **6-year hold has teeth.** Selling a duty-free fridge in year 3 to upgrade is a tax-payback event plus possible criminal investigation. Surface this every time on the timeline.
8. **Spousal anti-stacking.** If user's spouse already imported a duty-free washing machine 4 years ago and the user is now claiming a returnee basket, that washing machine is NOT a fresh entitlement for the same household. The 6-year clock resets independently per item type per couple.
9. **The "type" definition is clerk-judgment.** A combo fridge-freezer is one item; a separate fridge and separate freezer is two items of different "types", or one of the same "refrigeration" type, depending on the clerk. Tell the user to ask Meches in writing before shipping borderline items.
10. **Mail packages count.** A shipment of household goods sent via post counts as one of the 2 shipments. Clothing-only mail in the 30-day-before / day-of / 3-months-after window does not.
11. **Save money: consolidate.** Meches counts shipments by Bill of Lading. Two scheduled lifts combined into one container = one shipment, leaving the second slot open. Many returnees save $4-7k by asking the forwarder to consolidate.
12. **Vehicle equipment-level refund is not automatic.** The downstream refund based on actual equipment level requires the returnee to come back to Meches with documentation. Most returnees do not know this exists. Surface as an opportunity.
13. **Insure at full value INCLUDING all taxes.** The gov.il guide chapter 9 explicitly requires insuring shipments at their full value including the customs duties and taxes ("בערכם המלא, כולל כל המסים"). Under-insured shipments get claims rejected at Meches when something is damaged or stolen in transit. Quote the FULL landed-cost figure to the insurer, not the abroad-market value.
14. **Restricted-permit items require a separate import permit.** Drones, communications gear, weapons, lasers, e-scooters, plants, certain electronics , most-confiscated category at Ashdod. Verify the import permit from the relevant ministry BEFORE shipping; the customs benefit does not waive the permit requirement.
15. **Inheritance items have their own basket.** Items inherited abroad and shipped to Israel travel under inheritance documentation, NOT counted under the 2-shipment household cap. Refer the user to a broker for the inheritance-channel paperwork.

## Reference Links

| URL | Topic |
|---|---|
| https://www.gov.il/he/pages/customs-guide-for-returning-residents | Official customs guide for returning residents (Israel Tax Authority), updated 18.05.2026 |
| https://www.gov.il/he/service/request-for-entitlement-exemption-for-returning-resident-student | Online service: open a customs entitlement file (תיק זכאות) |
| https://www.gov.il/he/pages/personal_import_of_vehicles_guide | Personal vehicle import guide (Israel Tax Authority) |
| https://www.gov.il/he/departments/guides/personal_import_of_vehicles | Personal vehicle import (Misrad HaTachbura, approvals + type approval) |
| https://www.kolzchut.org.il/he/יבוא_אישי_של_רכב_לתושבים_וסטודנטים_חוזרים | kolzchut, personal vehicle import for returning residents and students (updated 10.12.2025) |
| https://www.kolzchut.org.il/he/פטור_ממס_קניה,_מע"מ_ותשלומי_מכס_לתושב_חוזר_ולסטודנט_חוזר_בייבוא_חפצי_בית | kolzchut, customs exemption for returnee / student importing household goods (updated 02.03.2025) |

## Troubleshooting

- **gov.il customs guide URL returns a 403 to scrapers**: it loads fine in a real browser; if an agent cannot fetch it, fall back to the kolzchut mirrors above and the citations in `references/domain-checklist.md`.
- **Meches clerk insists on the Misrad HaAliyah certificate even though the gov.il guide says the online system handles it**: this is a known inconsistency. The user can (a) wait, or (b) escalate via the 1299 hotline.
- **Auto-approval fails for a returnee who was abroad on a long trip but kept an Israeli address**: Meches may classify the user as never having lost residency. Bring proof of foreign residency (lease, tax returns, work permit) to the in-person appointment.
- **Customs broker (סוכן מכס) gives a different number than this skill quotes**: a broker is dealing with the live takanot and Meches commissioner discretion. Trust the broker on the actual filing; use this skill for the planning conversation BEFORE engaging the broker.
- **The user already shipped 3 shipments**: not all is lost, the third shipment will clear as a regular import (full tax), but the goods clear; user pays the tax difference. This skill should have prevented this; surface the lesson and move on.
