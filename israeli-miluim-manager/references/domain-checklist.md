# Domain checklist: israeli-miluim-manager

Anchor for Expert Review (update-skill Phase 5.8). Bootstrapped 2026-09-25 from the 3.0 aggregator sweep (Kol Zchut reservist pages, read in a browser), the 3b.5 coverage audit, and the primary sources listed at the end. Each row names the evidence.json claim that backs it, or the reference file section that carries it.

## Must cover (core)

| # | Topic | Every category the answer varies by | Where / evidence |
|---|-------|-------------------------------------|------------------|
| 1 | Who pays what: the BTL tagmul vs the three IDF payments | Payer (BTL / IDF / Tax Authority / MoD); the right hotline for each | SKILL.md Step 3; `tagmul-nosaf-idf`, `tagmul-paid-by-idf` |
| 2 | BTL daily basis | Monthly, daily and hourly employee; self-employed; not working or student; stopped work within vs after 60 days; left keva within 60 days; on unemployment benefit; wage basis below the floor; working youth (114.73 minimum); under 60 days worked (best 3 of 6 months); several employers; employee who is also self-employed | btl-payment-rules.md section 1; `bl-min-daily-2026`, `bl-max-daily-2026` |
| 3 | BTL 40% supplement | Remainder of service days / 7: 0 to 6 | btl-payment-rules.md section 2 |
| 4 | Self-employed 25% compensation and the combined cap | Self-employed vs not | SKILL.md Step 3 |
| 5 | Amendment 253 repeat-service basis | Gap between services under or over 60 days | bituach-leumi-filing-guide.md; `amendment-253-date` |
| 6 | Tagmul Meyuchad, two layers | Days 32-60 (133.33) vs beyond 60; SERVICE YEAR (2024 flat 133, 2025 by array 133.33/60/40, 2026 by activity tier 133/113/86/60/40/30); order type (צו 8 only before 2026); over-age reservists from day 1; commanders | 2026-law-changes.md; `tagmul-meyuchad-base-32-60`, `tagmul-meyuchad-2025-bands`, `tagmul-meyuchad-61` |
| 7 | Tagmul Nosaf | Day bands; payment by 1 May of the following year; 25% special tax; no credit points | 2026-law-changes.md; `tagmul-nosaf-25pct-tax` |
| 8 | Over-age tagmul | Enlisted 40+ / officers 45+ by role; אל"ם and above excluded | `tagmul-moharegei-gil`, `moharegei-gil-eligibility` |
| 9 | s.39B combat tax credit | SERVICE year: 2024 or earlier none; 2025-2026 temporary 30-day table (15 rows); 2027 on permanent 20-day rule (14 rows to 85+); ishur lochem required; credited the tax year after; Form 101 route vs refund route vs annual return | 2026-law-changes.md; `s39b-temporary-2026-2027`, `s39b-permanent-20-days`, `s39b-commencement-2026`, `form-101-refund-routes` |
| 10 | Employment protection | During service + 30 days (s.41A(b), ועדת התעסוקה); days 31-60 (extension order, ועדת פיקוח, prospective from 29.04.2026); causal ban; spouse permanent ban and temporary 14-day window; notice-period exclusion; burden of proof; remedies | SKILL.md Step 2; `tzav-14498-*`, `s41a2-*` |
| 11 | 20% employer compensation | All employers except public ones | `permanent-20pct-nii-amendment` |
| 12 | Keren HaSiyua 2026 grants | Activity tier; day thresholds; child ages | 2026-law-changes.md; `manak-*`, `arnak-digitali`, `shover-nofesh` |
| 13 | Keren HaSiyua rules by service period | 2023-2025 service filed by 31.12.2026 under the 23.07.2025 regulations; 2026 service under the 2026 regulations; routine-order service under the new ones only | 2026-law-changes.md, transition table; `keren-transition-7b`, `keren-transition-routine-order` |
| 14 | Partner income loss | Service period (see 13); tier bands for 2026 service; 10+ consecutive days; child under 14 / 21; 2026: monthly and annual cap, taxable; 2023-2025 (previous regs): no tiers, 10,000/month cap raisable by the exceptions committee | `keren-partner-*` |
| 15 | Service injury and PTSD | MoD Agaf HaShikum (not BTL); 20% floor for off-duty injury; 8944 | `shikum-*`, `aka-8944-hotline` |
| 16 | Rejected BTL claim | 12 months to the Labour Court; ועדת תביעות does not pause the clock; legal aid scope | `btl-appeal-12-months`, `btl-legal-aid-397` |
| 17 | Self-employed indirect-damage grant | Window per eligibility period; 2026 track | 2026-law-changes.md; `nezek-akif-*` |
| 18 | Students | 50+ days window 23.10.2025-30.09.2026; tier bands | `student-tuition-bands` |
| 19 | Deadlines falling before the end of the current year | Keren, Manak Nezek Akif, student window, Form 101 | 2026-law-changes.md, deadline table |

## Should cover (advanced)

- Reserve exemption ages by role (temporary order 09.08.2024 to 30.06.2027). `miluim-age-thresholds`.
- Deferral and shortening of a call-up (ולת"ם, Form 58).
- Travel reimbursement. `travel-66-cap`.
- Accrued annual leave carry, spouse paid absence days.
- Commanders' grant, relocation, maternity-leave and camps grants.

## Out of scope (explicit)

- Regular (sadir) service, draft deferral, career (keva) pay and pension. The description excludes them. Refreshed 2026-09-25.
- Computing the self-employed indirect-damage grant amount: routed to `israeli-business-war-compensation`. Refreshed 2026-09-25.
- Bank of Israel relief figures: no current primary source publishes them. The skill routes the user to their bank. Re-litigated 2026-09-25: a user would ask for them, but they are still not capturable.

## Open (deferred to the next cycle, see optimization-log.json)

- The 5-9 day personal-expenses tagmul (Kol Zchut gives 266 per period; unverified). Needs a primary source.
- Pre-2026 grants still claimable until 31.12.2026 (family grant, 2025 combat and persistence grants, home repairs, flights, equipment).
- Arnona discount, mortgage supplement, company-car benefit relief, protection from attachment, IDF disability-income top-up, Form 58 family grounds, academic credit points.
- (Resolved 2026-09-26) The 23.07.2025 Keren regulations are now read and cited.

## Authoritative sources

- he.wikisource.org: Income Tax Ordinance s.39B; Reserve Service Law; Discharged Soldiers (Return to Work) Law; NI (claim deadlines) regulations.
- Tax Authority employer circular 2025-001368 of 16.12.2025 (s.39B).
- btl.gov.il Reserve_Service pages (rates, TagmulZacay, PizoyLmasik).
- miluim.idf.il 2026 policy page, and the Keren HaSiyua regulations PDF (current version 05.07.2026, with the Annex B transition provision).
- gov.il/he/service/grant-for-reservists.
- Kol Zchut reservist pages. These are secondary; they need a browser to read.
