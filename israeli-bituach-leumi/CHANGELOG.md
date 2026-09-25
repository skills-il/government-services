# Changelog

## 1.8.1 - 2026-09-26

Corrected the unemployment waiting days. The skill said the 5-day waiting period "applies only to
terminations". BTL's payment page says the first 5 days of unemployment in each run of 4
consecutive reporting months are unpaid for every claimant, and are not deducted from the benefit
quota. The 90-day wait after an unjustified resignation is a separate rule. Fixed in SKILL.md,
SKILL_HE.md and benefit-programs.md, with a new evidence entry.

Corrected unemployment eligibility. The skill said the job had to end "by termination, not
resignation". BTL's eligibility page includes anyone who was dismissed, resigned, or was put on
unpaid leave by the employer; the reason only affects when payment starts. Added the 20-67 age
condition and the 12-of-18 qualifying rule with its source. Fixed in SKILL.md, SKILL_HE.md and
benefit-programs.md.

Corrected the justified-cause list for resigning, in SKILL.md, SKILL_HE.md (instructions, Gotcha
and troubleshooting) and references/troubleshooting.md, and added BTL's full list to
benefit-programs.md. Relocation is a distance test (more than 60 km between the new home and the
workplace, or 40 km for a mother of a child under 7), not "following a spouse". The health ground
covers the claimant or a spouse, parent, child, grandchild or sibling, not generic "family care".
The end of a fixed-term contract is not a resignation: BTL pays it from the first reporting day.
The 90-day rule is now described as a delay to the start of payment, not a disqualification.

Added evidence entries for the 90-day wait, the 12-of-18 qualifying period, the age condition,
each justified cause, and the two training rules for women aged 57-60 (100% but no more than
201.03 a day; refusing training from day 176 forfeits the remaining days).

## 1.8.0 - 2026-09-25

Fixed the survivors qualifying period, which read "12 of the last 18, OR 24 of the last 60, OR
60 months total". BTL's rule is 12 insured months in the year before death, OR 24 in the last 5
years, OR 60 in the last 10 years, OR 144 in total, OR 60 since first becoming a resident.
Corrected in SKILL.md, SKILL_HE.md and the qualifying-period table in benefit-programs.md. The
same line also said a widow qualifies with "reduced earning capacity" (a dependents'-track rule);
it now states the 40+ or with-a-child rule and the widower income-test carve-out.

Reserve duty: added the partial-week ("40%") supplement (service days divided by 7, the remainder
adds 0.4 to 2 paid days), the self-employed base (reported advances, recomputed on the final
assessment) and the separate 25% self-employed compensation capped with the reward at the daily
maximum, the war-time wage-change rule for repeat call-ups from 1.5.25, and the employer
compensation of 20% of pay for pension and NI contributions during service. The calculator's
miluim estimate now applies the supplement (20 days pay 21, as in BTL's example) and the capped
25% compensation, and rejects a zero day count.

Household-help employers: added the two missing BTL rows, 3.6% for a worker resident in Judea and
Samaria or abroad, and 4.6% for a worker with a 100% work-disability or 75%+ general-disability
pension.

Evidence: repointed the form 480 snippet (the form was reissued 09.2026) and re-checked the
Kol Zchut entries in a browser.

## 1.7.2 - 2026-08-19

Fixed the reduced-band NI/health split written for the 67-70 non-pensioner row. The file said
"0.61% + 3.23% = 3.93%", which does not add up: 0.61% is the EMPLOYER rate for a minor. BTL
publishes only the employee total for that row (3.93% reduced, 10.03% full) plus the employer
columns, so the file now quotes the total and names the 3.23% health component, with a note
explaining why no reduced-band split is quoted.

Added the employer columns for the four naturalized-over-62 rows (1.04% / 0.7% / 0.66% / 0.61%
reduced, 2.95% / 2.47% / 2.31% / 2.12% full) and a new table of the controlling-shareholder
variants of the reduced rows (employer 0.6% / 2.06%, and 4.12% / 6.9% for ages 67-70). Removed
five em dashes from SKILL.md.

The published calculator (/tools/bituach-leumi-contributions) was rebuilt against this table.
It previously charged a working disability-pension recipient the standard 4.27% / 12.17% instead
of 3.23% / 5.17%, charged a woman aged 62-66 and an employee over 70 the standard rate, and knew
only two employer rates. It now covers all 20 payer categories from the official table.

## 1.7.1 - 2026-08-13

Moved the Troubleshooting section to references/ to bring SKILL.md under the 5,000-word validator cap, which it had been exceeding. No content was removed.

All notable changes to this skill are documented here.

## [1.7.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
