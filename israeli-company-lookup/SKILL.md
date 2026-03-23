---
name: israeli-company-lookup
description: Look up Israeli company information and understand business entity types. Use when user asks about Israeli companies, "chevra", business registration, "Rasham HaChevarot", company numbers, entity types, or needs to register a business in Israel. Covers Ltd companies, partnerships, non-profits (amuta), cooperatives, and sole proprietors. Do NOT use for non-Israeli corporate registries or stock market analysis.
license: MIT
allowed-tools: WebFetch
compatibility: Network access helpful for registrar lookups.
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
| Registration | Rasham, ~2,600 NIS (verify at ica.justice.gov.il) | Tax Authority, free | Rasham HaAmutot |
| Annual filing | Yes (financial statements) | Tax returns only | Yes (report to Rasham) |
| Minimum directors | 1 | N/A | 2 board members |
| Best for | Companies, startups | Freelancers, small biz | Non-profits, social |

### Step 4: Registration Steps (Chevra Baam -- most common)
1. Choose unique company name (check availability at Rasham)
2. Draft Articles of Association (takanon)
3. File incorporation documents at Rasham HaChevarot
4. Pay registration fee (~2,600 NIS (verify at ica.justice.gov.il))
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

### Example 3: Compare Entity Types
User says: "I'm starting a business in Israel, should I register as an Osek Murshe or a Chevra?"
Actions:
1. Compare entity types (Osek Patur, Osek Murshe, Ltd company) by criteria -- tax rates, liability, NI contributions, compliance burden, VAT obligations
Result: Side-by-side comparison table with recommendation based on expected annual turnover.

## Bundled Resources

### Scripts
- `scripts/search_company.py` — Display Israeli business entity types (Chevra Baam, Osek Morsheh, Amuta, etc.) with side-by-side comparison of liability, tax rates, and registration requirements, plus step-by-step Chevra Baam incorporation instructions. Supports subcommands: `entity-types`, `compare`, `registration-steps`. Run: `python scripts/search_company.py --help`

### References
- `references/entity-types.md` — Comprehensive table of all 8 Israeli business entity types with their registries, liability structures, tax rates, and company number format prefixes (51- for companies, 58- for non-profits, 55- for partnerships). Consult when advising users on entity type selection or interpreting company registration numbers.

## Gotchas
- Israeli company registration numbers (mispar chevra) are 9 digits, not the same as the tax ID (mispar osek). Agents may confuse these two identifiers or use one when the other is required.
- The Companies Registrar (Rasham HaChavarot) database contains Hebrew-only company names. Agents may search using English company names, which will return no results.
- Company status in the registrar can be "active" (pe'ila), "in dissolution" (be-piruq), or "stricken off" (nimekhqa). Agents may not check the status and return information about inactive companies as if they are operational.
- Israeli business types include Chevra Baam (Ltd.), Shutafut (Partnership), Amuta (NPO), and Aguda Shitufit (Cooperative). Each has different registration systems. Agents may search for a partnership in the company registrar, which only lists Ltd. companies.

## Troubleshooting

### Error: "Company not found"
Cause: Name spelling mismatch or company registered under different name
Solution: Try Hebrew name, or search by company number if available. Some companies register with English names different from their trading name.

### Error: "Company number format invalid"
Cause: Israeli company numbers (Chevra) are 9 digits; sole proprietor numbers match their TZ (ID); partnership and amuta numbers differ
Solution: Verify the entity type first. Companies: 51-XXXXXXX (9 digits), Amutot: 58-XXXXXXX, Partnerships: 55-XXXXXXX. Use the Rasham HaChevarot search to validate.

### Error: "Entity type confusion (Osek Patur vs Osek Morsheh)"
Cause: Users confuse tax registration types with company registration types
Solution: Osek Patur/Morsheh are VAT registration types at the Tax Authority (SHAAM), not company types at the Registrar of Companies. A person can be an Osek Morsheh without registering a company. Clarify the user's actual need: business entity lookup vs. tax registration status.