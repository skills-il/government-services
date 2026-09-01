# Changelog

## 1.3.0 - 2026-09-02

Rebuilt the fee content on primary sources and closed several coverage gaps.

- Captured the full annual licence-fee table (7 licence groups x 4 year bands, 849 to 5,364 NIS) into `references/license-fee-table.md`, and put the lookup key in the body: the group is printed on the left side of the vehicle licence. The skill previously published only a range and told the user to go look it up.
- Replaced the secondary-blog sourcing for fees with the Ministry of Transport fee board and the price-controlled licensing-station order (קובץ התקנות 12400, effective 01.06.2026). Added the retest tariff, which was previously "a partial fee may apply".
- Corrected the broadcasting levy from 135 to the 139 NIS actually added to the renewal invoice.
- New sections: taking a vehicle off the road (ביטול רישום), including that a lien, pledge or 7A/8A debt blocks it and that a pro-rata fee is owed on a lapsed licence; and disability-related reductions (30 NIS annual fee, and the tax-difference repayment on transfer).
- New: the Ministry's fraudulent-transfer blocking service launched 27.07.2026, and the identity-theft pattern behind it (never send a photo of your vehicle licence to an unverified buyer).
- Settled the transfer-deadline question from the regulations themselves: תקנה 284 sets no express deadline; the widely-quoted 15 days comes from the residual clause תקנה 10. `references/ownership-transfer.md` still carried the "15-Day Deadline" section that v1.2.1 retracted from the body, so the skill shipped both a claim and its retraction.
- Rewrote `scripts/test-reminder.py`. It could never report an overdue test, keyed the due date off the registration anniversary rather than the licence expiry, and required a third-party package. It now takes `--expiry-date`, reports OVERDUE with the matching penalty band, uses the standard library only, and refuses to model vehicle classes it does not cover.
- Insurance: stated plainly that mandatory cover pays for no property damage at all, and added the residual insurance arrangement and Karnit.
- Added the green pollution rating (1 to 15) that drives purchase tax, and corrected the 2025 EV benefit ceiling to the Tax Authority's 35,000 NIS.
- Corrected TesTime from an SMS service to online booking. Removed the driver medical-examination and ride-hailing gotchas: both were outside the skill's stated scope and the ride-hailing one was factually wrong (Uber has not been approved to re-enter).
- Removed the unsourced light-electric-vehicle plate fee. The fee board carries no such line.
- Added the required `## Examples` and `## Reference Links` sections, and bootstrapped `references/domain-checklist.md`.
- Added the legal notice required by the skills-il legal gate (Tier B) immediately after the H1 in both languages, and the short qualifying clause opening both descriptions.
- Replaced six dead gov.il URLs found during verification, and added the licence-renewal, licence-deposit, reduced-fee/refund and disabled-parking-badge services. The Registrar of Pledges service slug has been renumbered, so the skill now routes by name instead of shipping a dead bookmark.
- Corrected the late-renewal timeline from an unverified "blocked after 3 months" to the Ministry's published sequence: reminder letters at about one, two and three months, and renewal at the Penalties Collection Center from about four months.
- Added, from the Ministry renewal service: an old vehicle renews every six months with an inspection certificate, an open safety recall blocks renewal, and the test cannot be done before the payment registers.
- Added the total-loss (אובדן להלכה) flag to the used-car checks, separated עיקול from שעבוד in the lien guidance, and removed a categorical "the creditor can seize the car" conclusion in favour of noting that a good-faith purchaser defence exists and is fact-dependent.
- Corrected the online-transfer payment window: it runs from completion of the transfer flow, not from opening the form.
- Softened the "one third of vehicles fail" statistic; the Ministry page carrying it is no longer published.
- Second review round: the retracted "the creditor can seize the vehicle from the new owner" sentence had survived in `references/ownership-transfer.md` after the body was fixed, which is the same one-file-only sweep failure the 15-day deadline showed. Swept to zero across both languages, both references and the script.
- Dropped the pre-test price range. Its evidence entry cited a page the snippet does not appear on, and the entry had been given a source_note wrongly asserting that page was dead.
- The test-reminder script no longer prints a shekel penalty or the no-grace-period line when it is only inferring from a registration date, because that accused compliant owners. It now says it cannot tell and sends the user to the licence.
- Softened the insurance-pool text to what the source actually supports (the Pool sells mandatory cover directly), removed an unsourced total-loss valuation claim, and noted that the Ministry does not define the age threshold for a rechev meyushan.
- Repointed the new-vehicle test exemption to a live source; the previous gov.il URL is a hard 404.

## 1.2.1 - 2026-08-13

Removed the 15-day ownership-transfer deadline. The only citation for it was a Kol-Zchut page that no longer exists, published figures disagree, and no primary source could be verified. The guidance now says to register the transfer the same day and explains that the seller stays liable until it is recorded.

