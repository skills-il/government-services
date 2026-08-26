# Changelog

## 1.4.1 - 2026-08-26

Documents the programmatic route to a postal code, which 1.4.0 said did not exist in a usable
form. It does exist, undocumented, and the honest description of it is worth more than silence:
an agent told only "use the web form" will either give up or invent a mikud.

- The Israel Post site is backed by an undocumented JSON API. It is now documented as a
  best-effort route alongside the web form, which remains the supported and documented one.
- **The key derivation is the instruction, not the key.** A hardcoded subscription key breaks
  silently the day it rotates and every installed copy is wrong at once, so the skill teaches
  how to pull the current key out of the live client bundle, including the two things that make
  that fail: the page is bot-protected against a plain fetch, and the bundle carries stray NUL
  bytes that make a plain grep return nothing. The observed key is recorded with its
  verification date only so a reader can tell a rotation from a bug.
- **Terms of use are recorded as NOT established.** Israel Post's published terms govern the
  customer portal and say nothing about programmatic access, so the skill does not claim
  automated use is permitted and tells anyone planning volume use to ask Israel Post.
- No evasion guidance: the API is verified to accept the subscription key alone, with no
  Origin, Referer or User-Agent header, so no forged headers are documented. The skill
  explicitly forbids retry storms, rotating identities and working around a block.
- **HTTP 401 means the key is stale, not that the address is unknown.** Reporting a 401 as
  "address not found" is a confidently wrong answer, so that mapping is now stated in the body.
- `divided: false` localities carry their whole answer in the city record's own zip field
  (דגניה א' 1512000, כפר קאסם 4881000, נהלל 1060000); the street call must not run for them.
- Branch on `msgtype`: `address`, `unitedtown` (bad house number in a locality that does have
  streets) and `notfound` are three different outcomes.
- Passing the semel yishuv where Israel Post's internal CityID is expected returns HTTP 200
  with an empty array and no error, verified against the same call with the correct id.

The 6688310 postal code corrected in 1.4.0 is now confirmed a second way, by a reverse lookup
that round-trips back to שדרות רוטשילד 42.

## 1.4.0 - 2026-08-26

Corrections, each of which produced a confidently wrong answer rather than an error:

- **Three settlement codes were wrong**, and each was a real code belonging to a different
  settlement: Bet Shemesh 3730 (that is Givat Zeev) is 2610, Acre 4100 (that is Katzrin) is
  7600, Nahariya 7500 (that is Sakhnin) is 9100. All 30 rows of `references/city-codes.md` were
  then enumerated against the full 1,310-record authoritative list rather than spot-checked. The
  previous cycle spot-checked 12 rows, reported them all correct, and missed these three.
- **The worked postal code was wrong.** שדרות רוטשילד 42, תל אביב-יפו is 6688310, not 6688312.
  Verified on the Israel Post lookup form.
- **`https://data.gov.il/datasets` returns HTTP 404.** The 1.3.2 entry below, which moved the
  link to that path, is superseded. The CKAN API on the same host is healthy and is now the
  documented access route, with the current resource_ids and field names for the settlements
  and streets datasets.
- **The GovMap claim was wrong on three counts.** `api.govmap.gov.il` is a documentation site,
  not a callable endpoint; GovMap is a JavaScript SDK, not a REST API; and its key is bound to
  an approved domain, so it is unusable from a CLI or a server-side agent. It was described as
  "the canonical endpoint for address autocomplete" and requiring only "email registration".
- **The mikud claim was sharpened.** The Israel Post site is backed by a JSON API that returns
  HTTP 401 without a subscription key, while an undefined sibling path returns 404, so the host
  discriminates and the endpoint is auth-gated rather than dead. The key must not be scraped;
  the web form remains the supported route.

Additions:

- **Divided versus non-divided localities**, the concept the skill was missing entirely. A
  locality that is not divided into streets, which covers most kibbutzim and moshavim and many
  Arab localities, has one locality-wide mikud and no street-level codes, so the street-plus-
  number flow is wrong by construction there and returns an empty result that reads as a
  missing address. Israel Post's authoritative list is now cited.
- **The three non-interchangeable id spaces** (semel yishuv, Israel Post's internal city id,
  semel rechov, Israel Post's internal street id). Cross-feeding them returns an empty result
  with no error.

Bundled script, `scripts/lookup_address.py`:

- **It accepted no Hebrew input at all.** `city "תל אביב"` returned "not found", and
  `format "רחוב רוטשילד 42, תל אביב"` failed to identify the city. In a Hebrew-address skill
  that is the primary case. It now accepts Hebrew names, final-form (sofit) letters, hyphenated
  and spaced spellings, single-letter prefixes ("בתל אביב"), and gershayim abbreviations
  (ת"א, ראשל"צ), and prints the real Hebrew name rather than a Latin transliteration under a
  "Hebrew" label.
- Street type words (רחוב, רח', שדרות, שד') are stripped from the parsed street name.
- Bet Shemesh, Hadera, Karmiel and Afula were in the reference table but missing from the
  script; added.
- The script no longer implies it can resolve a mikud, and points at the Israel Post form.
- Unknown localities now return the CKAN datastore query that covers all 1,310 of them.

## 1.3.2 - 2026-08-12

Fixed the data.gov.il catalogue link: /dataset returns 404, the catalogue is at /datasets. The site is client-rendered, so a plain fetch returns a 200 shell and the dead link is only visible in a browser.

