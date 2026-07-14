# Domain Coverage Checklist, israeli-discharged-soldier-navigator

Generated: 2026-05-18 via research on hachvana.mod.gov.il, kolzchut.org.il, nevo.co.il, hilan.co.il, he.wikipedia.org.

## Must cover (core)

- [x] **Pikadon eligibility rules**, IDF / MAGAV / Police / SHABAS / SLE, minimum 12 months (less if medical / training injury), source: kolzchut Pikadon page, why core: most common first question; SLE / under-12-months edge cases mislead users
- [x] **Pikadon monthly amount per service type (May 2026)**, lochem 990.63, tomech lechima 825.52, orfi 660.42, SLE 660.42, intermediate civilian track 495.38, split civilian track 330.25 NIS/month, AND the training reclassification (a combat soldier's first 4 training months accrue at the combat-support rate; a combat-support soldier's first 2 accrue at the "other" rate). Grant rates per month: 684.99 / 570.42 / 455.84 / 342.50 / 227.92, source: hachvana DepositUpTo5 page, why core: the "kama magia li?" answer; tier multipliers needed for sanity-check; instruct user to verify via official calculator since rates change monthly with index
- [x] **Pikadon 14-day availability rule (IDF) vs 30-day (SLE)**, source: kolzchut Pikadon page + hachvana, why core: distinct from 60-day grant timeline; users confuse the windows
- [x] **6 permitted pre-5y withdrawal purposes (exact Hebrew list)**, לימודים אקדמיים, הכשרה מקצועית, לימודי נהיגה, פתיחת/השקעה בעסק, נישואין, רכישת דירה/בית/קרקע. **Rental NOT included.**, source: hachvana GrantAndDeposit + DepositUpTo5, why core: most common user mistake is assuming rent qualifies; closed statutory list per Chok Klitat Chayalim Meshuchrarim
- [x] **5-year auto-transfer rule**, at end of 5 years remaining balance auto-transfers to bank for any purpose, source: kolzchut Pikadon page, why core: the "I forgot about my Pikadon" recovery flow
- [x] **Discharge grant (manak shichrur)**, separate from Pikadon, 20-60 days from end of service, unrestricted use, source: hachvana GrantAndDeposit + kolzchut grant page, why core: users confuse this with Pikadon; the grant is separate and unrestricted
- [x] **Tax exemption (Pikadon and grant)**, Section 9(27) Pkudat Mas Hachnasa, source: kolzchut, why core: prevents users panicking about tax on withdrawal
- [x] **Tax credit points (nekudot zikui), Section 39a, NOT 11**, 36 months from month after discharge, 2 points/year for ≥23 months (male) or ≥22 months (female), 1 point/year for 12-22 months. 2026 value: 242 NIS/month per point. Total benefit: ₪8,712 or ₪17,424, source: kolzchut nekudot zikui page, why core: single largest year-1 tax saving; service-length table routinely misquoted
- [x] **How to claim nekudot zikui (Tofes 101 + Tofes 135 retroactive)**, source: kolzchut nekudot zikui page, why core: unclaimed benefit = lost money
- [x] **Iron Swords full-tuition combat-soldier law**, Knesset legislation passed late 2023 covering 100% annual tuition for combat soldiers discharged from Oct 2023 onward, usable up to 5 years post-discharge, source: Times of Israel + hachvana IronSwords page, why core: most valuable post-discharge benefit for a typical 21-year-old planning university
- [x] **MY VISIT app / personal area at hachvana.mod.gov.il**, single login for balance, withdrawals, bank account updates, career-counselor scheduling, source: hachvana, why core: no manual/paper flow for most actions
- [x] **Required documents**, Teudat Shichrur, Teudat Zehut, Israeli bank account; purpose-specific evidence for withdrawals, source: hachvana, why core: missing Teudat Shichrur blocks every benefit
- [x] **Service-type cap: 32 months male / 24 months female**, source: hilan Chapter ג summary, why core: extra unpaid service does not accrue Pikadon
- [x] **Pikadon non-transferable / non-pledgeable / non-seizable**, source: hilan Chapter ג, why core: cannot be used as loan collateral

## Should cover (advanced / edge cases)

- [x] **SLE parity vs IDF**, same 12-month threshold, SLE gets the regular (acher) tier rate, 30-day rule (not 14), source: hachvana
- [x] **Service-type classification on Teudat Shichrur**, mention that combat-support vs combat classification drives the multiplier; appeal exists via Mador Iturim
- [x] **Pikadon for rishyon nehiga**, permitted; need driving school receipts
- [x] **Pikadon for opening a business**, needs Osek Patur/Murshe registration; defer to israeli-freelancer-ops for the Osek setup
- [x] **Pikadon for apartment purchase**, permitted for purchase only, NOT rental; flag mashkanta interaction (defer to israeli-mortgage-comparator)
- [x] **Pikadon for marriage**, evidence: Teudat Nisuin or wedding hall receipts
- [x] **Withdrawal for academic studies abroad**, eligible if institution recognized by Mishrad HaChinuch/GHIL
- [x] **Tofes 135 retroactive refund up to 6 years back**, if employer failed to apply credit points
- [x] **Pikadon inheritance on death in service**, refer to Mador Mishpachot Shakulot
- [ ] **Mimadim LiLimudim extended-window rules**, separate from the Pikadon 5-year window. Verify the current eligibility extension rules (mehina / GED / psychometric completion) on hachvana before quoting durations.
- [x] **Adjacent benefits (mention-and-link)**: Bituach Leumi + health exemption window, free public transport window, arnona discount, year-1 dmei avtala for discharged soldiers, Bahatzda discount card. Exact durations and thresholds change, surface as routes to the specialist skills (`israeli-bituach-leumi`, `israeli-unemployment-benefits-navigator`) and to the relevant municipal/transit operator rather than asserting specific magnitudes here.

## Out of scope (explicit, with rationale)

- Reservist (miluim) compensation → `israeli-miluim-manager`
- Lone soldier (chayal boded) post-discharge specific package → `israeli-lone-soldier-rights` (to be created)
- Academic scholarships beyond Mimadim (PEREACH, Adams, Rothschild, Rashi) → `israeli-academic-scholarships`
- Vocational course catalog matching → potential future skill
- PTSD / Aka 8944 disability recognition → `israeli-miluim-manager` + `israeli-mental-health-navigator`
- Mortgage benefits / Misrad HaShikun discount → `israeli-mortgage-comparator` + `israeli-real-estate`
- General Bituach Leumi benefits → `israeli-bituach-leumi`
- Pension funds, keren hishtalmut → `israeli-pension-advisor`
- Voluntary tax refund flow for salaried employees (Tofes 135 broader use) → `israeli-employee-tax-refund`

## Authoritative sources

- https://www.hachvana.mod.gov.il/Pages/default.aspx, MoD Department for Discharged Soldiers homepage; verify channels and service map
- https://www.hachvana.mod.gov.il/GrantAndDeposit/Pages/default.aspx, Grant + Deposit hub; verify 6-purpose list and 60-day grant timeline
- https://www.hachvana.mod.gov.il/GrantAndDeposit/DepositUpTo5/Pages/default.aspx, Pikadon pre-5y page; verify current per-tier monthly NIS amounts (change monthly with CPI)
- https://www.hachvana.mod.gov.il/IronSwords/Pages/sword.aspx, Iron Swords wartime benefits hub; verify which expansions remain in force
- Kol Zchut: search "פיקדון אישי לחיילים משוחררים", Pikadon page (6-purpose canonical list, SLE 30-day rule, medical-early-discharge exception)
- Kol Zchut: search "נקודות זיכוי ממס הכנסה לחיילים משוחררים", nekudot zikui (36-month duration, service-length point table, Section 39a, Tofes 101 + Tofes 135 process)
- Kol Zchut: search "מענק שחרור לחיילים משוחררים", discharge grant (20-60 day window)
- https://www.nevo.co.il/law_html/law01/150_023.htm, Chok Klitat Chayalim Meshuchrarim full text; statutory base
- hilan.co.il legislation center "חוק קליטת חיילים משוחררים פרק ג פקדון ומענק", Chapter ג summary (sections 8-11); verify caps and non-transferable clause
- https://he.wikipedia.org/wiki/חוק_ממדים_ללימודים, Wikipedia Hebrew article on Chok Mimadim LiLimudim; Tikkun 25 Dec 2023 raised coverage to 100% and extended window 3y→5y
- https://www.kolzchut.org.il/he/החזר_מס_הכנסה, Kol Zchut Tofes 135 process for retroactive employee tax refunds (6-year window, 4% interest)
