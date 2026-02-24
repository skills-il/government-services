---
name: israeli-real-estate
description: >-
  Israeli real estate data, property valuation, transaction guidance, and
  regulatory compliance. Use when user asks about Israeli property, "nadlan",
  "dira", apartment prices, purchase tax (mas rechisha), Tabu extract, rental
  agreements, mortgage (mashkanta), or Israel Land Authority tenders. Covers
  buying, selling, and renting in Israel. Do NOT use for non-Israeli real
  estate markets.
license: MIT
compatibility: "Network access helpful for data lookups. Enhanced by remy-mcp for land tenders."
metadata:
  author: skills-il
  version: 1.0.0
  category: government-services
  tags: [real-estate, property, nadlan, tabu, mas-rechisha, israel]
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
For apartment purchases (2025 rates, verify annually):

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
| 6,055,071 - 20,183,565 | 10% |
| 20,183,566+ | 12% |

### Step 3: Buying Process Checklist
1. **Pre-approval:** Get mortgage pre-approval (ishur ikroni) from bank
2. **Property search:** View properties, check neighborhood
3. **Attorney:** Hire real estate attorney (orech din mikrkain) BEFORE signing
4. **Tabu check:** Attorney obtains Tabu extract to verify ownership, liens
5. **Negotiation:** Agree on price, payment schedule
6. **Contract:** Sign purchase agreement (chozeh mcher)
7. **Purchase tax:** Pay mas rechisha within 50 days of signing
8. **Mortgage:** Finalize with bank, appraiser visit
9. **Registration:** Attorney registers transfer in Tabu
10. **Possession:** Key handover per contract schedule

### Step 4: Tabu Extract (Nesach Tabu)
A Tabu extract shows:
- **Section 1:** Property description (gush, chelka, tat-chelka)
- **Section 2:** Registered owners and shares
- **Section 3:** Mortgages (mashkantaot)
- **Section 4:** Liens, warnings (hearot azhara), court orders

**How to obtain:**
- Online: `https://ecom.gov.il/voucherspa/tabu/` (limited info, ~15 NIS)
- Full extract: Through attorney or in-person at Tabu office
- Required info: Gush (block) and Chelka (parcel) numbers

### Step 5: Rental Agreement Key Terms
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
Result: Mas rechisha breakdown: 0% on first 1,978,745 + 3.5% on remainder = ~18,245 NIS

### Example 2: Buying Process
User says: "I want to buy an apartment in Tel Aviv, what do I need to know?"
Result: Full checklist with Tel Aviv specific notes (high prices, urban renewal projects, tama 38)

## Bundled Resources

### Scripts
- `scripts/calculate_mas_rechisha.py` — Calculate Israeli purchase tax (mas rechisha) with full bracket-by-bracket breakdown for both first apartment (dira yechida) and non-first apartment buyers, including effective tax rate and JSON output option. Run: `python scripts/calculate_mas_rechisha.py --help`

### References
- `references/transaction-guide.md` — Step-by-step Israeli property buying checklist (from pre-approval through key handover), 2025 purchase tax brackets for first and non-first apartments, Tabu extract section descriptions (gush, chelka, mortgages, liens), and key transaction cost breakdown (attorney, agent, mortgage fees). Consult when guiding users through the purchase process or calculating total acquisition costs.

## Troubleshooting

### Error: "Cannot access Tabu online"
Cause: Online Tabu has limited public access
Solution: Use an attorney or Tabu office for full extracts. Online gives basic ownership info only.

### Error: "Purchase tax rates outdated"
Cause: Rates updated annually by Tax Authority
Solution: Verify current year brackets at Israel Tax Authority website.
