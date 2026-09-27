# Changelog

All notable changes to this skill are documented here.

## [1.1.0] - 2026-09-28

### Fixed

- Holder's duty to report: the skill, three references and the `moved` checklist said no rule obliges the holder to report a lost criterion. Criteria regulations 3(d) and 2(c) require notice to the licensing official "without delay" when the criterion, the status or the health condition stops applying. Corrected everywhere.
- Expired licenses: a request after expiry is now described as a new application (criteria regulation 8), with the licensing official's discretion to renew within 30 days of expiry (validity regulation 5), the 72-hour deposit of firearm, license and ammunition (regulation 9(a)), the receipt (Law s.14), refusal for non-deposit (9(b)) and the one-year offence (Law s.16(a)(1)). The 2014-procedure figures (district supervisor, 3-year block) were removed.
- Wartime extensions are presented as history. The April 2026 order expired on 31.8.2026; the June and July 2025 order and the 2023 and 2024 validity and training regulations (covered periods 26.10.2023 or 31.10.2023 to 31.12.2023, and 31.1.2024 or 1.1.2024 to 31.3.2024, with an extended date named for each month-end) are encoded as history. `calculate_license_dates.py` no longer treats them as current, applies an order to a date it names, and reports any other date inside a covered period or month as "possibly covered".
- Calculator status logic: while an extension may still apply (a possibly covered date, a reservist answer of "unknown" within 6 months of expiry, or a reservist extension combined with a temporary order, where the regulations do not say which date regulation 4A counts from), the status is "uncertain", with no surcharge and no offence note; the 72-hour deposit is shown only as "if no extension applies". An earlier draft of this release claimed that behaviour but still returned "expired" with a surcharge for an unknown reservist answer and anchored the reservist window on the pre-order date; both are fixed. The one-year note (Law s.16(a)(1)) is measured from the latest possible date, phrased conditionally before it, and describes s.16(a)(1) as a specific, lighter penalty (with Penal Law s.144(b1)). The late-renewal rule line cites the 72-hour rule instead of "immediately"; the delay is shown in months and days; a non-positive `--annual-fee` is rejected; the refresher's possible extension is no longer discarded.
- Loss or theft: Law s.15(a) counts 48 hours from the loss itself, not from learning of it; learning late is only a defence, and only together with reasonable holding conditions. Fixed in the references, both scripts and the clock table; `--loss-date` added. Automatic cancellation and the replacement rule are attributed to the 2014 procedure and hedged.
- Conditional approval: the expiry printed on the document governs; the 6-month figure (Knesset review, 2024) is shown only as an estimate, and `--conditional-expires` was added.
- Amendment 25 now states the medical-committee "unfit for service" condition and that the power is discretionary (Law s.11c(b)(2)). The unsourced "a false declaration is a criminal offence" and "omitting history is itself a false declaration" statements were removed.
- Appeals: the skill never produces a finished appeal letter or fills in the appeal form; it gives the structure and points for the user and their lawyer to write and sign. The legal notice gained the AI-fallibility, automatic-draft and not-a-substitute clauses.
- Renewal timing is labelled as the source states it: renewal in year 3, reminder from 3 months before expiry. Deposit after expiry is at the police station of residence or business (Law s.14). Dealer custody is sourced to Law s.14c, with a hedge for deposits forced by a missed refresher. The career-soldier relief (gov.il, 14.07.2025) is applied to the license extension as well as the refresher.
- Criterion 10(a) quoted from the regulation (kam and professional-officer ranks, 5-year or 60-day condition, exclusions) with the gov.il summary alongside; criterion 10(f) is the closed list of roles; the one-license limit for criteria 1 to 12 (regulation 7(a)(2)); the criterion-2 note that said "criterion 4".
- Dead dealers URL replaced with `gunshops_listing`; range and criteria URLs updated to their redirect targets; unsourced "form 19" and "voucher 388" removed; details that rested only on unlinked procedures 12.01.30 and 12.02.06 removed; the police-appeal route now cites Law s.12(c1)(2).
- All commands use `python3`; `allowed-tools` is `Bash(python3:*) WebFetch`; the compatibility line no longer claims Claude.ai.
- Frontmatter descriptions open with "Not legal advice."

### Added

- Reservist extension of the license (validity regulation 4A) and of the refresher (training regulation 3A), with `--reservist-expiry` and `--reservist-refresher` in the calculator.
- Extension on request (validity regulation 4: 30 days at a time, 45 in total) and the 10-year continuity renewal (criteria regulation 10, only while the license is valid).
- The active police volunteer criterion (item 11(c)), full role lists for items 4(c), 5 and 11, the combat-certificate age route (regulation 2(a)(4)(a2)), reservist relief for criteria 9 and 13 (regulation 3(g) and (h)), use restrictions (regulation 5), the regulation 11 exception, the 18-month memento window (regulation 12), and the consequences of a dealer deposit including sale after one year (Kol Zchut).
- Post-expiry clocks in the calculator (72-hour deposit, 30-day request) and a license-status line.
- While the status is uncertain, the calculator also shows the 30-day renewal-request cut-off that applies if no extension did (validity regulation 5), and after expiry the matching cut-off counted from a possible extended date. The expired status line now reads "expired on the dates given; confirm with the service center". An expiry between 1.1.2024 and 30.1.2024 gets a note that it falls between the two 2023/2024 orders.

## [1.0.0] - 2026-09-14

### Added

- Initial release. Stage map for the private firearm license process (eligibility, application, interview, conditional approval, training, purchase, magnetic card, year-2 refresher, year-3 renewal, expiry), with every clock sourced to gov.il, the Knesset Research and Information Center review of 13.02.2024, or the Firearms Law and regulations.
- `scripts/calculate_license_dates.py` for the 6-month conditional approval, the 3-month theory pass, the 3-year license, the refresher and renewal windows, late-renewal surcharge tiers, and the April 2026 emergency extensions.
- `scripts/build_stage_checklist.py` with English and Hebrew checklists for 13 stages and events.
- Six reference files: eligibility criteria, process stages, renewal and refresher, storage, ammunition and incidents, refusal and appeal, glossary.
- Hebrew companion `SKILL_HE.md` with section parity, and `evidence.json` with verbatim snippets from the sources read on 14.09.2026.
- "Voice and tone" section: everyday second-person Hebrew in the plural imperative, plain glosses for bureaucratic terms, official phrasing limited to numbers, dates and document names, and a serious register wherever the user may be committing an offence.
