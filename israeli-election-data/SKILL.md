---
name: israeli-election-data
description: Access Israeli election and political data from the Knesset API and Central Elections Committee. Use when user asks about Knesset, Israeli elections, MK (Member of Knesset) information, Israeli voting records, legislative bills in Israel, Knesset committees, Israeli political parties, coalition data, or election results by locality. Covers Knesset OData API, election commission data, and Israeli political system structure. Do NOT use for non-Israeli elections or political opinion/prediction.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Requires network access for Knesset API. No API keys needed (public data). Data primarily in Hebrew.
---

# Israeli Election Data

## Instructions

### Step 1: Identify Data Need

| Data Type | Source | API |
|-----------|--------|-----|
| MK information | Knesset API | KNS_Person, KNS_MkSiteCode |
| Voting records | Knesset API | Note: Vote data is not available through the public OData API |
| Bills / legislation | Knesset API | KNS_Bill, KNS_BillInitiator |
| Committee sessions | Knesset API | KNS_CmtSessionItem |
| Election results | Elections Committee | votes.gov.il |
| Party information | Knesset API | KNS_Faction |

### Step 2: Query Knesset API

**Base URL:** `https://www.knesset.gov.il/Odata/ParliamentInfo.svc/`

**Query pattern:**
```
GET {BASE_URL}/{ENTITY}?$format=json&$filter={FILTER}&$top={LIMIT}&$select={FIELDS}
```

**Get all MKs for current Knesset (25th):**
```
GET .../KNS_PersonToPosition?$format=json&$filter=KnessetNum eq 25 and (PositionID eq 43 or PositionID eq 61)&$top=120
```

**Search MK by name:**
```
GET .../KNS_Person?$format=json&$filter=substringof('name', LastName)&$top=10
```

### Step 3: Access Voting Data

**Note:** Vote data is not available through the public OData API. The entities KNS_VoteMain and KNS_VoteDetail do NOT exist in the public Knesset OData service. For voting data, consult the Knesset website directly or check if alternative data sources are available.

### Step 4: Track Legislation

**Search bills:**
```
GET .../KNS_Bill?$format=json&$filter=KnessetNum eq 25 and substringof('keyword', Name)&$top=50
```

**Bill status codes:**
- 108 = Preparation for first reading
- 118 = Approved in third reading (became law)
- 120 = For plenum discussion on continuity law application

**Legislative process stages:**
1. Bill Draft, Private member or Government bill
2. Preliminary Reading, Private bills only, plenum vote
3. Committee Review, Assigned to relevant committee
4. First Reading, Plenum vote on bill principles
5. Committee Preparation, Detailed clause-by-clause review
6. Second Reading, Clause-by-clause plenum vote
7. Third Reading, Final vote on entire bill
8. Publication, Published in official gazette (Reshumot), becomes law

### Step 5: Election Results
Access election data from Central Elections Committee (votes.gov.il):
- Final results by ballot location (~12,000 stations)
- Party lists and candidates
- Voter turnout by locality
- Historical data for all 25 Knesset elections since 1949

**Electoral system facts:**
- 120 seats, proportional representation
- 3.25% electoral threshold
- Modified D'Hondt method (Bader-Ofer) for seat allocation
- Surplus vote agreements between parties

### Step 6: Party and Coalition Data

**Get factions in a Knesset session:**
```
GET .../KNS_Faction?$format=json&$filter=KnessetNum eq 25
```

**Israeli political terminology:**
| Hebrew | English | Meaning |
|--------|---------|---------|
| knesset | Knesset | Parliament |
| chaver knesset | MK | Member of Knesset |
| siaa | Faction | Political party/bloc in Knesset |
| koalitzia | Coalition | Governing alliance |
| opozitzia | Opposition | Non-governing parties |
| hatzaat chok | Bill | Legislative proposal |
| chok yesod | Basic Law | Constitutional law |
| vaada | Committee | Knesset committee |
| mliaa | Plenum | Full Knesset session |
| hatzbaa | Vote | Parliamentary vote |

## Examples

### Example 1: MK Lookup
User says: "Tell me about MK [name]"
Actions:
1. Search KNS_Person for MK by name
2. Get PersonID, then query KNS_PersonToPosition for roles
3. Look up faction via KNS_Faction
4. Present MK profile with party affiliation and positions held
Result: MK profile with political background. Note: per-MK voting data is not available via the public OData API.

### Example 2: Bill Tracking
User says: "What happened to the bill about [topic]?"
Actions:
1. Search KNS_Bill with keyword
2. Get bill status and current stage
3. Find sponsors via KNS_BillInitiator
4. Check committee assignments and readings
Result: Bill status with full legislative history.

### Example 3: Election Analysis
User says: "Show me election results for Haifa in the last election"
Actions:
1. Access Central Elections Committee data for 25th Knesset
2. Filter by Haifa ballot locations
3. Aggregate results by party
4. Compare to national results
Result: Haifa-specific election breakdown with party results.

## Bundled Resources

### Scripts
- `scripts/query_knesset.py` — Query the Knesset OData API to list MKs by Knesset session, search MKs by name, retrieve plenum voting records with for/against/abstain breakdowns, search legislative bills by keyword, and list political factions. Supports subcommands: `mks`, `search-mk`, `votes`, `vote-detail`, `bills`, `factions`. Run: `python scripts/query_knesset.py --help`

### References
- `references/knesset-api-entities.md` — Complete entity reference for the Knesset OData API including field names for KNS_Person, KNS_Bill, KNS_Faction, and other entities, plus OData v3 filter syntax and position ID codes (43=MK male, 61=MK female, 45=Prime Minister, 39=Minister male, 57=Minister female). Note: vote data is not available via the public OData API. Consult when constructing OData queries.

## Recommended MCP Servers

For live Knesset and parliamentary data, pair this skill with:

| MCP Server | What it provides | Install |
|------------|-----------------|---------|
| **knesset** | MCP interface to the Israeli Knesset OData API: committee data, committee sessions, bills (private/government/committee), MK information, bill search, and current Knesset number. Includes prompt templates for analyzing legislation and voting records. | [Install knesset](https://agentskills.co.il/en/mcps/knesset) |

When the `knesset` MCP is available, use its tools for real-time legislative data instead of manually constructing OData queries. The MCP handles API pagination, filtering, and data formatting automatically.

## Gotchas
- Israeli elections use a proportional representation system with a 3.25% electoral threshold, not a district-based system. Agents may describe Israeli elections using US congressional district terminology.
- Israel has no fixed election schedule. Elections can be called at any time when the Knesset dissolves. Agents should not assume a 4-year cycle.
- Israeli political party names change frequently due to mergers, splits, and rebranding. Agents may reference party names that no longer exist or conflate different parties.
- Election results data from the Central Elections Committee (vaádat habechirot hamerkazit) is published in Hebrew. Party letter symbols (otiyot) are used alongside names and differ each election.

## Troubleshooting

### Error: "OData query syntax error"
Cause: Incorrect OData v3 filter syntax
Solution: Use `eq` for equals, `and`/`or` for logic, `substringof('text', Field)` for text search. Ensure string values are in single quotes.

### Error: "Data returned in Hebrew"
Cause: Knesset data is primarily in Hebrew
Solution: Field names are in English (camelCase), but values (names, bill text, etc.) are in Hebrew. Use translation or maintain Hebrew for accuracy.

### Error: "Entity not found"
Cause: Entity name is case-sensitive
Solution: Use exact entity names as documented: KNS_Person, KNS_Bill, etc. All start with "KNS_" prefix. Query the service root for available entities.