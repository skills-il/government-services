#!/usr/bin/env python3
"""Read C2PA Content Credentials from an image or video using c2patool.

This is the strongest verification layer because a valid C2PA manifest is
cryptographically signed: it can state who created the asset, which tool made it
(including whether an AI generator was used), and the edit history.

IMPORTANT honesty note: the ABSENCE of a manifest proves nothing. Most authentic
media has no Content Credentials, and forwarding or screenshotting strips them
from real and fake content alike. A null result here is "no signal", not "fake".

Install c2patool (macOS): brew install c2patool
Other platforms: download a binary from the c2pa-rs releases page, or build with cargo.

Usage:
  python check_provenance.py <file>          # summary report
  python check_provenance.py <file> --detailed
"""
import argparse
import json
import shutil
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Read C2PA Content Credentials via c2patool")
    parser.add_argument("file", help="Path to the image or video to inspect")
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Show the detailed C2PA-formatted manifest (c2patool -d)",
    )
    args = parser.parse_args()

    if shutil.which("c2patool") is None:
        print(
            "c2patool not found.\n"
            "Install it with: brew install c2patool  (macOS)\n"
            "or download a binary from the c2pa-rs releases page.\n"
            "Skipping provenance; continue with metadata + visual + source layers.",
            file=sys.stderr,
        )
        return 3

    cmd = ["c2patool", args.file]
    if args.detailed:
        cmd.append("-d")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        print("c2patool timed out.", file=sys.stderr)
        return 1

    out = (result.stdout or "").strip()
    err = (result.stderr or "").strip()

    # Decide present vs. null vs. error WITHOUT relying on brittle English
    # substrings. A real manifest report contains structural tokens like
    # "manifests", "claim_generator", "active_manifest", or a JSON object.
    # c2patool's exact "no manifest" wording has changed across versions
    # (development moved from c2patool to c2pa-rs), so do not key off it.
    manifest_tokens = ("manifest", "claim_generator", "active_manifest", "validation_status")
    looks_like_manifest = out.startswith("{") or any(tok in out.lower() for tok in manifest_tokens)

    if not looks_like_manifest:
        # No structured manifest data in stdout.
        if result.returncode != 0 and err and "no" not in err.lower() and "claim" not in err.lower():
            # A genuine tool error (bad path, unsupported format), not a clean null.
            print("ERROR running c2patool. This is NOT a 'no credentials' result.", file=sys.stderr)
            print(err, file=sys.stderr)
            return 1
        print("RESULT: no Content Credentials found in this file.")
        print("Interpretation: NULL signal. This is the common case and does NOT")
        print("indicate the media is fake or real. Move on to the other layers.")
        if err:
            print("\n(c2patool stderr)\n" + err, file=sys.stderr)
        return 0

    # Try to pretty-print and surface the key fields when summary JSON is returned.
    print("RESULT: Content Credentials present. Read the signer and claim generator below.")
    try:
        data = json.loads(out)
        gen = data.get("claim_generator") or data.get("claim_generator_info")
        if gen:
            print(f"  claim_generator: {gen}")
        manifests = data.get("manifests") or {}
        active = data.get("active_manifest")
        print(f"  active_manifest: {active}")
        print(f"  manifest_count: {len(manifests)}")
        print("\nFull report:\n")
    except (json.JSONDecodeError, AttributeError):
        pass

    print(out)
    print(
        "\nReminder: a present manifest is only as trustworthy as its signer. A signed"
        "\n'created with AI' claim is strong; a signed camera-capture claim supports"
        "\nauthenticity. Verify the signer, do not stop at 'a manifest exists'."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
