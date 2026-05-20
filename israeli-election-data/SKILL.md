---
name: israeli-election-data
description: Access Israeli election and political data from the Knesset OData API and the Central Elections Committee (data.gov.il). Use when user asks about Knesset, Israeli elections, MK (Member of Knesset) information, Israeli voting records, legislative bills in Israel, Knesset committees, Israeli political parties, coalition data, or election results by locality or ballot. Covers Knesset OData v3 API, Central Elections Committee CSV datasets on data.gov.il, municipal elections, and Israeli political system structure. Do NOT use for non-Israeli elections or political opinion/prediction.
license: MIT
allowed-tools: Bash(python:*), WebFetch
compatibility: Requires network access for Knesset API and data.gov.il. No API keys needed (public data). Data primarily in Hebrew (field names English, values Hebrew).
---

# Israeli Election Data

## Instructions

### Step 1: Identify Data Need

| Data Type | Source | Endpoint / Dataset |
|-----------|--------|--------------------|
| MK information | Knesset OData API | `KNS_Person`, `KNS_PersonToPosition`, `KNS_MkSiteCode` |
| Plenum votes (per-MK detail) | Not in public OData | Use Knesset SessionVotes site or `hasadna/knesset-data` mirror |
| Bills / legislation | Knesset OData API | `KNS_Bill`, `KNS_BillInitiator`, `KNS_BillName` |
| Committee sessions | Knesset OData API | `KNS_Committee`, `KNS_CommitteeSession`, `KNS_CmtSessionItem` |
| Knesset session dates | Knesset OData API | `KNS_KnessetDates` |
| Election results (per locality / per ballot) | data.gov.il (Central Elections Committee) | dataset `votes-knesset` (CSVs for Knessets 16-25) |
| Party platforms / candidate lists | Central Elections Committee | `bechirot.gov.il` |
| Party information | Knesset OData API | `KNS_Faction` |
| Laws (in force) | Knesset OData API | `KNS_Law`, `KNS_IsraelLaw` |

### Step 2: Query the Knesset OData API

**Base URL:** `https://knesset.gov.il/Odata/ParliamentInfo.svc/`

The service is OData v3. The root URL returns the entity list. As of May 2026 it exposes 38 entities, all prefixed `KNS_` (see `references/knesset-api-entities.md`).

**Query pattern:**
```
GET {BASE_URL}/{ENTITY}?$format=json&$filter={FILTER}&$top={LIMIT}&$select={FIELDS}
```

**Get all MKs in the 25th Knesset (current, sworn in 2022-11-15):**
```
GET .../KNS_PersonToPosition?$format=json&$filter=KnessetNum eq 25 and (PositionID eq 43 or PositionID eq 61)&$top=120
```
PositionID 43 = male MK (`חבר הכנסת`), 61 = female MK (`חברת הכנסת`). See the full position table in `references/knesset-api-entities.md`.

**Search MK by name (Hebrew or English):**
```
GET .../KNS_Person?$format=json&$filter=substringof('שם', LastName) or substringof('שם', FirstName)&$top=10
```

**Get factions in a Knesset:**
```
GET .../KNS_Faction?$format=json&$filter=KnessetNum eq 25
```

### Step 3: Per-MK Vote Data (Important Limitation)

The public OData service **does NOT expose `KNS_VoteMain` or `KNS_VoteDetail`**. A direct request returns `Resource not found for the segment 'KNS_VoteMain'`.

To get per-MK plenum votes, use one of these alternates:

1. **Knesset SessionVotes web page** -- `https://main.knesset.gov.il/Activity/plenum/Pages/SessionVotes.aspx`. Renders per-session vote breakdowns, scrapeable with care.
2. **`hasadna/knesset-data`** -- community ETL at `https://github.com/hasadna/knesset-data` that mirrors Knesset internal databases (including vote tables) into open CSV/parquet dumps. This is the standard route for academic and journalistic analysis.
3. **Open Knesset** -- `https://oknesset.org/` (archive of pre-25th-Knesset voting data, no longer actively updated).

For aggregate "did the bill pass" status, use `KNS_Bill.StatusID` instead (Step 4).

### Step 4: Track Legislation

**Search bills by keyword:**
```
GET .../KNS_Bill?$format=json&$filter=KnessetNum eq 25 and substringof('keyword', Name)&$top=50
```

**Bill status codes (key values):**
- 108 = Preparation for first reading
- 118 = Approved in third reading (became law)
- 120 = For plenum discussion on continuity law application
- 125 = Rejected

For the full list, query `KNS_Status?$format=json&$filter=TypeID eq 5`.

**Legislative process stages:**
1. Bill draft (private member or government bill)
2. Preliminary reading (private bills only, plenum vote)
3. Committee review (assigned to the relevant committee)
4. First reading (plenum vote on bill principles)
5. Committee preparation (clause-by-clause review)
6. Second reading (clause-by-clause plenum vote)
7. Third reading (final vote on the entire bill)
8. Publication in Reshumot (official gazette), the bill becomes law

### Step 5: Election Results (per Locality / per Ballot)

The Central Elections Committee publishes results on **data.gov.il** under the dataset `votes-knesset`:

- Catalog page: `https://data.gov.il/dataset/votes-knesset`
- CKAN API: `https://data.gov.il/api/3/action/package_show?id=votes-knesset`

Each Knesset election (16th through 25th) has two CSV files:
- **By locality** (`לפי יישובים`) -- aggregated turnout and vote counts per city/town. ~12,000 lines per cycle.
- **By ballot box** (`לפי קלפיות`) -- raw per-ballot results, ~12,000 ballots per cycle. Useful for granular analysis.

Example URL for 25th Knesset by locality:
```
https://e.data.gov.il/dataset/26f9fa06-fcd7-4173-8df5-65797b63e857/resource/b392b8ee-ba45-4ea0-bfed-f03a1a36e99c/download/-25-.csv
```

Find the latest resource IDs via the CKAN API call above.

**Note on `votes.gov.il`:** Older documentation cites `votes.gov.il` as the results site. That hostname no longer resolves; the canonical site is now `https://www.bechirot.gov.il/` (Central Elections Committee, may be in maintenance between election cycles) and the canonical data is on data.gov.il.

### Step 6: Electoral System Facts

- **Knesset size:** 120 seats (unchanged since 1949).
- **System:** Single national-list proportional representation, no districts.
- **Electoral threshold:** **3.25%** of valid votes since the 2014 amendment to Basic Law: The Knesset (Section 81). Was 2% before March 2014.
- **Seat allocation:** Modified D'Hondt, named **Bader-Ofer** in Israel (after MKs Yohanan Bader and Avraham Ofer). Internationally equivalent to the Hagenbach-Bischoff method. Two-phase allocation: (1) integer share of valid votes among parties that crossed the threshold, (2) "leftover seats" via D'Hondt highest-averages.
- **Surplus-vote agreements (`heskemei odafim`):** Two parties may sign a pre-election pact to be treated as one bloc for the leftover-seat round only. Each election cycle most parties pair off.
- **Election schedule:** No fixed cycle. Knesset term is up to 4 years but can be dissolved earlier. The next election (26th Knesset) must be held no later than **27 October 2026** under current legislation, though analysts widely expect an earlier dissolution.

### Step 7: 2022 Election Results (25th Knesset)

Canonical seat counts for the November 1, 2022 election:

| Faction (Hebrew) | Faction (English) | Seats | Bloc |
|------------------|-------------------|-------|------|
| הליכוד | Likud | 32 | Coalition |
| יש עתיד | Yesh Atid | 24 | Opposition |
| הציונות הדתית | Religious Zionism-Otzma Yehudit | 14 | Coalition |
| המחנה הממלכתי | National Unity | 12 | Opposition |
| ש"ס | Shas | 11 | Coalition |
| יהדות התורה | United Torah Judaism (UTJ) | 7 | Coalition |
| ישראל ביתנו | Yisrael Beiteinu | 6 | Opposition |
| רע"מ | Ra'am (United Arab List) | 5 | Opposition |
| חד"ש-תע"ל | Hadash-Ta'al | 5 | Opposition |
| העבודה | Labor | 4 | Opposition |

**Total coalition: 64, opposition: 56.** Below-threshold parties: Meretz (3.16%) and Balad (2.91%) -- both received 0 seats. The 25th Knesset was sworn in on November 15, 2022.

### Step 8: Municipal Elections

Municipal elections (`bechirot reshuyot mekomiyot`) are normally held every five years. Most recent cycle:

- **27 February 2024** -- 242 localities. Runoff round 10 March 2024 in 35 localities where no candidate cleared 40%.
- **November 2024** -- separate round for 11 northern and southern localities that were evacuated due to the Gaza/Lebanon wars and could not vote in February.
- Turnout was a historic low of approximately 49.5%.

Municipal results live on `https://www.bechirot.gov.il/local2024/Pages/default.aspx` and were eventually mirrored to `data.gov.il`. Each city publishes its own breakdown via the Ministry of Interior (`https://www.gov.il/he/departments/ministry_of_interior`).

### Step 9: Coalition, Government, and Auxiliary Data

| Topic | Source |
|-------|--------|
| Coalition agreements (full text, Hebrew) | `https://www.gov.il/he/Departments/policies` and PMO publications |
| Government composition (current ministers) | `KNS_PersonToPosition` filtered to `PositionID eq 39` (male) / `57` (female) / `45` (PM) |
| Knesset committee composition | `KNS_PersonToPosition` filtered to `PositionID eq 41` (chair) / `42` (member) |
| Knesset speaker | `PositionID eq 122` (male) / `123` (female) |
| Party financing reports | State Comptroller (`mevaker hamedina`): `https://www.mevaker.gov.il/` |
| Voter eligibility / registration check | Ministry of Interior: `https://www.gov.il/he/service/check_voter_registration` |
| Population context (per-locality demographics) | Central Bureau of Statistics: `https://www.cbs.gov.il/` |

### Israeli Political Terminology

| Hebrew | English | Meaning |
|--------|---------|---------|
| כנסת | Knesset | Parliament |
| חבר/ת כנסת | MK | Member of Knesset |
| סיעה | Faction | Political party/bloc inside the Knesset |
| מפלגה | Party | Registered political party (separate from `סיעה`) |
| קואליציה | Coalition | Governing alliance |
| אופוזיציה | Opposition | Non-governing parties |
| הצעת חוק | Bill | Legislative proposal |
| חוק יסוד | Basic Law | Quasi-constitutional law |
| ועדה | Committee | Knesset committee |
| מליאה | Plenum | Full Knesset session |
| הצבעה | Vote | Parliamentary vote |
| אחוז חסימה | Electoral threshold | Minimum vote share for representation (3.25%) |
| הסכם עודפים | Surplus-vote agreement | Pre-election pact between two parties for leftover-seat allocation |
| בדר-עופר | Bader-Ofer | The Israeli D'Hondt seat-allocation formula |
| קלפי | Kalpi | Ballot box / polling station |
| רשומות | Reshumot | Official gazette where laws are published |
| ועדת הבחירות המרכזית | Central Elections Committee | National election authority |

## Examples

### Example 1: MK Lookup
User says: "Tell me about MK Karine Elharrar."
Actions:
1. Search `KNS_Person?$filter=substringof('אלהרר', LastName)` to find PersonID.
2. Query `KNS_PersonToPosition?$filter=PersonID eq {id}` to enumerate her current and historical roles (MK terms, ministerial positions).
3. Use `KNS_Faction` to resolve `FactionID` → faction name per Knesset.
4. Present MK profile with party affiliation and ministerial history. For per-vote analysis, redirect to `hasadna/knesset-data` (per-MK votes are not in the public OData service).

### Example 2: Bill Tracking
User says: "What happened to the bill on the haredi draft?"
Actions:
1. Search `KNS_Bill?$filter=KnessetNum eq 25 and substringof('גיוס', Name)`.
2. Get `BillID`, `StatusID`, `SubTypeID`.
3. Find sponsors via `KNS_BillInitiator?$filter=BillID eq {id}`.
4. Look up status text via `KNS_Status`.
5. Pull related committee sessions via `KNS_CmtSessionItem?$filter=ItemID eq {billID}`.
6. Present bill status, sponsor list, committee assignment, and current reading.

### Example 3: Election Analysis by Locality
User says: "Show me the 25th Knesset results for Haifa."
Actions:
1. Resolve the latest `votes-knesset` per-locality CSV via the CKAN API: `GET data.gov.il/api/3/action/package_show?id=votes-knesset` → pick the resource named `תוצאות האמת של הבחירות לכנסת ה-25 לפי ייישובים`.
2. Download the CSV (`-25-.csv`).
3. Filter by locality code or Hebrew name (`חיפה`).
4. Aggregate by faction column.
5. Compare to national results from Step 7.

### Example 4: Coalition Composition
User says: "Which factions are in the current coalition?"
Actions:
1. Query `KNS_Faction?$filter=KnessetNum eq 25` to list all factions.
2. Match against the canonical Step 7 table (Likud, Religious Zionism, Shas, UTJ are coalition).
3. Note that coalition composition can shift mid-term -- always confirm against current Knesset/Government news.

## Bundled Resources

### Scripts
- `scripts/query_knesset.py` -- Query the Knesset OData API. Subcommands: `mks` (list MKs by Knesset), `search-mk` (by name), `bills` (search by keyword), `factions` (list factions), `entities` (list available OData entities), `positions` (list position-ID lexicon). Run: `python scripts/query_knesset.py --help`.

### References
- `references/knesset-api-entities.md` -- Entity reference for the Knesset OData v3 API: field names, OData filter syntax, the full PositionID lexicon (43=MK male, 61=MK female, 45=PM, 39=Minister male, 57=Minister female, 41=Committee Chair, 42=Committee Member, 122/123=Knesset Speaker, etc.), and notes on which entities are NOT exposed publicly (KNS_VoteMain, KNS_VoteDetail).

## Recommended MCP Servers

For live Knesset and parliamentary data, pair this skill with:

| MCP Server | What it provides | Install |
|------------|------------------|---------|
| **knesset** | MCP interface to the Israeli Knesset OData API: committee data, sessions, bills (private/government/committee), MK information, bill search, and current Knesset number. Prompt templates for analyzing legislation. | [Install knesset](https://agentskills.co.il/en/mcp/knesset) |

When the `knesset` MCP is available, use its tools for live legislative data instead of manually constructing OData queries.

## Gotchas
- Israeli elections use a single national-list proportional representation system with a 3.25% electoral threshold. There are no districts. Agents may incorrectly describe Israeli elections using US congressional-district terminology.
- Israel has no fixed election schedule. Elections can be called at any time if the Knesset dissolves. Do not assume a 4-year cycle.
- Israeli political party names change frequently due to mergers, splits, and rebranding (Likud-Beytenu, Blue and White, Yamina, National Unity, etc.). Agents may reference party names that no longer exist or conflate different parties across cycles.
- Central Elections Committee results are published in Hebrew. Party letter symbols (`otiyot`) are used alongside names and change every election (the letters are assigned by lottery before each cycle).
- The Knesset OData service is OData **v3**, not v4. Filter syntax is `substringof('text', Field)`, NOT v4's `contains(Field, 'text')`. Using v4 syntax returns a 400 error.
- `votes.gov.il` no longer resolves. Use `bechirot.gov.il` for the live site and `data.gov.il/dataset/votes-knesset` for the CSVs.
- Per-MK plenum vote records are NOT in the public OData service. `KNS_VoteMain` and `KNS_VoteDetail` return 404. Use `hasadna/knesset-data` or scrape the Knesset SessionVotes page.

## Troubleshooting

### Error: "Resource not found for the segment 'KNS_VoteMain'"
Cause: The public OData service does not expose vote tables.
Solution: Use `hasadna/knesset-data` (GitHub) for per-MK vote dumps, or query `KNS_Bill.StatusID` for aggregate "passed/failed" status.

### Error: "OData query syntax error"
Cause: Incorrect OData v3 filter syntax (often from using v4 patterns).
Solution: Use `eq` for equals, `and`/`or` for logic, `substringof('text', Field)` for text search. String values must be in single quotes. Numeric values without quotes. Do NOT use `contains(Field, 'text')` -- that is OData v4 and will fail.

### Error: "Data returned in Hebrew"
Cause: Knesset data values are primarily in Hebrew.
Solution: Field names are in English (camelCase) but values (MK names, bill titles, party names, position descriptions) are in Hebrew. Use a translation step at the application layer or preserve Hebrew for accuracy.

### Error: "Entity not found" (404)
Cause: Entity names are case-sensitive.
Solution: All entities start with the `KNS_` prefix and use exact capitalization (`KNS_Person`, `KNS_Bill`, `KNS_Faction`). Query the service root URL (`https://knesset.gov.il/Odata/ParliamentInfo.svc/?$format=json`) to see the live entity list.

### Error: "votes.gov.il connection refused"
Cause: That hostname is dead.
Solution: Use `https://www.bechirot.gov.il/` for the live Central Elections Committee site, or `https://data.gov.il/dataset/votes-knesset` for the historical CSVs.

### Error: "data.gov.il CSV is in legacy Hebrew encoding"
Cause: Older `votes-knesset` CSVs (Knesset 16-20) may be in Windows-1255 instead of UTF-8.
Solution: Read with `encoding='cp1255'` in Python, or detect via `chardet`. Newer files (21+) are UTF-8 with BOM.
