---
name: israel-gov-api
description: >-
  Discover, query, and analyze Israeli government open data from data.gov.il
  (CKAN API). Use when user asks about Israeli government data, "data.gov.il",
  government datasets, CBS statistics, or needs data about Israeli
  transportation, education, health, geography, economy, or environment.
  Supports dataset search, tabular data queries, and analysis guidance. Enhances
  existing datagov-mcp and data-gov-il-mcp servers with workflow best practices.
  Do NOT use for classified government data or data requiring security
  clearance.
license: MIT
allowed-tools: 'Bash(python:*) WebFetch'
compatibility: >-
  Requires network access for data.gov.il API. Enhanced by datagov-mcp or
  data-gov-il-mcp servers.
metadata:
  author: skills-il
  version: 1.0.0
  category: government-services
  tags:
    - government
    - data
    - ckan
    - statistics
    - open-data
    - israel
  mcp-server: datagov-mcp
  display_name:
    he: ממשקי API ממשלתיים
    en: Israel Gov Api
  display_description:
    he: גישה למידע ממשלתי פתוח מתוך data.gov.il
    en: >-
      Discover, query, and analyze Israeli government open data from data.gov.il
      (CKAN API). Use when user asks about Israeli government data,
      "data.gov.il", government datasets, CBS statistics, or needs data about
      Israeli transportation, education, health, geography, economy, or
      environment. Supports dataset search, tabular data queries, and analysis
      guidance. Enhances existing datagov-mcp and data-gov-il-mcp servers with
      workflow best practices. Do NOT use for classified government data or data
      requiring security clearance.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# Israel Government API

## Instructions

### Step 1: Understand the Data Need
Ask the user:
- **What topic?** (transportation, health, education, economy, etc.)
- **What geography?** (national, specific city/region, specific address)
- **What time period?** (current, historical, time series)
- **What format?** (raw data, summary statistics, visualization)

### Step 2: Search for Datasets
Use the data.gov.il CKAN API to find relevant datasets:

**Search by keyword:**
```
GET https://data.gov.il/api/3/action/package_search?q=KEYWORD&rows=10
```

**Search by organization (ministry):**
```
GET https://data.gov.il/api/3/action/package_search?fq=organization:MINISTRY_ID
```

**Common organization IDs:**
| Ministry | ID | Hebrew |
|----------|-----|--------|
| Central Bureau of Statistics | cbs | halishka hamerkazit listatistika |
| Ministry of Transportation | mot | misrad hatahaburah |
| Ministry of Health | moh | misrad habriut |
| Ministry of Education | moe | misrad hachinuch |
| Israel Tax Authority | ita | rashut hamisim |
| Israel Land Authority | ila | rashut mekarkei yisrael |
| Ministry of Interior | moi | misrad hapnim |

### Step 3: Retrieve and Query Data
Once a dataset is found:

**Get dataset details:**
```
GET https://data.gov.il/api/3/action/package_show?id=DATASET_ID
```

**Query tabular data (datastore):**
```
GET https://data.gov.il/api/3/action/datastore_search?resource_id=RESOURCE_ID&limit=100
```

**SQL-like queries (powerful):**
```
GET https://data.gov.il/api/3/action/datastore_search_sql?sql=SELECT * FROM "RESOURCE_ID" WHERE field = 'value' LIMIT 100
```

**Tips:**
- Field names are often in Hebrew -- use `datastore_search` with `limit=1` first to see field names
- Large datasets: use `limit` and `offset` for pagination
- Date fields may be in various formats -- check dataset documentation

### Step 4: Analyze and Present
For the retrieved data:
1. Summarize key findings in plain language
2. Calculate basic statistics if requested (mean, median, trends)
3. Suggest visualizations (bar chart, line graph, map) appropriate to the data
4. Note data freshness (last update date) and any caveats
5. Provide the direct link to the dataset on data.gov.il for reference

### Step 5: Cross-Reference (Advanced)
When combining multiple datasets:
1. Identify common keys (city code, date, category code)
2. Use Israeli administrative codes (CBS city codes) for geographic joins
3. Note that field names across datasets may differ -- match by content not name
4. Document data lineage: which datasets contributed to the analysis

## Commonly Requested Datasets

| Dataset | Resource ID | Updated | Description |
|---------|------------|---------|-------------|
| GTFS transit data | various | Daily | Bus/train schedules and routes |
| School list | various | Annual | All schools with details |
| Hospital quality | various | Quarterly | Ministry of Health quality indicators |
| Real estate prices | various | Monthly | Tax Authority transaction prices |
| Business registry | various | Daily | Active businesses |
| Air quality | various | Hourly | Environmental monitoring stations |

## Examples

### Example 1: Find School Data
User says: "I need data about schools in Tel Aviv"
Actions:
1. Search: `package_search?q=schools+tel+aviv`
2. Find education dataset, get resource ID
3. Query: Filter by city code for Tel Aviv (5000)
4. Present: School count, types, sizes
Result: Structured school data for Tel Aviv

### Example 2: Analyze Housing Prices
User says: "Show me housing price trends in Haifa"
Actions:
1. Find Tax Authority real estate transactions dataset
2. Filter by Haifa city code, last 12 months
3. Calculate median price per square meter by month
4. Present trend with percentage change
Result: Monthly price trend for Haifa with analysis

### Example 3: Municipal Data Comparison
User says: "Compare education spending across Israeli cities"
Actions:
1. Search for municipal budget datasets
2. Filter by education category
3. Normalize per capita
4. Present comparison table
Result: Ranked comparison of education spending per student across major Israeli municipalities with data source and year.

## Bundled Resources

### Scripts
- `scripts/query_datagov.py` — Search datasets, inspect resources, and run SQL/datastore queries against the data.gov.il CKAN API directly from the command line. Supports subcommands: `search`, `dataset`, `query`, `sql`, `orgs`. Run: `python scripts/query_datagov.py --help`

### References
- `references/ckan-api-reference.md` — Complete endpoint catalog for the data.gov.il CKAN API including search parameters, datastore query syntax, SQL capabilities, and common organization IDs. Consult when constructing API calls or debugging query syntax.

## Troubleshooting

### Error: "Dataset not found"
Cause: Search terms too specific or in wrong language
Solution: Try broader Hebrew keywords. Government data is primarily in Hebrew.

### Error: "Datastore not available"
Cause: Not all resources have the datastore (queryable) API enabled
Solution: Download the CSV/Excel resource directly and process locally.

### Error: "Hebrew field names"
Cause: Most government datasets have Hebrew column names
Solution: First query with limit=1 to see all field names, then construct targeted queries.