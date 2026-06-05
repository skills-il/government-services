---
name: israeli-media-authenticity-verifier
description: "Run a structured check on whether an image or video is AI-generated, digitally manipulated, or authentic-but-miscaptioned, and produce a sourced verdict with a confidence level. Use when a user forwards a dramatic war or news photo or clip on WhatsApp or Telegram and asks if it is real, when a journalist or community moderator needs a repeatable verification report before sharing or debunking, or when someone gets a suspicious image or voice claiming to be a known person. Combines cryptographic provenance (C2PA Content Credentials, SynthID, EXIF metadata), the agent's own visual inspection against an artifact checklist, and source tracing (reverse-image search, earliest-appearance, geolocation). This is a verifier, not a magic detector: it never claims certainty from one signal and says can't-verify when evidence is thin. Do NOT use for numeric or textual claim fact-checking (use israeli-fact-checker), for generating or removing deepfakes, or as court-admissible forensic certification."
license: MIT
compatibility: "Needs an agent with image vision plus a local shell (to run the provenance and metadata scripts) and web access (for reverse-image search). Degrades to a manual checklist on agents without a shell."
---

# Israeli Media Authenticity Verifier

## Problem

Israelis are flooded with images and videos forwarded on WhatsApp and Telegram, especially during security events, and it is genuinely hard to tell what is real. The June 2025 Iran-Israel conflict was, in the words of experts, the first major conflict where generative AI shaped the information battlefield: fake clips of missile damage in Tel Aviv and at Ben Gurion Airport circulated, and flight-simulator footage passed off as real airstrikes reached over 21 million views before removal. Most people have no reliable way to check, and the automated "AI detector" websites are themselves unreliable, so a forwarded lie spreads faster than the correction.

## What this skill is (and is not)

This skill makes you a disciplined verifier, not a detector. There is no button that says "fake" or "real." Instead you combine four kinds of evidence, weight them, and report a verdict with an honest confidence level.

| Layer | What it checks | How conclusive |
|-------|----------------|----------------|
| 1. Provenance | C2PA Content Credentials, SynthID watermark, EXIF metadata | Strong WHEN present; absence proves nothing |
| 2. Visual inspection | Your own vision against an artifact checklist | Suggestive, never proof |
| 3. Source tracing | Reverse-image search, earliest appearance, geolocation | Best for catching recycled or miscaptioned real media |
| 4. External tools | contentcredentials.org, SynthID detector, openai verify | Corroborating only; AI-detector sites are unreliable |

**Four honesty rules, always:**
1. A missing Content Credential or watermark is NOT evidence that media is fake or real. Screenshotting and re-encoding strip these signals from real and fake content alike.
2. You cannot run a forensic AI-classifier yourself. Do not pretend to. Your vision pass is informed judgment, not a measurement.
3. Automated AI-image detector websites mislead users. A NewsGuard audit found such tools "declared authentic images to be AI-generated 13.33 percent of the time, and one tool got it wrong 40 percent of the time." Treat any detector score as one weak signal, never the verdict.
4. The most common wartime fake is not a deepfake at all: it is real footage that is old, from another place, or from a video game, just miscaptioned. As Poynter put it, viral war imagery is "often ... generated with artificial intelligence or else it's old footage misrepresented as if it's new." Always include "authentic but miscaptioned" as a possible verdict.

## Instructions

Work the layers in order. Stop early only when provenance gives a cryptographically signed answer; otherwise gather all four and weigh them.

### Step 0: Intake

Ask for the actual file if you only have a screenshot or a forwarded clip. A re-screenshotted image has lost its metadata and credentials, which changes what Layer 1 can do. Note the claim attached to the media ("this is Tel Aviv last night") separately from the media itself, because a real image with a false caption is a distinct verdict.

**If this is an active security incident, check the authoritative source first.** When the user is asking "is a missile hitting Tel Aviv right now," the fastest correct move is not forensics, it is the primary source: the Home Front Command (Pikud HaOref) official app and alerts, and established news desks. Tell the user not to act on or re-share a forward before confirming against an authority. Run the verification layers below in parallel, but never let the analysis delay the user from the real-time source.

**Try to recover the original.** Provenance and metadata survive only on the original file from the account or platform that first posted it. If you only have a forward, the highest-value step is to trace back to the earliest poster (see Step 3) and get their upload, or check whether the hosting platform shows its own "made with AI" label on the original post. A platform label is a zero-effort check for a user who has no shell.

### Step 1: Provenance (run the scripts)

Provenance is the only layer that can be cryptographically conclusive, so start here.

1. **Content Credentials (C2PA).** Run `scripts/check_provenance.py <file>`. It wraps `c2patool` and reports the signer, the claim generator (for example a field naming the AI tool that made it), and the validation status. A valid signed manifest that says the asset was generated by an AI tool is near-conclusive. A manifest that says "captured by camera X" with a verified signature is strong evidence of authenticity. No manifest is the common case and means nothing on its own.
2. **Metadata (EXIF).** Run `scripts/dump_metadata.py <file>`. It wraps `exiftool` and surfaces camera Make/Model, DateTimeOriginal, GPS, and the Software field (an edit fingerprint like an image editor or generator name). It can also write an Error Level Analysis (ELA) image as a hint for spliced regions. Read absence as "no signal," not as "fake."
3. **No-code fallback.** If you have no shell, tell the user to drag the file into the Verify tool at contentcredentials.org, or to ask the originating platform's own checker (for example whether an image came from a specific generator). Note that those sites upload the file to a remote server, which matters for sensitive media.

See `references/provenance.md` for how to read a manifest, what SynthID covers, and the limits of each tool.

### Step 2: Visual inspection (your vision + the checklist)

Look at the actual pixels using `references/artifact-checklist.md`. The checklist is current for 2026 and, importantly, flags which old tells are now unreliable (hands and Latin-script text are largely fixed in modern generators, so a correct hand proves nothing). Focus on the tells that still hold: garbled non-Latin text and signage (Hebrew and Arabic especially), broken shadow and reflection physics, impossible jewelry or accessories, over-smooth skin, and warped backgrounds and architecture. For video, run `scripts/extract_frames.py <file>` to pull frames and step through them for temporal flicker, identity drift, unnatural blinking, and lip-sync drift.

Record each observation as a signal with a direction (leans-synthetic, leans-authentic, neutral). Do not collapse them into a verdict yet.

### Step 3: Source and context tracing

This layer catches the dominant real-world case: recycled or miscaptioned real media. Follow `references/source-tracing.md`.

1. Reverse-image search the still (or a representative frame) across more than one engine. Look for the earliest appearance, not just any appearance, to expose old footage relabeled as current.
2. Geolocate and chronolocate: check signage, landmarks, and license plates against maps, and sun and shadow angles and weather against the claimed date and time.
3. Check whether an Israeli verification outlet has already addressed it (see `references/israeli-context.md`).

### Step 4: External corroboration (optional, caveated)

If you want a second opinion, you may point the user to a watermark or detector tool, but apply honesty rule 3. State explicitly that a single detector score does not decide the verdict. Never paste a detector percentage as if it were proof.

### Audio and voice notes (a separate, weaker lane)

If the item is a voice note or a call recording (a cloned-voice "CEO," a "family member in trouble," a public figure saying something), the image and video layers above do not apply. Be honest that audio is the hardest case:

- **No reliable consumer audio detector**, especially on WhatsApp or phone-compressed voice notes. Compression destroys the very artifacts detectors look for. Do not paste an audio-detector score as a verdict.
- **Provenance still helps when present.** Google's SynthID also watermarks AI-generated audio, so audio from Google's tools may carry a watermark you can check via Google's own tooling. Absence proves nothing, as always.
- **The strongest move is out-of-band verification.** Tell the user to confirm through a known, independent channel: call the person back on a number they already have (not one supplied in the message), or contact the institution through its official line. A cloned voice cannot survive a callback to a trusted number.
- **Listen for tells** (suggestive only): flat or mismatched emotional tone, unnatural pacing and breath, missing room or background noise, abrupt edits, and a request that creates urgency or asks for money or codes (the classic scam shape).
- **If it is fraud or impersonation, route it** (see `references/israeli-context.md`): the National Cyber Directorate 119 hotline for cyber incidents, the bank's fraud line for financial impersonation, and 105 specifically when the target is a minor.

Report an audio item with the same verdict structure, but expect `inconclusive` more often, and lead with the out-of-band verification advice.

### Step 5: Write the verdict report

Produce the report using this structure (template in `references/verdict-report-template.md`):

- **Verdict:** one of `authentic` / `AI-generated` / `digitally manipulated` / `authentic but miscaptioned` / `inconclusive`.
- **Confidence:** low / medium / high, with one sentence on why.
- **Evidence by layer:** what each of the four layers found, including null results.
- **What would change the verdict:** the missing piece that would raise or lower confidence.
- **Sources:** every external link or tool used.

Prefer `inconclusive` over a confident guess. Calling real content fake is itself a harm (the "liar's dividend"), so distinguish "no evidence of manipulation found" from "proven authentic."

## Examples

### Example 1: Forwarded war clip on WhatsApp
User says: "Got this video of a missile hitting a Tel Aviv tower last night, is it real?"
Actions:
1. Ask for the original file, not the WhatsApp re-encode, if available.
2. `scripts/check_provenance.py clip.mp4` and `scripts/dump_metadata.py clip.mp4` (likely stripped on a forward, note that).
3. `scripts/extract_frames.py clip.mp4`, then inspect frames against the checklist (skyline geometry, smoke physics, temporal flicker).
4. Reverse-image search key frames for earliest appearance; check whether it is a known recycled or game clip.
Result: A verdict report, for example "authentic but miscaptioned: footage matches a 2024 event in another city, confidence medium," or "inconclusive: no provenance, no prior match, minor frame artifacts."

### Example 2: Suspicious image of a public figure
User says: "Is this photo of the minister saying X real?"
Actions:
1. Run provenance and metadata scripts.
2. Vision pass focused on text/signage, hands-in-context, lighting consistency.
3. Reverse-image search; look for the original and the earliest publication.
Result: Report with verdict and confidence, plus a pointer to report impersonation if it targets a minor (105) or appears to be financial-impersonation fraud (see `references/israeli-context.md`).

## Bundled Resources

### Scripts
- `scripts/check_provenance.py` -- reads C2PA Content Credentials via `c2patool`. Run: `python scripts/check_provenance.py <file>`
- `scripts/dump_metadata.py` -- dumps key EXIF fields via `exiftool` and can write an ELA image. Run: `python scripts/dump_metadata.py <file>`
- `scripts/extract_frames.py` -- extracts frames from a video via `ffmpeg` for frame-by-frame inspection. Run: `python scripts/extract_frames.py <video>`

### References
- `references/provenance.md` -- how to read a C2PA manifest, what SynthID and EXIF do, and the limits of each.
- `references/artifact-checklist.md` -- the 2026 visual-inspection checklist, including which tells are now obsolete.
- `references/source-tracing.md` -- reverse-image, earliest-appearance, geolocation and chronolocation.
- `references/israeli-context.md` -- the Iran-Israel media-manipulation landscape and Israeli verification and reporting channels.
- `references/verdict-report-template.md` -- the output structure.
- `references/domain-checklist.md` -- coverage contract this skill is maintained against.

## Recommended MCP Servers

No MCP server currently provides media-authenticity data for Israel. The genuinely Israeli player in this space (deepfake and disinformation detection) is enterprise-only with no public API, and global AI-detector APIs are unreliable (see honesty rule 3), so this skill deliberately does not wrap one. The companion `israeli-fact-checker` skill handles numeric and textual claim verification against official Israeli data.

## Gotchas

- **Treating "no Content Credentials" as proof of fake.** Most authentic media has no manifest, and forwarding strips manifests from real and fake content alike. Absence is a null result, not a verdict.
- **Trusting an AI-detector website's percentage.** These tools false-flag authentic photos at material rates (NewsGuard found 13.33 percent on average, 40 percent for one tool). Use them only as a weak corroborating signal.
- **Defaulting to "it's a deepfake."** The most common manipulation in the 2025 Iran-Israel flood was recycled or miscaptioned real footage and even flight-simulator clips, not synthesis. Always test the "authentic but miscaptioned" hypothesis with reverse-image search.
- **Relying on obsolete visual tells.** Modern generators fixed hands and Latin-script text; a clean hand or readable English caption is not evidence of authenticity. Lean on shadow physics, non-Latin text, and reflections instead.
- **Forgetting the liar's dividend.** Wrongly calling real footage fake also spreads disinformation. Distinguish "no manipulation evidence found" from "proven authentic," and prefer inconclusive over a confident guess.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Content Credentials Verify tool | https://contentcredentials.org/verify | No-code provenance check for an image or video |
| c2patool docs | https://opensource.contentauthenticity.org/docs/c2patool/ | Install and read C2PA manifests from the command line |
| Google SynthID | https://deepmind.google/science/synthid/ | What the SynthID watermark covers and its limits |
| NewsGuard detector audit | https://www.newsguardtech.com/special-reports/leading-ai-image-detection-tools-mislead-online-users-often-declaring-authentic-content-fake/ | Why automated AI-image detectors are unreliable |
| Poynter, spotting fake war images | https://www.poynter.org/fact-checking/2026/fake-images-iran-war-how-spot-them/ | Recycled and miscaptioned footage as the dominant fake |
| Israel 105 (Child Online Protection) | https://www.gov.il/en/departments/units/105_call_center | Reporting online harm to minors, including AI impersonation |
| Bank of Israel fraud warning | https://www.boi.org.il/en/information-and-service-to-the-public/consumer-enquiries-and-inspections/warning-to-the-public-with-regard-to-fraud-by-impersonating-the-bank-of-israel-or-commercial-banks/ | Impersonation-fraud guidance |

## Troubleshooting

### Error: "c2patool: command not found"
Cause: The C2PA tool is not installed.
Solution: Install with `brew install c2patool` (macOS). The script will print this hint and continue with metadata-only analysis if the tool is missing.

### Error: "exiftool: command not found"
Cause: ExifTool is not installed.
Solution: Install with `brew install exiftool` (macOS) or your platform package manager. Metadata analysis is skipped without it; the other three layers still work.

### Issue: "Every layer is null / inconclusive"
Cause: The media was forwarded and stripped, has no prior online match, and shows no clear artifacts.
Solution: This is a legitimate `inconclusive` verdict. Report it honestly with the missing pieces that would change it, rather than guessing. Suggest the user obtain the original file or wait for a verification outlet to weigh in.
