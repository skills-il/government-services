# Changelog

## 1.5.0 - 2026-08-26

Added the March-2026 temporary provision (חוק עידוד עלייה לישראל וחזרה אליה (הוראת שעה), התשפ"ו-2026): an exemption on Israeli-source earned income for olim and toshav chozer vatik who became Israeli residents between 05.11.2025 and the end of tax year 2026, with the per-year ceilings, the reduced 140,000 NIS ceiling for income from a relative, the pro-rated 2026 ceiling, and the conjunctive forfeiture rule. The eligibility window closes at the end of tax year 2026.

Fixed the kupat cholim redemption (pidyon): the body already carried the correct fixed 16,860 NIS (2026), but the old "12 minimum monthly contributions" figure had survived in Example 3, in references/troubleshooting.md, in the checklist script, and as a contradictory entry inside evidence.json. All corrected.

Rental tax tracks: the skill listed only the 10% and progressive tracks and steered users to 10% "for simplicity". Added the exemption track for residential rent under the monthly exemption ceiling, which can tax qualifying rent at zero, and made it the first thing to check.

Return planning: added the Bituach Leumi residency questionnaire (Form 628) step, which gates the kupat cholim waiting-period clock and the restoration of kitzvat yeladim, and added the PIBA foreign-passport arrangement expiring 30.09.2026.

Scripts: relocation-checklist.py now filters phases by --stage (a returning user no longer receives the full pre-move checklist) and actually consumes --duration, which was declared but unused. residency-check.py now warns about the Section 100A exit tax and the kupat cholim consequence before recommending severance.

Amendment 272: dropped the unverifiable "published April 2025" date and repointed the citation, which had gone dead.

Also aligned the Misrad HaAliyah visits-test window with the sister skill, added references/domain-checklist.md, and moved detail to references/ to get back under the word cap.

---
## 1.4.1 - 2026-08-13

Corrected the early-withdrawal tax: withdrawing provident-fund savings before the statutory age costs 35% on the accumulated balance, not ~47%. The Kol-Zchut voluntary-Bituach-Leumi page no longer exists and has no successor, so that guidance now routes to BL directly instead of citing a dead page; the 7%/5% contribution rates it carried could not be verified against a primary source and were replaced with a pointer to BL.

All notable changes to this skill are documented here.

## [1.4.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
