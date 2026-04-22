#!/usr/bin/env python3
"""
plan_shipments.py - Plan the 3-shipment aliyah customs exemption.

Reads a JSON inventory, classifies each item against per-family caps,
proposes a 3-shipment split, and drafts a declaration per shipment.

Usage:
    python plan_shipments.py --inventory inventory.json \
        --aliyah-date 2026-06-01 \
        --family-size 4 \
        --home-area-sqm 80

Inventory JSON shape:
    {
      "items": [
        {"name": "laptop", "category": "computer", "count": 2, "declared_value": 2000, "currency": "USD"},
        {"name": "TV 55 inch", "category": "television", "count": 3, "declared_value": 1500, "currency": "USD"},
        ...
      ]
    }

Categories recognized by the classifier:
    television, computer, cell_phone, carpet_sqm, refrigerator, oven,
    washing_machine, clothes_dryer, microwave, dishwasher,
    air_conditioner, other_appliance, furniture, books, clothing,
    linens, kitchen_utensils, personal_effects, office_equipment,
    commercial, restricted, vehicle

Exit codes:
    0 = plan generated
    1 = inventory invalid
    2 = user status not supported (e.g., toshav_chozer)
"""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path


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
    "air_conditioner": 1,
    "other_appliance": 1,  # one of each type - user must split into distinct types
}

UNLIMITED_EXEMPT = {
    "furniture", "books", "clothing", "linens", "kitchen_utensils", "personal_effects",
}

NON_HOUSEHOLD = {"office_equipment", "commercial"}
SEPARATE_TRACK = {"vehicle"}
RESTRICTED = {"restricted"}


def classify(items, home_area_sqm):
    """Classify items against per-family caps. Returns a list of tagged items."""
    tagged = []
    for item in items:
        name = item.get("name", "unnamed")
        category = item.get("category", "personal_effects")
        count = int(item.get("count", 1))
        value = item.get("declared_value", 0)
        currency = item.get("currency", "USD")

        entry = {
            "name": name,
            "category": category,
            "count": count,
            "declared_value": value,
            "currency": currency,
        }

        if category == "carpet_sqm":
            allowed_sqm = home_area_sqm * 0.25
            if count <= allowed_sqm:
                entry["flag"] = "exempt"
                entry["note"] = f"within 25% of {home_area_sqm} sqm home ({allowed_sqm:.1f} sqm allowed)"
            else:
                over = count - allowed_sqm
                entry["flag"] = "over-limit"
                entry["note"] = f"{over:.1f} sqm over the 25% carpet cap"
        elif category in PER_FAMILY_CAPS:
            cap = PER_FAMILY_CAPS[category]
            if count <= cap:
                entry["flag"] = "exempt"
                entry["note"] = f"{count} of {cap} family cap"
            else:
                entry["flag"] = "over-limit"
                entry["note"] = f"{count - cap} over the {cap} family cap"
        elif category in UNLIMITED_EXEMPT:
            entry["flag"] = "exempt"
            entry["note"] = "personal/household use, no numerical cap"
        elif category in NON_HOUSEHOLD:
            entry["flag"] = "non-household"
            entry["note"] = "not covered by aliyah exemption; clear as ordinary import"
        elif category in SEPARATE_TRACK:
            entry["flag"] = "vehicle"
            entry["note"] = "vehicle benefit is a separate track with its own 3-year window and 5-year retention"
        elif category in RESTRICTED:
            entry["flag"] = "restricted"
            entry["note"] = "needs separate permit (firearms/plants/medication/drones/food)"
        else:
            entry["flag"] = "exempt"
            entry["note"] = "assumed personal/household use"
        tagged.append(entry)
    return tagged


def propose_split(tagged, aliyah_date):
    """Propose a 3-shipment split. Heuristic only - user should adjust to their move."""
    shipment_1 = []
    shipment_2 = []
    shipment_3 = []

    for item in tagged:
        if item["flag"] in ("non-household", "vehicle", "restricted"):
            continue
        cat = item["category"]
        if cat in {"clothing", "linens", "personal_effects"} or cat == "computer" and item["count"] >= 1:
            # Essentials go in shipment 1 (by partial count)
            shipment_1.append(item)
        elif cat in {"furniture", "books", "kitchen_utensils"} or cat in PER_FAMILY_CAPS:
            shipment_2.append(item)
        else:
            shipment_2.append(item)

    # Leave shipment 3 as reserve unless shipment 2 is heavy with capped items
    appliance_count = sum(1 for i in shipment_2 if i["category"] in PER_FAMILY_CAPS)
    if appliance_count >= 5:
        # Move one capped item to shipment 3 as reserve demonstration
        for i, itm in enumerate(shipment_2):
            if itm["category"] in {"microwave", "dishwasher", "air_conditioner"}:
                shipment_3.append(shipment_2.pop(i))
                break

    deadline = aliyah_date + timedelta(days=3 * 365)
    return {
        "shipment_1": shipment_1,
        "shipment_2": shipment_2,
        "shipment_3": shipment_3,
        "deadline_iso": deadline.isoformat(),
    }


def draft_declarations(split):
    """Draft a declaration summary per shipment."""
    declarations = []
    for key in ("shipment_1", "shipment_2", "shipment_3"):
        items = split[key]
        if not items:
            declarations.append({
                "shipment": key,
                "status": "reserved",
                "note": "No items planned; reserve for later use within 3-year window.",
            })
            continue
        exempt = [i for i in items if i["flag"] == "exempt"]
        over_limit = [i for i in items if i["flag"] == "over-limit"]
        total_value = sum(
            i["declared_value"] * i["count"] if i["category"] != "carpet_sqm" else i["declared_value"]
            for i in items
        )
        declarations.append({
            "shipment": key,
            "status": "planned",
            "item_count": len(items),
            "exempt_count": len(exempt),
            "over_limit_count": len(over_limit),
            "total_declared_value": total_value,
            "items": items,
            "note": (
                "Contains over-limit items; get a pre-clearance quote from a licensed customs broker (amil meches)."
                if over_limit else "All items within caps; self-clearance possible with teudat oleh and inventory list."
            ),
        })
    return declarations


def main():
    parser = argparse.ArgumentParser(description="Plan 3-shipment aliyah customs exemption")
    parser.add_argument("--inventory", type=Path, required=True, help="Path to inventory JSON")
    parser.add_argument("--aliyah-date", type=str, required=True, help="Aliyah date YYYY-MM-DD (teudat oleh issue date)")
    parser.add_argument("--family-size", type=int, default=1, help="Household size")
    parser.add_argument("--home-area-sqm", type=float, default=0.0, help="Planned home area in Israel (square meters)")
    parser.add_argument("--status", type=str, default="oleh_chadash", choices=["oleh_chadash", "toshav_chozer"])
    args = parser.parse_args()

    if args.status == "toshav_chozer":
        print("ERROR: Toshav Chozer (returning resident) has limited customs benefits that differ from Oleh Chadash.", file=sys.stderr)
        print("This planner is for Oleh Chadash only.", file=sys.stderr)
        print("Route the user to Misrad HaKlita Returning Resident desk and see references/returning-residents.md.", file=sys.stderr)
        return 2

    if not args.inventory.exists():
        print(f"ERROR: Inventory file not found: {args.inventory}", file=sys.stderr)
        return 1

    try:
        data = json.loads(args.inventory.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        return 1

    items = data.get("items", [])
    if not items:
        print("ERROR: Inventory is empty.", file=sys.stderr)
        return 1

    try:
        aliyah_date = date.fromisoformat(args.aliyah_date)
    except ValueError:
        print(f"ERROR: Invalid aliyah date: {args.aliyah_date} (expected YYYY-MM-DD)", file=sys.stderr)
        return 1

    tagged = classify(items, args.home_area_sqm)
    split = propose_split(tagged, aliyah_date)
    declarations = draft_declarations(split)

    over_limit = [i for i in tagged if i["flag"] == "over-limit"]
    result = {
        "input": {
            "family_size": args.family_size,
            "home_area_sqm": args.home_area_sqm,
            "aliyah_date": args.aliyah_date,
            "status": args.status,
        },
        "deadline_iso": split["deadline_iso"],
        "classified_items": tagged,
        "over_limit_summary": over_limit,
        "declarations": declarations,
        "retention_note": "All exempt items must remain in the oleh's household for 6 years from import (5 years for vehicles) or depreciated tax is owed to Meches.",
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
