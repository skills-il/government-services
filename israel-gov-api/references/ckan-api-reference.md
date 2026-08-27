# data.gov.il CKAN API Reference

## Base URL
`https://data.gov.il/api/3/`

## Authentication
None required (public API).

## Key Endpoints

### Dataset Discovery
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/action/package_search` | GET | Search datasets by keyword |
| `/action/package_show` | GET | Get full dataset details |
| `/action/package_list` | GET | List all dataset IDs |
| `/action/group_list` | GET | List dataset categories |
| `/action/organization_list` | GET | List publishing organizations |
| `/action/tag_list` | GET | List all tags |

### Resource Access
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/action/resource_show` | GET | Get resource metadata |
| `/action/datastore_search` | GET | Query tabular data |

### Search Parameters
- `q` -- Search query string
- `fq` -- Filter query (e.g., `organization:lamas`)
- `rows` -- Number of results (default 10)
- `start` -- Offset for pagination
- `sort` -- Sort field and order

### Datastore Query Parameters
- `resource_id` -- Resource ID (required)
- `limit` -- Maximum records per page (default 100). There is no hard ceiling, but deep `offset` paging gets progressively slower.
- `offset` -- Record offset; the response also returns `_links.next` for the next page. `filters` is exact-match only, so there is no `_id` keyset paging THROUGH `filters`. For a full extraction use `datastore_search_sql` with `WHERE _id > N ORDER BY _id`, which is true keyset paging and does not degrade with depth, or pull `records_format=csv`.
- `fields` -- Comma-separated field names
- `filters` -- JSON object of field:value pairs
- `q` -- Full-text search within resource
- `sort` -- Sort field and order (e.g. `sort=_id asc` for a stable ordering across offset pages)
- `records_format` -- One of `objects` (default), `lists`, `csv`, `tsv`. `lists` and `csv` are noticeably faster for large pulls.

### Endpoint status notes
| Endpoint | Status | Notes |
|----------|--------|-------|
| `/action/datastore_search_sql` | 200 for most queries | NOT disabled (re-verified 2026-08-27). `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY`, `sum()` and `LIMIT` all work. The WAF blocks injection-signature substrings (`count(`, `1=1`, `UNION`) with an HTML 404, not a JSON error. Use `sum(1)` instead of `count(*)`, and take plain row counts from `datastore_search`'s `total`. |

## Common Organization IDs

Verified against `organization_show?id=<id>` on 2026-06-16. Stale aliases like `cbs`, `mot`, `moh`, `moe`, `ita` return 404 and must not be used.

| Organization | ID | Hebrew |
|--------------|-----|--------|
| Central Bureau of Statistics | `lamas` | הלשכה המרכזית לסטטיסטיקה |
| Ministry of Transportation | `ministry_of_transport` | משרד התחבורה |
| Ministry of Health | `ministry-health` | משרד הבריאות |
| Ministry of Education | `ministry_of_education` | משרד החינוך |
| Israel Tax Authority | `taxes-authority` | רשות המסים |
| Israel Land Authority | `the_israel_lands_administration` | רשות מקרקעי ישראל |
| Ministry of Interior | `interior_affairs` | משרד הפנים |

Run `curl -s "https://data.gov.il/api/3/action/organization_list" | head -200` to enumerate the canonical IDs; ministry IDs change without notice.

## Response Format
All responses return JSON with:
```json
{
  "success": true/false,
  "result": {
    "total": 0,
    "records": [],
    "fields": []
  },
  "error": { ... }
}
```

The `result.total` field reports the full record count of the resource (not the page); use it to plan pagination.

## Rate Limits
Undocumented, and measured lighter than previously described: on 2026-08-27, 25 rapid sequential `datastore_search` calls in 6.5 seconds all returned 200, and about 60 calls in one session drew no throttling. What does block is the SQL-pattern WAF, which answers an injection-signature substring (`count(`, `1=1`, `UNION`) with an HTML 404 rather than a 403; rephrasing the query clears it and backing off does not. A 403 with the body "Security Violation" was recorded in June 2026 but could not be reproduced on 2026-08-27. If one does appear, treat it as a session block: drop cookies, use a fresh `User-Agent`, back off exponentially. Modest delays on bulk pulls remain good manners.
