---
name: israeli-unemployment-benefits-navigator
description: "Walk a user through Israeli dmei avtala (דמי אבטלה / unemployment benefits) end to end: check eligibility under the 12-of-18 months qualifying period (tkufat akhshara), calculate expected benefit with the 2026 progressive tier formula, map max days by age and dependents (50 to 300 days), warn about the 90-day resignation waiting period, and generate a personalized application checklist for Sherut HaTaasuka and Bituach Leumi. Use when a user asks about avtala, dmei avtala, unemployment benefits in Israel, how much avtala they will get, how to apply, eligibility after quitting, tkufat akhshara, being laid off or fired in Israel, or benefit duration. Do NOT use for other Bituach Leumi programs (use israeli-bituach-leumi), net salary calculations (use israeli-payroll-calculator), reservist compensation (use israeli-miluim-manager), aliyah benefits (use israeli-aliyah-navigator), or employment contract legal review."
license: MIT
allowed-tools: ''
compatibility: Works with Claude, Claude Code, ChatGPT, Cursor. Optional pairing with kolzchut MCP for live rule lookups. No network required for standalone calculations.
---

# Israeli Unemployment Benefits Navigator

## Problem
Every year, tens of thousands of Israelis lose their job or are placed on unpaid leave (חל"ת) and leave avtala money on the table because the rules are dense, the qualifying period is easy to miscount, and the Bituach Leumi website buries the progressive benefit formula under links. Resigning without knowing about the 90-day waiting period, registering late at Sherut HaTaasuka, or forgetting that only 12 salaried months out of the last 18 qualify, all cost real shekels. This skill gives a clear "Am I eligible? How much will I get? What do I do first?" answer in one pass, with a personalized application checklist the user can execute the same day.

## Instructions

### Step 1: Collect User Inputs

| Input | Required | Used for |
|-------|----------|----------|
| Reason employment ended | Yes | Fired / laid off / made redundant / resigned / unpaid leave (chalat). Determines the 90-day waiting period |
| Last day of work | Yes | Starts the 3-month registration clock and anchors the 18-month lookback |
| Age in years | Yes | Determines max benefit days and the under-28 vs 28+ benefit rate tier |
| Number of people you support (spouse + children) | Yes | Determines max benefit days bracket |
| Average monthly gross salary over the last 6 months | Yes | Drives benefit amount via the progressive tier formula |
| Number of months worked as an employee in the last 18 | Yes | Verifies tkufat akhshara (must be at least 12) |
| Israeli resident? | Yes | Non-residents are ineligible |
| Already registered at Sherut HaTaasuka? | Yes | If not, this is the first action |
| Gender and exact date of birth | If aged 57 to 67 | Women born 1960 or later get a special 300-day track |

### Step 2: Check Eligibility (tkufat akhshara)

Run the eligibility gate in this order. Stop at the first failure and tell the user exactly which rule blocks them.

| Gate | Rule | Fail action |
|------|------|-------------|
| Residency | Must be an Israeli resident | Explain that non-residents cannot claim dmei avtala |
| Age | Between 20 and 67 | Below 20: not eligible. Above 67: explain kiztavat zikna instead |
| Qualifying period | At least 12 months of work as a salaried employee (shakhir) in the last 18 months | Explain that freelance (osek) months do not count, that even one day in a month counts as a full month, and advise waiting until the count reaches 12 |
| Registration window | Must register at Sherut HaTaasuka within 3 months of the last day of work | If outside window, eligibility still exists but the 18-month lookback starts from registration, not termination, which may disqualify older months |

Under Israeli law, a month with even a single day of salaried work counts as a full qualifying month. This is a common point of confusion.

### Step 3: Check Waiting Period (reason for termination)

| Reason | Waiting period | Notes |
|--------|---------------|-------|
| Fired / laid off (pituin) | None | Full entitlement from day 1 |
| Made redundant | None | Same as fired |
| Employer bankrupt | None | Employee can claim both unpaid wages from Bituach Leumi and dmei avtala |
| Unpaid leave (chalat) of 30+ days | None | Standard chalat rules |
| Resignation without justified cause | 90 days | Blocks the first 90 days of benefits |
| Resignation with justified cause (hitpatrut b'din mefuteret) | None | Must prove grounds: health issue, relocation of spouse, sexual harassment, severe worsening of terms, drop of 25%+ in pay, move to another city due to marriage. Bituach Leumi decides |
| Refused a job offer from Sherut HaTaasuka | 90 days + 30 day reduction in total entitlement | Do not refuse offers lightly |

If the user resigned, flag the 90-day wait prominently and list the recognized "justified cause" grounds so they can check whether they qualify.

### Step 4: Calculate Maximum Benefit Days

Use the age + dependents table. "Dependents" = spouse + children the user supports.

| Age at start of unemployment | Dependents | Max days |
|------------------------------|-----------|----------|
| 20-25 | 0, 1, or 2 | 50 |
| 20-25 | 3 or more | 138 |
| 25-28 | 0, 1, or 2 | 67 |
| 25-28 | 3 or more | 138 |
| 28-35 | 0, 1, or 2 | 100 |
| 28-35 | 3 or more | 138 |
| 35-45 | 0, 1, or 2 | 138 |
| 35-45 | 3 or more | 175 |
| 45-67 | Any | 175 |
| Women 57-67 born 1960 or later | Any | 300 (special track, 18-month window) |

The maximum days must be used within 12 months from the 1st of the registration month. The special women's track uses 18 months instead of 12.

### Step 5: Calculate Daily Benefit Amount

The daily benefit is based on the user's average daily wage over the last 6 full months of work.

**Step 5a: Average daily wage**
```
average_daily_wage = (gross salary over last 6 months) / 150
```
(The divisor is 150, not 180, because Bituach Leumi assumes 25 working days per month * 6 months.)

**Step 5b: Apply the progressive formula for 2026**

Under 28 years old:

| Daily wage bracket | Rate |
|-------------------|------|
| Up to ₪207.50 | 60% |
| ₪207.50 to ₪311 | 40% on the portion above ₪207.50 |
| ₪311 to ₪415 | 35% on the portion above ₪311 |
| ₪415 to daily ceiling | 25% on the portion above ₪415 |

Aged 28 and over:

| Daily wage bracket | Rate |
|-------------------|------|
| Up to ₪207.50 | 80% |
| ₪207.50 to ₪311 | 50% on the portion above ₪207.50 |
| ₪311 to ₪415 | 45% on the portion above ₪311 |
| ₪415 to daily ceiling | 30% on the portion above ₪415 |

Sum each bracket contribution to get the gross daily benefit.

**Step 5c: Apply the 2026 daily ceilings**

- First 125 days of unemployment: maximum ₪550.76 per day
- Day 126 onwards: maximum ₪367.17 per day
- Cap whatever the formula produces to these ceilings

**Step 5d: Deductions**

The gross benefit is taxed like income:
- Income tax at the user's marginal rate (often reduced because avtala is below the first tax bracket for low-wage earners)
- Bituach Leumi: fixed ₪32 per month as of 2026
- Mas briut (health tax)

The net amount the user actually receives is the gross benefit minus these deductions. Do not promise the user the gross number as take-home.

**Worked example (28+ earner making ₪15,000/month gross):**

```
6-month gross total: 15000 * 6 = 90,000
average_daily_wage: 90000 / 150 = 600

Bracket 1 (up to 207.50): 207.50 * 80% = 166.00
Bracket 2 (207.50 to 311): (311 - 207.50) * 50% = 51.75
Bracket 3 (311 to 415): (415 - 311) * 45% = 46.80
Bracket 4 (415 to 600): (600 - 415) * 30% = 55.50
daily_gross: 166.00 + 51.75 + 46.80 + 55.50 = 320.05

Ceiling check: 320.05 < 550.76 (ok for first 125 days)
Monthly gross (approx 25 working days): 320.05 * 25 = 8,001.25
Minus deductions (income tax, BL 32, health): net receives less
```

### Step 6: Generate the Application Checklist

Give the user a personalized, ordered checklist. Each step references a real form or portal.

```
1. Register at Sherut HaTaasuka (Employment Service)
   URL: https://www.taasuka.gov.il
   - Required within 3 months of last workday
   - Bring: teudat zehut, last 3 payslips, termination letter
   - Output: dorsh avoda status, scheduled reporting days

2. File the Bituach Leumi claim
   URL: https://www.btl.gov.il
   - Unified online form through the gov.il national ID login
   - Required: bank details, termination letter, 6 most recent payslips, form 126 from last employer

3. Attend scheduled reporting (harshama) at Sherut HaTaasuka
   - Attend every scheduled meeting or face suspension
   - Apply to the required number of jobs per reporting period

4. Monitor the Bituach Leumi decision
   - First payment typically lands 30-45 days after registration
   - Check decision letter for any denial grounds

5. If denied or underpaid, file an appeal (irur)
   - Within 12 months of the decision
   - Appeal to the Labor Court (Beit Din Ezorit L'Avoda)
```

### Step 7: Flag Common Denial Risks

Warn the user if any of these apply to their case:

| Risk | What Bituach Leumi will do | How to avoid |
|------|---------------------------|--------------|
| Resigned without justified cause | 90-day waiting period | Document any justified grounds and provide evidence |
| Refused a job from Sherut HaTaasuka | 90 days + 30 days reduction | Do not refuse offers that match your profile |
| Did not register within 3 months | Lookback shifts, may lose qualifying months | Register immediately, within the first 2 weeks ideally |
| Missed scheduled reporting | Benefits suspended for the period | Always attend or reschedule in advance |
| Self-employed (osek) during last 18 months | Freelance months do not count toward tkufat akhshara | Need 12 salaried months specifically |
| Worked for a family member | Benefits denied unless proven arms-length employment | Need payslips, tax filings, real work evidence |
| Working part-time during unemployment | Benefit reduced proportionally | Report all income honestly |

## Bundled Resources

### References

| File | Purpose |
|------|---------|
| `references/eligibility-rules.md` | Full eligibility rule table including edge cases and exceptions |
| `references/benefit-calculation-tables.md` | 2026 progressive brackets, ceilings, and worked examples |
| `references/application-forms.md` | Links to all Bituach Leumi and Sherut HaTaasuka forms and portals |

### Scripts

| File | Purpose |
|------|---------|
| `scripts/avtala_calculator.py` | Command-line calculator that takes age, dependents, and 6-month salary and returns eligibility + daily benefit + max days |

## Recommended MCP Servers

| MCP | When to pair | Purpose |
|-----|--------------|---------|
| `kolzchut` (All-Rights) | For authoritative rule text with legal citations | Pulls live content from Kolzchut's database of Israeli social rights, including dmei avtala eligibility and exceptions |
| `israeli-cbs` | If comparing expected benefit against regional wages | Central Bureau of Statistics salary and employment data |

If neither MCP is installed, the skill still works from the built-in reference tables, but the user should cross-check numbers against kolzchut.org.il or btl.gov.il before taking action.

## Gotchas

1. **Confusing qualifying months with calendar months**. One day of work in a month counts as a full month. Agents often miscount because they assume 30 days equals 1 month. Use the "any paid day in the month" rule.

2. **Telling a resigner they get 90 days of nothing**. The 90-day waiting period blocks benefits for 90 days, but it does NOT reduce the total entitlement. After the wait, the full max days apply. Do not double-count the loss.

3. **Mixing up the under-28 and 28+ rate tables**. The under-28 rates are significantly lower (60/40/35/25%) than the 28+ rates (80/50/45/30%). Agents often grab the wrong table for a 26-year-old.

4. **Ignoring the 3-month registration window**. If the user missed the 3-month window from their last workday, the lookback shifts and they may have fewer qualifying months. Always ask when they last worked AND when they registered (or will register).

5. **Applying the wrong daily ceiling past day 125**. After 125 days, the ceiling drops from ₪550.76 to ₪367.17. Agents keep using the higher number and overstate the benefit.

6. **Counting osek (freelance) months as qualifying**. Only salaried (shakhir) work counts toward tkufat akhshara. A year of freelance equals zero qualifying months.

7. **Promising the gross amount as net**. Benefits are taxable. The user's take-home is always lower. Show gross AND estimated net.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Bituach Leumi: unemployment benefits eligibility (official) | https://www.btl.gov.il/benefits/Unemployment/Pages/zakaut.aspx | Authoritative eligibility rules |
| Kolzchut: dmei avtala (right) | https://www.kolzchut.org.il/he/%D7%93%D7%9E%D7%99_%D7%90%D7%91%D7%98%D7%9C%D7%94 | Plain-language rules and exceptions in Hebrew |
| Kolzchut: qualifying period (tkufat akhshara) | https://www.kolzchut.org.il/he/%D7%AA%D7%A7%D7%95%D7%A4%D7%AA_%D7%90%D7%9B%D7%A9%D7%A8%D7%94_%D7%9C%D7%93%D7%9E%D7%99_%D7%90%D7%91%D7%98%D7%9C%D7%94 | How months are counted |
| Kolzchut: maximum days by age and dependents | https://www.kolzchut.org.il/he/%D7%9E%D7%A1%D7%A4%D7%A8_%D7%94%D7%99%D7%9E%D7%99%D7%9D_%D7%94%D7%9E%D7%99%D7%A8%D7%91%D7%99_%D7%9C%D7%A7%D7%91%D7%9C%D7%AA_%D7%93%D7%9E%D7%99_%D7%90%D7%91%D7%98%D7%9C%D7%94 | Max days table |
| Sherut HaTaasuka: applicant info | https://www.taasuka.gov.il/applicants/dmeiavtala/ | Registration steps |
| Bituach Leumi: special benefits for women 57-67 | https://www.btl.gov.il/benefits/Unemployment/Pages/zecoyot-nasim.aspx | 300-day track rules |

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Benefit amount looks too high | Did not apply the daily ceiling or used wrong age tier | Re-check age is 28+ vs under-28, apply ₪550.76 / ₪367.17 ceilings |
| User has only 11 qualifying months | Just short of the 12-month threshold | Explain the rule. If they can wait one more month of salaried work, they reach 12 |
| Resigner confused about 90-day wait | Thinks they lose 90 days of total entitlement | Clarify: the 90-day wait delays the start, but does not reduce total max days |
| User was fired from a family member's business | Bituach Leumi rejects as non-arms-length | Advise gathering evidence: payslips, bank transfers, form 126, contract |
| Calculation shows benefit below minimum wage | Low salary user | Confirm tier 1 at the correct rate (80% for 28+, 60% for under 28). Still may be low, that is the legal minimum |
| Claim denied with no explanation | Decision letter unclear | Appeal to Beit Din Ezorit L'Avoda within 12 months |
