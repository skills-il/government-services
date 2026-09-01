# Domain Coverage Checklist: israeli-vehicle-manager

Scope: managing ownership of a vehicle already in Israel. Bootstrapped 2026-09-02 (v1.3.0).

## Must cover (core)

| Item | Why it is core | Covered |
|---|---|---|
| Annual test (מבחן רישוי): who needs it, new-vehicle exemptions, what is inspected | The recurring compulsory event for every registered vehicle | Yes, Step 2 |
| Test and retest tariff by vehicle type | Price-controlled order, updated 1 June and 1 December; users ask "how much" | Yes, Step 2 + `license-fee-table.md` |
| 15+ year old vehicles: braking-system check at a licensed garage before the test | Extra precondition most owners are unaware of | Yes, Step 2 and Gotcha 5 |
| Annual licence fee: **the lookup key**, licence group 1-7 printed on the licence, by year of road entry | Fee varies about sixfold; a range without the key is unusable | Yes, Step 3 + `license-fee-table.md` |
| Full licence-fee table (7 groups x 4 year bands) | Rate-table completeness: a range is not the table | Yes, `license-fee-table.md` |
| Broadcasting Corporation levy added to the renewal invoice | Surprises first-time renewers | Yes, Step 3 |
| Renewal obligation runs from the printed expiry regardless of the mailed notice | Non-delivery is not a defence | Yes, Step 3 |
| Penalties for driving on an expired test, graduated | Direct financial and licence-point exposure | Yes, Step 3 and Troubleshooting |
| Mandatory insurance as a precondition of renewal | Blocks the renewal | Yes, Step 3 |
| Used-car checks: history report, pre-purchase inspection | The buyer's core due diligence | Yes, Step 4 |
| Liens and pledges: which register is authoritative, and that a pledge blocks a transfer | Buyer can lose the vehicle to a creditor; transfer cannot register | Yes, Step 4 |
| Used-car valuation: official MOT pricelist, commercial pricelist, and the adjustment factors | Anchors the negotiation | Yes, Step 4 |
| Ownership transfer: channels and fees, online / post / dealer / bureau | The transaction itself | Yes, Step 4 |
| How quickly the transfer must be registered, and the seller's continuing liability | The retracted "15 days" needs a correct replacement, not silence | Yes, Step 4 + `ownership-transfer.md` |
| Blocking a fraudulent post-office transfer, and the identity-theft pattern | Live MoT service since 27.07.2026; direct fraud exposure | Yes, Step 4 |
| Transfer after the owner's death (succession or probate order, bureau only) | Guaranteed lifecycle event | Yes, transfer table + `ownership-transfer.md` |
| Encumbered / leased vehicles: release letter, and who actually owns a leased car | Large share of the Israeli used fleet | Yes, Step 4 + `ownership-transfer.md` |
| Tax-difference repayment when transferring a vehicle bought with an exemption | Can materially change the price of such a car | Yes, Step 7 |
| Deregistration (ביטול רישום): when, what blocks it, the pro-rata fee | Fee accrues indefinitely on a scrapped car otherwise | Yes, Step 6 |
| Insurance types, and that chova covers no property damage at all | The most consequential misunderstanding in the domain | Yes, Step 5 |
| Residual insurance arrangement and Karnit | The two "I have no options" cases | Yes, Step 5 |
| Disability: reduced annual licence fee, and the transfer clawback | Fee is 30 NIS against 849-5,364; quoting the range is simply wrong | Yes, Step 7 |
| Light electric vehicles: registration duty and personal plate | Compulsory since 01.08.2024, widely ignored | Yes, Gotcha 6 |

## Should cover (advanced)

| Item | Covered |
|---|---|
| Green pollution rating 1-15 and its effect on purchase tax | Yes, Gotcha 2 |
| EV purchase-tax rate and benefit ceiling | Yes, Gotcha 2 |
| Reservist discount on the annual licence fee | Yes, Step 3 |
| Reservist deferrals on test and renewal deadlines | Yes, Gotcha 7 |
| Old vehicle (רכב מיושן): six-month renewal cycle with an inspection certificate | Yes, Step 3 |
| Open safety recall blocks renewal | Yes, Step 3 and Step 4 |
| Late-renewal letter sequence and the four-month Penalties Collection Center route | Yes, Step 3 |
| Renewing the licence of a deceased owner's vehicle | Yes, `ownership-transfer.md` |
| Residual insurance pool and the statutory compensation fund | Yes, Step 5 |
| Motorcycle licence and transfer fees | Yes, `license-fee-table.md` and transfer table |
| Collector, driving-school and duplicate-licence fees | Yes, `license-fee-table.md` |
| Personal import (יבוא אישי): the import process itself | **No.** Named only as a resale-value factor. Deferred, see `optimization-log.json` |
| Total loss / אובדן להלכה appearing on the vehicle record | Yes, Step 4 check 1 |
| Deposit of the licence (הפקדה) and the reduced-fee / refund route | Yes, Step 6 and Step 7 |

## Out of scope (explicit)

| Item | Rationale | Reviewed |
|---|---|---|
| Road accidents and insurance claims handling | Stated anti-trigger in the description; a claim is a separate workflow with its own skill surface | 2026-09-02 |
| Driver licensing: renewal, medical examinations, licence points as a standalone topic | Stated anti-trigger. Content on the age-75 medical exam was removed in v1.3.0 as scope leakage. Points are mentioned only as a consequence of a vehicle-side offence | 2026-09-02 |
| Ride-hailing / taxi-app market | Removed in v1.3.0. News trivia with no user action attached, and not vehicle-ownership paperwork | 2026-09-02 |
| Commercial fleet operations, trade licences, taxi and bus operation | A commercial operator is a different audience with a different regulator surface. The private-owner-relevant fee rows are still listed in the reference | 2026-09-02 |
| Buying a new car: importer negotiation, financing products | Consumer purchase advice rather than ownership administration | 2026-09-02 |
| Disabled parking permit (תו חניה לנכה) application procedure | A parking entitlement under the parking-for-the-disabled law, not vehicle registration. The skill names it and routes onward | 2026-09-02 |

## Authoritative sources

| Source | URL |
|---|---|
| MOT fee board (licence, transfer, special categories) | https://www.gov.il/he/pages/drivers-car-license-fee-boards |
| Licensing-station tariffs (price-controlled order) | https://www.gov.il/he/pages/2026-licensing-institute-rates |
| Ownership transfer service | https://www.gov.il/he/service/ownership-vehicles-transfer |
| Deregistration service | https://www.gov.il/he/service/request_to_cancel_vehicle_registration |
| Traffic Regulations, consolidated | https://www.nevo.co.il/law_html/law01/p230_011.htm |
| Israel Tax Authority, green taxation | https://www.gov.il/he/pages/sa311224-2 |
| Vehicle licence renewal | https://www.gov.il/he/service/car_licence_renewal |
| Licence deposit / cancellation of deposit | https://www.gov.il/he/service/request_to_deposit_vehicle_license |
| Reduced licence fee or refund | https://www.gov.il/he/service/exemptions_from_vehicle_license_fee |
| Registrar of Pledges | Ministry of Justice online services (the gov.il service slug has been renumbered; search by name) |
