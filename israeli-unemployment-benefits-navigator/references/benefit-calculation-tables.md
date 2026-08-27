# Dmei Avtala 2026 Benefit Calculation Tables

All figures effective 01.01.2026 and linked to inflation. They re-link in January 2027. Source of truth: btl.gov.il/benefits/Unemployment/Pages/hisuv.aspx (kolzchut.org.il occasionally lags by a year on the BL deduction figure). Verify the current-year table before quoting numbers.

## Base Figures (2026)

| Figure | Value |
|--------|-------|
| Daily base amount | ₪415 |
| Daily ceiling, days 1-125 | ₪550.76 |
| Daily ceiling, days 126-175 | ₪367.17 |
| Daily ceiling, days 176+ (women aged 57-60 on the 300-day track ONLY) | ₪201.03 (effective 01.01.2026) |
| Daily ceiling, days 176+ (women aged 60-67 on the 300-day track) | ₪367.17, no extra cap |
| Statutory minimum daily benefit, discharged soldier | ₪144.62 |
| Daily ceiling for a repeat claimant under 40, after 100% of days used | ₪468.15 |
| Bituach Leumi monthly deduction from benefit | ₪48 (effective 01.01.2026) |
| Divisor for average daily wage | 150 (= 25 days * 6 months) |

## Progressive Rate Tables

### Claimants Under 28 Years Old

| Daily wage bracket | Rate applied to bracket |
|-------------------|-------------------------|
| ₪0 to ₪207.50 | 60% |
| ₪207.50 to ₪311.25 | 40% |
| ₪311.25 to ₪415 | 35% |
| ₪415 to ₪2,075 (5x the basic daily amount) | 25% |

**Example calculation (under 28, ₪10,000/month gross):**
```
Sum of last 6 months gross: 60,000
Average daily wage: 60,000 / 150 = 400
Bracket 1 (0 to 207.50): 207.50 * 60% = 124.50
Bracket 2 (207.50 to 311.25): (311.25 - 207.50) * 40% = 41.50
Bracket 3 (311.25 to 400): (400 - 311.25) * 35% = 31.06
Daily gross benefit: 124.50 + 41.50 + 31.0625 = 197.0625, shown as 197.06
Approx monthly gross (25 days): 197.06 * 25 = 4,926.50
```

### Claimants 28 Years and Older

| Daily wage bracket | Rate applied to bracket |
|-------------------|-------------------------|
| ₪0 to ₪207.50 | 80% |
| ₪207.50 to ₪311.25 | 50% |
| ₪311.25 to ₪415 | 45% |
| ₪415 to ₪2,075 (5x the basic daily amount) | 30% |

**Example calculation (28+, ₪15,000/month gross):**
```
Sum of last 6 months gross: 90,000
Average daily wage: 90,000 / 150 = 600
Bracket 1 (0 to 207.50): 207.50 * 80% = 166.00
Bracket 2 (207.50 to 311.25): (311.25 - 207.50) * 50% = 51.88
Bracket 3 (311.25 to 415): (415 - 311.25) * 45% = 46.69
Bracket 4 (415 to 600): (600 - 415) * 30% = 55.50
Daily gross benefit: 166.00 + 51.875 + 46.6875 + 55.50 = 320.0625, shown as 320.06
Ceiling check: 320.06 < 550.76 (ok for days 1-125)
Approx monthly gross (25 days): 320.06 * 25 = 8,001.56
```

## Long-Entitlement Projection (post-day-125 drop)

For claimants in 138, 175, or 300 day brackets, the average daily benefit drops at day 126. Project the front portion at the day-1-to-125 ceiling and the tail at the day-126+ ceiling separately. Example for a 138-day entitlement at ₪320.06/day with no ceiling collisions:

```
Days 1-125: 125 * 320.06 = 40,007
Days 126-138: 13 * 320.06 = 4,161 (still below 367.17 ceiling, no further cap)
Total entitlement gross: ~44,168
Then subtract the unpaid first 5 unemployment days in each 4 consecutive attendance months (see below)
```

If the user's calculated daily rate exceeds ₪367.17, the tail portion is capped at the lower ceiling. Do NOT multiply the day-1 rate by the full max-days; you'll overstate by 5-15% on long entitlements.

**The women's 300-day track (ages 57-67, born 1/1/1960 or later) splits in two at age 60, and the split governs the AMOUNT, not the duration.** Both sub-bands get 300 days over an 18-month window.

- **Women 57 to 60:** from day 176 the daily benefit is capped at **₪201.03** (2026). Project in three slices: days 1-125 at ₪550.76, days 126-175 at ₪367.17, days 176-300 at ₪201.03. A woman in this band who participates in vocational training is paid 100% of her wage but still no more than ₪201.03 a day. Refusing vocational training in the first 175 days costs her 90 days of disqualification plus 30 days off the entitlement, leaving 270.
- **Women 60 to 67:** there is **NO day-176 cap**. Her tail stays at the ₪367.17 ceiling, she is paid 100% during vocational training, and refusing work or training does not cut her benefit. Applying the 201.03 cap to her understates her entitlement by (367.17 - 201.03) for each of the 125 days from day 176, which is up to **₪20,767.50** for a claimant at or above the 367.17 ceiling, and proportionally less for a lower daily rate. Below ₪201.03 a day the cap makes no difference at all.

Source: btl.gov.il/benefits/Unemployment/Pages/zecoyot-nasim.aspx, which sets out the two sub-bands separately ("זכויות לנשים בגילאי 57 עד 60" and "זכויות לנשים בגילאי 60 עד 67").

## Payable days per month

Bituach Leumi does not pay a flat calendar month. It pays for the **"possible work days" in each calendar month, and those days EXCLUDE Shabbat**, so a real month is usually around 26 payable days rather than 25 or 30. The number therefore moves month to month.

`ימים אלה אינם כוללים את ימי שבת` (btl.gov.il/benefits/Unemployment/Pages/pay.aspx)

Two consequences worth stating to the user. First, `daily * 25` is a conservative baseline for a monthly figure, not a promise; label it "approximate". Second, do not confuse this with the **150 divisor** used to build the average daily wage, which is a separate BL convention (25 working days x 6 months) and is not affected by how many days a given month happens to carry.

Then subtract the unpaid first-5-day blocks (see the end of this file), which are the larger correction in month 1.

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

**Who counts as a tlui (dependent) is a statutory test, not a judgement call.** Source: btl.gov.il/benefits/Unemployment/Pages/tkufat_zakaut.aspx.

- **Dependent husband:** aged 70 or over, OR aged 50 or over with income no higher than 57% of the average wage, **₪7,848 a month (from 01.01.2026)**.
- **Dependent wife:** all three must hold. (a) she has been his wife for at least a year or bore him a child; (b) she is 45 or over, or has his child living with her; (c) her income is no higher than **₪7,848 a month (from 01.01.2026)**.
- **Child:** son or daughter, including a stepchild, an adopted child, or a grandchild whose entire maintenance falls on the insured, excluding a married minor, who meets ONE of: under 18; under 20 and completing upper-secondary studies or studying for a bagrut, or with a learning disability in a framework BL recognises; under 20 and a shocher in an IDF pre-military framework; under 21 volunteering for a public purpose for up to 12 months with military service deferred for it; under 24 in regular IDF service; under 24 volunteering in national service; under 24 studying in atuda with regular service deferred for the studies.

The last four limbs are the ones agents drop. A 22-year-old in regular IDF service IS a tlui, and missing them can move a 30-year-old claimant from 100 days to 138. Single-parent claims are NOT automatically treated as 3+ dependents; count the actual dependents against the limbs above.

## Hefreshim (retroactive differentials)

If, after the employment ended, the employer pays the claimant anything **for the 6 months of work that were used to compute the benefit**, the claimant may be entitled to a differential top-up on benefit already paid. Apply to the local Bituach Leumi branch; it is not paid automatically.

`אם לאחר שהפסקת לעבוד קיבלת ממעסיקך תשלומים עבור 6 חודשי העבודה שנלקחו לצורך חישוב דמי האבטלה, אתה עשוי להיות זכאי לתשלום הפרשים לדמי אבטלה.` (btl.gov.il/benefits/Unemployment/Pages/hisuv.aspx)

Typical triggers: a bonus paid late, back-pay after a wage dispute, or a labour-court settlement, any of which commonly land months after the claim was decided.

## Deductions From Gross Benefit

Before the claimant receives money in their bank account:

1. **Income tax** at the claimant's marginal rate. Often near 0% because dmei avtala is typically below the first tax bracket annual ceiling after credits (nekudot zikui). High earners still hit mass.
2. **Bituach Leumi contribution**: fixed ₪48 per month (effective 01.01.2026; kolzchut still shows the older ₪32 figure, btl.gov.il is authoritative)
3. **Mas briut (health tax)**: percentage of the benefit

**Rule of thumb:** Low-income claimants net close to 100% of gross. Mid-income net approximately 85-90% of gross. High-income (hitting ceilings) net approximately 80-85%.

## Special Cases

| Case | Effect on calculation |
|------|----------------------|
| Worked part-time during unemployment | BL compares per day, it does not take a flat percentage. Gross monthly wage divided by the number of days actually worked gives an average daily wage; if that is BELOW the daily benefit the claimant gets the difference for those days and the full benefit for the remaining days; if it is at or ABOVE the daily benefit, nothing is paid for those days. Self-employed income: annual income / 12 / 30, settled only after the final tax assessment. Pension: gross monthly pension / 30. Source: btl.gov.il/benefits/Unemployment/Pages/incomes.aspx |
| First-time claimant who has never worked | Not eligible (tkufat akhshara not met) |
| Return to the same employer briefly | A new claim may only be filed 12 months after the start of the previous entitlement; before that, keep attending and draw the remaining days rather than re-filing (btl.gov.il/benefits/Unemployment/Pages/submit.aspx). Whether a short re-employment restarts the window is not published; ask the branch rather than asserting it |
| Vocational training stipend (hachshara miktzoit) | Avtala continues during approved Sherut HaTaasuka programs (kursim mukarim, maslulei mahalehet). May add an enhanced kiyum stipend. Days in training do not consume max-days the same way. Refusing assigned training = 90-day wait + 30-day deduction |
| Hashlamat hachnasa (income supplementation) | Low earners with dependents may stack avtala with hashlamat hachnasa via BL form 5320. The amount follows the hashlamat hachnasa rules; BL publishes no typical supplement figure, so do not quote one. Apply separately, not automatic |
| Vacation pay and pay in lieu of prior notice | These, not severance, postpone the benefit. No benefit is paid for a period covered by vacation pay under the Annual Leave Law, a collective agreement or an employment contract, nor for a period covered by payment for failure to give prior notice (at most one month). Legal pitzuei piturin do NOT delay or reduce avtala. Source: btl.gov.il/benefits/Unemployment/Pages/pay.aspx |
| Foreign work months | Work abroad counts only (a) for an Israeli employer under a contract signed in Israel, or (b) by aggregating periods from a country with which Israel has a treaty **in the unemployment branch**, which is only **Austria, the Netherlands and Sweden**. Israel's general social-security treaties (US, UK, Germany, France, Canada, Switzerland and others) do NOT cover unemployment. Source: btl.gov.il/benefits/Unemployment/Pages/DaysHaxhsharaAvt.aspx |
| Shaagat HaAri 2026 chal"t track **[CLOSED 14.5.2026, does not apply to new claims]** | Akhshara reduced to 6 months out of 18; **bifurcated minimum (effective 5.5.2026): chal"t qualifies from 5 consecutive days ONLY if started 28.2.2026 or 1.3.2026, otherwise 10 consecutive days**; avtala from day 1; no need to exhaust accrued vacation. Defining period 28 Feb to 14 Apr 2026 (extendable to 14 May 2026). The statute records itself as `התקבל בכנסת ביום י״ג בניסן התשפ״ו (31 במרץ 2026)`. **Retracted:** an earlier version cited a second and third reading on 4.5.2026 and a Sefer HaChukim volume 3525. Neither could be confirmed; do not reintroduce a Reshumot reference for this law |
| Claimant on long miluim service | Hok Khayalim Meshukhrarim s. 41a forbids dismissal during miluim and 30 days after. Registration window extended via hekel mizvad on request |


## Discharged soldiers (first year after release)

- Maximum **70** benefit days if the unemployment period starts in the first year after release from regular service.
- The daily benefit never falls below the **statutory minimum of ₪144.62** for a discharged soldier.
- Up to **6 months of regular service** count toward the 12-of-18 qualifying period; employed months that overlapped the service count too.
- Vocational training through the Employment Service in the first year: **no qualifying period required**, 70 days of benefit (or **138** days for someone with fewer than 12 years of education). Resigning in order to start that training is a justified resignation.
- Source: btl.gov.il, "משוחררים משירות צבאי ומשירות לאומי/אזרחי".

## Repeat claimant (mobtal chozer)

A repeat claimant is someone who filed **at least 2 unemployment claims in the last 4 years**.

| | Under 40 | 40 and over |
|---|---|---|
| Days | All claims in the 4-year window are capped at **180%** of the maximum days | If unemployment was paid in the 11 months before the claim, each month's days are reduced by the days already paid in the preceding 11 months (rolling window); otherwise as a first claim |
| Amount | Once 100% of the days are used, the daily maximum drops to **₪468.15** | **No cap on the amount** |

Bituach Leumi's own example: someone who used all 175 days and claims again gets 140 days (80%), with the first 125 capped at ₪468.15.

Source: btl.gov.il/benefits/Unemployment/Pages/MovtalHozer.aspx.


## The first 5 unemployment days are never paid

No benefit is paid for the **first 5 unemployment days in each 4 consecutive months of attendance**, counted from the date of first attendance at Sherut HaTaasuka. These days are **NOT** deducted from the maximum-days quota, so they shorten the cash, not the entitlement. The rule recurs roughly three times a year over a long claim, so a 138-day or 175-day projection that ignores it overstates the total by one or two 5-day blocks.

Source: btl.gov.il/benefits/Unemployment/Pages/pay.aspx ("לא ישולמו לך דמי אבטלה עבור 5 ימי האבטלה הראשונים בכל 4 חודשי התייצבות רצופים").
