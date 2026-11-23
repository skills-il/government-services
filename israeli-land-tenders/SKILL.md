---
name: israeli-land-tenders
description: Not a property appraisal and not an appraiser's opinion. Israeli Land Authority (RMI) tender data, land allocation guidance, and bid process navigation. Use when user asks about Israeli land tenders, "michraz", "rashut mekarkei yisrael", RMI, Israel Land Authority, government land auctions, "haktzaah", land lottery ("hagralah"), "Dira BeHanacha" sub-tracks (Mechir Lamishtaken, Mechir Matara, Mechir Muphchat, Dira Lehaskir), lottery eligibility, reservist priority or reservist land discounts ("Mimiluim LaMafteach"), resale lockup, building rights, or state land allocation. Enhances remy-land-authority MCP server with tender process guidance and Hebrew terminology. Do NOT use for private real estate transactions (use israeli-real-estate skill instead) or non-Israeli land systems.
license: MIT
allowed-tools: WebFetch
compatibility: Network access helpful for tender data lookups. Enhanced by remy-land-authority MCP server.
---

# Israeli Land Tenders (RMI)

## Legal notice
This skill is a free information tool operated by an AI model. It explains how Israel Land Authority tenders and the Dira BeHanacha lotteries work and applies the published rules to the details you give it, with no involvement, review or approval by a lawyer or a licensed real estate appraiser. Its output is not a land appraisal (shuma), not legal advice or a legal opinion, not a professional opinion and not a decision on your eligibility. It is general information and a preliminary check against published rules only: it does not inspect the plot, does not perform appraisal adjustments, and does not review the full tender booklet or your personal documents. An AI model can err, omit data or reach a wrong conclusion. Do not present the output as an appraisal, rely on it as evidence, submit it to a court or authority, or base a bid on it; those uses require a licensed appraiser or a lawyer. Eligibility is decided by the Ministry of Construction and Housing and by RMI, and the tender booklet prevails. This tool is not a substitute for advice that takes into account the particular data and needs of each person, and any use of its output is your sole responsibility.

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
| Tender analysis | Interpret conditions and list the factors to review |
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
- Open competitive bidding
- Bidders submit sealed or online proposals; the highest qualifying bid is declared the winner unless the booklet sets additional rules
- Most common for large residential and commercial projects
- Requires financial capacity; the booklet states any experience or threshold conditions
- Bid guarantee (arbon): an autonomous bank guarantee. The default formula is 10% of the land value (before development costs and area discount) or 10% of the development costs, whichever is higher, rounded down to the nearest 1,000 NIS. The tender committee may set a different amount, so the figure in the booklet is the one that binds

**Lottery (Hagralah)**

The word covers two separate systems, so identify which one the user means:
- **Dira BeHanacha** (formerly "Mechir Lamishtaken", מחיר למשתכן): apartments in developer projects. The Ministry of Construction and Housing runs eligibility, registration and the draw at `dira.moch.gov.il`. RMI only supplies the land through a tender.
- **RMI self-build registration and lottery (harshama vehagrala)**: residential plots, run under the RMI tender booklet rather than the Housing Ministry site. The priority order is in `references/lottery-and-reservist-rules.md`.

Dira BeHanacha tracks:
- **Mechir Matara** (marketed through 31.12.2027): the developer must discount the computed apartment price by 25%, up to 550,000 NIS per unit. Projects tendered under earlier versions of the decision can carry other terms, so confirm the discount on the project page.
- **Mechir Lamishtaken** and **Mechir Muphchat**: earlier tracks whose projects still appear. Read the price and specification off the project page.
- **Dira Lehaskir**: long-term regulated rental, not purchase. Through 31.12.2029 first priority goes to active reservists and to bereaved widows and widowers of security-forces fallen or hostile-action victims, combat reservists first.

Check these gates, in order, and present them as published conditions the household can compare itself against. The Ministry decides eligibility:
1. **IDF status (since 24.05.2026)**: a person may join a lottery only if IDF data does not define them, or either spouse, as draft-obligated without a regularised status. This blocks entry even with a valid certificate, and the check can run after registration closes. Maof reports the Ministry is also applying this to people waiting from past lotteries, so anyone in that position should ask their registration company before relying on a win.
2. **Eligible population** (Israeli citizens): married or common-law couples (including an Israeli whose partner is a foreign resident), couples marrying within 3 months of applying, a parent of an unmarried child under 21 (pregnant from the fifth month counts), widows and widowers **at any age**, single or divorced people aged 35+, and singles aged 21+ with a permanent medical disability of 75% or more; or a permanent medical disability above 50% with mobility and special-services benefits (Kol Zchut says at least 50%, so a person at exactly 50% should confirm); or a permanent 50%+ disability with hostile-action or Defence Ministry payments.
3. **Existing property (chasrey dira or upgrader)**: Owning or holding rights in an apartment or land, including partial shares, key money, rights under construction or purchase-group rights, can affect eligibility. The rules and thresholds differ by type of right and by whether the applicant is a first-time buyer or an upgrader. Check the specific holding against the current Israel Land Council decision (sub-chapter 4.7, https://apps.land.gov.il/CouncilDecisions/assets/data/96/CouncilDecisions.pdf) or with the Housing Ministry or a registration company before applying. A household that already bought through an affordable-housing program cannot join again.
4. **Valid certificate (teudat zakaut)**: required on registration day and again when choosing the apartment, matching the household's current status, or the win cannot be used. Issued through a registration company (Alonim, Milgam, Maof), valid one year. New 200 NIS. Renewal 50 NIS within 60 days of the reminder; after that it is cancelled and a new 200 NIS certificate is needed at a branch. Winners renew for 50 NIS even after expiry. **Apply before a round is announced**: issue can take up to 10 working days, Maof currently warns of longer, and a round can close certificate issue before registration closes (reported for Lottery 11: 7 June against 22 June).

Then:
- **Upgraders (mishaprey diur)**: first-time buyers come first. One year after a project's first lottery, units they did not take are sold on the same terms to upgraders (a family unit, a widow or widower, or an individual 35+). An upgrader who still owns an apartment must sell it no later than 12 months after occupancy approval of the new one. The existing-property check in gate 3 applies to upgraders too. Maof states that the November 2026 continuation lotteries were open to upgraders; confirm per round.
- **Round mechanics**: registration opens for at least 8 days; the draw follows within 10 days of closing; a win cancels other registrations. A winner can cancel online before signing with the contractor, which takes up to 72 hours, so cancel at least 72 hours before another lottery closes. First-series registrants may pick projects in at most 3 localities; continuation series have no locality limit.
- **Priorities, in order**: (1) wheelchair-bound applicants, one unit per 30; (2) active reservists, up to 50% of units in national-priority localities at periphery index 1-4 (up to 25% combat first) and up to 35% elsewhere (up to 15% combat first); (3) local residents, up to 20%. Together at most 73%. Lottery 11 had a one-time 50% rule in all localities. Maof states that the November 2026 continuation lotteries had no priorities; confirm per round. On the confrontation line the local-resident share can reach 60% through 31.12.2028.
- **Reservist test for the lottery**: at least 60 days under Order 8 since 07.10.2023. For Lottery 11 the counted window was published as ending 30.04.2026, so confirm the current round's cutoff with the IDF reserve centre (1111 extension 4). The IDF supplies the data after registration closes, with time to appeal before the draw.
- **Financing**: mortgage up to 75% of the price for chasrey dira and 70% for upgraders, with own equity of at least 60,000 NIS for periphery-grant recipients and 100,000 NIS otherwise. Banks may use an appraisal value, with a 2.1 million NIS rule. Check feasibility before registering.
- **Periphery grant (not universal)**: a conditional grant structured as a loan forgiven at the end of the 5 or 7 year commitment. Mechir Lamishtaken 40,000 or 60,000 NIS by locality; Mechir Muphchat and Mechir Matara 40,000 NIS. Paid through the mortgage bank after signing; buyers with no mortgage obtain a certificate from a mortgage bank.
- **Resale lockup**: no **sale** (including a transfer for free or at a reduced price) for **5 years from the completion certificate (teudat gmar) OR 7 years from the lottery, whichever comes first**. Kol Zchut words the first trigger as Tofes 4, so confirm the end date in the signed undertaking. For a unit bought outside a lottery (a leftover unit), the "lottery date" is the date the sale agreement was signed. A transfer inside the period needs Housing Ministry approval, and the seller repays the discount, linked to the CPI from possession. The clause does not mention renting, so check the undertaking before saying renting is allowed or banned.
- **Current round**: never present a past round as open. Lottery 11 ran in May-June 2026 and has closed. Continuation lotteries in Harish, Dimona, Haifa and Beit Shean (about 101 units) took registrations from 03.11.2026 until mid-November. Check `dira.moch.gov.il` and the registration companies for what is open today.
- **Choosing the apartment**: winners are called in draw order and typically get about 45 minutes to choose. An advance (2,000 NIS, or another amount set at registration) may be required and is not refunded if the win is cancelled after choosing.

**Reservist land discount and separate IDF-disabled benefits (RMI, not part of Dira BeHanacha)**
RMI gives active reservists a one-off discount on **low-rise** residential land, for one dwelling unit. It is not an extra discount on a Dira BeHanacha apartment. Legal basis: sub-chapter 4.2, Sign B, of the Israel Land Council decisions.

| Route | Benefit | Cap (excl. VAT) |
|---|---|---|
| Lottery or tender-exempt allocation | Discount by national-priority area: 35% in area A, 20% in area B, 10% elsewhere | 100,000 NIS active reservist / 150,000 NIS combat reservist |
| Public tender win | 15% off the price bid, applied after the winner is determined | Same caps |
| Purchase through an association (amuta) that won a public tender | 15% refund on the member's land share | Same caps |

- **Who qualifies** (a different test from the lottery): a six-year active-reservist certificate; or at least 6 years on the reserve roster plus 80 reserve days since 2000 within up to 6 consecutive calendar years; or more than 45 reserve days between 07.10.2023 and the declared end of the Iron Swords war.
- **Timing**: eligibility must exist by the deal's payment dates or 90 days from deal approval, whichever is earlier, so file before the first payment. Use is possible up to 6 years from discharge (routes 1 and 2) or from the end of that war service (route 3). Kol Zchut still shows 3 years for the certificate route, so a user between years 3 and 6 should get written confirmation from RMI.
- **Stacking and spouses**: discounts can combine unless RMI management excluded the combination, so confirm in writing. If both spouses qualify, each gets the full discount with their own cap, up to 300,000 NIS for two combat reservists.
- **IDF-disabled buyers**: a wounded reservist should check the reservist discount under Council section 4.2.12 with RMI. The 31% tender-exempt plot applies only at 100% special disability. The IDF-disabled sub-priority in a self-build lottery applies at 100% or 100% special disability. A self-build lottery also has a priority tier for people with disabilities under an RMI definition, so a veteran at a lower rating should ask RMI.
- **Self-build lotteries**: "chasar diur" means holding a Housing Ministry chasar diur eligibility certificate. It drives the priority tier, the reduced rate and the higher ceiling, so obtain it in time and check the booklet for the date it must be held by.
- **Lease fees, area exceptions, self-build priority order, reservist-only plots, IDF-disabled and bereaved-family benefits**: see `references/lottery-and-reservist-rules.md`. Read it before quoting a lease rate: the reduced rates have land-value ceilings (500,000 / 900,000 NIS) and locality conditions.
- **To claim**: a declaration of reserve service signed before a lawyer plus the relevant IDF confirmation (IDF reserve centre, 1111 extension 4), and for combat reservists also the summary of qualifying days, filed at the RMI regional office. RMI enquiries: 03-9533333 or *5575, Sunday to Thursday 08:00-17:00.

**Price Buyer (Mechir Larocheish)**
- Legacy term: the current Israel Land Council decisions (version of 04.08.2026) contain no track by this name, so do not describe eligibility, price or lockup rules for it
- A user who says this usually means Dira BeHanacha or a self-build plot by registration and lottery. Identify which one, then use that track's rules

**Direct Allocation (Haktzaah Yeshira)**
- No competitive process, allowed only under an exemption in the Mandatory Tenders Regulations, 1993
- Covers public institutions and public needs, and also specific private cases such as the IDF-disabled plot in the reference file
- The exemption and its conditions are specific to each case, so confirm them with RMI

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
   - Minimum price: usually published, as a share of RMI's estimate: 50% for low-rise; 35% for saturated housing, **rising to 50% if fewer than 3 qualifying bids arrive**; 25% for saturated housing in national-priority areas and Jerusalem, for low-rise in national-priority areas or approved localities, and for tenders with subsidised development, **rising to 35% with fewer than 3 bids**. RMI management can set other rules, so read the booklet and check a bid against the higher threshold. Mechir Matara tenders have no minimum for the residential component
   - Bid guarantee (arbon): the amount stated in the booklet, given as an autonomous bank guarantee (digital in online bids)
   - Development costs: stated separately in the tender where they apply
   - Charges and levies: the booklet states which apply and who bears them
   - Apartment pricing: in residential tenders the buyer's payment may not be CPI-linked or bear interest, except construction-input indexation on the building component as defined in the booklet
   - Bidder limits: a contractor designated as a registration refuser (sarvanit rishum) is barred unless it completes registration or posts a 100,000 NIS guarantee

3. **Prepare required documents**
   - Company registration (if corporate bidder)
   - Financial statements or bank guarantees
   - Signed tender conditions acceptance
   - Bid form with proposed price
   - Autonomous bank guarantee

4. **Factors to review before you set your own bid**
   - Published results of comparable tenders in the area, shown as data
   - Building rights, location, costs, financing, taxes, levies, profit and risk, for the user's own appraiser or financial adviser
   - Do not state a land value, residual value, maximum bid, bid range or recommended amount, even if the user supplies every input

5. **Submit before deadline**
   - RMI operates an online submission system at `apps.land.gov.il/MichrazimSite/`, entered through the national identification system. The booklet states whether online submission is available or required. The service is free.
   - Online bids deposit a DIGITAL guarantee. A later bid by the same user replaces the earlier one, and only the last bid is considered.
   - Support: RMI call centre *5575 (Sunday to Thursday 08:00-17:00); technical faults 073-3429900 (09:00-14:00). On the closing day, gov.il says support is answered only until 10:00, so do not leave submission to the last hours.
   - Some specialty tenders still require physical submission in a sealed envelope to the regional RMI office; the tender booklet specifies the required channel -- always verify per tender.
   - An online bid not recorded in the system by the deadline, for any reason, is not accepted. Check the booklet for other channels.

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

**No value calculation.** Do not compute what a plot is worth. For a user screening a tender, list the items to take to their own appraiser or financial adviser: built area, expected sale prices, development and construction costs, levies, financing, taxes, profit and risk. A valuation (shuma) must come from a licensed appraiser (shamai mikrkain).

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
Result: Query the remy-land-authority MCP (or `apps.land.gov.il/MichrazimSite/`) for Beer Sheva residential tenders. Present active tenders with: tender number, exact location, plot size, building rights, minimum price, and submission deadline.

### Example 2: Lottery Guidance
User says: "How do I apply for mechir lamishtaken?"
Result: Clarify that "Mechir Lamishtaken" is now one sub-track inside the umbrella program **"Dira BeHanacha" (דירה בהנחה)** operated by the Ministry of Construction and Housing (not RMI directly). Walk through: (1) the sub-tracks (Mechir Lamishtaken, Mechir Matara, Mechir Muphchat, Dira Lehaskir) and that Mechir Matara is a 25% discount capped at 550,000 NIS per unit, (2) the entry gates in order: IDF status since 24.05.2026, eligible population, existing property, (3) the eligibility certificate from a registration company (200 NIS new, 50 NIS renewal, valid one year), obtained before a round opens, (4) registration at `dira.moch.gov.il` for a round that is currently open (never assume a past round is still open, verify on the site), (5) the priority order, the 60-day reservist test, and that priorities may not apply in continuation lotteries, and (6) the resale lockup of 5 years from the completion certificate (teudat gmar; Kol Zchut says Tofes 4, confirm in the signed undertaking) or 7 years from the lottery, whichever comes first. If the user is a reservist, also mention the separate RMI discount on low-rise land, which is not a discount on a Dira BeHanacha apartment and uses a different service test.

### Example 3: A Question About the Bid Amount
User says: "There's a tender in Netanya, minimum price 15 million, how much should I bid?"
Result: Show published results of comparable Netanya tenders as data, explain how the minimum can rise if fewer than 3 qualifying bids arrive, and list the factors to review. Decline to name any bid amount, range, ceiling or typical premium, and refer the user to a licensed appraiser (shamai mikrkain) and an attorney.

## Bundled Resources

### Scripts
- `scripts/search_tenders.py` - Display RMI tender type descriptions (michraz, hagralah, the legacy term mechir larocheish, haktzaah), step-by-step bid submission guide for public tenders, Hebrew-English terminology glossary for tender documents, and land use category definitions. Supports subcommands: `tender-types`, `bid-guide`, `terminology`, `land-use`. Run: `python scripts/search_tenders.py --help`

### References
- `references/rmi-system-guide.md` - Overview of Israel's state land system (about 93% state or quasi-state owned, leasehold model), tender type comparison table, land use categories with Hebrew terms, building rights terminology (zchuyot bniyah, achuz bniyah, kav binyan), and official RMI portal URLs. Consult when explaining Israel's land ownership model or decoding tender document terms.
- `references/lottery-and-reservist-rules.md` - Other eligibility conditions, draw priorities, the two reservist service tests, land discounts, lease-fee rates and ceilings, the self-build lottery order, and IDF-disabled and bereaved-family benefits. Read before answering a reservist, self-build, or borderline-eligibility question.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [remy-land-authority](https://agentskills.co.il/he/mcp/remy-land-authority) | Live programmatic access to RMI tender listings, filters by location/land-use/status, and structured tender metadata. Pair with this skill when the user needs real data, not just process guidance. |

## Gotchas
- Israeli land tenders (michrazei karka'ot) from the Israel Land Authority (RMI/Rami) are published in Hebrew only. Agents may search for tenders using English location names, which will return no results.
- The minimum price printed in a booklet may not be the effective one: in many residential tenders it rises if fewer than 3 qualifying bids arrive. Agents that call it a fixed floor can steer a bidder below the real threshold.
- Land measurements in Israeli tenders use dunam (1 dunam = 1,000 square meters), not acres or hectares. Agents may convert to international units without noting the original dunam figure.
- Tender participation requires an autonomous bank guarantee. The default is 10% of land value or of development costs, whichever is higher, but the tender committee can change it. Agents may suggest bidding without mentioning this upfront requirement, or quote the default when the booklet says otherwise.
- Israeli land in urban areas is often leased from the state (chakira) long-term (generally 98 years plus a 98-year option by tender, up to 49 plus 49 without one), not purchased outright as in the US. Agents may describe land acquisition using ownership terminology when it is actually a long-term lease.
- The affordable-housing lottery program is administered by the Ministry of Construction and Housing at `dira.moch.gov.il`, not by RMI directly. Agents that point users to the RMI site for lottery registration will send them to the wrong place. RMI tenders the land; the Housing Ministry runs eligibility, registration, and the drawing.
- "Mechir Lamishtaken" is the legacy name; today it is one sub-track inside Dira BeHanacha. **Mechir Matara** is a distinct sub-track with different rules (25% discount capped at 550,000 NIS, 40,000 NIS periphery grant). Treating them as the same program produces wrong eligibility information.
- Dira BeHanacha resale lockup is **5 years from the completion certificate (teudat gmar; Kol Zchut says Tofes 4, confirm in the signed undertaking) OR 7 years from the lottery, whichever comes first**, not a flat number of years. For a unit bought outside a lottery the 7 years run from the sale agreement. Agents that quote "5 years" or "7 years" alone will mislead users on when they can sell. The clause restricts sale, so do not state a rental ban as settled.
- Active reservists have a SEPARATE RMI discount on low-rise land (percentage by national-priority area, capped in shekels), and reservists and 100% IDF-disabled buyers can get plots marketed exclusively to them. It is unrelated to the Dira BeHanacha reservist priority and **uses a different service test: more than 45 days for land, at least 60 days under Order 8 for the lottery**. A reservist can qualify for one and not the other.
- A valid eligibility certificate does not by itself allow lottery entry. Since 24.05.2026 the IDF status of the applicant and any spouse is a separate condition. Agents that stop at the certificate will send an affected household to a lottery it cannot join.
- Lottery rounds open and close on a calendar. A round named in any document, including this skill, may be closed by the time the user asks. Always verify the currently open round on `dira.moch.gov.il` before describing a round as open.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| RMI tender portal (MichrazimSite) | https://apps.land.gov.il/MichrazimSite/ | Active and recent tenders, tender booklets, online bid submission |
| Israel Land Authority (gov.il) | https://www.gov.il/he/departments/israel_land_authority | Official RMI department page, announcements, policy updates |
| RMI land tenders hub | https://www.gov.il/he/departments/topics/land_tenders | Tender system, tender map, and exemption-from-tender information |
| Dira BeHanacha lottery | https://dira.moch.gov.il/ | Current and upcoming affordable-housing lottery rounds, eligibility certificate |
| Online bid submission service | https://www.gov.il/he/service/tenders-online | Online bid rules, digital guarantee, support numbers |
| RMI services portal | https://www.gov.il/en/service/my-ramitech | "My ILA" -- view participated tenders, mailings, exercise bid wins |
| Reservist land discount (Kol Zchut) | https://www.kolzchut.org.il/he/הנחה_לחייל_מילואים_ברכישת_קרקע_למגורים | Discount rates by priority area, caps, lease-fee reduction, qualifying reserve service |
| Dira BeHanacha rules (Kol Zchut) | https://www.kolzchut.org.il/he/דירה_בהנחה_(מחיר_למשתכן) | Eligible populations, chasrey dira definition, upgrader rule, priorities, periphery grant |
| Israel Land Council decisions | https://apps.land.gov.il/CouncilDecisions/assets/data/96/CouncilDecisions.pdf | Binding text (version of 04.08.2026; a newer version may exist): sub-chapters 4.2 (discounts), 4.5 (tenders), 4.7 (Mechir Matara), 4.8 (rental) |

## Troubleshooting

### Error: "Tender not found"
Cause: Tender may have expired, been cancelled, or search terms do not match Hebrew listing
Solution: Search by tender number if known. Try broader location terms. Check if the tender was cancelled (mevutal) or postponed (nidcha). RMI occasionally cancels tenders if no qualifying bids received.

### Error: "Cannot determine eligibility"
Cause: Lottery tracks have specific eligibility criteria
Solution: Each tender defines its own eligibility. Common criteria: no property ownership, age range, specific population group. Check the specific tender booklet (chovert michraz) for exact requirements. For Dira BeHanacha, eligibility is issued by the Housing Ministry as a teudat zakaut, not by RMI.

### Error: "Tender results not published"
Cause: Results publication may be delayed due to objections or committee review
Solution: Check the RMI tender portal under "results" (totz'ot). During the objection period, results may be preliminary.
