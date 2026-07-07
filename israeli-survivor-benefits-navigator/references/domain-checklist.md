# Domain-completeness checklist: Israeli survivor benefits

Built from an aggregator sweep of the Bituach Leumi "שאירים" (Survivors' Insurance) section
index and the Kol-Zchut survivors hub "שאירים (אלמנות, יתמות ושכול)", then verified against
btl.gov.il, kolzchut.org.il and pension/insurance sources. Every named benefit or status
became a row below.

Sources swept:
- Bituach Leumi survivors index (btl.gov.il, Survivors_ Insurance section)
- Bituach Leumi survivor-allowance amounts index (btl.gov.il, shiuraihakizba)
- Kol-Zchut survivors hub (search Kol-Zchut for the "שאירים (אלמנות, יתמות ושכול)" page)
- Bituach Leumi work-injury family-rights pages (btl.gov.il, Work_Injury section)

## Must cover (core death-triggered benefits + the computable rate sub-dimensions)

### Bituach Leumi survivor's allowance (קצבת שאירים), rate-table sub-dimensions
Because this skill computes an amount, each categorical row of the rate table is its own must-cover item:
- [x] Who is a "שאיר" (she'er): widow/widower definition (married or common-law incl. same-sex; 1 year cohabitation, or 6 months if 55+, or a shared child waives the duration), orphan age cutoffs (18; 20 in secondary school / pre-military mechina; 21 in national/community service), plus the 4 eligibility conditions (insured, akhshara period, counted as she'er, no arrears)
- [x] Qualifying (akhshara) period test: 12 months before death, or 24 months in the last 5 years, or 60 in 10 years, or 144 total, or the resident-ratio route; plus the no-akhshara cases (new resident within a year, before age 19, primary breadwinner, woman within a year of divorce/widowhood)
- [x] 12-month filing deadline; late filing caps retroactive payment at 12 months
- [x] Widow(er) aged 40-50 without children, rate row
- [x] Widow(er) aged 50+ without children, rate row
- [x] Widow(er) aged 80+, rate row
- [x] Widow(er) with one child, rate row
- [x] Widow(er) with two children, rate row
- [x] Each additional child increment (no cap on number of children), rate row
- [x] Old-age (vatik) pension interaction: old-age paid in full PLUS half the survivor's allowance (919 = half the childless-50+ base; half the higher rate when there are children), rate row
- [x] Per-orphan amounts (parent not entitled; single vs multiple), rate rows
- [x] Orphan of both parents, rate row
- [x] Seniority increment (תוספת ותק): 2% per insurance year, max 50%, increment dimension
- [x] Income test for widower: 7,848 NIS ceiling, 2,093 NIS deduction, income-test threshold dimension
- [x] Combined family maximum note (allowance folds child portions into the "with children" rows; no explicit family cap on child count)

### Other death-triggered benefits
- [x] Death grant (מענק פטירה), one-time 10,514 NIS, automatic, covered by form 410
- [x] Survivor grant (מענק שאירים), one-time = 36 monthly allowances, widow(er) under 40 no children / income cases
- [x] Special survivors' allowance (גמלת שאירים מיוחדת), non-insured olim, form 4506
- [x] Income supplement (תוספת השלמת הכנסה), form 430
- [x] Orphan living allowance (דמי מחיה ליתומים), form 2910
- [x] Burial fees (דמי קבורה), paid direct to Chevra Kadisha; basic burial free
- [x] Dependents' allowance (קצבת תלויים), work-related death track; % of full work-disability pension; distinct from survivor's allowance; cannot receive both
- [x] Pension-fund survivor pension (פנסיית שאירים), ~60% spouse, ~40% orphans <21, fund-specific per takanon
- [x] Provident fund / life insurance beneficiary (מוטב) claims, section 147: beneficiary designation overrides the will
- [x] Widow(er) already on old-age pension: old-age paid in full plus half the survivor's allowance (delivered in Step 3 + gotchas)
- [x] Under-40 childless survivor exception: usually a one-time grant, but a monthly allowance if pregnant with / bearing the deceased's child, or (work-injury track) unable to support herself from work (delivered in Step 3)

## Should cover (adjacent, mention + route)
- [x] Study grant for single-parent families (מענק לימודים), mention, not central
- [x] Bar/bat mitzvah grant (מענק בר-מצווה), mention
- [x] Marriage grant on remarriage (מענק נישואים): delivered in full (Step 5 + form 408 row), not just mentioned; remarriage ends the allowance, grant = 36 allowances in two installments, with continuation/reinstatement rules
- [x] Vocational training + living allowance for widow(er)s (הכשרה מקצועית ודמי מחיה לאלמנים ואלמנות), mention
- [x] Municipal arnona discount and local-authority help, mention, route to municipality
- [x] Employment rights: mourning leave (ימי אבל), severance to survivors (פיצויי פיטורים לשאירים), mention
- [ ] "חיסכון לכל ילד" residual withdrawal / residual old-age payment: NOT delivered in the body (out of this skill's core scope); route the family to the general Bituach Leumi navigator if it comes up

## Out of scope (route elsewhere)
- Operational after-death tasks (death certificate, burial logistics, closing accounts, notifying institutions, asset transfer) → `israeli-estate-settlement-navigator`
- Writing a will / obtaining succession (ירושה) or probate (קיום צוואה) orders → `israeli-wills-inheritance`
- General ongoing Bituach Leumi navigation unrelated to death → `israeli-bituach-leumi`
- Pension planning while alive (accumulation, fund selection) → `israeli-pension-advisor`
- IDF / terror-victim bereavement (Ministry of Defense / משפחות שכולות of security forces), different institution, not covered

## Notes on verification method
- All NIS amounts and the rate tables were rendered live from btl.gov.il with the Playwright MCP
  (browser_navigate + browser_evaluate on the page's main text), because WebFetch mangles the
  multi-table gov.il pages. Effective date on every current figure: 01.01.2026.
- Pension-fund percentages (60% / 40%) are typical for the new comprehensive funds and are
  fund-specific; flagged medium confidence and always deferred to the fund's takanon.
