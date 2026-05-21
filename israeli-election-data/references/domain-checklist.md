# Domain Checklist: Israeli Election Data

Coverage anchor for the expert-review pipeline. The skill should be evaluated against this list, not against an open-ended "what could be useful".

## Must cover (core)

- Knesset OData v4 base URL and entity-discovery via the service root. Source: live API at `https://knesset.gov.il/OdataV4/ParliamentInfo/`.
- v4 filter syntax (`contains`, `in`, ISO 8601 datetimes, no `datetime'...'` wrapper). Source: OData v4 spec at `https://www.odata.org`.
- v3 fallback callout (legacy endpoint at `/Odata/ParliamentInfo.svc/` still up but does not expose vote tables). Source: live API.
- The two vote entities `KNS_PlenumVote` and `KNS_PlenumVoteResult` with `VoteTitle`, `MkId`, `ResultDesc` fields. Source: live API metadata + sample rows.
- PositionID lexicon at minimum: 43 (MK male), 61 (MK female), 45 (PM), 39/57 (Minister), 41 (Committee Chair), 42 (Committee Member), 122/123 (Knesset Speaker), 54 (faction member, with the explicit note that 54 ≠ MK role).
- Bill status codes for the common transitions: 108 (prep for 1st reading), 118 (approved 3rd reading = became law), 125 (rejected). Source: hasadna/knesset-data status_id mapping + live KNS_Status table.
- Electoral threshold = 3.25% since the March 2014 amendment (was 2% before). Source: Knesset Lexicon, IDI.
- Knesset size = 120 (unchanged since 1949). Source: Basic Law: The Knesset §3.
- Seat allocation = Bader-Ofer (modified D'Hondt). Source: Knesset Lexicon.
- 2022 election (25th Knesset) seat distribution. Source: Wikipedia 2022 Israeli legislative election, cross-confirmed with IDI.
- data.gov.il `votes-knesset` dataset for per-locality / per-ballot CSVs (Knessets 16-25). Source: data.gov.il CKAN package_show.
- 2024 municipal elections summary (Feb 27 + March 10 runoff + Nov 2024 evacuated-localities round; ~49.5% turnout). Source: IDI 2024 local elections analysis, Knesset RIC fact sheet.
- `votes.gov.il` is dead; canonical Central Elections Committee site is `bechirot.gov.il`. Source: direct DNS probe.
- Hebrew-encoding caveat for older `votes-knesset` CSVs (Windows-1255 for Knessets 16-20, UTF-8 with BOM for 21+). Source: empirical observation.

## Should cover (advanced)

- `KNS_Query` parliamentary questions and the `GovMinistryID` (integer) vs nonexistent `GovMinistryName` distinction. Source: live API metadata.
- `KNS_Agenda` agenda proposals. Source: live API.
- `KNS_IsraelLaw` enacted law corpus and the `KNS_IsraelLawClassificiation` intentional-typo gotcha. Source: live API.
- `KNS_SecondaryLaw` for regulations / orders / decrees. Source: live API.
- `$expand` syntax with nested ordering and nested filters (for bill -> initiators, vote -> session, etc.). Source: OData v4 spec.
- Pagination via `@odata.nextLink` and the `$count=true` + `$top=0` count-only pattern. Source: OData v4 spec.
- `KNS_CommitteeSession.StatusID = 193` cancelled-session filter. Source: live API.
- `KNS_PlmSessionItem.Ordinal` sorting is broken (known API bug). Source: hasadna/knesset-data community notes.
- Knesset 0 = Provisional State Council; data quality improves from Knesset 17+. Source: Knesset databases portal.
- Government composition queries via `KNS_PersonToPosition` with `PositionID eq 39/57/45`. Source: live API.
- Coalition agreements at `gov.il/he/Departments/policies` and PMO publications. Source: gov.il navigation.
- Party financing reports at `mevaker.gov.il`. Source: State Comptroller site.
- Voter registration check at `gov.il/he/service/check_voter_registration`. Source: Ministry of Interior site.
- Surplus-vote agreements (`heskemei odafim`) mechanic. Source: Times of Israel "How Bader-Ofer Really Works", Knesset Lexicon.

## Out of scope (explicit)

- Political opinion, prediction, or punditry. The skill returns raw and structured data; interpretation is the user's job.
- Non-Israeli elections. Different system, different sources.
- Pre-1949 elections (the State of Israel did not exist).
- Knesset member personal opinions, social-media content, or private statements. Skill covers official records only.
- Real-time results during election night, the official feeds are operational only after the Central Elections Committee certifies counts.
- Litigation around election integrity (Bagatz petitions, etc.). Adjacent and important but handled by Bagatz/legal-research skills, not this one.
- Coalition negotiation drafts or unofficial leaks, only published agreements live here.

## Authoritative sources

- `https://knesset.gov.il/OdataV4/ParliamentInfo/` (live API root)
- `https://knesset.gov.il/OdataV4/ParliamentInfo/$metadata` (full schema)
- `https://main.knesset.gov.il/activity/info/pages/databases.aspx` (Knesset databases portal)
- `https://main.knesset.gov.il/EN/About/Lexicon/Pages/seats.aspx` (Bader-Ofer, threshold, seat math)
- `https://data.gov.il/dataset/votes-knesset` (Central Elections Committee CSVs)
- `https://www.bechirot.gov.il/` (Central Elections Committee live site)
- `https://en.idi.org.il/` (Israel Democracy Institute, post-election analysis)
- `https://github.com/hasadna/knesset-data` (community ETL of internal Knesset DBs)
- `https://www.odata.org` (OData v4 spec)
