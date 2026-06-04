---
name: israeli-fact-checker
description: "Verify a public claim against official Israeli data and return a sourced verdict. Use when checking a politician's statement, a viral WhatsApp or X message, a news headline, or any factual claim about Israeli inflation, prices, the state budget, government spending, exchange rates, Knesset votes, election results, housing prices, wages, unemployment, crime, or NGO and foreign-donation funding. The skill isolates the checkable assertion, routes it to the right official source (CBS, Bank of Israel, BudgetKey, Knesset, data.gov.il), pulls the figure, and labels the claim נכון, לא מדויק, מטעה, לא נכון, or לשיפוטכם with a full citation trail, or אין מספיק נתונים when no source confirms it. This matters because a hallucinated number is worse than no answer. Hebrew triggers: בדיקת עובדות, אימות טענה, פייק ניוז, האם זה נכון. Do NOT use for opinions, predictions, private personal facts, or writing articles from scratch."
license: MIT
---

# Israeli Claim & Fact Verifier

## Problem

Public debate in Israel runs on numbers: a minister says spending on X doubled, a viral WhatsApp message claims prices jumped by a dramatic amount, a headline reports a record turnout. Most of these are checkable against an official Israeli dataset, but the data is scattered across the CBS, the Bank of Israel, the state budget, the Knesset, and dozens of data.gov.il datasets, each with its own caveats (nominal vs real, monthly vs annual, planned vs executed). An AI asked to "fact-check" a claim will often produce a confident, plausible, and completely fabricated figure, which is worse than admitting it does not know. This skill turns a claim into a sourced verdict, and refuses to invent a number when no source confirms it.

## Instructions

You are a verifier, not a commentator. Your job is to settle a specific factual claim against an authoritative Israeli source and label it. You do not argue, you do not predict, and you never fill a gap with a guessed number.

### The non-negotiable rule (read this first)

Every number, percentage, shekel amount, date, or ranking in your verdict MUST come from a source you actually pulled this session (an MCP tool result or a page you fetched) and MUST be quoted with its source name and the data's reference period. If you cannot pull a confirming figure, the verdict is **אין מספיק נתונים** (insufficient data). Do not estimate, do not infer from training data, do not "approximately." A fabricated fact-check is the one failure mode this skill exists to prevent.

### Step 1: Isolate the checkable claim

Take what the user gave you (often rhetoric plus a fact) and strip it down to the atomic, empirically checkable assertion(s). A single sentence can hold several.

- "This failing government let inflation explode to the highest in a decade" decomposes into: (a) what was the most recent CPI annual rate, (b) is it the highest in ten years. The word "failing" is opinion and gets no verdict.
- Separate fact from opinion from prediction. Opinions ("worst government ever") and predictions ("prices will rise next year") are flagged as out of scope for a verdict. You may show the relevant baseline data, but you do not rate them true or false.
- Causal claims ("the reform caused prices to rise") are not a clean true or false. Data can show a correlation but rarely proves causation. Rate these לשיפוטכם and present the data, do not stamp them נכון or לא נכון.

### Step 2: Recover the original context

The most common reason a true number becomes a מטעה (misleading) verdict is missing context. Before you check, establish: who said it, when, and against which baseline. A figure that is technically correct but compares the wrong years, mixes nominal with real, or quotes a monthly change as if annual, is misleading even when the raw number checks out.

Pin down which figure the claim actually means before you pick a source. Claims are often ambiguous between measures (nominal vs real, this year vs a multi-year total, planned vs executed budget, the statutory average wage vs the survey average). Check the most charitable correct reading of the claim, not the measure that is easiest to pull. If the claim is genuinely ambiguous, say so and verify the most plausible reading rather than the one that makes the verdict cleanest.

For any "highest, lowest, or first time in N years" claim, you cannot settle it with one current figure plus a remembered peak. Pull the full data series, confirm the index base year did not change mid-series, and compare like for like. A remembered historical peak is a fabricated comparison.

### Step 3: Route the claim to the right official source

Match the claim type to its authoritative source. Prefer the dedicated MCP server when installed; otherwise fetch the official page directly. See `references/source-map.md` for the full table and the per-source pitfalls.

| Claim is about | Authoritative source | MCP (if installed) |
|---|---|---|
| Inflation, CPI, cost of living, a specific price change | Central Bureau of Statistics (CBS) | `israel-statistics`, `israeli-cbs` |
| State budget, ministry spending, procurement, support payments | BudgetKey / OpenBudget | `budgetkey`, `il-budget` |
| Exchange rate, the value of the shekel | Bank of Israel representative rate | `boi-exchange` |
| A bill, a committee, what the Knesset passed | Knesset OData | `knesset` |
| Election results, turnout, party seats | Central Elections Committee (data.gov.il) | `israel-elections` |
| Apartment / housing prices, a specific deal | CBS housing index + Nadlan recorded deals | `nadlan` |
| NGO finances, foreign political donations, amuta status | Ministry of Justice Corporations Authority | `israel-amutot` |
| Unemployment, wages, average wage | CBS labour-force survey + Bituach Leumi | `israel-statistics` |
| Crime, road safety, population, health, vehicles | Israel Police / CBS / Ministry of Health / Ministry of Transport via data.gov.il | `data-gov-il`, `israel-vehicles` |
| Anything else with a government dataset | data.gov.il (CKAN search) | `data-gov-il`, `datagov-israel` |

If the claim is a manipulated image, audio, or video rather than a statistic, the question is provenance, not a data lookup. Find the original unedited source first (reverse-image search, the original post, the full clip), because the difference between עבר שינוי (altered) and חסר הקשר (real but stripped of context) depends on seeing the original. Use FakeReporter to check whether a coordinated network or a known fake has already been exposed, not as proof on its own: absence from FakeReporter says nothing about a given item.

### Step 4: Pull the figure and record the citation trail

Query the source. For every figure you bring back, record four things, because they go into the verdict verbatim:

1. The exact figure as published.
2. The source name (e.g. "CBS Consumer Price Index").
3. The reference period (e.g. "April 2026", "Q1 2026", "rate of 2026-06-04").
4. Any framing caveat (nominal vs real, planned vs executed budget, survey vs registered).

If the source returns nothing, or you cannot reach it, say so plainly and move toward אין מספיק נתונים. Do not substitute a number from memory.

### Step 5: Assign one verdict label with the citation trail

Use the scale published by The Whistle (המשרוקית), the Israeli fact-checking desk and the country's IFCN signatory since 2018. The first five labels below are The Whistle's published scale; the sixth, אין מספיק נתונים, is this skill's anti-fabrication addition for when no source can settle the claim. Use one label per claim:

| Label | When to use it |
|---|---|
| **נכון** | The statement is true in its near-entirety. |
| **לא מדויק** | Substantial parts of the statement are wrong. |
| **מטעה** | The statement creates a false impression or takes facts out of context, even if a raw number is technically correct. |
| **לא נכון** | The statement is false. |
| **לשיפוטכם** | The factual situation is too complex for a single definitive score. Lay out the data and let the reader judge. |
| **אין מספיק נתונים** | No authoritative source confirms or refutes it. This is the anti-fabrication fallback, not a failure. |

For a viral image, audio, or video, the platform-style labels fit better: לא נכון, עבר שינוי (altered), לא נכון חלקית (partly false), חסר הקשר (missing context), or סאטירה.

Apply the same standard regardless of who made the claim. Non-partisanship is the point.

### Step 6: Output the verdict

Produce a compact, quotable verdict block. Default to Hebrew when the claim was Hebrew, English when it was English. Structure:

```
טענה: <the claim as stated, in one line>
פסיקה: <one label from the scale>
מה הנתונים מראים: <the authoritative figure, quoted>
מקור: <source name>, <dataset / page>, <reference period>, נמשך ב-<date you pulled it>
הערת הקשר: <one line if context changes the picture, otherwise omit>
```

If the claim decomposed into several atomic assertions (Step 1), emit one verdict block per assertion. A compound claim has no single label: rate each part on its own, and if it helps the reader, add a one-line overall read (for example, partly נכון and partly מטעה). Keep it to the verdict and its evidence. Do not add advocacy, recommendations, or a call to action.

## Recommended MCP Servers

Install the MCP that matches the claim type for live, structured access. All are in the agentskills.co.il directory. Without an MCP, fetch the official page directly (see Reference Links), but the MCP is faster and returns structured data you can quote precisely.

| MCP | Use it for |
|---|---|
| `budgetkey` / `il-budget` | State budget, executed vs planned spending, procurement, support payments |
| `israel-statistics` / `israeli-cbs` | CPI, inflation, housing index, labour force, demographics |
| `boi-exchange` | Official Bank of Israel representative exchange rates |
| `knesset` | Bills, committees, member profiles, legislative status |
| `israel-elections` | Knesset election results, seats, turnout |
| `nadlan` | Recorded real-estate transaction prices |
| `israel-amutot` | Non-profit registry, foreign political donation disclosures |
| `data-gov-il` / `datagov-israel` | Any government dataset via CKAN search |

## Bundled Resources

- `references/source-map.md`: the full claim-type to source mapping, each source's update cadence, and the per-source pitfalls that turn a correct number into a misleading one.
- `references/domain-checklist.md`: the coverage contract for this skill, the verdict scale with sources, and the standard fact-check workflow.
- `scripts/verdict_template.py`: prints the verdict scale and a fillable verdict skeleton, and suggests the likely source for a claim from keywords. It scaffolds structure only and never produces a figure.

## Gotchas

These are mistakes an AI agent makes when fact-checking Israeli claims, not user errors.

- **Filling the gap with a plausible number.** The single biggest failure. When the source is unreachable or silent, the agent invents a figure that "sounds right". The correct move is אין מספיק נתונים. A fabricated verdict is worse than no verdict.
- **Confusing the two unemployment figures.** The CBS labour-force survey unemployment rate and the Sherut HaTaasuka count of registered job-seekers are different numbers measuring different things. Quoting one as the other is a classic מטעה.
- **Planned vs executed budget.** A claim about spending must be checked against executed budget (ביצוע), not the original planned budget (תקציב מקורי). They diverge, and citing the wrong one flips the verdict.
- **Market spot rate vs representative rate.** For shekel exchange-rate claims, only the Bank of Israel representative rate (שער יציג) is authoritative. A market spot rate from a finance site is not the official figure.
- **Asking prices vs recorded deals.** "Apartment prices" claims need recorded transaction prices (Nadlan) or the CBS House Price Index, not listing/asking prices from a real-estate portal. For a national trend use the CBS index, not an average of individual deals.
- **Per-MK plenum votes are a separate Knesset dataset, not the elections committee.** The ParliamentInfo OData service exposes bills, committees, and members, but not how each MK voted on the plenum floor. For roll-call votes use the Knesset's own plenum-votes dataset on data.gov.il (הצבעות חברי הכנסת במליאה, published by the Knesset). Do NOT use the Central Elections Committee data for this: it holds ballot-box election results, not how MKs voted on laws.
- **Provisional vs revised figures.** The CBS and the Bank of Israel revise numbers (CPI revisions, GDP revisions, provisional vs final budget execution). A claim that is true against the first provisional print can be false against the revised one. Note whether the figure you pulled is provisional or final, and pin the verdict to that.
- **Treating a stale dataset as current.** data.gov.il datasets update on wildly different schedules. Always read the resource's last-updated metadata and state the reference period; do not present three-year-old data as today's.

## Reference Links

| Source | URL | What to check |
|---|---|---|
| The Whistle methodology (verdict scale) | https://www.globes.co.il/news/article.aspx?did=1001372882 | The five Hebrew verdict labels and editorial method |
| IFCN Code of Principles | https://ifcncodeofprinciples.poynter.org/the-commitments | Non-partisanship, source and methodology transparency |
| Central Bureau of Statistics | https://www.cbs.gov.il | CPI, price indices, labour force, housing index, demographics |
| Bank of Israel exchange rates | https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/ | Official representative rate (שער יציג) |
| BudgetKey / OpenBudget | https://next.obudget.org/ | State budget, executed spending, procurement, support payments |
| Knesset OData | https://knesset.gov.il/Odata/ParliamentInfo.svc/ | Bills, committees, member profiles |
| Central Elections Committee (data.gov.il) | https://data.gov.il/he/datasets/central-election-committee/votes-knesset | Official election results, seats, turnout |
| Government real-estate site (Nadlan) | https://www.nadlan.gov.il/ | Recorded real-estate transaction prices |
| Bituach Leumi average wage | https://www.btl.gov.il | Statutory benefit-base average wage (cost-of-living claims need the CBS survey average instead) |
| FakeReporter | https://fakereporter.net/ | Provenance of viral media, exposed fakes and networks |
| data.gov.il | https://data.gov.il | CKAN search for any ministry dataset |

## Troubleshooting

**The source is down or returns nothing.** Do not substitute a remembered figure. Retry once, try the dedicated MCP if you used the web page (or vice versa), and if still empty, return אין מספיק נתונים and say which source you could not reach.

**The claim mixes several facts.** Decompose it (Step 1) and issue a separate verdict per atomic assertion. A compound statement can be partly נכון and partly לא נכון.

**The claim is an opinion or a prediction.** It gets no true/false verdict. Say so, and optionally present the relevant baseline data without rating it.

**Two sources disagree.** Prefer the primary official dataset over a news summary of it. If two official sources genuinely differ (e.g. different definitions), that is a לשיפוטכם, and you explain the definitional gap rather than picking one.

**The user wants the verdict in the other language.** Translate the prose but keep the source names and reference periods intact, and keep the Hebrew verdict label alongside its English gloss.
