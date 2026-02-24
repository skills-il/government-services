#!/usr/bin/env python3
"""
Israeli Drug Database Lookup Utility

Look up drugs in the Israeli pharmaceutical registry, check health
basket coverage, and find generic alternatives.

Usage:
    python lookup_drug.py common-drugs
    python lookup_drug.py generics "Lipitor"
    python lookup_drug.py pregnancy-categories
    python lookup_drug.py prescription-types
"""

import argparse
import sys


COMMON_DRUGS = {
    "Acamol": {
        "generic": "Paracetamol (Acetaminophen)",
        "ingredient": "Paracetamol 500mg",
        "form": "Tablet",
        "prescription": "OTC",
        "basket": "Yes (minimal copay)",
        "generics_available": True,
        "category": "Pain relief / Antipyretic",
    },
    "Optalgin": {
        "generic": "Dipyrone (Metamizole)",
        "ingredient": "Dipyrone 500mg",
        "form": "Tablet",
        "prescription": "OTC",
        "basket": "Yes (minimal copay)",
        "generics_available": True,
        "category": "Pain relief / Antipyretic",
    },
    "Ibufen": {
        "generic": "Ibuprofen",
        "ingredient": "Ibuprofen 200-400mg",
        "form": "Tablet/Syrup",
        "prescription": "OTC (200mg), Rx (400mg+)",
        "basket": "Yes",
        "generics_available": True,
        "category": "NSAID / Pain relief",
    },
    "Lipitor": {
        "generic": "Atorvastatin",
        "ingredient": "Atorvastatin 10-80mg",
        "form": "Tablet",
        "prescription": "Prescription",
        "basket": "Yes",
        "generics_available": True,
        "category": "Cholesterol lowering (Statin)",
    },
    "Losec": {
        "generic": "Omeprazole",
        "ingredient": "Omeprazole 20mg",
        "form": "Capsule",
        "prescription": "Prescription",
        "basket": "Yes",
        "generics_available": True,
        "category": "Proton pump inhibitor (PPI)",
    },
    "Norvasc": {
        "generic": "Amlodipine",
        "ingredient": "Amlodipine 5-10mg",
        "form": "Tablet",
        "prescription": "Prescription",
        "basket": "Yes",
        "generics_available": True,
        "category": "Blood pressure (Calcium channel blocker)",
    },
    "Clexane": {
        "generic": "Enoxaparin",
        "ingredient": "Enoxaparin sodium",
        "form": "Injection",
        "prescription": "Prescription",
        "basket": "Yes",
        "generics_available": True,
        "category": "Anticoagulant (Blood thinner)",
    },
    "Glucophage": {
        "generic": "Metformin",
        "ingredient": "Metformin 500-1000mg",
        "form": "Tablet",
        "prescription": "Prescription",
        "basket": "Yes",
        "generics_available": True,
        "category": "Diabetes (Type 2)",
    },
}

PREGNANCY_CATEGORIES = {
    "A": "No risk demonstrated in human studies",
    "B": "No risk in animal studies, limited human data",
    "C": "Risk cannot be ruled out",
    "D": "Evidence of risk, may be used when benefit outweighs",
    "X": "Contraindicated in pregnancy",
}

PRESCRIPTION_TYPES = {
    "OTC (llo mircham)": "Available without prescription at pharmacies",
    "Prescription (mircham)": "Requires physician prescription",
    "Restricted (mircham meyuchad)": "Specialist prescription or hospital-only",
    "Narcotic (sam mefakach)": "Controlled substance, special prescription form",
}


def show_common_drugs() -> None:
    """Display common Israeli medications."""
    print("=== Common Israeli Medications ===\n")

    for name, info in COMMON_DRUGS.items():
        print(f"  {name} ({info['generic']})")
        print(f"    Active ingredient: {info['ingredient']}")
        print(f"    Form: {info['form']}")
        print(f"    Prescription: {info['prescription']}")
        print(f"    Health basket: {info['basket']}")
        print(f"    Generics available: {'Yes' if info['generics_available'] else 'No'}")
        print(f"    Category: {info['category']}")
        print()


def find_generics(brand_name: str) -> None:
    """Find generic alternatives for a brand-name drug."""
    print(f"=== Generic Alternatives for {brand_name} ===\n")

    drug = COMMON_DRUGS.get(brand_name)
    if not drug:
        # Try case-insensitive search
        for name, info in COMMON_DRUGS.items():
            if name.lower() == brand_name.lower():
                drug = info
                brand_name = name
                break

    if not drug:
        print(f"Drug '{brand_name}' not found in reference data.")
        print("Try searching by brand name (e.g., Acamol, Lipitor, Losec).")
        print("For full registry search, use the MoH drug database at data.health.gov.il")
        return

    print(f"Brand: {brand_name}")
    print(f"Generic name: {drug['generic']}")
    print(f"Active ingredient: {drug['ingredient']}")
    print()

    if drug["generics_available"]:
        print("Generic alternatives ARE available in Israel.")
        print("Generics typically cost 40-60% less than brand-name.")
        print()
        print("To switch to a generic:")
        print("  1. Discuss with your physician")
        print("  2. Physician prescribes by generic name")
        print("  3. Pharmacist dispenses available generic")
        print("  4. Health basket copay typically lower for generics")
    else:
        print("No generic alternatives currently available in Israel.")

    print()
    print("NOTE: Always consult physician before switching medications.")


def show_pregnancy_categories() -> None:
    """Display pregnancy risk categories."""
    print("=== Drug Pregnancy Risk Categories ===\n")

    for cat, desc in PREGNANCY_CATEGORIES.items():
        print(f"  Category {cat}: {desc}")

    print()
    print("IMPORTANT: Always consult physician about medication safety during pregnancy.")


def show_prescription_types() -> None:
    """Display Israeli prescription categories."""
    print("=== Israeli Prescription Categories ===\n")

    for ptype, desc in PRESCRIPTION_TYPES.items():
        print(f"  {ptype}")
        print(f"    {desc}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Israeli Drug Database Lookup"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("common-drugs", help="List common Israeli medications")

    gen_parser = subparsers.add_parser("generics", help="Find generic alternatives")
    gen_parser.add_argument("brand", help="Brand name to look up")

    subparsers.add_parser("pregnancy-categories", help="Pregnancy risk categories")
    subparsers.add_parser("prescription-types", help="Prescription types in Israel")

    args = parser.parse_args()

    if args.command == "common-drugs":
        show_common_drugs()
    elif args.command == "generics":
        find_generics(args.brand)
    elif args.command == "pregnancy-categories":
        show_pregnancy_categories()
    elif args.command == "prescription-types":
        show_prescription_types()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
