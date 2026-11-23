---
name: israeli-media-authenticity-verifier
description: "Run a structured check on whether an image or video is AI-generated, digitally manipulated, or authentic-but-miscaptioned, and produce a sourced verdict with a confidence level. Use when a user forwards a dramatic war or news photo or clip on WhatsApp or Telegram and asks if it is real, when a journalist or community moderator needs a repeatable verification report before sharing or debunking, or when someone gets a suspicious image or voice claiming to be a known person. Combines cryptographic provenance (C2PA Content Credentials, SynthID, EXIF metadata), the agent's own visual inspection against an artifact checklist, and source tracing (reverse-image search, earliest-appearance, geolocation). This is a verifier, not a magic detector: it never claims certainty from one signal and says can't-verify when evidence is thin. Do NOT use for numeric or textual claim fact-checking (use israeli-fact-checker), for generating or removing deepfakes, or as court-admissible forensic certification."
license: MIT
compatibility: "Needs an agent with image vision plus a local shell (to run the provenance and metadata scripts) and web access (for reverse-image search). Degrades to a manual checklist on agents without a shell."
---

# Israeli Media Authenticity Verifier

## Legal notice

This skill produces an assistive verification summary. It is not legal advice, not a forensic certification, and not admissible expert evidence. What it is, positively: a structured record of which signals were found, which were absent, and how much weight each carries. It performs no chain-of-custody handling, no bit-level forensic analysis of the file, and no laboratory-grade classification, which are the steps a qualified examiner performs and which is why its output is not one. It does not determine whether any publication is lawful, and it does not identify people. Where the stakes are legal (defamation, a criminal complaint, an election-propaganda dispute, employment or custody consequences), the user needs a licensed lawyer and, for evidentiary purposes, a qualified forensic examiner.

Note also that the user is usually about to forward something, and forwarding is not a neutral act. Israeli defamation law defines publication broadly rather than by medium, so a forward may itself amount to publishing the content. Separately, sharing violent or terror-related material with approving framing may carry criminal exposure, quite apart from whether the footage is authentic. The election disclosure duty is written to apply to a person who publishes such propaganda, and it does not say it is limited to parties or candidates, so forwarding synthetic campaign material may raise this question too. Military censorship restrictions on publishing strike locations may also apply, including when forwarding real footage, so check before sharing. These are questions for a lawyer on the specific facts. This skill only flags that the exposures exist; it does not assess them and does not tell the user where the line falls.

This is a free information tool operated by an AI model, with no involvement, review or approval by an expert examiner, and it can be wrong. Do not present the output as an expert opinion or submit it as evidence. It is not a substitute for advice that takes into account the specific facts and needs of each person, and any use of it is the user's responsibility.

## Problem

Israelis are flooded with images and videos forwarded on WhatsApp and Telegram, especially during security events, and it is genuinely hard to tell what is real. The June 2025 Iran-Israel conflict was, in the words of experts, the first major conflict where generative AI shaped the information battlefield: fake clips of missile damage in Tel Aviv and at Ben Gurion Airport circulated, and flight-simulator footage passed off as real airstrikes reached over 21 million views before removal. Most people have no reliable way to check, and the automated "AI detector" websites are themselves unreliable, so a forwarded lie spreads faster than the correction.

## What this skill is (and is not)

This skill makes you a disciplined verifier, not a detector. There is no button that says "fake" or "real." Instead you combine four kinds of evidence, weight them, and report a verdict with an honest confidence level.

| Layer | What it checks | How conclusive |
|-------|----------------|----------------|
| 1. Provenance | C2PA Content Credentials, SynthID watermark, EXIF metadata | A declaration to check, never a verdict by itself; absence proves nothing |
| 2. Visual inspection | Your own vision against an artifact checklist | Suggestive, never proof |
| 3. Source tracing | Reverse-image search, earliest appearance, geolocation | Best for catching recycled or miscaptioned real media |
| 4. Ecosystem verifiers | Content Credentials Verify, OpenAI Verify, SynthID via the Gemini app | A hit is informative; a miss concludes nothing. Generic AI-detector sites stay unreliable |

**Four honesty rules, always:**
1. A missing Content Credential or watermark is NOT evidence that media is fake or real. Screenshotting and re-encoding strip these signals from real and fake content alike.
2. You cannot run a forensic AI-classifier yourself. Do not pretend to. Your vision pass is informed judgment, not a measurement.
3. Automated AI-image detector websites mislead users. A NewsGuard audit found such tools "declared authentic images to be AI-generated 13.33 percent of the time, and one tool got it wrong 40 percent of the time." Treat any detector score as one weak signal, never the verdict.
4. A common and often overlooked wartime fake is not a deepfake at all: it is real footage that is old or from another place, or game or simulator footage presented as real. As Poynter put it, viral war imagery is "often ... generated with artificial intelligence or else it's old footage misrepresented as if it's new." Always test "authentic but miscaptioned" and "not real footage".

## Instructions

Work the layers in order. Gather all four and weigh them. Credentials and metadata alone never decide a verdict.

### Step 0: Safety triage and intake

Before asking for or opening the file:

- **Stop rule, before anything else: if the item may be sexual imagery of a minor, real or AI-generated, whether attached or only described, stop the verification.** Do not analyze, describe, search, save, copy, screenshot, extract frames, run scripts on, upload or forward it. Tell the user to report it to 105 or the police, say where and when they received it, and follow their instructions about the file.
- **Siren or official alert right now:** follow Home Front Command instructions and go to the protected space. Verification can wait.
- **Intimate or sexual imagery of an adult:** do not ask to see it and send it to no external service. The person does not need to prove it is fake to get help, so go straight to the routes in Step 6.
- **Anyone else identifiable:** external services include verifiers, AI detectors, reverse-image engines and, on a hosted agent, the model that views the image, so let the user decide before attaching sensitive media. Do not upload media showing a minor or an identifiable private individual to any external verifier, detector, reverse-image or visual-search tool: use the local tools, the caption text, or a locally made crop with no person in it. The face rule in Step 3 applies to everyone, public figures included.

Then ask for the actual file if you only have a screenshot or a forwarded clip. A re-screenshotted image has lost its metadata and credentials, which changes what Layer 1 can do. Note the claim attached to the media ("this is Tel Aviv last night") separately from the media itself, because a real image with a false caption is a distinct verdict.

**If this is an active security incident, check the authoritative source first.** When the user is asking "is a missile hitting Tel Aviv right now," the fastest correct move is not forensics, it is the primary source: the Home Front Command (Pikud HaOref) official app and alerts, and established news desks. Tell the user not to re-share or act on an unconfirmed forward, and never to ignore an official alert because of one. Run the verification layers below in parallel, but never let the analysis delay the user from the real-time source.

**Try to recover the original.** Provenance and metadata survive only on the original file from the account or platform that first posted it. If you only have a forward, the highest-value step is to trace back to the earliest poster (see Step 3) and get their upload, or check whether the hosting platform shows its own "made with AI" label on the original post.

### Step 1: Provenance (run the scripts)

Provenance can show what a signer declared, so start here.

1. **Content Credentials (C2PA).** Run `c2patool` against the official trust list, save its output, then interpret the saved files:
   ```bash
   curl -fsSLO https://raw.githubusercontent.com/c2pa-org/conformance-public/main/trust-list/C2PA-TRUST-LIST.pem
   c2patool <file> trust --trust_anchors C2PA-TRUST-LIST.pem > report.json 2> report.err
   python scripts/check_provenance.py report.json --stderr report.err
   ```
   The script lists the declared actions and sources and gives no verdict. `Valid` means only that the signature and hashes check out, and anyone can produce it with their own certificate, so it is not verified. Only `Trusted` may be called signer-attested, and even then it is the signer's statement: it never makes an item authentic or AI-generated by itself, so always continue to source tracing. If the official list returns `Valid`, re-check against the frozen interim list (`references/provenance.md`), which older credentials may rely on. The Verify site still uses that list, so it can show a signer the official list does not. Record which list matched. `Invalid` may mean the file was changed or damaged. No manifest is the common case and means nothing on its own.
2. **Metadata (EXIF).** Save the `exiftool` output and interpret it:
   ```bash
   exiftool -json -G1 <file> > meta.json
   python scripts/dump_metadata.py meta.json
   ```
   This surfaces camera Make/Model, DateTimeOriginal, GPS, the Software field (an edit fingerprint), and the IPTC DigitalSourceType. `python scripts/dump_metadata.py --ela <image> <out.jpg>` writes an Error Level Analysis image as a hint for spliced regions. Read absence as "no signal," not as "fake." A script error means the check did not run, which is different from a clean null.
3. **No-code fallback (three free checks).** If you have no shell, these checks cover Layer 1, unless Step 0 bars the upload. In that case record "Layer 1 not run: upload barred to protect a person in the media", check the platform label on the original post, and continue with Steps 2 and 3. Each of these is ecosystem-scoped, so a hit is informative and a miss concludes nothing:
   - **Content Credentials Verify** at https://verify.contentauthenticity.org (the old Content Credentials verify address redirects here). Drag the file in to read any C2PA manifest and its edit history. It accepts images, video, audio and PDF.
   - **OpenAI Verify** at https://openai.com/research/verify/. It reports whether a file carries OpenAI provenance signals, checking both Content Credentials and the SynthID watermark, and it covers images and (since 31 July 2026) supported audio. It only covers content made with ChatGPT, the OpenAI API or Codex, and it deliberately draws no conclusion when it finds nothing. A hit means the content was likely processed by OpenAI tools; the extent is not shown.
   - **Gemini verification.** Signed in to Gemini, upload the image, video or audio clip and ask "Was this created or edited by Google AI?" It checks for a SynthID watermark, and at gemini.google.com and on Android it also reads Content Credentials. Its SynthID check recognizes Google AI content only, so a miss says nothing about OpenAI or any other generator.
   - Also check whether the originating platform shows its own "made with AI" label on the ORIGINAL post.

   All three upload the file to a remote server, so apply the Step 0 rule first. Uploading another person's identifiable media without consent is a transfer of their personal data. The local tools in Step 1.1 and 1.2 keep the file on the machine. A crop loses Content Credentials, so never run a provenance check on a crop or report its result as being about the original.

See `references/provenance.md` for how to read a manifest, what SynthID covers, and the limits of each tool.

### Step 2: Visual inspection (your vision + the checklist)

Look at the actual pixels using `references/artifact-checklist.md`. The checklist is current for 2026 and, importantly, flags which old tells are now unreliable (hands and Latin-script text are largely fixed in modern generators, so a correct hand proves nothing). Focus on the tells that still hold: garbled non-Latin text and signage (Hebrew and Arabic especially), broken shadow and reflection physics, impossible jewelry or accessories, over-smooth skin, and warped backgrounds and architecture. For video, run `scripts/extract_frames.py <file>`, then run the ffmpeg command it prints, to pull frames and step through them for temporal flicker, identity drift and motion warping. **Lip-sync is no longer a usable tell**: current generators produce the speech and the picture together (Google says of Veo that it generates all audio natively), so matched lips are what a good generation looks like, not evidence of a real recording. Treat blink cadence the same way (our reasoning, not a cited finding). Accept that a modern text-to-video clip of a talking person may leave NO visual signal at all, in which case the verdict has to come from provenance and source tracing. Also test non-AI edits: replaced audio, added sirens or explosions, speed changes, selective cuts, and footage filmed off a screen. Compression artifacts are not synthetic tells.

Record each observation as a signal with a direction (leans-synthetic, leans-authentic, neutral). Do not collapse them into a verdict yet.

### Step 3: Source and context tracing

This layer catches a common real-world case: recycled or miscaptioned real media. Follow `references/source-tracing.md`.

1. **No image, video frame, clip or link showing an identifiable person's face goes to any reverse-image, visual-search or multi-engine tool, including TinEye, Yandex, Bing, Google Lens and InVID. Extract frames locally and crop or blur faces first, or search on non-face context only. If a minor or identifiable private individual appears, blurring the face is not enough: search only the caption text or a locally made crop with no person in it.** Then reverse-image search the still (or a representative frame) across more than one engine. Use TinEye for the EARLIEST appearance (that is the question this layer is answering), Yandex for scene matching, Lens for identifying a place or object. Lens answers "what is similar", not "when was this first posted", so do not let it stand in for the earliest-appearance question.
2. **For video, there is still no true reverse-video search.** Say so. Extract frames (`scripts/extract_frames.py <file> --iframes` on a recompressed forward, `--keyframes` for a clip with scene cuts, then run the printed command) and reverse-search several of them; If an identifiable person's face may appear in the clip, do not give the clip or its link to InVID/WeVerify: extract frames locally, crop or blur the faces, and search only those copies, within the item 1 limit for minors and private individuals. Browser users can use the plugin's one-step route only for a clip with no identifiable faces.
3. **Work the platform's own provenance.** Telegram exposes the forwarded-from chain, a no-account channel view at `t.me/s/<channel>`, and sequential message IDs you can date-bracket. On a WhatsApp screenshot, crop the chat chrome and any faces before searching, and read the "Forwarded many times" label and the visible timestamps as evidence in their own right. Trace the item, not the person: do not compile information about a poster's identity, home, workplace or contacts.
4. Geolocate and chronolocate with named tools, not by eye: Google Earth Pro historical imagery, Mapillary street level, Overpass Turbo for OSM features, and SunCalc to work a shadow back to a time of day. Check Israeli specifics (Hebrew vs Arabic vs Farsi signage, plate colour and format compared against current photos of the claimed area, bus liveries). If the item may show a recent strike or hit in Israel, no field of a shareable report may state, confirm or deny where it happened, and it must not repeat a claimed place. Write "Location checked, details withheld" and "GPS present, withheld". Military censorship restrictions on publishing strike locations may apply, including when forwarding, so check the current rules before sharing.
5. Check whether an Israeli verification outlet has already addressed it: המשרוקית at Globes is the Hebrew claim-rating desk (see `references/israeli-context.md`).
6. **Do not use a face-recognition or face-search engine at all** (PimEyes and similar), and decline requests to. This skill does not do this, whatever the purpose. A biometric identifier used to identify a person is "מידע בעל רגישות מיוחדת" under Israel's Privacy Protection Law, a category with heightened protection. To check a CLAIMED KNOWN identity, search the caption and compare by eye against the person's own published photographs from verified accounts or news archives. Never use a lookalike result to identify anyone.

### Step 4: External corroboration (optional, caveated)

Keep the two kinds of external tool apart, because they deserve opposite levels of trust:

- **Ecosystem verifiers** (Content Credentials Verify, OpenAI Verify, Gemini verification) read a signal the generator actually put there. They belong in Step 1, and you should already have run them. A hit is evidence about that ecosystem, not a verdict; a miss concludes nothing.
- **Generic AI-detector websites** guess from pixels. Apply honesty rule 3: state explicitly that a single detector score does not decide the verdict, and never paste a detector percentage as if it were proof.

### Election-period campaign media (Israel): the label is itself a signal

If the item is election propaganda (a party clip, a candidate image, a campaign audio message), Israel has a labelling duty that changes how you read it. Section 2א2 of the Elections (Propaganda Methods) Law, added as a **temporary provision** by the Elections Law for the Twenty-Sixth Knesset, 5786-2026, says a person publishing election propaganda that is "נחזות עמוקה" (visual or audio content that may appear originally documented but was digitally created or materially altered) "יצרף לה גילוי המציין באופן ברור ובולט כי התוכן שבה לא תועד במקור". The arrangement runs until 26 October 2027, so check its status after that date.

The chair's rules, in force since 26 July 2026, accept a statement that all or a named part of the content was digitally created and not originally documented, or digitally edited in a way that materially changed it, or a logo bearing "AI" with that wording. A video must show the notice for as long as the content appears. **Audio-only content cannot use the logo**: it needs a spoken notice at its start and end, so do not look for a visual label on a voice message.

How to use this in a verification:
- **A visible disclosure is the publisher's own statement.** Report what it says and which part it covers, and keep checking anything it does not cover.
- **No visible disclosure does not show the item is authentic and does not show a breach.** It may not be election propaganda, may predate the section (which excludes propaganda first published before it began), may be genuine, or may have lost its label when cropped or re-shared.
- **If you believe synthetic campaign material was published without disclosure,** the user can raise it with the Central Elections Committee, whose chair decides. That is a different route from 119 or 105 (see `references/israeli-context.md`).
- Do not tell the user whether a specific publication is lawful. Describe what the rule requires, what you observed, and where to complain.

Context outside Israel: EU AI Act Article 50 has applied since 2 August 2026 and requires deployers to disclose deepfake content on first exposure. Per the European Commission, providers of systems placed on the market before that date have until 2 December 2026 for machine-readable marking (Article 50(2)), so a missing mark on recent content is still not a signal. Content generated before 2 August 2026 need not be labelled retroactively.

### Audio and voice notes (a separate, weaker lane)

If the item is a voice note or a call recording (a cloned-voice "CEO," a "family member in trouble," a public figure saying something), the image and video layers above do not apply. Be honest that audio is the hardest case:

- **No reliable consumer audio detector**, especially on WhatsApp or phone-compressed voice notes. Compression destroys the very artifacts detectors look for. Do not paste an audio-detector score as a verdict.
- **Ecosystem-scoped provenance still helps when present** (same logic as C2PA for images: a positive is informative, absence proves nothing). Three ecosystem checks, for the user's own recording or one they may lawfully upload:
  - **ElevenLabs AI Speech Classifier** (free): it estimates whether a clip was made with ElevenLabs. Two limits the tool states itself, and they matter: it "does not reliably classify audio generated with the Eleven v3 model", and it cannot detect audio from other providers. So a hit is strong, a miss says nothing about other tools, and a miss does not even show ElevenLabs was not used, because the voice may have come from v3. Never report a low score as "probably not ElevenLabs".
  - **OpenAI Verify** (free, https://openai.com/research/verify/): since 31 July 2026 it verifies supported audio as well as images, checking Content Credentials and SynthID. Scoped to audio generated with OpenAI tools.
  - **Gemini verification**: upload the clip and ask whether it was created or edited by Google AI. Other companies now embed SynthID too, but Gemini recognizes only Google AI content, and OpenAI Verify covers only OpenAI's. Run the checker for each ecosystem, and read a miss as saying nothing about the others. Compression or re-encoding can still strip a watermark.
  - Do NOT use a general "voice deepfake detector" score as your verdict. Treat it as a weak corroborating signal only.
- The same upload rule applies to voice notes. For a third party's voice the default is no upload: use `c2patool`, `exiftool`, careful listening, and the check below.
- **The strongest move is out-of-band verification.** Tell the user to make an ordinary phone call to a number they already saved (not one from the message, and not a call inside the same app, since the account may be hijacked), reach the person through a relative, or contact the institution through its official line. Reaching them on a number you already trust is strong evidence about this message; failing to reach them settles nothing.
- **Listen for tells** (suggestive only): flat or mismatched emotional tone, unnatural pacing and breath, missing room or background noise, abrupt edits, and a request that creates urgency or asks for money or codes (the classic scam shape).
- **If it is fraud or impersonation, route it** (see `references/israeli-context.md`). Do not pay. If money or a code has already gone, call the bank's fraud line immediately, change exposed passwords, then file a police complaint and report to 119. Use 105 when the target is a minor.

Report an audio item with the same verdict structure, but expect `inconclusive` more often, and lead with the out-of-band verification advice.

### Step 5: Write the verdict report

Produce the report using this structure (template in `references/verdict-report-template.md`):

- **Verdict:** one of `authentic` / `AI-generated` / `digitally manipulated` / `authentic but miscaptioned` / `not real footage` (game, simulator or CGI) / `inconclusive`.
- **Confidence:** low / medium / high, with one sentence on why. Visual-only findings cap at medium and read "likely". High needs a located original, or `Trusted` provenance confirmed by source tracing; a vendor hit alone does not.
- **Possible recent strike in Israel:** in every field, speak only to whether the footage is genuine and recent, never to the place. Use `authentic but miscaptioned` only when tracing shows an older event or footage from outside Israel, and say only that. Write "GPS present, withheld", and list place-revealing sources as "withheld from the shareable version".
- **Evidence by layer:** what each of the four layers found, including null results.
- **What would change the verdict:** the missing piece that would raise or lower confidence.
- **Sources:** every external link or tool used.
- **Caveat (always include, in the report's language):** Produced by a free AI-operated tool with no review by an expert examiner, and it can be wrong. Not an expert opinion or evidence. A missing credential or watermark is not proof of fakery, and automated AI detectors are unreliable. Publishing this conclusion about an identifiable person may carry legal exposure.

Prefer `inconclusive` over a confident guess. Calling real content fake is itself a harm (the "liar's dividend"), so distinguish "no evidence of manipulation found" from "proven authentic."

### Step 6: Before the user acts on the verdict

The verdict feeds a decision the user is about to make, usually "do I forward this". Close with the two things that decision needs:

1. **Preserve first, if any reporting or complaint may follow** (never for possible sexual imagery of a minor: see Step 0). Keep the original file rather than a fresh screenshot, do not delete the thread, and record the sender identifier, the timestamps and when they received it. Every route in `references/israeli-context.md` works better with an intact artefact, and it degrades by the hour.
2. **Name the right channel for the harm, and note the exposure that comes with forwarding.** Route by who was harmed: 119 for a cyber or impersonation incident; the bank's fraud line, then police and 119, for financial impersonation; 105 only when the target is a minor; for an adult targeted by synthetic sexual imagery, the 1202/1203 helplines, the police, and StopNCII (hashes on the user's device; public platforms only, not encrypted messaging); the Central Elections Committee for a concern about undisclosed synthetic campaign material. Remind the user that forwarding can itself be publication, that footage revealing a recent strike location should not be posted or forwarded before checking the censorship rules, and point them to the Legal notice above rather than assessing their exposure.

## Examples

### Example 1: Forwarded war clip on WhatsApp
User says: "Got this video of a missile hitting a Tel Aviv tower last night, is it real?"
Actions:
1. Ask for the original file, not the WhatsApp re-encode, if available.
2. Save `c2patool` and `exiftool` output for `clip.mp4` and interpret it with `scripts/check_provenance.py` and `scripts/dump_metadata.py` (likely stripped on a forward, note that).
3. `scripts/extract_frames.py clip.mp4 --iframes`, run the printed command, then inspect frames against the checklist (skyline geometry, smoke physics, temporal flicker).
4. Reverse-image search key frames, with any identifiable faces cropped or blurred first, for earliest appearance; check whether it is a known recycled or game clip.
Result: A verdict report, for example "authentic but miscaptioned: footage traces to a 2024 event, confidence medium," or "inconclusive: no provenance, no prior match, minor frame artifacts."

### Example 2: Suspicious image of a public figure
User says: "Is this photo of the minister saying X real?"
Actions:
1. Run provenance and metadata scripts.
2. Vision pass focused on text/signage, hands-in-context, lighting consistency.
3. Search the caption, and reverse-search only a version with faces cropped or blurred; look for the original and the earliest publication.
Result: Report with verdict and confidence, plus the matching route: the Central Elections Committee for campaign material, FakeReporter for a coordinated network (see `references/israeli-context.md`).

## Bundled Resources

### Scripts
- `scripts/check_provenance.py` -- lists what a saved `c2patool` report declares and gives no verdict. Run: `python scripts/check_provenance.py report.json --stderr report.err`
- `scripts/dump_metadata.py` -- interprets saved `exiftool -json -G1` output and can write an ELA image. Run: `python scripts/dump_metadata.py meta.json`
- `scripts/extract_frames.py` -- prints the correct `ffmpeg` command for fixed-rate, scene-change or I-frame extraction. Run: `python scripts/extract_frames.py <video> --iframes`

### References
- `references/provenance.md` -- how to read a C2PA manifest, what SynthID and EXIF do, and the limits of each.
- `references/artifact-checklist.md` -- the 2026 visual-inspection checklist, including which tells are now obsolete.
- `references/source-tracing.md` -- reverse-image, earliest-appearance, geolocation and chronolocation.
- `references/israeli-context.md` -- the Iran-Israel media-manipulation landscape and Israeli verification and reporting channels.
- `references/verdict-report-template.md` -- the output structure.
- `references/domain-checklist.md` -- coverage contract this skill is maintained against.

## Recommended MCP Servers

No MCP server currently provides media-authenticity data for Israel, and AI-detector APIs are unreliable (see honesty rule 3), so this skill deliberately does not wrap one. The companion `israeli-fact-checker` skill handles numeric and textual claim verification against official Israeli data.

## Gotchas

- **Defaulting to "it's a deepfake."** The 2025 Iran-Israel flood also included recycled or miscaptioned real footage and flight-simulator clips. Always test the "authentic but miscaptioned" hypothesis with reverse-image search, with any identifiable faces cropped or blurred first.
- **Reporting `Valid` as verified.** Without a trust list, `c2patool` can return `Valid` for a manifest signed with anyone's certificate. Only `Trusted` ties the claim to a listed signer.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Content Credentials Verify tool | https://verify.contentauthenticity.org/ | No-code provenance check for an image, video, audio or PDF |
| OpenAI Verify | https://openai.com/research/verify/ | Free check for OpenAI Content Credentials and SynthID in images and audio |
| Israeli election AI-labelling rules | https://www.law.co.il/news/2026/07/27/deep-fake-and-ai-elections-propaganda-rules/ | The disclosure a campaign item must carry, in force 26.07.2026 |
| c2patool docs | https://opensource.contentauthenticity.org/docs/sdk-repos/c2patool/docs/usage | Read manifests and validate against a trust list |
| C2PA trust lists | https://opensource.contentauthenticity.org/docs/conformance/trust-lists | Official list, frozen interim list, and which one each tool uses |
| Gemini verification | https://support.google.com/gemini/answer/16722517?hl=en | What Gemini's SynthID and Content Credentials checks cover |
| ElevenLabs AI Speech Classifier | https://elevenlabs.io/ai-speech-classifier | Free check for whether audio was made with ElevenLabs |
| NewsGuard detector audit | https://www.newsguardtech.com/special-reports/leading-ai-image-detection-tools-mislead-online-users-often-declaring-authentic-content-fake/ | Why automated AI-image detectors are unreliable |
| Poynter, spotting fake war images | https://www.poynter.org/fact-checking/2026/fake-images-iran-war-how-spot-them/ | Recycled and miscaptioned footage as a common fake |
| Israel 105 (Child Online Protection) | https://www.gov.il/en/departments/units/105_call_center | Reporting online harm to minors |
| Bank of Israel fraud warning | https://www.boi.org.il/en/information-and-service-to-the-public/consumer-enquiries-and-inspections/warning-to-the-public-with-regard-to-fraud-by-impersonating-the-bank-of-israel-or-commercial-banks/ | Impersonation-fraud guidance |

## Troubleshooting

### Error: "c2patool: command not found"
Cause: The C2PA tool is not installed.
Solution: Install with `brew install c2patool` (macOS). Until it is installed, Layer 1 has no C2PA result: record that the check did not run, and continue with the other layers.

### Error: "exiftool: command not found"
Cause: ExifTool is not installed.
Solution: Install with `brew install exiftool` (macOS) or your platform package manager. Metadata analysis is skipped without it; the other three layers still work.

### Error: "Unrecognized option 'vsync'"
Cause: A command written for older ffmpeg. Current ffmpeg replaced `-vsync` with `-fps_mode`.
Solution: Use the command printed by `scripts/extract_frames.py`. It needs ffmpeg 5.1 or newer.

### Issue: "`--keyframes` produced no frames or an ffmpeg error"
Cause: A single continuous shot has no scene cut to select (reproduced on a test clip).
Solution: This says nothing about authenticity. Use `--iframes` or the default fixed-rate mode.

### Issue: "Every layer is null / inconclusive"
Cause: The media was forwarded and stripped, has no prior online match, and shows no clear artifacts.
Solution: This is a legitimate `inconclusive` verdict. Report it honestly with the missing pieces that would change it, rather than guessing. Suggest the user obtain the original file or wait for a verification outlet to weigh in.
