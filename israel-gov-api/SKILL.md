---
name: israel-gov-api
description: Discover, query, and analyze Israeli government open data from data.gov.il (CKAN API). Use when user asks about Israeli government data, "data.gov.il", government datasets, CBS statistics, or needs data about Israeli transportation, education, health, geography, economy, or environment. Supports dataset search, tabular data queries, and analysis guidance. Pair with the MCP servers listed below for direct tool access from your agent. Do NOT use for classified government data or data requiring security clearance.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Requires network access for data.gov.il API. Enhanced by datagov-mcp or data-gov-il-mcp servers.
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
| Central Bureau of Statistics | lamas | halishka hamerkazit listatistika |
| Ministry of Transportation | ministry_of_transport | misrad hatahaburah |
| Ministry of Health | ministry-health | misrad habriut |
| Ministry of Education | ministry_of_education | misrad hachinuch |
| Israel Tax Authority | taxes-authority | rashut hamisim |
| Israel Land Authority | the_israel_lands_administration | rashut mekarkei yisrael |
| Ministry of Interior | interior_affairs | misrad hapnim |

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

**Filter by field values:**
```
GET https://data.gov.il/api/3/action/datastore_search?resource_id=RESOURCE_ID&filters={"field_name":"value"}&limit=100
```

**Select specific fields and sort:**
```
GET https://data.gov.il/api/3/action/datastore_search?resource_id=RESOURCE_ID&fields=field1,field2&sort=field1 desc&limit=100
```

**Full-text search within a resource:**
```
GET https://data.gov.il/api/3/action/datastore_search?resource_id=RESOURCE_ID&q=search+term&limit=100
```

**Important:** The `datastore_search_sql` endpoint may be disabled on data.gov.il (often returns 403 Forbidden). Use `datastore_search` with `filters`, `fields`, `sort`, `q`, `limit`, and `offset` parameters instead.

**Tips:**
- Field names are often in Hebrew -- use `datastore_search` with `limit=1` first to see field names
- Use `filters` parameter with a JSON object for exact field matching (e.g., `filters={"city_code":"5000"}`)
- Use `q` parameter for full-text search across all fields
- Large datasets: use `limit` and `offset` for pagination
- Date fields may be in various formats -- check dataset documentation

**Pagination:**
- Offset paging caps at roughly 32,000 records on the data.gov.il datastore. Above that, deep `offset=` requests will start returning errors or empty pages.
- For datasets above ~32k rows, switch to cursor paging on `_id`: sort by `_id` ascending and keep `filters={"_id":">LAST_ID"}` between calls. CKAN exposes the `_id` integer on every record.
- The response `total` field is the count of all records in the resource (not in the page), so use it to plan how many pages you need.
- `records_format` accepts `objects` (default JSON), `lists` (positional arrays), `csv`, or `tsv`. `lists` and `csv` are noticeably faster and cheaper for large pulls; reach for them when streaming or bulk-extracting.

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

Resource IDs below were verified live on 2026-05-13 via `datastore_search?resource_id=<id>&limit=1`. IDs on data.gov.il do change without notice. Always re-verify before quoting them to a user.

| Dataset | Resource ID | Description |
|---------|------------|-------------|
| Private and commercial vehicles (vehicle registration) | `053cea08-09bc-40ec-8f7a-156f0677aff3` | Full registry of private and commercial vehicle license plates with make, model, year. ~4.1M rows. |
| Public-transport vehicles | `cf29862d-ca25-4691-84f6-1be60dcb4a1e` | Active license plates of public-transport vehicles (buses, taxis). ~65k rows. |
| Education institutions (`mosdot`) | `5548fd63-5868-4053-ad81-98caddc5e232` | Characteristics of educational institutions supervised by the Ministry of Education. ~120k rows. |
| Registered amutot (NGOs) | `be5b7935-3922-45d4-9638-08871b17ec95` | Ministry of Justice registry of associations / non-profits. ~75k rows. |

For other domains (GTFS public transport, real-estate transactions, hospital quality, air quality), use `package_search` to discover the current dataset, then `package_show` to grab the active `resources[].id` -- those IDs rotate when datasets are re-published year over year.

## Examples

### Example 1: Find School Data (full chained workflow)
User says: "I need data about schools in Tel Aviv"

Actions (do not skip the lookup steps -- resource IDs rotate):

1. Discover candidate datasets:
   ```
   curl -s "https://data.gov.il/api/3/action/package_search?q=mosdot&rows=5"
   ```
2. Inspect the chosen dataset and grab the active `resources[].id`:
   ```
   curl -s "https://data.gov.il/api/3/action/package_show?id=mosdot" \
     | python3 -c "import sys,json; r=json.load(sys.stdin)['result']['resources']; [print(x['id'], x['format'], x.get('name','')) for x in r]"
   ```
3. Peek at field names with `limit=1`:
   ```
   curl -s "https://data.gov.il/api/3/action/datastore_search?resource_id=5548fd63-5868-4053-ad81-98caddc5e232&limit=1"
   ```
4. Filter by Tel Aviv city code (5000) once you have the correct Hebrew field name (commonly `סמל_ישוב`). Hebrew values must be percent-encoded:
   ```
   curl -s "https://data.gov.il/api/3/action/datastore_search?resource_id=5548fd63-5868-4053-ad81-98caddc5e232&filters=%7B%22%D7%A1%D7%9E%D7%9C_%D7%99%D7%A9%D7%95%D7%91%22%3A%225000%22%7D&limit=100"
   ```

Result: Structured school list for Tel Aviv (count, types, sizes).

### Example 2: Analyze Housing Prices
User says: "Show me housing price trends in Haifa"

Actions:
1. `package_search?q=nadlan` or `q=%D7%A2%D7%A1%D7%A7%D7%90%D7%95%D7%AA` to find the Tax Authority real-estate transactions dataset.
2. `package_show?id=<slug>` and grab the most recent year's resource id from `resources[]`.
3. `datastore_search` with the Haifa city code filter, sorted by transaction date descending.
4. Group by month, compute median price per square meter, calculate month-over-month percentage change.

Result: Monthly price trend for Haifa with analysis.

### Example 3: Municipal Data Comparison
User says: "Compare education spending across Israeli cities"

Actions:
1. `package_search?q=%D7%AA%D7%A7%D7%A6%D7%99%D7%91%20%D7%97%D7%99%D7%A0%D7%95%D7%9A` (budget + education in Hebrew, percent-encoded).
2. Pick a municipal-budget dataset, `package_show` to retrieve the active resource id.
3. `datastore_search` filtered to education-category rows; paginate via `_id` cursor if the resource exceeds 32k rows.
4. Normalize per capita using `lamas` (CBS) population figures.

Result: Ranked comparison of education spending per student across major Israeli municipalities with data source and year.

## Bundled Resources

### Scripts
- `scripts/query_datagov.py` -- Search datasets, inspect resources, and run datastore queries against the data.gov.il CKAN API directly from the command line. Supports subcommands: `search`, `dataset`, `query`, `orgs`. Run: `python scripts/query_datagov.py --help`

### References
- `references/ckan-api-reference.md` -- Complete endpoint catalog for the data.gov.il CKAN API including search parameters, datastore query syntax, and common organization IDs. Consult when constructing API calls or debugging query syntax.

## Recommended MCP Servers

Pair this skill with an MCP server so your agent can call data.gov.il (or a derived dataset) directly as tools, without scripting HTTP calls.

| MCP | URL | What it gives you |
|-----|-----|-------------------|
| `datagov-israel` | https://agentskills.co.il/he/mcps/government-services/datagov-israel | Direct MCP tool access to the data.gov.il CKAN API (search, package_show, datastore_search). |
| `data-gov-il` | https://agentskills.co.il/he/mcps/government-services/data-gov-il | Alternative MCP wrapping the same data.gov.il CKAN API. |
| `israel-vehicles` | https://agentskills.co.il/he/mcps/government-services/israel-vehicles | Pre-scoped MCP for the vehicle registration dataset (license-plate lookup, make/model/year). |
| `israel-amutot` | https://agentskills.co.il/he/mcps/government-services/israel-amutot | Pre-scoped MCP for the Ministry of Justice amutot (NGO) registry. |
| `israel-elections` | https://agentskills.co.il/he/mcps/government-services/israel-elections | Pre-scoped MCP for Israeli election results data. |

When this skill walks the user through a query, prefer the dedicated MCP if it's installed; fall back to the raw CKAN API otherwise.

## Gotchas
- Israeli government data APIs (data.gov.il) frequently change URLs and endpoint structures without notice. Agents may hardcode endpoints that worked last month but now return 404. Re-verify resource IDs with `package_show` before quoting them.
- The data.gov.il API returns data with Hebrew column headers by default. Agents may fail to parse responses that contain non-ASCII header names in JSON or CSV output.
- Hebrew filter values and `q` parameters must be UTF-8 percent-encoded. Raw Hebrew in URLs breaks several HTTP clients (some `curl` builds, older `requests` versions, certain proxies). Example: search for "רכב" as `q=%D7%A8%D7%9B%D7%91`; filter on "חיפה" as `filters=%7B%22city%22%3A%22%D7%97%D7%99%D7%A4%D7%94%22%7D`.
- Rate limiting on gov.il APIs is strict and undocumented. Agents that make rapid sequential requests will be blocked. Always add delays between API calls.
- A 403 response with body `Security Violation` is the data.gov.il WAF terminating your session. This is distinct from an auth 403. Recovery: back off exponentially (10s, 30s, 60s), drop any session cookies, and retry with a fresh `User-Agent`. Do not retry tight-loop, the WAF will extend the block.
- Many government datasets have date fields in DD/MM/YYYY format (Israeli convention), not ISO 8601. Agents may parse "01/02/2026" as February 1st instead of January 2nd.
- Offset paging caps around 32k records. For larger pulls, use cursor paging on `_id` (sort by `_id` ascending, filter `_id` greater than last seen).

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| data.gov.il portal | https://data.gov.il | Browse Israeli open data catalog, organizations, datasets |
| CKAN API reference | https://docs.ckan.org/en/latest/api/ | `package_search`, `package_show`, `datastore_search` signatures |
| data.gov.il dataset list | https://data.gov.il/dataset | Discover available datasets by organization and tag |
| Central Bureau of Statistics | https://www.cbs.gov.il | Upstream source for many data.gov.il statistics |
| Bank of Israel data | https://www.boi.org.il | Financial and monetary datasets not on data.gov.il |

## Troubleshooting

### Error: "Dataset not found"
Cause: Search terms too specific or in wrong language
Solution: Try broader Hebrew keywords. Government data is primarily in Hebrew.

### Error: "Datastore not available"
Cause: Not all resources have the datastore (queryable) API enabled
Solution: Download the CSV/Excel resource directly and process locally.

### Error: "403 Forbidden" on SQL queries
Cause: The `datastore_search_sql` endpoint may be disabled by data.gov.il
Solution: Use `datastore_search` with `filters`, `fields`, `sort`, and `q` parameters instead. For example: `datastore_search?resource_id=ID&filters={"city":"Haifa"}&fields=field1,field2&sort=field1 desc&limit=100`

### Error: "Hebrew field names"
Cause: Most government datasets have Hebrew column names
Solution: First query with limit=1 to see all field names, then construct targeted queries.