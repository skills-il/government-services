#!/usr/bin/env python3
"""
Israeli Company Search Utility

Search for Israeli companies and compare business entity types.
Uses the Israel Corporations Authority (Rasham HaChevarot) web interface.

Usage:
    python search_company.py entity-types
    python search_company.py registration-steps
    python search_company.py compare
"""

import argparse
import json
import sys


ENTITY_TYPES = {
    "chevra_baam": {
        "name": "Chevra Baam (Ltd)",
        "hebrew": "chevra baam",
        "registry": "Rasham HaChevarot",
        "liability": "Limited to investment",
        "tax_rate": "Corporate ~23%",
        "registration_fee": "~2,559 NIS online / ~3,123 NIS paper (2026)",
        "annual_filing": "Financial statements required",
        "min_directors": 1,
        "best_for": "Companies, startups, growing businesses",
    },
    "chevra_tziburit": {
        "name": "Chevra Tziburit (Public)",
        "hebrew": "chevra tziburit",
        "registry": "Rasham HaChevarot + TASE",
        "liability": "Limited to investment",
        "tax_rate": "Corporate ~23%",
        "registration_fee": "Significant (listing fees)",
        "annual_filing": "Extensive public reporting",
        "min_directors": 2,
        "best_for": "Large companies seeking public capital",
    },
    "osek_morsheh": {
        "name": "Osek Morsheh (Licensed Dealer)",
        "hebrew": "osek morsheh",
        "registry": "Tax Authority",
        "liability": "Personal, unlimited",
        "tax_rate": "Personal brackets (10-47%)",
        "registration_fee": "Free",
        "annual_filing": "Tax returns only",
        "min_directors": "N/A",
        "best_for": "Freelancers, small businesses",
    },
    "osek_patur": {
        "name": "Osek Patur (Exempt Dealer)",
        "hebrew": "osek patur",
        "registry": "Tax Authority",
        "liability": "Personal, unlimited",
        "tax_rate": "Personal brackets (10-47%)",
        "registration_fee": "Free",
        "annual_filing": "Simplified tax returns",
        "min_directors": "N/A",
        "best_for": "Very small businesses (under ~120K NIS/year revenue)",
    },
    "amuta": {
        "name": "Amuta (Non-profit)",
        "hebrew": "amuta",
        "registry": "Rasham HaAmutot",
        "liability": "Limited",
        "tax_rate": "Exempt (with conditions)",
        "registration_fee": "~1,200 NIS",
        "annual_filing": "Annual report to Rasham",
        "min_directors": "2 board members",
        "best_for": "Non-profits, social organizations, charities",
    },
    "shutfut": {
        "name": "Shutfut Klalit (General Partnership)",
        "hebrew": "shutfut klalit",
        "registry": "Rasham HaShutfuyot",
        "liability": "Unlimited (all partners)",
        "tax_rate": "Personal brackets per partner",
        "registration_fee": "~1,200 NIS",
        "annual_filing": "Tax returns per partner",
        "min_directors": "N/A (partners manage)",
        "best_for": "Professional partnerships (law firms, accounting)",
    },
}


def show_entity_types() -> None:
    """Display all Israeli business entity types."""
    print("=== Israeli Business Entity Types ===\n")

    for key, info in ENTITY_TYPES.items():
        print(f"  {info['name']}")
        print(f"  Hebrew: {info['hebrew']}")
        print(f"  Registry: {info['registry']}")
        print(f"  Liability: {info['liability']}")
        print(f"  Tax rate: {info['tax_rate']}")
        print(f"  Registration fee: {info['registration_fee']}")
        print(f"  Best for: {info['best_for']}")
        print()


def show_comparison() -> None:
    """Compare entity types side by side."""
    print("=== Entity Type Comparison ===\n")

    headers = ["Feature", "Chevra Baam", "Osek Morsheh", "Amuta"]
    features = [
        ("Liability", "Limited", "Unlimited", "Limited"),
        ("Tax", "~23% corporate", "10-47% personal", "Exempt*"),
        ("Registration", "Rasham, 2,559/3,123 NIS (2026)", "Tax Authority, free", "Rasham (verify current fee)"),
        ("Annual filing", "Financial statements", "Tax returns only", "Report to Rasham"),
        ("Minimum officers", "1 director", "N/A", "2 board members"),
        ("Best for", "Startups, companies", "Freelancers", "Non-profits"),
    ]

    # Print header
    print(f"{'Feature':<20} {'Chevra Baam':<22} {'Osek Morsheh':<22} {'Amuta':<22}")
    print("-" * 86)

    for feature in features:
        print(f"{feature[0]:<20} {feature[1]:<22} {feature[2]:<22} {feature[3]:<22}")

    print()
    print("* Amuta tax exemption requires meeting specific conditions.")


def show_registration_steps() -> None:
    """Show registration steps for Chevra Baam (most common)."""
    print("=== Registration Steps: Chevra Baam (Ltd) ===\n")

    steps = [
        ("1. Name check", "Verify company name availability at Rasham HaChevarot"),
        ("2. Articles", "Draft Articles of Association (takanon)"),
        ("3. File documents", "Submit incorporation documents to Rasham"),
        ("4. Pay fee", "Pay registration fee (2,559 NIS online or 3,123 NIS paper, 2026; verify at ica.justice.gov.il)"),
        ("5. Certificate", "Receive Certificate of Incorporation (teuda le-hitaagdut)"),
        ("6. Tax registration", "Register with Tax Authority for income tax and VAT"),
        ("7. Bank account", "Open business bank account with incorporation certificate"),
        ("8. Bituach Leumi", "Register as employer with National Insurance (if hiring)"),
    ]

    for step, description in steps:
        print(f"  {step}")
        print(f"    {description}")
        print()

    print("Search companies at: https://ica.justice.gov.il/GenericCorporarionInfo/SearchCorporation")
    print("Company number format: 51-XXXXXXX (8-9 digits)")


def main():
    parser = argparse.ArgumentParser(
        description="Israeli Company Search and Entity Type Guide"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("entity-types", help="Show all entity types")
    subparsers.add_parser("compare", help="Compare entity types")
    subparsers.add_parser("registration-steps", help="Show registration steps")

    args = parser.parse_args()

    if args.command == "entity-types":
        show_entity_types()
    elif args.command == "compare":
        show_comparison()
    elif args.command == "registration-steps":
        show_registration_steps()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
