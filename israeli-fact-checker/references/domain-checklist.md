# Domain Coverage Checklist - israeli-fact-checker

Generated: 2026-06-04 via research on: The Whistle / המשרוקית (globes.co.il methodology), Meta Transparency Center Hebrew fact-checker content ratings, IFCN Code of Principles (Poynter), FakeReporter, CBS (cbs.gov.il), Bank of Israel (boi.org.il), Knesset OData, Central Elections Committee (data.gov.il), Nadlan (nadlan.gov.il), Ministry of Justice Corporations Authority, Bituach Leumi, Israel Police crime data, PIBA, Ministry of Health, OECD PISA, and data.gov.il CKAN.

## Israeli fact-check verdict scale (real terms)

The Whistle (המשרוקית), an Israeli IFCN signatory, uses a 5-point scale. This is the canonical scale for the skill (IFCN verification issued 23 Jan 2025, valid to 23 Jan 2027; re-check after that date). Meta's Hebrew fact-checker rating set is a parallel reference because viral WhatsApp/X content is what users most often submit, and those labels are what platforms attach. The Whistle left Meta's programme in December 2020, so the Meta labels are Meta's, not The Whistle's. Meta replaced third-party fact-checking with Community Notes in the US; its Community Notes page (updated September 2026) lists only the US and a Latin American test, so Israel still sees third-party labels. Re-check each cycle.

| Hebrew term | Gloss | Which desk | Source |
|---|---|---|---|
| נכון | Correct / True (true in its near-entirety) | The Whistle | globes.co.il methodology |
| לא מדויק | Inaccurate (substantial parts wrong) | The Whistle | globes.co.il methodology |
| מטעה | Misleading (false impression / out of context) | The Whistle | globes.co.il methodology |
| לא נכון | Not correct / False | The Whistle | globes.co.il methodology |
| לשיפוטכם | For your judgment (too complex for a definitive score) | The Whistle | globes.co.il methodology |
| אין מספיק נתונים | Insufficient data (anti-fabrication fallback) | skill convention, aligned to IFCN | ifcncodeofprinciples.poynter.org |

Parallel reference (platform labels on viral content): לא נכון, עבר שינוי, לא נכון חלקית, חסר הקשר, סאטירה, נכון (Meta Hebrew ratings).

Rule for the skill: use נכון / לא מדויק / מטעה / לא נכון / לשיפוטכם as the primary scale and reserve אין מספיק נתונים for the anti-fabrication path. Do NOT invent an אמת/שקר pair or a calqued "חצי אמת".

## Standard fact-check workflow

1. Isolate the checkable claim. Strip opinion, rhetoric, prediction; decompose compound statements into atomic assertions. Source: globes.co.il methodology.
2. Distinguish fact from opinion from prediction. Only empirically checkable assertions get a verdict. Source: ifcncodeofprinciples.poynter.org.
3. Primary-source rule. Use reliable, named sources; prefer the originating official dataset over a news summary. Source: globes.co.il methodology.
4. Recover the original context. Establish what was actually said, in what setting, against which baseline. Out-of-context numbers are the most common cause of a מטעה verdict. Source: globes.co.il methodology.
5. Date the data. Pin every figure to a reference period and publication date; note nominal vs real, monthly vs annual. Source: Meta transparency center.
6. Non-partisanship. Same standard regardless of speaker identity. Source: ifcncodeofprinciples.poynter.org.
7. One verdict label per claim with a full citation trail.
8. Anti-fabrication gate (hard rule). If no authoritative source confirms a number, the verdict is אין מספיק נתונים. Never synthesize a figure.

## Must cover (core)

- [ ] Verdict scale + anti-fabrication rule - The Whistle 5-point scale + IFCN methodology - source: globes.co.il methodology - why core: without a defined Hebrew verdict vocabulary and a "cannot be verified" fallback the skill gives unlabeled or fabricated answers - pitfalls: do not invent a retired 10-point scale; never default to a fabricated number instead of אין מספיק נתונים.
- [ ] Inflation / cost of living / CPI / specific price changes - CBS [MCP: israel-statistics / israeli-cbs] - source: cbs.gov.il price indices - why core: the most common viral/political claim type and the only authoritative CPI - pitfalls: indices publish monthly; distinguish nominal vs real, MoM vs YoY, and base year/basket.
- [ ] State budget / ministry spending / procurement / support payments - BudgetKey / OpenBudget [MCP: budgetkey, il-budget] - source: obudget.org - why core: "the government spent X on Y" needs executed-vs-planned data - pitfalls: distinguish planned (תקציב מקורי) vs executed (ביצוע); procurement coverage starts in recent years only, so verify the data exists for the period claimed.
- [ ] Exchange rates / shekel value - Bank of Israel representative rate [MCP: boi-exchange] - source: boi.org.il exchange rates - why core: "the shekel weakened to X" is settled only by the daily representative rate (שער יציג) - pitfalls: use שער יציג, not market spot; pick the correct dated rate.
- [ ] Legislation / bills / committee activity - Knesset OData [MCP: knesset] - source: knesset.gov.il/Odata - why core: "MK X proposed / the Knesset passed" needs bill status - pitfalls: per-MK voting records are NOT in the ParliamentInfo OData; use Knesset OData V4 (knesset.gov.il/OdataV4/ParliamentInfo/, KNS_PlenumVote + KNS_PlenumVoteResult), not the Central Elections Committee, before asserting how an MK voted. The data.gov.il package 'vote' (הצבעות חברי הכנסת במליאה) has zero data files as of 2026-10-01 and is not a source.
- [ ] Election results / turnout / party seats - Central Elections Committee + data.gov.il [MCP: israel-elections] - source: data.gov.il elections dataset - why core: seats and turnout are high-frequency claims with one authoritative source - pitfalls: use official final results, not exit polls; turnout denominator is eligible voters.
- [ ] Housing prices / real-estate transactions - CBS housing index + Nadlan deals [MCP: nadlan] - source: nadlan.gov.il - why core: "apartment prices rose X%" needs recorded transaction prices, not asking prices - pitfalls: Nadlan has reporting lag; for the national trend use the CBS House Price Index, not an aggregation of deals.
- [ ] Non-profit finances / foreign-state-entity support / amuta status - Ministry of Justice Corporations Authority, GuideStar (guidestar.org.il) - why core: "amuta X is foreign-funded" is a recurring claim - pitfalls: the MoJ amutot dataset on data.gov.il has a separate file of donations from a foreign STATE entity (תרומות מישות מדינית זרה); it says nothing about private foreign donors; absence of a report is not proof of no funding; party and candidate funding is the State Comptroller's regime.
- [ ] Unemployment / labor force - CBS labour-force survey - source: cbs.gov.il - why core: "unemployment is X%" is defined by the CBS survey - pitfalls: CBS survey unemployment differs from Sherut HaTaasuka registered job-seekers; do not conflate.
- [ ] Wages / average wage - CBS + Bituach Leumi - source: btl.gov.il average wage - why core: "the average wage is X" anchors cost-of-living and benefit claims - pitfalls: statutory "שכר ממוצע במשק" differs from the CBS average monthly wage; check the CBS definition (per person or per job, average or median) and cite the reference period.
- [ ] General government datasets (catch-all) - data.gov.il CKAN - source: data.gov.il - why core: many claims map to a ministry dataset with no dedicated MCP; CKAN search is the universal fallback router - pitfalls: dataset freshness varies; always read the resource last-updated metadata.

## Should cover (advanced / edge cases)

- [ ] Crime statistics - Israel Police + CBS (search data.gov.il for the Israel Police crime dataset) - why advanced: published crime data covers only selected offense categories, so verify the period and category exist - pitfalls: reported-crime counts are not victimization rates.
- [ ] Health / hospital / mortality / vaccination - Ministry of Health - why advanced: claims need careful denominators (per-capita, age-standardized) - pitfalls: crude vs age-adjusted mortality.
- [ ] Demographics / population / immigration - CBS + PIBA - why advanced: figures split between CBS population estimates and PIBA entry/status reports - pitfalls: PIBA counts legal status and entries, CBS counts resident population, aliyah sits with CBS/Jewish Agency; do not merge.
- [ ] Vehicles / road safety - Ministry of Transport + data.gov.il [MCP: israel-vehicles] - why advanced: registry and accident data are separate datasets - pitfalls: road-fatality counts vary by definition (30-day vs scene) and source.
- [ ] Education / Bagrut / PISA - Ministry of Education + OECD - why advanced: international comparisons need the OECD PISA primary tables - pitfalls: PISA is triennial, so check which cycle is the latest and do not cite an old cycle as current.
- [ ] Company facts / ownership - Registrar of Companies - why advanced: free basic info, paid full extract (נסח חברה) - pitfalls: beneficial ownership is not fully public.
- [ ] Screenshot / image / video provenance (SKILL.md Step 3a) - prior checks (Google Fact Check Explorer, The Whistle archive, irrelevant.org.il for chain letters, FakeReporter for networks), original post, Wayback Machine + archive.today, reverse-image search on keyframes (Google Lens, TinEye, Yandex, Bing Visual Search; InVID-WeVerify plugin for keyframes) - why core: a screenshot of a minister's post is the most common viral political artifact and attribution must be settled before the figure - pitfalls: no original and no capture means אין מספיק נתונים, not לא נכון; recycled or cut real footage is חסר הקשר, not עבר שינוי; an AI-detector score is not a verdict.
- [ ] Interest rate, poverty, State Comptroller findings - BoI monetary policy announcements, BTL poverty report, mevaker.gov.il - why advanced: frequent political claims that otherwise fall to the data.gov.il catch-all - pitfalls: provisional vs revised; persons vs families.
- [ ] Rent, opinion polls, local elections - CBS CPI rent component; the original poll publication; the Ministry of Interior local-elections data - pitfalls: Nadlan and the House Price Index cover purchases, not rent; a poll is never rated against official data.
- [ ] GDP, deficit, national debt - NOT YET MAPPED (2026-10-01): the Accountant General pages on gov.il were Cloudflare-blocked and no official deep link could be verified, so the skill routes these to the official publisher's own release by hand, never a news summary.
- [ ] CPI across a base change - CBS index calculator (api.cbs.gov.il) - pitfalls: never subtract raw index points across a rebase; state the index-month convention (known index vs index for the month).
- [ ] Defense / security budget caveats - BudgetKey + Knesset committee - why advanced: large parts are classified or off-book - pitfalls: label a confirmed published number as partial rather than implying completeness.

## Out of scope (explicit, with rationale)

- Verifying private individuals' undisclosed personal facts (income, health, relationships) - privacy; no authoritative public source and checking would breach Israel's Privacy Protection Law.
- Opinions, value judgments, rhetoric - not empirically checkable; flag as opinion, no verdict.
- Predictions and forecasts - unfalsifiable at check time; present the baseline data but no true/false verdict.
- Religious, theological, or ideological truth claims - not adjudicable against an official dataset.
- Real-time breaking-news casualty/event counts during an active incident - figures change hourly and official confirmation lags; defer to official spokesunits and date everything.
- Classified or non-published government figures - no authoritative open source; return אין מספיק נתונים.
- Foreign (non-Israeli) claims with no Israeli data anchor - outside the source map; route to a general fact-checker.
- Forensic attribution of synthetic media (which model, who made it) - needs forensic tooling the skill does not have; the skill settles provenance with honest uncertainty instead (re-litigated 2026-10-01: users do ask "is this a deepfake", and Step 3a now answers that with the provenance path rather than silence).

## Authoritative sources

- globes.co.il The Whistle methodology - the 5-label Hebrew verdict scale + editorial process.
- transparency.meta.com he-il content ratings - Hebrew platform rating labels for viral content.
- ifcncodeofprinciples.poynter.org - IFCN commitments (non-partisanship, source + methodology transparency).
- fakereporter.net - provenance / coordinated-network / deepfake exposure history.
- cbs.gov.il - CPI, price indices, labour force, demographics, housing index.
- boi.org.il exchange rates - shekel representative rate (שער יציג).
- obudget.org / budgetkey - state budget, support payments, procurement.
- knesset.gov.il/Odata - bills, committees, MK profiles (no per-MK votes).
- knesset.gov.il/OdataV4/ParliamentInfo - KNS_PlenumVote, KNS_PlenumVoteResult (per-MK plenum votes).
- data.gov.il elections dataset - official results, seats, turnout.
- nadlan.gov.il - recorded real-estate transaction prices.
- guidestar.org.il (Ministry of Justice) - registered amutot, filings, foreign-state-entity support disclosures.
- toolbox.google.com/factcheck/explorer, web.archive.org, archive.ph, tineye.com - prior checks, captures, reverse-image search.
- btl.gov.il - statutory average wage (National Insurance Law ss.1-2).
- data.gov.il - CKAN catch-all router for any ministry dataset.
