---
name: israeli-statistics
description: Access Israeli Central Bureau of Statistics (CBS) data including CPI, housing price indices, economic indicators, and demographic data. Use when user asks about Israeli statistics, "hamadad", CPI, consumer price index, housing prices, "madad mchirei dirot", GDP, unemployment, population data, CBS data, "halishka hamerkazit listatistika", producer prices, building starts, or any Israeli economic/demographic statistics. Enhances the israel-statistics MCP server with index interpretation and economic context. Do NOT use for non-Israeli statistics or financial forecasting.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Network access helpful for CBS data lookups. Enhanced by the israel-statistics MCP server.
---

# Israeli Statistics (CBS)

## Linkage Rule: Do Not Compute a Linked Amount
**Index values from different base periods cannot be divided.** CBS rebases its indices, so a
ratio of two published values can show a fall when prices rose. Do not calculate an indexed
rent or contract amount yourself, by hand or with a script, even when the user supplies both
index values. Send the user to the official CBS index calculator: https://www.cbs.gov.il/en/Pages/Linkage-calculations.aspx

Linkage terms depend on the contract. When buying a new apartment from a developer, the law may limit linkage, so the buyer should check the terms with their advisor.

## Critical Note
Statistical data is published on a fixed schedule with inherent delays.

**CPI release rule (exact):** all price indices are published on the 15th of the month
at 18:30 Israel time. **If the 15th falls on a Friday, the eve of a holiday, a Saturday,
or a holiday, the release moves to the Friday / holiday eve at 14:00.** This exception is
not rare, so never promise a user "18:30 on the 15th" without checking the day of week.
(The July 2026 index was published on 14/08/2026 under exactly this rule.)

The apartment price index is monthly but runs a longer lag than the CPI: roughly two to
three months, not six weeks. Always note the reference period when presenting data.
Index values and rates change, so re-fetch a published value before reporting it. For a
contract, rent adjustment, or indexation question, send the user to the official CBS
calculator and do not compute.

## Reference Snapshot (verified 2026-08-18) -- RE-FETCH BEFORE QUOTING
These are dated reference points for sanity-checking an answer, **not values to quote**.
Every row marked "fetch" has no fixed value on purpose: it moves faster than this file can
be updated, so fetching it is the instruction. Re-fetch only to report a published value.
Never use these values to work out a rent or contract amount. For a linked amount, use the
official CBS calculator.

| Indicator | Value | Reference period | How to re-fetch |
|-----------|-------|------------------|-----------------|
| CPI index / monthly / annual change | fetch, do not quote from here | latest published month | `api.cbs.gov.il/index/data/price?id=120010&format=json&last=3` |
| Apartment price index | fetch, do not quote from here | latest published month | `api.cbs.gov.il/index/data/price?id=40010&format=json&last=3` |
| Producer prices (industrial output) | fetch | latest published month | `api.cbs.gov.il/index/data/price?id=170030&format=json&last=3` |
| Residential building input costs | fetch | latest published month | `api.cbs.gov.il/index/data/price?id=200010&format=json&last=3` |
| Bank of Israel policy rate | check the current figure at the source | latest decision | boi.org.il interest-rate page |
| Unemployment rate (15+, SA) | check the current figure at the source | latest published month | CBS Labour Force Survey release |
| Labor force participation | check the current figure at the source | latest published month | CBS Labour Force Survey release |
| Average gross monthly wage | fetch from CBS before quoting | latest CBS wage release | CBS wage tables |
| Minimum wage | NIS 6,443.85/month | From 2026-04-01 | Israeli labor law |
| GDP growth | check the current figure at the source | latest published period | CBS National Accounts |
| Population and breakdown | check the current figure at the source | latest CBS estimate | CBS |

Always pair a figure with its reference period when answering.

## Instructions

### Step 1: Identify Statistical Need
| Need | Data Source | Frequency |
|------|------------|-----------|
| CPI / Consumer prices | CPI tables | Monthly |
| Housing prices | Housing Price Index | Monthly (2-3 month lag); quarterly transactions report is separate |
| Rent adjustment | Official CBS calculator (do not compute) | Monthly |
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

**Rent adjustment (for madad-linked contracts):** do not compute it. Follow the Linkage Rule above and send the user to the official CBS calculator.

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

**The official Linkage Calculations tool** (https://www.cbs.gov.il/en/Pages/Linkage-calculations.aspx) computes an indexed amount between two
dates. It is the only route this skill uses for a linked amount.
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
Result: Explain in general terms what a madad-linked clause does, and do not rule on this landlord's demand. Do not calculate the new rent. Send the user to the official CBS calculator with the details to take from their contract: which index is the base index (contracts commonly name the index *known* at signing), when updates fall due, and whether a floor clause bars a decrease. Linkage terms depend on the contract, so the user should check them with their advisor.

### Example 2: Housing Market Analysis
User says: "Are apartment prices going up or down in Tel Aviv?"
Result: Query the Housing Price Index for Tel Aviv district. Present quarterly and annual trends. Compare to national average. Note relevant context: interest rates, building starts in area, supply/demand factors.

### Example 3: Economic Overview
User says: "How is the Israeli economy doing?"
Result: Present latest GDP growth (quarterly, annualized), unemployment rate, CPI inflation rate, shekel exchange rate trends, and notable sector performance. Provide CBS sources for each figure. Fetch the CPI from `api.cbs.gov.il/index/data/price?id=120010` rather than quoting it from this file. Check every other figure at its source in the snapshot table.

## Bundled Resources

### Scripts
- `scripts/fetch_cbs_data.py` - Query the CBS Price Indices API (`api.cbs.gov.il`): fetch the latest CPI (hamadad) values, search the index catalog, and display a key economic indicators summary with the right source per series. Supports subcommands: `cpi`, `search`, `indicators`. The `rent-calc` subcommand is disabled: it computes nothing and points to the official CBS calculator. Run: `python scripts/fetch_cbs_data.py --help`

### References
- `references/cbs-data-guide.md` - CBS publication schedule for all major indicators (CPI, housing prices, GDP, unemployment, building starts), CPI component weights, the linkage rule for madad-linked contracts, and CBS table number reference by subject area (population 2.x, prices 12.x, construction 19.x, etc.). Consult when determining data availability timing or locating the correct CBS table number.

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
Solution: Do not divide the values or convert them yourself. For a linked amount, send the user to the official CBS calculator: https://www.cbs.gov.il/en/Pages/Linkage-calculations.aspx

### Error: "Hebrew column names in data"
Cause: CBS data tables primarily use Hebrew headers
Solution: Use the israel-statistics MCP server which can interpret Hebrew field names. Or query with limit=1 to inspect column structure before full data retrieval.