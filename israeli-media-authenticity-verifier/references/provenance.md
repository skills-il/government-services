# Provenance layer: C2PA, SynthID, EXIF

Provenance is the only layer that can be cryptographically conclusive. Work it first.

## C2PA Content Credentials

C2PA (Coalition for Content Provenance and Authenticity) defines "Content Credentials":
a tamper-evident manifest attached to a file that records who created it, which tool
made it (including whether an AI generator was involved), and the edit history. The
manifest is signed, so a valid signature ties the claims to a known signer.

How to read it:
- Run `scripts/check_provenance.py <file>` (wraps `c2patool`). Install with `brew install c2patool`.
- A valid signed manifest whose claim generator names an AI image tool is near-conclusive
  evidence the asset is AI-generated.
- A valid signed manifest with a camera-capture claim is strong support for authenticity.
- The no-code path: the Verify tool at https://contentcredentials.org/verify lets a user
  drag in a file and see the same history. It uploads to a remote server, so avoid it for
  sensitive media.

What it does NOT tell you:
- Absence of a manifest is the common case and proves nothing. Social platforms and
  messaging apps strip C2PA on upload, and screenshotting destroys it.
- A manifest is only as trustworthy as its signer. Treat an unknown or self-signed signer
  with caution; do not stop at "a manifest exists."

Recovering provenance for a forwarded file:
- Because the forward you were handed is stripped, the actionable move is to get the
  ORIGINAL. Trace back to the earliest poster (see source-tracing.md) and check their
  upload, not the re-share.
- Many platforms (large social and video sites) now show their own "made with AI" or
  "AI info" label on the original post and ingest C2PA. For a user with no shell, reading
  that label on the original is a faster, higher-yield check than any tool.

## SynthID (watermark)

Google's SynthID embeds an imperceptible watermark into AI-generated media. Per Google,
"SynthID embeds digital watermarks directly into AI-generated images, audio, text or video"
(https://deepmind.google/science/synthid/). Detection is accessed through Google's own
tools rather than a local CLI.

Limits, and this matters operationally: SynthID only flags content made by Google's own AI
models. A clean SynthID result tells you nothing about images from other generators, which
produce most viral war fakes. So "no SynthID watermark" is not reassurance, it is just "not
a Google-model image, or the watermark was stripped." Re-encoding, cropping, or
screenshotting can also weaken or remove it. No watermark found is never evidence of
authenticity.

## EXIF / metadata

Run `scripts/dump_metadata.py <file>` (wraps `exiftool`, install with `brew install exiftool`).
Read:
- Make / Model / DateTimeOriginal / GPS: capture provenance. Internally consistent values
  support a real-camera origin.
- Software: an edit fingerprint. A generator or editor name here is a meaningful signal.

Limits: forwarded and uploaded media is routinely stripped of EXIF, so absence is the norm
and is not evidence of fakery. ELA (Error Level Analysis), available via the script's
`--ela` flag, is a hint for splicing only and has a high false-positive rate.

## Weighting

| Finding | Weight |
|---------|--------|
| Valid signed C2PA "created with AI" claim | Near-conclusive: AI-generated |
| Valid signed camera-capture C2PA claim | Strong: authentic origin |
| Google tool reports SynthID watermark | Strong: AI-generated (Google family) |
| Software field names a generator | Moderate: synthetic or edited |
| No manifest, no watermark, stripped EXIF | NULL: no signal, proceed to other layers |
