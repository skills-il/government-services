#!/usr/bin/env python3
"""Dump the EXIF/metadata fields that matter for authenticity, via exiftool.

What to read from the output:
  - Make / Model / DateTimeOriginal / GPS: capture provenance. Present and
    internally consistent supports a real-camera origin.
  - Software: an edit fingerprint. A generator or editor name here (for example
    a diffusion tool or an image editor) is a meaningful lean-synthetic / edited
    signal.
  - MIMEType / FileType: sanity check the container.

Honesty note: social platforms strip EXIF on upload, so ABSENCE of metadata is
the norm for forwarded media and is NOT evidence of fakery. Read it as no signal.

Install exiftool (macOS): brew install exiftool

Usage:
  python dump_metadata.py <file>            # key fields
  python dump_metadata.py <file> --all      # full dump
  python dump_metadata.py <file> --ela out.jpg   # write an Error Level Analysis image (needs Pillow)
"""
import argparse
import shutil
import subprocess
import sys

KEY_TAGS = [
    "-Make",
    "-Model",
    "-DateTimeOriginal",
    "-CreateDate",
    "-GPSLatitude",
    "-GPSLongitude",
    "-Software",
    "-MIMEType",
    "-FileType",
    "-ImageWidth",
    "-ImageHeight",
]


def run_exiftool(path: str, all_tags: bool) -> int:
    if shutil.which("exiftool") is None:
        print(
            "exiftool not found.\n"
            "Install it with: brew install exiftool  (macOS)\n"
            "or your platform package manager.\n"
            "Skipping metadata; continue with provenance + visual + source layers.",
            file=sys.stderr,
        )
        return 3

    cmd = ["exiftool"] + ([] if all_tags else KEY_TAGS) + [path]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = (result.stdout or "").strip()
    if not out:
        print("RESULT: no readable metadata (likely stripped on upload/forward).")
        print("Interpretation: NULL signal, not evidence of fakery.")
        return 0
    print(out)
    print(
        "\nReminder: stripped or missing fields are normal for forwarded media."
        "\nA Software field naming a generator/editor is a real signal; absence is not."
    )
    return 0


def write_ela(path: str, out_path: str) -> int:
    """Error Level Analysis: re-save as JPEG and amplify the difference.

    Bright, uneven regions can hint at splicing, but ELA has a high false-positive
    rate and is easily misread. Use it as a hint only, never as a verdict.
    """
    try:
        from PIL import Image, ImageChops, ImageEnhance
    except ImportError:
        print("Pillow not installed. Install with: pip install Pillow", file=sys.stderr)
        return 3

    import os
    import tempfile

    quality = 90
    original = Image.open(path).convert("RGB")
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp_name = tmp.name
    try:
        original.save(tmp_name, "JPEG", quality=quality)
        resaved = Image.open(tmp_name)
        diff = ImageChops.difference(original, resaved)
        extrema = diff.getextrema()
        max_diff = max(e[1] for e in extrema) or 1
        scale = 255.0 / max_diff
        diff = ImageEnhance.Brightness(diff).enhance(scale)
        diff.save(out_path)
    finally:
        os.unlink(tmp_name)

    print(f"ELA image written to {out_path}")
    print(
        "Interpretation: look for regions that are noticeably brighter/different"
        "\nfrom their surroundings. This is a HINT for possible edits, not proof."
        "\nELA produces many false positives; weigh it lightly."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Dump authenticity-relevant metadata via exiftool")
    parser.add_argument("file", help="Path to the image or video")
    parser.add_argument("--all", action="store_true", help="Dump all tags, not just key ones")
    parser.add_argument("--ela", metavar="OUT", help="Write an Error Level Analysis JPEG to OUT (images only)")
    args = parser.parse_args()

    code = run_exiftool(args.file, args.all)
    if args.ela:
        ela_code = write_ela(args.file, args.ela)
        code = code or ela_code
    return code


if __name__ == "__main__":
    raise SystemExit(main())
