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
- `limit` -- Maximum records (default 100, hard ceiling around 32,000 via `offset` paging)
- `offset` -- Record offset (use cursor paging on `_id` for datasets larger than ~32k records)
- `fields` -- Comma-separated field names
- `filters` -- JSON object of field:value pairs
- `q` -- Full-text search within resource
- `sort` -- Sort field and order (use `sort=_id asc` for cursor paging)
- `records_format` -- One of `objects` (default), `lists`, `csv`, `tsv`. `lists` and `csv` are noticeably faster for large pulls.

### Deprecated Endpoints
| Endpoint | Status | Notes |
|----------|--------|-------|
| `/action/datastore_search_sql` | 403 Forbidden | SQL queries disabled by data.gov.il. Use `datastore_search` with `filters`, `fields`, `sort`, and `q` parameters instead. |

## Common Organization IDs

Verified against `organization_show?id=<id>` on 2026-05-13. Stale aliases like `cbs`, `mot`, `moh`, `moe`, `ita` return 404 and must not be used.

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
Undocumented and enforced by a WAF. A "Security Violation" / 403 response is distinct from a permissions 403: the WAF terminates the session and discards cookies. Recover by backing off exponentially, dropping any session cookies, and retrying with a fresh `User-Agent`. Implement reasonable delays (1-2 seconds) for bulk queries.
