# Source Map: claim type to authoritative Israeli source

For each claim type, this is the authoritative source, the matching skills-il MCP (if one exists), the update cadence, and the pitfalls that most often turn a correct figure into a misleading verdict. Always prefer the primary official dataset over a news article that summarizes it.

## Economy and prices

| Claim type | Authoritative source | MCP | Cadence | Pitfalls |
|---|---|---|---|---|
| Inflation / CPI / cost of living / a specific price change | Central Bureau of Statistics (CBS) | `israel-statistics`, `israeli-cbs` | Monthly | Distinguish month-over-month from year-over-year, nominal from real, and note the base year and basket. |
| Exchange rate / value of the shekel | Bank of Israel representative rate (שער יציג) | `boi-exchange` | Daily (business days) | Use the official representative rate, not a market spot rate. Pick the rate for the correct date. |
| Unemployment | CBS labour-force survey | `israel-statistics` | Monthly / quarterly | CBS survey unemployment is not the Sherut HaTaasuka count of registered job-seekers. Do not conflate. |
| Wages / average wage | CBS + Bituach Leumi statutory average wage | `israel-statistics` | Periodic | The statutory "average wage in the economy" differs from the survey average. State which, and the reference period. |

## Government and politics

| Claim type | Authoritative source | MCP | Cadence | Pitfalls |
|---|---|---|---|---|
| State budget / ministry spending / procurement / support payments | BudgetKey / OpenBudget | `budgetkey`, `il-budget` | Updated through the current fiscal cycle | Check executed budget (ביצוע), not the original planned budget (תקציב מקורי). They diverge. |
| A bill / committee / what the Knesset passed | Knesset ParliamentInfo OData | `knesset` | Continuous | The OData has bills, committees, and members, but not per-MK plenum votes. For roll-call votes use the Knesset's own plenum-votes dataset on data.gov.il (הצבעות חברי הכנסת במליאה), not the Central Elections Committee (which holds ballot-box election results). |
| Election results / turnout / party seats | Central Elections Committee (data.gov.il) | `israel-elections` | Per election | Use official final results, not exit polls. Turnout denominator is eligible voters. |
| NGO finances / foreign political donations / amuta status | Ministry of Justice Corporations Authority | `israel-amutot` | Periodic disclosures | Known under-reporting. Absence of a disclosure is not proof of no funding. Note the reporting threshold. |

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

When the claim is a doctored image, audio clip, or video rather than a statistic, the verdict path is provenance, not a data pull. Check exposure history at FakeReporter and use the platform labels (עבר שינוי, חסר הקשר, סאטירה) rather than a number. FakeReporter exposes networks and fakes; it is not a numeric fact-check desk.
