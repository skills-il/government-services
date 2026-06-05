# Domain Coverage Checklist - israeli-media-authenticity-verifier

Generated 2026-06-05. This is the coverage contract the skill is maintained against.
Source references below are written as bare domains (no scheme) on purpose: they are
maintenance pointers, not factual claims rendered to users. The factual claims that ARE
asserted in the skill body live in evidence.json with full source URLs and verbatim
snippets.

## Must cover (core)

- [x] C2PA Content Credentials model: manifest = signed claim about creator, tool (incl. AI), edits. source: spec.c2pa.org, opensource.contentauthenticity.org. why core: only cryptographically conclusive layer.
- [x] c2patool read/verify, with install: provided as scripts/check_provenance.py + brew install. source: opensource.contentauthenticity.org/docs/c2patool. why core: the runnable provenance check.
- [x] Content Credentials Verify tool (no-code path): contentcredentials.org/verify. why core: the non-technical Israeli user path.
- [x] SynthID watermark + its access path + limits. source: deepmind.google/science/synthid. why core: dominant production watermark.
- [x] Watermark/credential limitation: screenshot/re-encode strips them; absence proves nothing. why core: prevents over-trusting a null.
- [x] EXIF/metadata forensics via exiftool, with the absence-is-normal caveat: scripts/dump_metadata.py. source: exiftool.org. why core: cheapest first-pass layer.
- [x] Visual artifact inspection by the model, WITH the obsolete-tells caveat (hands/Latin text fixed). references/artifact-checklist.md. why core: the agent's native capability, must be framed as suggestive.
- [x] Video deepfake tells (blink, lip-sync, temporal flicker, identity drift). scripts/extract_frames.py + checklist. why core: scope covers video.
- [x] Reverse-image search across multiple engines, earliest-appearance focus. references/source-tracing.md. why core: catches recycled media.
- [x] "Recycled / video-game / miscaptioned" failure mode as a distinct verdict. source: poynter.org. why core: dominant wartime category.
- [x] Reliability ceiling of automated AI-image detectors (NewsGuard finding), used as caveat. source: newsguardtech.com. why core: must never output a verdict on a detector score alone.
- [x] June 2025 Israel-Iran AI-misinformation anchor. source: eweek.com, carnegieendowment.org. why core: headline Israeli use case.
- [x] Israeli reporting channels scoped correctly (105 for minors; BOI/banks + police for fraud). source: gov.il, boi.org.il. why core: scope requires Israeli pointers.
- [x] Sourced verdict report with explicit confidence level. references/verdict-report-template.md. why core: the skill's defining output.

## Should cover (advanced / edge cases)

- [x] Hebrew WhatsApp/Telegram stripped-forward triage lane (start from source tracing). references/israeli-context.md.
- [x] Error Level Analysis basics and its high false-positive caveat. scripts/dump_metadata.py --ela.
- [x] Geolocation + chronolocation (signage, sun/shadow, weather). references/source-tracing.md.
- [x] Signer-trust nuance: a present manifest is only as good as its signer. references/provenance.md.
- [x] Liar's-dividend framing: false "fake" is also harm. references/verdict-report-template.md.
- [x] Hand-off boundary to israeli-fact-checker for numeric/textual claims. SKILL.md description + MCP section.
- [ ] Browser-extension in-page credential checkers (Digimarc and similar): mention as a lower-friction option. (deferred: keep skill tool-agnostic for now)

## Out of scope (explicit, with rationale)

- Generating, removing, or evading deepfakes/watermarks: this is a verifier, not a forgery or evasion tool.
- A definitive binary "fully-AI versus fully-real" verdict: every layer is probabilistic.
- Court-admissible forensic certification: assistive triage only; point users with legal stakes to professionals.
- Face-based person identification / doxxing: face search is for verification only; identification use excluded for privacy (Amendment 13).
- Real-time live-call / deepfake-stream interception: out of scope for a file/URL workflow.
- Numeric/textual claim fact-checking: owned by israeli-fact-checker.

## Authoritative sources (bare domains; full URLs + snippets in evidence.json)

- spec.c2pa.org, opensource.contentauthenticity.org/docs/c2patool - C2PA model + c2patool.
- contentcredentials.org/verify - no-code verify tool.
- deepmind.google/science/synthid - SynthID coverage + limits.
- exiftool.org - metadata extraction.
- newsguardtech.com - AI-detector reliability finding.
- poynter.org - recycled/miscaptioned footage as dominant fake.
- eweek.com, carnegieendowment.org - June 2025 Israel-Iran misinformation flood.
- getclarity.ai - April 2025 manipulated-broadcast incident.
- gov.il/en/departments/units/105_call_center - 105 child-online-protection reporting.
- boi.org.il - impersonation-fraud warning.
- fakereporter.net - Israeli disinformation watchdog.
