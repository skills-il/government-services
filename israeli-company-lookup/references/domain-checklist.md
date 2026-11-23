# Domain coverage checklist: israeli-company-lookup

Scope: looking up an Israeli registered entity, reading its registrar status, and understanding
Israeli business entity types.

## Must cover (core)

| Item | Why it is core | Covered? |
|---|---|---|
| Companies Registrar (Rasham HaChevarot / ICA) public search entry point | The single canonical free lookup surface for Ltd companies | Yes, Step 2 |
| A programmatic lookup path that an agent can actually execute | The skill is named "lookup"; the ICA web UI cannot be driven by an agent. The Ministry of Justice publishes the full registrar dump as an open CKAN datastore on data.gov.il | Yes, Step 2b (added v1.3.0) |
| All status values, breach flag, sub-status and recent events, with unknown values shown raw | "Active" alone is not a clean result | Yes, Step 2b |
| Identity, bank-account and signing-authority check before paying | A real company number can be quoted by anyone | Yes, Step 2c |
| Number prefix as a first guess at the register | Choosing the wrong register returns a false "not found" | Yes, Step 2b |
| An individual dealer is not in the companies register | A miss on a dealer number proves nothing | Yes, Gotchas |
| Amutot are in a separate register; a CHL"Tz is a company | Searching the wrong register returns a false "not found" | Yes, Gotchas + Troubleshooting |
| Partnerships are in Rasham HaShutfuyot, not the companies registrar | Partnerships Ordinance registry is separate | Yes, Step 2 |
| Entity-type description by liability and registration | Users need to understand the differences; the skill does not pick one | Yes, Step 3 |
| Osek patur is not decided by turnover alone | VAT Registration Regulations r.13 and VAT Regulations r.6א | Yes, Step 3 |
| Registration fee, online vs paper, current year | Fees change annually and the online discount is material | Yes, 2,559 / 3,123 NIS (2026) |
| Annual registrar fee, reduced vs full band | Unpaid fees are one ground for the separate `מפרה` marking | Yes, references/entity-types.md |
| Insolvency Commissioner replaced the Official Receiver; the Administrator General is separate | Searching the wrong docket returns a false clean result | Yes, Gotchas |

## Should cover (advanced)

| Item | Why | Covered? |
|---|---|---|
| Reshumot / Yalkut HaPirsumim for liquidation and creditor notices | Registrar status lags the gazette | Yes, Reference Links |
| NBCTF terror-designation list | A public list a user can check before dealing with a counterparty | Yes, Reference Links |
| ISA and Capital Market Authority licensed-entity registries | Confirms a financial counterparty is licensed, which the companies registrar cannot tell you | Yes, Reference Links |
| Maya (TASE) disclosures as the only public ownership surface for listed companies | Public source for listed-company ownership disclosures | Yes, Troubleshooting |
| Last-filed annual report year as a staleness signal | Exposed by the open dataset; a company whose last report is years old deserves a question | Yes, Step 2b (added v1.3.0) |

## Out of scope (explicit)

- **Credit scoring and financial-strength ratings** (BDI/CofaceBdi, Dun & Bradstreet Israel).
  Commercial, paid, and licence-restricted; the registrar publishes no credit data.
  Re-litigated 2026-08-18: an ordinary user may ask, and the honest answer is that this is a
  paid commercial product, which the skill states rather than implying the registrar covers it.
- **Litigation history against a company.** Net HaMishpat search is not a public bulk surface and
  case-level access is restricted. Re-litigated 2026-08-18: still not capturable.
- **Foreign corporate registries.** Explicit anti-trigger in the description.
- **Stock analysis / valuation of a listed company.** Explicit anti-trigger; company-valuation
  is a separate skill.
- **Filing an incorporation on the user's behalf.** The skill explains the procedure; it does not
  transact.

## Authoritative sources

- Israel Corporations Authority (ICA / Rashut HaTagidim): https://ica.justice.gov.il
- Registrar open dataset (CKAN): https://data.gov.il/api/3/action/package_show?id=ica_companies
- Companies Law 1999 and Income Tax Ordinance: https://www.nevo.co.il
- GuideStar (amutot, CHL"Tz): https://www.guidestar.org.il
- Annual fee schedule: https://www.gov.il/he/service/company_partnership_annual_payment
