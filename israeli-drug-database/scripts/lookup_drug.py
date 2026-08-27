#!/usr/bin/env python3
"""Israeli MoH drug-registry lookup.

Queries the live registry at israeldrugs.health.gov.il. Nothing clinical is hardcoded.

An earlier version of this script shipped a COMMON_DRUGS dictionary carrying dose strings,
prescription status and health-basket status per BRAND. It was removed in v1.3.0 because it was
verifiably wrong against the live registry (it recorded Glucophage as in the basket when all three
registrations return health=false, and gave Ibufen an OTC/Rx split at 400 mg when IBUFEN 400 is
OTC and IBUFEN 600 is prescription), and because basket and prescription status are properties of
a registration number, not of a brand name.

This script will not print a dose, a maximum daily dose, an interaction or a pregnancy category.
Those are clinical judgements. It prints the leaflet reference instead.

Usage:
  python scripts/lookup_drug.py search acamol
  python scripts/lookup_drug.py drug "020 16 20534 00"
  python scripts/lookup_drug.py generics PARACETAMOL
  python scripts/lookup_drug.py prescription-types
"""

import argparse
import json
import ssl
from datetime import datetime, timezone
import sys
import urllib.request
import urllib.error


def _ssl_context():
    """Some Python installs (notably python.org builds on macOS) ship without a usable CA
    bundle, which makes every HTTPS call fail with CERTIFICATE_VERIFY_FAILED even though the
    server is fine. Fall back to certifi's bundle when it is available. Verification is never
    disabled: this is drug data, and an unauthenticated answer is worse than no answer."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


SSL_CONTEXT = _ssl_context()


def epoch_ms(v):
    """The registry returns some dates as epoch milliseconds. Printing the raw float is
    meaningless to a reader and easy to mistake for a registration number."""
    try:
        return datetime.fromtimestamp(float(v) / 1000, tz=timezone.utc).strftime("%d.%m.%Y")
    except (TypeError, ValueError, OSError, OverflowError):
        return str(v) if v not in (None, "") else "unknown"

BASE = "https://israeldrugs.health.gov.il/GovServiceList/IDRServer"
# brochure[].url is a bare filename, not a URL. This is the host that serves them.
BROCHURE_BASE = "https://mohpublic.health.gov.il/IsraelDrugs"
# The consumer leaflet. brochure[] is dominated by 'החמרה לעלון' (leaflet amendment notices),
# which are NOT the leaflet: for one product brochure[0] is an amendment from 2017 while the
# actual consumer leaflet is from 2026. Handing a patient the first array element and calling it
# the leaflet is the failure this filter exists to prevent.
CONSUMER_LEAFLET = "עלון לצרכן"
PAGE_SIZE = 10
MAX_PAGES = 30

HEADERS = {
    "Content-Type": "application/json",
    # The service returns its HTML error page when Accept does not admit JSON.
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Origin": "https://israeldrugs.health.gov.il",
    "Referer": "https://israeldrugs.health.gov.il/",
}

PRESCRIPTION_TYPES = [
    ("GSL", "תכשיר שניתן למכור שלא בבית מרקחת",
     "Sellable outside a pharmacy. Exposed as the isGSL filter on SearchByAdv."),
    ("OTC", "ללא מרשם",
     "No prescription needed at a pharmacy. SearchByName returns prescription=false."),
    ("Prescription", "מרשם",
     "Requires a physician's prescription. SearchByName returns prescription=true."),
    ("Restricted", "מרשם מוגבל",
     "Specialist prescription or hospital-only. Surfaces in GetSpecificDrug.limitations."),
    ("Dangerous drug", "סם מסוכן",
     "Controlled under פקודת הסמים המסוכנים, on a special prescription form."),
]


class RegistryError(RuntimeError):
    """The service did not return a real answer.

    Status codes carry no signal on this host: a fabricated endpoint path answers HTTP 200 with an
    HTML error page, and a real endpoint under load answers HTTP 502 with a maintenance page. The
    only reliable test is whether the body parses as JSON.
    """


def call(action: str, payload: dict):
    req = urllib.request.Request(
        f"{BASE}/{action}",
        data=json.dumps(payload).encode("utf-8"),
        headers=HEADERS,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60, context=SSL_CONTEXT) as resp:
            raw = resp.read().decode("utf-8", "replace")
            status = resp.status
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        status = e.code
    except urllib.error.URLError as e:
        if isinstance(getattr(e, "reason", None), ssl.SSLCertVerificationError):
            raise RegistryError(
                f"{action}: TLS certificate verification failed. This is almost always a local CA "
                f"bundle problem, not the registry. Try `pip install certifi`, or on macOS run "
                f"'Install Certificates.command' in your Python folder. Do NOT work around this by "
                f"disabling verification.") from e
        raise RegistryError(f"{action}: network failure ({e}).") from e
    except Exception as e:
        raise RegistryError(f"{action}: network failure ({e}).") from e

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        if "maintanance" in raw or "maintenance" in raw or status == 502:
            raise RegistryError(
                f"{action}: the registry is in maintenance (HTTP {status}). Retry later; do not "
                f"change the call.")
        raise RegistryError(
            f"{action}: HTTP {status} but the body is not JSON. Either the endpoint name or a "
            f"parameter name is wrong. A fabricated path and a wrong parameter both return this "
            f"same HTML error page under a 200.")


def search_by_name(val, page=1):
    return call("SearchByName", {
        "val": val, "prescription": False, "healthServices": False,
        "pageIndex": page, "orderBy": 0,
    })


def all_pages(val):
    """Page to completion. Ten results is a page, not an answer."""
    first = search_by_name(val, 1)
    rows = list(first.get("results") or [])
    pages = rows[0].get("pages") if rows else 1
    try:
        pages = int(pages or 1)
    except (TypeError, ValueError):
        pages = 1
    for pg in range(2, min(pages, MAX_PAGES) + 1):
        rows.extend(search_by_name(val, pg).get("results") or [])
    truncated = pages > MAX_PAGES
    return rows, pages, truncated


def fmt_row(r):
    return (f"  {r.get('dragRegNum','?'):<20} {(r.get('dragEnName') or '')[:34]:<34} "
            f"basket={str(r.get('health')):<5} rx={str(r.get('prescription')):<5} "
            f"price={r.get('customerPrice')}")


def cmd_search(args):
    rows, pages, truncated = all_pages(args.name)
    live = [r for r in rows if not r.get("iscanceled")]
    cancelled = len(rows) - len(live)
    suffix = f" ({cancelled} cancelled, not shown)" if cancelled else ""
    print(f"{len(live)} active registration(s) across {pages} page(s) for "
          f"{args.name!r}{suffix}\n")
    if not live:
        print("  No active registrations matched.")
        print("\nThat is not the same as 'this drug does not exist'. Try the active ingredient")
        print("instead of the trade name: Israeli brand names often differ from international")
        print("ones. If it is genuinely unregistered in Israel, say so and stop.")
        return
    for r in live:
        print(fmt_row(r))
    print("\nBasket and prescription status are per registration number, not per brand: the rows")
    print("above can and do disagree with each other. price is the regulated maximum consumer")
    print("price, NOT your copay; a price of 0 means the drug is not sold at retail.")
    if truncated:
        print(f"WARNING: stopped at {MAX_PAGES} pages; this list is INCOMPLETE.")


def cmd_drug(args):
    d = call("GetSpecificDrug", {"dragRegNum": args.reg})
    if not isinstance(d, dict) or not d.get("dragRegNum"):
        raise RegistryError(
            f"no registration found for {args.reg!r}. Registration numbers are space-separated "
            f"(e.g. \"020 16 20534 00\"). Use the search subcommand to find the right one; do not "
            f"guess a number.")
    print(f"{d.get('dragEnName')}  /  {d.get('dragHebName')}")
    print(f"  registration : {d.get('dragRegNum')}   registered {epoch_ms(d.get('regDate'))}"
          f"   expires {epoch_ms(d.get('regExpDate'))}")
    print(f"  holder       : {d.get('regOwnerName')}")
    print(f"  form         : {d.get('dosageFormEng')}   route {d.get('usageFormEng')}")
    for a in d.get("atc") or []:
        print(f"  ATC          : {a.get('atc5Code')} {a.get('atc5Name')}")
    print(f"  cancelled    : {d.get('iscanceled')}")
    print(f"  max price    : {d.get('maxPrice')}  (regulated ceiling, not a copay)")
    print(f"  in basket    : {d.get('health')}")
    print(f"  limitations  : {(d.get('limitations') or '').strip() or '(none)'}")
    sal = d.get("salList") or []
    print(f"  basket indications listed: {len(sal)}")
    if sal:
        print("  -> Entitlement exists ONLY for the listed indications. Answering 'yes, it is")
        print("     covered' from the basket flag alone would be wrong for any other diagnosis.")
        for e in sal[:3]:
            print(f"     - {' '.join((e.get('indication') or '').split())[:140]}")
        if len(sal) > 3:
            print(f"     ... and {len(sal) - 3} more.")
    else:
        print("  -> No per-indication list: read 'limitations' for who may prescribe.")
    fw = " ".join((d.get("frameworkOfInclusion") or "").split())
    if fw:
        print(f"  framework    : {fw[:220]}")
    leaflets = [b for b in (d.get("brochure") or [])
                if (b.get("type") or "").strip() == CONSUMER_LEAFLET]
    if leaflets:
        leaflets.sort(key=lambda b: b.get("updateDate") or 0, reverse=True)
        print("  consumer leaflet(s), newest first:")
        seen = set()
        for b in leaflets:
            lng = (b.get("lng") or "").strip() or "?"
            if lng in seen:
                continue
            seen.add(lng)
            print(f"    [{lng}] {epoch_ms(b.get('updateDate'))}  "
                  f"{BROCHURE_BASE}/{b.get('url')}")
        print("    Read these for dosing and contraindications. This tool will not state either.")
    else:
        print("  consumer leaflet: none published under this registration. Ask the pharmacist;")
        print("    do NOT substitute a leaflet amendment notice or another product's leaflet.")
    print()
    print("NOTE: prescription status is deliberately NOT reported here. GetSpecificDrug's")
    print("isPrescription contradicts SearchByName for real products (Keytruda: true vs false).")
    print("Use the search subcommand, and confirm with the pharmacy.")


def cmd_generics(args):
    rows, pages, truncated = all_pages(args.ingredient)
    want = args.ingredient.strip().upper()
    hits = [r for r in rows
            if (r.get("activeComponentsCompareName") or "").strip().upper() == want
            and not r.get("iscanceled")]
    print(f"{len(hits)} active registration(s) with activeComponentsCompareName == {want!r} "
          f"({pages} page(s) scanned)\n")
    for r in hits:
        print(fmt_row(r))
    prices = []
    for r in hits:
        try:
            v = float(r.get("customerPrice"))
        except (TypeError, ValueError):
            continue
        if v > 0:
            prices.append(v)
    if prices:
        print(f"\nRetail price range actually retrieved: {min(prices):.2f} to {max(prices):.2f} NIS.")
        print("Compare these figures. Do not quote a percentage saving: no such figure is published")
        print("and the spread above would make any single headline number wrong.")
    if truncated:
        print(f"WARNING: stopped at {MAX_PAGES} pages; this list is INCOMPLETE.")
    print("\nSwitching between products is a decision for the prescriber and the pharmacist.")


def cmd_prescription_types(_args):
    print("Israeli prescription categories\n")
    for en, he, note in PRESCRIPTION_TYPES:
        print(f"  {en:<16} {he}")
        print(f"                   {note}")
    print("\n'סם מסוכן' is the statutory term (פקודת הסמים המסוכנים). Earlier versions of this")
    print("skill used 'sam mefakach', which is not the term the Ministry uses.")


def main():
    ap = argparse.ArgumentParser(description="Israeli MoH drug-registry lookup (live).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="Search registrations by trade or generic name.")
    s.add_argument("name")
    s.set_defaults(func=cmd_search)

    d = sub.add_parser("drug", help="Full record by registration number, with basket indications.")
    d.add_argument("reg", help='e.g. "020 16 20534 00"')
    d.set_defaults(func=cmd_drug)

    g = sub.add_parser("generics", help="Registrations sharing an exact active ingredient.")
    g.add_argument("ingredient", help="e.g. PARACETAMOL")
    g.set_defaults(func=cmd_generics)

    p = sub.add_parser("prescription-types", help="The five statutory categories.")
    p.set_defaults(func=cmd_prescription_types)

    args = ap.parse_args()
    try:
        args.func(args)
    except RegistryError as e:
        print(f"Refusing to answer: {e}", file=sys.stderr)
        print("Tell the user the registry could not be queried. Do not answer from memory.",
              file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
