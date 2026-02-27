---
name: israeli-statistics
description: >-
  Access Israeli Central Bureau of Statistics (CBS) data including CPI, housing
  price indices, economic indicators, and demographic data. Use when user asks
  about Israeli statistics, "hamadad", CPI, consumer price index, housing
  prices, "madad mchirei dirot", GDP, unemployment, population data, CBS data,
  "halishka hamerkazit listatistika", producer prices, building starts, or any
  Israeli economic/demographic statistics. Enhances israel-statistics-mcp server
  with index interpretation and economic context. Do NOT use for non-Israeli
  statistics or financial forecasting.
license: MIT
allowed-tools: 'Bash(python:*) WebFetch'
compatibility: >-
  Network access helpful for CBS data lookups. Enhanced by israel-statistics-mcp
  server (8 tools).
metadata:
  author: skills-il
  version: 1.0.0
  category: government-services
  tags:
    he:
      - סטטיסטיקה
      - מדד-המחירים
      - מחירי-דיור
      - כלכלה
      - דמוגרפיה
      - הלמ״ס
      - ישראל
    en:
      - statistics
      - cpi
      - housing-prices
      - economics
      - demographics
      - cbs
      - israel
  mcp-server: israel-statistics-mcp
  display_name:
    he: סטטיסטיקה ישראלית
    en: Israeli Statistics
  display_description:
    he: 'נתוני הלמ"ס — מדד המחירים, דיור, תעסוקה ונתונים כלכליים'
    en: >-
      Access Israeli Central Bureau of Statistics (CBS) data including CPI,
      housing price indices, economic indicators, and demographic data. Use when
      user asks about Israeli statistics, "hamadad", CPI, consumer price index,
      housing prices, "madad mchirei dirot", GDP, unemployment, population data,
      CBS data, "halishka hamerkazit listatistika", producer prices, building
      starts, or any Israeli economic/demographic statistics. Enhances
      israel-statistics-mcp server with index interpretation and economic
      context. Do NOT use for non-Israeli statistics or financial forecasting.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - openclaw
---

# Israeli Statistics (CBS)

## Critical Note
Statistical data is published on a fixed schedule with inherent delays. CPI is released
~15 days after month-end. Housing prices are quarterly with ~3-month lag. Always note
the reference period when presenting data. Index values and rates change -- verify
current figures at cbs.gov.il for time-sensitive decisions such as rent adjustments or
contract indexation.

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
Using the israel-statistics-mcp server or direct CBS access:

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
Result: Present latest GDP growth (quarterly, annualized), unemployment rate, CPI inflation rate, shekel exchange rate trends, and notable sector performance. Provide CBS sources for each figure.

## Bundled Resources

### Scripts
- `scripts/fetch_cbs_data.py` — Search CBS datasets on data.gov.il, fetch CPI (hamadad) component weights and available datasets, calculate madad-linked rent adjustments from old/new CPI values, and display a key economic indicators dashboard with CBS table references. Supports subcommands: `cpi`, `rent-calc`, `search`, `indicators`. Run: `python scripts/fetch_cbs_data.py --help`

### References
- `references/cbs-data-guide.md` — CBS publication schedule for all major indicators (CPI, housing prices, GDP, unemployment, building starts), CPI component weights, the rent adjustment formula for madad-linked contracts, and CBS table number reference by subject area (population 2.x, prices 12.x, construction 19.x, etc.). Consult when determining data availability timing or locating the correct CBS table number.

## Troubleshooting

### Error: "Data not yet published"
Cause: CBS follows a fixed publication calendar with reporting lags
Solution: Check the CBS publication calendar (luach pirsumim) for the expected release date. CPI: ~15th of the month. Housing: ~6 weeks after quarter end. GDP: ~6 weeks after quarter end.

### Error: "Index base period mismatch"
Cause: CBS periodically rebases indices, causing series breaks
Solution: Ensure both values being compared use the same base period. CBS publishes conversion tables between old and new base periods. For CPI, check which base year applies to the series.

### Error: "Hebrew column names in data"
Cause: CBS data tables primarily use Hebrew headers
Solution: Use the israel-statistics-mcp server which can interpret Hebrew field names. Or query with limit=1 to inspect column structure before full data retrieval.