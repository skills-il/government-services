---
name: israeli-real-estate
description: Israeli real estate data, property valuation, transaction guidance, and regulatory compliance. Use when user asks about Israeli property, "nadlan", "dira", apartment prices, purchase tax (mas rechisha), Tabu extract, rental agreements, mortgage (mashkanta), or Israel Land Authority tenders. Covers buying, selling, and renting in Israel. Do NOT use for non-Israeli real estate markets.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Network access helpful for data lookups. Enhanced by remy-land-authority MCP for land tenders.
---

# Israeli Real Estate

## Instructions

### Step 1: Identify Real Estate Need
| Need | Action |
|------|--------|
| Property valuation | Use comparable sales data methodology |
| Buying guidance | Full transaction checklist |
| Purchase tax calculation | Apply mas rechisha brackets |
| Tabu extract | Guide through obtaining nesach tabu |
| Rental agreement | Key terms for Israeli chozeh schirut |
| Land tender | Query RMI tender data |

### Step 2: Purchase Tax (Mas Rechisha) Calculator
For apartment purchases (2026 rates, frozen at 2025 levels; first-apartment brackets are frozen until Jan 15, 2028; verify annually at the Israel Tax Authority):

**First apartment buyer (dira yechida):**
| Price Range (NIS) | Tax Rate |
|-------------------|----------|
| 0 - 1,978,745 | 0% |
| 1,978,746 - 2,347,040 | 3.5% |
| 2,347,041 - 6,055,070 | 5% |
| 6,055,071 - 20,183,565 | 8% |
| 20,183,566+ | 10% |

**Non-first apartment (investment/additional):**
| Price Range (NIS) | Tax Rate |
|-------------------|----------|
| 0 - 6,055,070 | 8% |
| 6,055,071+ | 10% |

**New immigrant (oleh chadash), single residential home:** under Purchase Tax Regulation 12a (the reformed track in force from 15 August 2024), an oleh buying a single residential home gets:
| Price Range (NIS) | Tax Rate |
|-------------------|----------|
| 0 - 1,978,745 | 0% |
| 1,978,746 - 6,055,070 | 0.5% |
| 6,055,071 - 20,183,565 | 8% |

**The relief has a value ceiling.** If the home is worth MORE than 20,183,565 NIS, Regulation 12a does not apply at all: the purchase is taxed under the ordinary brackets (the first-home or additional-home ladder above, as applicable) on the FULL price, not under the oleh ladder with a 10% top band. ITA purchase-tax circular 1/2026, footnote 1: "בדירה ששוויה מעל סכום זה, ההקלה שבתקנה 12א לא תחול". Do not tell an oleh buying a 21M NIS home that they still get the 0% and 0.5% steps, they get none of them.

The oleh benefit is granted once only, applies only to a single residential home (not an investment apartment), and is available from one year before aliyah to seven years after. The reformed track no longer requires the home to be the oleh's actual residence.

Note: The older 12% bracket for properties above 20,183,565 NIS was dropped. Investors pay 8% from the first shekel (no exemption).

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
- Online: the Land Registry online extract service at `https://www.gov.il/he/service/land_registration_extract` (portal: `https://mekarkein-online.justice.gov.il/voucher/main`). A regular online extract costs about 15 NIS. A historical extract is about 74 NIS. A consolidated extract is about 131 NIS. No account needed, extract arrives by email with an electronic signature.
- Full extract: Through attorney or in-person at the Land Registry office
- Required info: Gush (block) and Chelka (parcel) numbers

### Step 5: Betterment Tax (Heitel Hashbacha)
Betterment tax is a municipal levy of 50% of the rise in property value caused by a planning action (new or amended zoning plan, a granted variance, or a use permit).
- **When it crystallizes:** the levy is assessed when the betterment plan is approved, but is actually paid at the point of realization (sale of the property or the issuance of a building permit that uses the added rights).
- **Who pays:** the owner at the time of realization, typically the seller.
- **Reductions and exemptions:** the local authority may reduce the levy to 25% or grant a full exemption in defined cases (urban renewal, certain Tama 38 projects, rehabilitation neighborhoods). Always check the specific plan and the municipality's policy.
- Factor this into renovation ROI and sale-price math, it can be a large unplanned cost.

### Step 6: Rental Agreement Key Terms
Israeli rental contracts (chozeh schirut) must include:
- Duration and renewal terms
- Monthly rent amount and payment method
- Security deposit (pikadon) -- typically 1-3 months, capped by law
- Arnona (property tax) -- clarify who pays
- Vaad bayit (building maintenance) -- clarify who pays
- Maintenance responsibilities
- Termination conditions and notice period
- Option to extend and rent adjustment terms

IMPORTANT: Since 2022, the Rental Law (Fair Rent) applies to some properties. Check applicability.

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
1. Check for required clauses under the 2022 Fair Rent Law
2. Verify arnona responsibility
3. Vaad bayit obligations
4. Deposit terms
5. Early termination conditions
Result: Checklist of compliant vs. missing clauses with recommendations.

## Bundled Resources

### Scripts
- `scripts/calculate_mas_rechisha.py` - Calculate Israeli purchase tax (mas rechisha) with full bracket-by-bracket breakdown for both first apartment (dira yechida) and non-first apartment buyers, including effective tax rate and JSON output option. Run: `python scripts/calculate_mas_rechisha.py --help`

### References
- `references/transaction-guide.md` - Step-by-step Israeli property buying checklist (from pre-approval through key handover), 2025 purchase tax brackets for first and non-first apartments, Tabu extract section descriptions (gush, chelka, mortgages, liens), and key transaction cost breakdown (attorney, agent, mortgage fees). Consult when guiding users through the purchase process or calculating total acquisition costs.

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
| Land Registry extract service (Tabu) | https://www.gov.il/he/service/land_registration_extract | Order a Tabu extract online (regular 15 / historical 74 / consolidated 131 NIS), gush/chelka lookup, liens and mortgages |
| Israel Land Authority (Rami) | https://www.gov.il/he/departments/israel_land_authority | Rami-registered properties, long-term leases |
| Israel Tax Authority -- real estate tax | https://www.gov.il/he/service/real_eatate_taxsimulator | Purchase tax (mas rechisha) simulator and current brackets |
| Nadlan (Tax Authority transactions) | https://www.nadlan.gov.il | Historical sale prices for Israeli residential properties |
| Discounted housing (Dira BeHanacha) | https://www.gov.il/he/departments/topics/dira/govil-landing-page | Reduced-price apartment program eligibility and listings |

## Troubleshooting

### Error: "Cannot access Tabu online"
Cause: Online Tabu has limited public access
Solution: Use an attorney or Tabu office for full extracts. Online gives basic ownership info only.

### Error: "Purchase tax rates outdated"
Cause: Rates updated annually by Tax Authority
Solution: Verify current year brackets at Israel Tax Authority website.