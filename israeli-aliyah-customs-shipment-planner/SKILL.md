---
name: israeli-aliyah-customs-shipment-planner
description: "Plan the 3-shipment customs exemption for new olim (zchuyot olim): classify belongings as exempt or over-limit, flag the 3-TV / 3-computer / 5-phone / 25%-carpet / one-of-each-appliance caps, split inventory across shipment 1/2/3 within the 3-year window, and draft customs declarations. Use when user asks about olim shipping rights, teudat oleh customs benefits, meches olim, lift shipping plan, how many TVs can I bring, or how to split my aliyah shipment. Do NOT use for general aliyah absorption (sal klita, ulpan, Misrad HaKlita) - use israeli-aliyah-navigator instead."
license: MIT
compatibility: "Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex, Antigravity, Gemini CLI. Python 3.8+ for the planning script."
---

# Israeli Aliyah Customs Shipment Planner

## Legal notice

This is a free information tool operated by an AI model. It explains customs and import rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a customs agent or tax adviser. The output is not a filed customs declaration and not a professional opinion, but an explanation and a draft only. An AI model may err, omit data, or present a wrong conclusion.

A declaration to the customs authority is a legal document, and a false declaration carries liability. Any text this tool produces is therefore an automatic draft for your personal preparation only, to be checked with a customs agent or with the Tax Authority before filing. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and all use of its output is the user's sole responsibility.


## Problem

New olim (immigrants) to Israel may import household goods free of import taxes in up to three shipments within three years of receiving oleh status, but the rules are full of per-family caps (TVs, computers, appliances, carpeting) and a six-year personal-use rule that blocks resale or lending. Most olim pack by emotion, then discover at the port that a fourth computer or a second fridge triggers customs duty plus VAT plus purchase tax. This skill plans the split across three shipments, flags over-limit items before packing, and drafts a clean declaration per shipment.

## Instructions

### Step 1: Collect Aliyah Profile

Ask the user for the following before planning anything:

| Field | Why it matters |
|-------|---------------|
| Date oleh status was received | Starts the 3-year eligibility period. Usually the entry day; later if the status was granted after a stay in Israel (Tax Authority guide). |
| Status | Oleh (Law of Return, including those holding only a printed status confirmation), Ezrach Oleh, Katin Chozer and permanent residents are all entitled under the Tax Authority olim guide. Toshav Chozer (returning resident) is a different, narrower track (see below), and so is a SECOND-TIME oleh. Always ask: "Have you ever lived in Israel as a resident or made aliyah before?" |
| Age at aliyah and household | Concessions are generally granted to adults (18+) who maintain an independent household; a minor oleh gets only personal items needed right after aliyah, unless they enlist in the IDF within a year of entering at 17+ or start full-time higher education within 18 months and study for at least two consecutive years (Misrad HaKlita Guide for the New Immigrant, 2022 edition; confirm with customs). A single adult with no independent household yet (for example a lone soldier on base or on a kibbutz) should confirm with customs before shipping a lift; regular IDF service does not count against the 3 years, so the lift can wait until after discharge. |
| Household size | Caps are per family, not per person |
| Planned home area in Israel (sqm) and number of rooms | Carpet allowance (25% of the home area per NBN) and the air-conditioner/heater allowance (relative to the number of rooms) depend on it. Customs may ask for a rental or purchase contract. |
| Spouse's status, and whether the spouse already used benefits | Spouses share ONE set of benefits: the family gets the rights of the spouse with the broader entitlement, and spouses who received status at different times are together entitled to 3 shipments only, and the second spouse can bring capped items only if the first has not used the full cap. If a spouse used the capped-goods exemption BEFORE the marriage, the oleh gets that item type exempt only once 6 years have passed since the spouse's release. Customs will not approve either spouse without checking the other's passport (Tax Authority guide). Ask how many shipments and which capped items the spouse already used. |
| IDF / national service, full-time study, or 6+ months abroad | Can extend the 3-year window (see Step 3) |
| Previous customs concessions as a temporary resident (A/1) | Concessions already received as A/1 cannot be received again as an oleh (Misrad HaKlita guide) |

**Toshav Chozer (returning resident).** The Tax Authority returning-residents guide covers three groups: residents abroad 2+ years who return permanently, second-time olim (as defined in Ministry of Interior regulations), and others the Tax Authority classifies as returning residents. They may import household goods in **two shipments only, within 9 months of returning, and this period cannot be extended**, with the same 3-TV / 3-computer / one-of-each caps. The Misrad HaKlita guide adds that returning residents are not eligible for the oleh vehicle tax concession. Do not run the oleh 3-shipment plan for them; route to `israeli-returning-resident-navigator` and `references/returning-residents.md`.

The customs eligibility file is opened automatically from Misrad HaKlita data. If it was not (a fault, or status granted after a long stay with only a printed confirmation), open it with a customs officer or by email, presenting the Misrad HaKlita certificate and the foreign passport with the aliyah visa or an Israeli passport.

### Step 2: Classify Every Item

For each item on the user's packing list, tag it as one of:

| Tag | Meaning | Action |
|-----|---------|--------|
| exempt | Household item within per-family cap | Include in a shipment |
| over-limit | Item count exceeds cap (e.g., 4th TV, 2nd fridge) | Duty + VAT + purchase tax applies; recommend sell/gift before aliyah |
| verify | Allowance depends on facts customs decides (AC units vs rooms, hand tools, business equipment, an unrecognised item) | Confirm with the customs office or a licensed customs broker before packing |
| non-household | Office equipment, commercial goods, permanently installed fittings | Not covered by the household exemption |
| restricted | Firearms, plants, pets, certain medications, drones, food; cannabis is never importable | Separate permit path, see below |
| vehicle | Car, motorcycle | Separate vehicle benefit, outside this shipment plan |

Per-family caps to enforce during classification. The primary source is the Israel Tax Authority import-tax guide for new olim; rows marked NBN come only from Nefesh B'Nefesh:

| Category | Cap per family |
|----------|----------------|
| Televisions | Up to 3 (Tax Authority) |
| Personal computers | Up to 3 (Tax Authority) |
| Other electrical and electronic appliances (fridge, oven, washing machine, dryer, microwave, etc.) | One of each type (Tax Authority) |
| Major furniture items | One of each type (Tax Authority) |
| Cell phones | NBN lists up to 5 per family; the Tax Authority guide does not list a phone count. Importing more than 5 needs Ministry of Communications approval (NBN). |
| Carpeting | NBN: up to 25% of the area of the oleh's home in Israel. Not in the Tax Authority guide. The exemption excludes permanently installed equipment such as flooring and wall coverings, so wall-to-wall carpet may be refused; confirm with customs. |
| Air conditioners, fans, heaters | NBN: relative to the number of rooms in the new home. Separately, the approval lets the oleh BUY an Israeli-made air conditioner VAT-free, up to two units or one mini-central unit (Tax Authority). |
| Hand-held work tools | Total value up to USD 1,650, for the oleh's professional needs, of the hand-held type (customs tariff item 84.67), as determined by the customs officer (Tax Authority) |
| Machinery and equipment to set up a business | Up to USD 36,000 FOB in total, INCLUDING the hand tools, subject to the Director's approval, used and kept on the business premises, against a bank guarantee for the taxes (Tax Authority) |
| Books, clothing, linens, kitchen utensils, pictures, decorations, media, personal effects | No numeric cap, household use (NBN). Anything with a motor or heating element that customs would read as an appliance falls under one-of-each; when in doubt classify it as an appliance. |
| Permanently installed equipment (plumbing, building materials, flooring, wall coverings such as wallpaper, tiles, marble) | NOT exempt (Tax Authority) |

Customs releases goods only in the name of the entitled person (or their customs agent holding a power of attorney), and only in reasonable quantities for personal use.

**Accompanying luggage on the aliyah flight.** An oleh who arrives with an aliyah visa and receives status on the day of entry may bring household goods as accompanying luggage, on the same flight, free of import taxes and **in addition to** the 3 shipments (Tax Authority). Anything beyond the standard traveller allowance below requires the Red lane, a declaration and a request for the oleh exemption. Standard Green-lane allowance per entrant:

| Category | Allowance | Notes |
|---|---|---|
| Clothing, footwear, personal toiletries | Types and quantities customary for travellers' luggage | No dollar value cap |
| Spirits / wine | 1 litre spirits + 2 litres wine | Each entrant aged 18+ |
| Alcohol-based cosmetics (perfume) | Up to 1/4 litre | Each entrant |
| Tobacco | 250 grams, or 200 cigarettes (one carton) | |
| Other items for own use or as gifts | Up to USD 200 per item, each entrant aged 2+ | Includes up to 3 kg of food, no more than 1 kg per type. Allowances of several entrants cannot be pooled for an item worth more than USD 200. |

**Postal packages.** A postal package of household items counts as one of the 3 shipments. A package containing ONLY clothing and footwear is exempt and does not count as a shipment if it arrives from 30 days before receiving status up to 3 months after (Tax Authority). To release a package with oleh benefits, NBN describes sending the Customs Exemption Request Form with copies of the teudat oleh and the teudat zehut with sefach to customs. With couriers (UPS, FedEx, DHL), check before shipping that you can clear with your oleh benefit yourself: NBN warns that in most cases, if the courier pays the customs fee on your behalf, you will NOT get a refund.

**Cash and cannabis.** Any cash above NIS 50,000 carried on the aliyah flight must be declared; it is not taxed (NBN). Cannabis-based products or medication cannot be imported, for any reason (NBN).

**Pets (dogs and cats).** A separate Ministry of Agriculture track, never a shipment slot, and the Tax Authority notes that aliyah with animals requires an import licence application BEFORE aliyah. For the exemption-from-licence route the Ministry requires: up to two dogs or two cats a year, the animal over 5 months old on arrival, an owner over 18 travelling on the same flight, the animal in the owner's possession for at least 90 days before the flight, not a restricted breed, and not intended for sale or transfer. The Ministry's veterinary certificate (valid 10 days) requires an ISO 11784/11785 microchip, a rabies vaccination no more than one year and no less than 30 days before arrival (some origin countries excepted), and, where required, a rabies antibody titer of at least 0.5 IU/ml from an EU- or WOAH-approved laboratory. If any exemption condition fails (the animal is not on the owner's flight, is 5 months or younger, is a third animal that year, or has been with the owner under 90 days), the route is an import LICENCE, which must be obtained before arrival: obtaining one after the animal arrives is an offence (Tax Authority). If the animal travels as cargo on the owner's own flight, ask the Ministry's import unit which route applies. For a dog or cat born with a short tail, imported under a licence, the Ministry's forms include a veterinarian's declaration that the tail was not docked. Route the user to the Ministry's dog-and-cat import page for the current breed list and forms.

Run `scripts/plan_shipments.py` to do this classification automatically from a JSON inventory. Fill the `type` field on `other_appliance` and `furniture` rows (the one-of-each rule is applied per type), and when a spouse already used benefits, pass `--shipments-used` and list the capped items the spouse already brought as rows with `"already_imported": true`, so they count toward the family cap first; the output lists them once, under "counted_toward_caps_already_imported_by_spouse", and leaves them out of the shipment plan and every declaration total.

### Step 3: Propose a 3-Shipment Split

Rule of thumb for splitting within the 3-year window:

1. Accompanying luggage (aliyah flight, only for an oleh arriving on an aliyah visa who receives status on the day of entry): suitcases of household items, declared in the Red lane. Not a shipment. Household items brought on a LATER trip into Israel do count as a shipment.
2. Shipment 1 (arrival): essentials only. Beds, a basic kitchen, enough clothes for a few months, one laptop, one TV.
3. Shipment 2 (3-9 months after aliyah): the bulk lift. Remaining furniture, appliances (one of each), books, kitchenware, second computer/TV if needed.
4. Shipment 3 (reserve, before the window closes): whatever the family realised they need later.

Shipments may come from any country, not only the country of aliyah (NBN). Container math: if a sea shipment is larger than a full container it counts as two shipments, unless both come on the same ship and are cleared through customs at the same time (NBN). Flag this in the plan.

**Extending the 3-year window** (Tax Authority, the only grounds):
- **Regular IDF or national service** during the eligibility period: the service period (not career service) does not count, and the remaining period resumes after discharge.
- **Higher education**: studies begun within 18 months of entry as a full-time student at a recognised institution, continuous and no longer than 5 years (longer possible for medicine and law): the period is extended by one year from the end of studies. This extension is not frozen, even if the student leaves Israel right after.
- **6 or more consecutive months abroad** during the eligibility period (does not apply to a Katin Chozer): the time abroad does not count; extend via the online form, no visit to customs needed.
- The eligibility period can be extended up to 6 years, longer in some cases. Beyond that, an exceptions committee can review special cases (goods received before status was completed, or arriving after 3 years for special reasons).

### Step 4: Draft the Per-Shipment Declaration Worksheet

For each shipment, produce a worksheet the user or broker files from:

- Shipment number (1 / 2 / 3)
- Expected arrival port (Haifa, Ashdod, Ben Gurion air cargo)
- Freight mode (air, sea LCL, sea FCL 20-foot, sea FCL 40-foot)
- Inventory list grouped by category (furniture, appliances, electronics, personal)
- Declared value per unit and line total (the script reads `declared_value` as per unit)
- Flag column: exempt / over-limit / verify / non-household
- Totals: total items, over-limit count, items needing verification

List every item in detail. The returning-residents guide requires a detailed list of everything in the luggage and insurance at full value including all taxes; treat both as good practice for olim too.

Do NOT fabricate NIS amounts for duty or purchase tax on over-limit items: rates come from the customs tariff and change. Tell the user to get a pre-clearance quote from a licensed customs broker (amil meches) for any over-limit item.

### Step 5: Advise on the 6-Year Personal-Use Rule

Goods imported or bought under oleh rights must be for the oleh's own use in Israel for at least 6 years from their release or purchase (for a vehicle: 4 years of personal use after release, a restriction on use and sale after release, not a rule about the car's age). They may not be passed to anyone else's use before the period ends, temporarily or permanently, for payment or free; doing so breaches the exemption conditions (Tax Authority). Proof that the items are used by the oleh may be required even when no guarantee was given (Misrad HaKlita guide). Plan around it:

- Do not import items you plan to resell, lend or give away within 6 years.
- Do not use the exemption for relatives who live outside your household.
- Before transferring an item early, ask the customs office what taxes would be owed; do not estimate it yourself.

### Step 6: Write the Checklist Back to the User

Output a clean 3-column table: shipment number, items, flags. Include a short list of next actions: (a) confirm the customs eligibility file was opened, (b) choose a customs broker or self-clear, (c) get insurance valuations, (d) book freight, (e) pre-check anything flagged over-limit or verify.

## Examples

### Example 1: Single Software Engineer from the US

User: "I'm making aliyah in June, solo, from Boston. One bedroom I'll rent. I have 2 laptops, 1 desktop, 1 TV, no furniture, lots of books, espresso machine. Plan my shipments."

Actions:
1. Profile: Oleh, adult with an independent household of 1, renting, sea LCL.
2. Classify: 3 computers total (2 laptops + 1 desktop) = at the Tax Authority cap of 3, exempt. 1 TV within the cap. Espresso machine is one appliance (OK). Books and clothes are personal effects (OK).
3. Split:
   - Accompanying luggage: 1 laptop and essentials (Red lane if beyond the traveller allowance).
   - Shipment 1 (air, around arrival): clothes and personal effects.
   - Shipment 2 (sea LCL, 2 months after arrival): other laptop, desktop, TV, espresso machine, books.
   - Shipment 3: reserve.
   This is also the script's starting split (personal items in 1, everything else in 2). A user who can wait may merge shipments 1 and 2 to keep two in reserve.
4. Declaration: 2 shipments used, 1 in reserve. Nothing flagged.
5. Timing note: the 6-year rule runs from the customs release date, so a shipment released around August 2026 must not be sold or lent before about August 2032.

Result: Clean plan, one shipment kept in reserve.

### Example 2: Family of 4 from France

User: "Family of 4 from Paris. 3 TVs, 4 computers (2 parents + 2 kids), fridge, 2 dishwashers (one for dairy one for meat), full furniture set, 25 sqm of rugs, renting an 80 sqm apartment in Netanya."

Actions:
1. Profile: Oleh family, household of 4, renting 80 sqm.
2. Classify:
   - 3 TVs = at the cap of 3. Exempt.
   - 4 computers = over the cap of 3. 3 exempt; flag the 4th as over-limit.
   - Fridge OK (one of type).
   - 2 dishwashers = over one-of-each. Flag the second as over-limit.
   - Rugs: NBN 25% of 80 sqm = 20 sqm. Flag 5 sqm as over-limit, and confirm with customs that loose rugs (not fitted carpet) are what is being imported.
   - Furniture: household use, one of each major item; several beds for several children are a "verify" item for customs to decide.
3. Recommend: leave the 4th computer with family in France. For the second dishwasher, the user may still want to pay duty for halachic reasons; get a broker quote.
4. Split:
   - Shipment 1 (air): clothes, bedding, kids' essentials.
   - Shipment 2 (sea FCL 40-foot): furniture, appliances, kitchen, books, TVs, 3 computers, both dishwashers (the second declared over-limit, taxes paid), 20 sqm of rugs. Must fit in one container or come on the same ship and clear together.
   - Shipment 3: a real reserve. Do not spend it on a taxed item that can ride in shipment 2.
5. Declaration: flag over-limit rows clearly. No fixed duty number in this plan.

Result: A plan that avoids over-cap charges on the easy items and forces an explicit decision on the second dishwasher. Enter rows as the user describes them ("2 parents + 2 kids"): the script sums rows of the same category before applying the cap.

### Example 3: Toshav Chozer Returning After 8 Years in London

User: "I left Israel in 2018, lived in London since, now returning. Can I use the 3-shipment rule?"

Actions:
1. Profile: returning resident (abroad 2+ years), not an oleh. The same answer applies to someone making aliyah for the second time.
2. Explain the different track from the Tax Authority returning-residents guide: household goods in two shipments only, arriving within 9 months of the return, not extendable; the same 3-TV / 3-computer / one-of-each caps; no oleh vehicle concession.
3. Do NOT produce the oleh 3-shipment plan. Route to `israeli-returning-resident-navigator` for the full returning-resident picture, and to the customs office to open the eligibility file (online form).

Result: The user gets the right window and shipment count instead of an oleh plan that would cost them their exemption.

## Bundled Resources

### Scripts
- `scripts/plan_shipments.py` - Takes a JSON inventory (items, counts, category, optional type, per-unit declared values), the status date, home area and rooms. Sums rows of the same category (per type for appliances and furniture), classifies them against the per-family caps (including the 25% carpet rule and the USD 1,650 hand-tool and USD 36,000 business-equipment ceilings), flags over-limit and verify items, proposes a starting 3-shipment split, and drafts a worksheet per shipment. Exits 2 for a returning resident or second-time oleh. Run: `python scripts/plan_shipments.py --help`

### References
- `references/allowed-items-list.md` - Detailed classification of household items: exempt, capped, non-household, permit-only. Consult for unusual items.
- `references/shipment-planning-strategy.md` - Sequencing shipments across the window, container math, air vs sea, broker vs self-clear.
- `references/returning-residents.md` - Toshav Chozer rules and when to route the user away from this planner.
- `references/domain-checklist.md` - Coverage checklist with sources.

## Recommended MCP Servers

| MCP Server | Purpose | Status |
|------------|---------|--------|
| [Kol-Zchut MCP](https://agentskills.co.il/he/mcp/kolzchut) | Look up Israeli rights pages, including olim and returning-resident customs rights | Available |
| Customs tariff / duty calculation | Customs tariff lookup, live duty calculation | No MCP server currently wraps the Israeli customs tariff. Use the official sources in Reference Links and a licensed customs broker for duty quotes. |

## Gotchas

- The 3-year window runs from the day oleh status was received, not from the planning date and not from the day the lift is shipped. A shipment that ARRIVES after the window closes is outside it.
- "One of each appliance" is strict: a second refrigerator, oven or washing machine is over-limit even for families with halachic reasons to own two.
- Spouses do not double the allowance. Spouses who received status at different times are together entitled to 3 shipments, and capped items the first spouse already brought count against the second (Tax Authority).
- Household items carried on the aliyah flight are a free extra, not a shipment, but only on the same flight and only through the Red lane. Agents often omit this and waste a shipment slot.
- A household-items postal package uses a full shipment slot. Only a clothing-and-footwear-only package inside the window is free.
- Cars are a separate benefit with their own 3-year window and a 4-year personal-use restriction after release (the Tax Authority olim guide: the car may be sold only after 4 years of use in Israel). This is a restriction on use and sale after release, not a rule about the car's age. Do not count a car against the 3 shipment slots; for an oleh's vehicle questions use the "taxes on a vehicle" chapter of the Tax Authority olim guide (the returning-resident vehicle skill is for returning residents only).
- Toshav Chozer, and a second-time oleh, are a different track: 2 shipments within 9 months, no extension. Never apply the oleh plan, and ask about prior residency before planning.
- Letting a courier pay the duty on a parcel usually forfeits the benefit with no refund (NBN).

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Tax Authority - Import tax guide for new olim (Hebrew) | https://www.gov.il/he/pages/guide-for-immigrants-and-foreign-residents | Eligible statuses, caps, shipments, accompanying luggage, eligibility period and extensions, spouses |
| Israel Tax Authority - same guide (English) | https://www.gov.il/en/pages/guide-for-immigrants-and-foreign-residents | English version of the above |
| Israel Tax Authority - Customs guide for returning residents | https://www.gov.il/he/Departments/Guides/customs-guide-for-returning-residents | Toshav Chozer shipments, 9-month window |
| Ministry of Agriculture - Importing dogs and cats | https://www.gov.il/he/service/import_pets_cats_dogs | Pet licence or exemption conditions |
| Nefesh B'Nefesh - Customs Benefits | https://www.nbn.org.il/life-in-israel/government-services/rights-and-benefits/understanding-customs-benefits/ | Phone and carpet caps, container rule, postal release procedure |
| Misrad HaKlita (Ministry of Aliyah and Integration) | https://www.gov.il/en/departments/ministry_of_aliyah_and_integration | Oleh status, Guide for the New Immigrant |

## Troubleshooting

### Error: "User does not know their exact aliyah date yet"
Cause: User is planning shipments before making aliyah.
Solution: Use the planned date as a proxy. The 3-year clock only starts when oleh status is received. Pre-aliyah freight quotes are fine; exemption paperwork cannot be completed until the status exists.

### Error: "Item count is exactly at the cap - is that allowed?"
Cause: Family has exactly 3 TVs or 3 computers.
Solution: Yes. The Tax Authority guide allows up to 3 TVs and 3 personal computers per family, so items exactly at the cap are exempt. Only items over the cap need broker quotes.

### Error: "User wants to gift an exempt appliance to a relative"
Cause: Personal-use rule confusion.
Solution: Passing an exempt item to anyone else's use within 6 years, even free or temporarily, breaches the exemption conditions. Tell the user to keep it 6 years or ask the customs office what would be owed first.

### Error: "Second container of a sea shipment was delayed and arrived separately"
Cause: Same-ship / same-clearance rule broken.
Solution: NBN's rule needs BOTH conditions: the containers came on the same ship AND were cleared together. A container that arrived on a different ship counts as a second shipment, and holding the first one at the port does not change that. Prevent it at booking: put both containers on the same vessel. If it already happened, accept the 2-shipment count or ask the customs office; do not promise a fix.

### Error: "Toshav Chozer user is asking for the full 3-shipment plan"
Cause: Wrong status applied.
Solution: Do NOT output the standard plan. Explain the 2-shipment / 9-month returning-resident track and route to `israeli-returning-resident-navigator` and `references/returning-residents.md`.
