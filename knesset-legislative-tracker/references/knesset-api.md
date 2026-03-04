# Knesset Open Data API Reference

## Base URL

```
https://main.knesset.gov.il/Activity/Info/api/v2
```

The API follows OData v4 conventions and returns JSON by default.

## Entity Types

### Bills (Hatza'ot Chok)

**Endpoint:** `/api/v2/bills`

| Field | Type | Description |
|-------|------|-------------|
| ID | int | Unique bill identifier |
| Name | string | Bill name (Hebrew) |
| KnessetNum | int | Knesset term number |
| StatusTypeDesc | string | Current status description |
| SubTypeDesc | string | Bill subtype |
| InitiatorFirstName | string | Proposing MK first name |
| InitiatorLastName | string | Proposing MK last name |
| LastUpdatedDate | datetime | Last status update |
| PublicationDate | datetime | Publication date |

**Status Values:**
| Status | Hebrew | Meaning |
|--------|--------|---------|
| Proposed | הוצעה | Initial submission |
| PreVote | הצבעה מוקדמת | Preliminary vote pending |
| InCommittee | בוועדה | Under committee review |
| FirstReading | קריאה ראשונה | First reading vote |
| PrepSecondReading | הכנה לקריאה שנייה | Committee preparation for final vote |
| SecondThirdReading | קריאה שנייה ושלישית | Final vote |
| Approved | אושרה | Enacted into law |
| Rejected | נדחתה | Defeated |

### Members (Chavrei Knesset)

**Endpoint:** `/api/v2/members`

| Field | Type | Description |
|-------|------|-------------|
| ID | int | Unique member identifier |
| FirstName | string | First name (Hebrew) |
| LastName | string | Last name (Hebrew) |
| FactionName | string | Party/faction name |
| IsCurrent | boolean | Currently serving |
| KnessetNum | int | Knesset term |
| Email | string | Contact email |

### Committees (Vaadot)

**Endpoint:** `/api/v2/committees`

| Field | Type | Description |
|-------|------|-------------|
| ID | int | Session identifier |
| TypeDesc | string | Committee name |
| StartDate | datetime | Session start time |
| FinishDate | datetime | Session end time |
| KnessetNum | int | Knesset term |
| Location | string | Meeting location |

### Votes (Hatzbao't)

**Endpoint:** `/api/v2/votes`

| Field | Type | Description |
|-------|------|-------------|
| ID | int | Vote identifier |
| BillID | int | Associated bill |
| SessionID | int | Plenum session |
| Date | datetime | Vote date |
| For | int | Votes in favor |
| Against | int | Votes against |
| Abstaining | int | Abstentions |
| Result | string | Vote result |

## OData Query Options

The API supports standard OData query parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| $filter | Filter results | `$filter=KnessetNum eq 25` |
| $select | Choose fields | `$select=Name,StatusTypeDesc` |
| $top | Limit results | `$top=10` |
| $skip | Skip records (pagination) | `$skip=20` |
| $orderby | Sort results | `$orderby=LastUpdatedDate desc` |
| $count | Include total count | `$count=true` |

### Filter Functions

| Function | Example | Description |
|----------|---------|-------------|
| contains | `contains(Name,'פרטיות')` | Substring match |
| startswith | `startswith(Name,'חוק')` | Prefix match |
| endswith | `endswith(Name,'2024')` | Suffix match |
| eq | `KnessetNum eq 25` | Exact match |
| ne | `StatusTypeDesc ne 'נדחתה'` | Not equal |
| gt / ge | `LastUpdatedDate ge 2024-01-01T00:00:00Z` | Greater than / equal |
| lt / le | `KnessetNum le 24` | Less than / equal |
| and / or | `IsCurrent eq true and contains(FactionName,'ליכוד')` | Logical operators |

## Common Query Patterns

### Recent bills on a topic
```
/api/v2/bills?$filter=contains(Name,'סייבר') and LastUpdatedDate ge 2024-01-01T00:00:00Z&$orderby=LastUpdatedDate desc&$top=10
```

### Current MKs from a specific party
```
/api/v2/members?$filter=IsCurrent eq true and contains(FactionName,'יש עתיד')
```

### Committee sessions this month
```
/api/v2/committees?$filter=StartDate ge 2024-03-01T00:00:00Z&$orderby=StartDate desc
```

### Approved bills in current Knesset
```
/api/v2/bills?$filter=KnessetNum eq 25 and StatusTypeDesc eq 'אושרה'&$orderby=LastUpdatedDate desc
```

## Knesset Terms

| Knesset | Years | Notes |
|---------|-------|-------|
| 18th | 2009-2013 | Earliest with reliable API data |
| 19th | 2013-2015 | |
| 20th | 2015-2019 | |
| 21st | 2019 | Short term |
| 22nd | 2019-2020 | Short term |
| 23rd | 2020-2021 | |
| 24th | 2021-2022 | |
| 25th | 2022-present | Current |

## Rate Limiting and Best Practices

- No official rate limit documented, but add 1-second delays between requests
- Use `$top` and `$skip` for pagination (default page size varies)
- Cache results when possible to reduce API load
- Bill names are in formal legal Hebrew; try multiple keyword variants
- The API may return partial data for older Knesset terms
