# Domain Checklist - Aliyah Customs Shipment Planning

Coverage anchor for reviewers. Built 2026-10-29 from the Israel Tax Authority import-tax guide for new olim (gov.il/he/pages/guide-for-immigrants-and-foreign-residents, updated 21.10.2026), the Tax Authority customs guide for returning residents (updated 30.07.2026), the Ministry of Agriculture dog-and-cat import page (updated 22.10.2026) and veterinary certificate (Annex A), the Misrad HaKlita Guide for the New Immigrant (15th edition), and Nefesh B'Nefesh "Understanding Your Customs Benefits" (updated 12.03.2026).

## Must cover (core)

| Item | Where in the skill | Source |
|---|---|---|
| Who is entitled: oleh (incl. printed-confirmation only), Ezrach Oleh, Katin Chozer, permanent resident | Step 1 | Tax Authority olim guide |
| Toshav Chozer, including second-time olim, is a different track: 2 shipments, 9 months, not extendable | Step 1, Example 3, returning-residents.md, script exit 2 | Tax Authority RR guide |
| Window starts on the day oleh status is received; 3 years | Step 1, Gotchas | Tax Authority olim guide |
| Up to 3 shipments; what counts as a shipment (ship, plane, post, later entry) | Step 3, strategy | Tax Authority olim guide |
| Accompanying luggage on the aliyah flight is extra and not a shipment | Step 2, Step 3 | Tax Authority olim guide |
| Container rule (larger than a full container = 2 shipments unless same ship, cleared together) | Step 3 | NBN |
| Caps: 3 TVs, 3 computers, one of each appliance and major furniture item | Step 2 | Tax Authority olim guide |
| Permanently installed equipment is excluded | Step 2 | Tax Authority olim guide |
| Hand tools USD 1,650; business equipment USD 36,000 FOB incl. tools, Director approval, bank guarantee | Step 2, script | Tax Authority olim guide |
| 6-year personal-use rule, no transfer to others even free or temporarily; vehicle 4 years | Step 5 | Tax Authority olim guide |
| Extensions: regular service, studies (+1 year), 6+ months abroad, up to 6 years, exceptions committee | Step 3 | Tax Authority olim guide |
| Spouses: broader entitlement applies, 3 shipments together, shared caps, pre-marriage 6-year rule, other spouse's passport checked | Step 1, Gotchas | Tax Authority olim guide |
| Clothing-only postal package window (30 days before to 3 months after status) | Step 2 | Tax Authority olim guide |
| Green-lane traveller allowance (alcohol, perfume, tobacco, USD 200 per item, food) | Step 2 | Tax Authority olim guide |
| Pets: licence or licence-exemption before aliyah; 5 months, 90 days, 2 per year, rabies vaccine and titer | Step 2 | Ministry of Agriculture |
| Adults 18+ with independent household; minor exceptions | Step 1 | Misrad HaKlita guide |

## Should cover (advanced)

| Item | Where | Source |
|---|---|---|
| Phones (5, NBN only) and MoC approval above 5 | Step 2 | NBN |
| Carpet 25% of home area (NBN only), fitted carpet risk | Step 2, script | NBN + Tax Authority exclusion |
| AC / fans / heaters relative to rooms; Israeli-made AC VAT-free purchase (2 units or 1 mini-central) | Step 2 | NBN + Tax Authority |
| Permit-path authorities (drones MoC, weapons, transport items, laser); cannabis never importable | allowed-items-list.md, Step 2 | Tax Authority olim guide, NBN |
| Courier pays duty = usually no refund; cash over NIS 50,000 declared | Step 2 | NBN |
| Customs file opens automatically; manual opening documents | Step 1 | Tax Authority olim guide |
| A/1 temporary-resident concessions not repeatable | Step 1 | Misrad HaKlita guide |

## Out of scope (explicit)

| Item | Rationale (reviewed 2026-10-29) |
|---|---|
| Vehicle tax computation, licence conditions, early-sale tax | A user will ask, so the skill answers with the separate-track facts (3 years, 4-year personal use, one car per couple, 50% customs plus VAT) and routes to the "taxes on a vehicle" chapter of the Tax Authority olim guide. No olim vehicle skill exists in the catalog; `israeli-returning-resident-customs-vehicle` is for returning residents only. |
| Duty amounts on over-limit items | Tariff-dependent and item-specific; not capturable as a stable rule. Route to a broker quote. |
| Returning-resident full planning, Toshav Chozer Vatik tax status | Different track; routed to `israeli-returning-resident-navigator` and `israeli-toshav-chozer-vatik-tax-planner`. |
| Medication import quantities | Health-ministry rules; only the permit path is flagged. NBN describes plane/mail limits but this is not a customs-shipment question. |
| Dangerous-dog breed list | Changes by ministry notice; the skill routes to the Ministry of Agriculture page rather than freezing a list. |

## Authoritative sources

- https://www.gov.il/he/pages/guide-for-immigrants-and-foreign-residents
- https://www.gov.il/he/Departments/Guides/customs-guide-for-returning-residents
- https://www.gov.il/he/service/import_pets_cats_dogs
- https://www.gov.il/BlobFolder/generalpage/information_olim_tuota/he/guide-for-the-new-immigrant-en.pdf
- https://www.nbn.org.il/life-in-israel/government-services/rights-and-benefits/understanding-customs-benefits/
