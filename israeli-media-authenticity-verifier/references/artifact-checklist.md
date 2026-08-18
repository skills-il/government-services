# Visual artifact checklist (2026)

This is the layer where the agent uses its own image vision. It is informed judgment,
never proof. Record each item as a signal with a direction: leans-synthetic,
leans-authentic, or neutral. Do not collapse into a verdict here.

## Tells that are now UNRELIABLE (do not lean on these)

Modern generators fixed these, so a clean result proves nothing:
- Hands and fingers: largely correct now. A normal hand is not evidence of authenticity.
- Latin-script text and captions: often rendered correctly now.
- General sharpness and resolution: high quality is trivial to produce.
- **Lip-sync, and by the same reasoning blink cadence (video).** These were the classic
  deepfake tells and they no longer hold as a class. The cited source below speaks directly
  to audio and lip motion; the blink half is our inference from the same mechanism (a fully
  generated clip renders the eyes too, so there is no face-swap seam), not a sourced finding. Current video generators produce speech and picture jointly rather
  than pasting a face onto a clip: Google says of Veo that it "lets you add sound effects,
  ambient noise, and even dialogue to your creations - generating all audio natively"
  (https://deepmind.google/models/veo/). Correct lips and normal blinking are therefore the
  expected output of a good generator, not a sign of a real recording. The narrow residue
  Google itself still concedes is that "creating videos with natural and consistent spoken
  audio, particularly for shorter speech segments, remains an area of active development",
  so incoherent or glitching speech in a SHORT segment is a weak lean-synthetic signal, and
  its absence means nothing.

**Consequence for video: there may be NO visual tell at all.** For a modern text-to-video
generation of a talking person, the vision pass can legitimately return zero signal on an
entirely synthetic clip. When that happens the verdict must rest on provenance and on
earliest-copy tracing, not on "it looked fine."

If you catch yourself concluding "real" because the hands look fine, stop.

## Tells that still hold (weight these)

For images:
- Non-Latin text and signage. Hebrew and Arabic letters are frequently garbled,
  inconsistent, or nonsensical in AI images. This is one of the strongest remaining tells
  for Israeli content.
- Shadow and reflection physics. Shadows pointing the wrong way, missing reflections, or
  reflections that do not match the scene.
- Light source consistency. Faces or objects lit from impossible or conflicting directions.
- Jewelry, accessories, and symmetry. Earrings that differ, glasses that merge into skin,
  straps that vanish.
- Skin and texture. Plastic, over-smooth, or waxy skin; repeating texture patterns.
- Background coherence. Warped architecture, melting crowds, objects that merge, repeated
  faces in a crowd.
- Edges and seams. Halos or smearing around a subject (a sign of compositing).

For video (extract frames with `scripts/extract_frames.py`):
- Temporal flicker. Details that pop in and out between frames (teeth, jewelry, freckles).
- Identity drift. A face subtly changing shape or features across frames (per-frame swaps).
- Motion warping. Background or limbs warping as the subject moves.
- Incoherent or glitching speech in a SHORT segment, which is the one narrow audio-video
  weakness the generators' own documentation still concedes. Weak signal, and its absence
  means nothing. Blink cadence and lip-sync belong in the UNRELIABLE list above; do not
  re-add them here.

## How to weight the visual layer

- Several strong tells together: meaningful lean-synthetic, but still corroborate with
  provenance and source tracing.
- One ambiguous tell: neutral. Note it, do not let it drive the verdict.
- A clean visual pass: NOT evidence of authenticity (generators are good now). It only
  means the visual layer added no signal.
