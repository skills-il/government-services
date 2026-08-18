# Changelog

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
