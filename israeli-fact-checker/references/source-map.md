# Source Map: claim type to authoritative Israeli source

For each claim type, this is the authoritative source, the matching skills-il MCP (if one exists), the update cadence, and the pitfalls that most often turn a correct figure into a misleading verdict. Always prefer the primary official dataset over a news article that summarizes it.

## Economy and prices

| Claim type | Authoritative source | MCP | Cadence | Pitfalls |
|---|---|---|---|---|
| Inflation / CPI / cost of living / a specific price change | Central Bureau of Statistics (CBS) | `israel-statistics`, `israeli-cbs` | Monthly | Distinguish month-over-month from year-over-year, nominal from real, and note the base year and basket. |
| Exchange rate / value of the shekel | Bank of Israel representative rate (שער יציג) | `boi-exchange` | Daily (business days) | Use the official representative rate, not a market spot rate. Pick the rate for the correct date. |
| Unemployment | CBS labour-force survey | `israel-statistics` | Monthly / quarterly | CBS survey unemployment is not the Sherut HaTaasuka count of registered job-seekers. Do not conflate. |
| Wages / average wage | CBS average monthly wage + Bituach Leumi statutory average wage | `israel-statistics` | Periodic | The statutory figure under the National Insurance Law differs from the CBS headline wage. Check the release's definition (per person or per job, average or median), state which, and the reference period. |
| Bank of Israel interest rate | BoI monetary policy announcements | none | Per Monetary Committee decision | Use the decision in force on the date the claim refers to. |
| Rent | CBS CPI rent component (שכר דירה) | `israel-statistics` | Monthly | Nadlan and the House Price Index cover purchases, not leases. |
| An opinion poll | The original poll publication | none | Per poll | Institute, sample, field dates, margin of error, question wording. Never rated against official data. |
| GDP growth / deficit / national debt | Not yet mapped: use the official publisher's own release, never a news summary | none | Varies | Provisional vs revised; deficit in % of GDP vs shekels. |
| Poverty | Bituach Leumi annual poverty and income-inequality report | none | Annual | Persons vs families vs children; the survey year lags the publication year. |
| CPI change across years | CBS index calculator / chained series | `israel-statistics` | Monthly | Never subtract raw index points across a base change. State whether the known index or the index for the month was used. |

## Government and politics

| Claim type | Authoritative source | MCP | Cadence | Pitfalls |
|---|---|---|---|---|
| State budget / ministry spending / procurement / support payments | BudgetKey / OpenBudget | `budgetkey`, `il-budget` | Updated through the current fiscal cycle | Check executed budget (ביצוע), not the original planned budget (תקציב מקורי). They diverge. |
| A bill / committee / what the Knesset passed | Knesset ParliamentInfo OData | `knesset` | Continuous | ParliamentInfo has bills, committees, and members, but not per-MK plenum votes. |
| How an MK voted in the plenum | Knesset OData V4 (`KNS_PlenumVote`, `KNS_PlenumVoteResult`) | `knesset` | Continuous | One row per recorded MK; נוכח (present) is not a vote, and no row is not "voted against". The data.gov.il package הצבעות חברי הכנסת במליאה has no data files. Not the Central Elections Committee (ballot-box results). |
| Election results / turnout / party seats | Central Elections Committee (data.gov.il) for Knesset elections; Ministry of Interior for local-authority elections (it publishes their polling-station data) | `israel-elections` | Per election | Use official final results, not exit polls. Turnout denominator is eligible voters. |
| NGO finances / foreign-state-entity support / amuta status | Ministry of Justice Corporations Authority (GuideStar) | `israel-amutot` | Periodic disclosures | Donations from a foreign state entity are a separate file in the MoJ amutot dataset on data.gov.il (moj-amutot); that file says nothing about private foreign donors. Absence of a disclosure is not proof of no funding. Party and candidate funding is reported by the State Comptroller, not here. |
| A government failure / ministry performance | State Comptroller reports | none | Annual and special reports | Quote the specific chapter and year; a finding about one year is not a finding about today. |

## Property, demographics, and the catch-all

| Claim type | Authoritative source | MCP | Cadence | Pitfalls |
|---|---|---|---|---|
| Apartment / housing prices | CBS House Price Index + Nadlan recorded deals | `nadlan` | Monthly index / lagged deals | Nadlan has a reporting lag and shows recorded sold prices, not asking prices. For a national trend use the CBS index, not an average of deals. |
| Population / demographics / immigration | CBS + PIBA | none / `data-gov-il` | Periodic | PIBA counts legal status and entries; CBS counts resident population; aliyah figures sit with CBS / Jewish Agency. Do not merge the three. |
| Crime statistics | Israel Police + CBS | `data-gov-il` | Periodic | Published data covers selected offense categories only. Reported-crime counts are not victimization rates. |
| Health / mortality / vaccination | Ministry of Health | none | Periodic | Use the right denominator (per-capita, age-standardized). Crude and age-adjusted rates differ. |
| Vehicles / road safety | Ministry of Transport + data.gov.il | `israel-vehicles` | Periodic | Road-fatality counts vary by definition (30-day vs scene) and by source. Cite the definition. |
| Education / Bagrut / PISA | Ministry of Education + OECD | none | Bagrut annual / PISA triennial | PISA is triennial. Do not cite an old cycle as current. National averages mask large subgroup gaps. |
| Company facts / ownership | Registrar of Companies | none | Continuous | Basic info is free, the full extract (נסח חברה) is paid. Beneficial ownership is not fully public. |
| Anything else with a government dataset | data.gov.il (CKAN) | `data-gov-il`, `datagov-israel` | Varies | Read the resource's last-updated metadata. Do not treat a stale dataset as current. |

## Manipulated media (not a numeric lookup)

When the claim is a screenshot, a doctored image, an audio clip, or a video rather than a statistic, the verdict path is provenance, not a data pull (SKILL.md Step 3a).

| Need | Resource | Note |
|---|---|---|
| Was it already checked? | Google Fact Check Explorer (toolbox.google.com/factcheck/explorer); The Whistle archive (globes.co.il); irrelevant.org.il | irrelevant.org.il (Hanan Cohen, chain letters since 2002) declares itself non-objective: a lead, not an authority. |
| Coordinated networks, known fakes | FakeReporter (fakereporter.net) | Exposes networks and fakes; not a numeric fact-check desk. Absence proves nothing. |
| Did the post exist? | The original account; Wayback Machine (web.archive.org); archive.today (archive.ph) | No original and no capture means אין מספיק נתונים, not לא נכון. |
| Where did the image first appear? | Google Lens, TinEye (tineye.com), Yandex Images, Bing Visual Search | Run on keyframes for video. |
| Video keyframes | InVID-WeVerify browser plugin (Chrome Web Store) | Recycled or cut real footage is חסר הקשר, not עבר שינוי. |

Use Meta's platform labels (עבר שינוי, חסר הקשר, סאטירה) for media rather than a number. They are Meta's labels; The Whistle left Meta's programme in December 2020.
