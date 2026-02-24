# Israeli Health Data Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for Israeli Ministry of Health data access and healthcare system navigation — hospital quality indicators, health fund comparison, and patient rights under the National Health Insurance Law.

**Architecture:** MCP Enhancement + Domain-Specific Intelligence skill. Enhances the existing `ILHealth-mcp` server with healthcare system knowledge, health fund comparison data, and patient rights guidance.

**Tech Stack:** SKILL.md, references for MoH data sources, health fund services, and National Health Insurance Law.

---

## Research

### ILHealth-mcp Server
- **Repository:** Community MCP server for Israeli health data
- **Function:** Queries Ministry of Health datasets and quality indicators
- **Enhancement opportunity:** Add health fund comparison, patient rights, and healthcare navigation guidance

### Ministry of Health (Misrad HaBriut) Data
- **URL:** `https://www.health.gov.il`
- **Quality dashboard:** Hospital quality indicators published quarterly
  - `https://www.health.gov.il/UnitsOffice/HD/PH/Pages/Quality-Indicators.aspx`
- **Data portal:** Health-related datasets on data.gov.il
- **Key datasets:**
  - Hospital quality indicators (mortality rates, infection rates, wait times)
  - Licensed medical professionals registry
  - Health basket (sal briut) — list of covered medications and treatments
  - Hospital bed occupancy and capacity
  - Vaccination data

### Four Health Funds (Kupot Cholim)
Every Israeli resident must be enrolled in one of four health funds under the National Health Insurance Law (1995).

| Health Fund | Hebrew | Members (~) | Market Share | Strengths |
|-------------|--------|-------------|-------------|-----------|
| Clalit (Clalit Health Services) | clalit sherutei briut | ~4.8M | ~52% | Largest, owns hospitals (14), widest clinic network |
| Maccabi (Maccabi Healthcare Services) | maccabi sherutei briut | ~2.5M | ~27% | Strong digital services, Maccabi Online app |
| Meuhedet (Meuhedet Health Fund) | kupat cholim meuhedet | ~1.3M | ~14% | Fast specialist access, good supplementary plans |
| Leumit (Leumit Health Fund) | kupat cholim leumit | ~0.7M | ~7% | Flexible, good for small communities |

### National Health Insurance Law (Chok Bituach Briut Mamlachti, 1995)
- **Principle:** Universal coverage for all Israeli residents
- **Funding:** Health tax (mas briut) via Bituach Leumi
- **Health basket (sal briut):** Government-defined list of medications, treatments, and services all funds must provide
- **Switching:** Residents can switch health funds once per year (transfer takes effect after waiting period)
- **Supplementary insurance (shaban):** Optional additional coverage offered by each fund for extra services
- **Key rights:**
  - Choice of health fund
  - Defined basket of services
  - Maximum wait times for specialist appointments and surgeries
  - Second medical opinion
  - Access to medical records
  - Right to refuse treatment

### Use Cases
1. **Hospital quality comparison** — Compare hospitals by quality indicators
2. **Health fund comparison** — Compare the four kupot cholim by services, coverage, and satisfaction
3. **Patient rights** — Explain rights under National Health Insurance Law
4. **Health basket lookup** — Check if a treatment or medication is in sal briut
5. **Supplementary plan comparison** — Compare shaban plans across funds
6. **Specialist wait times** — Check expected wait times for specialist appointments

---

## Build Steps

### Task 1: Create SKILL.md

```markdown
---
name: israeli-health-data
description: >-
  Israeli Ministry of Health data, healthcare system navigation, and patient
  rights. Use when user asks about Israeli hospitals, "kupat cholim", health
  funds (Clalit, Maccabi, Meuhedet, Leumit), "sal briut" (health basket),
  hospital quality, patient rights, National Health Insurance Law, supplementary
  insurance ("shaban"), or any Israeli healthcare system question. Enhances
  ILHealth-mcp server with health fund comparison and patient rights guidance.
  Do NOT use for non-Israeli healthcare systems or private medical advice.
license: MIT
allowed-tools: "WebFetch"
compatibility: "Network access helpful for MoH data lookups. Enhanced by ILHealth-mcp server."
metadata:
  author: skills-il
  version: 1.0.0
  category: government-services
  tags: [health, hospital, kupat-cholim, health-fund, patient-rights, israel]
  mcp-server: ILHealth-mcp
---

# Israeli Health Data

## Critical Note
This skill provides general healthcare system information only. It does NOT provide
medical advice, diagnoses, or treatment recommendations. Always direct users to their
health fund (kupat cholim) or physician for personal medical questions. Data such as
hospital quality indicators and wait times are based on published MoH reports and may
not reflect current conditions.

## Instructions

### Step 1: Identify Healthcare Need
| Need | Action |
|------|--------|
| Hospital quality | Query MoH quality indicators |
| Health fund comparison | Compare four kupot cholim |
| Patient rights | Explain rights under NHIL |
| Health basket lookup | Check sal briut coverage |
| Supplementary insurance | Compare shaban plans |
| Specialist access | Check wait times and referral process |
| Switch health fund | Guide through transfer process |

### Step 2: Hospital Quality Indicators
Ministry of Health publishes quarterly quality indicators for all hospitals:

**Key Indicators:**
| Indicator | What It Measures | Lower is Better? |
|-----------|-----------------|-------------------|
| Standardized mortality ratio | Deaths vs. expected | Yes |
| Surgical site infection rate | Post-surgery infections | Yes |
| Central line infection rate | CLABSI per 1,000 catheter-days | Yes |
| 30-day readmission rate | Unplanned readmissions | Yes |
| Emergency dept wait time | Time to first physician | Yes |
| Patient satisfaction | Survey scores | No (higher = better) |
| Bed occupancy rate | Percentage of beds occupied | Optimal: 80-85% |

**Major Hospitals:**
| Hospital | Hebrew | City | Type | Beds (~) |
|----------|--------|------|------|----------|
| Sheba (Tel Hashomer) | sheba tel hashomer | Ramat Gan | Government | 1,700 |
| Rambam | rambam | Haifa | Government | 1,000 |
| Hadassah Ein Kerem | hadasa ein kerem | Jerusalem | Non-profit | 800 |
| Ichilov (Sourasky) | ichilov souraski | Tel Aviv | Municipal | 1,100 |
| Soroka | soroka | Beer Sheva | Government | 1,100 |
| Beilinson (Rabin) | beilinson rabin | Petah Tikva | Clalit | 900 |
| Meir | meir | Kfar Saba | Clalit | 700 |
| Kaplan | kaplan | Rehovot | Clalit | 700 |
| Wolfson | wolfson | Holon | Government | 600 |
| Assuta | asuta | Tel Aviv/Ashdod | Private | Varies |

### Step 3: Health Fund Comparison
Compare the four kupot cholim across key dimensions:

**Coverage and Services:**
| Feature | Clalit | Maccabi | Meuhedet | Leumit |
|---------|--------|---------|----------|--------|
| Clinics nationwide | ~1,500 | ~300 | ~250 | ~200 |
| Own hospitals | 14 | 0 (Assuta partnership) | 0 | 0 |
| Digital services | Good | Excellent | Good | Fair |
| Supplementary plans | Mushlam/Platinum | Magen Zahav/Sheli | Adif/Magen | Zahav/Kesher |
| Specialist wait (avg) | Moderate | Short-moderate | Short | Short |

**Supplementary Insurance (Shaban) Comparison:**
All four funds offer 2-3 tiers of supplementary insurance:
- **Basic tier:** ~30-50 NIS/month — Reduced specialist copays, extended treatments
- **Mid tier:** ~80-120 NIS/month — Private specialist access, shorter waits, fertility
- **Premium tier:** ~150-250 NIS/month — Surgery abroad, experimental treatments, private rooms

### Step 4: Patient Rights Under National Health Insurance Law
Every Israeli resident has the following rights:

1. **Choice of health fund** — Can choose any of the four kupot cholim
2. **Health basket (sal briut)** — All medications, treatments, and services in the basket must be provided
3. **Maximum wait times:**
   - General practitioner: Same day or next day
   - Specialist: Up to 30 days (varies by specialty)
   - Non-urgent surgery: Published maximum wait guidelines
4. **Second opinion** — Right to seek a second medical opinion
5. **Medical records** — Right to access complete medical records
6. **Informed consent** — Full explanation before any procedure
7. **Privacy** — Medical information confidentiality
8. **Switching funds:** Can switch once per year, transfer takes 1-6 months
9. **Complaint process:** Each fund has an ombudsman (netziv tlunot hatzibbur)

### Step 5: Health Basket (Sal Briut)
The health basket is updated annually by the Health Basket Committee:
- **What's covered:** Medications, medical devices, procedures, and treatments
- **New additions:** Committee adds ~500-700M NIS of new technologies annually
- **Not covered:** Cosmetic procedures, some advanced treatments pending approval
- **How to check:** MoH publishes the full basket list; each fund's website lists covered services
- **Copay (hishtattfut atzmit):** Patients pay partial cost for medications and some services

### Step 6: Switching Health Funds
Process for switching kupat cholim:
1. Visit a branch of the desired new health fund OR apply online
2. Fill out transfer form with ID (teudat zehut) details
3. Waiting period: Typically 1-6 months depending on conditions
4. No transfer permitted if currently hospitalized
5. Pre-existing conditions: Cannot be denied by new fund
6. Supplementary insurance: New enrollment required at new fund (may have waiting period)

## Examples

### Example 1: Hospital Comparison
User says: "Which hospital in Tel Aviv has the best quality ratings?"
Result: Compare Ichilov (Sourasky) and Sheba (Tel Hashomer, nearby) on MoH quality indicators — mortality ratio, infection rates, patient satisfaction. Note Assuta for elective/private procedures.

### Example 2: Health Fund Selection
User says: "I just made aliyah, which kupat cholim should I join?"
Result: Compare all four funds. For new immigrants: Clalit has widest coverage and most clinics, Maccabi has best digital experience, Meuhedet and Leumit may offer faster specialist access. Recommend based on residential area and priorities.

### Example 3: Patient Rights
User says: "My kupat cholim is making me wait 3 months for a specialist"
Result: Explain maximum wait time guidelines, right to complain to fund's ombudsman, option to request referral to external specialist, and how to escalate to MoH if wait exceeds published limits.

## Troubleshooting

### Error: "Quality data outdated"
Cause: MoH publishes quality indicators quarterly with a delay
Solution: Note the reporting period. Direct users to MoH quality dashboard for most recent published data.

### Error: "Treatment not found in health basket"
Cause: Treatment may be new, under review, or covered under a different name
Solution: Check both Hebrew and English names. Some treatments are covered under supplementary insurance (shaban) even if not in basic basket. Contact kupat cholim directly for borderline cases.

### Error: "Cannot switch health fund"
Cause: May be within transfer waiting period or currently hospitalized
Solution: Check timing of last switch (once per year limit), verify no hospitalization, confirm with current fund that no blocking conditions exist.
```
