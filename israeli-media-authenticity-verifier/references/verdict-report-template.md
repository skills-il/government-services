# Verdict report template

Use this structure for the output. Fill every section, including null results. For a possible
recent strike in Israel, no field may state, confirm or deny the place: write "Location checked,
details withheld" and "GPS present, withheld", and list place-revealing sources as "withheld from
the shareable version". Do not use this template for possible sexual imagery of a minor: stop
and follow Step 0. Prefer "inconclusive" over a confident guess.

```
MEDIA VERIFICATION SUMMARY

Item: <one line describing the media and the claim. For a possible recent strike in Israel, do not name the place>

Verdict: <authentic | AI-generated | digitally manipulated | authentic but miscaptioned | not real footage | inconclusive>
Confidence: <low | medium | high>
Why this confidence: <one sentence>

Evidence by layer:
- Provenance (C2PA state Trusted/Valid/Invalid and list used, SynthID, EXIF): <what was found, or "null: stripped / none">
- Visual inspection: <strongest signals and their direction, or "no signal">
- Source tracing: <earliest appearance, geolocation, chronolocation findings, or "no match found". For a possible recent strike in Israel, never state, confirm or deny the place: write "Location checked, details withheld">
- External tools (optional): <tool used and result, with the reliability caveat, or "not used">

What would change this verdict:
- <the missing piece that would raise or lower confidence>

Sources:
- <every external link or tool used>

Caveat: Produced by a free AI-operated tool with no review by an expert examiner, and it can
be wrong. Not an expert opinion or evidence. A missing credential or watermark is not proof
of fakery, and automated AI detectors are unreliable. Publishing this conclusion about an
identifiable person may carry legal exposure.
```

Hebrew caveat for a Hebrew report: הופק בכלי חינמי שפועל באמצעות בינה מלאכותית, בלי בדיקה של בודק
מומחה, והוא עלול לטעות. זו אינה חוות דעת מומחה ואינה ראיה. היעדר חתימה או סימן מים אינו הוכחה
לזיוף, וגלאי בינה מלאכותית אוטומטיים אינם אמינים. פרסום המסקנה הזאת לגבי אדם מזוהה עלול ליצור
חשיפה משפטית.

## Choosing the verdict

| Situation | Verdict |
|-----------|---------|
| A `Trusted` manifest declares AI creation of the whole item, and source tracing finds nothing that conflicts | AI-generated |
| A declared AI edit on real footage | digitally manipulated, extent unknown |
| Gemini SynthID hit or another AI declaration with the extent unknown | inconclusive as to extent: an AI tool was used on all or part of this item. A failed search for an original never upgrades this |
| OpenAI Verify hit | inconclusive as to extent: likely processed by OpenAI tools, extent not shown |
| Multiple strong synthetic tells with no prior match | likely AI-generated, confidence at most medium |
| Game, simulator or CGI footage presented as real | not real footage |
| Real source found, but caption or date is false (for a possible recent strike in Israel, only an older event or footage from outside Israel, and say only that) | authentic but miscaptioned |
| A located real source with consistent context. Credentials or metadata alone never establish this | authentic |
| Clear local edits (splice, removed/added object) on otherwise real media | digitally manipulated |
| Thin or conflicting evidence across all layers | inconclusive |

## The two error modes to avoid

1. False "fake": calling real footage fake also spreads disinformation (the liar's
   dividend). Distinguish "no manipulation evidence found" from "proven authentic."
2. False "real": a clean visual pass is not proof of authenticity because generators are
   good now. An "authentic" call needs a located real source.
