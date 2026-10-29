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

## Legal notice

This is a free information tool operated by an AI model. It explains customs and import rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a customs agent or tax adviser. The output is not a filed customs declaration and not a professional opinion, but an explanation and a draft only. An AI model may err, omit data, or present a wrong conclusion.

A declaration to the customs authority is a legal document, and a false declaration carries liability. Any text this tool produces is therefore an automatic draft for your personal preparation only, to be checked with a customs agent or with the Tax Authority before filing. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and all use of its output is the user's sole responsibility.


## Problem

Returnees routinely lose money on the trip back. They miss the 9-month customs window, conflate their 2-shipment basket with the oleh 3-shipment basket, ship 4 TVs when only 3 are duty-free, ship a car that will be over the age limit by the time it is registered, or ship a car expecting a purchase-tax break that does not exist. AI agents make this worse: training data conflates olim and returnees because both flows live under "personal import" at Meches. This skill checks each planned shipment against the basket, produces a ship-vs-sell vehicle worksheet, and builds a windows timeline so the user does not learn the rules by paying for a mistake.

## Instructions

### Step 1: Confirm customs status before quoting any number

Customs definitions are NOT the same as Misrad HaAliyah definitions. Ask:

- **Returning resident (תושב חוזר) for customs**: Israeli resident, abroad **2 years or more**, returning permanently. Also covers second-time olim and entrants the Israel Tax Authority specifically classifies as returnees.
- **Returning student (סטודנט חוזר)**: Israeli resident abroad **18+ months** who studied full-time **2 consecutive academic years** at a recognized institution, or earned a degree there. Not recognized if they return more than **6 months after finishing studies**, or after receiving the degree.
- **There is no "vatik (10-year)" customs basket.** The 10-year vatik threshold lives in income-tax world (Section 14). Meches only knows "returnee". Abroad 12 years gets the same customs basket as abroad 2 years. The tax-planner sister skill handles the 10-year math.
- **Year-of-absence rule**: a year of absence (counted from the day after leaving) still counts if the user visited Israel up to **4 cumulative months** in that year. Exceed 4 months in a single absence-year and that year does NOT count toward the 2-year or 18-month threshold. Returnees with regular visits often misread this as "no visits allowed."
- **Permanent-return entry vs. tourist visit**: the 9-month customs clock anchors to the **permanent-return entry**, NOT to an earlier tourist visit. Ask which trip is the permanent move; that is D in the timeline.
- **Non-Israeli spouse trap**: the goods and every import document (Bill of Lading, declaration, invoices) must be in the **returnee's** name. Goods shipped in a non-Israeli spouse's name are not covered by the returnee basket. Common failure mode: a dual-citizen family signs the moving contract in the non-Israeli spouse's name and the BL inherits it. Verify the BL name BEFORE the container ships.
- Abroad less than 2 years (or less than 18 months as a student): NOT a returnee for customs; the regular Israeli-resident personal-import rules apply. Stop and hand off.

The Misrad HaAliyah תעודת תושב חוזר is helpful but NOT required to open the customs file, which is opened on a separate Meches form. The user can start the customs file in parallel.

### Step 2: The household-shipment basket (returnees, NOT olim)

| Item | Returnee cap (per family) |
|---|---|
| Number of shipments | **2 shipments** (NOT 3 like olim) |
| Window to receive shipments | **9 months from the day of return** to Israel, NOT extendable |
| TV sets | up to **3** total |
| Personal computers | up to **3** total |
| Other electrical / electronic appliances | **1 per type** (1 fridge, 1 dishwasher, 1 washer, 1 dryer, 1 oven, 1 microwave, etc.) |
| Major furniture items | **1 per type** |
| What counts as household goods | goods of the kind used in a home; NOT permanent-installation items (plumbing, building materials, tiles, wallpaper, marble) |
| Hold period | items must remain in the returnee's own use in Israel for at least **6 years**; selling, transferring, or destroying inside the window triggers tax payback |
| Re-claim of same item type | only after the returnee has spent **6 years in Israel** since the prior duty-free release of that item type |
| Spousal anti-stacking | cannot re-claim what a spouse already released duty-free unless 6 years passed AND they were not spouses at the time of that release |

A household item from the list above brought as accompanying luggage on the entry day does NOT count as one of the 2 shipments and is duty-free, but must be declared on the red channel.

A mail package containing household goods DOES count as one of the 2 shipments. Clothing-and-footwear-only mail packages are exempt and do not count if they arrive within 30 days before entry, on the day of entry, or within 3 months after entry.

**Consolidate where possible.** Since the cap is two shipments, combining planned lifts into one shipment leaves the second slot free for a later package. Ask the forwarder and broker how Meches will count the lifts before booking.

The only Israeli-made household item that can currently be bought tax-free from an authorized Israeli manufacturer instead of shipped is an **air conditioner** (gov.il notes authorized manufacturers exist for air conditioners only).

### Step 3: Accompanying luggage, tools, and restricted items

On the entry day, every entrant aged 2+ may bring duty-free:

- Clothing, footwear, personal toiletries, in customary travel quantities.
- Other items for own use or as a gift, up to **$200** value per entrant. Not poolable across family members, and above $200 the user pays tax on the FULL value of the item, not just the excess. Within the $200: mixed food up to 3 kg total, no single food type over 1 kg.
- Entrants aged 18+: up to 1 liter spirit + 2 liters wine + 250 ml alcohol perfumes + 250 g tobacco / 200 cigarettes.

The exemption applies only to items carried on the same vehicle (flight) as the entrant. Anything beyond it means the red channel ("מסלול אדום"). Some items may not be imported at all; point the user to the gov.il chapter "פריטים שייבואם אסור" before packing.

**Tools of the trade and business equipment** have their own chapters, outside the household basket:
- **Hand-carried work tools** (customs item 84.67) for the returnee's profession, up to **$1,650** total value, duty-free.
- **Machines and equipment to set up the returnee's own business** (industry, craft, agriculture), up to **$36,000 FOB** (the $1,650 of tools included), subject to approval by the Tax Authority director and a bank guarantee for the taxes. Refer to a broker.

**Restricted-permit items** need a permit from the relevant authority on top of any customs benefit. An import licence (רישיון יבוא) must be obtained BEFORE the item arrives; an import approval (אישור יבוא) can come after arrival, but the item is held until it is shown. Frequent cases (gov.il list): drones and communications products (Misrad HaTikshoret, 03-5198282), plants and seeds (Misrad HaChaklaut plant protection, 03-9681587), pets (Misrad HaChaklaut veterinary services, 03-9485461), weapons and weapon parts (Ministry of Internal Security, 077-2324444), helmets, child car seats, car spare parts, e-scooters and e-bikes (Misrad HaTachbura, \*5678), laser pointers and meters (Misrad HaKalkala, \*6680). Tell the user to check the gov.il personal-import calculator (מחשבון ליבוא אישי) for the specific item BEFORE shipping. Pet entry requirements are in `references/household-shipment-rules.md`.

### Step 4: Vehicle import, the math that surprises most returnees

Returnees do NOT get a purchase-tax / VAT / customs-duty exemption on a personally-imported vehicle. The ONLY benefit is an extended age window:

| Eligibility | Max vehicle age from manufacture, **at registration in Israel** |
|---|---|
| Regular Israeli resident, personal import | **24 months** |
| Returning resident or returning student | **48 months** |

**The age is measured at Israeli registration, not at purchase, shipping, or clearance** (Takana 282, as quoted in Misrad HaTachbura procedure 02/12). Shipping, clearance, inspection, and registration take real time, and Misrad HaTachbura does not accept an import-licence application when fewer than **45 days** remain before the last date the car can be registered, and will not approve one with fewer than **7 working days** left. A car that is 46 months old on the day it sails is very likely lost. Count backwards from the 48-month date, not forwards from today.

Other conditions (ITA guide, chapter 2): the vehicle is approved for import by Misrad HaTachbura, the importer holds a valid Israeli driving licence for the vehicle category, is 17+ on the entry day, and the vehicle is imported within **9 months from the day of entry**. A returnee may APPLY with a foreign licence but must show a valid Israeli licence when the car is released from customs (procedure 02/12 s.12). Procedure 02/12 also words the 9 months as running from the date the returnee rights were granted; plan by the entry date, which is the earlier and safer anchor. The import licence must be issued BEFORE the car is shipped; a licence obtained after arrival is an offence that can carry a ransom payment (כופר).

**One vehicle under returnee rights.** Procedure 02/12 s.3: a returnee may import ONE vehicle under returnee rights. The ITA guide also limits regular residents to one personally-imported vehicle per 12 months (procedure 02/12 words it as one per calendar year). A couple where both spouses independently qualify should confirm each spouse's entitlement with Meches and Misrad HaTachbura before ordering a second car.

**Vehicle class and weight:** for personal import, "רכב" is a passenger motor vehicle up to **3,500 kg** or a motorcycle for own use (ITA guide).

**Documents at clearance (ITA guide):** Form 21 importer declaration, original bill of sale, original vehicle licence with export-country customs verification, import licence, valid driving licence, Bill of Lading, freight and insurance invoices, Form 139 with proof of purchase, and the money transfers abroad. By origin:
- **US**: the TITLE plus a copy of its back, a photo of the manufacturer's identification label, and a CARFAX report.
- **Europe**: the registration document (BRIEF), COC, and test, plus the manufacturer DATA CARD.

**US- and Canada-spec cars are importable.** Misrad HaTachbura states a car built to US federal or Canadian standards may be imported, even if manufactured outside the NAFTA countries. Do NOT tell a returnee a US car needs EU / EURO 6d certification; that rule does not exist. What a North-American car DOES need (procedure 02/12 s.7.2, s.15, s.16):
- the model is approved for sale in the US or Canada;
- ESP / stability control and a **metric speedometer**;
- an emissions-data letter from the brand's official Israeli importer, the manufacturer, or an authorized dealer. **Without it, Misrad HaTachbura assigns the highest pollution grade**, which turns the green-tax reduction into a surcharge (see the tax paragraph below).

**Hard-rejection rules (the shipment-killers):**

- **Right-hand drive.** A Misrad HaTachbura procedure states it is forbidden to import a car manufactured after 1960 with the steering wheel on the right. UK, Japan, Australia, South Africa, India, Singapore, Hong Kong, Cyprus and Malta cars are RHD by default. A returnee from London or Tokyo who ships a paid-off RHD car learns at port that it cannot register.
- **Salvage / total loss, or a reported accident.** A car declared SALVAGE or TOTAL LOSS abroad is not allowed in, and the procedure requires that the car has had no accident reported to the authorities. Check the CARFAX before buying or shipping.
- **Structural modifications.** No change after manufacture to dimensions, weights, tyre sizes, drive type, number of axles, engine model, displacement, or power.
- **Fuel.** Only petrol, diesel, petrol/diesel hybrid, or electric. LPG / CNG conversions are disqualifying.
- **ESP** must be present, verified from the technical specification and the dashboard indicator lamp. Many pre-2012 or classic cars lack it.
- **Payment.** The importer must pay the seller abroad personally, not through a third party, and pay the taxes personally (Car Services Licensing Law s.34).
- **A make with no official Israeli importer.** Procedure 02/12 s.10 expects the manufacturer to have a valid contract with an authorized Israeli importer. Otherwise (s.11) the application needs an undertaking from the manufacturer or its main agent to provide maintenance, warranty, recall repairs and parts, an undertaking from a licensed garage, and a lawyer-verified affidavit; s.17.1 adds a licensed garage's service approval. Section 14ב exempts EVs and hybrids from s.11 (and from s.26, the Takana 309 inspection section). A US-market make with no Israeli importer can fail here, so check BEFORE buying or shipping.
- **Affidavit.** Every application carries an affidavit signed before a lawyer (s.21); a car that needs a lab test in Israel also needs a lawyer-signed undertaking to re-export it if it fails (s.7.3.1). Users applying from abroad should line up a lawyer early.

Confirm the exact paperwork with the Misrad HaTachbura import unit (\*4515; from abroad +972-3-9695678) before booking freight. The import-licence application costs a fee and is handled within 21 working days at most.

**The vehicle 9-month window is a separate clock** from the household 9-month window. Both run from D, but missing one does not affect the other. Treat them as independent deadlines in any timeline.

**12-month ownership-transfer restriction**: every personally-imported vehicle, returnee or not, carries a 12-month ownership-transfer restriction counted **from its registration in Israel** (procedure 02/12 s.20). Misrad HaTachbura publishes a separate procedure ("נוהל הגשת בקשה להסרת הגבלת העברת בעלות מרכב ביבוא אישי") for applying to remove it early. Neither the Tax Authority guide nor the Misrad HaTachbura procedure sets any longer hold (such as 4 years) on a returnee's car; do not import oleh-benefit rules here.

**Registration (מכון רישוי, per Takana 309).** After clearance, the car gets a temporary licence valid for 48 hours, during which it must be registered and licensed (Takana 282(a)(3)). It must pass the Misrad HaTachbura standards checks, a licensing test at a מכון רישוי appointed to register personal imports, and installation of safety systems. gov.il lists the appointed institutes. Procedure 02/12 s.14ב says s.26 (the Takana 309 inspection section) does not apply to an EV or hybrid, so an EV or hybrid importer should confirm with \*4515 which inspection their car still needs. Budget this separately from the broker fee.

**Taxes in 2026.** The tax is calculated at the exchange rate on the payment day, on the customs value. **The customs value is not today's resale price**: it is the declared value, based among other things on the price in the bill of sale, plus freight and insurance, if the assessor accepts it as reasonable and genuine; otherwise the assessor sets it from the Israeli price list less use depreciation, and the importer has 30 days to respond in writing. For a car owned for years, ask the broker which figure the assessor will use before running the worksheet. The parameters (Customs Book, as of 29.10.2026):
- Purchase tax **83%** for a passenger car up to 3,500 kg, including hybrids and plug-in hybrids; **48%** for an EV.
- Green tax: a fixed NIS amount subtracted from or added to the purchase tax by green score, from a **14,523 NIS** reduction for the cleanest grades to an **8,690 NIS** surcharge for the most polluting. Because it is a fixed amount, cheaper clean cars get a much lower effective rate.
- EV cap: the EV tax may not fall more than **22,000 NIS** below the regular method. Above a value of roughly 104,000 NIS the EV starts paying more than the headline rate, and the gap grows with value (about 89% of value at 159,000 NIS). The ITA guide prints a larger EV green reduction (19,498 NIS) that the Customs Book table lacks; if it applies, the threshold is higher, so confirm with a broker.
- Customs duty: none for a car made in a free-trade-agreement country and shipped directly or via another party to the same agreement; otherwise duty applies.
- VAT **18%** on the value plus duty plus purchase tax.

The ITA guide's headline totals (tax as a share of the vehicle value, before the green adjustment): about **116%** for a passenger car under a trade agreement, **131%** otherwise; about **75% / 87%** for an EV. After registration, a safety-equipment refund (250 to 2,400 NIS by equipment level) can be claimed at the customs house with the vehicle licence. **For 1.1.2027 nothing is enacted yet** as of 29.10.2026: press reports a possible extension of the EV benefit and a new green-tax formula. Tell the user the rate is the one in force on payment day and to re-check if clearance falls in 2027.

**The ship-vs-sell decision** usually pencils to "sell abroad and buy locally" because the returnee pays full Israeli tax. Shipping makes sense when the car is paid off and the user is attached to it, the model is rare in Israel, or the local equivalent is meaningfully more expensive. Run `scripts/vehicle-decision.py` for the worksheet; it needs the exchange rate and, ideally, the green score from the import licence.

### Step 5: Open the customs entitlement file (תיק זכאות)

1. Online: fill the returnee-status form at [gov.il, בקשת זכאות לפטור לתושבים חוזרים](https://www.gov.il/he/service/request-for-entitlement-exemption-for-returning-resident-student). The system opens the file automatically; no visit or documents in the happy path.
2. If the system does not approve it, visit a customs house with your ID + passport, your spouse's ID + passport, and the Misrad HaAliyah תעודת תושב חוזר if you have it. A customs employee checks the entitlement.
3. Returning students: bring a certificate from the institution of 2 academic years as a regular student, or of the degree.
4. **Deposit**: a returnee whose status is not yet determined may have to deposit the applicable taxes on entry (Kol-Zchut). It is refunded once the status and entitlement are approved, and is used to pay the taxes if the user does not apply within the 9 months or is refused. Kol-Zchut also lists proof of an independent household (property ownership or a valid lease) among the documents for the in-person route.

If a clerk demands the certificate, the user can wait for Misrad HaAliyah or call the **Tax Authority national service centre \*4954** (Sun-Thu 08:15-15:45; extension 1 includes parcel-post customs). For vehicle import-licence status, **\*4515** (Misrad HaTachbura).

### Step 6: Currency on the body (anti-money-laundering)

Section 9 of the Anti-Money-Laundering Law requires a report on entry or exit when funds exceed:

- **50,000 NIS** at air / sea borders
- **12,000 NIS** at land borders

Travelling with another person, even family, does not remove the duty, and jointly owned funds split between travellers below the threshold must still be reported if the total is above it. Unreported funds can be seized and a criminal investigation opened, ending in a fine or an indictment with up to 6 months imprisonment.

### Step 7: Build the timeline

Hand the user `references/customs-timeline.md` or compute it inline. Anchor everything to **D = date of permanent-return entry** (NOT a prior tourist visit, NOT the certificate date):

- Before D: get the vehicle import licence BEFORE the car sails; check the car's 48-month date.
- D + 0: red channel for anything over the personal allowance; report currency if applicable; deposit if required.
- D + 0 to D + 30: open the online entitlement file if not already done.
- D + 0 to D + 9 months (household clock): both household shipments must arrive.
- D + 0 to D + 9 months (vehicle clock): the vehicle must be imported, AND registered before it turns 48 months.
- Registration to registration + 12 months: ownership-transfer restriction on the vehicle.
- D + 0 to release + 6 years: household-goods hold period; no selling, transferring, or destroying duty-free items.
- 6 years in Israel after release: re-claim window opens for the same item types.

### Step 8: When to hand off

- Process / kupat cholim / Form 628 / driver's license → `israeli-returning-resident-navigator`.
- Section 14 10-year exemption math / Form 1348 → `israeli-toshav-chozer-vatik-tax-planner`.
- Oleh chadash 3-shipment basket → `israeli-aliyah-customs-shipment-planner`.
- People planning to leave Israel → `israeli-relocation-abroad`.
- Actual filing of the declaration, HS codes, the safety-equipment refund, disputes with the assessor → licensed customs broker (סוכן מכס). This skill is a planning aid, not a substitute for a broker.

## Examples

### Example 1: Two-shipment family with one TV too many

> User: "אני חוזרת אחרי 7 שנים בסיליקון ואלי, יש לי בעל וילד. אנחנו מתכננים לשלוח 4 טלוויזיות (סלון, חדר שינה, חדר עבודה, חדר ילדים), מקרר, מייבש, מקפיא נפרד, שני מחשבים שולחניים, ולפטופ אחד. כמה משלוחים? מה לזרוק?"

Response framework:
1. Returnee customs status: yes (7 years > 2 years), but it does NOT change the basket.
2. Shipments: 2 max.
3. Cap: 3 TVs, so the 4th is taxable: sell it, leave it, or pay tax.
4. 1 fridge OK, 1 dryer OK. **Whether a separate freezer is its own "type"** is the clerk's call; ask Meches in writing before shipping.
5. 2 desktops + 1 laptop = 3 PCs, right at the cap.
6. Send the user to the online entitlement form before shipping.

### Example 2: Ship the car or sell it?

> User: "יש לי טויוטה הייבריד 2023 עם 40 אלף מייל. שווייה בארה״ב כ-28 אלף דולר. עלות משלוח לישראל כ-3,500 דולר. כדאי לשלוח?"

Response framework:
1. Age: count to the expected Israeli registration date. A car built in mid-2023 and registered in early 2027 is about 43 months, inside 48 but with little slack. Get the exact build date from the door-jamb label and the import licence BEFORE booking.
2. **No purchase-tax exemption.** A hybrid pays the passenger-car rate (83%) minus its green-score reduction, plus 18% VAT. The trade-agreement treatment depends on where the car was MANUFACTURED and on direct shipment, not on where it was bought: a Toyota sold in the US may have been built in Japan, which changes the duty. Without the emissions letter from the Israeli Toyota importer, the car gets the highest pollution grade.
3. Run the worksheet: `python3 scripts/vehicle-decision.py --car-value-usd 28000 --shipping-usd 3500 --manufacture-date <from the label> --local-price-usd 50000 --ils-per-usd <today's rate> --vehicle-class hybrid --green-score <from licence>`, using the value the assessor will accept rather than the resale price. At an illustrative 3.70 NIS/USD, a green score of 120, and a car built in the US and shipped directly, the tax is about 117,991 NIS (101% of CIF) and the landed cost about $64,600 against a $50,000 local price; with no emissions letter, about $72,000; if it was built in Japan (`--origin other`), about 116% and $69,400. Shipping loses unless the model is unavailable locally.
4. Surface: 12-month ownership-transfer restriction from registration.

### Example 3: 6-year hold trap

> User: "חזרתי לפני 4 שנים, פתחתי תיק זכאות וייבאתי מקרר ומכונת כביסה בפטור. עכשיו אני רוצה לעבור דירה ולקנות מקרר חדש בארץ. צריך לשלם משהו?"

Response framework:
1. Selling or transferring the duty-free fridge inside the 6 years triggers tax payback. Ask: did the user sell it, give it away, or keep it?
2. If the original fridge stays in the user's own use (moves to the new home), there is no problem; they may ALSO buy a new fridge at full Israeli price. The hold rule is about the duty-free unit.
3. If sold or given away: taxes are due; refer to Meches for the amount.
4. A NEW duty-free fridge is only possible after 6 years in Israel from the previous release.

## Bundled Resources

- `references/domain-checklist.md`: authoritative sources, must-cover and should-cover facts, out-of-scope list.
- `references/vehicle-import-benefit.md`: eligibility, the age-at-registration rule, 2026 tax parameters, documents, ship-vs-sell guide.
- `references/household-shipment-rules.md`: 2-shipment basket, 9-month window, item caps, 6-year hold, spousal anti-stacking, pet entry rules.
- `references/customs-timeline.md`: day-by-day from entry to year 6.
- `scripts/vehicle-decision.py`: checks the age at registration (from the manufacture date) and the 45-day application cutoff, then computes duty, purchase tax (with green score or EV cap), and VAT, and prints a ship-vs-sell worksheet for passenger cars up to 3,500 kg.

## Recommended MCP Servers

None directly applicable. The Tax Authority does not expose an MCP / API. Customs questions: **\*4954** (Tax Authority national service centre). Vehicle import licence: **\*4515** (Misrad HaTachbura). Misrad HaAliyah and the תעודת תושב חוזר: **\*2994**.

## Gotchas

1. **Returnees are NOT olim.** The most common mistake is assuming the oleh 3-shipment basket. Returnees get 2 shipments.
2. **No purchase-tax exemption on vehicles for returnees.** Stop quoting "tax-free car import". Purchase tax 83% (EV 48%, capped), plus VAT 18%, plus duty for non-agreement origin. The 48-month window is the only benefit.
3. **The 48 months are counted at Israeli registration.** Agents compute the car's age today and call it eligible. Add the shipping, clearance, and inspection time, and remember the 45-day application cutoff.
4. **US cars are importable; EURO 6d is not required.** But a US car without the emissions letter is taxed at the worst green grade, and needs ESP and a metric speedometer.
5. **12-month ownership-transfer restriction**, counted from registration. Do not import longer oleh-style holds into a returnee answer.
6. **Vehicle 9-month window ≠ household 9-month window.** Independent clocks, both from D.
7. **Permanent-return entry, not a tourist visit, anchors D.**
8. **9-month clock starts on entry, not on certificate issue.** Returnees chasing the Misrad HaAliyah certificate first can burn months of the window.
9. **6-year hold has teeth.** Selling a duty-free fridge in year 3 makes the taxes due. Surface it on every timeline.
10. **Spousal anti-stacking.** An item type the spouse already released duty-free is not a fresh entitlement for the couple.
11. **The "type" definition is the clerk's judgment.** Ask Meches in writing before shipping borderline items.
12. **Mail packages count.** Household goods by post use one of the 2 shipments; clothing-only mail in the window does not.
13. **Insure at full value INCLUDING all taxes.** The gov.il guide requires insuring the goods "בערכם המלא, כולל כל המסים". Quote the full landed figure to the insurer.
14. **Restricted-permit items need their own permit,** and an import licence must exist before the item arrives.
15. **The safety-equipment refund is not automatic.** After registration, the user returns to the customs house with the vehicle licence to claim it.

## Reference Links

| URL | Topic |
|---|---|
| https://www.gov.il/he/pages/customs-guide-for-returning-residents | Customs guide for returning residents (Israel Tax Authority), updated 30.07.2026 |
| https://www.gov.il/he/service/request-for-entitlement-exemption-for-returning-resident-student | Online service: open a customs entitlement file (תיק זכאות) |
| https://www.gov.il/he/pages/personal_import_of_vehicles_guide | Personal vehicle import guide (Israel Tax Authority), updated 15.01.2026: conditions, tax table, green tax, documents |
| https://www.gov.il/he/pages/personal_import_of_vehicles | Personal vehicle import (Misrad HaTachbura), updated 22.09.2026: age at registration, US/Canada standards, ESP, salvage, 12-month restriction, procedures |
| https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/he/CustomsBook/Import/Rules?customsItemId=18359 | Customs Book, chapter 87 rules: purchase-tax rates, EV cap, green-tax table |
| https://www.kolzchut.org.il/he/יבוא_אישי_של_רכב_לתושבים_וסטודנטים_חוזרים | Kol-Zchut, personal vehicle import for returning residents and students |
| Kol-Zchut, search the page titled "פטור ממס קניה, מע"מ ותשלומי מכס לתושב חוזר ולסטודנט חוזר בייבוא חפצי בית" | Kol-Zchut, household-goods exemption and the deposit |
| https://www.gov.il/he/pages/ta-contact-us | Tax Authority contact page (\*4954) |
| https://www.nbn.org.il/life-in-israel/government-services/rights-and-benefits/benefits-for-toshavim-chozrim-returning-residents/ | Nefesh B'Nefesh, returning-resident benefits (returnees pay full vehicle tax) |
| https://shivatzion-support.freshdesk.com/en/support/solutions/501000223548 | Shivat Zion knowledge base for returning Israelis |

## Troubleshooting

- **gov.il pages return 403 to scrapers**: they load in a real browser. If an agent cannot fetch them, use the Kol-Zchut pages and the citations in `references/domain-checklist.md`, and say the figure was not re-checked live.
- **Meches clerk insists on the Misrad HaAliyah certificate although the online system handles it**: the user can wait for the certificate or call \*4954.
- **Auto-approval fails for a returnee who kept an Israeli address**: the gov.il guide only says exceptional cases go to the customs house; bring proof of the years abroad (passport stamps and foreign-residency documents) to that appointment.
- **A customs broker gives a different number than this skill**: the broker works from the live rates, the assessor's valuation, and the actual green score. Trust the broker on the filing; use this skill for planning BEFORE engaging one.
- **The user already shipped a third shipment**: it clears as a regular import at full tax; the goods still clear.
