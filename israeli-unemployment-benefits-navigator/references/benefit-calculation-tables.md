# Dmei Avtala 2026 Benefit Calculation Tables

All figures current for 2026. Source: Bituach Leumi, Kolzchut.

## Base Figures (2026)

| Figure | Value |
|--------|-------|
| Daily base amount | ₪415 |
| Daily ceiling, days 1-125 | ₪550.76 |
| Daily ceiling, days 126+ | ₪367.17 |
| Bituach Leumi monthly deduction from benefit | ₪32 |
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
Monthly gross (25 days): 197.05 * 25 = 4,926.25
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
Monthly gross (25 days): 320.05 * 25 = 8,001.25
```

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

"Dependents" count = spouse + children that the claimant financially supports.

## Deductions From Gross Benefit

Before the claimant receives money in their bank account:

1. **Income tax** at the claimant's marginal rate. Often 0% because dmei avtala is typically below the first tax bracket annual ceiling after credits (nekudot zikui). High earners still hit mass.
2. **Bituach Leumi contribution**: fixed ₪32 per month (2026)
3. **Mas briut (health tax)**: percentage of the benefit

**Rule of thumb:** Low-income claimants net close to 100% of gross. Mid-income net approximately 85-90% of gross. High-income (hitting ceilings) net approximately 80-85%.

## Special Cases

| Case | Effect on calculation |
|------|----------------------|
| Worked part-time during unemployment | Gross benefit reduced by 75% of the part-time gross wage |
| First-time claimant who has never worked | Not eligible (tkufat akhshara not met) |
| Return to the same employer briefly | May extend benefit duration if remains within 12-month window |
| Benefit from a vocational training stipend (hachshara miktzoit) | Treated differently, usually higher amount |
| Claimant is a single parent | No special calculation but treated as 3+ dependents for max days |
