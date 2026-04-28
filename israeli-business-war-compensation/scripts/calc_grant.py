#!/usr/bin/env python3
"""Reference implementation of the wage-track and fixed-cost-track calculations.

This script computes the indirect-damage compensation grant under both the
nationwide track of the Shaagat HaAri (March 2026) framework and the parallel
Iron Swords (October 2023 onward) framework. It does NOT replace the official
Tax Authority filing portal at gov.il/he/service/compensation-indirect-damage.

Usage:
    python calc_grant.py --ref 280000 --claim 168000 --wages 70000 --employees 5 --fixed 28000

Output explains both tracks, identifies the higher one, and lists the gates passed.

Sources for every figure in this file are listed in evidence.json (sibling file
in the skill folder). Average wage 13,773 NIS, 75% wage formula, 25%/12.5%
thresholds, 12,000-400M NIS turnover band, and tier multipliers (7/11/15/22%)
all come from the Tax Authority's published Shaagat HaAri framework.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass


AVERAGE_WAGE_NIS = 13_773  # Shaagat HaAri 2026 framework: per-employee cap base
WAGE_FORMULA_RATE = 0.75
MIN_DECLINE_MONTHLY = 0.25
MIN_DECLINE_BIMONTHLY = 0.125
TURNOVER_FLOOR = 12_000
TURNOVER_CEILING = 400_000_000
SMALL_BUSINESS_THRESHOLD = 300_000  # routes to the small-business continuity track
AGGREGATE_CAP_OVER_300K = 600_000  # aggregate ceiling for businesses above 300k turnover

# Fixed-cost track tiered multipliers (decline tier -> multiplier on monthly fixed expenses)
FIXED_COST_TIERS: list[tuple[float, float, float]] = [
    (0.25, 0.40, 0.07),
    (0.40, 0.60, 0.11),
    (0.60, 0.80, 0.15),
    (0.80, 1.00, 0.22),
]


@dataclass
class GrantResult:
    decline_rate: float
    eligible: bool
    eligibility_reason: str
    wage_track_grant: float
    wage_track_per_emp_cap: float
    wage_track_raw: float
    fixed_cost_track_grant: float
    fixed_cost_tier_multiplier: float | None
    aggregate_cap_applied: bool
    recommended_track: str
    recommended_amount: float


def fixed_cost_multiplier(decline: float) -> float | None:
    """Return the multiplier for the decline tier, or None if below 25%."""
    for low, high, mult in FIXED_COST_TIERS:
        if low <= decline < high or (decline == 1.0 and high == 1.0):
            return mult
    return None


def calc_grant(
    ref_turnover: float,
    claim_turnover: float,
    wages_in_period: float,
    employees: int,
    monthly_fixed_expenses: float,
    reporting_period_months: int = 1,
    is_bimonthly_filer: bool = False,
) -> GrantResult:
    """Calculate the wage-track and fixed-cost-track grants.

    Returns the higher of the two as the recommended grant for the nationwide track.
    Does NOT compute the small-business continuity track (turnover <= 300,000 NIS)
    or the red-track §35 advance - those are separate forms with separate flows.
    """
    if ref_turnover <= 0:
        return GrantResult(0, False, "Reference turnover must be positive", 0, 0, 0, 0, None, False, "none", 0)

    decline = (ref_turnover - claim_turnover) / ref_turnover

    threshold = MIN_DECLINE_BIMONTHLY if is_bimonthly_filer else MIN_DECLINE_MONTHLY
    if decline < threshold:
        return GrantResult(
            decline_rate=decline,
            eligible=False,
            eligibility_reason=f"Decline {decline:.1%} below {threshold:.1%} threshold for {'bi-monthly' if is_bimonthly_filer else 'monthly'} filer",
            wage_track_grant=0,
            wage_track_per_emp_cap=0,
            wage_track_raw=0,
            fixed_cost_track_grant=0,
            fixed_cost_tier_multiplier=None,
            aggregate_cap_applied=False,
            recommended_track="none",
            recommended_amount=0,
        )

    annual_turnover_estimate = claim_turnover * 12 if reporting_period_months == 1 else claim_turnover * (12 / reporting_period_months)
    if annual_turnover_estimate < TURNOVER_FLOOR or annual_turnover_estimate > TURNOVER_CEILING:
        return GrantResult(
            decline_rate=decline,
            eligible=False,
            eligibility_reason=f"Annual turnover ~{annual_turnover_estimate:,.0f} NIS outside {TURNOVER_FLOOR:,}-{TURNOVER_CEILING:,} band",
            wage_track_grant=0,
            wage_track_per_emp_cap=0,
            wage_track_raw=0,
            fixed_cost_track_grant=0,
            fixed_cost_tier_multiplier=None,
            aggregate_cap_applied=False,
            recommended_track="none",
            recommended_amount=0,
        )

    raw_wage = WAGE_FORMULA_RATE * decline * wages_in_period
    per_emp_cap = AVERAGE_WAGE_NIS * employees * decline
    wage_grant = min(raw_wage, per_emp_cap)

    multiplier = fixed_cost_multiplier(decline)
    fixed_cost_grant = (multiplier or 0) * monthly_fixed_expenses * reporting_period_months

    aggregate_applied = False
    if ref_turnover > SMALL_BUSINESS_THRESHOLD:
        if wage_grant > AGGREGATE_CAP_OVER_300K:
            wage_grant = AGGREGATE_CAP_OVER_300K
            aggregate_applied = True
        if fixed_cost_grant > AGGREGATE_CAP_OVER_300K:
            fixed_cost_grant = AGGREGATE_CAP_OVER_300K
            aggregate_applied = True

    if wage_grant >= fixed_cost_grant:
        recommended_track = "wage"
        recommended_amount = wage_grant
    else:
        recommended_track = "fixed-cost"
        recommended_amount = fixed_cost_grant

    return GrantResult(
        decline_rate=decline,
        eligible=True,
        eligibility_reason="OK",
        wage_track_grant=wage_grant,
        wage_track_per_emp_cap=per_emp_cap,
        wage_track_raw=raw_wage,
        fixed_cost_track_grant=fixed_cost_grant,
        fixed_cost_tier_multiplier=multiplier,
        aggregate_cap_applied=aggregate_applied,
        recommended_track=recommended_track,
        recommended_amount=recommended_amount,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ref", type=float, required=True, help="Reference turnover (NIS) - typically March 2025 or March 2023 (north)")
    parser.add_argument("--claim", type=float, required=True, help="Claim turnover (NIS) - typically March 2026")
    parser.add_argument("--wages", type=float, default=0, help="Wages paid in claim period (NIS)")
    parser.add_argument("--employees", type=int, default=0, help="Number of employees")
    parser.add_argument("--fixed", type=float, default=0, help="Monthly fixed expenses (NIS)")
    parser.add_argument("--months", type=int, default=1, help="Reporting period months (default 1)")
    parser.add_argument("--bimonthly", action="store_true", help="Bi-monthly VAT filer (12.5%% threshold instead of 25%%)")
    parser.add_argument("--example", action="store_true", help="Run a worked example and exit")
    args = parser.parse_args()

    if args.example:
        print("Worked example: Tel Aviv café - see references/calculator-walkthrough.md Example 1\n")
        result = calc_grant(280_000, 168_000, 70_000, 5, 28_000)
        _print_result(result)
        return 0

    result = calc_grant(
        ref_turnover=args.ref,
        claim_turnover=args.claim,
        wages_in_period=args.wages,
        employees=args.employees,
        monthly_fixed_expenses=args.fixed,
        reporting_period_months=args.months,
        is_bimonthly_filer=args.bimonthly,
    )
    _print_result(result)
    return 0


def _print_result(result: GrantResult) -> None:
    print(f"Turnover decline:        {result.decline_rate:.1%}")
    print(f"Eligible:                {result.eligible} ({result.eligibility_reason})")
    if not result.eligible:
        return
    print()
    print("Wage track:")
    print(f"  Raw wage grant:        {result.wage_track_raw:,.0f} NIS  (= 0.75 × {result.decline_rate:.1%} × wages)")
    print(f"  Per-employee cap:      {result.wage_track_per_emp_cap:,.0f} NIS  (= 13,773 × employees × {result.decline_rate:.1%})")
    print(f"  Wage grant:            {result.wage_track_grant:,.0f} NIS  (min of the two)")
    print()
    print("Fixed-cost track:")
    if result.fixed_cost_tier_multiplier is None:
        print("  Below 25% decline; no multiplier applies")
    else:
        print(f"  Tier multiplier:       {result.fixed_cost_tier_multiplier:.0%}")
    print(f"  Fixed-cost grant:      {result.fixed_cost_track_grant:,.0f} NIS")
    print()
    if result.aggregate_cap_applied:
        print(f"NOTE: Aggregate 600,000 NIS ceiling applied (turnover > 300,000 NIS)")
        print()
    print(f"Recommended track:       {result.recommended_track.upper()}")
    print(f"Recommended grant:       {result.recommended_amount:,.0f} NIS")


if __name__ == "__main__":
    sys.exit(main())
