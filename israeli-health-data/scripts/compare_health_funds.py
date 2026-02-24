#!/usr/bin/env python3
"""
Israeli Health Fund Comparison Utility

Compare the four Israeli health funds (kupot cholim) across
services, supplementary insurance, and patient rights.

Usage:
    python compare_health_funds.py compare
    python compare_health_funds.py hospitals
    python compare_health_funds.py rights
    python compare_health_funds.py shaban
"""

import argparse
import sys


HEALTH_FUNDS = {
    "clalit": {
        "name": "Clalit Health Services",
        "hebrew": "clalit sherutei briut",
        "members": "~4.8M",
        "market_share": "~52%",
        "clinics": "~1,500",
        "own_hospitals": 14,
        "digital": "Good",
        "specialist_wait": "Moderate",
        "shaban_plans": ["Mushlam", "Platinum"],
        "strengths": "Largest, owns hospitals, widest clinic network",
    },
    "maccabi": {
        "name": "Maccabi Healthcare Services",
        "hebrew": "maccabi sherutei briut",
        "members": "~2.5M",
        "market_share": "~27%",
        "clinics": "~300",
        "own_hospitals": 0,
        "digital": "Excellent",
        "specialist_wait": "Short-moderate",
        "shaban_plans": ["Magen Zahav", "Sheli"],
        "strengths": "Best digital services, Assuta partnership",
    },
    "meuhedet": {
        "name": "Meuhedet Health Fund",
        "hebrew": "kupat cholim meuhedet",
        "members": "~1.3M",
        "market_share": "~14%",
        "clinics": "~250",
        "own_hospitals": 0,
        "digital": "Good",
        "specialist_wait": "Short",
        "shaban_plans": ["Adif", "Magen"],
        "strengths": "Fast specialist access, good supplementary plans",
    },
    "leumit": {
        "name": "Leumit Health Fund",
        "hebrew": "kupat cholim leumit",
        "members": "~0.7M",
        "market_share": "~7%",
        "clinics": "~200",
        "own_hospitals": 0,
        "digital": "Fair",
        "specialist_wait": "Short",
        "shaban_plans": ["Zahav", "Kesher"],
        "strengths": "Flexible, good for small communities",
    },
}

HOSPITALS = [
    {"name": "Sheba (Tel Hashomer)", "city": "Ramat Gan", "type": "Government", "beds": 1700},
    {"name": "Ichilov (Sourasky)", "city": "Tel Aviv", "type": "Municipal", "beds": 1100},
    {"name": "Soroka", "city": "Beer Sheva", "type": "Government", "beds": 1100},
    {"name": "Rambam", "city": "Haifa", "type": "Government", "beds": 1000},
    {"name": "Beilinson (Rabin)", "city": "Petah Tikva", "type": "Clalit", "beds": 900},
    {"name": "Hadassah Ein Kerem", "city": "Jerusalem", "type": "Non-profit", "beds": 800},
    {"name": "Meir", "city": "Kfar Saba", "type": "Clalit", "beds": 700},
    {"name": "Kaplan", "city": "Rehovot", "type": "Clalit", "beds": 700},
    {"name": "Wolfson", "city": "Holon", "type": "Government", "beds": 600},
    {"name": "Assuta", "city": "Tel Aviv/Ashdod", "type": "Private", "beds": 0},
]


def compare_funds() -> None:
    """Compare all four health funds."""
    print("=== Israeli Health Fund Comparison ===\n")

    print(f"{'Feature':<22} {'Clalit':<18} {'Maccabi':<18} {'Meuhedet':<18} {'Leumit':<18}")
    print("-" * 94)

    features = [
        ("Members", "members"),
        ("Market share", "market_share"),
        ("Clinics", "clinics"),
        ("Own hospitals", "own_hospitals"),
        ("Digital services", "digital"),
        ("Specialist wait", "specialist_wait"),
    ]

    for label, key in features:
        row = f"{label:<22}"
        for fund_key in ["clalit", "maccabi", "meuhedet", "leumit"]:
            val = str(HEALTH_FUNDS[fund_key][key])
            row += f" {val:<17}"
        print(row)

    print()
    print("Key strengths:")
    for fund_key, fund in HEALTH_FUNDS.items():
        print(f"  {fund['name']}: {fund['strengths']}")


def show_hospitals() -> None:
    """Display major Israeli hospitals."""
    print("=== Major Israeli Hospitals ===\n")

    print(f"{'Hospital':<28} {'City':<16} {'Type':<14} {'Beds'}")
    print("-" * 65)

    for h in HOSPITALS:
        beds = str(h["beds"]) if h["beds"] > 0 else "Varies"
        print(f"{h['name']:<28} {h['city']:<16} {h['type']:<14} {beds}")

    print()
    print("Quality indicators published quarterly by Ministry of Health.")
    print("Dashboard: health.gov.il")


def show_patient_rights() -> None:
    """Display patient rights under National Health Insurance Law."""
    print("=== Patient Rights (National Health Insurance Law, 1995) ===\n")

    rights = [
        ("1. Choice of health fund", "Can choose any of the four kupot cholim"),
        ("2. Health basket (sal briut)", "All listed medications and treatments must be provided"),
        ("3. Maximum wait times", "GP: same/next day, Specialist: up to 30 days"),
        ("4. Second opinion", "Right to seek a second medical opinion"),
        ("5. Medical records", "Right to access complete medical records"),
        ("6. Informed consent", "Full explanation before any procedure"),
        ("7. Privacy", "Medical information confidentiality"),
        ("8. Switching funds", "Can switch once per year (1-6 month waiting period)"),
        ("9. Complaint process", "Each fund has an ombudsman (netziv tlunot)"),
    ]

    for title, desc in rights:
        print(f"  {title}")
        print(f"    {desc}")
        print()


def show_shaban() -> None:
    """Display supplementary insurance comparison."""
    print("=== Supplementary Insurance (Shaban) Comparison ===\n")

    tiers = [
        ("Basic tier", "~30-50 NIS/month", "Reduced specialist copays, extended treatments"),
        ("Mid tier", "~80-120 NIS/month", "Private specialist access, shorter waits, fertility"),
        ("Premium tier", "~150-250 NIS/month", "Surgery abroad, experimental treatments, private rooms"),
    ]

    print("All four funds offer 2-3 tiers of supplementary insurance:\n")
    for tier, cost, coverage in tiers:
        print(f"  {tier} ({cost})")
        print(f"    Coverage: {coverage}")
        print()

    print("Plans by fund:")
    for fund_key, fund in HEALTH_FUNDS.items():
        plans = ", ".join(fund["shaban_plans"])
        print(f"  {fund['name']}: {plans}")


def main():
    parser = argparse.ArgumentParser(
        description="Israeli Health Fund Comparison Utility"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("compare", help="Compare health funds")
    subparsers.add_parser("hospitals", help="List major hospitals")
    subparsers.add_parser("rights", help="Patient rights")
    subparsers.add_parser("shaban", help="Supplementary insurance comparison")

    args = parser.parse_args()

    if args.command == "compare":
        compare_funds()
    elif args.command == "hospitals":
        show_hospitals()
    elif args.command == "rights":
        show_patient_rights()
    elif args.command == "shaban":
        show_shaban()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
