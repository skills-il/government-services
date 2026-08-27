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

**Common organization IDs** (all 7 re-verified on 2026-08-27 via `package_search?fq=organization:<id>`, each returning a non-zero count):
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

**`datastore_search_sql` WORKS, with one WAF-shaped hole.** Re-tested live on 2026-08-27: `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY`, `sum()` and `LIMIT` all return HTTP 200 with `success:true` and real rows. What the WAF blocks is a small set of injection-signature substrings, `count(`, `1=1` and `UNION` among them, and it does so with an **HTML 404 page, not a JSON error and not a 403**, so a client that only checks `success` will read the block as a parse failure.

- Use `sum(1)` in place of `count(*)`. `SELECT col, sum(1) AS n FROM "<resource_id>" GROUP BY col ORDER BY n DESC LIMIT 10` returns exactly what the blocked `count(*)` form would.
- For a plain row count you do not need SQL at all: `datastore_search`'s `total` field already carries it.
- **SQL is the one way to get real keyset paging.** `filters` cannot do it, but `SELECT ... FROM "<rid>" WHERE _id > <last_id> ORDER BY _id LIMIT <n>` works and stays fast at any depth, unlike deep `offset`.
- **Read the response SHAPE before diagnosing anything.** data.gov.il answers the two failure classes completely differently, and conflating them sends an agent into the wrong fix:
  - **JSON with HTTP 409** and a `psycopg2` message = your SQL reached Postgres and Postgres rejected it (unknown column, bad syntax, unknown table). Read the message and fix the query.
  - **An HTML page with HTTP 404, about 1.4 kB** = the request never reached the SQL layer at all. This is the site's GENERIC error page and it has at least three distinct causes: a WAF-matched substring, an undefined action name, and a resource_id that does not exist. Do NOT assume it means the WAF. Disambiguate by re-running a known-good query (`SELECT * FROM "<rid>" LIMIT 1`) on the same resource: if that succeeds, the resource is fine and your SQL tripped the WAF; if it also returns HTML, the resource_id is dead or the action name is wrong.

**Tips:**
- Field names are often in Hebrew -- use `datastore_search` with `limit=1` first to see field names
- Use `filters` parameter with a JSON object for exact field matching (e.g., `filters={"city_code":"5000"}`)
- Use `q` parameter for full-text search across all fields
- Large datasets: use `limit` and `offset` for pagination
- Date fields may be in various formats -- check dataset documentation

**Pagination:**
- Page with `limit` + `offset`: the response returns `_links.next` (an offset-based next-page URL) you can follow, or you can increment `offset` yourself. Deep `offset` paging still works (large offsets return data, there is no hard cap), but the further you page the slower each request gets.
- data.gov.il's `filters` does exact matching only, so there is no `_id` keyset paging **through `filters`**: `filters={"_id":">N"}` returns `success:false` (an invalid query). Use offset paging, or `datastore_search_sql` with `WHERE _id > N ORDER BY _id`, which does give true keyset paging (see Step 3).
- For very large or full-table extractions, pass `records_format=csv`, or download the resource file from `resources[].url` in `package_show`. Note that the resource file is often **XLSX rather than CSV** (the mosdot resource is), so `records_format=csv` is the reliable CSV path; check `resources[].format` before assuming.
- The response `total` field is the count of all records in the resource (not in the page), so use it to plan how many pages you need.
- `records_format` accepts `objects` (default JSON), `lists` (positional arrays), `csv`, or `tsv`. `lists` and `csv` are noticeably faster and cheaper for large pulls; reach for them when streaming or bulk-extracting.

### Step 3b: Data-Layer Traps (read this before quoting any figure)

Step 3 gets you a 200 with rows. These are the ways those rows are still wrong. Every one was reproduced against the live API on 2026-08-27.

**Text columns are space-padded, and numeric-looking codes are stored as text.** In the CBS localities resource, `סמל_ישוב` has type `text` and its values carry a **trailing space**: `filters={"סמל_ישוב":"4000"}` returns `success:true` with `total:0`, while `"4000 "` returns Haifa. A zero-row success is the single most common silent wrong answer this API produces, because the agent reports "there is no data" and nothing looks broken. Always inspect the raw value with `limit=1` before equality-filtering a text field, then match the **exact padded string** through `filters` (`{"סמל_ישוב":"4000 "}` works), or fall back to `q=` full-text. You cannot TRIM your way out of this in SQL, for the reason in the next paragraph.


**The WAF also blocks SQL that references a HEBREW-named column in a predicate or a function.** This is the single most surprising constraint on the API and it decides which tool you reach for. Verified 2026-08-27:

| SQL | Result |
|---|---|
| `SELECT "שנה" FROM "<rid>" LIMIT 1` | 200, works |
| `... GROUP BY "שנה"` | 200, works |
| `... ORDER BY to_date("תאריך רישום עמותה",'DD/MM/YYYY') DESC` | 200, works, and is the correct fix for text dates |
| `... WHERE "שנה" = 2015` | HTML 404, blocked |
| `... WHERE TRIM("סמל_ישוב") = '4000'` | HTML 404, blocked |
| `... WHERE shnat_yitzur = 2016` (Latin column) | 200, works |
| `... WHERE _id > 100` | 200, works |

So the division of labour is: **filter Hebrew columns with `datastore_search`'s `filters`** (which handles Hebrew values fine, subject to the trailing-space rule above), and **use SQL for `_id` keyset paging, Latin-column predicates, `GROUP BY`, `sum(1)` and `to_date` ordering**. Do not try to TRIM a Hebrew column in SQL: match the exact padded string through `filters` instead.

**Joining on a locality NAME does not work without normalization.** The same city is spelled three ways across the two resources this skill tells you to join: localities has `'תל אביב - יפו '` (trailing space), mosdot has `'תל אביב - יפו'` in `שם ישוב` and `'תל אביב-יפו'` in `שם רשות`. A naive equality join drops every row. Pull both sides and normalize in your own code (strip, then collapse the spacing around the hyphen); the normalization cannot be pushed into the SQL, because a function on a Hebrew column is blocked.

**Some resources are multi-year panels, and their headline row count is not a count of things.** The mosdot resource holds one row per institution PER YEAR for **2011 to 2015 only**, so its 119,761 rows are five years of the same institutions and it contains nothing after 2015. Filter on `שנה` before counting anything, and never present the resource total as "the number of schools".

**Resource metadata freshness is not data freshness.** `resource_show` on mosdot reports a 2026 `last_modified`, describing when the FILE was republished, while the data inside ends in 2015. Derive the vintage from the data's own date column before quoting a figure to a user.

**Date columns are text, so `sort` on them is lexicographic and wrong.** In the amutot resource both `תאריך רישום עמותה` and `תאריך עדכון סטטוס` have type `text` in DD/MM/YYYY, so `sort=תאריך רישום עמותה desc` puts `31/12/2025` above any January 2026 row: it is sorting the day-of-month first. Formats also vary between columns of the same resource. For a real chronological order use SQL: `ORDER BY to_date("תאריך רישום עמותה",'DD/MM/YYYY') DESC` returns 26/08/2026 at the top, verified 2026-08-27. `to_date` in ORDER BY is allowed even on a Hebrew column; only predicates and TRIM are blocked.

**`records_format=csv` returns a HEADERLESS CSV string.** The column names live only in `result.fields`, in order. Prepend them yourself, or the Hebrew columns silently misalign.

**Check `datastore_active` before querying.** `package_show` / `resource_show` expose it per resource, and it is independent of `format`: the mosdot resource is `XLSX` and still `datastore_active:true`. A resource with `datastore_active:false` must be downloaded from `resources[].url` and parsed locally.

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

Resource IDs below were verified live on 2026-08-27 via `datastore_search?resource_id=<id>&limit=1`, checking the response BODY (a 200 with an empty `records` array means the resource is dead, whatever the status says). IDs on data.gov.il do change without notice. Always re-verify before quoting them to a user.

| Dataset | Resource ID | Description |
|---------|------------|-------------|
| Private and commercial vehicles (vehicle registration) | `053cea08-09bc-40ec-8f7a-156f0677aff3` | Full registry of private and commercial vehicle license plates with make, model, year. 4.17M rows. |
| Public-transport vehicles | `cf29862d-ca25-4691-84f6-1be60dcb4a1e` | Active license plates of public-transport vehicles (buses, taxis). 65,953 rows. |
| Education institutions (`mosdot`) | `5548fd63-5868-4053-ad81-98caddc5e232` | Characteristics of educational institutions supervised by the Ministry of Education. 119,761 rows. Resource format is XLSX. |
| Registered amutot (NGOs) | `be5b7935-3922-45d4-9638-08871b17ec95` | Ministry of Justice registry of associations / non-profits. 75,680 rows. |

For other domains, use `package_search` to discover the current dataset, then `package_show` to grab the active `resources[].id` -- those IDs rotate when datasets are re-published year over year.

**What is NOT on data.gov.il** (verified 2026-08-27; searching CKAN for these wastes the user's turn and invites an agent to invent a dataset):

| Data | Where it actually is | CKAN evidence |
|---|---|---|
| Real-estate transactions | `nadlan.gov.il` (its own API, not CKAN) | `q=nadlan` returns count 0; `fq=organization:taxes-authority` returns 4 datasets, all customs |
| Public-transport GTFS | `gtfs.mot.gov.il` (a static zip) | `q=gtfs` returns 2 unrelated datasets |
| Most CBS statistical series, including population by locality | `cbs.gov.il` | `fq=organization:lamas` returns 14 datasets, mostly road-accident PUFs plus the localities code list; none carries population |
| Monetary and financial series | `boi.org.il` | not published through CKAN |

The `lamas` organization on CKAN is a small slice of CBS output. Do not promise a user a CBS series without checking that specific series is on the portal.

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
4. The mosdot resource exposes the locality as a NAME field `שם ישוב` (city name text, e.g. `תל אביב - יפו`), not a numeric city code. Filter by the city name (or use `q=` full-text); Hebrew must be percent-encoded:
   ```
   # full-text search for Tel Aviv schools (q = "תל אביב", percent-encoded)
   curl -s "https://data.gov.il/api/3/action/datastore_search?resource_id=5548fd63-5868-4053-ad81-98caddc5e232&q=%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91&limit=100"
   ```
   The numeric CBS locality code (Tel Aviv-Yafo 5000, Haifa 4000, Jerusalem 3000) is the field `סמל_ישוב`, but it lives in the CBS localities dataset (resource `5c78e9fa-c2e2-4771-93ff-7f400a12f7ba`), not in the mosdot resource. Its values are **space-padded text**, so match on `TRIM(...)`, and normalize the city name before any join (see Step 3b).
5. **Pick a year, or the answer is five years of duplicates.** The mosdot resource is a per-year panel covering 2011 to 2015 only, so the unfiltered `q=תל אביב` result of 18,574 is not a school count. `שנה` is a Hebrew-named column, so filter it through `datastore_search`, NOT through SQL (a WHERE on a Hebrew column is WAF-blocked, see Step 3b):
   ```
   # schools in the 2015 slice, filtered by year through `filters`
   curl -s 'https://data.gov.il/api/3/action/datastore_search?resource_id=5548fd63-5868-4053-ad81-98caddc5e232&filters=%7B%22%D7%A9%D7%A0%D7%94%22%3A%222015%22%7D&limit=1'
   ```
   Read `total` from that response for the count. The per-year breakdown itself is a legal SQL query, because `GROUP BY` on a Hebrew column is allowed where `WHERE` is not:
   ```
   SELECT "שנה", sum(1) AS n FROM "5548fd63-5868-4053-ad81-98caddc5e232" GROUP BY "שנה"
   ```

Result: a school list for Tel Aviv for a NAMED year, presented with its 2015 vintage stated, not as a current figure.

### Example 2: A Request the Catalog Cannot Serve
User says: "Show me housing price trends in Haifa"

The right answer here is to STOP, not to keep searching. Real-estate transactions are not on data.gov.il: `q=nadlan` returns count 0, and the Tax Authority's four CKAN datasets are all customs (verified 2026-08-27).

Actions:
1. Run the discovery search once so the answer is evidence-based, not assumed.
2. On a zero or irrelevant count, say so plainly and redirect to `nadlan.gov.il`, which publishes transaction data through its own non-CKAN API.
3. Do NOT fall back to a plausible-looking dataset from a different organization, and do NOT synthesize figures.

Result: the user is sent to the source that actually has the data, in one turn instead of three. This example exists because the failure mode it prevents (searching, finding nothing, and inventing a dataset) is the most damaging thing an agent can do with this skill.

### Example 3: Municipal Data Comparison
User says: "Compare education spending across Israeli cities"

Actions:
1. `package_search?q=%D7%AA%D7%A7%D7%A6%D7%99%D7%91%20%D7%97%D7%99%D7%A0%D7%95%D7%9A` (budget + education in Hebrew, percent-encoded).
2. Pick a municipal-budget dataset, `package_show` to retrieve the active resource id.
3. `datastore_search` filtered to education-category rows; page with `offset` (or download the resource CSV) for large resources.
4. To normalize per capita you need population, which is **not** on CKAN (`fq=organization:lamas` carries no population table). Take it from `cbs.gov.il` and say where it came from, or present absolute figures and state that no per-capita normalization was applied.

Result: Ranked comparison of education spending per student across major Israeli municipalities with data source and year.

## Bundled Resources

### Scripts
- `scripts/query_datagov.py` -- Search datasets, inspect resources, and query the data.gov.il CKAN API from the command line. Subcommands: `search`, `dataset`, `query`, `sql`, `orgs`. `query` takes `--filters/--fields/--sort/-q/--offset/--records-format`; `sql` reaches `datastore_search_sql` for keyset paging and aggregation; both take `--json` for machine-readable output you can chain. Run: `python scripts/query_datagov.py --help`

### References
- `references/ckan-api-reference.md` -- Complete endpoint catalog for the data.gov.il CKAN API including search parameters, datastore query syntax, and common organization IDs. Consult when constructing API calls or debugging query syntax.

## Recommended MCP Servers

Pair this skill with an MCP server so your agent can call data.gov.il (or a derived dataset) directly as tools, without scripting HTTP calls.

| MCP | URL | What it gives you |
|-----|-----|-------------------|
| `datagov-israel` | https://agentskills.co.il/he/mcp/datagov-israel | Direct MCP tool access to the data.gov.il CKAN API (search, package_show, datastore_search). |
| `data-gov-il` | https://agentskills.co.il/he/mcp/data-gov-il | Alternative MCP wrapping the same data.gov.il CKAN API. |
| `israel-vehicles` | https://agentskills.co.il/he/mcp/israel-vehicles | Pre-scoped MCP for the vehicle registration dataset (license-plate lookup, make/model/year). |
| `israel-amutot` | https://agentskills.co.il/he/mcp/israel-amutot | Pre-scoped MCP for the Ministry of Justice amutot (NGO) registry. |
| `israel-elections` | https://agentskills.co.il/he/mcp/israel-elections | Pre-scoped MCP for Israeli election results data. |

When this skill walks the user through a query, prefer the dedicated MCP if it's installed; fall back to the raw CKAN API otherwise.

## Gotchas
- Israeli government data APIs (data.gov.il) frequently change URLs and endpoint structures without notice. Agents may hardcode endpoints that worked last month but now return 404. Re-verify resource IDs with `package_show` before quoting them.
- The data.gov.il API returns data with Hebrew column headers by default. Agents may fail to parse responses that contain non-ASCII header names in JSON or CSV output.
- Hebrew filter values and `q` parameters must be UTF-8 percent-encoded. Raw Hebrew in URLs breaks several HTTP clients (some `curl` builds, older `requests` versions, certain proxies). Example: search for "רכב" as `q=%D7%A8%D7%9B%D7%91`; filter on "חיפה" as `filters=%7B%22city%22%3A%22%D7%97%D7%99%D7%A4%D7%94%22%7D`.
- Rate limiting is undocumented, and its severity is easy to overstate. **Verified 2026-08-27: 25 rapid sequential `datastore_search` calls in 6.5 seconds all returned 200, and roughly 60 calls across a session drew no throttling at all.** Treat a modest delay as courtesy rather than as a documented requirement, and do not tell a user their problem is rate limiting without evidence; the block people actually hit is the SQL-pattern WAF below.
- The data.gov.il WAF blocks SQL that matches an injection signature (`count(`, `1=1`, `UNION` were all confirmed on 2026-08-27) and answers with an **HTML 404 page of about 1.4 kB**, not JSON and not a 403. Rephrasing the query fixes it immediately; backing off does not, because nothing is throttled. A 403 with the body `Security Violation` was observed in June 2026 but could NOT be reproduced on 2026-08-27; if you do see one, treat it as a session-level block (drop cookies, fresh `User-Agent`, exponential backoff) rather than a query problem.
- Many government datasets have date fields in DD/MM/YYYY format (Israeli convention), not ISO 8601. Agents may parse "01/02/2026" as February 1st instead of January 2nd.
- Deep offset paging gets progressively slower on large datasets (verified 2026-08-27: `offset=500000` still returns 200, so there is no hard cap, but big offsets are expensive). `filters` cannot do keyset paging (`{"_id":">N"}` fails with `success:false`), but `datastore_search_sql` with `WHERE _id > N ORDER BY _id` can, and it is the right tool for a full extraction.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| data.gov.il portal | https://data.gov.il | Browse Israeli open data catalog, organizations, datasets |
| CKAN API reference | https://docs.ckan.org/en/latest/api/ | `package_search`, `package_show`, `datastore_search` signatures |
| data.gov.il dataset list | https://data.gov.il/datasets | Discover available datasets by organization and tag. Note the plural: `/dataset` serves a client-side 404 page |
| Central Bureau of Statistics | https://www.cbs.gov.il | Upstream source for many data.gov.il statistics |
| Bank of Israel data | https://www.boi.org.il | Financial and monetary datasets not on data.gov.il |

## Troubleshooting

### `package_search` returns `count: 0`
Cause: search terms too specific, or in the wrong language, or the data is genuinely not on this portal.
Solution: retry with broader Hebrew keywords (the catalog is primarily Hebrew), then with `fq=organization:<id>`. If still zero, check the "What is NOT on data.gov.il" table in Step 2 before concluding anything: a zero count for real-estate, GTFS or most CBS series is the correct and final answer, and the right move is to redirect the user, not to substitute a different dataset.

### JSON with HTTP 409 and a Hebrew `Validation Error`
Cause: the request reached CKAN and CKAN rejected the arguments. A missing `resource_id`, for example, returns `{"error":{"resource_id":["ערך חסר"],"__type":"Validation Error"},"success":false}` with HTTP 409. The message is in Hebrew.
Solution: read `error` rather than the status. This is a caller bug, not an outage.

### The resource has no queryable datastore
Cause: `datastore_active` is false for that resource. It is independent of `format`: an XLSX resource can be datastore-active (mosdot is), and a CSV one may not be.
Solution: read `resources[].datastore_active` from `package_show` or `resource_show` BEFORE calling `datastore_search`. If false, download `resources[].url` and parse locally.

### Error: an HTML page instead of JSON from `datastore_search_sql`
Cause (verified 2026-08-27): the request never reached the SQL layer. The 1,376-byte HTML 404 is the site's GENERIC error page, shared by three causes: the WAF matched an injection-signature substring in your SQL (`count(`, `1=1` and `UNION` all trigger it), OR the action name does not exist, OR the resource_id does not exist. A client that only inspects `success` sees a parse failure in all three cases.
Solution: disambiguate first. Re-run `SELECT * FROM "<resource_id>" LIMIT 1`. If that succeeds, your SQL tripped the WAF: replace `count(*)` with `sum(1)`, take plain row counts from `datastore_search`'s `total`, and avoid `UNION` and tautologies. If it also returns HTML, the resource_id is dead (re-resolve it with `package_show`) or the action name is wrong. The SQL endpoint itself is NOT disabled: plain `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY` and `sum()` all return 200 with data.
Verified NOT to be the cause: rate limiting (25 rapid calls in 6.5s all returned 200), and a genuine SQL error, which returns **JSON with HTTP 409** and a `psycopg2` message rather than HTML.

### Error: `Connection error: [SSL: CERTIFICATE_VERIFY_FAILED]` from the bundled script
Cause: a python.org build on macOS ships without a populated CA store, so `urllib` cannot verify data.gov.il's certificate. This is a local trust-store problem, not a data.gov.il fault; `curl` on the same machine succeeds.
Solution: the script now prefers `certifi`'s bundle when it is installed (`pip install certifi`). Otherwise run `/Applications/Python\ 3.x/Install\ Certificates.command` once, or set `SSL_CERT_FILE=$(python3 -c 'import certifi; print(certifi.where())')`.

### `success:true` with `total: 0`, and the data plainly exists
Cause (verified 2026-08-27): almost always a space-padded text column. `filters={"סמל_ישוב":"4000"}` on the CBS localities resource returns zero rows because the stored value is `"4000 "`. Numeric-looking codes are stored as `text`, so `"4000"` and `4000` are also different.
Solution: inspect the raw value with `limit=1` first, then either match the exact padded string or use `datastore_search_sql` with `WHERE TRIM("col") = 'value'`. See Step 3b.

### Hebrew field names
Not an error. Most datasets have Hebrew column names, sometimes with a space (`שם ישוב`) and sometimes an underscore (`שם_ישוב`) in different resources. Query with `limit=1` first to read the exact field names, and percent-encode them in URLs.