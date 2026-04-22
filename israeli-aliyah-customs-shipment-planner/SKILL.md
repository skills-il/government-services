---
name: israeli-aliyah-customs-shipment-planner
description: "Plan the 3-shipment customs exemption for new olim (zchuyot olim): classify belongings as exempt or over-limit, flag the 3-TV / 3-computer / 5-phone / 25%-carpet / one-of-each-appliance caps, split inventory across shipment 1/2/3 within the 3-year window, and draft customs declarations. Use when user asks about olim shipping rights, teudat oleh customs benefits, meches olim, lift shipping plan, how many TVs can I bring, or how to split my aliyah shipment. Do NOT use for general aliyah absorption (sal klita, ulpan, Misrad HaKlita) - use israeli-aliyah-navigator instead."
license: MIT
compatibility: "Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex, Antigravity, Gemini CLI. Python 3.8+ for the planning script."
---

# Israeli Aliyah Customs Shipment Planner

## Problem

New olim (immigrants) to Israel are entitled to three duty-free shipments of household goods within three years of aliyah, but the rules are riddled with per-family caps (TVs, computers, cell phones, appliances, carpeting) and a six-year retention rule that blocks resale. Most olim pack by emotion, then discover at the port that a third computer or a fourth appliance triggers full duty plus VAT plus purchase tax. This skill plans the split across three shipments, flags over-limit items before packing, and drafts a clean declaration per shipment.

## Instructions

### Step 1: Collect Aliyah Profile

Ask the user for the following before planning anything:

| Field | Why it matters |
|-------|---------------|
| Aliyah date (teudat oleh issue date) | Starts the 3-year exemption window |
| Immigrant status | Oleh Chadash vs Toshav Chozer - returning residents have limited benefits only |
| Household size | Caps are per family, not per person |
| Planned home area in Israel (sqm) | Carpet exemption is up to 25% of home area |
| Origin country | Affects freight mode (air/sea) and container sizing |
| Is the spouse a non-oleh? | Mixed households reduce the per-family allowance |
| Full-time military service or study abroad? | May extend the 3-year window |

If the user is a Toshav Chozer, route them to Misrad HaKlita Returning Resident desk and note that entitlement is reduced - do not plan their shipment as if they are an Oleh Chadash.

### Step 2: Classify Every Item

For each item on the user's packing list, tag it as one of:

| Tag | Meaning | Action |
|-----|---------|--------|
| exempt | Household item within per-family cap | Include in a shipment |
| over-limit | Item count exceeds cap (e.g., 4th TV, 2nd fridge) | Duty + VAT + purchase tax applies; recommend sell/gift before aliyah |
| non-household | Office equipment, machinery, commercial goods | Not covered by exemption; clear as ordinary import |
| restricted | Firearms, plants, certain medications, drones, food | Separate permit path - outside this skill |
| vehicle | Car, motorcycle, ATV | Separate vehicle benefit (3-year window, Passport-to-Passport or new car) - outside this shipment plan |

Per-family caps to enforce during classification:

| Category | Cap per family |
|----------|----------------|
| Televisions | 3 |
| Computers | 3 |
| Cell phones | 5 |
| Carpeting | Up to 25% of the oleh's home area in Israel |
| Appliances / electronic equipment (fridge, oven, washing machine, dryer, microwave, etc.) | One of each type |
| Personal effects (books, clothing, linens, kitchen utensils, decorations) | No fixed cap - must be personal use |
| Furniture | Household use |

Run `scripts/plan_shipments.py` to do this classification automatically from a JSON inventory.

### Step 3: Propose a 3-Shipment Split

Rule of thumb for splitting within the 3-year window:

1. Shipment 1 (arrival): essentials only. Beds, a basic kitchen, enough clothes for a few months, one laptop, one TV. Ship 4-8 weeks before arrival if sea, 1-2 weeks if air.
2. Shipment 2 (3-9 months after aliyah): the bulk lift. Remaining furniture, appliances (one of each), books, kitchenware, second computer/TV if the family needs it.
3. Shipment 3 (reserve, up to 36 months after aliyah): whatever the family realized they need later - extra appliance on the cap, seasonal items, replacement furniture for Israel-sized apartments.

Container math: if shipment 2 does not fit in one 40-foot container it will count as 2 shipments (consuming shipment 3) unless both containers come on the same ship and are cleared together at the same customs appointment. Flag this in the plan.

### Step 4: Draft the Per-Shipment Customs Declaration

For each shipment, produce:

- Shipment number (1 / 2 / 3)
- Expected arrival port (Haifa, Ashdod, Ben Gurion air cargo)
- Freight mode (air, sea LCL, sea FCL 20-foot, sea FCL 40-foot)
- Inventory list grouped by category (furniture, appliances, electronics, personal)
- Declared value per line (insurance / customs valuation)
- Flag column: exempt / over-limit / non-household
- Totals: total items, over-limit count, estimated duty exposure on over-limit items

Do NOT fabricate specific NIS amounts for duty or purchase tax on over-limit items - rates are set by Tariff (Taarif HaMeches) and change. Tell the user to get a pre-clearance quote from a licensed customs broker (amil meches) for any over-limit item worth more than a few hundred shekels.

### Step 5: Advise on Timing and the 6-Year Hold

Remind the user of the retention rule: anything imported duty-free under aliyah rights must stay in their possession for at least 6 years from the date of import, or depreciated tax must be paid back to Meches. Cars must be kept 5 years. Plan around it:

- Do not import items you plan to resell within 6 years (e.g., "I will flip this fridge when I upgrade in 2 years").
- Do not use the exemption on gifts for relatives who live outside your household.
- Items that were already used abroad do depreciate in the retention formula, but you still owe something if you sell early - escalate to a customs broker for specifics.

### Step 6: Write the Checklist Back to the User

Output a clean 3-column table: shipment number, items, flags. Include a short list of next actions: (a) confirm Misrad HaKlita file is open, (b) choose a customs broker (amil meches) or self-clear, (c) get insurance valuations, (d) book freight, (e) pre-inspect anything flagged over-limit.

## Examples

### Example 1: Single Software Engineer from the US

User: "I'm making aliyah in June, solo, from Boston. One bedroom I'll rent. I have 2 laptops, 1 desktop, 1 TV, no furniture, lots of books, espresso machine. Plan my shipments."

Actions:
1. Profile: Oleh Chadash, household size 1, home area small (~40 sqm), sea LCL.
2. Classify: 3 computers total (2 laptops + 1 desktop) = at the per-family cap of 3. 1 TV under cap. Espresso machine is one appliance (OK). Books and clothes personal effects (OK).
3. Split:
   - Shipment 1 (air, before arrival): 1 laptop, clothes, essentials. (~100 kg)
   - Shipment 2 (sea LCL, 2 months after arrival): other laptop, desktop, TV, espresso machine, books.
   - Shipment 3: reserve.
4. Declaration: 2 shipments used, 1 in reserve. No over-limit items. Zero estimated duty.
5. Timing note: 6-year hold means do not sell the desktop before 2032.

Result: Clean plan, well under caps, one shipment kept in reserve for future Israel purchases.

### Example 2: Family of 4 from France

User: "Family of 4 from Paris. 3 TVs, 4 computers (2 parents + 2 kids), fridge, 2 washing machines (one for dairy one for meat), full furniture set, 80 sqm apartment in Netanya."

Actions:
1. Profile: Oleh Chadash, household size 4, 80 sqm home. Allowed carpet: 20 sqm.
2. Classify:
   - 3 TVs = at cap of 3. OK.
   - 4 computers = over the cap of 3 by one. Flag one computer as over-limit.
   - Fridge OK (one of type).
   - 2 washing machines = over the "one of each appliance" cap. Flag the second washer as over-limit.
   - Furniture personal use, OK.
3. Recommend: leave the 4th computer with family in France, buy new in Israel (may be cheaper than paying duty + VAT + purchase tax). For the second washing machine, user may still want to pay duty for halachic reasons - escalate to customs broker for a cost quote.
4. Split:
   - Shipment 1 (air, 200 kg): clothes, bedding, kids' essentials.
   - Shipment 2 (sea FCL 40-foot): all furniture, appliances, kitchen, books, TVs, 3 of 4 computers, first washer. Note: must fit in one container or it becomes 2 shipments.
   - Shipment 3 (reserve, within 36 months): second washer if family decides to import it (pay duty) plus any follow-up items.
5. Declaration: flag over-limit rows clearly. Expected duty exposure: full rates on any item shipped over cap, no fixed number in this plan.

Result: Plan that avoids over-cap charges on the easy ones and forces an explicit decision on the washing machine.

### Example 3: Toshav Chozer Returning After 8 Years in London

User: "I left Israel in 2018, lived in London since, now returning. Can I use the 3-shipment rule?"

Actions:
1. Profile: Toshav Chozer status - NOT full Oleh Chadash rights. Entitlement is "limited customs benefits only" per Nefesh B'Nefesh / Misrad HaKlita.
2. Do NOT plan as a full 3-shipment oleh. Instead:
   - Route user to Misrad HaKlita's Returning Resident desk to confirm eligibility and the exact item caps they qualify for (varies by years away and prior residency status).
   - Route user to a licensed customs broker (amil meches) for a goods list review.
3. Output a short advisory note, not a packing plan. Cite Kol-Zchut and Nefesh B'Nefesh rights hub.

Result: User is redirected to the correct authority instead of being handed an incorrect plan.

## Bundled Resources

### Scripts
- `scripts/plan_shipments.py` - Takes a JSON inventory (items, counts, category, declared values), family size, aliyah date, and home area. Classifies each item against per-family caps, flags over-limit, proposes a 3-shipment split, and drafts a declaration per shipment. Run: `python scripts/plan_shipments.py --help`

### References
- `references/allowed-items-list.md` - Detailed list of household items categorized as exempt, over-limit triggers, or non-household. Consult when classifying unusual items.
- `references/shipment-planning-strategy.md` - How to sequence 3 shipments across 36 months, container math, air vs sea tradeoffs, broker vs self-clear decision.
- `references/returning-residents.md` - Toshav Chozer rules: how they differ from Oleh Chadash, eligibility tiers, when to route the user away from this planner.

## Recommended MCP Servers

| MCP Server | Purpose | Status |
|------------|---------|--------|
| None currently available | Customs tariff lookup, live duty calculation | No MCP server currently wraps Israeli customs tariff (Taarif HaMeches) or Misrad HaKlita rights APIs. Consult the official sources in Reference Links and a licensed customs broker for duty quotes. |

## Gotchas

- The 3-year window starts from the date on the teudat oleh (aliyah certificate), not the day the oleh physically lands. Items arriving on day 1,096 after aliyah are already outside the window.
- "One of each appliance" is strict: a second refrigerator, a second oven, or a second washing machine is over-limit even for families with halachic reasons to own two. The exemption does not carve out dairy/meat duplicates.
- Cars are a completely separate benefit with its own 3-year clock and its own 5-year retention rule. Do not count a car against your 3 shipment slots.
- If a sea shipment exceeds one full container, it counts as 2 shipments unless both containers come on the same ship AND are cleared through customs at the same appointment. Losing the second container slot because it arrived a week late is a common and expensive mistake.
- Goods imported under aliyah rights must stay in the oleh's possession for 6 years, or depreciated tax must be paid back to Meches. Selling an "exempt" fridge after 2 years triggers a retroactive duty bill. Vehicles have a 5-year hold.
- Toshav Chozer (returning resident) is a different status with limited benefits. Do NOT apply the full Oleh Chadash 3-shipment plan to a returning resident without confirming eligibility at Misrad HaKlita.
- Mixed households where one spouse is a non-oleh do not get double the per-family allowance. The cap is still "one of each appliance" for the household.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Nefesh B'Nefesh - Customs Benefits | https://www.nbn.org.il/life-in-israel/government-services/rights-and-benefits/understanding-customs-benefits/ | Current per-family caps, shipment rules, vehicle benefit summary |
| Nefesh B'Nefesh - Rights Hub | https://www.nbn.org.il/life-in-israel/government-services/rights-and-benefits/ | Full rights index including banking, tax, license conversion |
| Anglo-List - Aliyah Shipping Rights | https://anglo-list.com/aliyah-shipping-rights/ | 6-year retention rule, practical packing guidance |
| Misrad HaKlita (Ministry of Aliyah and Integration) | https://www.gov.il/en/departments/ministry_of_aliyah_and_integration | Teudat oleh issuance, returning resident classification |
| Israel Tax Authority - Meches | https://www.gov.il/en/departments/israel_tax_authority | Official customs authority, Taarif HaMeches tariff database |
| Kol-Zchut - All Rights | https://www.kolzchut.org.il | Community-maintained Hebrew and English rights pages |

## Troubleshooting

### Error: "User does not know their exact aliyah date yet"
Cause: User is planning shipments before making aliyah.
Solution: Use the planned aliyah date as a proxy. Note that the 3-year clock only starts when the teudat oleh is issued, not when the plan is made. Pre-aliyah freight quotes are fine; actual exemption paperwork cannot be finalized until the teudat oleh exists.

### Error: "Item count is exactly at the cap - is that allowed?"
Cause: Family has 3 TVs, 3 computers, or exactly the cap number.
Solution: At the cap is allowed (the cap is 3, not "less than 3"). One unit above the cap is over-limit. Confirm by reading the cap table in Step 2.

### Error: "User wants to gift an exempt appliance to a relative"
Cause: Retention rule confusion.
Solution: The 6-year retention rule applies to the oleh's possession. Gifting an exempt item to a relative who lives in a different household within 6 years triggers depreciated duty. Tell the user to either keep the item 6 years or pay the retroactive duty through Meches.

### Error: "Second container of a sea shipment was delayed and arrived separately"
Cause: Same-ship / same-clearance rule broken.
Solution: If the two containers are now cleared on different days, they count as 2 shipments, consuming the shipment 3 slot. Work with the customs broker to either hold the first container at the port until the second arrives, or accept the 2-shipment cost.

### Error: "Toshav Chozer user is asking for the full 3-shipment plan"
Cause: Wrong status applied.
Solution: Do NOT output the standard 3-shipment plan. Route to Misrad HaKlita Returning Resident desk. Use `references/returning-residents.md`.
