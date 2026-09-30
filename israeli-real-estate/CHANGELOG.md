# Changelog

## 1.8.0 - 2026-10-01

- Fixed the Fair Rent claim. The skill said the "Fair Rent" rules apply "since 2022"; the residential-lease chapter of the Rental and Borrowing Law was enacted in 2017 and has applied since 17 September 2017. Added its main exclusions (short leases, leases over 10 years, monthly rent above 20,000 NIS, CPI-updated) and replaced "deposit typically 1-3 months" with the statutory cap: the lower of 3 months' rent or the rent for a third of the term, returned within 60 days.
- Fixed the mas shevach linear-exemption note. It said the linear benefit is "legislated to be phased out from 2030". It is not abolished generally: section 48a(b4) withdraws it only for land that had no dwelling at purchase and on 1.6.2023, where the dwelling is completed after 31.12.2030.
- Added the war deadline extension (ITA circular 2/2026): a trading-up sale window that overlaps 28.2.2026 to 31.5.2026 gets 3 more months.
- Additional-home temporary order: still not extended as of 30 September 2026. Added the election carry-over under section 38 of Basic Law: The Knesset (reported, not an ITA ruling) and what happens if the order lapses (the lower permanent ladder starting at 5%).
- Added who qualifies for the single-home ladder: Israeli residents only (a foreign resident pays the additional-home rate unless they become a resident within 2 years), the family-unit rule (buyer, spouse and minor children are one buyer), and the homes that do not count (protected tenancy before 1997, a share of one third or less, or one half if inherited). Without these the skill quoted 0% to buyers who owe 8%, and 8% to buyers who owe 0%.
- Added the 6% rate for land and non-residential property, with the one-sixth refund when a dwelling permit follows within 24 months. Israel Land Authority tender plots were in scope with no rate at all.
- Added the gift rules (one third of the tax to a relative, exempt to a cohabiting spouse) and the Finance Minister's power to lengthen the war period.
- Lease running costs: replaced "clarify who pays" with the statutory allocation in section 25i (tenant pays arnona, utilities and routine vaad bayit; not building insurance, fixed systems or the landlord's broker).
- Removed unsourced claims: an "older 12% bracket" that no source shows existed, an oleh-track start date and residence claim, the 1% floor of the agent fee, and a betterment-levy "25% or full exemption" power that the Third Schedule does not grant in that form. The betterment bullet now follows sections 3a and 19(b)(10). Example 3 now produces a general checklist and points to raise with a lawyer, not recommendations on the user's own contract.
- Re-verified the purchase-tax ladders, the 5,008,000 NIS exemption ceiling, the betterment levy rate, the Bank of Israel LTV caps and the filing deadlines: unchanged. Re-ran `scripts/calculate_mas_rechisha.py` on all five tracks against hand-computed values; all match.

## 1.7.0 - 2026-08-19

- Re-verified the 2026 purchase-tax ladders against the primary source (הוראת ביצוע מיסוי מקרקעין 1/2026, 18 January 2026). All figures confirmed unchanged. Bracket amounts are normally CPI-updated every 16 January; these are frozen by the 2025 Arrangements Law for 16.1.2025 to 15.1.2028, and the skill now states that vintage explicitly instead of "frozen at 2025 levels".
- Confirmed the additional-home 8%/10% temporary order has NOT been extended: circular 1/2026 still ends it on 31 December 2026. Corrected its frozen tier vintage from 16.1.2024 to 16.1.2025 and named its statutory hook, section 9(c1f).
- Rewrote the Regulation 11 reduced track (disability, blindness, victims of hostile action, families of soldiers who fell in action) against the regulation text: the two cases as a table, the 2,500,000 NIS cliff (not a bracket), the twice-in-a-lifetime cap, and the fact that the relief needs an application and often a Bituach Leumi medical committee.
- `scripts/calculate_mas_rechisha.py` carried only the first-home and non-first ladders while the skill documented four tracks. Added `--track {first,additional,oleh,reduced-single,reduced-other}`, including the Regulation 12a relief ceiling at 20,183,565 NIS and the Regulation 11 cliff at 2,500,000 NIS. `--first` still works.
- Repaired two dead citations. `gov.il/he/pages/tax-purchase-1-2026` and `gov.il/he/departments/legalInfo/purchase-tax-additional-apartment` both 404 as of 19 August 2026; both now cite the ITA circular PDF, and the reduced track additionally cites the regulation text.
- Regenerated the `mas-rechisha` calculator: it now has a reduced-track buyer class, so a buyer with a disability or from a bereaved family is no longer charged the full ladder. Corrected the explanation text, which claimed the oleh track ends "8% and 10%" when Regulation 12a has no 10% band.

## 1.6.2 - 2026-08-13

Repaired three dead Kol-Zchut citations (linear mas shevach, single-home exemption, reduced purchase tax for buyers with a disability). The reduced purchase-tax passage claimed 0.5% up to a threshold, 5% above it, and twice in a lifetime; the source states no purchase tax up to 1,978,745 NIS and 0.5% on the remainder for a single home up to 2,500,000 NIS, and 0.5% flat otherwise, so the passage was rewritten. The single-home exemption ceiling is stated by the source as applying to 2024-2027, not 'frozen until 15 January 2028'.

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
