# Knesset OData API Entity Reference

## Base URL
`https://knesset.gov.il/Odata/ParliamentInfo.svc/`

OData v3 service. Root URL returns the live entity list.

## Query Format
```
GET {BASE}/{ENTITY}?$format=json&$filter={FILTER}&$top={LIMIT}&$select={FIELDS}
```

## Available Entities (38, as of 2026-05)

People and positions:
- `KNS_Person` -- MKs, ministers, other parliamentary figures.
- `KNS_PersonToPosition` -- Position history (MK terms, ministerial roles).
- `KNS_Position` -- Position-ID lexicon (see below).
- `KNS_MkSiteCode` -- MK website / personal page identifiers.

Factions:
- `KNS_Faction` -- Political factions per Knesset.

Bills and legislation:
- `KNS_Bill` -- Legislative bills.
- `KNS_BillName` -- Bill titles (multiple versions / readings).
- `KNS_BillInitiator` -- Current bill sponsors.
- `KNS_BillHistoryInitiator` -- Historical sponsor records.
- `KNS_BillSplit` -- Records of bills split during legislative process.
- `KNS_BillUnion` -- Records of bills merged during legislative process.

Committees:
- `KNS_Committee` -- Knesset committees.
- `KNS_CommitteeSession` -- Committee sessions.
- `KNS_CmtSessionItem` -- Items discussed in committee sessions.
- `KNS_CmtSiteCode` -- Committee website identifiers.
- `KNS_JointCommittee` -- Joint committees.

Plenum:
- `KNS_PlenumSession` -- Plenum sessions.
- `KNS_PlmSessionItem` -- Items on plenum agendas.

Laws:
- `KNS_Law` -- Knesset law records.
- `KNS_LawBinding` -- Law-to-Knesset binding records.
- `KNS_IsraelLaw` -- Israeli law records.
- `KNS_IsraelLawName` -- Israeli law titles.
- `KNS_IsraelLawBinding` -- Israeli law-to-Knesset binding.
- `KNS_IsraelLawClassificiation` -- Law classification (note: typo in upstream API).
- `KNS_IsraelLawMinistry` -- Law-to-ministry mapping.

Documents:
- `KNS_DocumentAgenda` -- Agenda documents.
- `KNS_DocumentBill` -- Bill documents.
- `KNS_DocumentCommitteeSession` -- Committee session documents.
- `KNS_DocumentIsraelLaw` -- Israeli law documents.
- `KNS_DocumentLaw` -- Knesset law documents.
- `KNS_DocumentPlenumSession` -- Plenum session documents.
- `KNS_DocumentQuery` -- Parliamentary query documents.

Other:
- `KNS_KnessetDates` -- Start and end dates of each Knesset.
- `KNS_GovMinistry` -- Government ministries.
- `KNS_Status` -- Status code lookup (bill statuses, etc.).
- `KNS_Agenda` -- Agenda items.
- `KNS_Query` -- Parliamentary queries.
- `KNS_ItemType` -- Item type lookup.

## Entities NOT in the public OData service

The following entities exist in the Knesset's internal database but are **not exposed publicly** via `ParliamentInfo.svc`. Requests return `Resource not found for the segment`:

- `KNS_VoteMain` -- main plenum vote records.
- `KNS_VoteDetail` -- individual MK votes.

For per-MK vote data, use `hasadna/knesset-data` (GitHub) or scrape `https://main.knesset.gov.il/Activity/plenum/Pages/SessionVotes.aspx`.

## Common Field Names

### KNS_Person
- `PersonID`, `FirstName`, `LastName`, `GenderID`, `GenderDesc`, `Email`, `LastUpdatedDate`

### KNS_PersonToPosition
- `PersonToPositionID`, `PersonID`, `PositionID`, `KnessetNum`, `FactionID`, `FactionName`, `GovernmentNum`, `StartDate`, `FinishDate`

### KNS_Faction
- `FactionID`, `Name`, `KnessetNum`, `StartDate`, `FinishDate`

### KNS_Bill
- `BillID`, `Name`, `KnessetNum`, `StatusID`, `SubTypeID`, `LastUpdatedDate`

### KNS_BillInitiator
- `BillInitiatorID`, `BillID`, `PersonID`

### KNS_Committee
- `CommitteeID`, `Name`, `KnessetNum`, `StartDate`, `FinishDate`

### KNS_CommitteeSession
- `CommitteeSessionID`, `Number`, `KnessetNum`, `TypeID`, `TypeDesc`, `CommitteeID`, `StartDate`, `FinishDate`

### KNS_KnessetDates
- `KnessetDateID`, `KnessetNum`, `Name`, `StartDate`, `FinishDate`, `IsCurrent`

## Position IDs (PositionID values)

Verified against live `KNS_Position` endpoint, 2026-05-20:

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

**Important:** To get all MKs in a Knesset, filter `PositionID eq 43 or PositionID eq 61`. PositionID 54 is faction membership, NOT MK status (faction membership applies to many roles, including senate-style affiliations).

## OData v3 Filter Syntax

- Equals: `field eq value`
- Not equals: `field ne value`
- Greater / less: `field gt value`, `field lt value`, `field ge value`, `field le value`
- Contains: `substringof('text', Field)` -- **NOT** `contains(Field, 'text')` (that's v4 and will fail)
- And/Or: `condition1 and condition2`, `condition1 or condition2`
- Negation: `not (condition)`
- Date: `Date gt datetime'2022-11-15'`
- String values in single quotes
- Numeric values without quotes
- URL-encode the entire `$filter` value when curling from a shell

## Pagination

Default response size is 100. Use `$top=N` to request up to ~250 per page. For more, page with `$skip=N` (OData v3 server-driven paging may also return a `next` link).

## Useful Constants

- Current Knesset (2026-05): **25** (sworn in 2022-11-15, next election no later than 2026-10-27).
- Knesset size: 120.
- Electoral threshold: 3.25% (since 2014).
- Allocation formula: Bader-Ofer (modified D'Hondt / Hagenbach-Bischoff equivalent).
