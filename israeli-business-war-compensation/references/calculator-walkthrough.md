# Calculator Walkthrough - All Four Tracks

Worked examples covering each of the four mutually exclusive compensation tracks under the Shaagat HaAri / Iron Swords frameworks. Use these as test cases when verifying an agent's calculation. All numbers below are illustrative inputs and derived outputs from the published formulas (see evidence.json for the source of every formula constant - average wage, tier multipliers, aggregate cap).

## Example 1: Tel Aviv café - wage track wins

Profile: café in central Tel Aviv, monthly VAT filer, 5 employees.

```
Inputs:
  Turnover March 2025         = 280000 NIS
  Turnover March 2026         = 168000 NIS
  March 2026 wages paid       = 70000 NIS
  Monthly fixed expenses      = 28000 NIS  (rent + electricity + leasing)
  Reporting period            = 1 month
  VAT cadence                 = monthly

Step A - eligibility
  decline = (280000 - 168000) / 280000 = 0.40   (40% drop)
  threshold (monthly filer) = 0.25              (PASS)
  annual turnover estimate ~ 168000 * 12 = 2.0M (within band)
  registration assumed pre-31.12.2024           (PASS)

Step B - wage track
  rawWageGrant = 0.75 * 0.40 * 70000 = 21000 NIS
  perEmpCap    = avgWage * 5 * 0.40            (per-employee × employees × decline)
  wageGrant    = min(rawWageGrant, perEmpCap)  (binding constraint reported by calc_grant.py)

Step C - fixed-cost track
  decline 0.40 sits at the 25-40% / 40-60% boundary
  conservative reading: tier multiplier = 0.07
  fixedCostGrant = 0.07 * 28000 * 1 = 1960 NIS

Result: wage track wins. File under the nationwide wage track.
```

## Example 2: Galilee restaurant evacuated since Oct 2023 - northern baseline

Profile: restaurant in Shtula (border yishuv), evacuated October 2023.

```
Inputs:
  Turnover March 2023         = 110000 NIS    (BASELINE - northern exception)
  Turnover March 2026         = 9000 NIS
  Wages paid                  = 0             (owner-only, no employees)
  Monthly fixed expenses      = 18000 NIS
  Reporting period            = 1 month

Step A - northern exception applies
  Baseline is March 2023 (not March 2025)
  decline = (110000 - 9000) / 110000 = 0.918   (91.8% drop)
  Northern dedicated track: NO minimum decline threshold required

Step B - track choice
  Shtula is on the red-track yishuv list
  Red track §35: no upper cap, profit losses compensable
  → recommend red track over wage/fixed-cost track

Step C - red track advance
  Per gov.il/he/pages/press_11032026, red-track businesses can request
  an advance up to 100000 NIS for the March 2026 damage period.

Result: file under red track §35. Request the advance immediately.
```

## Example 3: Solo bookkeeper - small business continuity track

Profile: osek murshe bookkeeper, no employees, home office.

```
Inputs:
  Turnover March 2025         = 18000 NIS
  Turnover March 2026         = 12500 NIS
  Wages paid                  = 0
  Monthly fixed expenses      = 1200 NIS
  Annual turnover (last year) = 215000 NIS

Step A - eligibility
  Annual turnover 215000 NIS is ≤ 300000 NIS
  → small business continuity grant track applies
  → 25% / 12.5% threshold does NOT apply on this track

Step B - exclusivity
  Small-business track is exclusive of wage/fixed-cost track
  Do NOT compute wage/fixed-cost
  Submit small-business form (separate flow)

Result: small business continuity grant per the gov.il table for
the 12000-300000 NIS bracket. Pull exact table amount from the
kolzchut entry: kolzchut.org.il/he/פיצוי_לעסקים_קטנים
```

## Example 4: Mid-size SaaS company - wage track wins despite per-employee cap

Profile: B2B SaaS, 8 employees on remote work, leased office.

```
Inputs:
  Turnover March 2025         = 850000 NIS
  Turnover March 2026         = 595000 NIS
  Wages paid                  = 220000 NIS
  Monthly fixed expenses      = 95000 NIS    (rent, AWS, leasing)

Step A - eligibility
  decline = (850000 - 595000) / 850000 = 0.30   (30% drop)
  Above 25% monthly threshold

Step B - wage track
  rawWageGrant = 0.75 * 0.30 * 220000 = 49500 NIS
  perEmpCap    = avgWage * 8 * 0.30
  wageGrant    = min(rawWageGrant, perEmpCap)
  Per-employee cap binds (wages above the average-wage proxy)
  → wageGrant ~ 33055 NIS

Step C - fixed-cost track
  decline 0.30 sits in 25-40% tier
  multiplier = 0.07
  fixedCostGrant = 0.07 * 95000 * 1 = 6650 NIS

Result: wage track ~ 33055 NIS clearly beats fixed-cost track 6650 NIS.
Surface that the per-employee cap reduced the grant from raw 49500 NIS.
```

## Example 5: Aggregate cap potentially binding - large corporation

Profile: retail chain, 60 employees, multiple stores.

```
Inputs:
  Turnover March 2025         = 4200000 NIS
  Turnover March 2026         = 2940000 NIS
  Wages paid                  = 1800000 NIS
  Monthly fixed expenses      = 540000 NIS

Step A - eligibility
  decline = 0.30, turnover 2.94M NIS within band
  Above 300000 NIS threshold → aggregate ceiling 600000 NIS applies

Step B - wage track
  rawWageGrant = 0.75 * 0.30 * 1800000 = 405000 NIS
  perEmpCap    = avgWage * 60 * 0.30
  wageGrant    = min(rawWageGrant, perEmpCap) ~ 247914 NIS

Step C - fixed-cost track
  fixedCostGrant = 0.07 * 540000 * 1 = 37800 NIS

Aggregate cap check: 247914 NIS < 600000 NIS → cap not binding here.
At higher wages it would clamp to 600000 NIS.

Result: wage track ~ 247914 NIS wins.
```

## How these examples were derived

Every dollar amount above is the output of the calc_grant.py script in scripts/, which encodes:

- The 75% wage formula multiplier (Shaagat HaAri framework)
- The average wage cap (13,773 NIS) on the per-employee branch
- The 25% / 12.5% eligibility threshold for monthly / bi-monthly filers
- The 12000-400M NIS annual turnover band
- The 300000 NIS small-business cutoff
- The 600000 NIS aggregate ceiling for businesses above the cutoff
- The fixed-cost tier multipliers: 7%, 11%, 15%, 22%
- The 100000 NIS red-track advance ceiling

Run `python scripts/calc_grant.py --example` to reproduce Example 1 directly.
