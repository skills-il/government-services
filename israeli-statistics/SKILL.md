---
name: israeli-statistics
description: Access Israeli Central Bureau of Statistics (CBS) data including CPI, housing price indices, economic indicators, and demographic data. Use when user asks about Israeli statistics, "hamadad", CPI, consumer price index, housing prices, "madad mchirei dirot", GDP, unemployment, population data, CBS data, "halishka hamerkazit listatistika", producer prices, building starts, or any Israeli economic/demographic statistics. Enhances the israel-statistics MCP server with index interpretation and economic context. Do NOT use for non-Israeli statistics or financial forecasting.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Network access helpful for CBS data lookups. Enhanced by the israel-statistics MCP server.
---

# Israeli Statistics (CBS)

## Critical Note
Statistical data is published on a fixed schedule with inherent delays. CPI is released
on the 15th of the following month at 18:30 Israel time. Housing prices are monthly
with a ~6-week lag (and a richer quarterly transactions report). Always note the
reference period when presenting data. Index values and rates change, verify current
figures at cbs.gov.il for time-sensitive decisions such as rent adjustments or contract
indexation.

## Current Snapshot (as of May 2026)
Use these as recent reference values only. For any contract, court filing, or
calculation, re-verify the latest CPI at `api.cbs.gov.il/index/data/price?id=120010`
before computing.

| Indicator | Value | Reference period | Source |
|-----------|-------|------------------|--------|
| CPI annual inflation | 1.9% | April 2026 | CBS, released 2026-05-15 |
| CPI monthly change | +1.2% | April 2026 vs March 2026 | CBS |
| Bank of Israel policy rate | 4.00% | Set 2026-03-30, unchanged from January | bankisrael.gov.il |
| Unemployment rate (15+, SA) | 2.7% | February 2026 | CBS Labour Force Survey |
| Labor force participation | 62.5% | February 2026 | CBS Labour Force Survey |
| Average gross monthly wage | ~NIS 13,623 | October 2025 (latest published) | CBS |
| Minimum wage | NIS 6,443.85/month | From 2026-04-01 | Israeli labor law |
| GDP growth (annual) | 3.0% | Full year 2025 | CBS National Accounts |
| Population | 10.178 million | 2026-01-01 estimate | CBS |
| Population breakdown | 76.3% Jews and others, 21.1% Arabs, 2.6% foreign nationals | 2026-01-01 | CBS |
| Average apartment price (national) | ~NIS 2.33 million | Q1 2026 | CBS Housing Price Index |
| Housing prices year-on-year | -1.7% | 12 months to early 2026 | CBS |

Always pair a figure with its reference period when answering, and tell the user to
re-fetch from CBS for any decision that depends on a current value.

## Instructions

### Step 1: Identify Statistical Need
| Need | Data Source | Frequency |
|------|------------|-----------|
| CPI / Consumer prices | CPI tables | Monthly |
| Housing prices | Housing Price Index | Quarterly |
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

**CPI Components (approximate weights):**
| Component | Hebrew | Weight (~%) |
|-----------|--------|-------------|
| Housing (rents) | diyur | ~25% |
| Transportation | tachburah | ~17% |
| Food | mazon | ~16% |
| Health | briut | ~6% |
| Education and culture | chinuch vetarbut | ~8% |
| Clothing and footwear | halbasha vehanala | ~3% |
| Furniture and household | rihut umeshek bayit | ~5% |
| Other | acher | ~20% |

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
- Quarterly change: Short-term market direction
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
- **CBS Price Indices API** (`api.cbs.gov.il/index`): the canonical source for CPI, housing prices, producer prices, and building input costs. List indices at `api.cbs.gov.il/index/catalog/catalog?format=json`, fetch a series at `api.cbs.gov.il/index/data/price?id=<code>&format=json` (CPI is `120010`, apartment prices `40010`).
- **data.gov.il** under organization `lamas` (not `cbs`): hosts a small set of CBS datasets such as census tabulations, localities, and traffic accidents. It does NOT host the CPI/GDP/unemployment time series.
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
Result: Explain madad-linked rental contracts. If the contract specifies CPI adjustment, calculate: look up CPI at contract signing date and current CPI, apply the formula. Note that adjustments are typically annual, not monthly. If CPI decreased, rent should decrease too.

### Example 2: Housing Market Analysis
User says: "Are apartment prices going up or down in Tel Aviv?"
Result: Query the Housing Price Index for Tel Aviv district. Present quarterly and annual trends. Compare to national average. Note relevant context: interest rates, building starts in area, supply/demand factors.

### Example 3: Economic Overview
User says: "How is the Israeli economy doing?"
Result: Present latest GDP growth (quarterly, annualized), unemployment rate, CPI inflation rate, shekel exchange rate trends, and notable sector performance. Provide CBS sources for each figure. As of May 2026 the reference baseline is: GDP +3.0% for 2025, CPI annual inflation 1.9% in April 2026, unemployment 2.7% in February 2026, Bank of Israel rate 4.00% set 2026-03-30. Always re-fetch before answering for a fresh date.

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
| CBS Price Indices API | https://api.cbs.gov.il/index/catalog/catalog?format=json | Canonical API for CPI, housing, producer-price, and building-cost series (use `data/price?id=<code>` to fetch a series) |
| CBS publication schedule | https://www.cbs.gov.il/he/pages/calendar.aspx | Release calendar for CPI, GDP, housing, demographics |
| data.gov.il - CBS datasets | https://data.gov.il/organization/lamas | Census tabulations, localities, and traffic-accident datasets (organization `lamas`, NOT `cbs`); does not host CPI/GDP time series |
| Bank of Israel data | https://www.boi.org.il | Monetary, financial, and exchange-rate data |
| CBS English portal | https://www.cbs.gov.il/en/Pages/default.aspx | English-language statistical tables and publications |

## Troubleshooting

### Error: "Data not yet published"
Cause: CBS follows a fixed publication calendar with reporting lags
Solution: Check the CBS publication calendar (luach pirsumim) for the expected release date. CPI: ~15th of the month. Housing: ~6 weeks after quarter end. GDP: ~6 weeks after quarter end.

### Error: "Index base period mismatch"
Cause: CBS periodically rebases indices, causing series breaks
Solution: Ensure both values being compared use the same base period. CBS publishes conversion tables between old and new base periods. For CPI, check which base year applies to the series.

### Error: "Hebrew column names in data"
Cause: CBS data tables primarily use Hebrew headers
Solution: Use the israel-statistics MCP server which can interpret Hebrew field names. Or query with limit=1 to inspect column structure before full data retrieval.