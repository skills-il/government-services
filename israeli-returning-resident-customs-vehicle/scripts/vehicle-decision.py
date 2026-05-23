#!/usr/bin/env python3
"""
Vehicle Decision Worksheet for Israeli Returning Residents

Produces a side-by-side comparison: ship the existing car from abroad vs. sell it
abroad and buy locally in Israel. Captures the key truth that returnees pay
FULL Israeli tax on a personally-imported vehicle (no purchase-tax exemption);
the only returnee benefit is the wider 48-month-from-manufacture age window.

This is a planning aid, NOT a binding tax calculation. The Israeli purchase-tax
rate varies by vehicle type (ICE, hybrid, electric), engine displacement, and
year. Always verify the exact rate with a licensed customs broker before
committing to shipment.

Usage:
    python3 vehicle-decision.py --car-value-usd 28000 --shipping-usd 3500 \\
        --car-age-months 30 --local-price-usd 50000

    python3 vehicle-decision.py --interactive
"""

import argparse
import sys
from datetime import datetime


# Total effective Israeli tax rate (customs duty + purchase tax + VAT combined)
# on personally-imported passenger vehicles, expressed as a percentage of CIF.
# Per gov.il personal_import_of_vehicles_guide chapter "חישוב המסים" (updated
# 15.01.2026): passenger cars from FTA-country origin clear at ~116% effective,
# from non-FTA origin ~131%. EVs ~75-87%. Collector cars ~103-117%. Hybrid
# rates depend on green-tax pollution grade.
#
# Use this combined-rate field; do NOT also stack VAT on top, because the
# gov.il table already includes VAT.
DEFAULT_TAX_RATE_LOW = 1.00   # conservative floor (combined rate), per gov.il personal_import_of_vehicles_guide chapter 3
DEFAULT_TAX_RATE_HIGH = 1.31  # 131% combined, non-FTA passenger ceiling
DEFAULT_TAX_RATE_MID = 1.16   # 116% combined, FTA-country passenger typical

# Israeli VAT rate, used ONLY for documentation / informational labelling.
# Israeli VAT was raised from 17% to 18% effective 2025-01-01 (per Knesset
# Arrangements Law for 2025). This script does NOT separately apply VAT on
# top of the combined tax rate above , the gov.il rates already include it.
VAT_RATE = 0.18  # 18% from 2025-01-01; reference only, do not double-count.

# Returnee age window: vehicle must be 48 months or younger from manufacture.
RETURNEE_AGE_CAP_MONTHS = 48
REGULAR_AGE_CAP_MONTHS = 24


def parse_args(argv):
    p = argparse.ArgumentParser(
        description="Ship-vs-sell vehicle decision worksheet for Israeli returnees",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--car-value-usd", type=float, help="Market value of the existing car abroad, in USD")
    p.add_argument("--shipping-usd", type=float, help="Estimated shipping + insurance + port handling, in USD")
    p.add_argument("--car-age-months", type=int, help="Vehicle age from manufacture, in months")
    p.add_argument(
        "--local-price-usd", type=float,
        help="Estimated price of an equivalent vehicle bought locally in Israel, in USD",
    )
    p.add_argument(
        "--broker-fees-usd", type=float, default=1200,
        help="Customs broker + Israeli registration + tests; default 1200 USD",
    )
    p.add_argument(
        "--tax-rate-low", type=float, default=DEFAULT_TAX_RATE_LOW,
        help=f"Low end of the Israeli purchase-tax rate band (default {DEFAULT_TAX_RATE_LOW})",
    )
    p.add_argument(
        "--tax-rate-high", type=float, default=DEFAULT_TAX_RATE_HIGH,
        help=f"High end of the Israeli purchase-tax rate band (default {DEFAULT_TAX_RATE_HIGH})",
    )
    p.add_argument(
        "--vehicle-class", choices=["ice", "hybrid", "ev"], default="ice",
        help="Vehicle class affects the tax rate band (ice / hybrid / ev). Default ice.",
    )
    p.add_argument(
        "--interactive", action="store_true",
        help="Prompt for inputs instead of reading from flags",
    )
    return p.parse_args(argv)


def prompt_float(label, default=None):
    suffix = f" [{default}]" if default is not None else ""
    raw = input(f"{label}{suffix}: ").strip()
    if not raw and default is not None:
        return float(default)
    return float(raw)


def prompt_int(label, default=None):
    suffix = f" [{default}]" if default is not None else ""
    raw = input(f"{label}{suffix}: ").strip()
    if not raw and default is not None:
        return int(default)
    return int(raw)


def interactive_inputs(args):
    print("Vehicle decision worksheet, interactive mode. Hit Enter to use the default if shown.")
    print()
    if args.car_value_usd is None:
        args.car_value_usd = prompt_float("Car market value abroad (USD)")
    if args.shipping_usd is None:
        args.shipping_usd = prompt_float("Estimated shipping + insurance + handling (USD)", 3500)
    if args.car_age_months is None:
        args.car_age_months = prompt_int("Vehicle age from manufacture (months)")
    if args.local_price_usd is None:
        args.local_price_usd = prompt_float("Equivalent vehicle price in Israel (USD)")
    return args


def adjust_tax_band(args):
    """Hybrids and EVs typically clear at a lower combined tax rate in Israel.

    Per gov.il personal_import_of_vehicles_guide (chapter 3): EVs ~75-87% all-in,
    hybrids depend on green-tax pollution grade. ICE passenger cars: ~116% from
    FTA-origin, ~131% from non-FTA-origin. Collector cars: ~103-117%.
    """
    if args.vehicle_class == "hybrid":
        return 0.85, 1.15
    if args.vehicle_class == "ev":
        return 0.75, 0.87
    return args.tax_rate_low, args.tax_rate_high


def compute_ship_cost(args, tax_rate):
    """Total landed cost if shipping the existing car.

    The tax_rate here is the COMBINED gov.il effective rate (customs + purchase
    tax + VAT), expressed as a fraction of CIF. We do NOT separately apply VAT,
    because the gov.il table already bakes VAT in.
    """
    cif = args.car_value_usd + args.shipping_usd  # cost + insurance + freight (rough)
    total_tax = cif * tax_rate
    return cif + total_tax + args.broker_fees_usd


def eligibility_check(args):
    issues = []
    if args.car_age_months > RETURNEE_AGE_CAP_MONTHS:
        issues.append(
            f"Vehicle is {args.car_age_months} months old. Returnee cap is {RETURNEE_AGE_CAP_MONTHS} months. "
            "Vehicle NOT eligible for personal import."
        )
    elif args.car_age_months > REGULAR_AGE_CAP_MONTHS:
        issues.append(
            f"Vehicle is {args.car_age_months} months old. Inside the 48-month returnee window "
            f"but outside the regular 24-month window, the returnee benefit IS the reason this car can come."
        )
    else:
        issues.append(
            f"Vehicle is {args.car_age_months} months old, under the regular 24-month window. "
            "Any Israeli resident could personally import it; the returnee benefit adds NO value here."
        )
    return issues


def print_worksheet(args):
    low_rate, high_rate = adjust_tax_band(args)
    mid_rate = (low_rate + high_rate) / 2

    ship_low = compute_ship_cost(args, low_rate)
    ship_mid = compute_ship_cost(args, mid_rate)
    ship_high = compute_ship_cost(args, high_rate)

    print()
    print("=" * 72)
    print("RETURNEE VEHICLE DECISION WORKSHEET")
    print(f"Generated {datetime.utcnow().date().isoformat()}, planning aid only")
    print("=" * 72)
    print()

    print(f"Vehicle class:       {args.vehicle_class.upper()}")
    print(f"Vehicle age:         {args.car_age_months} months from manufacture")
    print(f"Market value abroad: ${args.car_value_usd:,.0f}")
    print(f"Shipping + handling: ${args.shipping_usd:,.0f}")
    print(f"Broker + reg fees:   ${args.broker_fees_usd:,.0f}")
    print(f"Local Israel price:  ${args.local_price_usd:,.0f}")
    print()

    print("Eligibility check:")
    for line in eligibility_check(args):
        print(f"  - {line}")
    print()

    print(f"Israeli combined-tax planning band ({args.vehicle_class}): "
          f"{low_rate*100:.0f}% - {high_rate*100:.0f}% of CIF")
    print(f"  (this is customs + purchase tax + VAT, all baked in;")
    print(f"   Israeli VAT itself is {VAT_RATE*100:.0f}% as of 2025-01-01)")
    print()

    print("OPTION A: Ship the existing car")
    print(f"  Low estimate  (combined tax {low_rate*100:.0f}%): ${ship_low:,.0f}")
    print(f"  Mid estimate  (combined tax {mid_rate*100:.0f}%): ${ship_mid:,.0f}")
    print(f"  High estimate (combined tax {high_rate*100:.0f}%): ${ship_high:,.0f}")
    print()

    print("OPTION B: Sell abroad, buy locally in Israel")
    print(f"  Local price: ${args.local_price_usd:,.0f}")
    print(f"  Plus: lose resale value of existing car abroad (not modeled here)")
    print()

    delta_mid = ship_mid - args.local_price_usd
    print(f"DELTA (Option A mid - Option B): ${delta_mid:,.0f}")
    if delta_mid > 0:
        print(f"  Shipping costs ABOUT ${delta_mid:,.0f} MORE than buying locally (mid estimate).")
    else:
        print(f"  Shipping costs ABOUT ${-delta_mid:,.0f} LESS than buying locally (mid estimate).")
    print()

    print("REMEMBER:")
    print("  1. There is NO purchase-tax exemption for returnees on vehicles. The 48-month")
    print("     age window is the ONLY benefit.")
    print("  2. Numbers above are PLANNING ESTIMATES based on gov.il combined-rate tables")
    print("     (chapter 3 of personal_import_of_vehicles_guide). Actual rate depends on")
    print("     green-tax pollution grade, equipment level, and the takanot in force on")
    print("     clearance day. VERIFY with a licensed customs broker (סוכן מכס).")
    print("  3. Vehicle must clear customs within 9 months from your entry to Israel.")
    print("  4. After Misrad HaRishui registration you MAY claim an equipment-level tax")
    print("     refund at Meches with documentation; ask the broker.")
    print("  5. Misrad HaTachbura imposes a 12-month ownership-transfer restriction on")
    print("     personally-imported vehicles. Plan to keep the vehicle at least 12 months;")
    print("     a separate procedure (Nahal 416) exists for removing the restriction early.")
    print()
    print("=" * 72)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    if args.interactive:
        args = interactive_inputs(args)

    missing = []
    if args.car_value_usd is None: missing.append("--car-value-usd")
    if args.shipping_usd is None: missing.append("--shipping-usd")
    if args.car_age_months is None: missing.append("--car-age-months")
    if args.local_price_usd is None: missing.append("--local-price-usd")
    if missing:
        print(f"Missing required inputs: {', '.join(missing)}", file=sys.stderr)
        print("Re-run with --interactive or supply the flags. See --help.", file=sys.stderr)
        return 2

    print_worksheet(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
