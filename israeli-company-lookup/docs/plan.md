# Israeli Company Lookup Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for looking up Israeli company information from the Companies Registrar (Rasham HaChevarot) and understanding Israeli business entity types.

**Architecture:** MCP Enhancement + Domain Intelligence skill. Wraps government company data with Israeli business law knowledge.

**Tech Stack:** SKILL.md, references for business entity types and registrar access.

---

## Research

### Israeli Companies Registrar (Rasham HaChevarot)
- **URL:** `https://ica.justice.gov.il/` (Israel Corporations Authority)
- **Online search:** Basic company lookup by name or number (free, limited)
- **Full extract:** Requires registration, fee-based
- **Data available:** Company name, number, type, status, registration date, registered address
- **Company number format:** 51-XXXXXXX (8-9 digits)

### Israeli Business Entity Types
| Type | Hebrew | Registration | Liability |
|------|--------|-------------|-----------|
| Chevra Baam (Ltd) | chevra baam | Rasham HaChevarot | Limited |
| Chevra Tziburit (Public) | chevra tziburit | Rasham + TASE | Limited |
| Shutfut Klalit | shutfut klalit | Rasham HaShutfuyot | Unlimited (all partners) |
| Shutfut Mugbelet (LP) | shutfut mugbelet | Rasham HaShutfuyot | Limited (limited partners) |
| Amuta (Non-profit) | amuta | Rasham HaAmutot | Limited |
| Agudat Shitufit (Coop) | agudat shitufit | Rasham HaAgudot | Limited |
| Osek Morsheh | osek morsheh | Tax Authority | Unlimited (personal) |
| Osek Patur | osek patur | Tax Authority | Unlimited (personal) |

### Use Cases
1. **Company lookup** — Search by name or number
2. **Entity type guidance** — Which structure to choose for a new business
3. **Registration guidance** — Steps to register each entity type
4. **Due diligence** — Check company status, active/dissolved
5. **Directors and shareholders** — Understand public filing requirements

---

## Build Steps

### Task 1: Create SKILL.md

```markdown
---
name: israeli-company-lookup
description: >-
  Look up Israeli company information and understand business entity types.
  Use when user asks about Israeli companies, "chevra", business registration,
  "Rasham HaChevarot", company numbers, entity types, or needs to register
  a business in Israel. Covers Ltd companies, partnerships, non-profits (amuta),
  cooperatives, and sole proprietors. Do NOT use for non-Israeli corporate
  registries or stock market analysis.
license: MIT
allowed-tools: "WebFetch"
compatibility: "Network access helpful for registrar lookups."
metadata:
  author: skills-il
  version: 1.0.0
  category: government-services
  tags: [company, business, registration, corporate, israel]
---

# Israeli Company Lookup

## Instructions

### Step 1: Identify the Need
| Request | Approach |
|---------|----------|
| Look up existing company | Search by name/number at Rasham |
| Choose entity type | Compare types by liability, tax, complexity |
| Register new business | Step-by-step guide per entity type |
| Due diligence check | Verify status, directors, filings |

### Step 2: Company Search
Search the Israel Corporations Authority:
- URL: `https://ica.justice.gov.il/GenericCorporarionInfo/SearchCorporation`
- Search by: Company name (Hebrew or English) or company number
- Results: Name, number, type, status (active/dissolved/in liquidation), registration date

### Step 3: Entity Type Comparison
| Factor | Chevra Baam (Ltd) | Osek Morsheh | Amuta |
|--------|-------------------|-------------|-------|
| Liability | Limited to investment | Personal, unlimited | Limited |
| Tax | Corporate rate ~23% | Personal brackets | Exempt (conditions) |
| Registration | Rasham, ~1,700 NIS | Tax Authority, free | Rasham HaAmutot |
| Annual filing | Yes (financial statements) | Tax returns only | Yes (report to Rasham) |
| Minimum directors | 1 | N/A | 2 board members |
| Best for | Companies, startups | Freelancers, small biz | Non-profits, social |

### Step 4: Registration Steps (Chevra Baam — most common)
1. Choose unique company name (check availability at Rasham)
2. Draft Articles of Association (takanon)
3. File incorporation documents at Rasham HaChevarot
4. Pay registration fee (~1,700 NIS)
5. Receive Certificate of Incorporation (teuda le-hitaagdut)
6. Register with Tax Authority for income tax and VAT
7. Open business bank account with incorporation certificate
8. Register with Bituach Leumi as employer (if hiring)

## Examples

### Example 1: Company Lookup
User says: "Look up the company Monday.com"
Result: Monday.com Ltd, Company No. 51-530820-1, Status: Active, Type: Public Company (listed on NASDAQ)

### Example 2: Choose Entity Type
User says: "I'm a freelance developer, what business structure should I use?"
Result: Compare Osek Morsheh (simplest) vs. Chevra Baam (limited liability). Recommend Osek Morsheh for starting, switch to Chevra Baam when annual revenue exceeds ~400K NIS or liability protection needed.

## Troubleshooting

### Error: "Company not found"
Cause: Name spelling mismatch or company registered under different name
Solution: Try Hebrew name, or search by company number if available. Some companies register with English names different from their trading name.
```
