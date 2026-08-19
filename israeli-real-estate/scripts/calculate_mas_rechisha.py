#!/usr/bin/env python3
"""
Israeli Purchase Tax (Mas Rechisha) Calculator

Calculate purchase tax for Israeli real estate transactions
based on the 2026 tax brackets for all four documented tracks:
first apartment, non-first apartment, new immigrant (Regulation 12a)
and the Regulation 11 reduced track (disability, blindness, victims of
hostile action, families of soldiers who fell in action).

Usage:
    python calculate_mas_rechisha.py --price 2500000 --track first
    python calculate_mas_rechisha.py --price 5000000 --track additional
    python calculate_mas_rechisha.py --price 2500000 --track oleh
    python calculate_mas_rechisha.py --price 2400000 --track reduced-single
    python calculate_mas_rechisha.py --price 3000000 --track reduced-other
    python calculate_mas_rechisha.py --price 2500000 --track first --json
"""

import argparse
import json
import sys

# Single-home brackets, frozen 16.1.2025 to 15.1.2028 by the 2025 Arrangements
# Law and republished by ITA circular 1/2026. Always verify at the Israel Tax
# Authority:
# https://www.gov.il/he/service/real_eatate_taxsimulator
FIRST_APARTMENT_BRACKETS = [
    (1_978_745, 0.00),
    (2_347_040, 0.035),
    (6_055_070, 0.05),
    (20_183_565, 0.08),
    (float("inf"), 0.10),
]

# Non-first apartment has only 2 brackets in 2026
# (the older 12% ultra-high-value bracket was dropped).
# These rates are a temporary order under section 9(c1f) in force only
# through 31 December 2026. Re-verify before using them for a 2027 purchase.
NON_FIRST_APARTMENT_BRACKETS = [
    (6_055_070, 0.08),
    (float("inf"), 0.10),
]

# New immigrant (oleh) buying a single residential home, Purchase Tax
# Regulation 12a, reformed track in force from 15 August 2024.
OLEH_SINGLE_HOME_BRACKETS = [
    (1_978_745, 0.00),
    (6_055_070, 0.005),
    (20_183_565, 0.08),
]

# Regulation 12a relief is switched OFF above this value: the purchase is
# taxed under the ordinary ladder on the FULL price, with no 0% or 0.5% step.
# ITA circular 1/2026, footnote 1: "bedira sheshovyah meal schum zeh,
# hahakala shebetakana 12a lo tachul".
OLEH_RELIEF_CEILING = 20_183_565

# Regulation 11 reduced track: a person with a qualifying disability, a blind
# person, a victim of hostile action, or a family member of a soldier who fell
# in action. Granted to one person at most twice in a lifetime, on application
# to the Israel Tax Authority.
REDUCED_SINGLE_HOME_BRACKETS = [
    (1_978_745, 0.00),
    (float("inf"), 0.005),
]
REDUCED_FLAT_RATE = 0.005

# Above this value a Regulation 11 single home leaves the bracket track and
# pays 0.5% on the WHOLE value. This is a cliff, not a bracket edge.
REDUCED_SINGLE_HOME_CEILING = 2_500_000

TRACKS = ("first", "additional", "oleh", "reduced-single", "reduced-other")

TRACK_LABELS = {
    "first": "First apartment (dira yechida)",
    "additional": "Non-first apartment (investment/additional)",
    "oleh": "New immigrant, single home (Regulation 12a)",
    "reduced-single": "Reduced track, single home (Regulation 11)",
    "reduced-other": "Reduced track, other cases (Regulation 11)",
}


def _brackets_for(price: float, track: str):
    """Return (brackets, note) for the requested track at this price.

    Two tracks change shape with the price, and both changes are cliffs:
    Regulation 12a switches off entirely above 20,183,565, and a Regulation 11
    single home leaves the bracket table above 2,500,000.
    """
    if track == "first":
        return FIRST_APARTMENT_BRACKETS, ""
    if track == "additional":
        return NON_FIRST_APARTMENT_BRACKETS, (
            "8%/10% are a temporary order in force only through 31.12.2026."
        )
    if track == "oleh":
        if price > OLEH_RELIEF_CEILING:
            return FIRST_APARTMENT_BRACKETS, (
                f"Above {OLEH_RELIEF_CEILING:,.0f} NIS Regulation 12a does not apply "
                "at all: the ordinary single-home ladder is applied to the full price."
            )
        return OLEH_SINGLE_HOME_BRACKETS, (
            "Granted once only, from one year before aliyah to seven years after."
        )
    if track == "reduced-single":
        if price > REDUCED_SINGLE_HOME_CEILING:
            return [(float("inf"), REDUCED_FLAT_RATE)], (
                f"Above {REDUCED_SINGLE_HOME_CEILING:,.0f} NIS the reduced rate is "
                "0.5% of the whole value, from the first shekel."
            )
        return REDUCED_SINGLE_HOME_BRACKETS, (
            "Granted to one person at most twice in a lifetime, on application to the ITA."
        )
    if track == "reduced-other":
        return [(float("inf"), REDUCED_FLAT_RATE)], (
            "0.5% of the whole value. Granted at most twice in a lifetime."
        )
    raise ValueError(f"Unknown track: {track}")


def calculate_tax(price: float, track: str = "first") -> dict:
    """Calculate purchase tax with bracket breakdown."""
    brackets, track_note = _brackets_for(price, track)

    total_tax = 0.0
    breakdown = []
    remaining = price
    prev_limit = 0

    for limit, rate in brackets:
        if remaining <= 0:
            break

        bracket_amount = min(remaining, limit - prev_limit)
        bracket_tax = bracket_amount * rate

        if bracket_amount > 0:
            breakdown.append({
                "from": prev_limit,
                "to": min(price, limit),
                "rate": rate,
                "taxable_amount": bracket_amount,
                "tax": bracket_tax,
            })

        total_tax += bracket_tax
        remaining -= bracket_amount
        prev_limit = limit

    effective_rate = (total_tax / price * 100) if price > 0 else 0

    note = (
        "Amounts frozen 16.1.2025 to 15.1.2028 (ITA circular 1/2026). "
        "Verify current rates at the Israel Tax Authority."
    )
    if track_note:
        note = f"{track_note} {note}"

    return {
        "price": price,
        "track": track,
        "buyer_type": TRACK_LABELS[track],
        "total_tax": total_tax,
        "effective_rate": effective_rate,
        "breakdown": breakdown,
        "note": note,
    }


def print_result(result: dict, as_json: bool = False) -> None:
    """Display calculation results."""
    if as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print("=" * 60)
    print("  Israeli Purchase Tax (Mas Rechisha) Calculation")
    print("=" * 60)
    print()
    print(f"  Property price: {result['price']:>15,.0f} NIS")
    print(f"  Buyer type:     {result['buyer_type']}")
    print()
    print("  Bracket Breakdown:")
    print(f"  {'From':>12}  {'To':>12}  {'Rate':>6}  {'Taxable':>12}  {'Tax':>10}")
    print("  " + "-" * 56)

    for b in result["breakdown"]:
        to_str = f"{b['to']:>12,.0f}" if b['to'] < float("inf") else "       ..."
        rate_pct = f"{b['rate'] * 100:>4.1f}%"
        print(f"  {b['from']:>12,.0f}  {to_str}  {rate_pct:>6}  {b['taxable_amount']:>12,.0f}  {b['tax']:>10,.0f}")

    print("  " + "-" * 56)
    print(f"  {'TOTAL TAX':>34}  {'':>12}  {result['total_tax']:>10,.0f} NIS")
    print(f"  Effective rate: {result['effective_rate']:.2f}%")
    print()
    print(f"  File declaration within 30 days of signing; pay within 60 days.")
    print(f"  {result['note']}")


def main():
    parser = argparse.ArgumentParser(
        description="Israeli Purchase Tax (Mas Rechisha) Calculator"
    )
    parser.add_argument("--price", type=float, required=True,
                        help="Property purchase price in NIS")
    parser.add_argument("--track", choices=TRACKS, default=None,
                        help="Buyer track (default: first)")
    parser.add_argument("--first", action="store_true",
                        help="Deprecated alias for --track first")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()

    if args.price <= 0:
        print("Error: Price must be positive.", file=sys.stderr)
        sys.exit(1)

    track = args.track or ("first" if args.first else "first")
    result = calculate_tax(args.price, track)
    print_result(result, args.json)


if __name__ == "__main__":
    main()
