# Domain Coverage Checklist - israeli-media-authenticity-verifier

Generated 2026-06-05. Re-litigated 2026-08-18 (v1.1.0). This is the coverage contract the skill is maintained against.
Source references below are written as bare domains (no scheme) on purpose: they are
maintenance pointers, not factual claims rendered to users. The factual claims that ARE
asserted in the skill body live in evidence.json with full source URLs and verbatim
snippets.

## Must cover (core)

- [x] C2PA Content Credentials model: manifest = signed claim about creator, tool (incl. AI), edits. source: spec.c2pa.org, opensource.contentauthenticity.org. why core: only cryptographically conclusive layer.
- [x] c2patool read/verify, with install: provided as scripts/check_provenance.py + brew install. source: opensource.contentauthenticity.org/docs/sdk-repos/c2pa-rs/cli. why core: the runnable provenance check.
- [x] Content Credentials Verify tool (no-code path): verify.contentauthenticity.org. why core: the non-technical Israeli user path.
- [x] SynthID watermark + its access path + limits. source: deepmind.google/science/synthid. why core: dominant production watermark.
- [x] Watermark/credential limitation: screenshot/re-encode strips them; absence proves nothing. why core: prevents over-trusting a null.
- [x] EXIF/metadata forensics via exiftool, with the absence-is-normal caveat: scripts/dump_metadata.py. source: exiftool.org. why core: cheapest first-pass layer.
- [x] Visual artifact inspection by the model, WITH the obsolete-tells caveat (hands/Latin text fixed). references/artifact-checklist.md. why core: the agent's native capability, must be framed as suggestive.
- [x] Video deepfake tells (temporal flicker, identity drift, motion warping), with blink cadence and lip-sync explicitly RETIRED as tells in 2026. scripts/extract_frames.py + checklist. why core: scope covers video, and the retired tells were producing false leans-authentic on the talking-head case.
- [x] Reverse-image search across multiple engines, earliest-appearance focus. references/source-tracing.md. why core: catches recycled media.
- [x] "Recycled / video-game / miscaptioned" failure mode as a distinct verdict. source: poynter.org. why core: dominant wartime category.
- [x] Reliability ceiling of automated AI-image detectors (NewsGuard finding), used as caveat. source: newsguardtech.com. why core: must never output a verdict on a detector score alone.
- [x] June 2025 Israel-Iran AI-misinformation anchor. source: eweek.com, carnegieendowment.org. why core: headline Israeli use case.
- [x] Israeli reporting channels scoped correctly (105 for minors; BOI/banks + police for fraud). source: gov.il, boi.org.il. why core: scope requires Israeli pointers.
- [x] Israeli election-period AI-labelling duty as a READ signal + the Elections Committee complaint route. source: law.co.il (Elections Law for the 26th Knesset, 5786-2026; chair's rules in force 26.07.2026). why core: in force since 26.07.2026, an election period is the most predictable source of Israeli synthetic media, and the label's presence or absence changes the reading.
- [x] SynthID is NOT Google-only (OpenAI embeds it via a Google partnership), so a hit must not be attributed to a vendor. source: openai.com/index/advancing-content-provenance. why core: mis-attribution corrupts the provenance verdict.
- [x] OpenAI Verify as a third free no-code provenance check, images + audio. source: openai.com/index/advancing-content-provenance. why core: the no-shell user path, and the only new audio provenance route since publication.
- [x] Blink cadence and lip-sync are OBSOLETE video tells (joint audio-video generation). source: deepmind.google/models/veo. why core: the false-negative on the talking-head case the skill exists for.
- [x] No reverse-video search exists; keyframe reverse-search + InVID/WeVerify is the substitute. source: bellingcat.com advanced video guide. why core: video is in scope and the user will otherwise hunt for a tool that does not exist.
- [x] Telegram provenance lane (forwarded-from chain, t.me/s/<channel>, sequential message IDs). why core: Telegram is named in the description and both examples.
- [x] Named geolocation/chronolocation tools (SunCalc, Google Earth Pro history, Mapillary, Overpass Turbo) + Israeli signage/plate specifics. why core: the previous prose was a method description, not an actionable method.
- [x] Pikud HaOref named official channels (oref.org.il, the official app, verified Telegram @PikudHaOref_all) and the third-party-app distinction. why core: the highest-urgency instruction in the skill was unactionable without them.
- [x] IPTC XMP DigitalSourceType (trainedAlgorithmicMedia / compositeSynthetic) read by dump_metadata.py. source: cv.iptc.org/newscodes/digitalsourcetype. why core: the one metadata field that DECLARES AI origin, and it survives when C2PA does not.
- [x] Adult-victim route for synthetic sexual imagery (StopNCII on-device hashing, ISOC helpline, police complaint), kept distinct from 105. source: stopncii.org/faq. why core: 105 is minors-only and the skill said so while leaving adults with no route.
- [x] Evidence preservation checklist attached to every reporting route. source: isoc.org.il sextortion guidance. why core: preservation is not certification, and it degrades hourly.
- [x] Israeli claim-rating desk identified correctly: המשרוקית (Globes, IFCN member since 2018); FakeReporter is a watchdog, not a fact-check desk. source: globes.co.il about page. why core: the skill told users to check an outlet without naming the right kind of body.
- [x] Legal notice covering re-share exposure (defamation publication is medium-agnostic; praise-framed violent content) + no-forensic-certification + no-identification. why core: every user is standing at a share button.
- [x] Sourced verdict report with explicit confidence level. references/verdict-report-template.md. why core: the skill's defining output.

## Should cover (advanced / edge cases)

- [x] Hebrew WhatsApp/Telegram stripped-forward triage lane (start from source tracing). references/israeli-context.md.
- [x] Error Level Analysis basics and its high false-positive caveat. scripts/dump_metadata.py --ela.
- [x] Geolocation + chronolocation (signage, sun/shadow, weather). references/source-tracing.md.
- [x] Signer-trust nuance: a present manifest is only as good as its signer. references/provenance.md.
- [x] Liar's-dividend framing: false "fake" is also harm. references/verdict-report-template.md.
- [x] Hand-off boundary to israeli-fact-checker for numeric/textual claims. SKILL.md description + MCP section.
- [x] Browser-extension tooling: InVID/WeVerify added on its own merits as the video keyframe + reverse-search tool. Generic in-page credential-checker extensions (Digimarc and similar) stay deferred to keep the skill tool-agnostic.
- [ ] scripts/extract_audio.py (ffmpeg to WAV + ffprobe container dump + optional spectrogram) so the audio lane has runnable support. (deferred to next cycle, logged in optimization-log.json)
- [ ] extract_frames.py modernisation: -fps_mode instead of deprecated -vsync, exposed --scene-threshold, I-frame-only mode for heavy re-encodes. (deferred, logged)

## Out of scope (explicit, with rationale)

All rows re-litigated 2026-08-18 against the two tests (would an ordinary user plausibly ask
for this, and has it become capturable). Three rows failed and were reopened; they are now
in-scope content and are recorded here only as history.

- Generating, removing, or evading deepfakes/watermarks: this is a verifier, not a forgery or evasion tool. SURVIVES both tests (2026-08-18); a verifier that teaches watermark stripping is a forgery tool.
- A definitive binary "fully-AI versus fully-real" verdict: every layer is probabilistic. SURVIVES both tests (2026-08-18); the five-verdict scheme with an explicit inconclusive is the correct answer to the user's ask, not a refusal of it.
- Numeric/textual claim fact-checking: owned by israeli-fact-checker. SURVIVES both tests (2026-08-18); handoff now also names המשרוקית as the external claim-rating desk.
- Wrapping a commercial AI-detector API as an MCP server: SURVIVES both tests (2026-08-18); would manufacture the false-precision score honesty rule 3 exists to prevent.
- REOPENED 2026-08-18, formerly "Real-time live-call / deepfake-stream interception": the old rationale was an implementation detail (we take files) dressed as a scope boundary, and live-call impersonation is now a mainstream ask. A bounded live-call lane is now IN scope in references/israeli-context.md (liveness probe as convict-only, callback on a held number, safe word). Interception, recording and real-time classifiers remain out of scope.
- REOPENED (bounded) 2026-08-18, formerly "Face-based person identification / doxxing": the permitted half (verification against a claimed known identity) was never actually taught, so the row hid a gap rather than closing one. Verification-only face search is now IN scope and the identification prohibition is now stated in user-facing text with its Privacy Protection Law reason, instead of living only in this checklist. Identifying unknown persons stays excluded.
- REOPENED (split) 2026-08-18, formerly "Court-admissible forensic certification": issuing a certification or expert opinion stays OUT of scope. Evidence PRESERVATION is a different act, is asked for the moment the skill says "report this", and is now IN scope as a checklist attached to every reporting route.

## Authoritative sources (bare domains; full URLs + snippets in evidence.json)

- spec.c2pa.org, opensource.contentauthenticity.org/docs/sdk-repos/c2pa-rs/cli - C2PA model + c2patool.
- verify.contentauthenticity.org - no-code verify tool (old contentcredentials address redirects here).
- deepmind.google/science/synthid - SynthID coverage + limits.
- exiftool.org - metadata extraction.
- newsguardtech.com - AI-detector reliability finding.
- poynter.org - recycled/miscaptioned footage as dominant fake.
- eweek.com, carnegieendowment.org - June 2025 Israel-Iran misinformation flood.
- getclarity.ai - April 2025 manipulated-broadcast incident.
- openai.com/index/advancing-content-provenance - OpenAI Verify, C2PA conformance, cross-platform SynthID.
- deepmind.google/models/veo - joint audio-video generation (why blink/lip-sync tells are dead).
- cv.iptc.org/newscodes/digitalsourcetype - trainedAlgorithmicMedia / compositeSynthetic.
- law.co.il - Israeli election AI-labelling duty and the chair's disclosure rules.
- stopncii.org - adult NCII / synthetic-image takedown by on-device hashing.
- globes.co.il - המשרוקית, IFCN member since 2018.
- bellingcat.com - no reverse-video search; geolocation method.
- t.me/s/PikudHaOref_all, oref.org.il - official Home Front Command channels.
- gov.il/en/departments/units/105_call_center - 105 child-online-protection reporting.
- boi.org.il - impersonation-fraud warning.
- fakereporter.net - Israeli disinformation watchdog.
