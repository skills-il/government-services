# Dmei Avtala 2026 Benefit Calculation Tables

All figures effective 01.01.2026 and linked to inflation. They re-link in January 2027. Source of truth: btl.gov.il/benefits/Unemployment/Pages/hisuv.aspx (kolzchut.org.il occasionally lags by a year on the BL deduction figure). Verify the current-year table before quoting numbers.

## Base Figures (2026)

| Figure | Value |
|--------|-------|
| Daily base amount | ₪415 |
| Daily ceiling, days 1-125 | ₪550.76 |
| Daily ceiling, days 126+ | ₪367.17 |
| Bituach Leumi monthly deduction from benefit | ₪48 (effective 01.01.2026) |
| Divisor for average daily wage | 150 (= 25 days * 6 months) |

## Progressive Rate Tables

### Claimants Under 28 Years Old

| Daily wage bracket | Rate applied to bracket |
|-------------------|-------------------------|
| ₪0 to ₪207.50 | 60% |
| ₪207.50 to ₪311 | 40% |
| ₪311 to ₪415 | 35% |
| ₪415 to daily ceiling | 25% |

**Example calculation (under 28, ₪10,000/month gross):**
```
Sum of last 6 months gross: 60,000
Average daily wage: 60,000 / 150 = 400
Bracket 1 (0 to 207.50): 207.50 * 60% = 124.50
Bracket 2 (207.50 to 311): (311 - 207.50) * 40% = 41.40
Bracket 3 (311 to 400): (400 - 311) * 35% = 31.15
Daily gross benefit: 124.50 + 41.40 + 31.15 = 197.05
Approx monthly gross (25 days): 197.05 * 25 = 4,926.25
```

### Claimants 28 Years and Older

| Daily wage bracket | Rate applied to bracket |
|-------------------|-------------------------|
| ₪0 to ₪207.50 | 80% |
| ₪207.50 to ₪311 | 50% |
| ₪311 to ₪415 | 45% |
| ₪415 to daily ceiling | 30% |

**Example calculation (28+, ₪15,000/month gross):**
```
Sum of last 6 months gross: 90,000
Average daily wage: 90,000 / 150 = 600
Bracket 1 (0 to 207.50): 207.50 * 80% = 166.00
Bracket 2 (207.50 to 311): (311 - 207.50) * 50% = 51.75
Bracket 3 (311 to 415): (415 - 311) * 45% = 46.80
Bracket 4 (415 to 600): (600 - 415) * 30% = 55.50
Daily gross benefit: 166.00 + 51.75 + 46.80 + 55.50 = 320.05
Ceiling check: 320.05 < 550.76 (ok for days 1-125)
Approx monthly gross (25 days): 320.05 * 25 = 8,001.25
```

## Long-Entitlement Projection (post-day-125 drop)

For claimants in 138, 175, or 300 day brackets, the average daily benefit drops at day 126. Project the front portion at the day-1-to-125 ceiling and the tail at the day-126+ ceiling separately. Example for a 138-day entitlement at ₪320.05/day with no ceiling collisions:

```
Days 1-125: 125 * 320.05 = 40,006
Days 126-138: 13 * 320.05 = 4,161 (still below 367.17 ceiling, no further cap)
Total entitlement gross: ~44,167
```

If the user's calculated daily rate exceeds ₪367.17, the tail portion is capped at the lower ceiling. Do NOT multiply the day-1 rate by the full max-days; you'll overstate by 5-15% on long entitlements.

## Payment Cadence (5-weeks-per-month quirk)

Bituach Leumi pays per "reporting weeks" (chodesh dmei avtala = 4 or 5 weeks depending on Sundays in the calendar month), not per calendar month. About four months a year contain a 5-week BL month (about 31 paid days), and the others 4 weeks (about 25 paid days). When projecting cash flow for the user, label the figure "approximate monthly" and treat daily * 25 as a baseline only.

## Maximum Benefit Days Table

| Age at start of unemployment | Dependents | Max days | Notes |
|------------------------------|-----------|----------|-------|
| 20-25 | < 3 | 50 | 12-month window |
| 20-25 | >= 3 | 138 | 12-month window |
| 25-28 | < 3 | 67 | 12-month window |
| 25-28 | >= 3 | 138 | 12-month window |
| 28-35 | < 3 | 100 | 12-month window |
| 28-35 | >= 3 | 138 | 12-month window |
| 35-45 | < 3 | 138 | 12-month window |
| 35-45 | >= 3 | 175 | 12-month window |
| 45-67 | Any | 175 | 12-month window |
| Women 57-67 (born 1/1/1960 or later) | Any | 300 | 18-month window, special track |

"Dependents" count = spouse + children that the claimant financially supports. A spouse earning above ~½ the average wage may not count as a tlui (BL evaluates per case). Single-parent claims are NOT automatically treated as 3+ dependents; count the actual children supported.

## Deductions From Gross Benefit

Before the claimant receives money in their bank account:

1. **Income tax** at the claimant's marginal rate. Often near 0% because dmei avtala is typically below the first tax bracket annual ceiling after credits (nekudot zikui). High earners still hit mass.
2. **Bituach Leumi contribution**: fixed ₪48 per month (effective 01.01.2026; kolzchut still shows the older ₪32 figure, btl.gov.il is authoritative)
3. **Mas briut (health tax)**: percentage of the benefit

**Rule of thumb:** Low-income claimants net close to 100% of gross. Mid-income net approximately 85-90% of gross. High-income (hitting ceilings) net approximately 80-85%.

## Special Cases

| Case | Effect on calculation |
|------|----------------------|
| Worked part-time during unemployment | Gross benefit reduced by approximately 75% of the part-time gross wage. Below the BL kotzbat patur (small-earnings exemption) the reduction may not apply, verify thresholds |
| First-time claimant who has never worked | Not eligible (tkufat akhshara not met) |
| Return to the same employer briefly | A 30+ day re-employment can restart the 12-month entitlement window. Returning to the same employer within 90 days raises BL non-arms-length scrutiny |
| Vocational training stipend (hachshara miktzoit) | Avtala continues during approved Sherut HaTaasuka programs (kursim mukarim, maslulei mahalehet). May add an enhanced kiyum stipend. Days in training do not consume max-days the same way. Refusing assigned training = 90-day wait + 30-day deduction |
| Hashlamat hachnasa (income supplementation) | Low earners with dependents (especially single parents, families with 3+ children) may stack avtala with hashlamat hachnasa, typically ₪1,500 to ₪2,000/month, via BL form 5320. Apply separately, not automatic |
| Adam meritzon (severance beyond legal pitzuim) | Postpones the start by the equivalent number of months under National Insurance Law s. 174. Legal pitzuim alone do NOT delay or reduce avtala |
| Foreign work months under bilateral SS treaty | Counted toward akhshara via form בל/627. Treaty countries: US, UK, Germany, France, Canada, Switzerland, Belgium, Netherlands, Czech Republic, Bulgaria, Sweden, Austria, Finland, Romania, Uruguay, others |
| Shaagat HaArie 2026 chal"t track | Akhshara reduced to 6 months out of 18; chal"t qualifies from 5 days; avtala from day 1; no need to exhaust accrued vacation. Defining period 28 Feb to 14 Apr 2026 (extendable to 14 May 2026) |
| Claimant on long miluim service | Hok Khayalim Meshukhrarim s. 41a forbids dismissal during miluim and 30 days after. Registration window extended via hekel mizvad on request |
