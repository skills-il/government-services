---
name: israeli-returning-resident-customs-vehicle
description: >-
  מתכנן מכס ויבוא רכב לישראלים שחוזרים הביתה (תושב חוזר). השתמשו כשהמשתמש שואל על
  "מכס לתושב חוזר", "יבוא רכב לתושב חוזר", "כמה משלוחים מותר", "חלון 9 חודשים מכס",
  "כמה טלוויזיות מותר להביא", "האם משתלם לייבא את הרכב שלי", תקופת ההחזקה של 6 שנים
  על פריטים פטורים, חלון של 48 חודשים מתאריך ייצור הרכב, פתיחת תיק זכאות במכס,
  או איך המכס לתושב חוזר שונה מהמכס לעולה. מפריד תושב חוזר מעולה חדש (תושב חוזר
  מקבל 2 משלוחים ויחידה אחת מכל סוג מוצר חשמל, לא את הסל של 3 משלוחים שמקבל עולה
  חדש), ומסביר שאין פטור ממס קניה ברכב לתושב חוזר, רק חלון רחב יותר לגיל הרכב.
  אל תשתמשו בכלי הזה לניווט תהליך / טופס 628 / קופת חולים / רישיון נהיגה
  (השתמשו ב-israeli-returning-resident-navigator), לחישוב מס לפי סעיף 14 או טופס 1348
  (השתמשו ב-israeli-toshav-chozer-vatik-tax-planner), למכס לעולה חדש בסל 3 המשלוחים
  (השתמשו ב-israeli-aliyah-customs-shipment-planner), לישראלים שעוזבים את הארץ
  (השתמשו ב-israeli-relocation-abroad), או לייעוץ משפטי / מכסי מחייב (פנו לסוכן מכס מוסמך).
license: MIT
---

# מתכנן מכס ויבוא רכב לתושב חוזר

## הבעיה

תושבים חוזרים מאבדים כסף בדרך הביתה. הם מפספסים את חלון 9 החודשים, מתבלבלים בין הסל של עולה חדש (3 משלוחים) לבין הסל של תושב חוזר (2 משלוחים), שולחים 4 טלוויזיות כשרק 3 פטורות, מוכרים רכב משולם בחו"ל מתוך הנחה שאין יתרון ביבוא אישי כתושב חוזר (יש, אבל חלקי), או דווקא משלמים על משלוח רכב בציפייה לפטור ממס קניה, פטור שלא קיים לתושבים חוזרים. סוכני AI מעמיקים את הבלבול כי החומר מערבב עולים ותושבים חוזרים. הכלי הזה מפיק טיוטת הצהרת מכס לכל משלוח, גיליון החלטה לרכב, וציר זמן עם החלונות, כדי שהמשתמש לא ילמד את הכללים מטעות שעולה כסף.

## הוראות

### Step 1: Confirm customs status before quoting any number

Customs definitions are NOT the same as Misrad HaAliyah definitions. Ask:

- **Returning resident (תושב חוזר) for customs**: Israeli resident, abroad **2 years or more**, returning permanently. Also covers second-time olim and entrants the Israel Tax Authority specifically classifies as returnees.
- **Returning student (סטודנט חוזר)**: Israeli resident abroad **18+ months** who studied full-time **2 consecutive academic years** at a recognized institution, or earned a degree. Must return within **6 months of finishing studies / receiving the degree** or the student status lapses.
- **There is no "vatik (10-year)" customs basket.** The 6-year and 10-year vatik thresholds live in income-tax world (Section 14). Meches only knows "returnee". If the user has been abroad 12 years, they get the same customs basket as a 2-year returnee. The tax-planner sister skill handles the 10-year math.
- If the user has been abroad less than 2 years (or less than 18 months as a student), they are NOT a returnee for customs and the regular Israeli-resident personal-import rules apply. Stop and hand off.

The Misrad HaAliyah תעודת תושב חוזר is helpful but NOT required to open the customs file, the customs file is opened on a separate Meches form. If the user is still chasing the certificate, they can start the customs file in parallel.

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

### Step 3: Accompanying-luggage allowance (separate from the 2 shipments)

On entry day, every entrant aged 2+ may bring duty-free:

- Clothing, footwear, personal toiletries, customary travel quantities
- Other items up to **$200 USD value per entrant** (not poolable across family members). Above $200 the user pays tax on the FULL value of the item, not just the excess.
- Within the $200: mixed food up to 3 kg total, no single food type over 1 kg.
- Entrants aged 18+: up to 1 liter spirit + 2 liters wine + 250 ml alcohol perfumes + 250 g tobacco / 200 cigarettes.

If the user has anything beyond the personal allowance, they must use the red channel ("מסלול אדום") and declare.

### Step 4: Vehicle import, the math that surprises most returnees

Returnees do NOT get a purchase-tax / VAT / customs-duty exemption on a personally-imported vehicle. The ONLY benefit is an extended age window:

| Eligibility | Vehicle age cap from manufacture date |
|---|---|
| Regular Israeli resident, personal import | **24 months** |
| Returning resident or returning student | **48 months** |

Other conditions: vehicle must be a make/model approved by Misrad HaTachbura, current model year or one of the 4 previous model years, driver must hold a valid Israeli license for that vehicle category, age 17+ on entry day. The vehicle must be imported within **9 months from permanent-return entry**.

**The vehicle 9-month window is a SEPARATE clock** from the household 9-month window. Vehicles run under מס קניה / Misrad HaTachbura takanot; household goods run under customs takanot. Treat them independently.

**Per-family vehicle quota (operational)**: gov.il and kolzchut do not publish a hard cap, but customs broker practice treats the returnee benefit as one personally-imported vehicle per eligible returnee. A couple where both spouses qualify can in principle import two vehicles in the 9-month window.

**12-month bealut-transfer restriction**: Misrad HaTachbura imposes a 12-month hold on every personally-imported vehicle, returnee or not. Source: gov.il "יבוא אישי של כלי רכב": "על רכב המיובא ביבוא אישי מוטלת מגבלת העברת בעלות למשך 12 חודשים". Nahal 416 is the early-release procedure.

After clearance and Misrad HaRishui registration, a tax refund based on equipment level can sometimes be claimed at Meches ("החזר על הפרש המסים בהתאם לרמת האבזור"). Refer the user to a customs broker.

**The ship-vs-sell decision** almost always pencils to "sell abroad and buy locally" because the returnee pays full Israeli tax. Per gov.il personal_import_of_vehicles_guide chapter 3 (updated 15.01.2026), the combined customs + purchase tax + VAT (with VAT at 18% from 2025-01-01) lands at roughly 116% of CIF for passenger cars from FTA-origin, 131% for non-FTA, 75-87% for EVs, 103-117% for collector cars. Shipping makes sense when the model is rare in Israel or the user is bringing a high-spec North-American market vehicle. Run `scripts/vehicle-decision.py` for the worksheet.

### Step 5: Open the customs entitlement file (תיק זכאות)

1. Online: file the form via [gov.il, בקשת זכאות לפטור לתושבים חוזרים](https://www.gov.il/he/service/request-for-entitlement-exemption-for-returning-resident-student). The system opens the file automatically. No physical visit needed in the happy path.
2. If the auto-approval fails, visit a Meches office (find list at [gov.il customs guide](https://www.gov.il/he/pages/customs-guide-for-returning-residents), section "רשימת משרדי המכס") with:
   - Israeli ID + passport (yours)
   - Israeli ID + passport (spouse, if applicable)
   - תעודת תושב חוזר from Misrad HaAliyah, if you have it
3. Returning students: bring institutional certification (2 years full-time enrollment, or degree certificate).
4. On entry the customs officer may require a bond / deposit equal to 6 months of the applicable taxes. The deposit is refunded if the entitlement file is approved within 9 months. Plan for short-term cash-flow impact.

The returnee CAN start the file even before the תעודת תושב חוזר is issued; Meches has its own determination process. Sources of confusion: some Meches branches will ask for the certificate, others accept the online auto-approval. If a clerk demands the certificate, the returnee can either (a) wait for Misrad HaAliyah, or (b) escalate via the Rashut HaMisim 1299 hotline. For Misrad HaTachbura vehicle-specific status (import permit, Nahal 416), call \*4515. For Misrad HaAliyah certificate status, call \*2994.

### Step 6: Currency on the body (anti-money-laundering)

Section 9 of the Anti-Money-Laundering Law requires declaration on entry / exit if total value exceeds:

- **50,000 NIS** equivalent at air / sea borders
- **12,000 NIS** equivalent at land borders

Family members traveling together cannot pool to skirt the cap, each entrant declares independently if they personally carry above the threshold. Joint family ownership above threshold must be declared even if each individual carries less. Failure to declare triggers seizure, potential fine, or criminal indictment with up to 6 months imprisonment.

### Step 7: Build the timeline

Hand the user `references/customs-timeline.md` or compute it inline. Anchor everything to **D = date of permanent-return physical entry to Israel** (NOT a prior tourist visit, NOT date of certificate issue):

- D + 0: arrival; declare on red channel anything over personal allowance; declare currency if applicable; pay any required bond.
- D + 0 to D + 30: open online entitlement file at gov.il if not already done.
- D + 0 to D + 9 months (household clock): first and second household shipments must arrive AND clear customs.
- D + 0 to D + 9 months (separate vehicle clock under מס קניה / Misrad HaTachbura takanot): any personally-imported vehicle must arrive AND clear customs.
- Vehicle clearance to clearance + 12 months: Misrad HaTachbura bealut-transfer restriction.
- D + 0 to D + 6 years: household hold period, none of the duty-free items may be sold, transferred, or destroyed without paying back the tax + interest.
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
4. Cap: 1 fridge OK. 1 dryer OK. Separate freezer is a clerk-judgment item; ask Meches in writing before shipping.
5. Computers: 2 desktops + 1 laptop = 3 PCs total. Right at the cap. OK.
6. Send the user to the gov.il online entitlement form before shipping.

### Example 2: Ship the car or sell it?

> User: "יש לי טויוטה הייבריד 2023 עם 40 אלף מייל. שיוויה בארה״ב כ-28 אלף דולר. עלות משלוח לישראל כ-3,500 דולר. כדאי לשלוח?"

Response framework:
1. Vehicle is eligible for personal import (within 48 months from manufacture).
2. **No purchase-tax exemption.** Combined Israeli tax for an imported passenger car lands in a high band of CIF after customs duty + purchase tax + green-tax adjustment + VAT (gov.il vehicle guide chapter 3, exact rate depends on the pollution grade). VAT alone is 18% from 2025-01-01.
3. Run scripts/vehicle-decision.py: CIF ≈ $31,500, combined tax ≈ $31,500-$36,000, total landed ≈ $63k-$67k + ~$1,200 broker. Local Toyota hybrid ~$50k. Ship loses by $13k-$17k unless the local trim is meaningfully lower.
4. Misrad HaTachbura imposes a 12-month bealut-transfer restriction on every personally-imported vehicle. Plan to keep the vehicle at least 12 months.

### Example 3: 6-year hold trap

> User: "חזרתי לפני 4 שנים, ייבאתי מקרר ומכונת כביסה בפטור. עכשיו רוצה לעבור דירה ולקנות מקרר חדש בארץ. צריך לשלם משהו?"

Response framework:
1. Selling/transferring the duty-free fridge inside the 6-year hold triggers tax payback.
2. If user keeps the original in personal use AND buys a new one at full tax, no penalty.
3. If user sold/gave away the original: tax payback + interest, computed at Meches.
4. The re-claim window opens at year 6 from entry, not from sale date.

## Bundled Resources

- `references/domain-checklist.md`: authoritative sources, must-cover and should-cover facts, last-verified dates.
- `references/vehicle-import-benefit.md`: eligibility, age window, lack of purchase-tax exemption, citations.
- `references/household-shipment-rules.md`: 2-shipment basket, 9-month window, item-by-item caps, 6-year hold.
- `references/customs-timeline.md`: day-by-day from entry to year 6.
- `scripts/vehicle-decision.py`: side-by-side ship-vs-sell worksheet.

## Recommended MCP Servers

None directly applicable.

## Gotchas

1. **Returnees are NOT olim.** Returnees get 2 shipments, not 3.
2. **No purchase-tax exemption on vehicles for returnees.** Combined tax ~116% of CIF for FTA-origin passenger cars (gov.il personal_import_of_vehicles_guide ch. 3). The 48-month age window is the only benefit.
3. **Vehicle 12-month bealut-transfer restriction.** Misrad HaTachbura imposes a 12-month hold on every personally-imported vehicle. Nahal 416 is the early-release procedure.
4. **Vehicle 9-month window ≠ household 9-month window.** Separate procedural clocks under different takanot.
5. **Permanent-return entry, not tourist visit, anchors D.**
6. **9-month clock starts on entry**, not on certificate issue.
7. **6-year hold has teeth.** Selling a duty-free fridge in year 3 triggers tax payback.
8. **Spousal anti-stacking.** Cannot re-claim what spouse released duty-free within 6 years.
9. **"Type" is clerk-judgment.** Borderline items: ask Meches in writing before shipping.
10. **Mail packages count** against the 2-shipment quota if they contain household goods.
11. **Consolidate to save money.** Meches counts shipments by Bill of Lading; two lifts combined into one container = one shipment.
12. **Vehicle equipment-level refund is not automatic**, claim it back at Meches with documentation.
13. **Insure at full value INCLUDING taxes**, undervalued claims get rejected.
14. **Restricted-permit items** (drones, comm gear, weapons, lasers, e-scooters, plants, pets) need a separate import permit from the relevant ministry before shipping.
15. **Inheritance items** travel under their own customs basket, not the 2-shipment household cap.

## Reference Links

| URL | Topic |
|---|---|
| https://www.gov.il/he/pages/customs-guide-for-returning-residents | Customs guide for returning residents (Israel Tax Authority), updated 18.05.2026 |
| https://www.gov.il/he/service/request-for-entitlement-exemption-for-returning-resident-student | Open a customs entitlement file online |
| https://www.gov.il/he/pages/personal_import_of_vehicles_guide | Personal vehicle import guide (Israel Tax Authority) |
| https://www.gov.il/he/departments/guides/personal_import_of_vehicles | Personal vehicle import (Misrad HaTachbura) |
| https://www.kolzchut.org.il/he/יבוא_אישי_של_רכב_לתושבים_וסטודנטים_חוזרים | kolzchut, personal vehicle import for returnees (updated 10.12.2025) |
| https://www.kolzchut.org.il/he/פטור_ממס_קניה,_מע"מ_ותשלומי_מכס_לתושב_חוזר_ולסטודנט_חוזר_בייבוא_חפצי_בית | kolzchut, customs exemption for returnee household goods (updated 02.03.2025) |

## Troubleshooting

- **gov.il URLs return 403 to scrapers**: they load fine in a browser; use kolzchut mirrors as fallback.
- **Meches clerk insists on the certificate**: escalate via 1299 hotline.
- **Auto-approval fails**: bring proof of foreign residency to the in-person appointment.
- **Customs broker quotes different numbers**: trust the broker on the actual filing; this skill is for planning.
- **Already shipped 3 shipments**: the third clears at full tax; surface the lesson.
