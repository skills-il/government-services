# Visual artifact checklist (2026)

This is the layer where the agent uses its own image vision. It is informed judgment,
never proof. Record each item as a signal with a direction: leans-synthetic,
leans-authentic, or neutral. Do not collapse into a verdict here.

## Tells that are now UNRELIABLE (do not lean on these)

Modern generators fixed these, so a clean result proves nothing:
- Hands and fingers: largely correct now. A normal hand is not evidence of authenticity.
- Latin-script text and captions: often rendered correctly now.
- General sharpness and resolution: high quality is trivial to produce.

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
- Blink cadence. Absent, too-rare, or mechanical blinking.
- Lip-sync drift. Mute the audio and watch the mouth; then listen and check alignment.
- Motion warping. Background or limbs warping as the subject moves.

## How to weight the visual layer

- Several strong tells together: meaningful lean-synthetic, but still corroborate with
  provenance and source tracing.
- One ambiguous tell: neutral. Note it, do not let it drive the verdict.
- A clean visual pass: NOT evidence of authenticity (generators are good now). It only
  means the visual layer added no signal.
