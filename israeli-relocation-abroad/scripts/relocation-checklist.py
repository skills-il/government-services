#!/usr/bin/env python3
"""Generate a phased Israeli relocation abroad checklist.

Produces a before/during/return checklist based on the user's situation.
This is a guidance tool only, not legal or tax advice. Always recommend
a qualified accountant and lawyer for the final decisions.

Usage:
    python relocation-checklist.py --stage pre_move --destination usa \\
        --duration 4y --owns_apartment yes --family family
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field


TREATY_COUNTRIES = {
    "usa", "uk", "germany", "france", "netherlands", "belgium", "sweden",
    "denmark", "finland", "norway", "switzerland", "austria", "italy",
    "czech", "slovakia", "bulgaria", "romania", "canada", "uruguay",
}


@dataclass
class Plan:
    pre_move: list[str] = field(default_factory=list)
    first_90_days: list[str] = field(default_factory=list)
    ongoing: list[str] = field(default_factory=list)
    return_prep: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def build_plan(args: argparse.Namespace) -> Plan:
    plan = Plan()
    destination = args.destination.lower()
    is_treaty = destination in TREATY_COUNTRIES

    # Pre-move items, relevant for stage pre_move and useful context otherwise
    plan.pre_move.extend([
        "Decide tax residency strategy with an accountant (stay resident or nituk toshavut)",
        "If staying resident: open standing order to Bituach Leumi for minimum health insurance",
        "If cutting residency: prepare Form 1348 for next tax return and gather evidence of center-of-life abroad",
        "Freeze pension fund and keren hishtalmut in writing (do not withdraw)",
        "Notify Israeli bank of the move, ask about FATCA/CRS tagging",
        "Apostille marriage certificate, birth certificates, and relevant diplomas at the Foreign Ministry",
        "Apply for International Driving Permit at MEMSI",
        "Sign Tofes 161 with current Israeli employer (choose ritza for tax deferral on pitzuim if relevant)",
    ])

    if args.owns_apartment == "yes":
        plan.pre_move.extend([
            "Decide rental vs sale strategy for the Israeli apartment",
            "If renting: choose landlord tax track (10% flat vs progressive with deductions)",
            "Sign a property management agreement or give power of attorney to a family member",
        ])

    if args.family in ("family", "couple_with_kids", "children"):
        plan.pre_move.append(
            "Apostille children's school records (teudot gmar) in case of re-enrollment abroad"
        )

    plan.first_90_days.extend([
        "Verify Bituach Leumi standing order is executing (log in to ezor ishi at btl.gov.il)",
        "Open a bank account in destination country, receive first local paychecks",
        "Set up destination country tax ID and social security registration",
        "Buy private health insurance bridge for the gap until destination coverage starts",
        "Register foreign address with Israeli bank and with Bituach Leumi",
    ])

    if not is_treaty:
        plan.notes.append(
            f"{destination} is not a treaty country (or not in this tool's list). "
            "Israeli National Insurance is owed in full on reported income. "
            "If no income is reported, the minimum combined BL+health payment is 266 NIS/month (effective 01.01.2026). "
            "Verify with an accountant."
        )
    else:
        plan.notes.append(
            f"{destination} is a treaty country. If you pay social security there on employment income, "
            "you are exempt from Israeli National Insurance on that income and owe only health insurance (123 NIS/month minimum, effective 01.01.2026)."
        )

    plan.ongoing.extend([
        "File Israeli tax return annually (mandatory if still resident; optional if cut residency)",
        "Monitor Bituach Leumi balance quarterly",
        "Keep Israeli phone number active for .gov.il OTPs",
        "Track years abroad for future toshav chozer eligibility (6 years = regular, 10 years = vatik)",
    ])

    if args.stage in ("returning", "return_planning"):
        plan.return_prep.extend([
            "Determine toshav chozer status (6+ years = regular, 10+ years = vatik)",
            "Meet with a CPA specializing in toshav chozer 2-3 months before return",
            "Plan vehicle import (48 months max age, 9-month window from entry)",
            "Prepare customs declaration for household goods",
            "If Bituach Leumi payments were stopped: compare waiting period vs pidyon (12 minimum contributions)",
            "Re-activate kupat cholim after return or purchase pidyon for immediate coverage",
            "Re-file Israeli tax return from year of return, claim toshav chozer benefits correctly",
        ])

    return plan


def render(plan: Plan) -> str:
    sections = []
    if plan.pre_move:
        sections.append("## Pre-Move Checklist\n" + "\n".join(f"- {x}" for x in plan.pre_move))
    if plan.first_90_days:
        sections.append("## First 90 Days Abroad\n" + "\n".join(f"- {x}" for x in plan.first_90_days))
    if plan.ongoing:
        sections.append("## Ongoing While Abroad\n" + "\n".join(f"- {x}" for x in plan.ongoing))
    if plan.return_prep:
        sections.append("## Return Preparation\n" + "\n".join(f"- {x}" for x in plan.return_prep))
    if plan.notes:
        sections.append("## Notes\n" + "\n".join(f"- {x}" for x in plan.notes))
    sections.append(
        "\n_This is a guidance checklist, not legal or tax advice. "
        "Consult a qualified Israeli accountant (yo'etz mas) for decisions with financial impact._"
    )
    return "\n\n".join(sections)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stage",
        choices=["pre_move", "just_moved", "abroad", "returning", "return_planning"],
        default="pre_move",
    )
    parser.add_argument("--destination", default="usa", help="Destination country (lowercase, e.g. usa, uk, germany)")
    parser.add_argument("--duration", default="3y", help="Expected duration (free text, e.g. 2y, 5y, permanent)")
    parser.add_argument("--owns_apartment", choices=["yes", "no"], default="no")
    parser.add_argument(
        "--family",
        choices=["single", "couple", "family", "couple_with_kids", "children"],
        default="single",
    )
    args = parser.parse_args()

    plan = build_plan(args)
    print(render(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
