# Verdict report template

Use this structure for the output. Fill every section, including null results. Prefer
"inconclusive" over a confident guess.

```
MEDIA AUTHENTICITY VERDICT

Item: <one line describing the media and the claim attached to it>

Verdict: <authentic | AI-generated | digitally manipulated | authentic but miscaptioned | inconclusive>
Confidence: <low | medium | high>
Why this confidence: <one sentence>

Evidence by layer:
- Provenance (C2PA / SynthID / EXIF): <what was found, or "null: stripped / none">
- Visual inspection: <strongest signals and their direction, or "no signal">
- Source tracing: <earliest appearance, geolocation, chronolocation findings, or "no match found">
- External tools (optional): <tool used and result, with the reliability caveat, or "not used">

What would change this verdict:
- <the missing piece that would raise or lower confidence>

Sources:
- <every external link or tool used>

Caveat: This is an assistive verification, not a forensic certification. A missing
credential or watermark is not proof of fakery, and automated AI detectors are unreliable.
```

## Choosing the verdict

| Situation | Verdict |
|-----------|---------|
| Signed C2PA / SynthID says AI, or multiple strong synthetic tells with no prior match | AI-generated |
| Real source found, but caption/place/date is false | authentic but miscaptioned |
| Real source, signed camera provenance, consistent context | authentic |
| Clear local edits (splice, removed/added object) on otherwise real media | digitally manipulated |
| Thin or conflicting evidence across all layers | inconclusive |

## The two error modes to avoid

1. False "fake": calling real footage fake also spreads disinformation (the liar's
   dividend). Distinguish "no manipulation evidence found" from "proven authentic."
2. False "real": a clean visual pass is not proof of authenticity because generators are
   good now. Lean on provenance and source tracing for an "authentic" call.
