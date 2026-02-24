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
| `/action/datastore_search_sql` | GET | SQL queries on tabular data |

### Search Parameters
- `q` -- Search query string
- `fq` -- Filter query (e.g., `organization:cbs`)
- `rows` -- Number of results (default 10)
- `start` -- Offset for pagination
- `sort` -- Sort field and order

### Datastore Query Parameters
- `resource_id` -- Resource ID (required)
- `limit` -- Maximum records (default 100)
- `offset` -- Record offset
- `fields` -- Comma-separated field names
- `filters` -- JSON object of field:value pairs
- `q` -- Full-text search within resource
- `sort` -- Sort field and order

### SQL Query Syntax
```
SELECT field1, field2 FROM "resource_id" WHERE field1 = 'value' ORDER BY field2 LIMIT 100
```
Supports: SELECT, WHERE, ORDER BY, LIMIT, GROUP BY, COUNT, SUM, AVG

## Common Organization IDs
- `cbs` -- Central Bureau of Statistics
- `mot` -- Ministry of Transportation
- `moh` -- Ministry of Health
- `moe` -- Ministry of Education
- `ita` -- Israel Tax Authority

## Response Format
All responses return JSON with:
```json
{
  "success": true/false,
  "result": { ... },
  "error": { ... }
}
```

## Rate Limits
Undocumented but generous for public use. Implement reasonable delays for bulk queries.
