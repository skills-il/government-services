# Domain coverage checklist: israeli-company-lookup

Scope: looking up an Israeli registered entity, reading its registrar status, and choosing
between Israeli business entity types.

## Must cover (core)

| Item | Why it is core | Covered? |
|---|---|---|
| Companies Registrar (Rasham HaChevarot / ICA) public search entry point | The single canonical free lookup surface for Ltd companies (Companies Law 1999, s.36) | Yes, Step 2 |
| A programmatic lookup path that an agent can actually execute | The skill is named "lookup"; the ICA web UI cannot be driven by an agent. The Ministry of Justice publishes the full registrar dump as an open CKAN datastore on data.gov.il | Yes, Step 2b (added v1.3.0) |
| The four registrar status values, including "mufrat hok" | A company in breach of law is the highest-frequency due-diligence red flag and is not the same as struck-off | Yes, Gotchas |
| Company-number formats by entity type (51-/55-/57-/58-) | Wrong prefix means searching the wrong registry entirely | Yes, references/entity-types.md |
| Company number is not the tax ID (mispar osek) | Agents routinely conflate the two | Yes, Gotchas |
| Amutot and CHL"Tz live on GuideStar, not the ICA company search | Ministry of Justice split the NPO portal; searching ICA returns nothing | Yes, Gotchas + Troubleshooting |
| Partnerships are in Rasham HaShutfuyot, not the companies registrar | Partnerships Ordinance registry is separate | Yes, Step 2 |
| Entity-type comparison on liability, tax, filing burden | The second half of user intent ("which entity should I open") | Yes, Step 3 |
| Corporate tax rate (Income Tax Ordinance s.126) | Drives the entity-type decision | Yes, 23% |
| Osek patur annual turnover ceiling, current year | Selecting osek patur above the ceiling is a VAT offence | Yes, scripts, 122,833 NIS (2026) |
| Registration fee, online vs paper, current year | Fees change annually and the online discount is material | Yes, 2,559 / 3,123 NIS (2026) |
| Annual registrar fee, reduced vs full band | Non-payment is what produces the "mufrat hok" status the skill teaches users to read | Yes, references/entity-types.md |
| Israel has no operational public UBO registry | Users arrive expecting a UK-Companies-House-style PSC register; promising one is a factual error | Yes, Gotchas + Troubleshooting |
| Insolvency Commissioner replaced Apotropos Klali for post-2019 cases | Searching the wrong docket returns a false clean result | Yes, Gotchas |

## Should cover (advanced)

| Item | Why | Covered? |
|---|---|---|
| Reshumot / Yalkut HaPirsumim for liquidation and creditor notices | Registrar status lags the gazette | Yes, Reference Links |
| NBCTF terror-designation list | Mandatory screening for Israeli counterparty due diligence under the Counter-Terrorism Law 2016 | Yes, Reference Links |
| ISA and Capital Market Authority licensed-entity registries | Confirms a financial counterparty is licensed, which the companies registrar cannot tell you | Yes, Reference Links |
| Maya (TASE) disclosures as the only public ownership surface for listed companies | Closest available substitute for UBO data | Yes, Troubleshooting |
| Last-filed annual report year as a staleness signal | Exposed by the open dataset; a company whose last report is years old is a red flag even before it is flagged mufrat hok | Yes, Step 2b (added v1.3.0) |

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
