# Calculator Walkthrough (Shaagat HaAri, March-April 2026)

> **REGENERATED 2026-07-14 from `scripts/calc_grant.py`.** Every example below previously
> computed `MAX(wage track, fixed-cost track)`. That is not the law. §38לו defines הוצאות
> מזכות as the fixed expenses **plus** the eligible wage part, capped, then **doubled**.
> These examples are the calculator's own output, so prose and code cannot drift apart.

Command shape:

```
python scripts/calc_grant.py --ref-turnover R --claim-turnover C \
    --wages W --employees N --vat-inputs V --base-year-turnover B [--sector fuel|vat-exempt|contractor]
```

Reminder: `--vat-inputs` is the PREVIOUS year's total current VAT inputs (סך התשומות
השוטפות), NOT the owner's monthly rent and utilities. `--wages` is Form 102 gross wages
for March-April 2026, already net of vacation pay used and of any BTL reserve-duty
reimbursement to the employer.

## Example 1 - cafe, 40% decline, payroll + fixed costs

```
$ python scripts/calc_grant.py --ref-turnover 280000 --claim-turnover 168000 --wages 70000 --employees 5 --vat-inputs 336000 --base-year-turnover 1680000
=== Shaagat HaAri indirect-damage compensation (March-April 2026) ===

Turnover decline:      40.0%
Status:                OK (nationwide track)

Wage part              28,000.00 NIS  (per-employee cap 34,422.50)
Fixed-cost part      + 3,920.00 NIS  (coefficient 7.00%)
Eligible expenses    = 31,920.00 NIS  (ADDED, not compared)
Cap (before x2)        600,000.00 NIS
x2 per §38לו

TOTAL GRANT:           63,840.00 NIS

NOTE: fixed expenses come from the PREVIOUS year's total VAT inputs / 6,
      NOT from the owner's monthly rent and utility bills.
```

## Example 2 - small business (250-300K band), 70% decline

```
$ python scripts/calc_grant.py --ref-turnover 45000 --claim-turnover 13500 --base-year-turnover 270000
=== Shaagat HaAri indirect-damage compensation (March-April 2026) ===

Turnover decline:      70.0%
Status:                OK (small-business continuity track, <=300K turnover)

Small-business grant:  23,904.00 NIS
  (statutory monthly amount x damage coefficient, then x2 per §38לז(ב))

TOTAL GRANT:           23,904.00 NIS

NOTE: fixed expenses come from the PREVIOUS year's total VAT inputs / 6,
      NOT from the owner's monthly rent and utility bills.
```

## Example 3 - decline exactly 25%: NOT eligible on any track

```
$ python scripts/calc_grant.py --ref-turnover 100000 --claim-turnover 75000 --base-year-turnover 600000
=== Shaagat HaAri indirect-damage compensation (March-April 2026) ===

Turnover decline:      25.0%
NOT ELIGIBLE:          Decline 25.0% does not EXCEED the statutory 25% gate. No track is available, including the small-business track (§38לז(ב) incorporates the same >25% test through (a)(2)).
```

## Example 4 - execution contractor (sector coefficient x0.68)

```
$ python scripts/calc_grant.py --ref-turnover 500000 --claim-turnover 250000 --wages 200000 --employees 10 --vat-inputs 600000 --base-year-turnover 3000000 --sector contractor
=== Shaagat HaAri indirect-damage compensation (March-April 2026) ===

Turnover decline:      50.0%
Status:                OK (nationwide track)

Wage part              86,056.25 NIS  (per-employee cap 86,056.25)
Fixed-cost part      + 68,000.00 NIS  (coefficient 68.00%)
Eligible expenses    = 154,056.25 NIS  (ADDED, not compared)
Cap (before x2)        600,000.00 NIS
x2 per §38לו

TOTAL GRANT:           308,112.50 NIS

NOTE: fixed expenses come from the PREVIOUS year's total VAT inputs / 6,
      NOT from the owner's monthly rent and utility bills.
```

## Example 5 - large firm, cap binds

```
$ python scripts/calc_grant.py --ref-turnover 5000000 --claim-turnover 1000000 --wages 3000000 --employees 120 --vat-inputs 12000000 --base-year-turnover 30000000
=== Shaagat HaAri indirect-damage compensation (March-April 2026) ===

Turnover decline:      80.0%
Status:                OK (nationwide track)

Wage part              1,652,280.00 NIS  (per-employee cap 1,652,280.00)
Fixed-cost part      + 300,000.00 NIS  (coefficient 15.00%)
Eligible expenses    = 1,952,280.00 NIS  (ADDED, not compared)
Cap (before x2)        600,000.00 NIS   <- APPLIED
x2 per §38לו

TOTAL GRANT:           1,200,000.00 NIS

NOTE: fixed expenses come from the PREVIOUS year's total VAT inputs / 6,
      NOT from the owner's monthly rent and utility bills.
```

