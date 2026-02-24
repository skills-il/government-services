# Israeli Election Data Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for accessing Israeli election and political data — Knesset API, voting records, election results, MK (Member of Knesset) information, and legislative tracking.

**Architecture:** MCP Enhancement skill (Category 3). Guides queries against the Knesset Open Data API and election commission data for political research and civic technology applications.

**Tech Stack:** SKILL.md, references for Knesset API (OData), Central Elections Committee data, and Israeli political system structure.

---

## Research

### Knesset Open Data API
- **Base URL:** `https://knesset.gov.il/Odata/ParliamentInfo.svc/`
- **Format:** OData v3 (XML/JSON)
- **Auth:** None (public API)
- **Key Entities:**
  - `KNS_MkSiteCode` — MK (Member of Knesset) information
  - `KNS_Person` — Person details (MKs, ministers, etc.)
  - `KNS_PersonToPosition` — Position history (MK terms, ministerial roles)
  - `KNS_Bill` — Legislative bills
  - `KNS_BillInitiator` — Bill sponsors
  - `KNS_CmtSessionItem` — Committee session agenda items
  - `KNS_PlmSessionItem` — Plenum session items
  - `KNS_VoteMain` — Main votes
  - `KNS_VoteDetail` — Individual MK votes
  - `KNS_Faction` — Political parties (factions)
  - `KNS_FactionChair` — Faction leadership
- **Query format:** OData filter syntax — `$filter=KnessetNum eq 25&$format=json`
- **Documentation:** main.knesset.gov.il/Activity/Info/Pages/Databases.aspx

### Central Elections Committee
- **Website:** votes.gov.il
- **Data available:**
  - Final election results by ballot location
  - Party lists and candidates
  - Voter turnout by locality
  - Historical election data (all Knesset elections)
- **Knesset elections history:** 25 elections since 1949
- **Electoral system:** Proportional representation, 3.25% threshold
- **Latest:** 25th Knesset (November 2022)

### Israeli Political System Structure
- **Knesset:** 120 seats, unicameral legislature
- **Government:** Coalition-based, typically 60-68 MKs
- **Opposition:** Remaining MKs not in coalition
- **Committees:** 12 standing committees + special committees
- **Legislative process:** Private bill → Committee → Three readings → Law
- **Government bills:** Minister-sponsored, usually higher passage rate
- **Knesset number:** Sequential from 1st Knesset (1949) to 25th (2022)

### Election Data Points
- **Ballots (kalpi):** ~12,000 ballot stations nationwide
- **Parties:** Identified by Hebrew letter combinations (אות/אותיות)
- **Mandates:** 120 seats distributed by modified D'Hondt method (Bader-Ofer)
- **Surplus agreements:** Parties can share surplus votes (הסכמי עודפים)
- **Dual envelopes:** Soldiers, diplomats, prisoners, hospital patients

### Use Cases
1. **MK lookup** — Find MK details, positions, and voting history
2. **Bill tracking** — Track legislation through the Knesset process
3. **Vote analysis** — Analyze voting patterns by party and MK
4. **Election results** — Historical and current election results by location
5. **Committee monitoring** — Track committee sessions and agenda items

---

## Build Steps

### Task 1: Create SKILL.md

**Files:**
- Create: `repos/government-services/israeli-election-data/SKILL.md`

```markdown
---
name: israeli-election-data
description: >-
  Access Israeli election and political data from the Knesset API and Central
  Elections Committee. Use when user asks about Knesset, Israeli elections,
  MK (Member of Knesset) information, Israeli voting records, legislative
  bills in Israel, Knesset committees, Israeli political parties, coalition
  data, or election results by locality. Covers Knesset OData API, election
  commission data, and Israeli political system structure. Do NOT use for
  non-Israeli elections or political opinion/prediction.
license: MIT
allowed-tools: "Bash(python:*) WebFetch"
compatibility: "Requires network access for Knesset API. No API keys needed (public data). Data primarily in Hebrew."
metadata:
  author: skills-il
  version: 1.0.0
  category: government-services
  tags: [knesset, elections, politics, legislation, voting, government, israel]
---

# Israeli Election Data

## Instructions

### Step 1: Identify Data Need

| Data Type | Source | API |
|-----------|--------|-----|
| MK information | Knesset API | KNS_Person, KNS_MkSiteCode |
| Voting records | Knesset API | KNS_VoteMain, KNS_VoteDetail |
| Bills / legislation | Knesset API | KNS_Bill, KNS_BillInitiator |
| Committee sessions | Knesset API | KNS_CmtSessionItem |
| Election results | Elections Committee | votes.gov.il |
| Party information | Knesset API | KNS_Faction |

### Step 2: Query Knesset API

**Base pattern for Knesset OData queries:**
```python
import requests

KNESSET_BASE = "https://knesset.gov.il/Odata/ParliamentInfo.svc"

def query_knesset(entity: str, filters: str = "", top: int = 50,
                  select: str = "") -> dict:
    """Query the Knesset OData API."""
    url = f"{KNESSET_BASE}/{entity}"
    params = {
        "$format": "json",
        "$top": top,
    }
    if filters:
        params["$filter"] = filters
    if select:
        params["$select"] = select

    response = requests.get(url, params=params)
    data = response.json()
    return data.get("value", data.get("d", {}).get("results", []))
```

**Get all MKs for current Knesset (25th):**
```python
def get_current_mks():
    """Get all Members of the 25th Knesset."""
    return query_knesset(
        entity="KNS_PersonToPosition",
        filters="KnessetNum eq 25 and PositionID eq 54",  # 54 = MK position
        top=120
    )
```

**Get MK details by name:**
```python
def search_mk(first_name: str = "", last_name: str = ""):
    """Search for an MK by name."""
    filters = []
    if first_name:
        filters.append(f"substringof('{first_name}', FirstName)")
    if last_name:
        filters.append(f"substringof('{last_name}', LastName)")
    filter_str = " and ".join(filters)
    return query_knesset(
        entity="KNS_Person",
        filters=filter_str,
        top=10
    )
```

### Step 3: Access Voting Data

**Get votes for a specific Knesset session:**
```python
def get_votes(knesset_num: int = 25, limit: int = 50):
    """Get main votes for a Knesset session."""
    return query_knesset(
        entity="KNS_VoteMain",
        filters=f"KnessetNum eq {knesset_num}",
        top=limit,
        select="VoteID,SessionID,ItemID,TypeID,StatusID,AcceptedText,TopicText"
    )

def get_vote_details(vote_id: int):
    """Get how each MK voted on a specific vote."""
    results = query_knesset(
        entity="KNS_VoteDetail",
        filters=f"VoteID eq {vote_id}",
        top=120
    )
    # VoteValue: 1=For, 2=Against, 3=Abstain, 4=Absent
    vote_map = {1: "For", 2: "Against", 3: "Abstain", 4: "Absent"}
    for r in results:
        r["VoteText"] = vote_map.get(r.get("VoteValue"), "Unknown")
    return results
```

**Analyze voting patterns:**
```python
def analyze_mk_voting(person_id: int, knesset_num: int = 25):
    """Analyze an MK's voting record."""
    votes = query_knesset(
        entity="KNS_VoteDetail",
        filters=f"PersonID eq {person_id}",
        top=500
    )
    summary = {"for": 0, "against": 0, "abstain": 0, "absent": 0}
    for v in votes:
        val = v.get("VoteValue")
        if val == 1: summary["for"] += 1
        elif val == 2: summary["against"] += 1
        elif val == 3: summary["abstain"] += 1
        elif val == 4: summary["absent"] += 1

    total = sum(summary.values())
    summary["total_votes"] = total
    summary["participation_rate"] = (
        (summary["for"] + summary["against"] + summary["abstain"]) / total * 100
        if total > 0 else 0
    )
    return summary
```

### Step 4: Track Legislation

**Search bills:**
```python
def search_bills(keyword: str = "", knesset_num: int = 25,
                 status: str = ""):
    """Search for bills in the Knesset."""
    filters = [f"KnessetNum eq {knesset_num}"]
    if keyword:
        filters.append(f"substringof('{keyword}', Name)")
    if status:
        # StatusID: 108=In preparation, 118=First reading approved,
        # 120=Approved, 125=Rejected, etc.
        filters.append(f"StatusID eq {status}")
    return query_knesset(
        entity="KNS_Bill",
        filters=" and ".join(filters),
        top=50
    )

def get_bill_sponsors(bill_id: int):
    """Get sponsors (initiators) of a bill."""
    return query_knesset(
        entity="KNS_BillInitiator",
        filters=f"BillID eq {bill_id}"
    )
```

**Legislative process stages:**
```
Israeli Legislative Process:

1. Bill Draft (הצעת חוק)
   - Private member bill or Government bill

2. Preliminary Reading (קריאה טרומית)
   - Private bills only; presented to plenum
   - Vote: Simple majority to proceed

3. Committee Review
   - Assigned to relevant committee
   - Discussions, amendments, expert hearings

4. First Reading (קריאה ראשונה)
   - Plenum vote on bill principles

5. Committee Preparation for Second & Third Readings
   - Detailed clause-by-clause review
   - Amendments finalized

6. Second Reading (קריאה שנייה)
   - Clause-by-clause plenum vote
   - Reservations (הסתייגויות) voted on

7. Third Reading (קריאה שלישית)
   - Final vote on entire bill
   - Simple majority (61 out of 120 for Basic Laws)

8. Publication (פרסום ברשומות)
   - Published in official gazette (Reshumot)
   - Becomes law
```

### Step 5: Election Results

**Access election data:**
```python
def get_election_results_summary(knesset_num: int = 25):
    """Get election results summary by party."""
    # Election results available from Central Elections Committee
    # Main data at votes.gov.il or via Knesset faction data
    factions = query_knesset(
        entity="KNS_Faction",
        filters=f"KnessetNum eq {knesset_num}",
        select="FactionID,Name,KnessetNum"
    )
    return factions

# Recent Israeli elections reference
recent_elections = {
    "25th_knesset": {
        "date": "2022-11-01",
        "turnout": "70.6%",
        "eligible_voters": 6788804,
        "threshold": "3.25%",
    },
    "24th_knesset": {"date": "2021-03-23", "turnout": "67.4%"},
    "23rd_knesset": {"date": "2020-03-02", "turnout": "71.5%"},
    "22nd_knesset": {"date": "2019-09-17", "turnout": "69.8%"},
    "21st_knesset": {"date": "2019-04-09", "turnout": "68.5%"},
}
```

### Step 6: Party and Coalition Data

**Get faction (party) information:**
```python
def get_factions(knesset_num: int = 25):
    """Get all factions in a Knesset session."""
    return query_knesset(
        entity="KNS_Faction",
        filters=f"KnessetNum eq {knesset_num}"
    )

def get_faction_members(faction_id: int):
    """Get all MKs in a specific faction."""
    return query_knesset(
        entity="KNS_PersonToPosition",
        filters=f"FactionID eq {faction_id} and PositionID eq 54",
        top=40
    )
```

**Israeli political terminology:**
| Hebrew | English | Meaning |
|--------|---------|---------|
| כנסת | Knesset | Parliament |
| חבר כנסת (ח"כ) | MK | Member of Knesset |
| סיעה | Faction | Political party/bloc in Knesset |
| קואליציה | Coalition | Governing alliance |
| אופוזיציה | Opposition | Non-governing parties |
| הצעת חוק | Bill | Legislative proposal |
| חוק יסוד | Basic Law | Constitutional law |
| ועדה | Committee | Knesset committee |
| מליאה | Plenum | Full Knesset session |
| הצבעה | Vote | Parliamentary vote |

## Examples

### Example 1: MK Lookup
User says: "Tell me about MK voting record for [name]"
Actions:
1. Search KNS_Person for MK by name
2. Get PersonID, then query KNS_VoteDetail
3. Calculate voting participation and pattern
4. Present summary with for/against/abstain breakdown
Result: MK profile with voting statistics.

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
```

**Step 2: Create references**
- `references/knesset-api-entities.md` — Complete list of Knesset OData entities with field descriptions
- `references/israeli-political-glossary.md` — Hebrew-English political terminology reference

**Step 3: Validate and commit**
