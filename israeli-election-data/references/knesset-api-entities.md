# Knesset OData API Entity Reference

## Base URL
`https://knesset.gov.il/Odata/ParliamentInfo.svc/`

## Query Format
```
GET {BASE}/{ENTITY}?$format=json&$filter={FILTER}&$top={LIMIT}&$select={FIELDS}
```

## Key Entities

### KNS_Person
Person (MK, minister, etc.) information.
- PersonID, FirstName, LastName, GenderID, GenderDesc, Email

### KNS_PersonToPosition
Position history (MK terms, ministerial roles).
- PersonToPositionID, PersonID, PositionID, KnessetNum, FactionID, FactionName

### KNS_MkSiteCode
MK website information.
- MKSiteCode, KnsID, FirstName, LastName

### KNS_Faction
Political parties/factions.
- FactionID, Name, KnessetNum

### KNS_Bill
Legislative bills.
- BillID, Name, KnessetNum, StatusID, SubTypeID

### KNS_BillInitiator
Bill sponsors.
- BillInitiatorID, BillID, PersonID

### KNS_VoteMain
Main vote records.
- VoteID, SessionID, ItemID, TypeID, StatusID, AcceptedText, TopicText, KnessetNum

### KNS_VoteDetail
Individual MK votes.
- VoteDetailID, VoteID, PersonID, VoteValue, FirstName, LastName, FactionName
- VoteValue: 1=For, 2=Against, 3=Abstain, 4=Absent

### KNS_CmtSessionItem
Committee session items.
- CmtSessionItemID, ItemID, CmtSessionID

### KNS_PlmSessionItem
Plenum session items.
- PlmSessionItemID, ItemID, PlenumSessionID

## OData Filter Syntax
- Equals: `field eq value`
- Contains: `substringof('text', Field)`
- And/Or: `condition1 and condition2`
- String values in single quotes
- Numeric values without quotes

## Position IDs
- 54 = Member of Knesset (MK)
- 39 = Prime Minister
- 12 = Minister
