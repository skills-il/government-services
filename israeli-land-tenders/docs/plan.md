# Israeli Land Tenders Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for accessing Israeli Land Authority (Rashut Mekarkei Yisrael / RMI) tender data — tender search, bid guidance, land allocation types, and understanding the Israeli land system.

**Architecture:** MCP Enhancement + Domain-Specific Intelligence skill. Enhances the existing `remy-mcp` server with land authority knowledge, tender terminology in Hebrew, bid process guidance, and land allocation type explanations.

**Tech Stack:** SKILL.md, references for RMI tender system, land allocation types, and bid procedures.

---

## Research

### remy-mcp Server
- **Repository:** Community MCP server for RMI (Rashut Mekarkei Yisrael) tender data
- **Function:** Queries Israeli Land Authority tender listings and data
- **Hebrew support:** Handles Hebrew tender descriptions and location names
- **Enhancement opportunity:** Add bid process guidance, allocation type explanations, and tender analysis

### Israel Land Authority (Rashut Mekarkei Yisrael / RMI)
- **URL:** `https://www.gov.il/he/departments/israel_land_authority`
- **Tender portal:** `https://www.rmi.gov.il` (tender publications)
- **Role:** Manages ~93% of Israel's land (state land, JNF land, Development Authority land)
- **Functions:** Land allocation, tender publication, leasehold management, land policy
- **Context:** Since most Israeli land is state-owned, RMI tenders are the primary mechanism for land allocation for development

### Israeli Land System
- **~93% state-owned:** Israel Land Authority manages state, JNF (KKL), and Development Authority land
- **~7% private:** Privately owned (baalut pratit), registered in Tabu
- **Leasehold model:** Most land is leased for 49-98 years (chasichrat dor), not sold
- **Capitalization (hion):** Payment of full lease value upfront, effectively functioning like ownership
- **Reform (2009):** Law allows conversion of leasehold to ownership for residential properties (with conditions)

### Tender Types (Sugei Michrazim)
| Type | Hebrew | Description |
|------|--------|-------------|
| Public tender (michraz) | michraz | Open competitive bidding, highest price wins |
| Lottery (hagralah) | hagrala | Random selection among eligible applicants, fixed price |
| Direct allocation (haktzaah) | haktzaah yeshira | Direct allocation to qualifying entities (e.g., public institutions) |
| Price Buyer (mechir larocheish) | mechir larocheish | Fixed-price allocation with eligibility criteria |
| Urban renewal tender | michraz hitnadsut ironit | For Tama 38 / Pinui-Binui demolition-reconstruction projects |
| Negotiation (mikshar) | mikshar | Negotiated allocation for specific purposes |

### Land Use Categories
| Category | Hebrew | Typical Use |
|----------|--------|-------------|
| Residential (megurim) | megurim | Housing development |
| Commercial (miskhari) | miskhari | Office, retail, mixed-use |
| Industrial (taasiyati) | taasiyati | Factories, logistics |
| Agricultural (chaklai) | chaklai | Farming, orchards |
| Tourism (tayarut) | tayarut | Hotels, resorts |
| Public (tzibburi) | tzibburi | Schools, parks, government |
| Employment (taasuka) | taasuka | Employment zones, high-tech parks |

### Tender Process
1. **Publication:** RMI publishes tender on website and official gazette (reshumot)
2. **Review period:** 30-90 days for prospective bidders to review conditions
3. **Pre-qualification:** Some tenders require proof of financial capability, experience
4. **Submission:** Sealed bids (hatzaot) submitted by deadline
5. **Opening:** Public opening of bids (ptichat hatzaot)
6. **Decision:** Tender committee (vaada) selects winner based on criteria (price and/or quality)
7. **Objection period:** Losing bidders may appeal within defined timeframe
8. **Contract:** Winner signs development agreement with conditions and timeline

### Use Cases
1. **Tender search** — Find current and recent RMI tenders by location and type
2. **Bid guidance** — Understand bid process, required documents, and strategy
3. **Land allocation types** — Explain different allocation methods
4. **Tender analysis** — Interpret tender conditions and estimate competition
5. **Development terms** — Understand building rights, timelines, and conditions
6. **Regional tenders** — Track tenders by specific city or district

---

## Build Steps

### Task 1: Create SKILL.md

```markdown
---
name: israeli-land-tenders
description: >-
  Israeli Land Authority (RMI) tender data, land allocation guidance, and bid
  process navigation. Use when user asks about Israeli land tenders, "michraz",
  "rashut mekarkei yisrael", RMI, Israel Land Authority, government land
  auctions, "haktzaah", land lottery ("hagralah"), building rights, or state
  land allocation. Enhances remy-mcp server with tender process guidance and
  Hebrew terminology. Do NOT use for private real estate transactions (use
  israeli-real-estate skill instead) or non-Israeli land systems.
license: MIT
allowed-tools: "WebFetch"
compatibility: "Network access helpful for tender data lookups. Enhanced by remy-mcp server."
metadata:
  author: skills-il
  version: 1.0.0
  category: government-services
  tags: [land, tenders, rmi, michraz, real-estate, government-land, israel]
  mcp-server: remy-mcp
---

# Israeli Land Tenders (RMI)

## Critical Note
Tender conditions, deadlines, and requirements change with each publication.
Always verify current tender details on the official RMI website. This skill
provides general guidance on the tender system and process — specific tender
terms take precedence over general rules. Recommend users consult a real estate
attorney (orech din mikrkain) before submitting bids on significant tenders.

## Instructions

### Step 1: Identify Land Tender Need
| Need | Action |
|------|--------|
| Search tenders | Query RMI tender listings via remy-mcp |
| Understand tender type | Explain allocation method and implications |
| Bid process guidance | Step-by-step bid submission guide |
| Tender analysis | Interpret conditions, estimate competition |
| Land system explainer | Explain Israel's land ownership model |
| Development terms | Decode building rights and conditions |

### Step 2: Search for Tenders
Use remy-mcp server to search active and recent tenders:

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
- Popular for affordable housing programs (mechir lamishtaken)
- Eligibility criteria: first-time buyers, young couples, specific populations
- "Mechir Lamishtaken" program: Apartments sold below market price via lottery
- Registration fee: Relatively small compared to tender deposits

**Price Buyer (Mechir Larocheish)**
- Fixed price, allocated based on eligibility order
- Used for specific populations: discharged soldiers, new immigrants, residents of specific areas
- Price typically at or below market value
- Conditions on resale (lock-up period, typically 5-10 years)

**Direct Allocation (Haktzaah Yeshira)**
- No competitive process
- For public institutions, government bodies, specific approved projects
- Requires specific government/ministerial approval
- Examples: schools, synagogues, community centers

### Step 4: Bid Submission Guide (for Public Tenders)
Step-by-step process for submitting a tender bid:

1. **Review tender documents**
   - Download full tender booklet (chovert michraz) from RMI website
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
   - Consider minimum price as floor — winning bids often 10-50%+ above minimum
   - Higher competition areas (Tel Aviv, central Israel) command larger premiums

5. **Submit before deadline**
   - Physical submission to RMI office (not typically online)
   - Sealed envelope with all required documents
   - Late submissions are disqualified without exception

6. **Post-submission**
   - Public bid opening (ptichat hatzaot) at announced date and time
   - Results published on RMI website
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
Result: Query remy-mcp for Beer Sheva residential tenders. Present active tenders with: tender number, exact location, plot size, building rights, minimum price, and submission deadline. Note that Beer Sheva typically has lower minimum prices than central Israel.

### Example 2: Lottery Guidance
User says: "How do I apply for mechir lamishtaken?"
Result: Explain the Mechir Lamishtaken lottery program — eligibility criteria (first-time buyers without property, income thresholds, age), registration process, what to expect (random drawing, apartments below market price), resale restrictions (5-year lock-up period), and where to find current lottery publications on RMI website.

### Example 3: Bid Strategy
User says: "There's a tender in Netanya, minimum price 15 million, how much should I bid?"
Result: Explain that bid strategy depends on: recent comparable tender results in Netanya, number of expected bidders, building rights and development costs, current market conditions. Provide framework for analysis but recommend consulting a real estate appraiser (shamai mikrkain) and attorney for specific bid amount. Note that winning bids in Netanya coastal areas are typically 20-40% above minimum.

## Troubleshooting

### Error: "Tender not found"
Cause: Tender may have expired, been cancelled, or search terms do not match Hebrew listing
Solution: Search by tender number if known. Try broader location terms. Check if the tender was cancelled (mevutal) or postponed (nidcha). RMI occasionally cancels tenders if no qualifying bids received.

### Error: "Cannot determine eligibility"
Cause: Lottery and price-buyer tenders have specific eligibility criteria
Solution: Each tender defines its own eligibility. Common criteria: no property ownership, age range, specific population group. Check the specific tender booklet (chovert michraz) for exact requirements.

### Error: "Tender results not published"
Cause: Results publication may be delayed due to objections or committee review
Solution: Results are typically published 1-4 weeks after bid opening. Check RMI website under "results" (tochaot). During objection period, results may be preliminary.
```
