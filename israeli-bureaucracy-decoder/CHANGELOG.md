# Changelog

## 1.4.1 - 2026-10-31

The document analyzer no longer launches pdftotext itself: extract a PDF with `pdftotext -layout` first and pass the text file. The bidi-mark cleanup that recovers amounts and deadlines from PDF text is unchanged.

## 1.4.0 - 2026-10-29

Fixed wrong form numbers and deadlines across the forms index, the decision table and the bodies guide, each re-checked against gov.il, btl.gov.il or the statute text:

- Bituach Leumi claim forms: every number in the table was wrong. Reserve duty is 502, work injury 211, maternity 355, general disability 7801, unemployment 1500, child allowance 5025, old age 480, hostile action 580.
- Tax forms: 1214 is the company return (refunds go on 135, up to 6 years back), 1227 is not a real-estate form (a sale is declared on 7000 within 30 days), 134 is the excess-employer-contribution annex, and the 1301 companion forms "199-210 / 836" were replaced with the real annexes. VAT: 821 is registration; the periodic report is due by the 15th (19th online); the 874 and 852 descriptions were removed.
- Execution Office: an אזהרה on a judgment file gives 20 days, not 30. The 30-day opposition applies to bill and cheque files.
- Medical-committee ערר: 30 days for a work injury (60 stays correct for general disability).
- PIBA status decisions go to the Appeals Tribunal within 30 days, not to an internal appeal. ID cards and passports are PIBA services, not Interior Ministry offices.
- Planning: a permit refusal goes to the District Appeals Committee within 30 days; an administrative demolition order can be challenged in court within 15 days.
- Tax fines: a deficiency fine follows the 30-day objection route; a late-filing fine has no statutory appeal window.
- Apostille guidance corrected; added a note on administrative seizures that need no court order.
- New decision-table rows, each sourced to the statute: VAT and real-estate tax assessments, the arnona manager's answer and the 60-day deemed-acceptance rule, parking and traffic fine notices, Land Registry decisions (15 days), Small Claims, civil and Labour Court judgments, Execution Office registrar decisions, betterment levy assessments, and objections to הקלה / שימוש חורג notices. Urgency is now set by the length of the window. Each row points to the dedicated skill for the full procedure.
- The description now names court judgments, Execution Office warnings, fine notices and appeal deadlines, and term questions such as "what is a השגה", so those letters reach this skill.
- Reply drafting is limited to simple letters to an administrative body; for anything filed with a court, tribunal, appeals committee or the Execution Office registrar, the skill lists the points to raise and refers to a lawyer.
- Dead or moved links fixed: `kol-zchut.org.il` (does not resolve), `piba.gov.il`, `misim.gov.il`, the gov.il digital-identification page, the Justice Ministry e-signature page, and the unpublished Israel Law MCP.

Document analyzer: the window note now matches the sender and sub-type (a Land Registry refusal no longer gets Bituach Leumi's 12-month route, an income-tax order no longer suggests a second objection, a Small Claims judgment is no longer read as a claim); deadlines written as "תוך 30 יום" or in words are now found; the bidi marks that hid amounts and deadlines are stripped; reversed and visual-order text is detected; a Land Registry caveat is no longer flagged as an execution warning; typical-window notes now give the correct period for each document type.

## 1.3.3 - 2026-08-12

Freedom of Information: a complex request may be extended up to 120 days, not by an additional 30. Form 119 is the study-completion tax benefit, not a request for an advance tax ruling. Tax coordination is filed with Form 116 (or 101ג for pension-only pensioners), not Form 1325.

## 1.3.2 - 2026-08-11

Replaced the retired Enforcement and Collection Authority URL, which served gov.il's 404 page, with the live authority portal.

## 1.3.1 - 2026-08-10

Evidence re-grounded with deep links and verbatim quotes. Dropped an unverifiable phone line and corrected the Bituach Leumi second number to 04-8812345.

All notable changes to this skill are documented here.

## [1.3.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
