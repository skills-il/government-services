#!/usr/bin/env python3
"""
Israeli Land Tenders Information Utility

Reference utility for Israeli Land Authority (RMI) tender types,
bid process guidance, and Hebrew terminology.

Usage:
    python search_tenders.py tender-types
    python search_tenders.py bid-guide
    python search_tenders.py terminology
    python search_tenders.py land-use
"""

import argparse
import sys


TENDER_TYPES = {
    "michraz": {
        "name": "Public Tender (Michraz)",
        "hebrew": "michraz",
        "description": "Open competitive bidding, typically highest price wins",
        "deposit": "Usually 10-15% of minimum price",
        "best_for": "Large residential and commercial projects",
        "process": "Sealed bids, public opening",
    },
    "hagralah": {
        "name": "Lottery (Hagralah)",
        "hebrew": "hagrala",
        "description": "Random selection among eligible applicants, fixed price",
        "deposit": "Small registration fee",
        "best_for": "Affordable housing (mechir lamishtaken)",
        "process": "Register, verify eligibility, random drawing",
    },
    "mechir_larocheish": {
        "name": "Price Buyer (Mechir Larocheish)",
        "hebrew": "mechir larocheish",
        "description": "Fixed price, allocated based on eligibility order",
        "deposit": "Varies",
        "best_for": "Specific populations (soldiers, immigrants)",
        "process": "Apply, verify eligibility, allocation by priority",
    },
    "haktzaah": {
        "name": "Direct Allocation (Haktzaah Yeshira)",
        "hebrew": "haktzaah yeshira",
        "description": "No competitive process, direct to qualifying entities",
        "deposit": "N/A",
        "best_for": "Public institutions, government bodies",
        "process": "Application with government approval",
    },
}

LAND_USE_CATEGORIES = {
    "megurim": {"english": "Residential", "description": "Housing development"},
    "miskhari": {"english": "Commercial", "description": "Office, retail, mixed-use"},
    "taasiyati": {"english": "Industrial", "description": "Factories, logistics"},
    "chaklai": {"english": "Agricultural", "description": "Farming, orchards"},
    "tayarut": {"english": "Tourism", "description": "Hotels, resorts"},
    "tzibburi": {"english": "Public", "description": "Schools, parks, government"},
    "taasuka": {"english": "Employment", "description": "Employment zones, high-tech parks"},
}

TERMINOLOGY = {
    "michraz": ("Tender", "michraz"),
    "magia hatzaa": ("Bidder", "magia hatzaa"),
    "hatzaah": ("Bid/Proposal", "hatzaa"),
    "mechir minimum": ("Minimum price", "mechir minimum"),
    "arbon": ("Deposit", "arbon / pikdon"),
    "heskem pituach": ("Development agreement", "heskem pituach"),
    "tnaei pituach": ("Development conditions", "tnaei pituach"),
    "heter bniyah": ("Building permit", "heter bniya"),
    "moed siyum": ("Completion deadline", "moed siyum"),
    "archa": ("Extension", "archa"),
    "chilut": ("Forfeiture", "chilut"),
    "hashagah": ("Objection", "hashaga"),
    "zocheh": ("Winner", "zocheh"),
    "zchuyot bniyah": ("Building rights", "zchuyot bniya"),
    "shetach": ("Plot area", "shetach"),
    "komot": ("Floors/Stories", "komot"),
    "gova": ("Height", "gova"),
    "shimush": ("Permitted use", "shimush"),
    "taba": ("Zoning plan", "taba"),
}


def show_tender_types() -> None:
    """Display all tender types."""
    print("=== Israeli Land Authority Tender Types ===\n")

    for key, info in TENDER_TYPES.items():
        print(f"  {info['name']} ({info['hebrew']})")
        print(f"    Description: {info['description']}")
        print(f"    Deposit: {info['deposit']}")
        print(f"    Best for: {info['best_for']}")
        print(f"    Process: {info['process']}")
        print()


def show_bid_guide() -> None:
    """Display bid submission guide."""
    print("=== Bid Submission Guide (Public Tenders) ===\n")

    steps = [
        ("1. Review tender documents",
         "Download chovert michraz from RMI website. Read ALL conditions."),
        ("2. Assess financial capacity",
         "Minimum price + deposit (10-15%) + development costs + fees."),
        ("3. Prepare documents",
         "Company registration, financial statements, signed conditions, bid form."),
        ("4. Determine bid price",
         "Research comparable tenders. Winning bids often 10-50%+ above minimum."),
        ("5. Submit before deadline",
         "Physical submission, sealed envelope. Late = disqualified."),
        ("6. Post-submission",
         "Public opening, results on RMI website, sign development agreement."),
    ]

    for title, desc in steps:
        print(f"  {title}")
        print(f"    {desc}")
        print()

    print("Key calculation:")
    print("  Value = Building Rights (sq.m.) x Price/sq.m. (market) - Development Costs")
    print()
    print("RECOMMENDATION: Consult a real estate attorney and appraiser before bidding.")


def show_terminology() -> None:
    """Display Hebrew tender terminology."""
    print("=== Hebrew Tender Terminology ===\n")

    print(f"{'English':<25} {'Hebrew':<25} {'Transliteration'}")
    print("-" * 70)

    for hebrew, (english, translit) in TERMINOLOGY.items():
        print(f"{english:<25} {hebrew:<25} {translit}")


def show_land_use() -> None:
    """Display land use categories."""
    print("=== Land Use Categories ===\n")

    print(f"{'Hebrew':<15} {'English':<15} {'Description'}")
    print("-" * 50)

    for hebrew, info in LAND_USE_CATEGORIES.items():
        print(f"{hebrew:<15} {info['english']:<15} {info['description']}")


def main():
    parser = argparse.ArgumentParser(
        description="Israeli Land Tenders Information Utility"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("tender-types", help="Show tender types")
    subparsers.add_parser("bid-guide", help="Bid submission guide")
    subparsers.add_parser("terminology", help="Hebrew terminology")
    subparsers.add_parser("land-use", help="Land use categories")

    args = parser.parse_args()

    if args.command == "tender-types":
        show_tender_types()
    elif args.command == "bid-guide":
        show_bid_guide()
    elif args.command == "terminology":
        show_terminology()
    elif args.command == "land-use":
        show_land_use()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
