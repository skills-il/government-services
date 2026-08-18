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
Use the remy-land-authority MCP server, or query the official RMI tender portal at `apps.land.gov.il/MichrazimSite/`, to find active and recent tenders. RMI's land-tenders hub page at `gov.il/he/departments/topics/land_tenders` links the tender system and an interactive tender map.

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
- Deposit (arbon): set per tender in the tender document; read the amount off the specific michraz, never assume a rate

**Lottery (Hagralah)**
- Fixed price set by RMI, applicants drawn randomly
- Powers the affordable housing program formerly known as "Mechir Lamishtaken" (מחיר למשתכן), now operating as an umbrella program called **"Dira BeHanacha" (דירה בהנחה)** with multiple sub-tracks (mechir lamishtaken klali, mechir matara, mechir muphchat, dira lehaskir). Operated by the Ministry of Construction and Housing at `dira.moch.gov.il`. RMI supplies the land via the tender, the Housing Ministry runs eligibility, registration, and the drawing.
- Sub-tracks differ in discount mechanism and audience. **Mechir Matara** grants a capped percentage discount off market price and is explicitly open to dwelling upgraders (mishaprey diur) as well as first-time buyers. The percentage and its shekel ceiling are set per round and published summaries disagree on the ceiling, so read both off the specific round's terms rather than quoting a figure. **Mechir Lamishtaken** works by subsidising the land sold to the developer, who is bound to sell below market. **Mechir Muphchat** sets a maximum price per tender with a mandated build specification. **Dira Lehaskir** is long-term regulated rental, not purchase.
- **Periphery grant (not a universal buyer grant)**: buyers in periphery localities receive a conditional grant, structured as a loan forgiven at the end of the 5 or 7 year commitment period. Mechir Lamishtaken: 40,000 or 60,000 NIS depending on the locality. Mechir Muphchat: 40,000 NIS. Mechir Matara: 40,000 NIS. Paid through the mortgage bank after the purchase contract is signed; buyers who take no mortgage obtain a certificate from a mortgage bank instead.
- **Upgraders (mishaprey diur)**: one year after a project's first lottery, any units first-time buyers did not take are sold on the same winning terms to upgraders. An upgrader must sell the property they own no later than 12 months after occupancy approval (Tofes 4) on the new apartment.
- Eligible populations are wider than "young couples": married or common-law couples (including an Israeli whose partner is a foreign resident), couples marrying within 3 months of the application, a parent of at least one child under 21 (pregnant from the fifth month counts), singles/divorced/widowed aged 35+, and singles aged 21+ with 75% medical disability (or 50% with mobility allowance, hostile-action or Defence Ministry disability payments).
- **Chasrey dira** means that for the 3 years before the eligibility certificate was issued the applicant held no apartment or more than 1/3 of one, no key-money tenancy, no agricultural holding rights, no under-construction apartment, and no more than 1/3 of residential-zoned land. The condition must hold until the purchase contract is signed.
- **Eligibility certificate (teudat zakaut)**: issued through one of the registration companies (chevrot harshama), valid for one year. New certificate 200 NIS; renewal 50 NIS (online or through a registration company) within 60 days of the renewal reminder, after which the certificate is cancelled and a new 200 NIS certificate is needed at a branch. Winners renew for 50 NIS even after expiry.
- **Round mechanics**: registration for a project opens for at least 8 days once published; the draw takes place within 10 days of registration closing; winning one lottery automatically cancels the registrant's other registrations. In the first series of lotteries a registrant may pick projects in at most 3 localities (unlimited lotteries within each); in continuation series there is no locality limit.
- **Priorities**: residents of the host authority for the last 3 years, or 4 of the last 10, get priority in that project's draw (determined from Population Authority data, not appealable). In Mechir Matara draws, one apartment per 30 is allocated to wheelchair-bound applicants holding a 100% disability confirmation from the district health office. Reservist quotas are set per round.
- **Resale lockup**: cannot sell or rent for **5 years from Form 4 (Tofes 4 / occupancy approval) OR 7 years from the lottery win date, whichever comes first**. Selling earlier triggers clawback of the discount.
- **Current round**: rounds open and close on their own calendar, so never present a past round as open. Lottery 11 registration opened on 15 April 2026 with more than 7,000 units and has since closed. Check `dira.moch.gov.il` and the Housing Ministry site for the round that is open today.
- **Choosing the apartment**: winners are invited in draw order and are typically given about 45 minutes to choose from the remaining units. An advance (2,000 NIS, or another amount set at registration) may be required and is not refunded if the win is cancelled after an apartment was chosen.

**Reservist and IDF-disabled land benefits (a separate RMI track, not part of Dira BeHanacha)**
RMI grants active reservists a one-off discount on the price of land for low-rise housing, for one dwelling unit only, and also runs tenders marketed exclusively to reservists and IDF-disabled buyers. Legal basis: Sign B of Chapter 4 of the Israel Land Council decisions.

| Route | Benefit | Cap (excl. VAT) |
|---|---|---|
| Lottery or tender-exempt allocation | Discount on land price by national-priority area: 35% in area A, 20% in area B, 10% elsewhere | 100,000 NIS active reservist / 150,000 NIS combat reservist |
| Public tender win | 15% off the price bid, applied after the winner is determined | Same caps |
| Purchase through an association (amuta) that won a public tender | 15% refund on the member's share | Same caps |

- Lease-fee (dmei chakira) reduction in priority areas: area A pays 16% instead of 31%, area B 36% instead of 51%. Holders of a Housing Ministry "chasar diur" certificate pay 11% instead of 26% (A) and 31% instead of 46% (B).
- If both spouses qualify the rates double, with the ceiling capped at 300,000 NIS for the single dwelling unit.
- Who qualifies: a six-year active-reservist certificate (valid up to 3 years after discharge from reserve duty), or 80 reserve days accumulated over up to 6 calendar years (valid up to 6 years after discharge), or more than 45 reserve days between 07.10.2023 and the declared end of the Iron Swords war (valid up to 6 years from the end of that service).
- To claim: a declaration of reserve service signed before a lawyer plus the relevant IDF confirmation (obtained from the IDF reserve centre, 1111 extension 4), filed at the RMI regional office. RMI enquiries: 03-9533333 or *5575, Sunday to Thursday 08:00-17:00.

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
   - Download the full tender booklet (chovert michraz) from the RMI tender portal (`apps.land.gov.il/MichrazimSite/`) free of charge
   - Some tenders require the ORIGINAL booklet, which must be collected from the relevant RMI regional office (merchav); the booklet itself states when this applies
   - Tenders are advertised in at least one daily newspaper in Hebrew or Arabic as well as online, and the window to bid is usually about 30 days from the booklet's publication
   - Subscribe to the RMI mailing list through "My ILA" (`רמ"י שלי`) to be notified of new tenders and results
   - Read ALL conditions, especially development timeline and penalties
   - Check building rights (zchuyot bniyah) and permitted uses

2. **Assess financial capacity**
   - Minimum price: Listed in tender, can bid higher
   - Deposit (arbon): the amount is stated in the tender document, paid as a bank guarantee or check
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
   - RMI operates an online tender submission system at `apps.land.gov.il/MichrazimSite/`. Most residential and commercial tenders now accept (and often require) online bid submission, which needs registration on the National Identification System. The service is free.
   - Online bids deposit a DIGITAL guarantee, not a paper cheque or a physical bank guarantee. A later bid by the same user replaces the earlier one, and only the last bid is considered.
   - Support: RMI call centre *5574 (Sunday to Thursday 08:00-17:00); technical faults 073-3429900 (09:00-14:00), answered only until 10:00 on the closing day itself, so do not leave submission to the last hours.
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
This is rough screening arithmetic for deciding whether a tender is worth pursuing. It is not a land valuation (shuma). A valuation used for financing, taxation, an objection, or litigation must be produced by a licensed appraiser (shamai mikrkain), and this skill does not produce one.

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
Result: Clarify that "Mechir Lamishtaken" is now one sub-track inside the umbrella program **"Dira BeHanacha" (דירה בהנחה)** operated by the Ministry of Construction and Housing (not RMI directly). Walk through: (1) the sub-tracks (Mechir Lamishtaken, Mechir Matara, Mechir Muphchat, Dira Lehaskir) and that Mechir Matara is a capped percentage discount whose ceiling is set per round, (2) eligibility (chasrey dira or upgraders; the wider eligible populations, including singles 35+ and single parents), (3) the eligibility certificate from a registration company (200 NIS new, 50 NIS renewal, valid one year), (4) registration at `dira.moch.gov.il` for a round that is currently open (never assume a past round is still open, verify on the site), (5) the local-resident priority and the reservist quota for that round, and (6) the resale lockup of 5 years from Tofes 4 or 7 years from the lottery win, whichever comes first. If the user is a reservist, also raise the separate RMI land-price discount track, which is not part of Dira BeHanacha.

### Example 3: Bid Strategy
User says: "There's a tender in Netanya, minimum price 15 million, how much should I bid?"
Result: Explain that bid strategy depends on: recent comparable tender results in Netanya, number of expected bidders, building rights and development costs, current market conditions. Provide framework for analysis but recommend consulting a real estate appraiser (shamai mikrkain) and attorney for specific bid amount. Do not quote a typical premium over the minimum price: it varies by tender and is not published as a rate.

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
- Tender participation requires a deposit, usually as a bank guarantee (areva bankit), in the amount stated in the tender document. Agents may suggest bidding without mentioning this upfront financial requirement.
- Israeli land in urban areas is often leased from the state (chakira) for 49 or 98 years (not a free range, those are the canonical lease lengths), not purchased outright as in the US. Agents may describe land acquisition using ownership terminology when it is actually a long-term lease.
- The affordable-housing lottery program is administered by the Ministry of Construction and Housing at `dira.moch.gov.il`, not by RMI directly. Agents that point users to the RMI site for lottery registration will send them to the wrong place. RMI tenders the land; the Housing Ministry runs eligibility, registration, and the drawing.
- "Mechir Lamishtaken" is the legacy name; today it is one sub-track inside Dira BeHanacha. **Mechir Matara** is a distinct sub-track with different rules (20% / 500K NIS discount cap, 40,000 NIS buyer grant, open to dwelling upgraders). Treating them as the same program causes wrong eligibility advice.
- Dira BeHanacha resale lockup is **5 years from Form 4 OR 7 years from the lottery win, whichever comes first**, not a flat number of years. Agents that quote "5 years" or "7 years" alone will mislead users on when they can sell.
- Reservists and IDF-disabled buyers have a SEPARATE RMI land-price discount track (percentage by national-priority area, capped in shekels) plus tenders marketed exclusively to them. It is unrelated to the Dira BeHanacha reservist quota. Agents that answer a reservist only with the lottery quota miss the larger benefit.
- The Mechir Matara discount ceiling is set per round and published summaries disagree on the figure. Quoting a fixed shekel cap will be wrong for some rounds. Read the ceiling off the round's own terms.
- Lottery rounds open and close on a calendar. A round named in any document, including this skill, may be closed by the time the user asks. Always verify the currently open round on `dira.moch.gov.il` before telling a user to register.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| RMI tender portal (MichrazimSite) | https://apps.land.gov.il/MichrazimSite/ | Active and recent tenders, tender booklets, online bid submission |
| Israel Land Authority (gov.il) | https://www.gov.il/he/departments/israel_land_authority | Official RMI department page, announcements, policy updates |
| RMI land tenders hub | https://www.gov.il/he/departments/topics/land_tenders | Tender system, tender map, and exemption-from-tender information |
| Dira BeHanacha lottery | https://dira.moch.gov.il/ | Current and upcoming affordable-housing lottery rounds, eligibility certificate |
| Online bid submission service (English) | https://www.gov.il/en/service/tenders-online | English documentation of the online bid submission flow |
| RMI services portal | https://www.gov.il/en/service/my-ramitech | "My ILA" -- view participated tenders, mailings, exercise bid wins |
| Reservist land discount (Kol Zchut) | https://www.kolzchut.org.il/he/הנחה_לחייל_מילואים_ברכישת_קרקע_למגורים | Discount rates by priority area, caps, lease-fee reduction, qualifying reserve service |
| Dira BeHanacha rules (Kol Zchut) | https://www.kolzchut.org.il/he/דירה_בהנחה_(מחיר_למשתכן) | Eligible populations, chasrey dira definition, upgrader rule, priorities, periphery grant |

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
