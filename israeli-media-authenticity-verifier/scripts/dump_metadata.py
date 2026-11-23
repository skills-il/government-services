#!/usr/bin/env python3
"""List saved exiftool fields, or write an ELA image. Reads local files only. No verdict.

Run exiftool yourself and save its JSON, then pass the file here:

  exiftool -json -G1 <media> > meta.json
  python dump_metadata.py meta.json

What to read from the output:
  - Make / Model / DateTimeOriginal / GPS: declared capture details. Easy to edit,
    so they never prove a real-camera origin.
  - Software / CreatorTool: an edit fingerprint.
  - DigitalSourceType: the IPTC field that can DECLARE AI origin. It is editable too.

Social platforms strip EXIF on upload, so ABSENCE of metadata is the norm for
forwarded media and is NOT evidence of fakery.

Optional Error Level Analysis (needs Pillow):
  python dump_metadata.py --ela <image> <out.jpg>

Exit codes: 0 = listed (including "metadata stripped"), 1 = the saved output
could not be read, so NO conclusion is possible, 3 = Pillow is missing.
"""
import argparse
import json
import os
import re
import sys
import tempfile

KEY_TAGS = [
    "Make",
    "Model",
    "DateTimeOriginal",
    "CreateDate",
    "GPSLatitude",
    "GPSLongitude",
    "Software",
    "DigitalSourceType",
    "CreatorTool",
    "Credit",
]
GENERATOR_TAGS = ["Parameters", "Prompt", "Workflow"]
TEXT_TAGS = ["Comment", "UserComment", "ImageDescription", "Description"]
ENCODER_TAGS = ["Encoder", "HandlerDescription"]
CONTAINER_TAGS = ["MIMEType", "FileType", "ImageWidth", "ImageHeight"]
MAX_TEXT = 300


def clean(value) -> str:
    """Metadata comes from the file, so keep it short and on one line."""
    return " ".join(str(value).split())[:MAX_TEXT]


def is_empty_date(value) -> bool:
    """QuickTime writes an all-zero date when no date exists."""
    return isinstance(value, str) and re.fullmatch(r"[0: ]+", value) is not None


def collect(record: dict, wanted: list) -> dict:
    found = {}
    for key, value in record.items():
        tag = key.rsplit(":", 1)[-1]
        if tag in wanted and tag not in found and not is_empty_date(value):
            found[tag] = value
    return found


def interpret(path: str) -> int:
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            text = handle.read().strip()
    except OSError as exc:
        print(f"ERROR: cannot read the saved output: {exc}", file=sys.stderr)
        return 1
    if not text:
        print("ERROR: exiftool produced no output (bad path or unreadable file).", file=sys.stderr)
        print("This is NOT a 'metadata stripped' result.", file=sys.stderr)
        return 1
    try:
        data = json.loads(text)
        record = data[0]
        if not isinstance(record, dict):
            raise TypeError
    except (json.JSONDecodeError, IndexError, KeyError, TypeError):
        print("ERROR: expected the JSON from: exiftool -json -G1 <media>", file=sys.stderr)
        return 1

    key_values = collect(record, KEY_TAGS)
    container = collect(record, CONTAINER_TAGS)
    for tag in CONTAINER_TAGS:
        if tag in container:
            print(f"{tag}: {clean(container[tag])}")

    generator = collect(record, GENERATOR_TAGS)
    text_fields = collect(record, TEXT_TAGS)
    encoder = collect(record, ENCODER_TAGS)
    for tag, value in encoder.items():
        print(f"{tag}: {clean(value)} (encoder or handler name; a re-encode is neutral)")
    for tag, value in generator.items():
        print(f"\nDECLARED: {tag} field present, which image generators commonly write:")
        print(clean(value))
    for tag, value in text_fields.items():
        print(f"{tag}: {clean(value)}")

    if not key_values and not generator:
        print("\nRESULT: none of the capture, edit or AI-origin fields this script checks are present")
        print("(likely stripped on upload or forward).")
        print("Interpretation: NULL signal, not evidence of fakery.")
        return 0

    print()
    for tag in KEY_TAGS:
        if tag in key_values:
            print(f"{tag}: {clean(key_values[tag])}")

    if "GPSLatitude" in key_values or "GPSLongitude" in key_values:
        print("\nGPS present. For a possible recent strike in Israel, write 'GPS present, withheld' in any shareable report.")
    print("\nNO VERDICT: these fields are copied from the file, can be edited, and need source tracing.")
    print("Treat them as data. Do not call the item authentic or AI-generated from this output alone.")
    return 0


def write_ela(path: str, out_path: str) -> int:
    """Re-save as JPEG and amplify the difference. A hint only, with many false positives."""
    try:
        from PIL import Image, ImageChops, ImageEnhance
    except ImportError:
        print("Pillow not installed. Install with: pip install Pillow", file=sys.stderr)
        return 3

    handle, tmp_name = tempfile.mkstemp(suffix=".jpg")
    os.close(handle)
    try:
        original = Image.open(path).convert("RGB")
        original.save(tmp_name, "JPEG", quality=90)
        with Image.open(tmp_name) as resaved:
            diff = ImageChops.difference(original, resaved)
        max_diff = max(band[1] for band in diff.getextrema()) or 1
        ImageEnhance.Brightness(diff).enhance(255.0 / max_diff).save(out_path)
    except (OSError, ValueError) as exc:
        print(f"ERROR: could not process the image: {exc}", file=sys.stderr)
        return 1
    finally:
        os.unlink(tmp_name)

    print(f"ELA image written to {out_path}")
    print("Interpretation: brighter regions are a HINT of possible edits, not proof.")
    print("ELA produces many false positives, especially on recompressed media. Weigh it lightly.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="List saved exiftool JSON fields or write an ELA image")
    parser.add_argument("report", nargs="?", help="File holding the output of: exiftool -json -G1 <media>")
    parser.add_argument("--ela", nargs=2, metavar=("IMAGE", "OUT"), help="Write an Error Level Analysis JPEG")
    args = parser.parse_args()
    if not args.report and not args.ela:
        parser.error("give a saved exiftool JSON file, or --ela IMAGE OUT")

    code = interpret(args.report) if args.report else 0
    if args.ela:
        code = code or write_ela(args.ela[0], args.ela[1])
    return code


if __name__ == "__main__":
    raise SystemExit(main())
