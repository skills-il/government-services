# Changelog

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
