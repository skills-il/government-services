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
- [x] Who is a "שאיר" (she'er): widow/widower definition (married or common-law incl. same-sex; 1 year cohabitation, or 6 months if 55+, or a shared child waives the duration), orphan age cutoffs, FULL official list (18; 20 for secondary school / bagrut / learning-disability framework; 20 for a pre-military mechina or kadatz-tratz; 20 for 20+ weekly hours in an institution approved by law; 21 for public-purpose volunteering with deferred draft; 24 for regular IDF service, 36 months; 24 for national service; 24 for atuda), corrected in v1.3.0 after the earlier three-row version understated the army and national-service cohorts, plus the 4 eligibility conditions (insured, akhshara period, counted as she'er, no arrears)
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
- [x] Income supplement (תוספת השלמת הכנסה), form 430 plus income declaration 412, WITH the full 3-age-band x 3-family-composition amount table (4,375 to 8,563), added v1.3.0
- [x] Separated widow: the four alternative conditions (separation under 36 months, cohabitation in the last year, maintenance paid or owed, an increment paid for her in his pension), added v1.3.0
- [x] Discretionary grant on equitable grounds (הענקה מטעמי צדק) when akhshara or contribution arrears fail, added v1.3.0
- [x] Dependents'-allowance sub-tables: orphans alone (60/80/90/100%) and other dependants (50/75/90/100%), plus the 60%-at-any-age unable-to-support-self rule and the pregnant-widow 60%-then-80% rule, added v1.3.0
- [x] Choice between the survivor's allowance and any OTHER National Insurance allowance that is not the old-age pension, with the children's carve-out and the revival rule, added v1.3.0
- [x] Rejection handling: 12 months to appeal to the regional labour court, 30 days to the national labour court, medical-committee route first, added v1.3.0
- [x] Special survivors' allowance for a late-immigrating uninsured deceased, delivered in Step 2 (not only in the form map), added v1.3.0
- [x] Cause-of-death triage in Step 1: ordinary vs work injury vs hostile act (Bituach Leumi, separate law and track) vs IDF service (Ministry of Defence) vs road accident (motor insurer, with Bituach Leumi payments deducted), added v1.3.0
- [x] Orphan living allowance (דמי מחיה ליתומים), form 2910
- [x] Burial fees (דמי קבורה), paid direct to Chevra Kadisha; basic burial free
- [x] Dependents' allowance (קצבת תלויים), work-related death track; % of full work-disability pension; distinct from survivor's allowance; cannot receive both
- [x] Pension-fund survivor pension (פנסיית שאירים): veteran Amitim split 60% spouse / 20% orphan / 40% orphan of both parents / 15% dependent parent, capped at 100%; fund-specific per takanon; plus the v1.3.0 risk-cover-lapse gate (confirm deposits were live before quoting any percentage)
- [x] Provident fund / life insurance beneficiary (מוטב) claims, section 147: beneficiary designation overrides the will
- [x] Widow(er) already on old-age pension: old-age paid in full plus half the survivor's allowance (delivered in Step 3 + gotchas)
- [x] Under-40 childless survivor exception: usually a one-time grant, but a monthly allowance if pregnant with / bearing the deceased's child, or (work-injury track) unable to support herself from work (delivered in Step 3)

## Should cover (adjacent, mention + route)
- [x] Annual study grant (מענק לימודים), delivered as an automatic payment in Step 5, v1.3.0
- [x] Bar/bat mitzvah grant (מענק בר-מצווה), 7,009 NIS, automatic, delivered in Step 5, v1.3.0 (was marked covered in v1.2.0 while the body never named it)
- [x] Marriage grant on remarriage (מענק נישואים): delivered in full (Step 5 + form 408 row), not just mentioned; remarriage ends the allowance, grant = 36 allowances in two installments, with continuation/reinstatement rules
- [x] Vocational rehabilitation + training living allowance for widow(er)s, delivered in Step 5 with the routing to the branch rehabilitation department, v1.3.0 (was marked covered in v1.2.0 while the body never named it)
- [x] Arnona discount: discretionary per authority (rate and capped area vary), never automatic, must be claimed with the entitlement letter, v1.3.0
- [x] Severance to survivors under section 5 of the Severance Pay Law, with its own she'er definition and the employer as payer, delivered in Step 6, v1.3.0; mourning leave still mention-only
- [x] Budgetary pension (פנסיה תקציבית) survivors track, delivered in Step 6, v1.3.0
- [x] Pension-fund risk cover can lapse when deposits stop (hesder risk), so ask whether the deceased was still depositing before quoting a percentage, v1.3.0
- [x] Insurance limitation period: section 31 of the Insurance Contract Law, 3 years, 5 for life/illness-hospitalisation/LTC contracts made or renewed from 25.11.2020, v1.3.0
- [ ] "חיסכון לכל ילד" residual withdrawal / residual old-age payment: NOT delivered in the body (out of this skill's core scope); route the family to the general Bituach Leumi navigator if it comes up

## Out of scope (route elsewhere)
- Operational after-death tasks (death certificate, burial logistics, closing accounts, notifying institutions, asset transfer) → `israeli-estate-settlement-navigator`
- Writing a will / obtaining succession (ירושה) or probate (קיום צוואה) orders → `israeli-wills-inheritance`
- General ongoing Bituach Leumi navigation unrelated to death → `israeli-bituach-leumi`
- Pension planning while alive (accumulation, fund selection) → `israeli-pension-advisor`
- Death of a serving soldier: Ministry of Defence rehabilitation department, different institution, not covered beyond the Step 1 routing line. NOTE: a civilian killed in a HOSTILE ACT is NOT in this out-of-scope row, that claim is paid by Bituach Leumi under the hostile-action compensation law, and Step 1 now routes it there instead of to form 410

## Notes on verification method
- All NIS amounts and the rate tables were rendered live from btl.gov.il with the Playwright MCP
  (browser_navigate + browser_evaluate on the page's main text), because WebFetch mangles the
  multi-table gov.il pages. Effective date on every current figure: 01.01.2026.
- Pension-fund percentages are the veteran Amitim published split and are
  fund-specific; flagged medium confidence and always deferred to the fund's takanon.


## Re-litigated out-of-scope rows (2026-08-18 cycle)
- "חיסכון לכל ילד" residual withdrawal: still out of scope for the residual-withdrawal mechanics, but an
  ordinary user WOULD ask what happens to the orphan's account, so the mainstream answer (the account
  continues and the surviving parent controls the track and the withdrawal decision) is a carried lesson
  for the next cycle rather than a silent omission.
- IDF/terror bereavement: partially re-opened this cycle, see the split above. This is the model case for
  why an out-of-scope row must be re-read: it bundled two different institutions into one exclusion.

## Deferred to the next cycle (logged in optimization-log.json)
- Encoding the income supplement and the dependents' sub-tables into scripts/estimate_survivor_allowance.py (both are surfaced as caveats today)
- Rules for a survivor living abroad (review after 3 months, annual life certificate)
- Clawback of allowances deposited to the deceased after the date of death, and transfer of child allowance
- Tax treatment: the Bituach Leumi allowance is exempt while a pension-fund survivors' pension is taxable
- Income-support allowance for an orphan child (קצבת הבטחת הכנסה לילד יתום)
