# Knesset OData API Entity Reference

## Base URL (current)
`https://knesset.gov.il/OdataV4/ParliamentInfo/`

OData v4 service. Root URL returns the live entity list.

### Legacy v3 endpoint (still up)
`https://knesset.gov.il/Odata/ParliamentInfo.svc/`

Same parliamentary data, older protocol version. Use only if maintaining existing code; v4 is the current API and is the only one that exposes per-MK vote tables.

## v4 Query Format
```
GET {BASE}/{ENTITY}?$filter={FILTER}&$top={LIMIT}&$select={FIELDS}&$orderby={FIELD}&$expand={REL}&$count=true
```

v4 returns JSON by default. `$format=json` is not required.

## Available Entities

People and positions:
- `KNS_Person`, MKs, ministers, other parliamentary figures.
- `KNS_PersonToPosition`, position history (MK terms, ministerial roles).
- `KNS_Position`, position-ID lexicon (see below).
- `KNS_MkSiteCode`, MK website / personal page identifiers.

Factions:
- `KNS_Faction`, political factions per Knesset.

Bills and legislation:
- `KNS_Bill`, legislative bills.
- `KNS_BillName`, bill titles (multiple versions / readings).
- `KNS_BillInitiator`, current bill sponsors.
- `KNS_BillHistoryInitiator`, historical sponsor records.
- `KNS_BillSplit`, records of bills split during legislative process.
- `KNS_BillUnion`, records of bills merged during legislative process.

Israeli law corpus:
- `KNS_IsraelLaw`, enacted Israeli law records.
- `KNS_IsraelLawName`, Israeli law titles (multiple versions over time).
- `KNS_IsraelLawBinding`, law-to-Knesset binding records.
- `KNS_IsraelLawClassificiation`, law classification. **Note the upstream typo** (double 'i'). The correctly-spelled `KNS_IsraelLawClassification` returns 404.
- `KNS_IsraelLawMinistry`, law-to-ministry mapping.
- `KNS_SecondaryLaw`, secondary legislation (regulations, orders, decrees).

Committees:
- `KNS_Committee`, Knesset committees.
- `KNS_CommitteeSession`, committee sessions.
- `KNS_CmtSessionItem`, items discussed in committee sessions.
- `KNS_CmtSiteCode`, committee website identifiers.
- `KNS_JointCommittee`, joint committees.

Plenum + votes:
- `KNS_PlenumSession`, plenum sessions.
- `KNS_PlmSessionItem`, items on plenum agendas.
- `KNS_PlenumVote`, **plenum votes (v4-only, exposed publicly)**. One row per vote: `Id`, `VoteDateTime`, `SessionID`, `ItemID`, `Ordinal`, `VoteMethodID`, `VoteMethodDesc`, `VoteStatusCode`, `VoteStatusDesc`, `VoteTitle`, `VoteSubject`, `IsNoConfidenceInGov`, `LastUpdatedDate`, `ForOptionID`, `ForOptionDesc`, `AgainstOptionID`, `AgainstOptionDesc`. **Field is `VoteTitle`, not `ItemTitle`**.
- `KNS_PlenumVoteResult`, **per-MK vote results (v4-only)**. One row per MK per vote: `Id`, `MkId`, `VoteID`, `VoteDate`, `ResultCode`, `ResultDesc` ("בעד" / "נגד" / "נמנע"), `LastUpdatedDate`, `LastName`, `FirstName`, `SessionID`, `ItemID`. **Field is `MkId`, not `PersonID`. Use `ResultDesc` for the outcome; `ResultCode` integers do not follow a simple 1/2/3 mapping.**

Questions + agenda:
- `KNS_Query`, parliamentary questions (שאילתות). Stores `GovMinistryID` (integer), NOT `GovMinistryName`. Resolve names first via `KNS_GovMinistry?$filter=contains(Name,'...')`.
- `KNS_Agenda`, agenda proposals (הצעות לסדר-היום).

Documents:
- `KNS_DocumentAgenda`, agenda documents.
- `KNS_DocumentBill`, bill documents.
- `KNS_DocumentCommitteeSession`, committee session documents.
- `KNS_DocumentIsraelLaw`, Israeli law documents.
- `KNS_DocumentSecondaryLaw`, secondary-legislation documents. (There is **no** `KNS_DocumentLaw` in v4; that name is v3-only and returns 404.)
- `KNS_DocumentPlenumSession`, plenum session documents.
- `KNS_DocumentQuery`, parliamentary query documents. **The service document advertises the entity set as `KNS_DocumentQuerie`, but that route returns 404; the working route is `KNS_DocumentQuery`.** Note also that it answers with a bare JSON array using camelCase keys (`id`, `queryID`, `groupTypeDesc`) and no `@odata.context`, i.e. a legacy response shape.

Lookups and metadata:
- `KNS_KnessetDates`, assembly/plenum session dates. **One row per assembly-plenum period, not one per Knesset.** **Knesset 0 = Provisional State Council** (מועצת המדינה הזמנית, 1948-49).
- `KNS_GovMinistry`, government ministries (used to resolve `GovMinistryID` -> name).
- `KNS_Status`, status code lookup (bill statuses, session statuses, etc.).
- `KNS_ItemType`, item type lookup.

## Entities NOT in the public OData service

`KNS_VoteMain` and `KNS_VoteDetail`, names from old internal databases. They never existed on the public API. Use `KNS_PlenumVote` + `KNS_PlenumVoteResult` (v4) instead.

## Common Field Names

### KNS_Person
- `Id`, `FirstName`, `LastName`, `GenderID`, `GenderDesc`, `Email`, `LastUpdatedDate`

### KNS_PersonToPosition
- `Id`, `PersonID`, `PositionID`, `KnessetNum`, `FactionID`, `FactionName`, `GovernmentNum`, `StartDate`, `FinishDate`, `IsCurrent`, `DutyDesc`, `GovMinistryID`, `GovMinistryName`, `CommitteeID`, `CommitteeName`, `LastUpdatedDate`
- **`FactionID` / `FactionName` are `null` on PositionID 43/61 rows.** Faction is carried only on the person's PositionID 54 row. Join on `PersonID` within the same `KnessetNum`; filtering 43/61 by `FactionID` returns nothing.
- **`FinishDate eq null` means "position not formally ended", not "the Knesset is sitting".** During a dissolution it still returns the full outgoing 120 with `IsCurrent` true.

### KNS_Faction
- `Id`, `Name`, `KnessetNum`, `StartDate`, `FinishDate`, `IsCurrent`, `LastUpdatedDate`

### KNS_Bill
- `Id`, `Name`, `KnessetNum`, `StatusID`, `SubTypeID`, `PublicationDate`, `LastUpdatedDate`

### KNS_BillInitiator
- `Id`, `BillID`, `PersonID`, `IsInitiator`, `Ordinal`

### KNS_Committee
- `Id`, `Name`, `KnessetNum`, `StartDate`, `FinishDate`

### KNS_CommitteeSession
- `Id`, `Number`, `KnessetNum`, `TypeID`, `TypeDesc`, `CommitteeID`, `StatusID`, `StartDate`, `FinishDate`. Filter `StatusID ne 193` to exclude cancelled sessions.

### KNS_PlenumVote
- `Id`, `VoteDateTime`, `SessionID`, `ItemID`, `Ordinal`, `VoteMethodID`, `VoteMethodDesc`, `VoteStatusCode`, `VoteStatusDesc`, `VoteTitle`, `VoteSubject`, `IsNoConfidenceInGov`, `LastUpdatedDate`, `ForOptionID`, `ForOptionDesc`, `AgainstOptionID`, `AgainstOptionDesc`

### KNS_PlenumVoteResult
- `Id`, `MkId`, `VoteID`, `VoteDate`, `ResultCode`, `ResultDesc`, `LastUpdatedDate`, `LastName`, `FirstName`, `SessionID`, `ItemID`

### KNS_KnessetDates
- `Id`, `KnessetNum`, `Name`, `Assembly`, `Plenum`, `PlenumStart`, `PlenumFinish`, `IsCurrent`, `LastUpdatedDate`.
- **There is no `StartDate` / `FinishDate` on this entity**; using them returns HTTP 400 (`Could not find a property named StartDate`). The date fields are `PlenumStart` / `PlenumFinish`.
- `IsCurrent eq true` returns exactly one row and is the reliable "where are we now" query. As of August 2026 it returns the Knesset 25 row whose `PlenumFinish` is the 2026-07-17 dissolution.
- A Knesset that has not convened still gets a row: `KnessetNum eq 26` returns `PlenumStart` 2026-11-10. This is the correct source for "when does the new Knesset convene".

## Position IDs (PositionID values)

Verified against live `KNS_Position` endpoint, 2026-05-21:

| ID | Hebrew | English |
|----|--------|---------|
| 29 | יושבת–ראש הקואליציה | Coalition Chair (female) |
| 30 | יושב–ראש הקואליציה | Coalition Chair (male) |
| 31 | משנה לראש הממשלה | Deputy PM |
| 39 | שר | Minister (male) |
| 40 | סגן שר | Deputy Minister (male) |
| 41 | יו"ר ועדה | Committee Chair |
| 42 | חבר ועדה | Committee Member |
| 43 | חבר הכנסת | MK (male) |
| 45 | ראש הממשלה | Prime Minister |
| 48 | יו"ר סיעה | Faction Leader |
| 50 | סגן ראש הממשלה | Deputy PM (alt title) |
| 51 | מ"מ ראש הממשלה | Acting PM |
| 54 | חבר/ת סיעה | Faction Member (note: NOT the same as MK; this records faction membership) |
| 57 | שרה | Minister (female) |
| 59 | סגנית שר | Deputy Minister (female) |
| 61 | חברת הכנסת | MK (female) |
| 65 | סגנית ראש הממשלה | Deputy PM (female) |
| 66 | חברת ועדה | Committee Member (female) |
| 67 | מ"מ חבר ועדה | Acting Committee Member |
| 70 | סגן יושב-ראש הכנסת | Knesset Deputy Speaker (male) |
| 71 | סגנית יושב-ראש הכנסת | Knesset Deputy Speaker (female) |
| 73 | ראש הממשלה החילופי | Alternate PM (Bennett-Lapid era construct) |
| 122 | יושב–ראש הכנסת | Knesset Speaker (male) |
| 123 | יושבת–ראש הכנסת | Knesset Speaker (female) |
| 130 | ראשת האופוזיציה | Opposition Leader (female) |
| 131 | ראש האופוזיציה | Opposition Leader (male) |
| 663 | משקיף ועדה | Committee Observer |

**Important:** To list all MKs in a Knesset, filter `PositionID eq 43 or PositionID eq 61`. PositionID 54 is faction membership and is recorded separately from the MK role itself, filtering by 54 alone returns the wrong set.

## OData v4 Filter Syntax

- Equals: `field eq value`
- Not equals: `field ne value`
- Greater / less: `field gt value`, `field lt value`, `field ge value`, `field le value`
- Substring: `contains(Field, 'text')` (v4). In v3 this was `substringof('text', Field)`.
- And/Or: `condition1 and condition2`, `condition1 or condition2`
- Negation: `not (condition)`
- Set membership: `Field in (v1,v2,v3)`
- Null check: `Field eq null`
- Date: `Field gt 2024-01-01` (no `datetime'...'` wrapper, that was v3)
- Datetime: `Field gt 2024-01-01T00:00:00Z`
- `now()`: `Field gt now()` for "from this moment"
- String values in single quotes
- Numeric values without quotes
- URL-encode the entire `$filter` value when curling from a shell

## $expand syntax (v4)

```
# Simple expand
$expand=KNS_BillInitiator

# Expand with nested ordering
$expand=KNS_BillInitiator($orderby=IsInitiator desc,Ordinal)

# Expand with nested filter
$expand=KNS_DocumentBill($filter=GroupTypeID eq 5)

# Multiple expands
$expand=KNS_BillInitiator,KNS_DocumentBill,KNS_BillName

# Order by expanded field
$expand=KNS_Person&$orderby=KNS_Person/LastName
```

## Pagination

- Default page size varies by entity; explicitly set `$top` for predictable behavior.
- `$skip=N` for offset paging.
- Set `$count=true` to receive the total count alongside the page; pair with `$top=0` for count-only.
- v4 server-driven paging returns `@odata.nextLink` when more pages exist; follow until absent.

## Useful Constants

- Electoral status (2026-08-24): the **25th** Knesset (sworn in 2022-11-15) dissolved on **2026-07-17** and continues in office under the continuity rule until the 26th convenes. Election **2026-10-27**; 26th Knesset first sitting scheduled **2026-11-10**. Do not hardcode a "current Knesset" number: derive it from `KNS_KnessetDates?$filter=IsCurrent eq true`.
- Knesset size: 120.
- Electoral threshold: 3.25% (since 2014).
- Allocation formula: Bader-Ofer (modified D'Hondt / Hagenbach-Bischoff equivalent).
- KNS_CommitteeSession StatusID 193 = cancelled.
