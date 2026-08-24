---
name: israeli-election-data
description: Access Israeli election and political data from the Knesset OData v4 API and the Central Elections Committee (data.gov.il). Use when user asks about Knesset, Israeli elections, MK (Member of Knesset) information, Israeli voting records (per-MK plenum votes via KNS_PlenumVote/KNS_PlenumVoteResult), legislative bills in Israel, Knesset committees, Israeli political parties, coalition data, or election results by locality or ballot. Covers Knesset OData v4 API, Central Elections Committee CSV datasets on data.gov.il, municipal elections, and Israeli political system structure. Do NOT use for non-Israeli elections or political opinion/prediction.
license: MIT
allowed-tools: Bash(python:*), WebFetch
compatibility: Requires network access for Knesset API and data.gov.il. No API keys needed (public data). Data primarily in Hebrew (field names English, values Hebrew).
---

# Israeli Election Data

## Instructions

### Step 1: Identify Data Need

| Data Type | Source | Endpoint / Dataset |
|-----------|--------|--------------------|
| MK information | Knesset OData v4 | `KNS_Person`, `KNS_PersonToPosition`, `KNS_MkSiteCode` |
| Plenum votes (per-MK detail) | Knesset OData v4 | `KNS_PlenumVote`, `KNS_PlenumVoteResult` |
| Bills / legislation | Knesset OData v4 | `KNS_Bill`, `KNS_BillInitiator`, `KNS_BillName` |
| Israeli law corpus (enacted) | Knesset OData v4 | `KNS_IsraelLaw`, `KNS_IsraelLawName`, `KNS_SecondaryLaw` |
| Committee sessions | Knesset OData v4 | `KNS_Committee`, `KNS_CommitteeSession`, `KNS_CmtSessionItem` |
| Plenum sessions | Knesset OData v4 | `KNS_PlenumSession`, `KNS_PlmSessionItem` |
| Parliamentary questions (שאילתות) | Knesset OData v4 | `KNS_Query` |
| Agenda proposals (הצעות לסדר-היום) | Knesset OData v4 | `KNS_Agenda` |
| Knesset session dates | Knesset OData v4 | `KNS_KnessetDates` |
| Party information | Knesset OData v4 | `KNS_Faction` |
| Election results (per locality / per ballot) | data.gov.il (Central Elections Committee) | dataset `votes-knesset` (CSVs for Knessets 16-25) |
| Party platforms / candidate lists | Central Elections Committee | `bechirot.gov.il` |

### Step 2: Query the Knesset OData v4 API

**Base URL:** `https://knesset.gov.il/OdataV4/ParliamentInfo/`

OData v4. The root URL returns the entity list. As of August 2026 the service exposes all `KNS_`-prefixed entities listed in Step 1 plus the document and lookup tables documented in `references/knesset-api-entities.md`.

**Legacy v3 fallback:** the older endpoint at `https://knesset.gov.il/Odata/ParliamentInfo.svc/` is still live. Code written against it keeps working, but v4 is the current API and exposes vote tables (`KNS_PlenumVote`, `KNS_PlenumVoteResult`) that v3 does not. New work should target v4.

**Query pattern (v4):**
```
GET {BASE_URL}/{ENTITY}?$filter={FILTER}&$top={LIMIT}&$select={FIELDS}&$orderby={FIELD}
```

v4 returns JSON by default; `$format=json` is no longer required. Include `$count=true` to get the total record count alongside the page; pair with `$top=0` to get a count-only response. For large result sets (any per-MK vote query, multi-Knesset historical pulls), the v4 server returns `@odata.nextLink` when more pages exist; loop on `nextLink` until it's absent. Default page size varies by entity, so do not rely on a single `$top=N` to return everything.

**Get all MKs in the 25th Knesset (sworn in 2022-11-15):**
```
GET .../KNS_PersonToPosition?$filter=KnessetNum eq 25 and (PositionID eq 43 or PositionID eq 61)&$top=120
```
PositionID 43 = male MK (`חבר הכנסת`), 61 = female MK (`חברת הכנסת`). PositionID 54 is a separate "faction member" designation, see Gotchas. Full lexicon in `references/knesset-api-entities.md`.

**Search MK by name (Hebrew or English), v4 uses `contains`, not v3's `substringof`:**
```
GET .../KNS_Person?$filter=contains(LastName,'נתניהו') or contains(FirstName,'נתניהו')&$top=10
```

**Get factions in a Knesset:**
```
GET .../KNS_Faction?$filter=KnessetNum eq 25
```

### Step 3: Per-MK Plenum Votes (v4)

The two entities to know:

| Entity | Role |
|--------|------|
| `KNS_PlenumVote` | One row per vote: title, time, session, method, status, for/against descriptions, no-confidence flag |
| `KNS_PlenumVoteResult` | One row per MK per vote: `MkId`, `VoteID`, `ResultDesc` ("בעד" / "נגד" / "נמנע"), `LastName`, `FirstName` |

**Find a vote, then the per-MK results:**

1. Find the vote by topic:
```
GET .../KNS_PlenumVote?$filter=contains(VoteTitle,'תקציב')&$orderby=VoteDateTime desc&$top=5
```
Field is `VoteTitle`, NOT `ItemTitle` (which does not exist on this entity, see Gotchas).

2. Pull per-MK results for that vote (paginate, do not assume 120 rows):
```
GET .../KNS_PlenumVoteResult?$filter=VoteID eq {id}&$top=200&$count=true
```
**Absent MKs are not in the response.** `KNS_PlenumVoteResult` only contains MKs who registered a vote (for / against / abstain). A missing MK row does NOT mean "voted no", it means "did not vote / not present". For attendance analysis, compare the returned `MkId` set against the active-MK list from `KNS_PersonToPosition` for that Knesset.

3. Filter to a specific MK by name (safest path, names are bundled in every result row):
```
GET .../KNS_PlenumVoteResult?$filter=VoteID eq {id} and contains(LastName,'גפני')
```
Or by `MkId` if you already have it from a prior `KNS_PlenumVoteResult` row:
```
GET .../KNS_PlenumVoteResult?$filter=VoteID eq {id} and MkId eq {mkId}
```
**`MkId` is a distinct identifier space from `KNS_Person.Id`.** Treat `MkId` as opaque, harvest it from `KNS_PlenumVoteResult` rows themselves (each row also carries `FirstName` / `LastName`), rather than assuming `KNS_Person.Id` equals `MkId`. If you only have a person from `KNS_Person`, find their `MkId` via a name match on a recent `KNS_PlenumVoteResult` query and cache it for the session.

Field is `MkId`, NOT `PersonID`. Read `ResultDesc` ("בעד" / "נגד" / "נמנע") for the outcome; `ResultCode` integer values do not follow a simple 1/2/3 mapping (the live value for "בעד" on row 1 is 7), always use `ResultDesc`.

For aggregate "did the bill pass" status without per-MK detail, query `KNS_Bill.StatusID` (Step 4).

**Historical / archival vote data** before public v4 access: the `hasadna/knesset-data` community ETL at `https://github.com/hasadna/knesset-data` mirrored Knesset internal databases to CSV/parquet. **It is unmaintained**, last commit 29 April 2018, so treat it as a frozen historical archive rather than a live feed. Anything from Knesset 20 onward should come from the v4 API instead.

### Step 4: Track Legislation

**Search bills by keyword (v4 `contains` syntax):**
```
GET .../KNS_Bill?$filter=KnessetNum eq 25 and contains(Name,'דיור')&$orderby=PublicationDate desc&$top=50
```

**Bill status codes (key values, verified against the live table):**
- 108 = `הכנה לקריאה ראשונה`, preparation for first reading
- 118 = `התקבלה בקריאה שלישית`, approved in third reading (became law)
- 177 = `נעצרה`, halted

There is **no status 125**, and there is no single "rejected" status. A bill that fails is usually halted (177), merged into another bill (122), or converted to an agenda item (124). Do not infer rejection from the absence of 118.

For the full list: `KNS_Status?$filter=TypeID eq 2` (35 rows). **`TypeID` 2 is bills**; `TypeID eq 5` returns plenum-session statuses (3 rows) and is a common wrong turn.

**Bill initiators, documents, related committee items:**
```
GET .../KNS_BillInitiator?$filter=BillID eq {id}&$expand=KNS_Person($orderby=LastName)
GET .../KNS_DocumentBill?$filter=BillID eq {id}
```
The `BillID` column in these related tables points back to `KNS_Bill.Id`. In v4 the primary key on every `KNS_*` entity is uniformly named `Id`; older "BillID / PersonID / CommitteeID" names persist only as foreign-key columns in related tables.

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

- Catalog page: `https://data.gov.il/api/3/action/package_show?id=votes-knesset`
- CKAN API: `https://data.gov.il/api/3/action/package_show?id=votes-knesset`

The package holds **17 resources**, not two per election:
- **By ballot box** (`לפי קלפיות`), raw per-ballot results, for Knessets **16 through 25**.
- **By locality** (`לפי יישובים`), aggregated turnout and vote counts per city/town, for Knessets **19 through 25 only**. Knessets 16, 17 and 18 have no per-locality file; aggregate the ballot file yourself for those years.

**Use the CKAN datastore, not the CSV download.** All 17 resources have `datastore_active: true`, and `datastore_search` returns clean UTF-8 JSON:
```
GET https://data.gov.il/api/3/action/datastore_search?resource_id={resource_id}&limit=1000&offset=0
```
Page with `limit` / `offset` until `records` comes back empty. Records are keyed by Hebrew column names, and the per-party columns are **ballot letter symbols** (`אמת`, `ב`, `ג`, `מחל`, `שס` ...) rather than party names. Example resource IDs for the 25th Knesset: `b392b8ee-ba45-4ea0-bfed-f03a1a36e99c` (by locality), `cc223336-07bc-485d-b160-62df92967c0a` (by ballot).

**The raw CSV download is not programmatically retrievable.** As observed on 24 August 2026, the `aws-e.data.gov.il/.../download/-25-.csv` URLs sit behind an AWS load-balancer Google-OAuth gate: a plain fetch returns 403, and a browser-like fetch returns HTTP 200 carrying roughly 1.2 MB of a Google sign-in page instead of the file. Re-probe before relying on the CSV route. That failure is **silent**, the response looks like a successful download. Treat the CSV route as browser-and-human only, and never feed its response to a CSV parser.
**Do not match resource names literally.** The publisher spells the per-locality files `לפי יישובים` (two yods) for Knessets 21-25 but `לפי ישובים` (one yod) for 19-20. Match on the Knesset number plus a yod-insensitive stem, or select by position in the resource list.

Find the latest resource IDs via the CKAN API call above.

**Coverage stops at the 25th Knesset.** The dataset carries Knessets 16 through 25 only. Results for the 26th Knesset (election scheduled 27 October 2026, see Step 6) will not appear here until the Central Elections Committee certifies the count after election day. If a user asks for 26th-Knesset results before then, tell them the data does not exist yet instead of searching for it.

**Per-cycle results subdomains.** Certified results for each election live on a `votesNN.bechirot.gov.il` subdomain (`https://votes25.bechirot.gov.il/` for 2022, with `/nationalresults`, `/cityresults` and `/ballotresults` paths). `votes26.bechirot.gov.il` returns **404 today** and is expected to appear around election night. A 404 there before 27 October 2026 is a calendar fact, not a broken link, so do not report the canonical results host as dead.

**Note on `votes.gov.il`:** older documentation cites `votes.gov.il` as the results site. That hostname no longer resolves; the canonical site is now `https://www.bechirot.gov.il/` (Central Elections Committee, live and currently running the 26th Knesset election cycle) and the canonical data is on data.gov.il.

### Step 6: Electoral System Facts

- **Knesset size:** 120 seats (unchanged since 1949).
- **System:** Single national-list proportional representation, no districts.
- **Electoral threshold:** **3.25%** of valid votes since the March 2014 amendment to the Knesset Elections Law (חוק הבחירות לכנסת). Was 2% before that.
- **Seat allocation:** Modified D'Hondt, named **Bader-Ofer** in Israel (after MKs Yohanan Bader and Avraham Ofer). Internationally equivalent to the Hagenbach-Bischoff method. Two-phase allocation: (1) integer share of valid votes among parties that crossed the threshold, (2) "leftover seats" via D'Hondt highest-averages.
- **Surplus-vote agreements (`heskemei odafim`):** Two parties may sign a pre-election pact to be treated as one bloc for the leftover-seat round only.
- **Election schedule:** No fixed cycle. Knesset term is up to 4 years but can be dissolved earlier.

**Current status (verified 24 August 2026): Israel is in an active election period.** The 25th Knesset formally dissolved on **17 July 2026** after completing its full four-year term. Elections to the **26th Knesset** are scheduled for **27 October 2026**, which is now a formally set date rather than merely the statutory outer limit. What this means for any query about "the current Knesset" or "the current coalition":

- The 26th Knesset does not exist yet. No MK list, faction list, or seat count for it exists in any source.
- **The outgoing Knesset remains in office until the incoming one convenes** (Basic Law: The Knesset, continuity rule). This is why `KNS_PersonToPosition` still returns 120 sitting MKs with `IsCurrent` true weeks after dissolution. That data is correct, not stale, but it does NOT mean the Knesset is sitting in the ordinary sense. Say which it is.
- The 37th government continues in a caretaker capacity until a new government is formed.
- **After election day**, results must be certified and published before the new Knesset convenes (scheduled 10 November 2026), after which the president assigns a government-formation mandate. Until a new government is sworn in, the outgoing one continues.
- Most `KNS_*` entities filtered on `KnessetNum eq 26` return empty (`KNS_Faction`, `KNS_Bill`, `KNS_PersonToPosition`, `KNS_PlenumSession`, `KNS_CommitteeSession` all return `@odata.count` 0). Use `KnessetNum eq 25` for the outgoing Knesset's records.
- **`KNS_KnessetDates` is the exception, and it is the one to query.** It already carries a Knesset 26 row with the scheduled first sitting: `KNS_KnessetDates?$filter=KnessetNum eq 26` returns `PlenumStart` **2026-11-10**. This is the API's own answer to "when does the new Knesset convene". `KNS_KnessetDates?$filter=IsCurrent eq true` returns the Knesset 25 row whose `PlenumFinish` is 2026-07-17. **`PlenumFinish` is the end of that sitting period (מושב), not a dissolution date** (Knesset 25's earlier sessions end 2023-07-30, 2024-07-28, 2025-07-27, all ordinary summer recesses), and the Knesset still recorded 35 plenum votes on and after 2026-07-17, 22 of them after that day, the latest on 2026-07-28. It happens to coincide with the dissolution this cycle. Take the dissolution date from the Central Elections Committee or the press, not by reading `PlenumFinish`.
- The Central Elections Committee publishes the official cycle timeline (voter-roll corrections, ballot-area allocation, candidate-list filing, disqualification petitions) at `https://www.bechirot.gov.il/`. Candidate lists are due to the committee on 7-8 September 2026. The committee's own timeline is authoritative on these dates.

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

**Total coalition: 64, opposition: 56.** Below-threshold parties: Meretz (3.16%) and Balad (2.91%), both received 0 seats. The 25th Knesset was sworn in on November 15, 2022.

### Step 8: Municipal Elections

Municipal elections (`bechirot reshuyot mekomiyot`) are normally held every five years. Most recent cycle:

- **27 February 2024**, 242 localities. Second round 10 March 2024 in 35 of them.
- **November 2024**, separate round for 11 northern and southern localities that were evacuated due to the Gaza/Lebanon wars and could not vote in February.
- Turnout in 2024 was lower than in 2018 but higher than in 2003, 2008 and 2013 (Israel Democracy Institute). Do not quote a single national turnout percentage -- the IDI analysis publishes it only as a chart.

Municipal results were published on a per-cycle Central Elections Committee site. **The 2024 municipal site has been retired**: `bechirot.gov.il/local2024/Pages/default.aspx` now redirects to `maintenance.gov.il`. There is **no national machine-readable municipal results dataset**: the `votes-knesset` package on data.gov.il is Knesset-only (all 17 resources). Start from the committee's historical-information section at `https://www.bechirot.gov.il/`, or pull results per authority via the Ministry of Interior. Each city publishes its own breakdown via the Ministry of Interior (`https://www.gov.il/he/departments/ministry_of_interior`).

### Step 9: Coalition, Government, and Auxiliary Data

| Topic | Source |
|-------|--------|
| Coalition agreements (full text, Hebrew) | Tabled with the Knesset and published by the PMO. `https://www.gov.il/he/Departments/policies` redirects to a generic all-ministry procedures collector and is NOT a coalition-agreement index, so search the Knesset site or PMO publications directly. |
| Government composition (current ministers) | `KNS_PersonToPosition` filtered to `PositionID eq 39` (male) / `57` (female) / `45` (PM) |
| Knesset committee composition | `KNS_PersonToPosition` filtered to `PositionID eq 41` (chair) / `42` (member) |
| Faction membership (separate from MK role) | `KNS_PersonToPosition` filtered to `PositionID eq 54` (see Gotchas) |
| Knesset speaker | `PositionID eq 122` (male) / `123` (female) |
| Party financing reports | State Comptroller (`mevaker hamedina`): `https://www.mevaker.gov.il/` |
| Voter roll (registration check, correction deadlines) | Central Elections Committee cycle timeline: `https://www.bechirot.gov.il/`. The Ministry of Interior operates the online check; its deep link moves between cycles, so navigate from the committee site rather than hardcoding a URL. |
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
1. Search `KNS_Person?$filter=contains(LastName,'אלהרר')` to find the person's `Id`.
2. Query `KNS_PersonToPosition?$filter=PersonID eq {id}` to enumerate her current and historical roles (MK terms, ministerial positions).
3. Use `KNS_Faction` to resolve `FactionID` to faction name per Knesset.
4. Present MK profile with party affiliation and ministerial history. For her actual votes on plenum motions, query `KNS_PlenumVoteResult?$filter=MkId eq {id}` (see Example 5).

### Example 2: Bill Tracking
User says: "What happened to the bill on the haredi draft?"
Actions:
1. Search `KNS_Bill?$filter=KnessetNum eq 25 and contains(Name,'גיוס')`.
2. Read each bill's `Id`, `StatusID`, `SubTypeID`.
3. Find sponsors: `KNS_BillInitiator?$filter=BillID eq {id}&$expand=KNS_Person`.
4. Look up status text via `KNS_Status`.
5. Pull related committee sessions via `KNS_CmtSessionItem?$filter=ItemID eq {bill.Id}`.
6. Present bill status, sponsor list, committee assignment, and current reading.

### Example 3: Election Analysis by Locality
User says: "Show me the 25th Knesset results for Haifa."
Actions:
1. Resolve the latest `votes-knesset` per-locality CSV via the CKAN API: `GET data.gov.il/api/3/action/package_show?id=votes-knesset`, pick the per-locality resource for Knesset 25 (spelled `לפי יישובים`, but match yod-insensitively per Step 5).
2. Pull the records via `datastore_search` (see Step 5). Do NOT use the CSV download URL.
3. Filter by locality code or Hebrew name (`חיפה`).
4. Aggregate by party column. **The columns are ballot letter symbols, not party names** (`אמת`, `ב`, `ג`, `מחל`, `שס` ...), alongside `שם ישוב`, `בזב` (eligible voters), `מצביעים`, `כשרים`, `פסולים`. Letters are re-assigned by lottery each cycle, so resolve them against the candidate-list letters for that specific election before naming any party.
5. Compare to national results from Step 7.

### Example 4: Coalition Composition
User says: "Which factions are in the current coalition?"
Actions:
1. **Check the electoral calendar first (Step 6).** As of August 2026 the Knesset is dissolved and the 37th government is a caretaker government pending the 27 October 2026 election. Say so before answering, because "the current coalition" means something different during an election period.
2. Query `KNS_Faction?$filter=KnessetNum eq 25` to list the outgoing Knesset's factions.
3. Do NOT read coalition membership off the Step 7 table. That table is the November 2022 election-night result, and factions split, merged and renamed across the term, so the live `KNS_Faction` list for Knesset 25 will not match it.
4. For authoritative membership at a given moment, use `KNS_PersonToPosition` with `FinishDate eq null`, and confirm against current Knesset and government publications.

### Example 5: Per-MK Vote Lookup (v4 only)
User says: "Did MK Gafni vote in favor of the budget?"
Actions:
1. Find the budget vote: `KNS_PlenumVote?$filter=contains(VoteTitle,'תקציב')&$orderby=VoteDateTime desc&$top=10`, pick the relevant `Id`.
2. Filter `KNS_PlenumVoteResult` by `VoteID` + last name (the row already carries `FirstName` / `LastName`, no need to resolve through `KNS_Person`): `KNS_PlenumVoteResult?$filter=VoteID eq {voteId} and contains(LastName,'גפני')`.
3. If the result set is empty, that means MK Gafni did not register a vote (absent / abstained-by-absence), NOT "voted no". Report the absence honestly.
4. If results exist, read `ResultDesc` ("בעד" / "נגד" / "נמנע") and present alongside `VoteTitle` and `VoteDateTime`. Note: do NOT derive `MkId` from `KNS_Person.Id`, those are different ID spaces; the name match on the result row is the reliable path.

## Bundled Resources

### Scripts
- `scripts/query_knesset.py`, Query the Knesset OData v4 API. Subcommands: `mks` (list MKs by Knesset), `search-mk` (by name), `bills` (search by keyword), `votes` (find votes by topic, optionally per-MK results), `factions` (list factions), `entities` (list available OData entities), `positions` (list position-ID lexicon). Run: `python scripts/query_knesset.py --help`.

### References
- `references/knesset-api-entities.md`, Entity reference for the Knesset OData v4 API: field names, OData v4 filter syntax (`contains`, `in`, `$expand`), the full PositionID lexicon (43=MK male, 61=MK female, 45=PM, 39=Minister male, 57=Minister female, 41=Committee Chair, 42=Committee Member, 54=faction member, 122/123=Knesset Speaker, etc.), the per-MK vote entities (`KNS_PlenumVote`, `KNS_PlenumVoteResult`), and v3 fallback notes.
- `references/domain-checklist.md`, Coverage checklist for a Knesset/elections skill (must-cover, should-cover, out-of-scope) used by the expert-review pipeline.

## Recommended MCP Servers

For live Knesset and parliamentary data, pair this skill with:

| MCP Server | What it provides | Install |
|------------|------------------|---------|
| **knesset** | MCP interface to the Israeli Knesset OData API: committee data, sessions, bills (private/government/committee), MK information, bill search, and current Knesset number. Prompt templates for analyzing legislation. | [Install knesset](https://agentskills.co.il/en/mcp/knesset) |

When the `knesset` MCP is available, use its tools for live legislative data instead of manually constructing OData queries.

## Gotchas
- Israeli elections use a single national-list proportional representation system with a 3.25% electoral threshold. There are no districts. Agents may incorrectly describe Israeli elections using US congressional-district terminology.
- Israel has no fixed election schedule. Elections can be called at any time if the Knesset dissolves. Do not assume a 4-year cycle.
- **Israel is in an active election period as of August 2026** (Knesset dissolved 17 July 2026, election 27 October 2026). Any answer about "the current Knesset", "the current government" or "the current coalition" has to say so. `KnessetNum eq 26` returns empty everywhere until the new Knesset is sworn in.
- **`FinishDate eq null` does NOT mean "the Knesset is sitting".** It means the position has not been formally ended, and under the continuity rule the outgoing MKs' positions stay open until the new Knesset convenes. Five weeks after the 17 July 2026 dissolution the filter still returns all 120 MKs with `IsCurrent` true. Pair it with the calendar from `KNS_KnessetDates`, never read it as a live-Knesset signal on its own.
- **A Knesset's faction list drifts away from its election-night result.** The Step 7 table is the November 2022 result. Factions split, merge and rename mid-term, so `KNS_Faction?$filter=KnessetNum eq 25` returns the live picture and will not match the election table. Use the API for "who is in which faction now", the table only for "what did the election return".
- **`main.knesset.gov.il` is bot-protected.** It answers plain automated requests with a non-standard HTTP `247` and a JavaScript interstitial, and a headless browser may get the same. The pages work normally for a human in a real browser, so do not report them as dead. Use the OData API for anything programmatic.
- Israeli political party names change frequently due to mergers, splits, and rebranding (Likud-Beytenu, Blue and White, Yamina, National Unity, etc.). Agents may reference party names that no longer exist or conflate different parties across cycles.
- Central Elections Committee results are published in Hebrew. Party letter symbols (`otiyot`) are used alongside names and change every election (the letters are assigned by lottery before each cycle).
- **v4 is the current API; v3 is legacy.** v4 uses `contains(Field,'text')` for substring matching; v3 used `substringof('text', Field)`. The v3 endpoint at `https://knesset.gov.il/Odata/ParliamentInfo.svc/` is still up but does NOT expose vote tables, prefer v4 for new code.
- **Primary key is uniformly `Id` in v4.** Older "BillID / PersonID / CommitteeID / FactionID" names persist as foreign-key columns in related tables, but the entity's own PK is always `Id`.
- **Per-MK plenum votes ARE in v4** via `KNS_PlenumVote` (one row per vote) + `KNS_PlenumVoteResult` (one row per MK per vote). The old "use hasadna scraper" advice applied to v3 only.
- **`KNS_PlenumVote.VoteTitle`, not `ItemTitle`.** `ItemTitle` does not exist on this entity and returns a 400 error.
- **`KNS_PlenumVoteResult.MkId`, not `PersonID`.** Use `ResultDesc` for the outcome ("בעד" / "נגד" / "נמנע"); `ResultCode` integers do not follow a simple 1/2/3 mapping (the live value for "בעד" on the first row is 7, not 1).
- **`KNS_Query` stores `GovMinistryID` (integer), not `GovMinistryName`.** Resolve names via `KNS_GovMinistry?$filter=contains(Name,'משפטים')&$select=Id,Name` first, then filter `KNS_Query` by `GovMinistryID in (<ids>)`.
- **PositionID 54 records faction membership; PositionID 43/61 record the MK role. You need BOTH.** `FactionID` and `FactionName` are `null` on every 43/61 row (`KnessetNum eq 25 and PositionID eq 43 and FactionID ne null` returns 0), and are populated only on PositionID 54 rows (193 for Knesset 25). So to list MKs by faction: take the PersonIDs from the 43/61 rows for the MK role, then join to that same person's PositionID 54 row for the faction. Filtering 43/61 by `FactionID` returns an empty set every time.
- **`KNS_IsraelLawClassificiation` is misspelled in the upstream API** (double 'i'). Do not "fix" it, the correctly-spelled name returns 404.
- **`KNS_CommitteeSession` StatusID 193 = cancelled.** Always filter with `StatusID ne 193` unless cancelled sessions are explicitly wanted.
- **Knesset 0 = Provisional State Council** (מועצת המדינה הזמנית, 1948-49). Data quality improves materially from Knesset 17 onward; older records may have gaps.
- **Datetime format** in v4: ISO 8601, no quotes. Use `VoteDateTime gt 2024-01-01T00:00:00Z`, not `datetime'2024-01-01'` (the v3 form).
- `votes.gov.il` no longer resolves. Use `bechirot.gov.il` for the live site and `data.gov.il/api/3/action/package_show?id=votes-knesset` for the CSVs.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Knesset OData v4 root | https://knesset.gov.il/OdataV4/ParliamentInfo/ | Live entity list |
| Knesset OData v4 metadata | https://knesset.gov.il/OdataV4/ParliamentInfo/$metadata | Full schema: field names, types, relationships |
| Knesset databases portal | https://knesset.gov.il/OdataV4/ParliamentInfo/ | Dataset announcements, API status |
| Bills search (web UI) | https://main.knesset.gov.il/Activity/Legislation/Laws/Pages/LawSuggestionsSearch.aspx | Cross-check bill data (bot-protected, open in a browser) |
| Plenum votes (web UI) | https://main.knesset.gov.il/activity/plenum/votes/pages/default.aspx | Cross-check vote data (bot-protected, open in a browser) |
| data.gov.il votes-knesset | https://data.gov.il/api/3/action/package_show?id=votes-knesset | Per-locality and per-ballot CSV results |
| Central Elections Committee | https://www.bechirot.gov.il/ | Official 26th Knesset election-cycle timeline, procedures, candidate lists |
| 25th Knesset official results | https://votes25.bechirot.gov.il/ | Certified national, per-locality and per-ballot results for the 2022 election |
| OData v4 spec | https://www.odata.org/documentation/ | Filter / expand / paging syntax reference |

## Troubleshooting

### Error: "OData query syntax error" / 400 Bad Request
Cause: Mixing v3 and v4 syntax. The most common slip is using `substringof('text', Field)` against the v4 endpoint, or `contains(Field,'text')` against the v3 endpoint.
Solution: On v4 (`/OdataV4/ParliamentInfo/`), use `contains(Field,'text')`, `in (v1,v2)`, ISO 8601 datetimes without the `datetime'...'` wrapper, and ISO 8601 dates like `2024-01-01`. On v3 (`/Odata/ParliamentInfo.svc/`), use `substringof('text', Field)` and `datetime'2024-01-01'`. Do not mix.

### Error: 404 on `KNS_VoteMain` or `KNS_VoteDetail`
Cause: Those entity names never existed on the public API. The names look plausible but are internal to the Knesset's legacy systems.
Solution: Use `KNS_PlenumVote` (the vote header) + `KNS_PlenumVoteResult` (per-MK rows) in v4. See Step 3.

### Error: 404 on `KNS_IsraelLawClassification` (correct English spelling)
Cause: The entity is intentionally misspelled in the API as `KNS_IsraelLawClassificiation` (double 'i').
Solution: Use the misspelled name exactly. Do not correct it, both v3 and v4 carry the same typo.

### Error: "Field 'ItemTitle' not found" on `KNS_PlenumVote`
Cause: `KNS_PlenumVote` uses `VoteTitle` for the descriptive label.
Solution: Replace `ItemTitle` with `VoteTitle`. There is no separate item-title column on this entity.

### Error: "Field 'PersonID' not found" on `KNS_PlenumVoteResult`
Cause: The MK foreign-key on this entity is `MkId`, not `PersonID`.
Solution: Use `MkId` in `$filter`. Read the MK's name from the row's bundled `FirstName`/`LastName` columns instead of joining back to `KNS_Person`.

### Error: ResultCode integers don't match expectation (1/2/3)
Cause: `KNS_PlenumVoteResult.ResultCode` is not a simple 1=for / 2=against / 3=abstain mapping.
Solution: Use `ResultDesc` ("בעד" / "נגד" / "נמנע") for the human-readable outcome and treat `ResultCode` as opaque.

### Error: "Field 'GovMinistryName' not found" on `KNS_Query`
Cause: `KNS_Query` stores `GovMinistryID` (integer), no name column.
Solution: Resolve the ID first via `KNS_GovMinistry?$filter=contains(Name,'משפטים')&$select=Id,Name`, then filter `KNS_Query` by `GovMinistryID in (<ids>)`.

### Error: Listing MKs by faction returns the wrong people
Cause: The MK role (PositionID 43/61) and faction membership (PositionID 54) are separate records, and `FactionID` is `null` on every 43/61 row. Filtering 43/61 by `FactionID` therefore returns nothing at all.
Solution: Two steps. Get the MK PersonIDs with `PositionID eq 43 or PositionID eq 61`, then get faction with `PositionID eq 54` for the same `KnessetNum` and join on `PersonID`. Note that `FinishDate eq null` means "position not formally ended", not "the Knesset is sitting": during a dissolution it still returns the full outgoing 120.

### Error: `KnessetNum eq 26` returns an empty result set
Cause: The 26th Knesset has not convened. The 25th Knesset dissolved on 17 July 2026 and the election is scheduled for 27 October 2026, so `KNS_Faction`, `KNS_Bill`, `KNS_PersonToPosition`, `KNS_PlenumSession` and `KNS_CommitteeSession` all return zero rows for Knesset 26.
Solution: Do not treat the empty response as an API fault or a filter-syntax error. Query `KnessetNum eq 25` for the outgoing Knesset's records. For the 26th Knesset itself, query `KNS_KnessetDates?$filter=KnessetNum eq 26`, which DOES return a row and gives the scheduled first sitting (`PlenumStart` 2026-11-10).

### Error: "Data returned in Hebrew"
Cause: Knesset data values are primarily in Hebrew.
Solution: Field names are in English (camelCase) but values (MK names, bill titles, party names, position descriptions) are in Hebrew. Use a translation step at the application layer or preserve Hebrew for accuracy.

### Error: "votes.gov.il connection refused"
Cause: That hostname is dead.
Solution: Use `https://www.bechirot.gov.il/` for the live Central Elections Committee site, or `https://data.gov.il/api/3/action/package_show?id=votes-knesset` for the historical CSVs.

### Error: "data.gov.il CSV is in legacy Hebrew encoding"
Cause: `votes-knesset` CSVs are not all in the same character encoding, and the publisher does not document which file uses which.
Solution: This applies only if you obtained the raw CSV through a browser. Detect the encoding per file (`chardet`) rather than assuming; if detection is inconclusive, try `utf-8-sig` and then `cp1255`. The `datastore_search` API route (Step 5) returns UTF-8 JSON and needs no encoding detection, so prefer it.
