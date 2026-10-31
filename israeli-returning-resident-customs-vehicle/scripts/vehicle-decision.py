#!/usr/bin/env python3
"""
Vehicle Decision Worksheet for Israeli Returning Residents

Produces a side-by-side comparison: ship the existing car from abroad vs. sell it
abroad and buy locally in Israel. Captures the key truth that returnees pay
FULL Israeli tax on a personally-imported vehicle (no purchase-tax exemption);
the only returnee benefit is the wider 48-month age window.

This is a planning aid, NOT a binding tax calculation. The customs value is set
by the assessor (declared value plus freight and insurance, or the price list if
the declared value is not accepted), and the final tax depends on the green
score and safety-equipment level fixed by Misrad HaTachbura. Always verify with
a licensed customs broker before committing to shipment.

Usage:
    python3 vehicle-decision.py --car-value-usd 28000 --shipping-usd 3500 \\
        --manufacture-date 2023-06-15 --local-price-usd 50000 --ils-per-usd 3.70 \\
        --gross-weight-kg 2100 --vehicle-class hybrid --green-score 120

    python3 vehicle-decision.py --interactive
"""

import argparse
import sys
from datetime import date, datetime, timezone


# 2026 tax parameters (Customs Book, chapter 87 additional Israeli rules, read
# 29.10.2026; ITA personal_import_of_vehicles_guide, updated 15.01.2026).
PURCHASE_TAX_PASSENGER = 0.83   # group א: passenger car up to 3,500 kg (ICE, hybrid, plug-in hybrid)
PURCHASE_TAX_EV = 0.48          # group ה'2: electric vehicle (Customs Book prints no effective date)
EV_BENEFIT_CAP_ILS = 22_000     # EV tax may not fall below the regular method minus 22,000 NIS (rule 4ב)
# Green reduction used inside the EV floor. The Customs Book rule 6 table (read
# 29.10.2026) gives 14,523 NIS for the cleanest grades; the ITA guide (updated
# 15.01.2026) prints a separate 19,498 NIS row for EV items. Not settled from the
# order itself, so the worksheet prints both; 14,523 is the higher-tax case.
EV_GREEN_REDUCTIONS_ILS = [("Customs Book table, 14,523 NIS reduction (higher tax)", 14_523),
                           ("ITA guide EV row, 19,498 NIS reduction", 19_498)]
MAX_GROSS_WEIGHT_KG = 3_500  # group א; heavier vehicles are group ב and outside this worksheet
VAT_RATE = 0.18                 # 18% from 2025-01-01, charged on value + duty + purchase tax
# Customs duty for a car that does NOT qualify under a free-trade agreement.
# Not quoted directly by the ITA guide; 7% is the rate implied by its own
# combined figures (1.07 x 1.83 x 1.18 = 2.31, i.e. "about 131%").
CUSTOMS_DUTY_NON_FTA = 0.07

# Green-score table (rule 6): (max score, NIS change). Negative = reduction.
GREEN_TABLE = [
    (50, -14_523), (130, -14_523), (150, -12_899), (170, -10_624),
    (175, -8_675), (180, -7_048), (185, -5_750), (190, -4_449),
    (195, -3_474), (200, -2_179), (205, -1_525), (210, -227),
    (220, 750), (250, 2_375), (300, 3_349), (350, 6_043),
]
GREEN_WORST_ILS = 8_690  # score 351 and above, also the fallback when no emissions data is supplied

# Age limits, measured at REGISTRATION in Israel (Takana 282, as quoted in
# Misrad HaTachbura procedure 02/12 s.9).
RETURNEE_AGE_CAP_MONTHS = 48
REGULAR_AGE_CAP_MONTHS = 24
# MoT will not accept an import-licence application with fewer than 45 days
# left before the last date the car can be registered.
APPLICATION_CUTOFF_DAYS = 45
DAYS_PER_MONTH = 365.25 / 12


def parse_args(argv):
    p = argparse.ArgumentParser(
        description="Ship-vs-sell vehicle decision worksheet for Israeli returnees",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "--car-value-usd", type=float,
        help="Value the customs assessor is expected to accept, in USD. NOT today's resale price: it starts "
             "from the bill-of-sale price; if the assessor rejects it, the Israeli price list less use "
             "depreciation. Ask a broker for the price-list figure. Also used as the car's value if sold abroad.",
    )
    p.add_argument("--shipping-usd", type=float, help="Shipping + transit insurance, in USD (added to the customs value)")
    p.add_argument("--manufacture-date", help="Manufacture date YYYY-MM-DD (COC field 0.11, DATA CARD, or the door-jamb label). Preferred over --car-age-months")
    p.add_argument("--car-age-months", type=float, help="Vehicle age from manufacture TODAY, in months; round UP part-months")
    p.add_argument(
        "--months-to-registration", type=float, default=3,
        help="Expected months from today until Israeli registration (shipping, clearance, "
             "inspection). Planning assumption, default 3; replace with your forwarder's estimate.",
    )
    p.add_argument(
        "--local-price-usd", type=float,
        help="Estimated price of an equivalent vehicle bought locally in Israel, in USD",
    )
    p.add_argument("--ils-per-usd", type=float, help="Exchange rate to use, NIS per USD (use the current Bank of Israel rate)")
    p.add_argument(
        "--broker-fees-usd", type=float, default=1200,
        help="Customs broker + licence fees + inspection + registration. Placeholder default 1200 USD; "
             "replace with real quotes",
    )
    p.add_argument(
        "--vehicle-class", choices=["ice", "hybrid", "phev", "ev"], default="ice",
        help="ice / hybrid / phev pay the passenger-car purchase tax less the green-score "
             "adjustment; ev (electric passenger car) pays the reduced EV rate subject to the 22,000 NIS cap. An electric pickup or goods vehicle (pass --goods-vehicle) is not covered. Default ice.",
    )
    p.add_argument(
        "--origin", choices=["fta", "other"], default="fta",
        help="fta = made in a free-trade-agreement country and shipped directly or via another "
             "party to the same agreement (no customs duty); other = customs duty applies. Default fta.",
    )
    p.add_argument(
        "--gross-weight-kg", type=float,
        help="Permitted total weight (GVWR) in kg, from the door-jamb label or COC. Required: only "
             "vehicles up to 3,500 kg (group א, including pickups at or under that weight) are covered",
    )
    p.add_argument("--motorcycle", action="store_true", help="The vehicle is a motorcycle (not covered by this worksheet)")
    p.add_argument("--goods-vehicle", action="store_true",
                   help="Pickup or other goods vehicle (customs item 87.04). Covered as ICE/hybrid up to 3,500 kg; "
                        "an ELECTRIC goods vehicle is taxed under a different group and floor and is not covered")
    p.add_argument("--green-score", type=int, help="Green score (ציון ירוק) from the import licence, if known")
    p.add_argument(
        "--no-emissions-data", action="store_true",
        help="US/Canada-spec car with no emissions letter from the Israeli importer, manufacturer or "
             "dealer: Misrad HaTachbura assigns the highest pollution grade",
    )
    p.add_argument("--interactive", action="store_true", help="Prompt for inputs instead of reading from flags")
    return p.parse_args(argv)


def prompt_float(label, default=None):
    suffix = f" [{default}]" if default is not None else ""
    raw = input(f"{label}{suffix}: ").strip()
    if not raw and default is not None:
        return float(default)
    return float(raw)


def interactive_inputs(args):
    print("Vehicle decision worksheet, interactive mode. Hit Enter to use the default if shown.")
    print()
    if args.car_value_usd is None:
        args.car_value_usd = prompt_float("Car market value abroad (USD)")
    if args.shipping_usd is None:
        args.shipping_usd = prompt_float("Shipping + transit insurance (USD)")
    if args.car_age_months is None and not args.manufacture_date:
        args.car_age_months = prompt_float("Vehicle age from manufacture today (months, round up)")
    if args.local_price_usd is None:
        args.local_price_usd = prompt_float("Equivalent vehicle price in Israel (USD)")
    if args.ils_per_usd is None:
        args.ils_per_usd = prompt_float("Exchange rate, NIS per USD")
    if args.gross_weight_kg is None:
        args.gross_weight_kg = prompt_float("Permitted total weight (GVWR), kg")
    return args


def green_change_ils(score):
    """NIS added to (positive) or removed from (negative) the purchase tax."""
    for max_score, change in GREEN_TABLE:
        if score <= max_score:
            return change
    return GREEN_WORST_ILS


def compute_tax_ils(value_ils, args, green_change, ev_green=None):
    """Return (duty, purchase_tax, vat) in NIS for one green-score assumption."""
    duty = value_ils * (CUSTOMS_DUTY_NON_FTA if args.origin == "other" else 0.0)
    base = value_ils + duty
    regular = max(0.0, base * PURCHASE_TAX_PASSENGER + green_change)
    if args.vehicle_class == "ev":
        # Rule 4ב: no lower than the regular method less the green reduction
        # and 22,000 NIS, and no higher than the regular method. Safety-equipment
        # reductions are ignored here, which overstates the floor slightly.
        regular_ev = max(0.0, base * PURCHASE_TAX_PASSENGER - ev_green)
        purchase_tax = min(max(base * PURCHASE_TAX_EV, regular_ev - EV_BENEFIT_CAP_ILS), regular_ev)
    else:
        purchase_tax = regular
    vat = (base + purchase_tax) * VAT_RATE
    return duty, purchase_tax, vat


def scenarios(args):
    """Green-score scenarios as (label, NIS change)."""
    if args.vehicle_class == "ev":
        return [(label, ("ev", red)) for label, red in EV_GREEN_REDUCTIONS_ILS]
    if args.no_emissions_data:
        return [("no emissions data, highest grade", GREEN_WORST_ILS)]
    if args.green_score is not None:
        return [(f"green score {args.green_score}", green_change_ils(args.green_score))]
    return [("cleanest grade", -14_523), ("most polluting grade", GREEN_WORST_ILS)]


def eligibility_check(args):
    """Return (eligible, list of messages)."""
    age_now = args.car_age_months
    at_reg = age_now + args.months_to_registration
    msgs = [f"Age today {age_now:.1f} months; expected age at Israeli registration "
            f"{at_reg:.1f} months (the limit is measured at registration, not at shipping)."]
    days_left = (RETURNEE_AGE_CAP_MONTHS - age_now) * DAYS_PER_MONTH
    if at_reg > RETURNEE_AGE_CAP_MONTHS:
        msgs.append(f"Over the {RETURNEE_AGE_CAP_MONTHS}-month returnee limit at registration. "
                    "This car CANNOT be registered as a personal import. Sell it abroad.")
        return False, msgs
    if days_left < APPLICATION_CUTOFF_DAYS:
        msgs.append(f"About {days_left:.0f} days remain until the car turns 48 months, the last date it can be "
                    "registered: Misrad HaTachbura does not accept an import-licence application with "
                    "under 45 days left. Treat as NOT importable.")
        return False, msgs
    if at_reg > REGULAR_AGE_CAP_MONTHS:
        msgs.append("Inside the 48-month returnee window but past the regular 24-month window: "
                    "the returnee benefit IS the reason this car can come.")
    else:
        msgs.append("Inside the regular 24-month window. Any Israeli resident could personally import "
                    "it; the returnee benefit adds NO value here.")
        if REGULAR_AGE_CAP_MONTHS - at_reg < 2:
            msgs.append("Close to 24 months at registration: if registration slips, only the returnee "
                        "window keeps it importable.")
    if RETURNEE_AGE_CAP_MONTHS - at_reg < 4:
        msgs.append("Tight timeline: a shipping or inspection delay of a few months pushes the car "
                    "over 48 months at registration. Get the import licence before the car sails.")
    if args.origin == "fta":
        msgs.append("Origin assumed FTA: built in a free-trade-agreement country and shipped directly. "
                    "If the car was built elsewhere (e.g. a car bought in the US but built in Japan), "
                    "re-run with --origin other.")
    return True, msgs


def print_worksheet(args):
    fx = args.ils_per_usd
    cif_usd = args.car_value_usd + args.shipping_usd
    value_ils = cif_usd * fx

    print()
    print("=" * 72)
    print("RETURNEE VEHICLE DECISION WORKSHEET")
    print(f"Generated {datetime.now(timezone.utc).date().isoformat()}, planning aid only")
    print("=" * 72)
    print()
    print(f"Vehicle class:        {args.vehicle_class.upper()}   Origin: {args.origin.upper()}")
    print(f"Market value abroad:  ${args.car_value_usd:,.0f}")
    print(f"Shipping + insurance: ${args.shipping_usd:,.0f}")
    print(f"Customs value (CIF):  ${cif_usd:,.0f} = {value_ils:,.0f} NIS at {fx:g} NIS/USD")
    print(f"Broker + reg fees:    ${args.broker_fees_usd:,.0f} (placeholder unless you entered quotes)")
    print(f"Local Israel price:   ${args.local_price_usd:,.0f}")
    print()

    eligible, msgs = eligibility_check(args)
    print("Eligibility check:")
    for line in msgs:
        print(f"  - {line}")
    print()
    if not eligible:
        print("No ship-vs-sell comparison: the car cannot be personally imported on this timeline.")
        print("=" * 72)
        return

    print("OPTION A: Ship the existing car")
    rows = []
    for label, change in scenarios(args):
        if isinstance(change, tuple):
            duty, pt, vat = compute_tax_ils(value_ils, args, 0, ev_green=change[1])
        else:
            duty, pt, vat = compute_tax_ils(value_ils, args, change)
        tax_ils = duty + pt + vat
        landed_usd = cif_usd + tax_ils / fx + args.broker_fees_usd
        rows.append((label, landed_usd))
        print(f"  [{label}] duty {duty:,.0f} + purchase tax {pt:,.0f} + VAT {vat:,.0f} "
              f"= {tax_ils:,.0f} NIS ({tax_ils / value_ils * 100:.0f}% of CIF)")
        print(f"      landed cost incl. the car itself: ${landed_usd:,.0f}")
    print()
    print("OPTION B: Sell abroad, buy locally in Israel")
    print(f"  Local price: ${args.local_price_usd:,.0f}")
    print("  (Option A already counts the car's own value, which is what selling it abroad")
    print("   would return, so the two totals compare directly.)")
    print()
    for label, landed in rows:
        delta = landed - args.local_price_usd
        word = "MORE" if delta > 0 else "LESS"
        print(f"DELTA [{label}]: shipping costs about ${abs(delta):,.0f} {word} than buying locally.")
    print()

    print("REMEMBER:")
    print("  1. There is NO purchase-tax exemption for returnees on vehicles. The 48-month")
    print("     age window (measured at Israeli registration) is the ONLY benefit.")
    if args.vehicle_class == "ev":
        print("  2. EVs: the 48% EV rate is capped, the tax cannot fall more than 22,000 NIS below")
        print("     the regular method, so pricier EVs pay more than the ~75% headline. The two rows")
        print("     differ only in which official green reduction enters that floor.")
    elif args.green_score is None and not args.no_emissions_data:
        print("  2. Pass --green-score (from the import licence) for a single figure. A US/Canada car")
        print("     with no emissions letter gets the highest pollution grade (--no-emissions-data).")
    else:
        print("  2. The green score is fixed by Misrad HaTachbura on the import licence.")
    print("  3. Not modeled: safety-equipment reductions (refunded after registration), the luxury")
    print("     surcharge above 300,000 NIS consumer price, and assessor revaluation of the CIF.")
    print("  4. Rates are those in force on payment day. VERIFY with a licensed customs broker.")
    print("  5. Misrad HaTachbura restricts ownership transfer for 12 months from Israeli")
    print("     registration; early removal needs an application under its published procedure.")
    print()
    print("=" * 72)


def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])
    if args.interactive:
        args = interactive_inputs(args)

    if args.manufacture_date:
        try:
            built = date.fromisoformat(args.manufacture_date)
        except ValueError:
            print("--manufacture-date must be YYYY-MM-DD.", file=sys.stderr)
            return 2
        args.car_age_months = (date.today() - built).days / DAYS_PER_MONTH

    missing = [flag for flag, val in (
        ("--car-value-usd", args.car_value_usd), ("--shipping-usd", args.shipping_usd),
        ("--car-age-months or --manufacture-date", args.car_age_months), ("--local-price-usd", args.local_price_usd),
        ("--ils-per-usd", args.ils_per_usd), ("--gross-weight-kg", args.gross_weight_kg),
    ) if val is None]
    if missing:
        print(f"Missing required inputs: {', '.join(missing)}", file=sys.stderr)
        print("Re-run with --interactive or supply the flags. See --help.", file=sys.stderr)
        return 2
    if args.ils_per_usd <= 0 or args.gross_weight_kg <= 0 or args.car_age_months < 0 or args.months_to_registration < 0:
        print("Exchange rate and weight must be positive; car age and months to registration non-negative.", file=sys.stderr)
        return 2

    if args.goods_vehicle and args.vehicle_class == "ev":
        print("NOT COVERED: an electric pickup or goods vehicle is taxed under a different purchase-tax "
              "group and floor than an electric passenger car. No figures printed; ask a licensed customs broker.")
        return 3
    if args.motorcycle or args.gross_weight_kg > MAX_GROSS_WEIGHT_KG:
        print("NOT COVERED: this worksheet only handles vehicles up to 3,500 kg permitted total weight "
              "(purchase-tax group א). Heavier vehicles (group ב) and motorcycles are taxed under other "
              "rules. No figures printed; ask a licensed customs broker.")
        return 3
    print_worksheet(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
