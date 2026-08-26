# Domain coverage checklist, israeli-address-autocomplete

Anchor for expert review. Scope: format, validate and structure Israeli addresses, resolve
settlement (semel yishuv) codes, and route the user to a working postal-code (mikud) lookup.

## Must cover (core)

1. Address structure: street, house number, locality, mikud, plus the granular form fields
   (apartment, floor, entrance, ת.ד., gush/helka, sub-parcel, semel yishuv).
2. Hebrew input as the primary case, including final-form (sofit) letters, hyphenated and
   spaced spellings, single-letter prefixes ("בתל אביב"), and gershayim abbreviations
   (ת"א, ראשל"צ). The bundled script must accept all of these.
3. Settlement codes resolved against the authoritative 1,310-record list, not a hand-kept
   subset. Every row of any bundled code table must be diffed against the full list, because
   a wrong code in this domain is a real code belonging to a DIFFERENT settlement, so the
   skill answers confidently wrong rather than erroring.
4. **Divided versus non-divided localities.** Israel Post marks each locality. A non-divided
   locality (most kibbutzim and moshavim, many Arab localities) has ONE locality-wide mikud
   and no street-level codes, so the street-plus-number flow is wrong by construction there
   and returns an empty result that reads as a missing address.
5. The three non-interchangeable id spaces: semel yishuv, Israel Post's internal city id,
   semel rechov, and Israel Post's internal street id. Cross-feeding them returns an empty
   result with no error.
6. Postal-code lookup: the supported route and its limits. There is no keyless public
   mikud-by-address API; the backing JSON API requires a subscription key.
7. Programmatic access to settlements and streets: the data.gov.il CKAN datastore, with the
   current resource_ids and field names.
8. gush/helka by address via the Survey of Israel tool or GovMap.
9. Kibbutz and moshav addressing with no street name.
10. Multiple valid transliterations and Hebrew/Arabic name variants; normalise before matching.

## Should cover (advanced)

11. Ambiguous locality names sharing a prefix; disambiguate by semel yishuv and nafa.
12. New neighbourhoods whose mikud differs from the parent city, and why a cached mikud goes
    stale.
13. ת.ד. addresses, which carry their own mikud distinct from a street address.
14. English-language lookup where the source supports it.

## Out of scope (explicit)

- Non-Israeli addresses. Stated in the description; a different problem domain entirely.
- Routing, distance and travel time. This skill resolves and formats addresses; it is not a
  mapping or navigation tool.
- Reverse geocoding from coordinates. GovMap covers it, but it is browser-only in practice
  (domain-locked API key), so the skill cannot offer an agent-usable path. Re-open if a keyless
  reverse-geocode source appears.
- Bulk mikud enrichment as an automated service. Reopened and re-answered 2026-08-26: an
  ordinary user WOULD ask for this (the batch-validation example invites it), and the honest
  answer is now stated in the skill rather than left silent: the settlement and street halves
  can be automated against the CKAN datastore, the mikud half cannot, because the only
  mikud source is a key-gated API whose key must not be scraped. That is a real answer, not a
  refusal.
- Property ownership and tabu records. The skill surfaces gush/helka as a form field and points
  at the official tool; reading the register itself is a different domain.

## Authoritative sources

- data.gov.il CKAN API: <https://data.gov.il/api/3/action/package_search>
  - settlements resource_id `5c78e9fa-c2e2-4771-93ff-7f400a12f7ba` (1,310 records)
  - streets resource_id `9ad3862c-8391-4b2f-84a4-2d4c68625f4b`
  - both published by רשות האוכלוסין וההגירה
- Israel Post mikud form: <https://doar.israelpost.co.il/locatezip>
- Israel Post localities with no delivery address: <https://doar.israelpost.co.il/content/no-address>
- Survey of Israel parcel tool: <https://www.gov.il/apps/mapi/parcel_address/parcel_address.html>
- GovMap developer docs (browser-only SDK): <https://api.govmap.gov.il/docs/intro>
- CBS (statistical publications using the semel yishuv): <https://www.cbs.gov.il>

## Verification note for future cycles

The evidence gate extracts **zero numeric facts** from this skill, because settlement codes are
bare integers in table cells and match none of the gate's currency, percentage or threshold
patterns. The gate therefore cannot catch a wrong settlement code, and did not catch the three
that were live from before this cycle. **Codes must be enumerated against the full authoritative
list by hand every cycle**; a green gate here says nothing about them.

## Expert-review disposition, cycle v1.4.0 (2026-08-26)

The Expert Review raised 4 CRITICAL findings. None was deferred; all four were fixed and each
was reproduced against the primary source or by running the script before being acted on.

| Finding | Resolution |
|---|---|
| The script swallowed apartment, floor, entrance and ת.ד. tokens into the street name (`format "רוטשילד 42 דירה 5, תל אביב"` returned street `רוטשילד דירה 5`) | Reproduced. The parser now extracts each granular component into its own field before deciding what is left is the street, and prints them as labelled form fields. A ת.ד. address with no street now formats correctly and states that a PO box carries its own mikud. |
| The script invented a street name for kibbutz and moshav addresses (`"משק 12, מושב נהלל"` returned street `משק מושב נהלל`), the exact case the prose documents | Reproduced. Locality-type words (משק, מושב, קיבוץ, כפר, שכונת) are now recognised, the no-street path prints locality plus plot number, and it routes the user to the Israel Post no-address list. |
| Example 3 promised a "validated CSV with postal codes" for 500 rows while the same skill states there is no mikud API | Rewritten in both languages to lead with what cannot be automated, to leave the mikud column deliberately empty with a per-row reason, and to report the count of rows needing manual lookup. |
| The מען (registered address) versus delivery address distinction was absent, which is the actual failure at a Bituach Leumi counter and the literal first user prompt | Added as a table in Step 1 in both languages, plus a line in the script's own output. The skill now says it cannot read the population registry and routes the user to the ספח and to a change-of-address notice. |

MAJOR findings fixed in the same pass, each verified against the live dataset first:

- All 1,310 `שם_ישוב` values carry trailing whitespace, so an exact join returns nothing.
- Bedouin (שבט) and (יישוב) pairs share a Latin name across different settlement codes
  (968/1342, 986/1321, 970/1346), which is the domain's signature wrong-but-real-code failure
  in a form that enumerating 30 large cities can never surface.
- `שם_ישוב_לועזי` is truncated at 20 characters on 15 rows and empty on others, so it is not a
  join key.
- Every locality has a `סמל_רחוב = 9000` self-row (exactly 1,310 of 63,571 street rows), which
  is both a trap when listing streets and the machine-readable non-divided test that works at
  CSV scale.
- No precedence rule existed for when the registry and Israel Post disagree. Now stated:
  registry for a form's locality and street fields, Israel Post for the mikud, surface the
  conflict rather than choosing silently.

MAJOR findings carried to `optimization-log.json` rather than fixed this cycle: East Jerusalem
and Area C addressing; merged and renamed localities and whether retired codes persist;
multi-entrance buildings beyond parsing the field.
