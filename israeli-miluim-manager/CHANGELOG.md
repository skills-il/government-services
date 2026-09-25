# Changelog

## 2.1.0 - 2026-09-25

Temporal pass on the combat tax credit, the 2026 Keren HaSiyua regulations, and deadlines falling before the end of 2026.

### Fixed

- **The permanent Section 39B table was missing, and the calculator applied the wrong table to 2027 service.** The 30-day table is a temporary provision for tax years 2026 and 2027 (`הוראת שעה בשנים 2026 ו־2027`), which means service in 2025 and 2026. From tax year 2028, that is for combat service from 2027, the permanent rule applies: 20 days = 0.75 point, +0.25 per further five days, capped at 4 points at 85 days. The skill previously framed this as "from 2028" and "planning service across 2027-2028", and the script had no year input, so a reservist with 50 combat days in 2027 would have been told 1.00 point instead of 2.25, and 20-29 days would have been told nothing. The script now takes `--service-year`, applies the right table, returns no credit for 2024 or earlier service, and flags that the 2028 point value is not yet published.
- **The Keren HaSiyua timing caveat was stale.** The 2026 regulations are published (current to 26.04.2026) and the 2026 budget law has passed; the skill still said neither had happened. Only the per-grant "dedicated policy" condition remains, and the skill now says to check a grant is open rather than that the package is pending.
- Manak Nezek Akif windows: the January-June 2024 periods have closed, and 2026 periods plus a new 21 / 30-day track from 01.01.2026 are now listed.

### Added

- **Keren HaSiyua filing deadline** (regulation 1.8): entitlement periods from 07.10.2023 to 31.12.2025 must be filed by 31.12.2026; from 2026, within a year of the event.
- **Partner income-loss compensation** (regulation 3.3.5): tier-banded 100 / 90 / 75 / 50%, 10+ consecutive shamap days, child under 14, NIS 10,000 a month and 40,000 a year, taxable.
- A prompt to ask about the previous year's combat days, since 2025 service is credited through Form 101 in 2026.
- A deadlines-before-end-of-2026 table in `references/2026-law-changes.md`.
- `allowed-tools: Bash(python:*)` in the frontmatter, declaring the one tool the bundled script needs.

### Fix round 1 (verification panel)

- Keren HaSiyua regulations re-cited to the current version of 05.07.2026, which adds Annex B, the transition provision. **Claims for service between 07.10.2023 and 31.12.2025, filed by 31.12.2026, are judged under the PREVIOUS regulations of 23.07.2025** (Annex B s.7(ב)). The 2026 partner income-loss tier bands are now scoped to 2026 service. A table in references sets out which rules govern which service.
- 2025 combat-array Tagmul Meyuchad beyond day 60 is 133.33, not 133. 2024 (flat 133) and the 2026 א'+ rate (133) are unchanged. The worked example now totals NIS 5,196.57.
- The Form 101 route is now sourced: file it with the employer during the year; once the year has ended, use an online refund request up to 6 years back. The unsourced "before the December payroll" wording is removed.
- "Service in 2024 or earlier earns no credit" is now sourced to the amending law's 01.01.2026 commencement (Tax Authority circular 16.12.2025).
- Script: the floor note now says what BTL says. The daily tagmul is never below NIS 328.76 for any employee or self-employed person, so a low earner is lifted to the floor. Below 30 days it no longer implies a "standard credit".
- Added references/domain-checklist.md, and a low-earner row in btl-payment-rules.md.

### Fix round 2 (verification panel)

- The 2023-2025 Keren rules are now sourced from the previous regulations themselves (`עדכני ליום 23/07/2025`), replacing a Kol Zchut summary. Those rules: partner income loss with no tiers, NIS 10,000 a month, and a higher amount through the exceptions committee. Nothing about tax is stated for that track. The NIS 4,500 grants now carry their OLD conditions: a status test on the release day, unpaid leave included, and no consecutive-days requirement for the partner. The NIS 10,700 grant and the 120-day combat-partner grant are listed.
- Script: zero income is now reported as "paid the floor directly", not as "above the floor". The working-youth minimum of NIS 114.73/day is noted, and the same row is added to btl-payment-rules.md.

### Evidence

- 23 legacy entries normalised to the canonical schema (`id` to `claim_id`, `fetched_at`, `appears_in`).
- 13 Kol Zchut entries that were unreachable to plain fetches were re-read in a browser; five snippets had drifted with page edits and were re-sliced to the current text.

## 2.0.3 - 2026-08-19

Closed the unevidenced procedural cluster carried since 2.0.1. Seven claims were checked against primary sources: two stood, one stood with a boundary the skill was missing, three were wrong, and one was unsupported anywhere.

### Fixed

- **Removed three Bituach Leumi processing windows that BTL does not publish** (30-60 days for employer reimbursement, 14-30 days, and 5-10 business days to payment). Its employer page says only to file `מוקדם ככול האפשר`. The only timings BTL actually publishes are the thresholds for filing a personal claim when nothing has arrived: 3 weeks after service for the self-employed, 2 weeks after discharge for someone on unemployment benefit. A nearby 14-day figure belongs to the indirect-damage grant and must not be imported.
- **Corrected the Manak Nezek Akif filing windows.** They are not short and rolling: every eligibility period from November-December 2024 onward closes on 31.12.2026. The November-December 2025 window runs 28.01.2026 to 31.12.2026, not to 31.05.2026. That May date belongs to the January-February and March-April 2024 periods and had been attached to the wrong period.
- **Corrected the exemption-age roster.** The dates and the two ages were right, but the six named roles were presented as "the roles at 49" when the order's schedule has 43 entries with 24 at 49. Two entries also split by RANK, which the earlier text erased: a remotely-piloted-aircraft operator is 49 only if an officer, and in unit 5410 an investigations officer is 49 while a prisoner interrogator is 45.
- **Added the boundary on Ministry of Justice legal aid.** The no-means-test track is real (regulation 4(b) disapplies the Legal Aid Law's economic limits) but regulation 1 scopes it to Labour Court proceedings `שהמוסד הוא צד בהם` and expressly excludes a claim `נגד מעביד`. A reservist suing their EMPLOYER over withheld pay is outside it. The skill discusses employer disputes heavily, so stating the aid without the boundary invited exactly the wrong inference.
- Replaced the bare "12 to 16 days a year" leave range with the statutory ladder: 16 days for each of the first five years, 18 in the sixth, 21 in the seventh, then one more per year up to 28.

### Verified and kept

- Form 101 carries the combat credit at part het, item 16.
- The appeal from a regional Labour Court runs 30 days, under regulation 73, from pronouncement, or from service where judgment was given in the parties' absence.

## 2.0.2 - 2026-08-18

The 2026 extension order was located in Rashumot and read, so the v2.0.1 hedge is replaced with sourced text. Two things in the order change the answer.

### Verified

- The successor instrument is **ילקוט הפרסומים 14498 of 29.04.2026, pages 5826-5830**, extending general collective agreement **7004/2026** signed 23.02.2026, signed by the Minister of Labour on 28.04.2026. The procedural chain is also in Rashumot: intent notice 03.03.2026 (י"פ 14321 p.4478), urgency notice 26.03.2026 (י"פ 14410), objection deadline 27.03.2026.
- Clause 3: `החל מיום 1 ינואר 2026 לתקופה בלתי קצובה`.
- Clause 5 carries the 30-plus-30 protection and DOES require seven consecutive days alongside 60 cumulative days, confirming a condition the superseded 2024 order did not contain.
- Clause 7: the supervision committee decides within 14 days, and closes the file within 5 days if it finds no dispute.

### Fixed

- **The protection is not retroactive, despite the order running from 01.01.2026.** Clause 5 ends `תוקפו של סעיף זה מיום פרסום צו זה ואילך`, and footnote 8 records that the Minister changed the agreement's original `מיום חתימת ההסכם` to say so. A dismissal before 29.04.2026 falls outside it. The earlier text would have told those users they were protected.
- **The 60 days are not calendar-year days.** Clause 2.4 defines the term to include prior-year days where the service ran continuously into the year, with continuity covering refresher service and gaps of up to five days. A reservist just short of 60 on calendar-year days alone may still qualify, and the earlier text would have turned them away.
- Public-sector employees are carved out, covered instead by the Government and Histadrut agreement of 26.03.2026.
- The spouse paid-absence table is now sourced (none up to 30 days, 2 for 31-60, 4 for 61-90, 6 for 91-120, 8 for 121+), closing one of the unevidenced clusters flagged in 2.0.1.

## 2.0.1 - 2026-08-18

Hotfix from the Independent Judge pass, which verified 111 of 120 claims but found nine broken citations and a set of figures whose only source was dead.

### Fixed

- **The days 31-60 dismissal layer was asserted on an instrument that expired on its face.** The extension order in evidence (י"פ 12159) fixes its own term at 07.10.2023 to 31.12.2024. A successor reportedly published 29.04.2026 was corroborated only by secondary sources and could not be confirmed from primary text, so the earlier release stated it as settled fact. It is now explicitly marked probable but unconfirmed, with the first 30 days (s.41A(b)) still stated as solid, and users are told to petition the supervision committee anyway because applying costs nothing and the window closes while they wait.
- **Removed five Bank of Israel figures** (a 3-month mortgage deferral, NIS 100,000 consumer and NIS 2,000,000 business loan deferrals, a 1% overdraft discount and an automatic NIS 30,000 self-employed overdraft). Their only citation was a Bank of Israel page that no longer resolves. A reservist would have quoted them to a bank.
- **Removed the *5266 lone-soldier number**, which appears on none of the pages checked and is uncorroborated.
- **Re-cited the 8944 hotline** to shikum.mod.gov.il after the original IDF unit page went dead.
- Repaired four evidence entries whose snippet was a bare URL or an HTML title rather than page text, and one that had a fragment from a different source spliced into it.
- Hedged the state-funded legal representation conditions as reported rather than verified, since the four-part eligibility test and its repayment undertaking are not in the evidence file.

## 2.0.0 - 2026-08-18

Major correction cycle. Four payment tracks, not three, and several claims that were shipped as facts turned out to be wrong.

### Fixed (user-harm)

- **Tagmul meyuchad is two layers, and the base one was missing.** v1.5.0 replaced the day-32 rule with the day-61 rule. Both are real: days 32-60 pay a flat 133.33 NIS per shamap day, and only the rate BEYOND day 60 is year-specific. A 70-day reservist was being under-told by 3,866.57 NIS, and anyone with 32-60 days was told they get nothing.
- **The beyond-60 rate is selected by service year.** The skill carried only the 2026 table. 2024 (flat 133) and 2025 (133/60/40) are tzav 8 only and still govern the cohort being paid in May 2026, which is the commonest live question.
- **The appeal deadline was the wrong body and the wrong clock.** references/troubleshooting.md said "file an appeal with Bituach Leumi within 6 months". The operative remedy is a filing with the regional Labour Court within 12 months of delivery of the decision (reg. 1(b), Moadim LeHagashat Tovanot). The 6-month window belongs to Vaadat Tviot, which can only recommend reconsideration and expressly does not pause the court clock.
- **The debt-offset instruction was inverted.** The skill told users arrears may be blocking their payout and to settle them. Bituach Leumi does not offset a debt unless the recipient asks it to.
- **Section 36A of the Defence Service Law was about to be cited for a payment.** It is the age-exemption provision with no payment language. The over-age tagmul is real and now documented, but that anchor is not.

### Added

- Fourth payment track: tagmul for over-age reservists, 133.33/day and 66.67/half-day, in addition to tagmul meyuchad, with the alouf mishne exclusion.
- Tagmul nosaf is no longer flagged unverified: 10+ cumulative shamap days under s.19, four bands to 5,808 NIS, the special 25% tax under s.19(e)(1), and the tension between the statutory payer (Tax Authority) and the operational route (IDF).
- Four Bituach Leumi income-basis rows that were missing entirely: non-workers, those who stopped work within 60 days of call-up, recent keva dischargees, and unemployment-benefit recipients.
- Employment protection rewritten around the right instruments: the void causal ban in s.41A(a1), the permit regime in s.41A(b) that also covers job scope and income, the notice-period exclusion in s.41A(c), the employer's burden in s.41A(d), and the s.21 remedies (a damages floor, not a cap).
- The 30 vs 31-60 day split now names both committees: Vaadat HaTaasuka (Defence) and Vaadat Pikuach (Labour).
- Spouse protection resolved into its two real layers: the permanent causal ban in s.41A2(b) with no day window, and a conditional 14-day temporary provision in force from 29.04.2026.
- State-funded legal representation for dismissal, shimua or unpaid leave over reserve service, including its repayment undertaking and the employees-only limit.
- Valtam and Form 58 routes for deferring or shortening a call-up, marked as army-order mechanisms with no statutory basis.
- Travel reimbursement, active-reservist (mashmap) status definition, BTL tax withholding, multi-employer rules, and escalation channels.
- New reference file `references/btl-payment-rules.md`.

### Changed

- SKILL_HE.md was never covered by the validator, which rejects any file not named SKILL.md. It was 6,762 words against a 5,000-word cap, still carried the Troubleshooting section that v1.6.2 moved out of the English file, and had two untranslated headings. Hebrew and English are now structurally aligned at 22 headings each.
- Travel deadline corrected from a reported 4 days to 2, and it forfeits nothing (fuel is claimable retroactively). The valtam appeal window is 72 hours, not the reported 7 days.

All notable changes to this skill are documented here.

## 1.6.2 - 2026-08-13

Moved the Troubleshooting section to references/ to bring SKILL.md under the 5,000-word validator cap, which it had been exceeding. No content was removed.

All notable changes to this skill are documented here.

## [1.6.1] - 2026-08-13

### Fixed

- Replaced 17 placeholder evidence entries with real sources. The credit-point value, the Section 39B combat-credit tiers and 4-point cap, the 2028 threshold, the self-employed keren hishtalmut ceilings, Form 101 and Form 106 are now quoted from the consolidated Income Tax Ordinance and the withholding regulations; the Labor Court fee from the Fees Regulations 2026 schedule; the 20% employer compensation and the *6050 number from Bituach Leumi.
- Removed the expedited Labor Court fee rate of "0.5%". The fee schedule sets a minimum of NIS 84 for an expedited hearing and states no percentage.
- Removed the Amendment 283 Knesset plenum date (19.11.2025) and Sefer HaChukim date (23.11.2025), and the 27.4.2026 plenum date for the 20% employer compensation. The Knesset site is unreadable to any automated fetch, so those dates were unsourced.
- The 60-day post-service dismissal protection for 60+ days of service is now marked unverified. Section 41A of the Discharged Soldiers (Return to Work) Law carries only the 30-day window in its consolidated text.

## [1.6.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
