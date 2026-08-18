---
name: israeli-statistics
description: Access Israeli Central Bureau of Statistics (CBS) data including CPI, housing price indices, economic indicators, and demographic data. Use when user asks about Israeli statistics, "hamadad", CPI, consumer price index, housing prices, "madad mchirei dirot", GDP, unemployment, population data, CBS data, "halishka hamerkazit listatistika", producer prices, building starts, or any Israeli economic/demographic statistics. Enhances the israel-statistics MCP server with index interpretation and economic context. Do NOT use for non-Israeli statistics or financial forecasting.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Network access helpful for CBS data lookups. Enhanced by the israel-statistics MCP server.
---

# Israeli Statistics (CBS)

## Critical Note
Statistical data is published on a fixed schedule with inherent delays.

**CPI release rule (exact):** all price indices are published on the 15th of the month
at 18:30 Israel time. **If the 15th falls on a Friday, the eve of a holiday, a Saturday,
or a holiday, the release moves to the Friday / holiday eve at 14:00.** This exception is
not rare, so never promise a user "18:30 on the 15th" without checking the day of week.
(The July 2026 index was published on 14/08/2026 under exactly this rule.)

The apartment price index is monthly but runs a longer lag than the CPI: roughly two to
three months, not six weeks. Always note the reference period when presenting data.
Index values and rates change, verify current figures at cbs.gov.il for time-sensitive
decisions such as rent adjustments or contract indexation.

## Reference Snapshot (verified 2026-08-18) -- RE-FETCH BEFORE QUOTING
These are dated reference points for sanity-checking an answer, **not values to quote**.
Every row marked "fetch" has no fixed value on purpose: it moves faster than this file can
be updated, so fetching it is the instruction. For any contract, court filing, rent
adjustment, or indexation calculation, re-fetch before computing, even for the rows that
do carry a number.

| Indicator | Value | Reference period | How to re-fetch |
|-----------|-------|------------------|-----------------|
| CPI index / monthly / annual change | fetch, do not quote from here | latest published month | `api.cbs.gov.il/index/data/price?id=120010&format=json&last=3` |
| Apartment price index | fetch, do not quote from here | latest published month | `api.cbs.gov.il/index/data/price?id=40010&format=json&last=3` |
| Producer prices (industrial output) | fetch | latest published month | `api.cbs.gov.il/index/data/price?id=170030&format=json&last=3` |
| Residential building input costs | fetch | latest published month | `api.cbs.gov.il/index/data/price?id=200010&format=json&last=3` |
| Bank of Israel policy rate | 3.5% (next decision 2026-08-31) | set 2026-07-06 | boi.org.il interest-rate page |
| Unemployment rate (15+, SA) | 3.1% | July 2026 (released 2026-08-17) | CBS Labour Force Survey release |
| Labor force participation | 62.2% | July 2026 | CBS Labour Force Survey release |
| Average gross monthly wage | fetch from CBS before quoting | latest CBS wage release | CBS wage tables |
| Minimum wage | NIS 6,443.85/month | From 2026-04-01 | Israeli labor law |
| GDP growth (annual) | 2.9% (revised down from an initial 3.1%) | Full year 2025 | CBS National Accounts |
| Population | 10.178 million | 2026-01-01 estimate | CBS |
| Population breakdown | 76.3% Jews and others, 21.1% Arabs, 2.6% foreign nationals | 2026-01-01 | CBS |

As a staleness check only, the CPI stood at 105.1 (2024 average base) for July 2026, +0.3%
on the month and +1.5% year-on-year, and the apartment price index was -1.5% year-on-year
in May 2026. If a fetch returns a materially different reference month than these, the
series has simply moved on, which is expected. Always pair a figure with its reference
period when answering.

## Instructions

### Step 1: Identify Statistical Need
| Need | Data Source | Frequency |
|------|------------|-----------|
| CPI / Consumer prices | CPI tables | Monthly |
| Housing prices | Housing Price Index | Monthly (2-3 month lag); quarterly transactions report is separate |
| Rent adjustment | CPI change calculation | Monthly |
| GDP / Economic growth | National Accounts | Quarterly |
| Unemployment | Labor Force Survey | Monthly |
| Population / Demographics | Population estimates | Annual/Quarterly |
| Producer prices | PPI tables | Monthly |
| Construction activity | Building starts data | Monthly |
| Trade / Exports | Foreign trade tables | Monthly |
| Wages / Income | Wage statistics | Quarterly |

### Step 2: Consumer Price Index (CPI) -- "Hamadad"
The CPI (madad hamchirim latarchan) is Israel's most widely referenced index.

**How to use CPI data:**
1. **Current month CPI:** Latest published value and monthly change
2. **Annual change:** Year-over-year percentage change (inflation rate)
3. **Component breakdown:** Which sectors are driving price changes

**CPI Components:** the CPI basket is divided into consumption groups (housing, transportation, food, health, education and culture, clothing and footwear, furniture and household, miscellaneous). The weight of each group is re-set by CBS and published with the index; do not quote a weight from memory.

**The API does not serve component weights.** The catalog endpoint
(`api.cbs.gov.il/index/catalog/catalog?format=json`) returns only a list of index chapters,
each with `chapterName` and `mainCode` -- no weights and no component breakdown. Do not send
an agent there for weights; it will come back empty and is then liable to invent a number.
Take the current weights from the CBS publications reached via the Main Price Indices hub
(https://www.cbs.gov.il/en/Pages/Main%20Price%20Indices.aspx), which links the monthly CPI
media release and the Price Statistics Monthly. If you cannot find a weight in those
publications, say so rather than supplying a number.

**Rent adjustment formula (for madad-linked contracts):**
```
New Rent = Old Rent * (Current CPI / CPI at contract signing)
```
Example: If CPI rose from 100.0 to 103.5 since contract start, rent increases by 3.5%.

### Step 3: Housing Price Index (Madad Mchirei Dirot)
Tracks residential property transaction prices:

**Key breakdowns:**
- **National average:** Overall price trend for all of Israel
- **By district:** Jerusalem, Tel Aviv, Haifa, Central, Southern, Northern
- **By city:** Major cities tracked individually
- **By property type:** New vs. existing apartments
- **By apartment size:** 1.5-2, 2.5-3, 3.5-4, 4.5+ rooms

**Interpreting the index:**
- Monthly change: Short-term market direction (noisy; the index is published as a rolling comparison, so read 3 months together)
- Annual change: Medium-term trend (smooths seasonal effects)
- Compared to wages: Affordability indicator

### Step 4: Economic Indicators Dashboard
Key macroeconomic data from CBS:

**GDP (Gross Domestic Product):**
- Quarterly publication, seasonally adjusted
- Real vs. nominal growth rates
- Per-capita GDP for international comparison

**Labor Market:**
- Unemployment rate (shiur haavtala): Monthly, ages 15+
- Labor force participation rate
- Employment by sector (tech, manufacturing, services, etc.)
- Average wage by sector (published quarterly)

**Trade and Balance of Payments:**
- Monthly export/import data
- Goods vs. services breakdown
- Key trading partners

**Construction:**
- Building starts (hatchalot bniya): Leading indicator for housing supply
- Building completions (gmitot bniya)
- Permits issued vs. starts vs. completions pipeline

### Step 5: Demographic Data
CBS is the authoritative source for Israeli demographics:

**Population:**
- Total population: Updated quarterly (interim) and annually (final)
- By religion: Jewish, Muslim, Christian, Druze, other
- By district and city
- Age distribution and dependency ratios
- Population projections (medium and long-term)

**Migration:**
- Aliyah (immigration) statistics: Monthly by country of origin
- Yerida (emigration) estimates
- Net migration trends

**Vital statistics:**
- Birth rate, death rate, natural increase
- Life expectancy (by gender)
- Marriage and divorce rates

### Step 6: Querying CBS Data
Using the israel-statistics MCP server or direct CBS access.

**Two distinct data sources:**
- **CBS Price Indices API** (`api.cbs.gov.il/index`): the canonical source for CPI, housing prices, producer prices, and building input costs. List indices at `api.cbs.gov.il/index/catalog/catalog?format=json`, fetch a series at `api.cbs.gov.il/index/data/price?id={code}&format=json`.

**Index codes served by the catalog.** The catalog carries more than the CPI, and Israeli
contracts are commonly linked to one of the input-cost indices rather than to the CPI. Pick
the index the contract actually names:

| Index | Code | Typical use |
|-------|------|-------------|
| Consumer Price Index (general) | 120010 | Rent, salaries, general madad-linked contracts |
| Apartment prices | 40010 | Housing market analysis |
| Producer prices, industrial output for local market | 170030 | Supply and manufacturing contracts |
| Residential building input costs | 200010 | Residential construction contracts |
| Commercial / office building input costs | 800010 | Commercial construction contracts |
| Paving and bridging input costs | 240010 | Infrastructure and public-works contracts |
| Agricultural input costs | 260010 | Agricultural supply contracts |

Linking a contract to the wrong index is a real and expensive error: a construction
contract indexed to the CPI rather than to building input costs tracks a different series
entirely. Read the contract's own wording before choosing a code.

The catalog also lists export producer-price and services producer-price chapters that carry
no `mainCode`; those are not fetchable through `data/price` and must be taken from the CBS
tables instead.

**CBS also publishes an official Linkage Calculations tool**
(https://www.cbs.gov.il/en/Pages/Linkage-calculations.aspx) that computes an indexed amount
between two dates. For a disputed contract or a court filing, prefer that tool's output over
a hand calculation, because it is the issuer's own arithmetic.
- **data.gov.il** under organization `lamas` (not `cbs`): hosts 14 CBS datasets, including the 2022 Population and Housing Census, the Israeli localities file, master code lists, and the injury-accident public-use files. It does NOT host the CPI/GDP/unemployment time series. Query it through the CKAN API (`data.gov.il/api/3/action/package_search?fq=organization:lamas`); the human browse pages under `/organization/` and `/dataset?organization=` currently return AccessDenied, so an agent that navigates there will wrongly conclude the datasets are gone.
- GDP, unemployment, population, and foreign-trade series are published as numbered CBS tables at `cbs.gov.il` and are not all exposed via a public API.

**CBS table structure:**
- Tables are identified by number (e.g., Table 2.1, Table 12.5)
- Data organized by subject area (population, prices, labor, etc.)
- Available in Hebrew and partially in English
- Downloadable as CSV, Excel, or via API

**Common table references:**
| Subject | Table Range | Description |
|---------|------------|-------------|
| Population | 2.x | Population size, demographics |
| Migration | 4.x | Immigration and emigration |
| Prices | 12.x | CPI, housing, producer prices |
| Labor | 12.x | Employment, wages, unemployment |
| National accounts | 16.x | GDP, growth, per capita |
| Construction | 19.x | Building activity |
| Foreign trade | 16.x | Exports, imports |

**Tips for CBS data queries:**
- Hebrew field names are common -- check column headers
- Date formats vary: some tables use Hebrew calendar, most use Gregorian
- Seasonal adjustment: Many series available both raw and seasonally adjusted
- Revisions: Preliminary data may be revised in subsequent releases

## Examples

### Example 1: CPI and Rent Adjustment
User says: "My landlord wants to raise my rent based on hamadad. Is that allowed?"
Result: Explain madad-linked rental contracts. If the contract specifies CPI adjustment, calculate: look up CPI at contract signing date and current CPI, apply the formula. Note that adjustments are typically annual, not monthly. Two contract details decide the answer and must be read out of the contract itself, not assumed: (1) **which index is the base index** (madad bassis) -- contracts commonly name the index *known* at signing, which is the previously published month, not the month of signing; using the wrong base shifts the result. (2) **whether the contract has a floor clause.** If CPI has fallen, the rent follows it down only where the contract does not bar a decrease; many Israeli rental contracts state that the rent never drops below the base. Do not tell the user their rent must fall without reading that clause.

### Example 2: Housing Market Analysis
User says: "Are apartment prices going up or down in Tel Aviv?"
Result: Query the Housing Price Index for Tel Aviv district. Present quarterly and annual trends. Compare to national average. Note relevant context: interest rates, building starts in area, supply/demand factors.

### Example 3: Economic Overview
User says: "How is the Israeli economy doing?"
Result: Present latest GDP growth (quarterly, annualized), unemployment rate, CPI inflation rate, shekel exchange rate trends, and notable sector performance. Provide CBS sources for each figure. Fetch the CPI from `api.cbs.gov.il/index/data/price?id=120010` rather than quoting it from this file. As a staleness check only, the 2026-08-18 baseline was: GDP +2.9% for 2025 (revised down from an initial 3.1%), CPI annual inflation 1.5% in July 2026 (monthly +0.3%, index 105.1 on the 2024 average base), unemployment 3.1% in July 2026, Bank of Israel rate 3.5% set 2026-07-06 with the next decision due 2026-08-31. Always re-fetch before answering for a fresh date.

## Bundled Resources

### Scripts
- `scripts/fetch_cbs_data.py` - Query the CBS Price Indices API (`api.cbs.gov.il`): fetch the latest CPI (hamadad) values plus component weights, search the index catalog, calculate madad-linked rent adjustments from old/new CPI values, and display a key economic indicators summary with the right source per series. Supports subcommands: `cpi`, `rent-calc`, `search`, `indicators`. Run: `python scripts/fetch_cbs_data.py --help`

### References
- `references/cbs-data-guide.md` - CBS publication schedule for all major indicators (CPI, housing prices, GDP, unemployment, building starts), CPI component weights, the rent adjustment formula for madad-linked contracts, and CBS table number reference by subject area (population 2.x, prices 12.x, construction 19.x, etc.). Consult when determining data availability timing or locating the correct CBS table number.

## Recommended MCP Servers

| MCP Server | What it adds | Link |
|------------|--------------|------|
| israel-statistics | Tools for CBS catalog browsing and economic-data lookups (CPI, housing, indicators) to pair with this skill's interpretation guidance | https://agentskills.co.il/he/mcp/israel-statistics |
| israeli-cbs | Alternative CBS MCP server for querying Israeli statistics tables and price indices | https://agentskills.co.il/he/mcp/israeli-cbs |

## Gotchas
- The Central Bureau of Statistics (CBS/Lama"s) publishes data primarily in Hebrew. API responses and dataset metadata use Hebrew field names. Agents may fail to parse non-ASCII column names.
- Israeli statistical surveys use a different geographic classification system (nafa, machoz) than US states/counties. Agents may try to map Israeli regions to US geographic concepts.
- CBS data release schedules are fixed but the publications often include preliminary data that is revised in subsequent releases. Agents may present preliminary figures as final without noting the revision status.
- Population statistics in Israel include or exclude different territories depending on the dataset. Agents should verify whether a given statistic covers Israel proper, the West Bank settlements, or East Jerusalem.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Central Bureau of Statistics | https://www.cbs.gov.il | CPI, housing prices, employment, population tables |
| CBS Price Indices API | https://api.cbs.gov.il/index/catalog/catalog?format=json | Canonical API for CPI, housing, producer-price, and building-cost series (use `data/price?id={code}` to fetch a series) |
| data.gov.il - CBS datasets (API) | https://data.gov.il/api/3/action/package_search?fq=organization:lamas | The 14 CBS datasets on data.gov.il: 2022 census, localities file, traffic-accident PUFs, code lists. Organization slug is `lamas`, NOT `cbs`; does not host CPI/GDP time series. **Use the API path: the human browse pages `data.gov.il/organization/lamas` and `data.gov.il/he/dataset?organization=lamas` currently return AccessDenied.** |
| CBS Main Price Indices hub | https://www.cbs.gov.il/en/Pages/Main%20Price%20Indices.aspx | Release rule and its Friday/holiday exception, latest media releases, CPI basket weights, linkage calculator |
| CBS Linkage Calculations | https://www.cbs.gov.il/en/Pages/Linkage-calculations.aspx | Official indexed-amount calculator for contract and rent indexation disputes |
| Bank of Israel data | https://www.boi.org.il | Monetary, financial, and exchange-rate data |
| CBS English portal | https://www.cbs.gov.il/en/Pages/default.aspx | English-language statistical tables and publications |

## Troubleshooting

### Error: "Data not yet published"
Cause: CBS follows a fixed publication calendar with reporting lags
Solution: Check the CBS publication calendar (luach pirsumim) for the expected release date. CPI: 15th of the month at 18:30, moved earlier to 14:00 on the preceding Friday or holiday eve when the 15th is a Friday, Saturday, holiday, or holiday eve. Apartment price index: monthly, but running 2-3 months behind (in mid-August 2026 the latest published month was May 2026). GDP: ~6 weeks after quarter end.

### Error: "Index base period mismatch"
Cause: CBS periodically rebases indices, causing series breaks
Solution: Ensure both values being compared use the same base period. CBS publishes conversion tables between old and new base periods. For CPI, check which base year applies to the series.

### Error: "Hebrew column names in data"
Cause: CBS data tables primarily use Hebrew headers
Solution: Use the israel-statistics MCP server which can interpret Hebrew field names. Or query with limit=1 to inspect column structure before full data retrieval.