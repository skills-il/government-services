---
name: israeli-land-tenders
description: Israeli Land Authority (RMI) tender data, land allocation guidance, and bid process navigation. Use when user asks about Israeli land tenders, "michraz", "rashut mekarkei yisrael", RMI, Israel Land Authority, government land auctions, "haktzaah", land lottery ("hagralah"), "Dira BeHanacha" sub-tracks (Mechir Lamishtaken, Mechir Matara, Mechir Muphchat, Dira Lehaskir), resale lockup, building rights, or state land allocation. Enhances remy-land-authority MCP server with tender process guidance and Hebrew terminology. Do NOT use for private real estate transactions (use israeli-real-estate skill instead) or non-Israeli land systems.
license: MIT
allowed-tools: WebFetch
compatibility: Network access helpful for tender data lookups. Enhanced by remy-land-authority MCP server.
---

# Israeli Land Tenders (RMI)

## Critical Note
Tender conditions, deadlines, and requirements change with each publication.
Always verify current tender details on the official RMI tender portal
(`apps.land.gov.il/MichrazimSite/`). This skill provides general guidance on
the tender system and process -- specific tender terms take precedence over
general rules. Recommend users consult a real estate attorney (orech din
mikrkain) before submitting bids on significant tenders.

## Instructions

### Step 1: Identify Land Tender Need
| Need | Action |
|------|--------|
| Search tenders | Query RMI tender listings via remy-land-authority MCP or apps.land.gov.il/MichrazimSite |
| Understand tender type | Explain allocation method and implications |
| Bid process guidance | Step-by-step bid submission guide |
| Tender analysis | Interpret conditions, estimate competition |
| Land system explainer | Explain Israel's land ownership model |
| Development terms | Decode building rights and conditions |

### Step 2: Search for Tenders
Use the remy-land-authority MCP server, or query the official RMI tender portal at `apps.land.gov.il/MichrazimSite/`, to find active and recent tenders. RMI also publishes an interactive tender map at `gov.il/he/departments/israel_land_authority/map/map_micrazim`.

**Search parameters:**
| Filter | Description | Example |
|--------|-------------|---------|
| Location (makom) | City or district | Tel Aviv, Jerusalem, Haifa |
| Land use (shimush) | Purpose category | Residential (megurim), commercial (miskhari) |
| Tender type (sug) | Allocation method | Tender (michraz), lottery (hagralah) |
| Status (matzav) | Current status | Open, closed, awarded |
| Date range | Publication period | Last 30/60/90 days |

**Key tender data fields:**
| Field | Hebrew | Description |
|-------|--------|-------------|
| Tender number | mispar michraz | Unique identifier |
| Location | makom / ktovet | City and specific area |
| Land use | yiud hakarka | Permitted use category |
| Plot size | shetach | Size in square meters or dunams |
| Building rights | zchuyot bniyah | Permitted construction area (sq. meters) |
| Minimum price | mechir minimum | Lowest acceptable bid |
| Deadline | moed acharon | Bid submission deadline |
| Deposit (arbon) | arbon / pikdon | Required bid deposit amount |
| Conditions | tnaim | Development conditions and timelines |

### Step 3: Understand Tender Types

**Public Tender (Michraz)**
- Open competitive bidding, typically highest price wins
- Bidders submit sealed proposals with price and sometimes qualitative criteria
- Most common for large residential and commercial projects
- Requires significant financial capacity and often development experience
- Deposit: Usually 10-15% of minimum price

**Lottery (Hagralah)**
- Fixed price set by RMI, applicants drawn randomly
- Powers the affordable housing program formerly known as "Mechir Lamishtaken" (מחיר למשתכן), now operating as an umbrella program called **"Dira BeHanacha" (דירה בהנחה)** with multiple sub-tracks (mechir lamishtaken klali, mechir matara, mechir muphchat, dira lehaskir). Operated by the Ministry of Construction and Housing at `dira.moch.gov.il`. RMI supplies the land via the tender, the Housing Ministry runs eligibility, registration, and the drawing.
- Sub-tracks differ in discount cap, grant, eligible audience: **Mechir Matara** caps the discount at 20% off market price or 500,000 NIS (whichever is lower) and is the only track currently open to dwelling upgraders (mishaprey diur), not only first-time buyers. Mechir Lamishtaken klali has no discount cap. Mechir Matara and Mechir Muphchat include a uniform 40,000 NIS buyer grant via the mortgage bank.
- Eligibility criteria: typically first-time buyers (chasrey dira) with no property ownership in the prior 3 years, a valid eligibility certificate (teudat zakaut) from the Housing Ministry, age and household thresholds defined per round. Eligibility certificate fee is around 200 NIS.
- **Lottery 11 (April 2026)**: registration opens 15 April 2026, ~7,000 units across roughly 16 cities including Ashdod, Rehovot, Hadera, Ma'ale Adumim, Kiryat Gat, Nahariya, Eilat, Yehud, Rishon LeZion, Kfar Saba. Up to 50% of units reserved for active reservists (miluimnikim), about 25% of those for reserve combat soldiers.
- **Resale lockup**: cannot sell or rent for **5 years from Form 4 (Tofes 4 / occupancy approval) OR 7 years from the lottery win date, whichever comes first**. Selling earlier triggers clawback of the discount.
- Registration fee: relatively small compared to tender deposits. Each round lets eligible registrants choose up to 3 cities and apply to all lotteries in those cities.

**Price Buyer (Mechir Larocheish)**
- Fixed price, allocated based on eligibility order
- Used for specific populations: discharged soldiers, new immigrants, residents of specific areas
- Price typically at or below market value
- Conditions on resale (lock-up period, typically 5-10 years)
- Historically less common than Dira BeHanacha; availability varies by government policy and region

**Direct Allocation (Haktzaah Yeshira)**
- No competitive process
- For public institutions, government bodies, specific approved projects
- Requires specific government/ministerial approval
- Examples: schools, synagogues, community centers

### Step 4: Bid Submission Guide (for Public Tenders)
Step-by-step process for submitting a tender bid:

1. **Review tender documents**
   - Download full tender booklet (chovert michraz) from the RMI tender portal (`apps.land.gov.il/MichrazimSite/`)
   - Read ALL conditions, especially development timeline and penalties
   - Check building rights (zchuyot bniyah) and permitted uses

2. **Assess financial capacity**
   - Minimum price: Listed in tender, can bid higher
   - Deposit (arbon): Typically 10-15% of minimum price, bank guarantee or check
   - Development costs: Estimate construction and infrastructure costs
   - Development fees: Government levies (hetel hashbacha, agrat pituach)

3. **Prepare required documents**
   - Company registration (if corporate bidder)
   - Financial statements or bank guarantees
   - Signed tender conditions acceptance
   - Bid form with proposed price
   - Deposit check or bank guarantee

4. **Determine bid price**
   - Research comparable recent tender results in the area
   - Factor in building rights, location, and market conditions
   - Consider minimum price as floor -- winning bids often 10-50%+ above minimum
   - Higher competition areas (Tel Aviv, central Israel) command larger premiums

5. **Submit before deadline**
   - RMI operates an online tender submission system at `apps.land.gov.il/MichrazimSite/`. Most residential and commercial tenders now accept (and often require) online bid submission, which needs a digital identification certificate (teudat zihuy digital) or smart card.
   - Some specialty tenders still require physical submission in a sealed envelope to the regional RMI office; the tender booklet specifies the required channel -- always verify per tender.
   - Late submissions are disqualified without exception regardless of channel.

6. **Post-submission**
   - Public bid opening (ptichat hatzaot) at announced date and time
   - Results published on the RMI tender portal
   - Winner signs development agreement within specified timeframe
   - Development must begin within timeline or face penalties/forfeiture

### Step 5: Understanding Building Rights
Tender conditions specify building rights:

| Term | Hebrew | Meaning |
|------|--------|---------|
| Shetach hamigresh | shetach hamigresh | Total plot area (sq. meters) |
| Achuz bniyah | achuz bniya | Building coverage percentage |
| Zchuyot bniyah | zchuyot bniya | Total permitted built area (sq. meters) |
| Komot (floors) | komot | Maximum number of stories |
| Gavoa (height) | gova | Maximum building height |
| Kav binyan | kav binyan | Building line / setback requirement |
| Shimush | shimush | Permitted uses |
| Taba | taba | Zoning plan governing the plot |

**Key calculation:**
```
Value = Building Rights (sq.m.) x Price per sq.m. (market) - Development Costs
```
This helps estimate maximum rational bid price.

### Step 6: Hebrew Tender Terminology Quick Reference
Essential terms for reading Hebrew tender documents:
| English | Hebrew | Transliteration |
|---------|--------|----------------|
| Tender | michraz | michraz |
| Bidder | magia hatzaa | magia hatzaa |
| Bid/Proposal | hatzaah | hatzaa |
| Minimum price | mechir minimum | mechir minimum |
| Deposit | arbon/pikdon | arbon / pikdon |
| Development agreement | heskem pituach | heskem pituach |
| Development conditions | tnaei pituach | tnaei pituach |
| Building permit | heter bniyah | heter bniya |
| Completion deadline | moed siyum | moed siyum |
| Extension | archa | archa |
| Forfeiture | chilut | chilut |
| Objection | hashagah | hashaga |
| Winner | zocheh | zocheh |

## Examples

### Example 1: Tender Search
User says: "Are there any land tenders open in Beer Sheva for residential?"
Result: Query the remy-land-authority MCP (or `apps.land.gov.il/MichrazimSite/`) for Beer Sheva residential tenders. Present active tenders with: tender number, exact location, plot size, building rights, minimum price, and submission deadline. Note that Beer Sheva typically has lower minimum prices than central Israel.

### Example 2: Lottery Guidance
User says: "How do I apply for mechir lamishtaken?"
Result: Clarify that "Mechir Lamishtaken" is now one sub-track inside the umbrella program **"Dira BeHanacha" (דירה בהנחה)** operated by the Ministry of Construction and Housing (not RMI directly). Walk through: (1) the current sub-tracks (Mechir Lamishtaken klali, Mechir Matara, Mechir Muphchat, Dira Lehaskir) and how Mechir Matara caps the discount at 20% off market or 500,000 NIS and is the only track open to dwelling upgraders, (2) eligibility (chasrey dira, valid teudat zakaut from the Housing Ministry, age and household thresholds), (3) the two-step flow (RMI tenders the land, Housing Ministry runs eligibility and the lottery), (4) registration at `dira.moch.gov.il`, (5) resale lockup of 5 years from Tofes 4 or 7 years from lottery win (earlier of the two), and (6) the current open round on the Housing Ministry site (Lottery 11 registration opened 15 April 2026, ~7,000 units in ~16 cities, up to 50% reserved for active reservists).

### Example 3: Bid Strategy
User says: "There's a tender in Netanya, minimum price 15 million, how much should I bid?"
Result: Explain that bid strategy depends on: recent comparable tender results in Netanya, number of expected bidders, building rights and development costs, current market conditions. Provide framework for analysis but recommend consulting a real estate appraiser (shamai mikrkain) and attorney for specific bid amount. Note that winning bids in Netanya coastal areas are typically 20-40% above minimum.

## Bundled Resources

### Scripts
- `scripts/search_tenders.py` - Display RMI tender type descriptions (michraz, hagralah, mechir larocheish, haktzaah), step-by-step bid submission guide for public tenders, Hebrew-English terminology glossary for tender documents, and land use category definitions. Supports subcommands: `tender-types`, `bid-guide`, `terminology`, `land-use`. Run: `python scripts/search_tenders.py --help`

### References
- `references/rmi-system-guide.md` - Overview of Israel's state land system (93% government-owned, leasehold model), tender type comparison table, land use categories with Hebrew terms, building rights terminology (zchuyot bniyah, achuz bniyah, kav binyan), and official RMI portal URLs. Consult when explaining Israel's land ownership model or decoding tender document terms.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [remy-land-authority](https://agentskills.co.il/he/mcp/remy-land-authority) | Live programmatic access to RMI tender listings, filters by location/land-use/status, and structured tender metadata. Pair with this skill when the user needs real data, not just process guidance. |

## Gotchas
- Israeli land tenders (michrazei karka'ot) from the Israel Land Authority (RMI/Rami) are published in Hebrew only. Agents may search for tenders using English location names, which will return no results.
- Land measurements in Israeli tenders use dunam (1 dunam = 1,000 square meters), not acres or hectares. Agents may convert to international units without noting the original dunam figure.
- Tender participation requires a bank guarantee (areva bankit) of 10-15% of the tender price. Agents may suggest bidding without mentioning this upfront financial requirement.
- Israeli land in urban areas is often leased from the state (chakira) for 49 or 98 years (not a free range, those are the canonical lease lengths), not purchased outright as in the US. Agents may describe land acquisition using ownership terminology when it is actually a long-term lease.
- The affordable-housing lottery program is administered by the Ministry of Construction and Housing at `dira.moch.gov.il`, not by RMI directly. Agents that point users to the RMI site for lottery registration will send them to the wrong place. RMI tenders the land; the Housing Ministry runs eligibility, registration, and the drawing.
- "Mechir Lamishtaken" is the legacy name; today it is one sub-track inside Dira BeHanacha. **Mechir Matara** is a distinct sub-track with different rules (20% / 500K NIS discount cap, 40,000 NIS buyer grant, open to dwelling upgraders). Treating them as the same program causes wrong eligibility advice.
- Dira BeHanacha resale lockup is **5 years from Form 4 OR 7 years from the lottery win, whichever comes first**, not a flat number of years. Agents that quote "5 years" or "7 years" alone will mislead users on when they can sell.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| RMI tender portal (MichrazimSite) | https://apps.land.gov.il/MichrazimSite/ | Active and recent tenders, tender booklets, online bid submission |
| Israel Land Authority (gov.il) | https://www.gov.il/he/departments/israel_land_authority | Official RMI department page, announcements, policy updates |
| RMI tender map | https://www.gov.il/he/departments/israel_land_authority/map/map_micrazim | Interactive map of active land tenders |
| Dira BeHanacha lottery | https://dira.moch.gov.il/ | Current and upcoming affordable-housing lottery rounds, eligibility certificate |
| Online bid submission service (English) | https://www.gov.il/en/service/tenders-online | English documentation of the online bid submission flow |
| RMI services portal | https://www.gov.il/en/service/my-ramitech | "My ILA" -- view participated tenders, mailings, exercise bid wins |

## Troubleshooting

### Error: "Tender not found"
Cause: Tender may have expired, been cancelled, or search terms do not match Hebrew listing
Solution: Search by tender number if known. Try broader location terms. Check if the tender was cancelled (mevutal) or postponed (nidcha). RMI occasionally cancels tenders if no qualifying bids received.

### Error: "Cannot determine eligibility"
Cause: Lottery and price-buyer tenders have specific eligibility criteria
Solution: Each tender defines its own eligibility. Common criteria: no property ownership, age range, specific population group. Check the specific tender booklet (chovert michraz) for exact requirements. For Dira BeHanacha, eligibility is issued by the Housing Ministry as a teudat zakaut, not by RMI.

### Error: "Tender results not published"
Cause: Results publication may be delayed due to objections or committee review
Solution: Results are typically published 1-4 weeks after bid opening. Check the RMI tender portal under "results" (totz'ot). During the objection period, results may be preliminary.
