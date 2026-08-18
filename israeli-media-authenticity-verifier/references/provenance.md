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
- The no-code path: the Verify tool at https://verify.contentauthenticity.org lets a user
  drag in a file and see the same history ("Drag content into Verify to inspect its Content
  Credentials in detail and see how it has changed over time"). It accepts images, video,
  audio and PDF. The old Content Credentials verify address redirects here. It uploads
  to a remote server, so avoid it for sensitive media.
- Signer check: `c2patool <file> --certs` prints the PEM certificate chain from the active
  manifest's signature, which is how you act on "a manifest is only as good as its signer"
  rather than just noting it.

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

Detection route for an ordinary user: per Google, "Simply upload the image, video or audio
clip to your chat, and ask if it's been created or altered by Google AI. Gemini will check
for a SynthID watermark, and let you know if it finds one." Google also runs a separate SynthID Detector
portal aimed at journalists and researchers rather than the general public, so the Gemini app
is the practical consumer route.

Scope, and this changed in 2026: SynthID is no longer a Google-only signal. OpenAI now
embeds it too, describing the move as "adding durable cross-platform SynthID watermarking to
images through a partnership with Google"
(https://openai.com/index/advancing-content-provenance/). So a SynthID hit means the asset
was watermarked by a participating generator, NOT that Google made it. Attribute the
specific tool from the C2PA manifest, not from the watermark.

The limit that has not changed: a clean SynthID result tells you nothing about images from
non-participating generators, which produce most viral war fakes. So "no SynthID watermark"
is not reassurance, it is just "not from a participating generator, or the watermark was
stripped." Re-encoding, cropping, or screenshotting can also weaken or remove it. No
watermark found is never evidence of authenticity.

## OpenAI Verify

A third free, no-code provenance check, at https://openai.com/research/verify/. Per OpenAI,
it is "a public verification tool that will help people verify whether an uploaded image was
generated on ChatGPT, the OpenAI API, or Codex, by checking if it contains provenance
signals, including Content Credentials and SynthID." Since 31 July 2026 it also verifies
supported audio files, and OpenAI audio now carries SynthID watermarking.

Read it exactly like the other two: ecosystem-scoped. A hit is informative. A miss is
deliberately inconclusive by the tool's own design, and OpenAI says so, because provenance
signals can be stripped.

## EXIF / metadata

Run `scripts/dump_metadata.py <file>` (wraps `exiftool`, install with `brew install exiftool`).
Read:
- Make / Model / DateTimeOriginal / GPS: capture provenance. Internally consistent values
  support a real-camera origin.
- Software: an edit fingerprint. A generator or editor name here is a meaningful signal.
- **DigitalSourceType (IPTC): the field that DECLARES AI origin.** The script now reads
  `XMP-iptcExt:DigitalSourceType`. Per the IPTC NewsCodes vocabulary, the value
  `trainedAlgorithmicMedia` means "Digital media created algorithmically using an Artificial
  Intelligence model trained on captured content", and `compositeSynthetic` means a mix or
  composite of several elements at least one of which is generative AI
  (https://cv.iptc.org/newscodes/digitalsourcetype/). This is a strong positive and it often
  survives when a C2PA manifest does not, because it is ordinary XMP. It is also much of
  what a platform's "made with AI" label is reading. Absence of the field remains a null,
  never a clearance.

Limits: forwarded and uploaded media is routinely stripped of EXIF, so absence is the norm
and is not evidence of fakery. ELA (Error Level Analysis), available via the script's
`--ela` flag, is a hint for splicing only and has a high false-positive rate.

## Weighting

| Finding | Weight |
|---------|--------|
| Valid signed C2PA "created with AI" claim | Near-conclusive: AI-generated |
| Valid signed camera-capture C2PA claim | Strong: authentic origin |
| Gemini or OpenAI Verify reports a SynthID watermark | Strong: AI-generated by a SynthID-participating generator (Google or OpenAI); do not attribute the specific tool from the watermark alone |
| Software field names a generator | Moderate: synthetic or edited |
| No manifest, no watermark, stripped EXIF | NULL: no signal, proceed to other layers |
