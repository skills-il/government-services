# Changelog

All notable changes to this skill are documented here.

## [1.3.0] - 2026-08-26

Corrected the kupat cholim waiting period. The skill stated a "minimum 2 months" floor for anyone abroad 12+ months; the cited Kol Zchut page states no minimum at all (the two-month figure there is a worked example). The rule is one waiting month per year of absence, capped at 6. The stale floor was also removed from references/eligibility-decision-tree.md, references/domain-checklist.md and from check-eligibility.py, which hard-coded it and so over-stated the wait for every returnee and pushed them toward an unnecessary 16,860 NIS redemption.

Added the waiting-period TRIGGER, which was missing entirely: the period applies only to someone abroad 18 consecutive months or more who also went 12+ months without paying health contributions, or who ceased to be a resident. A returnee who kept paying has no waiting period however long they were away.

Added the March-2026 temporary provision (חוק עידוד עלייה לישראל וחזרה אליה (הוראת שעה), התשפ"ו-2026) for toshav chozer vatik, with ceilings, the 140,000 NIS relative cap, the pro-rated 2026 ceiling and the conjunctive forfeiture rule. check-eligibility.py now raises it on the vatik branch. The eligibility window closes at the end of tax year 2026.

Corrected the passport guidance: the skill said boarding on a foreign passport is routinely refused, while its own evidence file recorded that the Population and Immigration Authority has permitted entry and exit on a valid foreign passport until 30.09.2026. The current rule and its expiry date are now stated.

Removed the invented call-centre language list (the ministry page lists Hebrew and Russian only), softened the unsourced 12-month retroactive kitzvat-yeladim window, and noted that official sources label the BL form "שאלון לקביעת תושבות" rather than by number.

metadata.json: tags were a bare array, so the site was showing Latin slugs as the Hebrew tags. Now nested {he, en}.

---

## [1.2.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
