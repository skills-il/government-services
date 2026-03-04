---
name: knesset-legislative-tracker
description: >-
  Track Israeli Knesset legislation, bills, and committee activity via the
  Knesset Open Data API. Use when user asks about "Hatza'ot Chok" (bill
  proposals), Knesset votes, MK (Member of Knesset) voting records, committee
  sessions ("vaadot"), or legislative status of specific bills. Monitors
  tech-sector legislation including privacy law amendments, cyber regulations,
  and labor law changes. Supports bill tracking through readings, committee vote
  analysis, and MK activity lookups. Do NOT use for historical Knesset data
  before the 18th Knesset or classified security committee proceedings.
license: MIT
allowed-tools: 'Bash(python:*) Bash(pip:*) WebFetch'
compatibility: >-
  Requires network access to the Knesset Open Data API
  (main.knesset.gov.il). Python 3.9+ for helper scripts.
metadata:
  author: skills-il
  version: 1.0.0
  category: government-services
  tags:
    he:
      - כנסת
      - חקיקה
      - הצעות-חוק
      - ועדות
      - הצבעות
      - ישראל
    en:
      - knesset
      - legislation
      - bills
      - committees
      - votes
      - israel
  display_name:
    he: מעקב חקיקה בכנסת
    en: Knesset Legislative Tracker
  display_description:
    he: >-
      מעקב אחר חקיקה, הצעות חוק ופעילות ועדות בכנסת באמצעות ה-API הפתוח של
      הכנסת. תומך בחיפוש הצעות חוק, ניתוח הצבעות ומעקב אחר חברי כנסת.
    en: >-
      Track Israeli Knesset legislation, bills, and committee activity via the
      Knesset Open Data API. Use when user asks about bill proposals, Knesset
      votes, MK voting records, committee sessions, or legislative status.
      Monitors tech-sector legislation including privacy and cyber regulations.
      Do NOT use for pre-18th Knesset data or classified proceedings.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# Knesset Legislative Tracker

## Instructions

### Step 1: Identify the Legislative Query

Ask the user what they want to track:

| Query Type | API Endpoint | Hebrew Term |
|-----------|-------------|-------------|
| Bill search | /api/v2/bills | Hatza'at Chok / הצעת חוק |
| Bill status | /api/v2/bills/{id} | Matsav Hatza'a / מצב הצעה |
| Committee sessions | /api/v2/committees | Vaada / ועדה |
| MK information | /api/v2/members | Chaver Knesset / חבר כנסת |
| Votes | /api/v2/votes | Hatzbaa / הצבעה |
| Knesset sessions | /api/v2/plenum | Moshav Meli'a / מושב מליאה |

Clarify:
- **What topic?** (specific bill, policy area, MK activity)
- **What Knesset term?** (current or specific historical term from 18th onward)
- **What output?** (status update, vote breakdown, timeline, trend analysis)

### Step 2: Query the Knesset Open Data API

Base URL: `https://main.knesset.gov.il/Activity/Info/`

The Knesset provides an OData-compatible REST API:

**Search bills by keyword:**
```
GET https://main.knesset.gov.il/Activity/Info/api/v2/bills?$filter=contains(Name,'KEYWORD')&$top=20
```

**Get bill details:**
```
GET https://main.knesset.gov.il/Activity/Info/api/v2/bills(BILL_ID)
```

**List committee sessions:**
```
GET https://main.knesset.gov.il/Activity/Info/api/v2/committees?$filter=TypeDesc eq 'COMMITTEE_NAME'
```

**Get MK voting record:**
```
GET https://main.knesset.gov.il/Activity/Info/api/v2/members(MEMBER_ID)/votes
```

**Filter by date range:**
```
GET https://main.knesset.gov.il/Activity/Info/api/v2/bills?$filter=LastUpdatedDate ge 2024-01-01T00:00:00Z
```

**Tips:**
- Use OData `$filter`, `$select`, `$top`, `$skip`, `$orderby` for queries
- Bill names are in Hebrew -- search with Hebrew keywords
- API returns JSON by default
- Pagination: use `$top` and `$skip` for large result sets

### Step 3: Track Bill Progress Through Readings

Israeli legislation follows a defined process:

| Stage | Hebrew | API Status | Description |
|-------|--------|-----------|-------------|
| Proposal | הצעה | Proposed | Initial bill text submitted |
| Pre-vote | הצבעה מוקדמת | PreVote | Preliminary Knesset vote |
| Committee | ועדה | InCommittee | Committee review and amendments |
| First reading | קריאה ראשונה | FirstReading | Full Knesset vote on principles |
| Committee prep | הכנה לקריאה שנייה | PrepSecondReading | Final committee amendments |
| Second and third reading | קריאה שנייה ושלישית | SecondThirdReading | Final vote, becomes law |
| Passed | אושר | Approved | Enacted as law |
| Rejected | נדחה | Rejected | Bill defeated |

**Track a specific bill through stages:**
```python
import requests

bill_id = 12345
url = f"https://main.knesset.gov.il/Activity/Info/api/v2/bills({bill_id})"
response = requests.get(url)
bill = response.json()

print(f"Bill: {bill.get('Name')}")
print(f"Status: {bill.get('StatusTypeDesc')}")
print(f"Last updated: {bill.get('LastUpdatedDate')}")
print(f"Proposers: {bill.get('InitiatorFirstName')} {bill.get('InitiatorLastName')}")
```

### Step 4: Monitor Committee Activity

Knesset committees (vaadot) handle detailed legislative review:

| Committee | Hebrew | Key Topics |
|-----------|--------|------------|
| Finance | ועדת הכספים | Budget, taxes, banking |
| Constitution, Law and Justice | ועדת חוקה, חוק ומשפט | Basic laws, civil rights, courts |
| Science and Technology | ועדת המדע והטכנולוגיה | Tech regulation, innovation, cyber |
| Economics | ועדת הכלכלה | Business regulation, competition |
| Labor and Welfare | ועדת העבודה והרווחה | Employment law, social benefits |
| Education | ועדת החינוך | Schools, higher education |
| Internal Affairs | ועדת הפנים | Local government, planning |

**Query committee sessions:**
```
GET https://main.knesset.gov.il/Activity/Info/api/v2/committees?$filter=KnessetNum eq 25&$orderby=StartDate desc&$top=10
```

### Step 5: Analyze MK Voting Records

Look up MK activity and voting patterns:

**Get MK list for current Knesset:**
```
GET https://main.knesset.gov.il/Activity/Info/api/v2/members?$filter=IsCurrent eq true
```

**Get specific MK details:**
```
GET https://main.knesset.gov.il/Activity/Info/api/v2/members(MEMBER_ID)
```

**Analyze voting patterns:**
1. Retrieve vote list for a bill or session
2. Cross-reference with party affiliation
3. Identify coalition vs. opposition voting patterns
4. Track absence rates and abstentions

**Party (Siya) affiliations:**
| Party | Hebrew | Coalition/Opposition |
|-------|--------|---------------------|
| Likud | ליכוד | Changes per term |
| Yesh Atid | יש עתיד | Changes per term |
| Shas | ש"ס | Changes per term |
| United Torah Judaism | יהדות התורה | Changes per term |
| National Unity | האחדות הלאומית | Changes per term |

### Step 6: Tech-Sector Legislation Alerts

Monitor legislation relevant to the tech industry:

**Key search terms for tech legislation:**
| Topic | Hebrew Keywords | English Keywords |
|-------|----------------|-----------------|
| Privacy/Data protection | הגנת פרטיות, מידע אישי | privacy, personal data |
| Cybersecurity | סייבר, אבטחת מידע | cyber, information security |
| AI regulation | בינה מלאכותית, AI | artificial intelligence |
| Labor/remote work | עבודה מרחוק, דיני עבודה | remote work, labor law |
| Intellectual property | קניין רוחני, פטנטים | IP, patents |
| Tax incentives | הטבות מס, אנגל | tax benefits, angel law |
| Fintech | פינטק, שירותים פיננסיים | fintech, financial services |

**Example: find recent tech-related bills:**
```python
import requests

keywords = ["סייבר", "פרטיות", "בינה מלאכותית", "טכנולוגיה"]
for kw in keywords:
    url = f"https://main.knesset.gov.il/Activity/Info/api/v2/bills"
    params = {"$filter": f"contains(Name,'{kw}')", "$top": 5, "$orderby": "LastUpdatedDate desc"}
    resp = requests.get(url, params=params)
    bills = resp.json().get("value", [])
    for bill in bills:
        print(f"[{bill['StatusTypeDesc']}] {bill['Name']}")
```

### Step 7: Present Findings

Format results for the user:
1. **Bill summary**: name, proposer(s), current status, next expected action
2. **Timeline**: key dates from proposal through current stage
3. **Vote breakdown**: for/against/abstain counts with party breakdown
4. **Committee notes**: relevant discussion points and amendments
5. **Impact assessment**: brief analysis of what the bill means for the user's domain

## Examples

### Example 1: Track a Specific Bill
User says: "What's the status of the privacy protection bill?"
Actions:
1. Search bills: `$filter=contains(Name,'הגנת פרטיות')`
2. Get latest matching bill details
3. Check current stage (committee, reading, etc.)
4. List proposing MKs and party affiliation
Result: Bill status with timeline and next expected action

### Example 2: MK Voting Record Analysis
User says: "How did MK X vote on tech-related bills this session?"
Actions:
1. Find MK by name in members API
2. Retrieve voting record for current Knesset term
3. Filter votes on tech-related bills (cyber, privacy, AI keywords)
4. Calculate voting pattern statistics
Result: Summary table of votes with for/against breakdown

### Example 3: Committee Session Monitoring
User says: "What did the Science and Technology committee discuss last month?"
Actions:
1. Query committees API filtered by Science and Technology
2. Filter sessions by date range (last 30 days)
3. Retrieve session agendas and discussed bills
4. Summarize key topics and decisions
Result: List of sessions with agenda items and outcomes

### Example 4: Tech Legislation Alert
User says: "Are there any new bills about AI regulation?"
Actions:
1. Search bills with keywords: "בינה מלאכותית", "AI", "אלגוריתם"
2. Filter by recent proposals (last 90 days)
3. Check status of each matching bill
4. Identify committee assignments and upcoming votes
Result: List of active AI-related bills with status and proposers

## Bundled Resources

### Scripts
- `scripts/fetch_knesset.py` -- Query the Knesset Open Data API for bills, votes, MK information, and committee sessions. Supports subcommands: `bills`, `bill`, `members`, `committees`, `votes`, `tech-alerts`. Run: `python scripts/fetch_knesset.py --help`

### References
- `references/knesset-api.md` -- Complete endpoint documentation for the Knesset Open Data API including OData query syntax, entity types, status codes, and common query patterns. Consult when constructing API calls.

## Troubleshooting

### Error: "No results returned"
Cause: Search terms may not match Hebrew bill names exactly
Solution: Try broader Hebrew keywords. Bill names use formal legal Hebrew which may differ from colloquial terms.

### Error: "API rate limit exceeded"
Cause: Too many requests in a short period
Solution: Add 1-second delays between API calls. Use `$top` and `$skip` for pagination instead of fetching all records.

### Error: "Member not found"
Cause: MK name spelling may vary between Hebrew and transliteration
Solution: Search by partial name or use the members list endpoint to find the correct ID first.

### Error: "Vote data unavailable"
Cause: Not all votes have detailed per-MK breakdowns in the API
Solution: Check the Knesset website directly for the specific plenum session vote record.
