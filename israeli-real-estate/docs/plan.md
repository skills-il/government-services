# Israeli Real Estate Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for Israeli real estate data aggregation — property valuation, Tabu (Land Registry) guidance, market analysis, and transaction support.

**Architecture:** Domain-Specific Intelligence skill with Workflow Automation for transaction flows. Embeds Israeli real estate law, property types, and market data sources.

**Tech Stack:** SKILL.md, references for real estate regulations and data sources.

---

## Research

### Israeli Real Estate Data Sources
- **Tax Authority:** Sold-price data (accessible via Madlan/data.gov.il)
- **Tabu (Land Registry):** Property ownership records, liens, mortgages
  - Managed by Ministry of Justice
  - Online limited queries: `https://ecom.gov.il/voucherspa/tabu/`
  - Full extract requires in-person or attorney request
- **Yad2:** Largest Israeli listing platform (no public API, scraping possible)
- **Madlan (by Localize.city):** Property data analytics, price history
- **Israel Land Authority (RMI):** Government land tenders, leasehold data
  - `remy-mcp` MCP server exists for tender data
- **Arnona (municipal property tax):** Municipal databases, varies by city

### Israeli Real Estate Concepts
- **Tabu vs Minhal:** Tabu (Land Registry) for private land, Israel Land Authority (Minhal) for state-leased land (~93% of land)
- **Property types:** Dira (apartment), Bayit Prati (house), Penthouse, Dupleks, Cottage, Studio
- **Ownership types:** Baalut (ownership), Chasichra (lease from ILA), Zacut Shimush
- **Key costs:** Purchase tax (mas rechisha), agent fees (1-2%), attorney fees (0.5-1.5%), mortgage (mashkanta)
- **Purchase tax rates:** Progressive scale, higher for non-first-apartment buyers

### Use Cases
1. **Property valuation** — Estimate value based on comparable sold prices
2. **Purchase tax calculation** — Calculate mas rechisha based on buyer status
3. **Transaction checklist** — Step-by-step guide for buying/selling in Israel
4. **Tabu extract guidance** — How to obtain and read a Tabu extract (nesach tabu)
5. **Rental agreement** — Key terms for Israeli rental contracts (chozeh schirut)

---

## Build Steps

### Task 1: Create SKILL.md

```markdown
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
| 20,183,566+ | 12% | (was temporarily 15% for foreign buyers)

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
- Security deposit (pikadon) — typically 1-3 months, capped by law
- Arnona (property tax) — clarify who pays
- Vaad bayit (building maintenance) — clarify who pays
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

## Troubleshooting

### Error: "Cannot access Tabu online"
Cause: Online Tabu has limited public access
Solution: Use an attorney or Tabu office for full extracts. Online gives basic ownership info only.

### Error: "Purchase tax rates outdated"
Cause: Rates updated annually by Tax Authority
Solution: Verify current year brackets at Israel Tax Authority website.
```
