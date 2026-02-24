#!/usr/bin/env python3
"""
Israeli Purchase Tax (Mas Rechisha) Calculator

Calculate purchase tax for Israeli real estate transactions
based on 2025 tax brackets for first and non-first apartment buyers.

Usage:
    python calculate_mas_rechisha.py --price 2500000 --first
    python calculate_mas_rechisha.py --price 5000000
    python calculate_mas_rechisha.py --price 2500000 --first --json
"""

import argparse
import json
import sys

# 2025 Tax brackets (verify annually at Israel Tax Authority)
FIRST_APARTMENT_BRACKETS = [
    (1_978_745, 0.00),
    (2_347_040, 0.035),
    (6_055_070, 0.05),
    (20_183_565, 0.08),
    (float("inf"), 0.10),
]

NON_FIRST_APARTMENT_BRACKETS = [
    (6_055_070, 0.08),
    (20_183_565, 0.10),
    (float("inf"), 0.12),
]


def calculate_tax(price: float, is_first: bool) -> dict:
    """Calculate purchase tax with bracket breakdown."""
    brackets = FIRST_APARTMENT_BRACKETS if is_first else NON_FIRST_APARTMENT_BRACKETS

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

    return {
        "price": price,
        "buyer_type": "First apartment (dira yechida)" if is_first else "Non-first apartment (investment/additional)",
        "total_tax": total_tax,
        "effective_rate": effective_rate,
        "breakdown": breakdown,
        "note": "2025 brackets. Verify current rates at Israel Tax Authority.",
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
        print(f"  {b['from']:>12,.0f}  {to_str}  {b['rate']:>5.1%}  {b['taxable_amount']:>12,.0f}  {b['tax']:>10,.0f}")

    print("  " + "-" * 56)
    print(f"  {'TOTAL TAX':>34}  {'':>12}  {result['total_tax']:>10,.0f} NIS")
    print(f"  Effective rate: {result['effective_rate']:.2f}%")
    print()
    print(f"  Due within 50 days of signing the purchase agreement.")
    print(f"  {result['note']}")


def main():
    parser = argparse.ArgumentParser(
        description="Israeli Purchase Tax (Mas Rechisha) Calculator"
    )
    parser.add_argument("--price", type=float, required=True,
                        help="Property purchase price in NIS")
    parser.add_argument("--first", action="store_true",
                        help="First apartment buyer (dira yechida)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()

    if args.price <= 0:
        print("Error: Price must be positive.", file=sys.stderr)
        sys.exit(1)

    result = calculate_tax(args.price, args.first)
    print_result(result, args.json)


if __name__ == "__main__":
    main()
