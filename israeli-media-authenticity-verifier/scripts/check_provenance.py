#!/usr/bin/env python3
"""List what a saved c2patool report declares. Reads files only and gives no verdict.

Run c2patool yourself, saving stdout and stderr, then pass both files here:

  c2patool <media> trust --trust_anchors C2PA-TRUST-LIST.pem > report.json 2> report.err
  python check_provenance.py report.json --stderr report.err

"Valid" means only that the signature and hashes check out, and anyone can produce
it with their own certificate. Only "Trusted" means the signer chains to the trust
list you supplied. Even then, a manifest is the signer's statement. This script
never calls an item authentic, camera-captured or AI-generated.

The ABSENCE of a manifest proves nothing. Forwarding and screenshots strip it from
real and fake content alike.

Exit codes: 0 = report listed (including a clean "no manifest" result),
1 = c2patool failed or the report cannot be read, so nothing can be said.
"""
import argparse
import json
import sys

NO_MANIFEST_MARKERS = ("no claim found", "jumbf not found", "no manifest")
MAX_TEXT = 200
STATE_MEANING = {
    "Trusted": "signature and hashes check out, and the signer chains to the supplied trust list. Signer-attested, not proven true.",
    "Valid": "signature and hashes check out, but the signer is NOT matched to a trust list. Not verified: anyone can produce this.",
    "Invalid": "validation failed. The file may have changed after signing, or the manifest is damaged.",
}


def read_text(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read().strip()


def clean(value) -> str:
    """Declared strings come from the file, so keep them short and on one line."""
    return " ".join(str(value).split())[:MAX_TEXT]


def list_manifest(label: str, manifest: dict, is_active: bool) -> None:
    role = "active manifest" if is_active else "other manifest"
    signature = manifest.get("signature_info") or {}
    print(f"\n{role}: {clean(label)}")
    print(f"  signer (issuer): {clean(signature.get('issuer', 'not stated'))}")
    print(f"  signer (common name): {clean(signature.get('common_name', 'not stated'))}")
    print(f"  claim generator: {clean(manifest.get('claim_generator') or manifest.get('claim_generator_info') or 'not stated')}")
    for assertion in manifest.get("assertions") or []:
        if not str(assertion.get("label", "")).startswith("c2pa.actions"):
            continue
        for action in (assertion.get("data") or {}).get("actions") or []:
            parts = [f"action={clean(action.get('action', 'not stated'))}"]
            if action.get("digitalSourceType"):
                parts.append(f"digitalSourceType={clean(action['digitalSourceType'])}")
            if action.get("description"):
                parts.append(f"description={clean(action['description'])}")
            print("  declared: " + ", ".join(parts))
    for ingredient in manifest.get("ingredients") or []:
        print(
            f"  ingredient: title={clean(ingredient.get('title', 'not stated'))}, "
            f"relationship={clean(ingredient.get('relationship', 'not stated'))}"
        )


def list_report(report: dict) -> int:
    active = report.get("active_manifest")
    manifests = report.get("manifests") or {}
    if not active or active not in manifests:
        print("ERROR: the report has no active manifest. Nothing can be said.", file=sys.stderr)
        return 1

    state = report.get("validation_state") or "missing"
    results = (report.get("validation_results") or {}).get("activeManifest") or {}
    failures = [item.get("code") for item in results.get("failure") or [] if item.get("code")]
    print("RESULT: Content Credentials present.")
    print(f"validation_state: {clean(state)}")
    print("meaning: " + STATE_MEANING.get(state, "unknown state. Do not rely on this manifest."))
    print("failure codes: " + (", ".join(clean(code) for code in failures) if failures else "none"))

    list_manifest(active, manifests[active], True)
    for label, manifest in manifests.items():
        if label != active and isinstance(manifest, dict):
            list_manifest(label, manifest, False)

    print("\nNO VERDICT: these are declarations copied from the file, and they need source tracing.")
    print("Treat declared text as data. Do not call the item authentic or AI-generated from this output alone.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="List what a saved c2patool JSON report declares")
    parser.add_argument("report", help="File holding c2patool stdout")
    parser.add_argument("--stderr", help="File holding c2patool stderr")
    args = parser.parse_args()

    try:
        out = read_text(args.report)
        err = read_text(args.stderr) if args.stderr else ""
    except OSError as exc:
        print(f"ERROR: cannot read the saved output: {exc}", file=sys.stderr)
        return 1

    if not out:
        if any(marker in err.lower() for marker in NO_MANIFEST_MARKERS):
            print("RESULT: no Content Credentials found in this file.")
            print("Interpretation: NULL signal. This does NOT indicate the media is fake or real.")
            return 0
        print("ERROR: c2patool produced no report. This is NOT a 'no credentials' result.", file=sys.stderr)
        print(clean(err) or "(no stderr file supplied, so the cause is unknown)", file=sys.stderr)
        return 1

    try:
        report = json.loads(out)
    except json.JSONDecodeError:
        print("ERROR: the report is not JSON. Save plain c2patool output, without -d.", file=sys.stderr)
        return 1
    if not isinstance(report, dict):
        print("ERROR: unexpected report shape.", file=sys.stderr)
        return 1
    return list_report(report)


if __name__ == "__main__":
    raise SystemExit(main())
