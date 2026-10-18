#!/usr/bin/env python3
"""Estimate the Pikadon and discharge grant for a recently-discharged Israeli soldier.

Rates indexed to August 2026 values from hachvana.mod.gov.il/GrantAndDeposit/DepositUpTo5.
THE RATES CHANGE MONTHLY WITH CPI. Always verify the personalized amount against the
official calculator before any user makes financial plans.

Usage:
  python pikadon-calculator.py --service-type lochem --months 32 --gender male
  python pikadon-calculator.py --service-type tomech-lechima --months 30 --gender male
  python pikadon-calculator.py --service-type acher --months 24 --gender female
  python pikadon-calculator.py --service-type sle --months 18 --gender female
"""

import argparse
import sys

# Monthly rates published by the MoD, updated August 2026.
# Source: hachvana.mod.gov.il/GrantAndDeposit/DepositUpTo5 (pikadon) and .../Grant (grant).
PIKADON_RATES = {
    "lochem": 1000.08,
    "tomech-lechima": 833.40,
    "acher": 666.72,
    "sle": 666.72,
    "ezrachi-beinayim": 500.10,   # מסלול אזרחי ביניים
    "ezrachi-mefutzal": 333.40,   # מסלול אזרחי מפוצל
}

GRANT_RATES = {
    "lochem": 691.53,
    "tomech-lechima": 575.86,
    "acher": 460.19,
    "sle": 460.19,
    "ezrachi-beinayim": 345.77,
    "ezrachi-mefutzal": 230.10,
}

# Basic training at the start of service is credited at a LOWER tier than the
# role actually served. The MoD states this explicitly: a combat soldier's first
# 4 training months count as combat support, and a combat-support soldier's
# first 2 training months count as "other". Ignoring this over-states the
# pikadon of every combat and combat-support soldier.
TRAINING_RECLASSIFICATION = {
    "lochem": (4, "tomech-lechima"),
    "tomech-lechima": (2, "acher"),
}

ACCRUAL_CAP = {"male": 32, "female": 24}

# A lochem or tomech lechima wounded during, or as a result of, training or
# operational activity who then moved to another role keeps the HIGHER rate for
# the whole service period. This script cannot detect that, so callers must pass
# the pre-injury service type for such a case; the printed note says so.
WOUNDED_KEEPS_HIGHER_RATE = True

NEKUDOT_ZIKUI_VALUE_PER_POINT_PER_MONTH_2026 = 242


def accrue(rates: dict, service_type: str, effective_months: int) -> tuple[float, list[str]]:
    """Sum an accrual over the service, applying the training reclassification."""
    breakdown: list[str] = []
    total = 0.0
    remaining = effective_months
    if service_type in TRAINING_RECLASSIFICATION:
        train_months, train_tier = TRAINING_RECLASSIFICATION[service_type]
        t = min(remaining, train_months)
        if t:
            total += t * rates[train_tier]
            breakdown.append(f"{t} training month(s) at the {train_tier} rate ({rates[train_tier]})")
            remaining -= t
    if remaining:
        total += remaining * rates[service_type]
        breakdown.append(f"{remaining} month(s) at the {service_type} rate ({rates[service_type]})")
    return round(total, 2), breakdown


def compute_pikadon(service_type: str, months: int, gender: str,
                    medical_discharge: bool = False,
                    total_service_months: int | None = None,
                    injury_discharge: bool = False) -> dict:
    if service_type not in PIKADON_RATES:
        raise ValueError(f"Unknown service-type {service_type!r}. Valid: {list(PIKADON_RATES)}")
    if gender not in ACCRUAL_CAP:
        raise ValueError(f"Unknown gender {gender!r}. Valid: male, female")
    if months < 0 or (total_service_months is not None and total_service_months < 0):
        raise ValueError("months must be non-negative")
    if injury_discharge and service_type in ("sle", "ezrachi-beinayim", "ezrachi-mefutzal"):
        raise ValueError("--injury-discharge applies to soldiers (s.10A(b) refers to the Head of IDF "
                         "Manpower); for national-civic service use --medical-discharge if relevant")

    # s.11(a) credits "every month of regular service", and SHLAT (unpaid service,
    # e.g. hesder yeshiva periods) counts too: it is trimmed only beyond the cap.
    # The hachvana grant page says the same. So the month count is the TOTAL
    # service, never paid months alone. The tier of SHLAT months is not published;
    # this script applies the served tier and the note says to confirm it.
    served = months if total_service_months is None else max(months, total_service_months)

    # Eligibility: 12 months, or fewer only on health grounds (pro-rata).
    # s.10A(b): a soldier the Head of Manpower determined was discharged for an
    # injury in training or operations is deemed to have completed the FULL
    # compulsory service for the Pikadon and grant. The obligated length is
    # approximated by the 32/24 cap; a man whose obligation was shorter should
    # confirm the figure in the personal area.
    eligible = served >= 12 or medical_discharge or injury_discharge

    # hachvana states the 32/24 cap next to every tier, civilian tracks included.
    cap = ACCRUAL_CAP[gender]
    # The s.10A(b) deeming applies "לעניין תקופת השירות כאמור בסעיפים 9(א) ו-10(א)"
    # only, so credit points below still use the months actually served.
    accrual_months = max(served, cap) if injury_discharge else served
    effective_months = min(accrual_months, cap) if eligible else 0
    rate = PIKADON_RATES[service_type]
    pikadon, pikadon_breakdown = accrue(PIKADON_RATES, service_type, effective_months)
    grant, grant_breakdown = accrue(GRANT_RATES, service_type, effective_months)

    # The tier of SHLAT months is unpublished. Give a low bound that prices the
    # SHLAT months inside the cap at the lowest ("acher") tier instead.
    shlat_in_cap = (max(0, min(served, cap) - min(months, cap))
                    if (total_service_months and eligible) else 0)
    low_pikadon = low_grant = None
    if shlat_in_cap and service_type not in ("acher", "sle", "ezrachi-beinayim", "ezrachi-mefutzal"):
        base_p, _ = accrue(PIKADON_RATES, service_type, effective_months - shlat_in_cap)
        base_g, _ = accrue(GRANT_RATES, service_type, effective_months - shlat_in_cap)
        low_pikadon = round(base_p + shlat_in_cap * PIKADON_RATES["acher"], 2)
        low_grant = round(base_g + shlat_in_cap * GRANT_RATES["acher"], 2)

    # Nekudot zikui thresholds differ by service population:
    #   Male IDF/MAGAV/Police/SHABAS: >=23 months => 2 points
    #   Female IDF/MAGAV/Police/SHABAS: >=22 months => 2 points
    #   National-civic service, all three civic tracks: >=24 months => 2 points
    # An early discharge on medical grounds is deemed to have completed 12.
    counted = served
    if (medical_discharge or injury_discharge) and counted < 12:
        counted = 12
    civic_track = service_type in ("sle", "ezrachi-beinayim", "ezrachi-mefutzal")
    if civic_track:
        points_per_year = 2 if counted >= 24 else (1 if counted >= 12 else 0)
    elif gender == "male":
        points_per_year = 2 if counted >= 23 else (1 if counted >= 12 else 0)
    else:
        points_per_year = 2 if counted >= 22 else (1 if counted >= 12 else 0)

    monthly_credit = NEKUDOT_ZIKUI_VALUE_PER_POINT_PER_MONTH_2026 * points_per_year
    total_36_months = monthly_credit * 36

    return {
        "service_type": service_type,
        "months_input": months,
        "months_counted": served,
        "months_effective": effective_months,
        "eligible": eligible,
        "cap_applied": eligible and served > cap,
        "rate_per_month_nis": rate,
        "pikadon_estimate_nis": pikadon,
        "pikadon_breakdown": pikadon_breakdown,
        "shlat_months_in_cap": shlat_in_cap,
        "pikadon_low_if_shlat_at_acher_nis": low_pikadon,
        "grant_low_if_shlat_at_acher_nis": low_grant,
        "grant_estimate_nis": grant,
        "grant_breakdown": grant_breakdown,
        "nekudot_zikui_points_per_year": points_per_year,
        "nekudot_zikui_monthly_credit_nis": monthly_credit,
        "nekudot_zikui_total_over_36_months_nis": total_36_months,
        "note": "MoD rates as published August 2026, with the training reclassification applied and statutorily non-counted periods assumed already excluded from the months entered. SHLAT months are priced at the served tier, which the MoD does not publish, so confirm them in the personal area. A soldier wounded in training or operational activity who moved to another role keeps the higher pre-injury rate for the whole service, so pass the pre-injury service type in that case. Verify on the hachvana.mod.gov.il official calculator before any financial decision.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--service-type", required=True, choices=list(PIKADON_RATES.keys()))
    parser.add_argument("--months", required=True, type=int,
                        help="Months of regular service (paid months if you also pass --total-service-months)")
    parser.add_argument("--gender", required=True, choices=["male", "female"])
    parser.add_argument("--medical-discharge", action="store_true",
                        help="Early discharge on health grounds: eligible under 12 months (Pikadon "
                             "and grant pro-rata on months served) and deemed to have completed 12 "
                             "months for the credit-point threshold")
    parser.add_argument("--injury-discharge", action="store_true",
                        help="Discharged for an injury in training or operations, as determined by "
                             "the Head of Manpower (s.10A(b)): deemed to have completed full "
                             "compulsory service for the Pikadon and grant (estimated at the 32/24 cap; "
                             "a man with a shorter obligation gets less). Soldiers only")
    parser.add_argument("--total-service-months", "--hesder-total-months", dest="total_service_months",
                        type=int, default=None,
                        help="Hesder/SHLAT: total service months from enlistment to discharge, "
                             "including unpaid service. SHLAT counts toward the Pikadon, the grant "
                             "and the credit-point threshold, capped at 32/24 (s.11(a))")
    args = parser.parse_args()

    try:
        result = compute_pikadon(args.service_type, args.months, args.gender,
                                 medical_discharge=args.medical_discharge,
                                 total_service_months=args.total_service_months,
                                 injury_discharge=args.injury_discharge)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    print("Pikadon and discharge-grant estimate (MoD rates, August 2026):")
    print(f"  Service type:                       {result['service_type']}")
    cap_note = f"cap {ACCRUAL_CAP[args.gender]} for {args.gender}"
    print(f"  Months counted / effective:         {result['months_counted']} / {result['months_effective']} ({cap_note})")
    if not result["eligible"]:
        print("  NOT ELIGIBLE: under 12 months without a medical discharge, so no Pikadon or grant")
    if result["cap_applied"]:
        print("  NOTE: Months exceeded the cap; service beyond it adds nothing")
    print(f"  Rate per month (served role):       {result['rate_per_month_nis']} NIS")
    print(f"  Pikadon estimate:                   {result['pikadon_estimate_nis']:,.2f} NIS")
    for line in result["pikadon_breakdown"]:
        print(f"      {line}")
    print(f"  Discharge grant estimate:           {result['grant_estimate_nis']:,.2f} NIS")
    for line in result["grant_breakdown"]:
        print(f"      {line}")
    if result["pikadon_low_if_shlat_at_acher_nis"] is not None:
        print(f"  SHLAT: {result['shlat_months_in_cap']} unpaid month(s) priced at the served tier above. The MoD does")
        print(f"  not publish their tier; at the 'acher' tier the figures would be")
        print(f"  Pikadon {result['pikadon_low_if_shlat_at_acher_nis']:,.2f} / grant {result['grant_low_if_shlat_at_acher_nis']:,.2f} NIS. Confirm in the personal area.")
    print()
    print("Nekudot zikui (Section 39a) over 36 months from month after discharge:")
    print(f"  Points per year:                    {result['nekudot_zikui_points_per_year']}")
    print(f"  Monthly tax credit:                 {result['nekudot_zikui_monthly_credit_nis']} NIS")
    print(f"  Total over 36 months:               {result['nekudot_zikui_total_over_36_months_nis']:,} NIS")
    print()
    print("NOTE:", result["note"])
    print()
    print("REMINDER:")
    print("  - Published rates are revised periodically. Verify on the official calculator")
    print("    at https://www.hachvana.mod.gov.il/GrantAndDeposit/DepositUpTo5/Pages/default.aspx")
    print("  - Forward nekudot zikui reduce tax owed and cannot go below zero; Tofes 135 refunds real over-withholding.")
    print("  - Submit Tofes 101 to employer + Teudat Shichrur to start receiving the credit.")
    print("  - If employer never applied: file Tofes 135 retroactive (up to 6 years back).")


if __name__ == "__main__":
    main()
