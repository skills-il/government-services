# Changelog

## 1.6.2 - 2026-08-13

Replaced 20 placeholder evidence entries (source_url "TBD", raw_snippet "PENDING_VERIFICATION") with real sources, and corrected four claims the sources contradicted:

- Form 100 is NOT the wrong document. Bituach Leumi asks the claimant to check that the employer transmitted Form 100 (the wage data) and only otherwise to attach an employer confirmation or 12 payslips. The old text told users Form 100 alone causes rejection and that Form 126 is required; Form 126 is the employer's annual report to the assessing officer and is not on the BTL document list.
- The "suitable offer" test now follows Section 165: job type or training match, wage at least the benefit otherwise due, and a 60 KILOMETRE (not 60 minute) relocation test, with the relaxation keyed to AGE (14/30/60 days) rather than to day 60 for everyone. The old "salary within 25% of prior wage" test appears in no source.
- Part-time income is deducted from the benefit under Section 176; the "roughly 75% of the part-time gross" factor appears in no source and was removed.
- Section 174 of the National Insurance Law is the preferred-employment grant, not a "tashlumei avoda" postponement rule. What postpones the benefit is vacation pay and payment in lieu of prior notice.

Nine claims could not be sourced anywhere reachable and are now labelled NOT VERIFIED in evidence.json rather than carrying a placeholder: form 5040, form bl/627, the *2496 and *3450 hotlines, the 6-month / 12-month / 60-day appeal windows, the 75% disability block, unemployment circulars 1287 and 1342 (and with them the form-1514 substitution route), amendment 232 of 2023, and the NIS 1,500-2,000 hashlamat hachnasa range. The skill body now hedges each of them.

## 1.6.1 - 2026-08-12

Corrected the enactment date of the Economic Assistance (Employment) Law: the statute records 31 March 2026, not 4.5.2026. Removed the 'Sefer HaChukim 3525' reference, which appears nowhere in the statute. Replaced the cited gov.il page, which is the BUSINESS assistance scheme and contains no employment or unemployment content, with the statute text itself, and sourced the dormant reactivation window to Section 7 rather than a secondary summary.

All notable changes to this skill are documented here.

## [1.6.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
