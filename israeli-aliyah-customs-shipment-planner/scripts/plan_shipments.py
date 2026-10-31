#!/usr/bin/env python3
"""
plan_shipments.py - Plan the 3-shipment aliyah customs exemption.

Reads a JSON inventory, classifies each item against per-family caps,
proposes a starting 3-shipment split, and drafts a declaration per shipment.

Usage:
    python plan_shipments.py --inventory inventory.json \
        --aliyah-date 2026-06-01 \
        --family-size 4 \
        --home-area-sqm 80 \
        --rooms 4

Sources for the caps (see evidence.json):
- Israel Tax Authority import-tax guide for new olim: up to 3 TVs and 3
  personal computers per family, one of each other electrical/electronic
  appliance and major furniture item, hand-held work tools up to USD 1,650,
  business machinery up to USD 36,000 FOB (including the tools) subject to the
  Director's approval and a bank guarantee, no exemption for permanently
  installed equipment.
- Nefesh B'Nefesh: up to 5 cell phones (more needs Ministry of Communications
  approval), carpeting up to 25% of the home area, air conditioners / fans /
  heaters relative to the number of rooms.

Inventory JSON shape:
    {
      "items": [
        {"name": "laptop", "category": "computer", "count": 2, "declared_value": 1000, "currency": "USD"},
        {"name": "sofa", "category": "furniture", "type": "sofa", "count": 1, "declared_value": 900},
        {"name": "rugs", "category": "carpet_sqm", "count": 18.5, "declared_value": 1200},
        ...
      ]
    }

Conventions:
- "count" is the number of units (square metres for carpet_sqm). It must be a
  positive number, and a whole number for every category except carpet_sqm.
- "declared_value" is PER UNIT; the line total is count x declared_value.
  For carpet_sqm it is the value of the whole line.
- Caps are per family, so rows of the same category are SUMMED before the cap
  is applied (other_appliance and furniture are summed per "type", falling
  back to "name": always fill "type" for those rows). Rows are filled in
  order: rows inside the cap stay exempt, the row that crosses it is
  over-limit for the excess.
- A row with "already_imported": true is something the family (e.g. a spouse)
  already released: it counts toward the family cap first and is left out of
  the shipment plan.
- A hand_tools or business_equipment row with no declared_value is "verify":
  those caps are defined by value.

Categories recognized by the classifier:
    television, computer, cell_phone, carpet_sqm, refrigerator, oven,
    washing_machine, clothes_dryer, microwave, dishwasher,
    air_conditioner, other_appliance, furniture, books, clothing,
    linens, kitchen_utensils, personal_effects, office_equipment,
    commercial, permanent_fixture, hand_tools, business_equipment,
    restricted, vehicle

A missing or unrecognised category is flagged "verify", never assumed exempt.

Exit codes:
    0 = plan generated
    1 = inventory invalid
    2 = user status not supported (returning resident / second-time oleh:
        2 shipments within 9 months)
"""

import argparse
import json
import math
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path


# Per-family caps. TV / computer / one-of-each come from the Tax Authority
# olim guide; the 5-phone count comes from NBN only.
PER_FAMILY_CAPS = {
    "television": 3,
    "computer": 3,
    "cell_phone": 5,
    "refrigerator": 1,
    "oven": 1,
    "washing_machine": 1,
    "clothes_dryer": 1,
    "microwave": 1,
    "dishwasher": 1,
    "other_appliance": 1,  # one of each TYPE
}
PER_TYPE = {"other_appliance", "furniture"}

HAND_TOOLS_CAP_USD = 1650
BUSINESS_EQUIPMENT_CAP_USD = 36000  # includes the hand tools
CARPET_SHARE_OF_HOME = 0.25  # NBN: up to 25% of the area of the oleh's home

UNLIMITED_EXEMPT = {"books", "clothing", "linens", "kitchen_utensils", "personal_effects"}
NON_HOUSEHOLD = {"office_equipment", "commercial", "permanent_fixture"}
SEPARATE_TRACK = {"vehicle"}
RESTRICTED = {"restricted"}
KNOWN = (set(PER_FAMILY_CAPS) | UNLIMITED_EXEMPT | NON_HOUSEHOLD | SEPARATE_TRACK
         | RESTRICTED | {"carpet_sqm", "air_conditioner", "furniture", "hand_tools", "business_equipment"})

OLIM_STATUSES = ["oleh_chadash", "ezrach_oleh", "katin_chozer", "permanent_resident"]
RETURNING_STATUSES = ["toshav_chozer", "second_time_oleh"]


class InventoryError(ValueError):
    pass


def add_years(d, years):
    """Calendar anniversary; 29 February rolls back to 28 February."""
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d.replace(year=d.year + years, day=28)


def _number(value, field, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        try:
            value = float(str(value).strip())
        except ValueError:
            raise InventoryError(f"item '{name}': {field} must be a number, got {value!r}")
    value = float(value)
    if not math.isfinite(value):
        raise InventoryError(f"item '{name}': {field} must be a finite number")
    return value


def normalise(items):
    """Validate rows and return clean dicts. Raises InventoryError."""
    clean = []
    for idx, item in enumerate(items, 1):
        if not isinstance(item, dict):
            raise InventoryError(f"row {idx} is not an object")
        name = str(item.get("name") or f"item {idx}")
        category = item.get("category")
        count = _number(item.get("count", 1), "count", name)
        if count <= 0:
            raise InventoryError(f"item '{name}': count must be positive, got {count:g}")
        if category != "carpet_sqm" and count != int(count):
            raise InventoryError(f"item '{name}': count must be a whole number, got {count:g}")
        raw_value = item.get("declared_value")
        value_given = raw_value not in (None, "")
        value = _number(raw_value, "declared_value", name) if value_given else 0.0
        if value < 0:
            raise InventoryError(f"item '{name}': declared_value cannot be negative")
        if not isinstance(item.get("already_imported", False), bool):
            raise InventoryError(f"item '{name}': already_imported must be JSON true or false")
        currency = str(item.get("currency") or "USD").upper()
        if category != "carpet_sqm":
            count = int(count)
        clean.append({
            "name": name,
            "category": category,
            "type": str(item.get("type") or name).strip().lower(),
            "count": count,
            "declared_value": value,
            "currency": currency,
            "value_given": value_given,
            "already_imported": item.get("already_imported", False) is True,
            "line_value": value if category == "carpet_sqm" else value * count,
        })
    return clean


def classify(items, home_area_sqm, rooms=None):
    """Classify normalised items against per-family caps."""
    groups = defaultdict(list)
    # Items a spouse already released count toward the family cap first.
    order = sorted(range(len(items)), key=lambda i: not items[i]["already_imported"])
    for i in order:
        item = items[i]
        cat = item["category"]
        if cat in PER_FAMILY_CAPS or cat in PER_TYPE or cat == "carpet_sqm":
            key = (cat, item["type"]) if cat in PER_TYPE else (cat,)
            groups[key].append(i)

    tools = [i for i in items if i["category"] == "hand_tools"]
    tools_non_usd = any(i["currency"] != "USD" for i in tools)
    tools_missing = any(not i["value_given"] for i in tools)
    tools_missing_names = ", ".join(f"'{i['name']}'" for i in tools if not i["value_given"])
    tools_usd = sum(i["line_value"] for i in tools if i["currency"] == "USD")
    biz = [i for i in items if i["category"] == "business_equipment"]
    biz_non_usd = any(i["currency"] != "USD" for i in biz)
    biz_missing = any(not i["value_given"] for i in biz)
    biz_usd = sum(i["line_value"] for i in biz if i["currency"] == "USD")

    tagged = [dict(i) for i in items]

    for key, idxs in groups.items():
        cat = key[0]
        total = sum(items[i]["count"] for i in idxs)
        spread = f" (family total {total:g} across {len(idxs)} rows)" if len(idxs) > 1 else ""
        for i in idxs:
            if items[i]["already_imported"]:
                tagged[i]["flag"] = "already-imported"
                tagged[i]["note"] = "already released by the family; counts toward the cap"
        if cat == "carpet_sqm" and (not home_area_sqm or home_area_sqm <= 0):
            for i in idxs:
                if items[i]["already_imported"]:
                    continue
                tagged[i]["flag"] = "verify"
                tagged[i]["note"] = "home area unknown; allowance is 25% of the home area (NBN). Pass --home-area-sqm"
            continue
        if cat == "furniture":
            for i in idxs:
                e = tagged[i]
                if items[i]["already_imported"]:
                    continue
                if total > 1:
                    e["flag"] = "verify"
                    e["note"] = (f"{total:g} x '{key[1]}'{spread}: one of each MAJOR furniture item (Tax Authority); "
                                 f"customs decides what counts as major and as a reasonable quantity")
                else:
                    e["flag"] = "exempt"
                    e["note"] = f"one '{key[1]}' (one of each major furniture item)"
            continue
        if cat == "carpet_sqm":
            cap = home_area_sqm * CARPET_SHARE_OF_HOME
            unit = " sqm"
            label = "carpet"
            tail = (f"; allowance 25% of {home_area_sqm:g} sqm = {cap:.2f} sqm (NBN); "
                    f"fitted wall-to-wall carpet may count as flooring, confirm with customs")
        else:
            cap = PER_FAMILY_CAPS[cat]
            unit = ""
            label = f"'{key[1]}'" if cat in PER_TYPE else cat
            tail = f"; family cap {cap}"
            if cat == "cell_phone" and total > 5:
                tail += "; more than 5 phones also needs Ministry of Communications approval (NBN)"
        used = 0.0
        for i in idxs:
            e = tagged[i]
            n = items[i]["count"]
            before, used = used, used + n
            if items[i]["already_imported"]:
                e["flag"] = "already-imported"
                e["note"] = f"{label}: already released by the family; counts toward the cap{spread}{tail}"
            elif used <= cap + 1e-9:
                e["flag"] = "exempt"
                e["note"] = f"{label}: within the cap{spread}{tail}"
            else:
                over = used - max(before, cap)
                e["flag"] = "over-limit"
                e["note"] = (f"{label}: {max(over, 0.01):.2f}{unit} of this row over the cap{spread}{tail}" if cat == "carpet_sqm"
                             else f"{label}: {over:g} of this row's {n:g} over the cap{spread}{tail}")

    for e in tagged:
        if "flag" in e:
            continue
        if e["already_imported"]:
            e["flag"] = "already-imported"
            e["note"] = "already released by the family; not part of this plan"
            continue
        cat = e["category"]
        if cat is None or cat not in KNOWN:
            e["flag"] = "verify"
            e["note"] = (f"unrecognised category {cat!r}; classify it before relying on the exemption"
                         if cat is not None else "no category given; classify it before relying on the exemption")
        elif cat == "air_conditioner":
            e["flag"] = "verify"
            e["note"] = (f"{e['count']} unit(s) for a {rooms}-room home; allowed relative to the number of rooms (NBN), customs decides"
                         if rooms else "allowed relative to the number of rooms (NBN); pass --rooms and confirm with customs")
        elif cat == "hand_tools":
            if tools_missing:
                e["flag"] = "verify"
                e["note"] = (f"this row has no declared value; the hand-tool cap is USD {HAND_TOOLS_CAP_USD:,} in total, add values"
                             if not e["value_given"] else
                             f"tools row(s) {tools_missing_names} have no declared value, so the USD {HAND_TOOLS_CAP_USD:,} total cannot be checked")
            elif tools_non_usd:
                e["flag"] = "verify"
                e["note"] = f"convert every tools row to USD: the cap is USD {HAND_TOOLS_CAP_USD:,} in total"
            elif tools_usd > HAND_TOOLS_CAP_USD:
                e["flag"] = "over-limit"
                e["note"] = (f"hand tools total USD {tools_usd:,.2f} is over the USD {HAND_TOOLS_CAP_USD:,} hand-tool cap; "
                             f"if setting up a business, ask customs whether they can be approved as business equipment "
                             f"(Director's approval, bank guarantee, USD {BUSINESS_EQUIPMENT_CAP_USD:,} FOB ceiling "
                             f"including up to USD {HAND_TOOLS_CAP_USD:,} of hand tools)")
            else:
                e["flag"] = "exempt"
                e["note"] = (f"hand tools total USD {tools_usd:,.2f} within the USD {HAND_TOOLS_CAP_USD:,} cap, "
                             f"if for professional use and of the hand-held type (customs officer decides)")
        elif cat == "business_equipment":
            combined = biz_usd + (0 if tools_non_usd else tools_usd)
            if biz_missing or tools_missing:
                e["flag"] = "verify"
                e["note"] = "a business-equipment or tools row has no declared value; add values (USD, FOB)"
            elif biz_non_usd or tools_non_usd:
                e["flag"] = "verify"
                e["note"] = f"convert to USD (FOB): ceiling is USD {BUSINESS_EQUIPMENT_CAP_USD:,} including hand tools"
            elif combined > BUSINESS_EQUIPMENT_CAP_USD:
                e["flag"] = "over-limit"
                e["note"] = (f"equipment plus hand tools USD {combined:,.2f} exceeds the USD {BUSINESS_EQUIPMENT_CAP_USD:,} FOB ceiling")
            else:
                e["flag"] = "verify"
                e["note"] = (f"equipment plus hand tools USD {combined:,.2f} within USD {BUSINESS_EQUIPMENT_CAP_USD:,} FOB, "
                             f"but needs the Director's approval and a bank guarantee, kept on the business premises")
        elif cat in UNLIMITED_EXEMPT:
            e["flag"] = "exempt"
            e["note"] = "personal/household use, no numerical cap"
        elif cat in NON_HOUSEHOLD:
            e["flag"] = "non-household"
            e["note"] = ("permanently installed equipment is not exempt" if cat == "permanent_fixture"
                         else "not covered by the household exemption; clear as an ordinary import")
        elif cat in SEPARATE_TRACK:
            e["flag"] = "vehicle"
            e["note"] = "separate vehicle benefit: own 3-year window and 4-year personal-use restriction"
        else:
            e["flag"] = "restricted"
            e["note"] = "needs a separate permit or licence (weapons/plants/pets/medication/drones)"
    return tagged


def propose_split(tagged, aliyah_date, shipments_used=0):
    """A starting split only; the user adjusts it to the real move."""
    shipment_1, shipment_2 = [], []
    for item in tagged:
        if item["flag"] in ("non-household", "vehicle", "restricted", "already-imported"):
            continue
        if item["category"] in {"clothing", "linens", "personal_effects"}:
            shipment_1.append(item)
        else:
            shipment_2.append(item)
    # Remaining slots after shipments already used: 3 -> [1, 2, reserve], 2 -> [1, 2], 1 -> [all]
    slots = {0: [shipment_1, shipment_2, []], 1: [shipment_1, shipment_2], 2: [shipment_1 + shipment_2]}[shipments_used]
    split = {f"shipment_{n}": items for n, items in enumerate(slots, shipments_used + 1)}
    split["deadline_iso"] = add_years(aliyah_date, 3).isoformat()
    return split


def draft_declarations(split):
    declarations = []
    for key in sorted(k for k in split if k.startswith("shipment_")):
        items = split[key]
        if not items:
            declarations.append({
                "shipment": key,
                "status": "reserved",
                "note": "No items planned; reserve for later use within the eligibility window.",
            })
            continue
        over_limit = [i for i in items if i["flag"] == "over-limit"]
        verify = [i for i in items if i["flag"] == "verify"]
        if over_limit:
            note = "Contains over-limit items; get a pre-clearance quote from a licensed customs broker (amil meches)."
        elif verify:
            note = "Contains items customs must decide on; confirm with the customs office or a licensed customs broker before shipping."
        else:
            note = "All items within caps; self-clearance possible in the oleh's name with an itemised list."
        values = defaultdict(float)
        for i in items:
            values[i["currency"]] += i["line_value"]
        declarations.append({
            "shipment": key,
            "status": "planned",
            "item_rows": len(items),
            "exempt_rows": sum(1 for i in items if i["flag"] == "exempt"),
            "over_limit_rows": len(over_limit),
            "verify_rows": len(verify),
            "total_declared_value_by_currency": dict(values),
            "items": items,
            "note": note,
        })
    return declarations


def deadline_note(status):
    abroad = ("" if status == "katin_chozer"
              else " 6+ consecutive months abroad do not count;")
    return ("3 years from the date oleh status was received. Regular IDF/national service does not count;"
            f"{abroad} studies begun within 18 months add 1 year from their end; extensions up to 6 years "
            "(Tax Authority). The split is a starting suggestion: adjust it to the real move.")


def main():
    parser = argparse.ArgumentParser(description="Plan 3-shipment aliyah customs exemption")
    parser.add_argument("--inventory", type=Path, required=True, help="Path to inventory JSON")
    parser.add_argument("--aliyah-date", type=str, required=True, help="Date oleh status was received, YYYY-MM-DD")
    parser.add_argument("--family-size", type=int, default=1, help="Household size (recorded; caps are per family)")
    parser.add_argument("--home-area-sqm", type=float, default=0.0, help="Home area in Israel, sqm (carpet allowance)")
    parser.add_argument("--rooms", type=int, default=None, help="Number of rooms in the Israeli home (AC/heater allowance)")
    parser.add_argument("--home-tenure", type=str, default="rent", choices=["own", "rent"],
                        help="Recorded only; the NBN carpet rule (25%% of home area) does not depend on tenure")
    parser.add_argument("--status", type=str, default="oleh_chadash", choices=OLIM_STATUSES + RETURNING_STATUSES)
    parser.add_argument("--shipments-used", type=int, default=0, choices=[0, 1, 2],
                        help="Exempt shipments the family (either spouse) already used")
    args = parser.parse_args()

    if args.status in RETURNING_STATUSES:
        print("ERROR: returning residents (including second-time olim) are a different customs track:", file=sys.stderr)
        print("household goods in 2 shipments only, within 9 months of returning, not extendable.", file=sys.stderr)
        print("This planner covers olim (oleh, ezrach oleh, katin chozer, permanent resident) only.", file=sys.stderr)
        print("See references/returning-residents.md.", file=sys.stderr)
        return 2

    if not math.isfinite(args.home_area_sqm) or args.home_area_sqm < 0:
        print("ERROR: --home-area-sqm must be a non-negative number", file=sys.stderr)
        return 1
    if args.rooms is not None and args.rooms < 1:
        print("ERROR: --rooms must be at least 1", file=sys.stderr)
        return 1
    if not args.inventory.exists():
        print(f"ERROR: Inventory file not found: {args.inventory}", file=sys.stderr)
        return 1
    try:
        data = json.loads(args.inventory.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        print('ERROR: inventory must be an object with an "items" list', file=sys.stderr)
        return 1
    if not data["items"]:
        print("ERROR: Inventory is empty.", file=sys.stderr)
        return 1
    try:
        aliyah_date = date.fromisoformat(args.aliyah_date)
    except ValueError:
        print(f"ERROR: Invalid aliyah date: {args.aliyah_date} (expected YYYY-MM-DD)", file=sys.stderr)
        return 1
    try:
        items = normalise(data["items"])
    except InventoryError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    tagged = classify(items, args.home_area_sqm, args.rooms)
    split = propose_split(tagged, aliyah_date, args.shipments_used)
    result = {
        "input": {
            "family_size": args.family_size,
            "home_area_sqm": args.home_area_sqm,
            "rooms": args.rooms,
            "home_tenure": args.home_tenure,
            "aliyah_date": args.aliyah_date,
            "status": args.status,
            "shipments_used": args.shipments_used,
        },
        "spouse_note": ("If a spouse already used shipments or capped items (TVs, computers, appliance types), "
                        "the remaining shipments and caps are lower: pass --shipments-used AND list the capped items "
                        "the spouse already brought as rows with \"already_imported\": true, so they count toward the "
                        "family cap (they are left out of the shipment plan). Then confirm with customs."),
        "deadline_iso": split["deadline_iso"],
        "deadline_note": deadline_note(args.status),
        "classified_items": [i for i in tagged if i["flag"] != "already-imported"],
        "counted_toward_caps_already_imported_by_spouse": [i for i in tagged if i["flag"] == "already-imported"],
        "over_limit_summary": [i for i in tagged if i["flag"] == "over-limit"],
        "verify_summary": [i for i in tagged if i["flag"] == "verify"],
        "declarations": draft_declarations(split),
        "retention_note": ("Exempt goods must be for the oleh's own use in Israel for at least 6 years from release or "
                           "purchase (vehicles: 4 years); passing them to others before then, even free or "
                           "temporarily, breaches the exemption."),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
