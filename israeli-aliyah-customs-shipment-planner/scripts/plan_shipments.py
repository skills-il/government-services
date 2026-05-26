#!/usr/bin/env python3
"""
plan_shipments.py - Plan the 3-shipment aliyah customs exemption.

Reads a JSON inventory, classifies each item against per-family caps,
proposes a 3-shipment split, and drafts a declaration per shipment.

Usage:
    python plan_shipments.py --inventory inventory.json \
        --aliyah-date 2026-06-01 \
        --family-size 4 \
        --home-area-sqm 80 \
        --home-tenure rent

Note on caps: sources disagree on the exact numeric duty-free caps for
computers and cell phones. Nefesh B'Nefesh reports 3 computers and 5 phones
per family; several customs brokers report only the first 2 computers clear
duty-free and the 3rd is taxed, and "5 phones" tracks a Ministry of
Communications import-approval threshold rather than a customs duty cap. This
script flags items at or above the conservative count as "verify" so the user
confirms with a licensed customs broker before packing.

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


# Per-family caps. "cap" = count at/below which the item is treated as within
# the family allowance; above it the item is over-limit. "verify_at" = count
# at/above which the item is flagged "verify with a customs broker" because
# sources disagree on whether it is genuinely duty-free.
# As of v1.2.0, Belong (https://belong.co.il/living/shipping-importation/) is
# treated as authoritative on 3 TVs / 3 computers / 1-of-each-appliance. The
# old over-hedging that flagged the 3rd computer as "verify" was removed.
# Set verify_at = cap + 1 (one above the cap) to disable the soft-verify flag.
# Note: air_conditioner cap=1 here is a placeholder; the real rule is per-room
# (1 AC per room, plus 1 for living area), so the assistant should pass an
# n_rooms hint or override this cap based on the family's home layout.
PER_FAMILY_CAPS = {
    "television": {"cap": 3, "verify_at": 4},
    "computer": {"cap": 3, "verify_at": 4},
    "cell_phone": {"cap": 5, "verify_at": 6},
    "refrigerator": {"cap": 1, "verify_at": 2},
    "oven": {"cap": 1, "verify_at": 2},
    "washing_machine": {"cap": 1, "verify_at": 2},
    "clothes_dryer": {"cap": 1, "verify_at": 2},
    "microwave": {"cap": 1, "verify_at": 2},
    "dishwasher": {"cap": 1, "verify_at": 2},
    "air_conditioner": {"cap": 1, "verify_at": 2},  # placeholder; real rule is per-room
    "other_appliance": {"cap": 1, "verify_at": 2},  # one of each type - user must split into distinct types
}

UNLIMITED_EXEMPT = {
    "furniture", "books", "clothing", "linens", "kitchen_utensils", "personal_effects",
}

NON_HOUSEHOLD = {"office_equipment", "commercial"}
SEPARATE_TRACK = {"vehicle"}
RESTRICTED = {"restricted"}


def carpet_allowance(home_area_sqm, home_tenure):
    """Return (allowed_sqm, description) for carpeting based on home tenure.

    NBN's published headline rule is "up to 25% of the area of the Oleh's home".
    Customs-broker practice often distinguishes between owners (claimed up to
    ~70% wall-to-wall) and renters (a flat ~30 sqm), but those finer numbers
    are NOT on the NBN page and should be confirmed with a licensed broker
    before relying on them. The script keeps the broker-practice split as a
    pragmatic planning aid and labels it as broker-practice in the description.
    """
    if home_tenure == "own":
        allowed = home_area_sqm * 0.70
        return allowed, (
            f"owner: up to ~70% of {home_area_sqm} sqm as wall-to-wall "
            f"({allowed:.1f} sqm), or up to 25% ({home_area_sqm * 0.25:.1f} sqm) as area rugs"
        )
    # default and "rent"
    return 30.0, "renter: flat ~30 sqm carpet allowance regardless of home size"


def classify(items, home_area_sqm, home_tenure):
    """Classify items against per-family caps. Returns a list of tagged items."""
    tagged = []
    allowed_carpet_sqm, carpet_desc = carpet_allowance(home_area_sqm, home_tenure)
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
            if count <= allowed_carpet_sqm:
                entry["flag"] = "exempt"
                entry["note"] = f"within carpet allowance ({carpet_desc})"
            else:
                over = count - allowed_carpet_sqm
                entry["flag"] = "over-limit"
                entry["note"] = f"{over:.1f} sqm over the carpet allowance ({carpet_desc})"
        elif category in PER_FAMILY_CAPS:
            cap = PER_FAMILY_CAPS[category]["cap"]
            verify_at = PER_FAMILY_CAPS[category]["verify_at"]
            if count > cap:
                entry["flag"] = "over-limit"
                entry["note"] = f"{count - cap} over the {cap} family cap"
            elif count >= verify_at:
                entry["flag"] = "verify"
                entry["note"] = (
                    f"{count} of reported {cap} family cap; sources disagree - "
                    f"confirm duty-free status with a licensed customs broker"
                )
            else:
                entry["flag"] = "exempt"
                entry["note"] = f"{count} of {cap} family cap"
        elif category in UNLIMITED_EXEMPT:
            entry["flag"] = "exempt"
            entry["note"] = "personal/household use, no numerical cap"
        elif category in NON_HOUSEHOLD:
            entry["flag"] = "non-household"
            entry["note"] = "not covered by aliyah exemption; clear as ordinary import"
        elif category in SEPARATE_TRACK:
            entry["flag"] = "vehicle"
            entry["note"] = "vehicle benefit is a separate track with its own 3-year window and 4-year resale restriction"
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
        if cat in {"clothing", "linens", "personal_effects"} or (cat == "computer" and item["count"] >= 1):
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
        verify = [i for i in items if i["flag"] == "verify"]
        total_value = sum(
            i["declared_value"] * i["count"] if i["category"] != "carpet_sqm" else i["declared_value"]
            for i in items
        )
        if over_limit:
            note = "Contains over-limit items; get a pre-clearance quote from a licensed customs broker (amil meches)."
        elif verify:
            note = "Contains items at a disputed cap; confirm duty-free status with a licensed customs broker (amil meches) before shipping."
        else:
            note = "All items within caps; self-clearance possible with teudat oleh and inventory list."
        declarations.append({
            "shipment": key,
            "status": "planned",
            "item_count": len(items),
            "exempt_count": len(exempt),
            "over_limit_count": len(over_limit),
            "verify_count": len(verify),
            "total_declared_value": total_value,
            "items": items,
            "note": note,
        })
    return declarations


def main():
    parser = argparse.ArgumentParser(description="Plan 3-shipment aliyah customs exemption")
    parser.add_argument("--inventory", type=Path, required=True, help="Path to inventory JSON")
    parser.add_argument("--aliyah-date", type=str, required=True, help="Aliyah date YYYY-MM-DD (teudat oleh issue date)")
    parser.add_argument("--family-size", type=int, default=1, help="Household size")
    parser.add_argument("--home-area-sqm", type=float, default=0.0, help="Planned home area in Israel (square meters)")
    parser.add_argument("--home-tenure", type=str, default="rent", choices=["own", "rent"],
                        help="Whether the oleh owns or rents the Israeli home (affects the carpet allowance)")
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

    tagged = classify(items, args.home_area_sqm, args.home_tenure)
    split = propose_split(tagged, aliyah_date)
    declarations = draft_declarations(split)

    over_limit = [i for i in tagged if i["flag"] == "over-limit"]
    verify = [i for i in tagged if i["flag"] == "verify"]
    result = {
        "input": {
            "family_size": args.family_size,
            "home_area_sqm": args.home_area_sqm,
            "home_tenure": args.home_tenure,
            "aliyah_date": args.aliyah_date,
            "status": args.status,
        },
        "deadline_iso": split["deadline_iso"],
        "classified_items": tagged,
        "over_limit_summary": over_limit,
        "verify_summary": verify,
        "declarations": declarations,
        "caps_note": "Numeric caps (computers, cell phones) are reported differently by different sources. Items flagged 'verify' sit at a disputed cap - confirm duty-free status with a licensed customs broker before shipping.",
        "retention_note": "All exempt items must remain in the oleh's household for 6 years from import (4-year resale restriction for vehicles from date of purchase) or depreciated tax is owed to Meches.",
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
