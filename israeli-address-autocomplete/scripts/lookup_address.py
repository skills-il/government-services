#!/usr/bin/env python3
"""
Israeli Address Lookup and Validation

Standalone utility for formatting, validating, and looking up
Israeli addresses and settlement (semel yishuv) codes.

Hebrew input is the primary case. An earlier version keyed the table on Latin
transliterations only, so `city "תל אביב"` returned "not found" for every Hebrew
city name, which is what an Israeli user actually types.

Usage:
    python lookup_address.py city "תל אביב"
    python lookup_address.py city "Tel Aviv"
    python lookup_address.py format "רוטשילד 42, תל אביב"
    python lookup_address.py format "Rothschild 42, Tel Aviv"
    python lookup_address.py cities

This script resolves settlement codes and parses address structure only. It does
NOT look up postal codes (mikud): there is no keyless public API for that, so use
the Israel Post web form. See SKILL.md.
"""

import argparse
import json
import re
import sys

# CBS city codes for major Israeli cities
CITY_CODES = {
    "jerusalem": {"code": 3000, "hebrew": "yerushalayim", "area_code": "02"},
    "tel aviv-yafo": {"code": 5000, "hebrew": "tel aviv-yafo", "area_code": "03"},
    "tel aviv": {"code": 5000, "hebrew": "tel aviv-yafo", "area_code": "03"},
    "haifa": {"code": 4000, "hebrew": "haifa", "area_code": "04"},
    "rishon lezion": {"code": 8300, "hebrew": "rishon letzion", "area_code": "03"},
    "petah tikva": {"code": 7900, "hebrew": "petach tikva", "area_code": "03"},
    "ashdod": {"code": 70, "hebrew": "ashdod", "area_code": "08"},
    "netanya": {"code": 7400, "hebrew": "netanya", "area_code": "09"},
    "beer sheva": {"code": 9000, "hebrew": "beer sheva", "area_code": "08"},
    "beersheba": {"code": 9000, "hebrew": "beer sheva", "area_code": "08"},
    "holon": {"code": 6600, "hebrew": "holon", "area_code": "03"},
    "bnei brak": {"code": 6100, "hebrew": "bnei brak", "area_code": "03"},
    "ramat gan": {"code": 8600, "hebrew": "ramat gan", "area_code": "03"},
    "bat yam": {"code": 6200, "hebrew": "bat yam", "area_code": "03"},
    "rehovot": {"code": 8400, "hebrew": "rechovot", "area_code": "08"},
    "ashkelon": {"code": 7100, "hebrew": "ashkelon", "area_code": "08"},
    "herzliya": {"code": 6400, "hebrew": "herzliya", "area_code": "09"},
    "kfar saba": {"code": 6900, "hebrew": "kfar saba", "area_code": "09"},
    "raanana": {"code": 8700, "hebrew": "raanana", "area_code": "09"},
    "modiin": {"code": 1200, "hebrew": "modiin-maccabim-reut", "area_code": "08"},
    "nazareth": {"code": 7300, "hebrew": "natzrat", "area_code": "04"},
    "lod": {"code": 7000, "hebrew": "lod", "area_code": "08"},
    "ramla": {"code": 8500, "hebrew": "ramla", "area_code": "08"},
    "eilat": {"code": 2600, "hebrew": "eilat", "area_code": "08"},
    "tiberias": {"code": 6700, "hebrew": "tveria", "area_code": "04"},
    "acre": {"code": 7600, "hebrew": "akko", "area_code": "04"},
    "akko": {"code": 7600, "hebrew": "akko", "area_code": "04"},
    "nahariya": {"code": 9100, "hebrew": "nahariya", "area_code": "04"},
    "givatayim": {"code": 6300, "hebrew": "givatayim", "area_code": "03"},
    "bet shemesh": {"code": 2610, "hebrew": "bet shemesh", "area_code": "02"},
    "beit shemesh": {"code": 2610, "hebrew": "bet shemesh", "area_code": "02"},
    "hadera": {"code": 6500, "hebrew": "chadera", "area_code": "04"},
    "karmiel": {"code": 1139, "hebrew": "karmiel", "area_code": "04"},
    "carmiel": {"code": 1139, "hebrew": "karmiel", "area_code": "04"},
    "afula": {"code": 7700, "hebrew": "afula", "area_code": "04"},
}

# Hebrew name -> the Latin key above. Every entry in CITY_CODES needs one: an
# Israeli user types Hebrew, and the Latin-only table returned "not found" for
# every Hebrew city name until this was added.
HEBREW_NAMES = {
    "ירושלים": "jerusalem",
    "תל אביב": "tel aviv-yafo",
    "תל אביב-יפו": "tel aviv-yafo",
    "תל אביב יפו": "tel aviv-yafo",
    "חיפה": "haifa",
    "ראשון לציון": "rishon lezion",
    "פתח תקווה": "petah tikva",
    "פתח תקוה": "petah tikva",
    "אשדוד": "ashdod",
    "נתניה": "netanya",
    "באר שבע": "beer sheva",
    "חולון": "holon",
    "בני ברק": "bnei brak",
    "רמת גן": "ramat gan",
    "בת ים": "bat yam",
    "רחובות": "rehovot",
    "אשקלון": "ashkelon",
    "הרצליה": "herzliya",
    "כפר סבא": "kfar saba",
    "רעננה": "raanana",
    "מודיעין": "modiin",
    "מודיעין מכבים רעות": "modiin",
    "נצרת": "nazareth",
    "לוד": "lod",
    "רמלה": "ramla",
    "אילת": "eilat",
    "טבריה": "tiberias",
    "עכו": "acre",
    "נהריה": "nahariya",
    "גבעתיים": "givatayim",
    "בית שמש": "bet shemesh",
    "חדרה": "hadera",
    "כרמיאל": "karmiel",
    "עפולה": "afula",
}

# Common colloquial abbreviations, written with gershayim or a double quote.
ALIASES = {
    "ת\"א": "tel aviv-yafo",
    "תא": "tel aviv-yafo",
    "ראשל\"צ": "rishon lezion",
    "פ\"ת": "petah tikva",
    "ב\"ש": "beer sheva",
    "ירושלים עיה\"ק": "jerusalem",
}

# Alias keys are compared AFTER normalize_hebrew(), which folds hyphens to
# spaces. Any alias written with a hyphen must therefore be stored in its
# normalised form, or the normaliser defeats its own alias table.
ALIASES["י ם"] = "jerusalem"

# Hebrew letters that change form at the end of a word. Normalising them lets
# "רמת גן" match a stored "רמת גן" regardless of which form the user typed, and
# guards against copy-paste from sources that use the non-final form mid-string.
# Canonical Hebrew name per Latin key, for display. Explicit rather than derived
# from HEBREW_NAMES, because that map has several spellings per city and the
# first one encountered is not always the canonical form.
LATIN_TO_HEBREW = {
    "jerusalem": "ירושלים",
    "tel aviv-yafo": "תל אביב-יפו",
    "tel aviv": "תל אביב-יפו",
    "haifa": "חיפה",
    "rishon lezion": "ראשון לציון",
    "petah tikva": "פתח תקווה",
    "ashdod": "אשדוד",
    "netanya": "נתניה",
    "beer sheva": "באר שבע",
    "beersheba": "באר שבע",
    "holon": "חולון",
    "bnei brak": "בני ברק",
    "ramat gan": "רמת גן",
    "bat yam": "בת ים",
    "rehovot": "רחובות",
    "ashkelon": "אשקלון",
    "herzliya": "הרצליה",
    "kfar saba": "כפר סבא",
    "raanana": "רעננה",
    "modiin": "מודיעין-מכבים-רעות",
    "nazareth": "נצרת",
    "lod": "לוד",
    "ramla": "רמלה",
    "eilat": "אילת",
    "tiberias": "טבריה",
    "acre": "עכו",
    "akko": "עכו",
    "nahariya": "נהריה",
    "givatayim": "גבעתיים",
    "bet shemesh": "בית שמש",
    "hadera": "חדרה",
    "karmiel": "כרמיאל",
    "afula": "עפולה",
}

SOFIT = str.maketrans({"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"})

# Prefixes that glue onto a Hebrew place name ("בתל אביב", "מירושלים").
HEBREW_PREFIXES = ("ב", "ל", "מ", "ה", "ו", "ש", "כ")


def normalize_hebrew(text: str) -> str:
    """Fold a Hebrew place name to a comparable form.

    Strips nikkud and gershayim, collapses whitespace and hyphens, and folds
    final-form letters. Returns the input unchanged for non-Hebrew text.
    """
    t = text.strip()
    t = re.sub(r"[\u0591-\u05C7]", "", t)          # nikkud and cantillation
    t = t.replace("\u05f3", "'").replace("\u05f4", '"')  # geresh, gershayim
    t = t.replace("-", " ")
    t = re.sub(r"\s+", " ", t)
    return t


def resolve_city_key(name: str):
    """Map any user-supplied city name, Hebrew or Latin, to a CITY_CODES key."""
    raw = normalize_hebrew(name)
    low = raw.lower()

    # 1. Latin key, exact
    if low in CITY_CODES:
        return low
    # 2. Alias (ת"א, ראשל"צ, ...)
    if raw in ALIASES and ALIASES[raw] in CITY_CODES:
        return ALIASES[raw]
    # 3. Hebrew name, exact then sofit-folded
    if raw in HEBREW_NAMES:
        return HEBREW_NAMES[raw]
    folded = raw.translate(SOFIT)
    for heb, key in HEBREW_NAMES.items():
        if normalize_hebrew(heb).translate(SOFIT) == folded:
            return key
    # 4. Hebrew name carrying a single-letter prefix ("בתל אביב")
    if raw and raw[0] in HEBREW_PREFIXES:
        stripped = raw[1:].strip()
        if stripped:
            inner = resolve_city_key(stripped)
            if inner:
                return inner
    return None


def lookup_city(name: str) -> None:
    """Look up a city's CBS code and details."""
    key = resolve_city_key(name)
    city = CITY_CODES.get(key) if key else None

    if city:
        print(f"City: {name}")
        print(f"Settlement code (semel yishuv): {city['code']}")
        heb = LATIN_TO_HEBREW.get(key)
        if heb:
            print(f"Hebrew name: {heb}")
        print(f"Transliteration: {city['hebrew']}")
        print(f"Area Code: {city['area_code']}")
    else:
        # Try partial match
        normalized = normalize_hebrew(name).lower()
        matches = [
            (k, v) for k, v in CITY_CODES.items()
            if normalized in k or k in normalized
        ]
        heb = normalize_hebrew(name).translate(SOFIT)
        matches += [
            (HEBREW_NAMES[h], CITY_CODES[HEBREW_NAMES[h]])
            for h in HEBREW_NAMES
            if heb and heb in normalize_hebrew(h).translate(SOFIT)
            and HEBREW_NAMES[h] in CITY_CODES
        ]
        matches = list(dict.fromkeys(matches))
        if matches:
            print(f"No exact match for '{name}'. Possible matches:")
            for k, v in matches:
                print(f"  {k}: semel {v['code']}, area code {v['area_code']}")
        else:
            unique = len({v["code"] for v in CITY_CODES.values()})
            print(f"City '{name}' not found in this script's {unique}-locality table.")
            print("This table covers major cities only. The official list has 1,310")
            print("localities. Query the full list from the data.gov.il CKAN datastore:")
            print("  https://data.gov.il/api/3/action/datastore_search"
                  "?resource_id=5c78e9fa-c2e2-4771-93ff-7f400a12f7ba&q=<name>")


# Locality-type words. A kibbutz or moshav address has no street at all
# ("משק 12, מושב נהלל"); without these the parser turns the locality-type word
# plus the locality name into an invented street.
LOCALITY_WORDS = ("מושב", "קיבוץ", "קבוץ", "משק", "כפר", "שכונת", "יישוב", "ישוב")

# Street type words, stripped from the parsed street name.
STREET_WORDS = ("רחוב", "רח'", "רח", "שדרות", "שד'", "שד", "סמטת", "סמטה",
                "דרך", "כיכר", "ככר", "שביל", "מעלה")

# Granular components Israeli forms split out. Each is captured as its own field
# rather than being swallowed into the street name, which is what an earlier
# version did: "רוטשילד 42 דירה 5" parsed as street "רוטשילד דירה 5".
COMPONENT_WORDS = {
    "דירה": "apartment", "דירת": "apartment", "אפ": "apartment",
    "קומה": "floor", "קומת": "floor",
    "כניסה": "entrance", "כניסת": "entrance",
    "ת.ד": "po_box", "ת.ד.": "po_box", "תד": "po_box",
}
COMPONENT_LABELS = {
    "apartment": ("מספר דירה", "Apartment"),
    "floor": ("קומה", "Floor"),
    "entrance": ("כניסה", "Entrance"),
    "po_box": ("ת.ד.", "PO Box"),
}


def format_address(address: str) -> None:
    """Parse and format an Israeli address, Hebrew or Latin.

    Resolves the locality by trying trailing token windows, then pulls out the
    granular components Israeli forms ask for separately (apartment, floor,
    entrance, PO box) before deciding what is left is the street name.
    """
    cleaned = normalize_hebrew(address.replace(",", " "))
    parts = [p for p in cleaned.split() if p]

    city_key = None
    city_span = (len(parts), len(parts))
    for start in range(len(parts)):
        for end in range(len(parts), start, -1):
            key = resolve_city_key(" ".join(parts[start:end]))
            if key:
                city_key, city_span = key, (start, end)
                break
        if city_key:
            break

    rest = parts[:city_span[0]] + parts[city_span[1]:] if city_key else list(parts)

    # Pull out granular components first: a component keyword consumes the token
    # after it, so its value never reaches the street name.
    components = {}
    remaining = []
    i = 0
    while i < len(rest):
        tok = rest[i]
        field = COMPONENT_WORDS.get(tok.rstrip("."))
        if field and i + 1 < len(rest):
            components[field] = rest[i + 1]
            i += 2
            continue
        remaining.append(tok)
        i += 1

    # A locality-type word means there is no street. Everything after it that is
    # not a number is the locality name, not a street.
    locality_form = any(t in LOCALITY_WORDS for t in remaining)

    number = None
    street_parts = []
    for tok in remaining:
        if tok.isdigit() and number is None:
            number = tok
        elif tok in LOCALITY_WORDS:
            continue
        else:
            street_parts.append(tok)

    while street_parts and street_parts[0] in STREET_WORDS:
        street_parts.pop(0)

    street = "" if locality_form and not city_key else " ".join(street_parts)
    heb_city = LATIN_TO_HEBREW.get(city_key) if city_key else None

    print("Parsed Address Components:")
    if locality_form and not city_key:
        print(f"  Locality (no street): {' '.join(street_parts) or 'Not identified'}")
        print(f"  Plot / house number: {number or 'Not found'}")
    else:
        print(f"  Street: {street or 'Not identified'}")
        print(f"  Number: {number or 'Not found'}")
        print(f"  City: {heb_city or city_key or 'Not identified'}")

    for field in ("apartment", "floor", "entrance", "po_box"):
        if field in components:
            he, en = COMPONENT_LABELS[field]
            print(f"  {en} ({he}): {components[field]}")

    if city_key and city_key in CITY_CODES:
        info = CITY_CODES[city_key]
        print(f"  Settlement code (semel yishuv): {info['code']}")
        print(f"  Area Code: {info['area_code']} (orientation only, not verified)")

    print()
    if locality_form and not city_key:
        print("This looks like a kibbutz or moshav address, which has no street name.")
        print("Format it as '<plot number>, <locality>' or just the locality. Such a")
        print("locality usually carries ONE locality-wide mikud with no street-level")
        print("codes, so do not look for a street. Check the locality against:")
        print("  https://doar.israelpost.co.il/content/no-address")
        return

    if "po_box" in components and city_key and not street:
        heb = LATIN_TO_HEBREW.get(city_key) or city_key.title()
        print("Formatted address (PO box, no street needed):")
        print(f"  Hebrew: ת.ד. {components['po_box']}, {heb}")
        print(f"  For forms: POBox={components['po_box']}, City={heb}, "
              f"Semel={CITY_CODES[city_key]['code']}")
        print()
        print("  A PO box has its OWN mikud, different from the mikud of a street")
        print("  address in the same locality. Look it up with the ת.ד option on")
        print("  the Israel Post form, not the address option:")
        print("  https://doar.israelpost.co.il/locatezip")
        return

    if street and number and city_key:
        display_city = heb_city or city_key.title()
        extra = "".join(
            f", {COMPONENT_LABELS[f][0]} {components[f]}"
            for f in ("entrance", "apartment", "floor", "po_box") if f in components
        )
        print("Formatted address:")
        if heb_city:
            print(f"  Hebrew: {street} {number}{extra}, {heb_city}")
        print(f"  Latin: {street.title()} {number}, {city_key.title()}")
        print(f"  For forms: Street={street}, Number={number}, "
              f"City={display_city}, Semel={CITY_CODES[city_key]['code']}"
              + "".join(f", {COMPONENT_LABELS[f][1]}={components[f]}"
                        for f in ("apartment", "floor", "entrance", "po_box")
                        if f in components))
        print()
        print("  Postal code (mikud): not resolved by this script. There is no")
        print("  keyless public mikud-by-address API. Use the Israel Post form:")
        print("  https://doar.israelpost.co.il/locatezip")
        print()
        print("  If the form asks for your registered address (מען) rather than a")
        print("  delivery address, use the address on your teudat zehut appendix,")
        print("  which changes only by filing a change-of-address notice with the")
        print("  Interior Ministry. They are often not the same address.")
    else:
        missing = []
        if not street:
            missing.append("street name")
        if not number:
            missing.append("house number")
        if not city_key:
            missing.append("locality (not in this script's table)")
        print("Could not fully format. Missing: " + ", ".join(missing) + ".")
        if not city_key:
            print("This table covers major cities only. Query the full 1,310-locality")
            print("list from the data.gov.il CKAN datastore:")
            print("  https://data.gov.il/api/3/action/datastore_search"
                  "?resource_id=5c78e9fa-c2e2-4771-93ff-7f400a12f7ba&q=<name>")


def list_cities() -> None:
    """List all known cities with CBS codes."""
    unique = len({v["code"] for v in CITY_CODES.values()})
    print(f"Known Israeli localities ({unique}; {len(CITY_CODES)} keys including aliases):\n")
    print(f"{'City':<22} {'Semel':<8} {'Area':<6} {'Hebrew'}")
    print("-" * 70)
    for name, info in sorted(CITY_CODES.items(), key=lambda x: x[1]["code"]):
        heb = LATIN_TO_HEBREW.get(name, "")
        print(f"{name:<22} {info['code']:<8} {info['area_code']:<6} {heb}")


def main():
    parser = argparse.ArgumentParser(
        description="Israeli Address Lookup and Validation"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # City lookup
    city_parser = subparsers.add_parser("city", help="Look up city by name")
    city_parser.add_argument("name", help="City name")

    # Format address
    fmt_parser = subparsers.add_parser("format", help="Format an address")
    fmt_parser.add_argument("address", help="Address string to format")

    # List cities
    subparsers.add_parser("cities", help="List all known cities")

    args = parser.parse_args()

    if args.command == "city":
        lookup_city(args.name)
    elif args.command == "format":
        format_address(args.address)
    elif args.command == "cities":
        list_cities()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
