# Changelog

## 1.6.1 (2026-08-11)

- Added a boundary to `israeli-tabu-extract-decoder`, which decodes an extract entry by entry. This skill explains what an extract is for and how to obtain one; it does not interpret each line.
- Removed three specific extract fees (regular, historical, consolidated). They rested on a commercial real-estate article rather than on the fee regulation, the amounts are index-linked, and at least three different figure sets are in circulation. The skill now cites תקנות המקרקעין (אגרות) and routes the user to the live government payments catalogue.
- Added the `Not legal advice.` opening clause to the SKILL.md frontmatter description, which previously carried it only in metadata.

All notable changes to this skill are documented here.

## [1.6.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, אילו התאמות שמאיות הוא אינו מבצע, ולאיזה בעל מקצוע מוסמך יש לפנות לקביעת שווי מחייבת, לעסקה במקרקעין ולחישוב מס.

### Changed

- הסקיל אינו מציג עוד "הערכת שווי נכסים" אלא ניתוח עסקאות השוואה מתוך עסקאות שדווחו ופורסמו, וזה מנוסח כך בתיאור, בטבלת הניתוב ובגוף המסמך.
- התיאור נפתח כעת בהבהרה שהפלט אינו שומת מקרקעין ואינו ייעוץ משפטי או מיסויי, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
