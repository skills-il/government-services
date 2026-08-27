# Changelog

## 1.7.0 - 2026-08-27

Coverage cycle driven by enumerating the full Bituach Leumi tables rather than spot-checking the values already present. Every stated figure was correct; what was missing were rows.

- **The bracket cut-points were wrong at the third boundary.** BL publishes the boundaries as FRACTIONS of the basic daily amount for computing benefits (415 ILS from 01.01.2026), not as shekel figures. Three quarters of 415 is 311.25, not 311. Corrected in SKILL.md, SKILL_HE.md, references/benefit-calculation-tables.md and the calculator, which now derives every boundary from the basic amount instead of hardcoding shekels. The top band's upper limit (5x the basic amount, 2,075 ILS) was missing entirely and is now stated. Note that BL's own worked example on hisuv.aspx is still built on an older basic amount, so its shekel slices must never be copied forward.
- **The first 5 unemployment days are never paid, and the skill never said so.** No benefit is paid for the first 5 unemployment days in EACH 4 consecutive months of attendance, and those days are not deducted from the quota. The rule appeared only inside the closed Shaagat HaAri comparison table, as the "standard track" column. Every projection the skill produced overstated month 1 by five days of benefit. Now in Step 5, the Gotchas, the reference file, and the calculator output.
- **The exclusion list was absent.** A controlling shareholder in a closely-held company is not insured for unemployment EVEN WHEN he draws a salary and contributions were paid. So are an osek, a kibbutz or moshav-shitufi member working inside the collective, anyone in regular or national service during that service, and non-working students. The skill would have told all of them they qualified on 12 salaried months. Added as the first gate in Step 2.
- **The dependant test was wrong and incomplete.** It said a spouse earning above "about half the average wage" may not count and that BL decides per case. The real test is statutory: a husband at 70+, or 50+ with income no higher than 7,848 ILS (57% of the average wage, from 01.01.2026); a wife on three cumulative conditions. The "child" definition, absent altogether, has seven limbs including under-24 in regular IDF service, in national service, and in atuda. Dropping one limb can move a 30-year-old from 138 days to 100.
- **The justified-cause list did not match BL's published list.** Added: a family member's health (spouse, parent, child, grandchild, sibling); the 60 km test and the 40 km variant for a mother of a child under 7; a professional-certificate holder resigning to work in their trade; a domestic-violence shelter; resignation from a new job held up to 6 months; resignation from a second job continued up to 3 months. Removed the "25% pay cut over 6 months" test and the "occupational physician, not a GP" requirement, neither of which appears on any reachable BL page.
- **Retirement had no row at all.** Employer-initiated or early-retirement-scheme retirement pays from the first day of attendance; voluntary retirement is a 90-day wait, and a woman retiring voluntarily after 62 is treated the same way.
- **Employee-initiated chal"t is a disqualification, not a waiting period**, and the vacation-day offset on employer-initiated chal"t (50-day leave, 20 vacation days, benefit from day 21) was missing.
- **The refusal penalty was stated as universal and is not.** A woman aged 60 to 67 on the 300-day track keeps her benefit in full when she refuses work or training. A woman aged 57 to 60 who refuses training from day 176 forfeits her entire remaining balance, which is harsher than 90+30.
- **"Under 20: not eligible" was a wrong confident negative.** BL's own eligibility page says a person under 20 may be entitled in certain cases, and there is a separate grant track for a na'ar from 15. The closed exception list is now in the reference file, and the calculator no longer answers a 19-year-old with a flat refusal.
- **The national-service 70-day track has conditions** (24 months of service, or a woman with 6+ months who married within 30 days of stopping) that were not stated.
- **Calculator bug: the waiting-period note said the 90-day clock starts on the REGISTRATION date**, contradicting the skill's own body, its Gotchas, and BL's wording (`מיום הפסקת העבודה`). A user running the script was told the opposite of the correct rule.
- **Stale figures the 1.6.2 cycle believed it had removed were still live.** The "roughly 75% of the part-time gross wage" factor, retracted in 1.6.2, was still in references/application-forms.md and references/benefit-calculation-tables.md; the same file still carried the section 174 postponement rule that 1.6.2 had corrected elsewhere in the very same file. Both are now gone, replaced by BL's actual per-day offset mechanism (wage / days worked, compared against the daily benefit) read from incomes.aspx in a browser. Unverifiable circular numbers (1287, 1342) and the unsourced 1,500-2,000 ILS hashlamat range were removed rather than left asserted.
- Section parity restored (EN 20 / HE 20): five subsections existed only in Hebrew, duplicating content already in references/eligibility-rules.md. The closed Shaagat HaAri section was compressed to a dormant-mechanism summary, keeping both bodies under the 5,000-word cap for the first time in several cycles.

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
