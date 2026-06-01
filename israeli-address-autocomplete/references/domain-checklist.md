# Domain coverage checklist, israeli-address-autocomplete

Anchor for expert review. Scope: format/validate/geocode Israeli addresses, CBS city codes, postal codes (mikud).

## Must cover (core)
- Address format (street, number, city, mikud) + Hebrew/English transliteration.
- CBS settlement (semel yishuv) codes for major cities; ~1,270 localities; resolve via data.gov.il / CBS.
- 7-digit postal code (mikud, since 1.2.2013); lookup via Israel Post web form (no official public API).
- Granular form fields (apartment/floor/entrance/PO box/gush-helka/sub-parcel/settlement code); kibbutz/moshav no-street case.
- gush/helka by address: Survey of Israel tool (gov.il/apps/mapi/parcel_address) + GovMap.
- Programmatic geocoding: GovMap API (api.govmap.gov.il); data.gov.il CKAN datastore for streets/localities.

## Out of scope (explicit)
- Non-Israeli addresses (per description).

## Authoritative sources
- CBS: https://www.cbs.gov.il
- data.gov.il: https://data.gov.il/dataset
- Israel Post mikud: https://doar.israelpost.co.il/locatezip
- GovMap API: https://api.govmap.gov.il
- Survey of Israel parcel tool: https://www.gov.il/apps/mapi/parcel_address/parcel_address.html
