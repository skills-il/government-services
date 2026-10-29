# Changelog

## 1.3.1 - 2026-10-29

### Changed

- scripts/vehicle-decision.py: for an EV the worksheet now prints the tax under both official green reductions inside the EV floor (Customs Book table 14,523 NIS, the higher-tax case; ITA guide EV row 19,498 NIS), since the two official sources disagree. It now requires --gross-weight-kg and refuses, with no figures, for vehicles above 3,500 kg permitted total weight or motorcycles.
- Example 2 tells a hybrid importer to confirm the inspection route with *4515.

## 1.3.0 - 2026-10-29

### Fixed

- The 2026-08-13 fix that made US-spec cars importable had reached the Hebrew file only. The English body still said US-spec powertrains are routinely rejected for lacking EURO 6d certification. Removed; US federal and Canadian standards are accepted. Added what a North-American car does need: model approved for sale in the US or Canada, ESP, a metric speedometer, and an emissions letter, without which the worst pollution grade is assigned.
- The 48-month age limit is measured at registration in Israel (Takana 282, Misrad HaTachbura procedure 02/12), not at shipping. Added the 45-day and 7-working-day application cutoffs.
- The 12-month ownership-transfer restriction runs from Israeli registration, not from clearance.
- Removed an unsourced "current model year or one of the 4 previous model years" condition, an unsourced separate inheritance basket, and the "Tofes 195" form name.
- The entry deposit is a deposit of the applicable taxes for a returnee whose status is not yet determined, refunded on approval and forfeited if no application is made within 9 months; it is not "6 months of taxes refunded within 9 months".
- Restricted items: e-scooters, e-bikes, helmets, child seats and car parts go to Misrad HaTachbura on *5678, lasers to Misrad HaKalkala on *6680.
- SKILL_HE.md had Hebrew headings over an English body, so the Hebrew page rendered in English. It is now fully in Hebrew.

### Changed

- Vehicle taxes stated with the 2026 parameters: purchase tax 83% (hybrids and plug-ins included), 48% for EVs with the 22,000 NIS cap, the green-tax NIS table, VAT 18%, duty only outside a trade agreement. Nothing is enacted yet for 1.1.2027.
- Added salvage / total-loss, structural-modification and personal-payment bars, the one-vehicle-under-returnee-rights rule, the foreign-licence rule, the clearance document list, the hand-tool ($1,650) and business-equipment ($36,000 FOB) caps.
- scripts/vehicle-decision.py rewritten: checks age at registration and the 45-day cutoff and stops for an ineligible car (it used to print a full cost comparison for a car that cannot be imported); computes duty, purchase tax, green-tax adjustment, the EV floor and VAT instead of an invented hybrid band; requires the exchange rate.
- Pet entry rules moved to references/household-shipment-rules.md.

## Unlogged releases

Versions 1.2.1 to 1.2.4 shipped without a skill_updates entry; the 1.3.0 update notice covers them.

## 1.2.4 - 2026-08-19

### Fixed

- Translated section headings that had been left in English in SKILL_HE.md, where they rendered as-is on the Hebrew page. Hebrew is the site's default locale, and the skill validator never checked the Hebrew file, so these went unnoticed.

## 1.2.3 - 2026-08-13

Repointed the Section 14 handoff citation from a dead Kol-Zchut page to the Income Tax Ordinance itself, and replaced three raw Kol-Zchut URLs containing a gershayim with the page titles, since the quote character truncated them into dead links.

## 1.2.2 - 2026-08-13

Four corrections against the official personal-import page. US federal and Canadian standards are explicitly accepted, so the claim that US-spec vehicles are rejected for lacking EURO 6d certification is removed. Inspection is at a מכון רישוי under Takana 309 (registration conditioned by Takana 282), not a מכון לבטיחות בדרכים. ESP is verified from the technical spec and dashboard lamp; there is no 'takan 124'. The Tax Authority line is *4954, not 1299.

## 1.2.1 - 2026-08-11

Removed the fabricated pre-registration inspection fee ("~1,500-2,500 NIS, turnaround ~1 week"). No fee or duration is published by any official source.

All notable changes to this skill are documented here.

## [1.2.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
