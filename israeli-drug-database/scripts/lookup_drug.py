#!/usr/bin/env python3
"""Israeli MoH drug-registry lookup.

Queries the live registry at registries.health.gov.il/Medicines. Nothing clinical is hardcoded.

The Ministry has moved the registry off israeldrugs.health.gov.il (confirmed 2026-10-28). That host now only
redirects to registries.health.gov.il/Medicines, and the old POST API under
/GovServiceList/IDRServer/ answers 403 from CloudFront. Versions of this script before 1.4.0
called that dead API and cannot work any more.

An earlier version of this script shipped a COMMON_DRUGS dictionary carrying dose strings,
prescription status and health-basket status per BRAND. It was removed in v1.3.0 because it was
verifiably wrong against the live registry, and because basket and prescription status are
properties of a registration number, not of a brand name.

This script will not print a dose, a maximum daily dose, an interaction or a pregnancy category.
Those are clinical judgements. It prints the leaflet link instead.

Usage:
  python scripts/lookup_drug.py search acamol
  python scripts/lookup_drug.py drug "020 16 20534 00"
  python scripts/lookup_drug.py generics PARACETAMOL
  python scripts/lookup_drug.py prescription-types
"""

import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request


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

BASE = "https://registries.health.gov.il/api/Medicines"
# GetMedicineDocuments returns fName, a bare filename. This is the host that serves the files.
DOC_BASE = "https://pharmaceuticalreg.health.gov.il/api/pharmaregistration/IsraelDrugs"
# The consumer leaflet. The document list also carries 'החמרה לעלון' / 'החמרה לעלון לצרכן'
# entries, which are leaflet AMENDMENT notices, not the leaflet. Handing a patient one of those and
# calling it the leaflet is the failure this filter exists to prevent. It does NOT mean amendments
# are ignored: see AMENDMENTS.
CONSUMER_LEAFLET = "עלון לצרכן"
# Safety-tightening notices. One that is newer than every consumer leaflet means the leaflet may
# not yet reflect it. Physician-leaflet amendments (החמרה לעלון לרופא) are not included.
AMENDMENTS = {"החמרה לעלון", "החמרה לעלון לצרכן"}
PAGE_SIZE = 100
MAX_PAGES = 20

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Referer": "https://registries.health.gov.il/Medicines",
}

PRESCRIPTION_TYPES = [
    ("GSL", "תרופות לשיווק כללי",
     "Sellable outside a pharmacy. The registry's telemOnly search filter selects them."),
    ("OTC", "ללא מרשם",
     "No prescription needed at a pharmacy. packages[].mirsham = 0, set per pack size."),
    ("Prescription", "מרשם",
     "Requires a physician's prescription. packages[].mirsham = 1, set per pack size."),
    ("Restricted", "מרשם מוגבל",
     "Specialist prescription or hospital-only. Surfaces in the 'limitations' field."),
    ("Dangerous drug", "סם מסוכן",
     "Controlled under פקודת הסמים המסוכנים, on a special prescription form."),
]


class RegistryError(RuntimeError):
    """The service did not return a real answer.

    Every real answer is JSON of the shape {returnObject, statusCode, message}. The HTTP status
    carries no signal: a registration that does not exist answers 200 with statusCode 404 inside
    the body, a misspelt endpoint or wrong method answers 200 with an HTML error page, and a
    missing parameter answers 200 with {"ClientMessage", "StatusCode": 400}. The retired
    israeldrugs.health.gov.il API answers 403. So the test is: does the body parse as JSON, and is
    the inner lowercase statusCode exactly 200.
    """


def _request(path, payload=None):
    url = f"{BASE}/{path}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=HEADERS,
                                 method="POST" if payload is not None else "GET")
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
                f"{path}: TLS certificate verification failed. This is almost always a local CA "
                f"bundle problem, not the registry. Try `pip install certifi`, or on macOS run "
                f"'Install Certificates.command' in your Python folder. Do NOT work around this by "
                f"disabling verification.") from e
        raise RegistryError(f"{path}: network failure ({e}).") from e
    except Exception as e:
        raise RegistryError(f"{path}: network failure ({e}).") from e

    try:
        body = json.loads(raw)
    except json.JSONDecodeError:
        raise RegistryError(
            f"{path}: HTTP {status} but the body is not JSON. On this host that means the "
            f"endpoint name or the method is wrong (both return an HTML error page under a 200), "
            f"or the service is down.")
    if not isinstance(body, dict) or body.get("statusCode") != 200:
        code = body.get("statusCode") if isinstance(body, dict) else "?"
        msg = body.get("message") if isinstance(body, dict) else None
        raise RegistryError(f"{path}: registry answered statusCode {code}"
                            f"{f' ({msg})' if msg else ''}.")
    return body.get("returnObject")


def get_medicines(**filters):
    payload = {"sortBy": "tradeNameHeb", "sortDirection": "asc", "maxResult": PAGE_SIZE,
               "pageNumber": 0, "includeActive": True, "includeCanceled": False}
    payload.update(filters)
    return _request("GetMedicines", payload)


def all_pages(**filters):
    """Page to completion. One page is a page, not an answer. pageNumber is zero-based."""
    first = get_medicines(**filters)
    rows = list(first.get("medicinesList") or [])
    total = int(first.get("totalRows") or 0)
    pages = max(1, -(-total // PAGE_SIZE))
    for pg in range(1, min(pages, MAX_PAGES)):
        rows.extend(get_medicines(pageNumber=pg, **filters).get("medicinesList") or [])
    return rows, total, pages > MAX_PAGES


def rx_status(r):
    """Prescription status is per PACKAGE, in packages[].mirsham (1 = prescription, 0 = not).
    One registration can have both: SINUFED TABLETS sells its 10-tablet pack without a
    prescription and its larger packs on prescription only. The registry's otcOnly search filter
    drops such mixed registrations entirely, so it must not be used to label them Rx."""
    flags = {p.get("mirsham") for p in (r.get("packages") or [])}
    if flags == {0}:
        return "OTC"
    if flags == {1}:
        return "Rx"
    if flags == {0, 1}:
        return "mixed"
    return "?"


def listed_prices(r):
    """customerPriceWithTax per package. 0 means the registry lists no price for that pack. It is
    0 for most prescription packs (every Lipitor pack, for example), so it does NOT mean the
    product is unavailable at retail, and it does not mean free."""
    return [p.get("customerPriceWithTax") for p in (r.get("packages") or [])
            if p.get("customerPriceWithTax")]


def fmt_row(r):
    prices = listed_prices(r)
    price = ", ".join(f"{p:.2f}" for p in prices) if prices else "none listed"
    vet = " VET" if r.get("veterinaryUse") == "כן" else ""
    return (f"  {r.get('regNumber','?'):<17} {(r.get('tradeName') or '').strip()[:34]:<34} "
            f"basket={r.get('basket','?'):<3} {rx_status(r):<5} price={price}{vet}")


def cmd_search(args):
    rows, total, truncated = all_pages(searchText=args.name)
    print(f"{total} active registration(s) for {args.name!r}\n")
    if not rows:
        print("  No active registrations matched.")
        print("\nThat is not the same as 'this drug does not exist'. Try the active ingredient")
        print("instead of the trade name: Israeli brand names often differ from international")
        print("ones. If it is genuinely unregistered in Israel, say so and stop.")
        return
    for r in rows:
        print(fmt_row(r))
    print("\nBasket (כן/לא) and OTC/Rx are per registration number, not per brand, and OTC/Rx is")
    print("really per PACK: 'mixed' means some pack sizes need a prescription and some do not; run")
    print("the drug subcommand for the per-pack list. price is the consumer price the registry lists")
    print("per pack, NOT your copay; 'none listed' is normal for prescription packs and does not")
    print("mean the product is unavailable. VET marks a veterinary product.")
    if truncated:
        print(f"WARNING: stopped at {MAX_PAGES} pages; this list is INCOMPLETE.")


def _lang(x):
    return (x.get("language") or "").strip() or (x.get("langDesc") or "").strip() or "language not stated"


def _day(x):
    return str(x.get("updateDate") or "")[:10]


def split_leaflets(docs):
    """Returns (current, older). Archived uploads (fName starting 'Arc') are dropped. In each
    language, the leaflets from the newest upload DAY are 'current'; every other leaflet is kept
    but labelled 'older'. Older is not the same as superseded: ACAMOL TEVA CAPLETS 176 61 37219 99
    has a general-sale Hebrew leaflet from 2025-12-17 and a pharmacy Hebrew leaflet from
    2025-11-24, and both are in force. A leaflet with no language is compared against the newest
    leaflet of ANY language, since it is usually an older upload of one of them."""
    by_lang = {}
    for x in docs:
        if (x.get("type") or "").strip() != CONSUMER_LEAFLET:
            continue
        if str(x.get("fName") or "").startswith("Arc"):
            continue
        by_lang.setdefault(_lang(x), []).append(x)
    if not by_lang:
        return [], []
    overall = max(_day(x) for xs in by_lang.values() for x in xs)
    current, older = [], []
    for lang, xs in by_lang.items():
        top = overall if lang == "language not stated" else max(_day(x) for x in xs)
        for x in xs:
            (current if _day(x) == top else older).append(x)
    key = lambda x: (_lang(x), x.get("updateDate") or "")
    return sorted(current, key=key, reverse=True), sorted(older, key=key, reverse=True)


def late_amendments(docs, leaflets):
    """Amendment notices dated on a LATER DAY than the newest current leaflet of some language.
    Same-day notices are part of the leaflet's own upload batch, so they are not flagged. Known
    blind spot: a genuinely later notice uploaded on the same day as the leaflet is missed; every
    same-day case seen had sequential file ids with the leaflet, i.e. one batch."""
    newest = {}
    for x in leaflets:
        newest[_lang(x)] = max(newest.get(_lang(x), ""), _day(x))
    out = []
    for x in docs:
        if (x.get("type") or "").strip() not in AMENDMENTS:
            continue
        langs = [lang for lang, d in newest.items() if _day(x) > d]
        if langs:
            out.append((x, sorted(langs)))
    return sorted(out, key=lambda t: t[0].get("updateDate") or "", reverse=True)


def cmd_drug(args):
    q = urllib.parse.quote(args.reg)
    try:
        d = _request(f"GetMedicineByRegNumber?regNumber={q}")
    except RegistryError as e:
        if "statusCode 404" in str(e):
            raise RegistryError(
                f"no registration found for {args.reg!r}. Registration numbers are space-separated "
                f"(e.g. \"020 16 20534 00\"). Use the search subcommand to find the right one; do "
                f"not guess a number.") from e
        raise
    mid = d.get("medicineId")
    print(f"{(d.get('tradeName') or '').strip()}  /  {(d.get('tradeNameHeb') or '').strip()}")
    print(f"  registration : {d.get('regNumber')}   registered {str(d.get('regDate'))[:10]}"
          f"   expires {str(d.get('regExpDate'))[:10]}")
    print(f"  holder       : {d.get('ownerName')}   manufacturer {d.get('manufacturerName')}")
    print(f"  form         : {d.get('dosageFormE')}"
          f"{'   VETERINARY' if d.get('veterinaryUse') == 'כן' else ''}")
    for c in d.get("components") or []:
        print(f"  ingredient   : {c.get('componentDesc')} {(c.get('dosage') or '').strip()}")
    for a in _request(f"GetMedicineAtc?medicineId={mid}") or []:
        if a.get("level") == 5:
            print(f"  ATC          : {a.get('atcCode')} {a.get('atcDesc')}")
    print(f"  cancelled    : {d.get('canceled')}")
    packs = _request(f"GetMedicinePackages?medicineId={mid}") or []
    print("  packs (prescription status and listed price are per pack):")
    for p in packs:
        rx = {0: "no prescription", 1: "prescription"}.get(p.get("mirsham"), "?")
        price = p.get("customerPriceWithTax")
        print(f"    {(p.get('quantity') or '').strip():<18} {rx:<16} "
              f"price={f'{price:.2f}' if price else 'none listed'}")
    print("    A listed price is the consumer price, not a copay. 'none listed' is normal for")
    print("    prescription packs; it does not mean free or unavailable.")
    print(f"  in basket    : {d.get('basket')}")
    print(f"  limitations  : {(d.get('limitations') or '').strip() or '(none)'}")
    sal = _request(f"GetMedicineBasketIndications?medicineId={mid}") or []
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
    print("     Basket terms apply when the drug is supplied through the kupah, not to a purchase")
    print("     at the counter.")
    fw = " ".join((d.get("framework") or "").split())
    if fw:
        print(f"  framework    : {fw[:220]}")
    docs = _request(f"GetMedicineDocuments?medicineId={mid}") or []
    leaflets, older = split_leaflets(docs)
    if leaflets:
        print("  newest consumer leaflet(s) per language. Two in one language can both be current")
        print("  (they can differ by pack or sales channel); have the user match the one for the")
        print("  pack they hold. Languages can be updated on different dates; compare the dates.")
        for x in leaflets:
            lang = _lang(x)
            hint = "  (open the file to see the language)" if lang == "language not stated" else ""
            print(f"    [{lang}] {str(x.get('updateDate'))[:10]}  {DOC_BASE}/{x.get('fName')}{hint}")
        if older:
            print("  older consumer leaflet(s). Each may be superseded OR may be the leaflet for a")
            print("  different pack or sales channel (pharmacy vs general sale). Open it and check")
            print("  the product name and channel against the pack; if unsure, ask the pharmacist:")
            for x in older:
                print(f"    [{_lang(x)}] {str(x.get('updateDate'))[:10]}  {DOC_BASE}/{x.get('fName')}")
        late = late_amendments(docs, leaflets)
        if late:
            print("  leaflet amendment notice(s) dated AFTER the current leaflet in at least one")
            print("  language. That leaflet may not yet include the change; hand these over with it:")
            for x, langs in late:
                print(f"    [{x.get('type')}] {str(x.get('updateDate'))[:10]}  "
                      f"{DOC_BASE}/{x.get('fName')}  newer than: {', '.join(langs)}")
        print("    Read these for dosing and contraindications. This tool will not state either.")
    else:
        print("  consumer leaflet: none published under this registration. Ask the pharmacist;")
        print("    do NOT substitute a leaflet amendment notice or another product's leaflet.")
    print()
    print("Confirm prescription status and the right leaflet with the pharmacist.")


# Release markers, matched as whole phrases or whole words only. As substrings they caught
# CRESTOR ('CR'), PRIZMA ('PR'), LAMICTAL ('LA') and the famotidine brand GASTRO. The registry also
# records release type inconsistently (NEXIUM and LOSEC carry no marker although proton-pump
# inhibitors are gastro-resistant, while ESOMEPRAZOLE INOVAMED says GASTRO RESISTANT), so the
# absence of a marker proves nothing and this tool never labels anything 'immediate release'.
RELEASE_MARKER = re.compile(
    r"\b(PROLONGED|EXTENDED|SLOW|MODIFIED|DELAYED|SUSTAINED|CONTROLLED|DUAL)\s+RELEASE\b"
    r"|\bGASTRO[\s-]+RESISTANT\b|\bENTERIC[\s-]+COATED\b|\bRELEASE\b"
    r"|\b(XR|XL|CR|SR|S\.R\.?|OD|ER|LA|MR|PR|PRT|RETARD|DEPOT)(?=\s|$|\.)")


def release_marker(r):
    """The release marker the registry states in the form or trade name, or None. None means
    'not stated', never 'immediate release'."""
    found = []
    for text in ((r.get("dosageFormE") or "").upper(), (r.get("tradeName") or "").upper()):
        for m in RELEASE_MARKER.finditer(" " + text + " "):
            if m.group(0).strip() not in found:
                found.append(m.group(0).strip())
    return ", ".join(found) or None


def cmd_generics(args):
    wants = [w.strip().upper() for w in args.ingredient]
    comps = _request("GetComponents") or []
    codes = [int(c["key"]) for c in comps
             if str(c.get("value") or "").strip().upper() in wants and str(c.get("key")).isdigit()]
    if not codes:
        raise RegistryError(
            f"{', '.join(wants)} is not an active-ingredient name in the registry's component "
            f"list. Use the English name as the registry spells it (e.g. PARACETAMOL, not "
            f"acetaminophen); the search subcommand shows a product's ingredient.")
    # Several codes in ONE componentCodes list are ANDed (products containing all of them), so a
    # synonym list must be queried one code at a time and merged.
    rows, seen, total, truncated = [], set(), 0, False
    for code in codes:
        part, n, cut = all_pages(componentCodes=[code])
        truncated = truncated or cut
        for r in part:
            if r.get("regNumber") not in seen:
                seen.add(r.get("regNumber"))
                rows.append(r)
    total = len(rows)
    # componentCodes also returns combination products and veterinary products. Keep human,
    # single-ingredient ones.
    hits = [r for r in rows if len(r.get("components") or []) == 1
            and r.get("veterinaryUse") != "כן"]
    print(f"{len(hits)} active human single-ingredient registration(s) "
          f"({total - len(hits)} combination or veterinary products not shown)\n")
    # One section per ingredient NAME, so two different substances passed together (e.g.
    # ESOMEPRAZOLE and PANTOPRAZOLE) are never shown as one list. Within a section, rows are
    # sorted by route then strength; the tool does not decide which rows can substitute.
    for name in wants:
        rs = [r for r in hits if (r["components"][0].get("componentDesc") or "").strip().upper() == name]
        if not rs:
            continue
        print(f"  {name}")
        def route(r):
            return ", ".join(sorted({(t.get("tzuratMatanDesc") or "?").strip()
                                     for t in (r.get("tzuratMatanCodes") or [])})) or "?"
        for r in sorted(rs, key=lambda r: (route(r), " ".join((r["components"][0].get("dosage") or "").split()))):
            dose = " ".join((r["components"][0].get("dosage") or "").split())
            mark = release_marker(r)
            print("  " + fmt_row(r) + f"   [{route(r)}; {(r.get('dosageFormE') or 'form not stated').strip()};"
                  f" {dose}]" + (f"  RELEASE MARKER: {mark}" if mark else ""))
        print()
    print("This is a list of registered products with the same active ingredient, NOT a list of")
    print("substitutes. Same ingredient and strength is necessary but not enough. Release type in")
    print("particular is not recorded reliably: do not yourself offer a RELEASE MARKER row (CR, XR,")
    print("SR, OD, RETARD, PROLONGED RELEASE, GASTRO RESISTANT...) in place of another product, and")
    print("the absence of a marker does NOT mean immediate release (NEXIUM and LOSEC carry none).")
    print("Whether such products can substitute is the pharmacist's decision. Show the list to the pharmacist, who decides what can substitute. Form")
    print("names differ in spelling (TABLETS / COATED TABLETS / FILM COATED TABLETS). Prices are")
    print("often not listed for prescription packs. Do not quote a percentage saving.")
    print("Pass several names only for the SAME substance under different entries (DIPYRONE and")
    print("METAMIZOLE SODIUM); each name gets its own section.")
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

    s = sub.add_parser("search", help="Search registrations by trade or ingredient name.")
    s.add_argument("name")
    s.set_defaults(func=cmd_search)

    d = sub.add_parser("drug", help="Full record by registration number, with basket indications.")
    d.add_argument("reg", help='e.g. "020 16 20534 00"')
    d.set_defaults(func=cmd_drug)

    g = sub.add_parser("generics", help="Registrations sharing an exact active ingredient.")
    g.add_argument("ingredient", nargs="+", help="e.g. PARACETAMOL, or several synonyms")
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
