# Provenance layer: C2PA, SynthID, EXIF

Provenance shows what a signer declared. Work it first, and never let it decide a verdict alone.

## C2PA Content Credentials

C2PA (Coalition for Content Provenance and Authenticity) defines "Content Credentials":
a tamper-evident manifest attached to a file that records who created it, which tool
made it (including whether an AI generator was involved), and the edit history. The
manifest is signed, so a valid signature ties the claims to a known signer.

How to read it:
- Install with `brew install c2patool`, run it against a trust list, save the output, and
  pass the saved files to `scripts/check_provenance.py`:

  ```bash
  curl -fsSLO https://raw.githubusercontent.com/c2pa-org/conformance-public/main/trust-list/C2PA-TRUST-LIST.pem
  c2patool <file> trust --trust_anchors C2PA-TRUST-LIST.pem > report.json 2> report.err
  python scripts/check_provenance.py report.json --stderr report.err
  ```

- The script lists declared actions and sources and gives no verdict.
- `Valid` means only that the signature and hashes check out. Anyone can produce it with their
  own certificate, so it is not verified. We reproduced it on a C2PA test-signed file whose
  failure list contained `signingCredential.untrusted`. Only `Trusted` means the signer chains
  to the list you supplied, and only `Trusted` may be called signer-attested. `Invalid` may mean
  the file was changed or damaged.
- Even a `Trusted` manifest is the signer's statement. Whatever it declares, AI or camera, needs
  source tracing before any verdict.

Two trust lists exist, and tools differ. The official C2PA trust list is current. The interim
trust list was frozen on 1 January 2026, but content signed while its certificates were valid
stays valid under the legacy model, and the Verify site still uses it. If the official list
returns `Valid`, check the interim list and report which list matched:

```bash
curl -fsSLO https://raw.githubusercontent.com/contentauth/verify-site/main/static/trust/anchors.pem
curl -fsSLO https://raw.githubusercontent.com/contentauth/verify-site/main/static/trust/allowed.pem
curl -fsSLO https://raw.githubusercontent.com/contentauth/verify-site/main/static/trust/store.cfg
c2patool <file> trust --trust_anchors anchors.pem --allowed_list allowed.pem \
  --trust_config store.cfg > report-itl.json 2> report-itl.err
python scripts/check_provenance.py report-itl.json --stderr report-itl.err
```

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
- Even a listed camera signer can fail. In September 2025 Nikon said it would revoke all C2PA
  certificates issued for the Z6 III after a vulnerability in its authenticity feature
  (https://www.digitalcameraworld.com/photography/photojournalism/nikon-revokes-all-c2pa-image-authenticity-certificates-after-major-vulnerability-exposed).
  So keep source tracing in the verdict even when the signature checks out.

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
(https://deepmind.google/models/synthid/). Detection is accessed through vendor tools
rather than a local CLI.

Detection route for an ordinary user: sign in to Gemini, upload the file and ask whether it
was created or edited by Google AI (https://support.google.com/gemini/answer/16722517?hl=en).
At gemini.google.com and on Android, the same check also reads Content Credentials.

Scope: the watermark is multi-vendor, but each checker is not. OpenAI embeds SynthID too,
describing "adding durable cross-platform SynthID watermarking to images through a
partnership with Google" (https://openai.com/index/advancing-content-provenance/). Google's
help page says: "While other companies have started to adopt SynthID watermarks, Gemini can
currently only recognize content created by Google AI tools." So a Gemini hit means Google AI
was used for all or part of the item. OpenAI's page says a detected signal "indicates that the
content was likely processed by OpenAI tools" and does not show whether or to what extent it
was generated or edited. A miss in either says nothing about the other.

A clean result also tells you nothing about generators outside that ecosystem. Re-encoding,
cropping, or screenshotting can weaken or remove a watermark. No watermark found is never
evidence of authenticity.

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

Install with `brew install exiftool`, then run `exiftool -json -G1 <file> > meta.json` and
`python scripts/dump_metadata.py meta.json`. Read:
- Make / Model / DateTimeOriginal / GPS: declared capture details. They are easy to edit and
  never prove a real-camera origin.
- Software: an edit fingerprint. A generator or editor name here is a lead to check.
- **DigitalSourceType (IPTC): the field that DECLARES AI origin.** The script reads it from
  the saved exiftool JSON. Per the IPTC NewsCodes vocabulary, the value
  `trainedAlgorithmicMedia` means "Digital media created algorithmically using an Artificial
  Intelligence model trained on captured content", `compositeWithTrainedAlgorithmicMedia`
  means edited using generative AI, and `compositeSynthetic` means a mix or composite of
  several elements at least one of which is generative AI
  (https://cv.iptc.org/newscodes/digitalsourcetype/). This is an editable declaration, and it often
  survives when a C2PA manifest does not, because it is ordinary XMP. It is also much of
  what a platform's "made with AI" label is reading. Absence of the field remains a null,
  never a clearance.

Limits: forwarded and uploaded media is routinely stripped of EXIF, so absence is the norm
and is not evidence of fakery. ELA (Error Level Analysis), available via the script's
`--ela IMAGE OUT` option, is a hint for splicing only and has a high false-positive rate.

## Weighting

| Finding | Weight |
|---------|--------|
| `Trusted` C2PA declaration of any kind | Signer-attested statement. Needs source tracing, never a verdict alone |
| `Valid` but not `Trusted` manifest | Not verified: self-description |
| `Invalid` manifest | Do not use as evidence of origin; the file may have been changed or damaged |
| Gemini reports a SynthID watermark | All or part made or edited with Google AI; the extent stays open |
| OpenAI Verify reports a provenance signal | Likely processed by OpenAI tools; extent not shown. Does not mean the whole item is AI-generated and cannot raise confidence to high on its own |
| Metadata names a generator or declares AI | Editable declaration: a lead for source tracing, never a verdict |
| No manifest, no watermark, stripped EXIF | NULL: no signal, proceed to other layers |
