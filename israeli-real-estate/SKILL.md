---
name: israeli-real-estate
description: Not legal advice. Israeli real estate data, comparable-sales analysis, transaction guidance, and regulatory compliance. Use when user asks about Israeli property, "nadlan", "dira", apartment prices, purchase tax (mas rechisha), Tabu extract, rental agreements, mortgage (mashkanta), or Israel Land Authority tenders. Covers buying, selling, and renting in Israel. Do NOT use for non-Israeli real estate markets, and do NOT use to decode a Tabu extract entry by entry (use israeli-tabu-extract-decoder for what each ownership share, mortgage rank, ikul, he'arat azhara, easement and hatzmada actually means).
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Network access helpful for data lookups. Enhanced by remy-land-authority MCP for land tenders.
---

# Israeli Real Estate

## Legal notice

This is a free information tool operated by an AI model. It explains Israeli real estate processes and presents data that has been published to the public. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a licensed real estate appraiser, advocate, or tax adviser. The output is not a property appraisal (shuma), not a professional opinion, and not legal or tax advice, but general information only: it involves no site visit, it does not perform the appraisal adjustments required by the comparison approach, and it does not examine the documents of your specific transaction. An AI model may err, omit data, or present a wrong conclusion.

The output must not be presented as a certified appraisal, must not be relied on as evidence, and must not be submitted to a court or an authority. A binding valuation requires a licensed appraiser, a property transaction requires an advocate, and a binding tax computation requires a tax adviser or accountant. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and all use of its output is the user's sole responsibility.


## Instructions

### Step 1: Identify Real Estate Need
| Need | Action |
|------|--------|
| Comparable-sales analysis | Present reported and published transactions, not an appraisal |
| Buying guidance | Full transaction checklist |
| Purchase tax calculation | Apply mas rechisha brackets |
| Tabu extract | Guide through obtaining nesach tabu |
| Rental agreement | Key terms for Israeli chozeh schirut |
| Land tender | Query RMI tender data |

### Step 2: Purchase Tax (Mas Rechisha) Calculator
For apartment purchases. Purchase-tax bracket amounts are normally CPI-updated every 16 January, but these ones are NOT: the 2025 Arrangements Law froze them, and ITA purchase-tax circular 1/2026 (18 January 2026) republishes the same amounts for 16.1.2025 to 15.1.2028. So the figures below are the frozen 16.1.2025 vintage and are the live 2026 figures. Re-verify after 15 January 2028, and re-verify the additional-home ladder after 31 December 2026 (see the temporary-order note below):

**First apartment buyer (dira yechida):**
| Price Range (NIS) | Tax Rate |
|-------------------|----------|
| 0 - 1,978,745 | 0% |
| 1,978,746 - 2,347,040 | 3.5% |
| 2,347,041 - 6,055,070 | 5% |
| 6,055,071 - 20,183,565 | 8% |
| 20,183,566+ | 10% |

**Who qualifies for the single-home ladder (check before quoting it):**
- **Israeli residents only.** The ladder is for an Israeli-resident individual (section 9(c1c)(2)). A foreign resident buying their only Israeli home pays the additional-home rate, unless they become a first-time or veteran returning resident within 2 years of the purchase (section 9(c1c)(4)(b)); that 2-year window is also covered by the 2026 war extension below.
- **Single home means the buyer's only home in Israel and the Area.** The buyer, a spouse (unless living permanently apart) and children under 18 (other than a married or orphaned child) count as ONE buyer (section 9(c1c)(4)(c)), so a buyer whose spouse already owns a home is not buying a single home.
- **Homes that do not count:** a home let under protected tenancy before 1 January 1997, or a home in which the buyer's share is one third or less (one half or less if inherited) (sections 9(c1c)(4)(a) and 49c(3)).

**Land and non-residential property are not on these ladders.** A vacant plot (including an Israel Land Authority tender plot), an office, a shop or other non-residential property pays 6% of the whole value (Regulation 2(1)). For land with a plan that permits at least one dwelling, one sixth of that tax is refunded if a permit for at least one dwelling is issued within 24 months of the purchase and the tax was not deducted for income-tax purposes (Regulation 2(1a)).

**Gifts:** a no-consideration transfer from an individual to a relative pays one third of the ordinary purchase tax (Regulation 20), and a no-consideration transfer of a residential home to a spouse who lives in it with the transferor is exempt (Regulation 21).

**Non-first apartment (investment/additional):**
| Price Range (NIS) | Tax Rate |
|-------------------|----------|
| 0 - 6,055,070 | 8% |
| 6,055,071+ | 10% |

**New immigrant (oleh chadash), single residential home:** under Purchase Tax Regulation 12a, an oleh buying a single residential home gets:
| Price Range (NIS) | Tax Rate |
|-------------------|----------|
| 0 - 1,978,745 | 0% |
| 1,978,746 - 6,055,070 | 0.5% |
| 6,055,071 - 20,183,565 | 8% |

**The relief has a value ceiling.** If the home is worth MORE than 20,183,565 NIS, Regulation 12a does not apply at all: the purchase is taxed under the ordinary brackets (the first-home or additional-home ladder above, as applicable) on the FULL price, not under the oleh ladder with a 10% top band. ITA purchase-tax circular 1/2026 (18 January 2026), footnote 1 to the Regulation 12a table: "בדירה ששוויה מעל סכום זה, ההקלה שבתקנה 12א לא תחול". Do not tell an oleh buying a 21M NIS home that they still get the 0% and 0.5% steps, they get none of them.

The oleh benefit is granted once only, applies only to a single residential home (not an investment apartment), and is available from one year before aliyah to seven years after.

Note: investors pay 8% from the first shekel (no exemption).

**The 8%/10% additional-home rates are a temporary order (hora'at sha'a) under section 9(c1f), in force through 31 December 2026**, using tier amounts frozen at the 16 January 2025 level. As of 30 September 2026 no extension has been enacted: circular 1/2026 still gives 31 December 2026 as its end date, and the Finance Minister's power to extend by order has already been used once. Two things complicate a purchase around the turn of the year:
- **Elections.** Knesset elections are due in late October 2026, and section 38 of Basic Law: The Knesset keeps in force any enactment that would expire within the first three months of the incoming Knesset's term, until those three months end. The press (Bizportal, 6 September 2026) reads this as carrying the 8%/10% rates into the first months of 2027. That is a press reading, not an ITA ruling, so present it as expected, not certain.
- **If the order does lapse,** the permanent additional-home ladder in section 9(c1c)(1) returns, which is LOWER and starts at 5% (5% up to 1,465,800 NIS, then 6%, 7%, 8% and 10%).

For an additional home bought in late 2026 or in 2027, check the ITA site for the status on the purchase date before relying on the 8%-from-the-first-shekel rate.

**Reduced rate for people with disabilities, the blind, terror/hostility victims, and bereaved families:** Purchase Tax Regulation 11 gives a reduced purchase-tax track to a person with a qualifying disability (nacheh), a blind person, a victim of hostile action (nifga), and a family member of a soldier who fell in action. Two cases:

| Case | Tax |
|------|-----|
| A qualifying single home (dira yechida) worth up to 2,500,000 NIS | 0% on the value up to 1,978,745 NIS, then 0.5% on the remainder |
| Anything else (not a single home, or a single home worth more than 2,500,000 NIS) | 0.5% of the WHOLE value, from the first shekel |

The relief is given for a home bought "for their housing" (le-shem shikunam), so it is not available on an investment purchase. Where a couple buys together and only ONE of them qualifies, Regulation 11(b) extends the 0.5% charge to BOTH spouses.

Three things people get wrong here:
- The 2,500,000 NIS line is a cliff, not a bracket edge. At exactly 2,500,000 NIS only the part above 1,978,745 NIS is taxed at 0.5%. One shekel more and the 0.5% applies to the whole value, which is roughly five times the tax.
- The 0.5% track is granted to one person **at most twice in a lifetime** (Regulation 11(a)).
- The reduced rate is not automatic. You file a request for a partial purchase-tax exemption with the Israel Tax Authority, and several of the eligibility routes require a Bituach Leumi medical committee first.

The 1,978,745 NIS figure is the section 9(c1c)(3)(a) amount, frozen to 15.1.2028. Verify the eligibility conditions with the Israel Tax Authority before quoting a number.

**Trading up (mishaprei diyur): you are still on the single-home ladder.** A buyer who already owns one home but is replacing it is taxed at the SINGLE-home rates, not the additional-home rates, provided the old home is sold within the statutory window: 18 months if the replacement was bought between 01.06.2023 and 31.05.2025, otherwise 24 months, and 12 months from the contractual handover date when buying new from a developer. You must declare the intention to sell when you report the purchase. Do not quote an upgrader the 8%-from-the-first-shekel rate.

**War extension ("Sha'agat HaAri"):** under the 2026 deadline-extension law (ITA circular 2/2026, 30 March 2026), if the sale window overlaps even one day of 28.2.2026 to 31.5.2026, its last day moves by 3 months, counted from the later of the original last day or 31.5.2026. Example from the circular: a replacement home bought 30.4.2025 had to sell the old home by 31.10.2026, and now has until 31.1.2027. The same extension covers the replacement-home route to the single-residence mas shevach exemption. The Finance Minister may lengthen the 28.2 to 31.5.2026 period further, in steps of up to 3 months and up to 9 months in total, so check the ITA site before relying on a deadline.

### Step 3: Buying Process Checklist
1. **Pre-approval:** Get mortgage pre-approval (ishur ikroni) from bank. Bank of Israel caps the loan-to-value (LTV): up to 75% for a first/sole home, 70% for a replacement home (selling your existing one), and 50% for an investment/additional property. Plan the down payment accordingly.
2. **Property search:** View properties, check neighborhood
3. **Attorney:** Hire real estate attorney (orech din mikrkain) BEFORE signing
4. **Tabu check:** Attorney obtains Tabu extract to verify ownership, liens
5. **Negotiation:** Agree on price, payment schedule
6. **Contract:** Sign purchase agreement (chozeh mcher)
7. **Purchase tax:** File declaration within 30 days of signing, pay within 60 days
8. **Mortgage:** Finalize with bank, appraiser visit
9. **Registration:** Attorney registers transfer in Tabu
10. **Possession:** Key handover per contract schedule

### Step 4: Tabu Extract (Nesach Tabu)
A Tabu extract shows:
- **Part 1:** Property description (gush, chelka, tat-chelka)
- **Part 2:** Registered owners and shares
- **Part 3:** Mortgages (mashkantaot)
- **Part 4:** Liens, warnings (hearot azhara), court orders

**How to obtain:**
- Online: the Land Registry online extract service at `https://www.gov.il/he/service/land_registration_extract` (portal: `https://mekarkein-online.justice.gov.il/voucher/main`). Fees are index-linked and are set in תקנות המקרקעין (אגרות); check the current amount on the government payments catalogue rather than relying on a figure quoted in an article, which in this domain is usually stale.
- Full extract: Through attorney or in-person at the Land Registry office
- Required info: Gush (block) and Chelka (parcel) numbers

**Reading the extract itself is a separate job.** This skill tells you what an extract is for and how to obtain one. For what each line on it MEANS, entry by entry (ownership shares, mortgage ranks and vacated ranks, attachments, caveats and their limits, consent-required notes, easements, attachments of common property, and whether the register is conclusive or merely prima facie evidence for this land), use `israeli-tabu-extract-decoder`.

### Step 5: Betterment Tax (Heitel Hashbacha)
Betterment tax is a municipal levy of 50% of the rise in property value caused by a planning action (new or amended zoning plan, a granted variance, or a use permit).
- **When it crystallizes:** the levy is assessed when the betterment plan is approved, but is actually paid at the point of realization (sale of the property or the issuance of a building permit that uses the added rights).
- **Who pays:** the owner at the time of realization, typically the seller.
- **Reductions and exemptions:** the Third Schedule to the Planning and Building Law sets the levy at one quarter of the betterment for a residential pinui-binui (evacuation and reconstruction) plan (section 3a, with transition rules), and section 19 lists exemptions, including a building permit issued under Tama 38 (with a quarter-rate levy on additions beyond 2.5 extended typical floors). Always check the specific plan and the municipality's policy.
- Factor this into renovation ROI and sale-price math, it can be a large unplanned cost.

Do NOT confuse betterment tax (heitel hashbacha, a municipal levy on a planning-driven value rise) with capital-gains tax on sale (mas shevach), covered next. They are different taxes with different authorities.

### Step 5b: Seller Capital Gains Tax (Mas Shevach)
When you SELL Israeli real estate, the seller (not the buyer) may owe mas shevach, the land-appreciation (capital-gains) tax, on the real gain between purchase and sale. This is the biggest tax a seller faces and is separate from the buyer's purchase tax and from betterment tax.
- **Rate:** 25% on the real gain (the gain after deducting the CPI-linked inflation component and allowable expenses such as purchase tax, agent and lawyer fees, and improvements).
- **Linear exemption for pre-2014 holdings:** for a residential home bought before 1 January 2014, the portion of the gain attributable to the period before that date is exempt, and only the portion from 1 January 2014 onward is taxed at 25% (the "linear" split by holding period). The linear benefit has NOT been abolished generally. Section 48a(b4) withdraws it only for a narrow case: land on which no dwelling stood both when it was bought and on 1 June 2023, where the dwelling was completed after 31 December 2030. Do not tell an ordinary pre-2014 owner that the linear exemption ends in 2030.
- **Single-residence exemption:** a seller of a qualifying residential home that was their only home and was held at least 18 months before the sale can be fully exempt on the sale, subject to a value ceiling of 5,008,000 NIS (1.1.2025 to 31.12.2027, per ITA circular 1/2026). The part of the value above the ceiling is taxed. Legal source: Land Taxation Law sections 49a(a1) and 49b.
- File the mas shevach declaration with the Israel Tax Authority within 30 days of the sale. Because the exemptions and expense deductions are technical, route a real seller to a CPA or real-estate lawyer before quoting a net figure.

### Step 6: Rental Agreement Key Terms
Israeli rental contracts (chozeh schirut) must include:
- Duration and renewal terms
- Monthly rent amount and payment method
- Security deposit (pikadon): all guarantees together are capped at the LOWER of 3 months' rent or the rent for one third of the lease term (section 25j(b)), and must be returned within 60 days of the tenant handing the apartment back (or once the tenant's debts under the lease are settled, if later)
- Running costs: by law the tenant pays arnona, utilities (water, electricity, gas, heating) and routine vaad bayit maintenance, and cannot be charged building insurance, the purchase or upgrade of fixed systems, or a broker who acted for the landlord (section 25i)
- Maintenance responsibilities
- Termination conditions and notice period
- Option to extend and rent adjustment terms

IMPORTANT: the "Fair Rent" amendment to the Rental and Borrowing Law (2017) has applied to residential leases since 17 September 2017. It does not apply to every lease: excluded are, among others, leases of 3 months or less with no extension option, leases of more than 10 years that the landlord cannot end earlier, and leases with monthly rent above 20,000 NIS (the statutory figure, CPI-updated every 1 January).

## Examples

### Example 1: Purchase Tax Calculation
User says: "I'm buying my first apartment for 2.5 million shekels"
Result: Mas rechisha breakdown: 0% on the first 1,978,745 + 3.5% on 368,295 (up to 2,347,040) + 5% on the remaining 152,960 = 20,538 NIS (effective rate ~0.82%)

### Example 2: Buying Process
User says: "I want to buy an apartment in Tel Aviv, what do I need to know?"
Result: Full checklist with Tel Aviv specific notes (high prices, urban renewal projects, tama 38)

### Example 3: Rental Agreement Review
User says: "Review my Israeli rental contract for common issues"
Actions:
1. Check for required clauses under the 2017 Fair Rent amendment
2. Verify arnona responsibility
3. Vaad bayit obligations
4. Deposit terms
5. Early termination conditions
Result: a general checklist of which of these clauses appear in the contract and which do not, with points to raise with a lawyer before signing. This is not a legal review of the contract.

## Bundled Resources

### Scripts
- `scripts/calculate_mas_rechisha.py` - Calculate Israeli purchase tax (mas rechisha) with full bracket-by-bracket breakdown for all four documented tracks: first apartment (dira yechida), non-first apartment, new immigrant single home (Regulation 12a, including the 20,183,565 NIS relief ceiling), and the Regulation 11 reduced track for people with disabilities, the blind, hostility victims and bereaved families. Includes effective tax rate and JSON output option. Run: `python scripts/calculate_mas_rechisha.py --help`

### References
- `references/transaction-guide.md` - Step-by-step Israeli property buying checklist (from pre-approval through key handover), the purchase tax brackets frozen 16.1.2025 to 15.1.2028 for first and non-first apartments, Tabu extract section descriptions (gush, chelka, mortgages, liens), and key transaction cost breakdown (attorney, agent, mortgage fees). Consult when guiding users through the purchase process or calculating total acquisition costs.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [Nadlan MCP](https://agentskills.co.il/he/mcp/nadlan) | Live lookup of historical residential sale prices by gush/chelka or address from the Israel Tax Authority Nadlan database. Replaces manual searches on nadlan.gov.il. |
| [Remy Land Authority](https://agentskills.co.il/he/mcp/remy-land-authority) | Query Israel Land Authority (רמ״י) tenders, geographic data, and settlement records programmatically. Covers the Rami system this skill references in Step 1. |

## Gotchas
- Israeli real estate transactions involve a purchase tax (mas rechisha) that varies by buyer category: first-time buyers get reduced rates, investors pay higher rates starting from the first shekel. Agents may apply a single flat rate.
- The Tabu (Land Registry) and the Israel Land Authority (Rami) are two separate systems. Not all properties are registered in the Tabu; some are in the Rami system only. Agents may search only one system.
- Real estate prices in Israel are commonly quoted in USD for large transactions and NIS for rent. Agents may confuse the currency or forget to specify which is being used.
- Israeli property improvements (hashbacha) can trigger betterment tax (hetel hashbacha) of up to 50% of the value increase. Agents may overlook this additional cost when calculating renovation ROI.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Land Registry extract service (Tabu) | https://www.gov.il/he/service/land_registration_extract | Order an extract online, gush/chelka lookup, and the current fee |
| תקנות המקרקעין (אגרות) | https://he.wikisource.org/wiki/תקנות_המקרקעין_%28אגרות%29 | The statutory fee items for each extract category |
| Israel Land Authority (Rami) | https://www.gov.il/he/departments/israel_land_authority | Rami-registered properties, long-term leases |
| Israel Tax Authority -- real estate tax | https://www.gov.il/he/service/real_eatate_taxsimulator | Purchase tax (mas rechisha) simulator and current brackets |
| Nadlan (Tax Authority transactions) | https://www.nadlan.gov.il | Historical sale prices for Israeli residential properties |
| Discounted housing (Dira BeHanacha) | https://www.gov.il/he/departments/topics/dira/govil-landing-page | Reduced-price apartment program eligibility and listings |

## Troubleshooting

### Error: "Cannot access Tabu online"
Cause: Online Tabu has limited public access
Solution: Use an attorney or Tabu office for full extracts. Online gives basic ownership info only.

### Error: "Purchase tax rates outdated"
Cause: Bracket amounts are normally CPI-updated every 16 January (frozen to 15.1.2028), and the additional-home rates are a temporary order ending 31.12.2026
Solution: Verify the brackets for the purchase date at the Israel Tax Authority website.