---
name: israeli-drug-database
description: >-
  Query the Israeli pharmaceutical database for drug information, health basket
  coverage, generic alternatives, and pricing. Use when user asks about Israeli
  medications, "trufot", drug names, "sal briut" drug coverage, generic drugs,
  drug prices in Israel, prescription requirements, or medication safety info.
  Enhances israel-drugs-mcp server with health basket context and patient-facing
  guidance. Do NOT use for medical advice, dosage recommendations, or diagnosis.
  Do NOT use for non-Israeli drug registries.
license: MIT
allowed-tools: "WebFetch"
compatibility: "Network access helpful for drug registry lookups. Enhanced by israel-drugs-mcp server."
metadata:
  author: skills-il
  version: 1.0.0
  category: government-services
  tags: [drugs, pharmaceutical, health-basket, medication, pharmacy, israel]
  mcp-server: israel-drugs-mcp
---

# Israeli Drug Database

## Critical Note
This skill provides DRUG INFORMATION ONLY, not medical advice. Never recommend
specific medications, dosages, or treatment changes. Always direct users to their
physician or pharmacist for personal medication questions. Drug coverage and pricing
data may change -- verify with the user's kupat cholim for current copay amounts.

## Instructions

### Step 1: Identify Drug Query Type
| Query | Action |
|-------|--------|
| Drug lookup | Search registry by name or ingredient |
| Health basket status | Check sal briut coverage tier |
| Generic alternatives | Find equivalent generics by active ingredient |
| Drug pricing | Look up regulated maximum price |
| Safety info | Retrieve side effects, interactions, pregnancy category |
| Prescription status | Check if OTC or prescription required |

### Step 2: Drug Lookup
Search the MoH drug registry:
- **By trade name:** Search Hebrew or English brand name (e.g., "Acamol", "Optalgin")
- **By generic/active ingredient:** Search by active substance (e.g., "paracetamol", "dipyrone")
- **By registration number:** Direct lookup by mispar rishum

**Key fields returned:**
| Field | Hebrew | Description |
|-------|--------|-------------|
| Trade name | shem miskhari | Brand name as marketed |
| Generic name | shem bilti muskam / shem generi | International nonproprietary name (INN) |
| Active ingredient | chomer peeil | Active substance and strength |
| Dosage form | tzurat matan | Tablet, capsule, injection, etc. |
| Manufacturer | yatzran | Company holding marketing authorization |
| ATC code | kod ATC | WHO anatomical therapeutic chemical code |
| Registration status | matzav rishum | Active, suspended, or cancelled |
| Prescription type | sug mircham | Prescription (mircham), OTC (lli mircham), restricted |

### Step 3: Health Basket Coverage
Check if a drug is covered in the national health basket:

**Coverage tiers:**
| Tier | Patient Cost | Typical Drugs |
|------|-------------|---------------|
| Full basket -- no copay | Free or minimal fee | Essential/life-saving medications |
| Full basket -- with copay | Fixed copay per package | Most chronic condition drugs |
| Partial basket | Percentage-based copay | Newer/expensive medications |
| Not in basket | Full price (or via shaban) | New drugs pending committee review |

**Copay ranges (approximate):**
- Generic drug: ~10-20 NIS per package
- Brand-name (when generic exists): ~30-50 NIS per package
- Specialty/biologic: Variable, often subsidized for qualifying patients

**How to check:** Query sal briut formulary via MoH data, or check kupat cholim website

### Step 4: Generic Alternatives
To find generic alternatives:
1. Identify the active ingredient (chomer peeil) of the brand-name drug
2. Search the registry for all products with the same active ingredient and strength
3. Filter for currently registered (active status) products
4. Compare:
   - Same active ingredient and strength
   - Same dosage form (tablet, capsule, etc.)
   - Different manufacturer (generic producer)
   - Typically 40-60% lower price

**Common Israeli generics:**
| Brand Name | Generic Name | Active Ingredient |
|------------|-------------|-------------------|
| Acamol | Paracetamol generics | Paracetamol |
| Optalgin | Dipyrone generics | Dipyrone (metamizole) |
| Ibufen | Ibuprofen generics | Ibuprofen |
| Losec | Omeprazole generics | Omeprazole |
| Lipitor | Atorvastatin generics | Atorvastatin |
| Norvasc | Amlodipine generics | Amlodipine |

### Step 5: Drug Safety Information
Provide safety context (NOT medical advice):

**Patient information leaflet (alon la-mitan):**
- Available in Hebrew for all registered drugs
- Published on MoH website and inside drug packaging
- Contains: Indications, contraindications, side effects, dosage

**Drug interactions:**
- Cross-reference by active ingredient
- Common interaction categories: blood thinners, diabetes medications, blood pressure drugs
- Always recommend consulting pharmacist for interaction checks

**Pregnancy categories:**
| Category | Meaning |
|----------|---------|
| A | No risk demonstrated in human studies |
| B | No risk in animal studies, limited human data |
| C | Risk cannot be ruled out |
| D | Evidence of risk, may be used when benefit outweighs |
| X | Contraindicated in pregnancy |

**Recall and safety alerts:**
- MoH publishes drug safety alerts at `health.gov.il`
- Pharmacovigilance reports via Yellow Card system

### Step 6: Prescription Status
Israeli prescription categories:
| Type | Hebrew | Meaning |
|------|--------|---------|
| OTC (lli mircham) | llo mircham | Available without prescription at pharmacies |
| Prescription (mircham) | mircham | Requires physician prescription |
| Restricted (mircham meyuchad) | mircham meyuchad | Specialist prescription or hospital-only |
| Narcotic (sam mefakach) | sam mefakach | Controlled substance, special prescription form |

## Examples

### Example 1: Drug Lookup
User says: "Tell me about Acamol"
Result: Acamol -- Trade name for paracetamol (acetaminophen). Active ingredient: Paracetamol 500mg (tablet form). OTC -- no prescription needed. In health basket with minimal copay. Multiple generic alternatives available. Common uses: pain relief, fever reduction. Max daily dose: consult leaflet (refer to physician).

### Example 2: Generic Alternative
User says: "Is there a cheaper alternative to Lipitor?"
Result: Lipitor contains atorvastatin. Multiple generic atorvastatin products are registered in Israel at the same strengths (10mg, 20mg, 40mg, 80mg). Generics are typically 40-60% cheaper. All covered in health basket. Switching from brand to generic requires physician approval -- discuss with your doctor.

### Example 3: Health Basket Check
User says: "Is Keytruda covered by kupat cholim?"
Result: Keytruda (pembrolizumab) is partially in the health basket for specific approved indications (e.g., certain cancers). Coverage depends on diagnosis and indication. For indications not yet in basket, may be available through supplementary insurance (shaban) or compassionate use. Contact kupat cholim oncology coordinator for specific eligibility.

## Troubleshooting

### Error: "Drug not found in registry"
Cause: Drug may be registered under different name, or not registered in Israel
Solution: Try searching by active ingredient instead of brand name. Some international brands are marketed under different names in Israel. Check if the drug is registered at all -- not all drugs approved abroad are registered in Israel.

### Error: "Health basket status unclear"
Cause: Drug may be covered for specific indications only, or recently added/removed
Solution: Health basket is updated annually. Check the most recent published formulary. For edge cases, contact the kupat cholim's pharmaceutical committee (vaada le-trufot).

### Error: "Price information unavailable"
Cause: MoH price list may not be current, or drug is hospital-only
Solution: Check with local pharmacy for current retail price. Hospital-administered drugs are not priced in the retail price list.
