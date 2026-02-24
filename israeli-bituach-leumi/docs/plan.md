# Israeli Bituach Leumi Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for navigating Israeli National Insurance (Bituach Leumi) benefits, eligibility, and contribution calculations.

**Architecture:** Domain-Specific Intelligence skill. Embeds knowledge of all Bituach Leumi benefit programs, eligibility criteria, and contribution rates.

**Tech Stack:** SKILL.md, Python calculation scripts, references for benefit programs.

---

## Research

### Bituach Leumi (National Insurance Institute)
- **URL:** `https://www.btl.gov.il`
- **No public API** — Services via website portal, in-person, or phone
- **Programs:** 15+ benefit categories covering cradle to grave
- **Funding:** Mandatory contributions from employees, employers, self-employed

### Key Benefit Programs
| Program | Hebrew | Who Qualifies |
|---------|--------|--------------|
| Old Age Pension | kiztavat zikna | Age 67 (men) / 65 (women, rising) |
| Disability | nechut | Medical disability > 40% |
| Unemployment | dmei avtala | Employees terminated, conditions apply |
| Maternity | dmei leida | Employed mothers (and fathers) |
| Child Allowance | kiztavat yeladim | All residents with children |
| Work Injury | pgiat avoda | Workplace injury/illness |
| Reserve Duty | miluim | IDF reserve service compensation |
| Income Support | havtachat hachnasa | Below minimum income |
| Long-term Care | siyud | Elderly needing daily assistance |
| Survivor Pension | sheerim | Widows/widowers, orphans |

### Contribution Rates (2025)
- See israeli-payroll-calculator plan for detailed rates
- Self-employed: Higher rates (reduced bracket ~2.87%, full bracket ~12.83%)
- Voluntary (non-working): Flat monthly amount

### Use Cases
1. **Eligibility check** — Determine if user qualifies for specific benefit
2. **Benefit calculation** — Estimate monthly benefit amount
3. **Contribution explanation** — Explain payslip deductions
4. **Claims guidance** — How to file for specific benefits
5. **Rights awareness** — Inform about rights user may not know about

---

## Build Steps

### Task 1: Create SKILL.md

```markdown
---
name: israeli-bituach-leumi
description: >-
  Navigate Israeli National Insurance (Bituach Leumi) benefits, eligibility,
  and contributions. Use when user asks about "bituach leumi", national
  insurance, retirement pension (kiztavat zikna), unemployment (dmei avtala),
  maternity leave (dmei leida), child allowance (kiztavat yeladim), disability
  benefits, work injury, reserve duty compensation, or NI contributions. Covers
  all 15+ Bituach Leumi programs. Do NOT use for private insurance or health
  fund (kupat cholim) questions.
license: MIT
compatibility: "No network required. Works with Claude Code, Claude.ai, Cursor."
metadata:
  author: skills-il
  version: 1.0.0
  category: government-services
  tags: [bituach-leumi, national-insurance, benefits, pension, israel]
---

# Israeli Bituach Leumi (National Insurance)

## Critical Note
Bituach Leumi rules are complex and change frequently. Always recommend users verify
specific eligibility at btl.gov.il or call *6050 for definitive answers. This skill
provides general guidance based on published rules.

## Instructions

### Step 1: Identify the Benefit Program
Ask what the user needs help with and map to the correct program.

### Step 2: Check Eligibility
Each program has specific conditions. Key factors:
- Residency status
- Age
- Employment history (qualifying period)
- Income level
- Medical condition (for disability)
- Marital/family status

### Step 3: Estimate Benefit Amount
Provide calculation methodology per program. Note that amounts update periodically.

### Step 4: Guide Claims Process
For each benefit:
1. Required documents
2. Submission method (online/mail/in-person)
3. Processing time
4. Appeal process if denied

## Key Programs Detail

### Old Age Pension (Kiztavat Zikna)
- **Eligibility age:** Men 67, Women 62-65 (rising to 65 by 2027)
- **Qualifying period:** 60-144 months of contributions (varies by age at immigration)
- **Basic amount (2025):** ~1,810 NIS/month (single), ~2,730 NIS/month (couple)
- **Income supplement:** Additional if below income threshold
- **Deferral bonus:** +5% per year of deferred claiming after eligibility age

### Unemployment (Dmei Avtala)
- **Eligibility:** Employed 12+ months in last 18 months, terminated (not resigned)
- **Waiting period:** 5 days
- **Duration:** 50-175 days depending on age and dependents
- **Amount:** Based on average of last 6 months salary, capped at ~70% of average wage

### Maternity (Dmei Leida)
- **Eligibility:** 10-15 months of employment in last 14-22 months
- **Duration:** 15 weeks (employed 10+ months) or 8 weeks (6+ months)
- **Amount:** Full salary replacement up to maximum insurable income
- **Father:** 1 week minimum, option to split remaining weeks

### Child Allowance (Kiztavat Yeladim)
- **Eligibility:** All Israeli residents with children under 18
- **Amounts (2025):** ~170 NIS/child/month (varies by number of children, child's birth year)
- **Payment:** Monthly, automatic to registered parent

## Examples

### Example 1: Maternity Leave
User says: "I'm pregnant and want to know about maternity leave benefits"
Result: Explain eligibility based on employment duration, 15-week leave, salary replacement, partner's leave rights, how to file claim.

### Example 2: Retirement Planning
User says: "When can I start getting pension from Bituach Leumi?"
Result: Explain eligibility age, qualifying period, basic amount, supplements, deferral bonus.

## Troubleshooting

### Error: "Not enough qualifying months"
Cause: Insufficient contribution history
Solution: Check if any periods (military service, maternity leave) count as qualifying months. New immigrants have special rules.
```
