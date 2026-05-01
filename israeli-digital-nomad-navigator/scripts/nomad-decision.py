#!/usr/bin/env python3
"""Israeli Digital Nomad Navigator — interactive decision script.

Takes the user's situation (employment shape, destination, duration, intent)
and outputs a phased checklist of Israeli-side actions, with cross-references
to the SKILL.md sections and links to authoritative sources.

This is an aid, not legal advice. Always pair with a CPA + lawyer for filings.

Usage:
  python scripts/nomad-decision.py --shape employee --destination portugal --duration 6m --intent stay
  python scripts/nomad-decision.py --shape freelancer --destination thailand --duration 24m --intent stay
  python scripts/nomad-decision.py --interactive
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from typing import Literal

EmploymentShape = Literal["employee", "freelancer", "mixed", "no_income"]
ResidencyIntent = Literal["stay", "cut", "undecided"]

# Bituach Leumi totalization treaty list (per btl.gov.il, May 2026).
TOTALIZATION_FULL = {
    "argentina", "austria", "belgium", "bulgaria", "czech_republic", "denmark",
    "finland", "france", "germany", "italy", "norway", "poland", "romania",
    "russia", "slovakia", "sweden", "switzerland", "netherlands",
    "united_kingdom", "uruguay",
}
TOTALIZATION_LIMITED = {"canada"}  # excluding Quebec

# 2026 visa data — verified per references/visa-by-country-2026.md.
VISA_DATA: dict[str, dict[str, str]] = {
    "thailand": {
        "program": "DTV (Destination Thailand Visa)",
        "income": "THB 500,000 across last 3 months + 6 months salary slips",
        "fee": "350 EUR / ฿13,350 at Royal Thai Embassy Tel Aviv",
        "validity": "5-year multi-entry; 180 days per entry; one 180-day extension at ฿1,900",
        "available": "yes",
    },
    "spain": {
        "program": "DNV (Visado de Teletrabajo)",
        "income": "€2,849/month (200% of 2026 SMI)",
        "fee": "Standard consular fee",
        "validity": "1-year if applied from abroad; 3-year residence permit if converted from inside",
        "available": "yes",
    },
    "portugal": {
        "program": "D8 Digital Nomad Visa",
        "income": "€3,680/month + €11,040 savings (12× minimum wage)",
        "fee": "Standard consular fee",
        "validity": "1-year temporary OR 2-year residency renewable for 3",
        "available": "yes",
    },
    "estonia": {
        "program": "Type D Digital Nomad Visa",
        "income": "€4,500/month gross",
        "fee": "Consular fee",
        "validity": "1 year",
        "available": "yes",
    },
    "croatia": {
        "program": "Digital Nomad Residence",
        "income": "€3,622.50/month or €39,540 savings (12-mo) / €59,310 (18-mo); +10% per family member",
        "fee": "Consular fee",
        "validity": "Up to 18 months, non-renewable consecutively (6-month gap to reapply); foreign income exempt from Croatian tax",
        "available": "yes",
    },
    "czech_republic": {
        "program": "Zivno (zivnostensky list — freelance/digital-nomad track)",
        "income": "~CZK 69,836/month for IT/marketing nomad track, or ~CZK 20,000/month for regular Zivno",
        "fee": "Consular fee + monthly social-security 5,720 CZK + health 3,306 CZK from Jan 2026",
        "validity": "1 year, renewable",
        "available": "yes",
    },
    "mexico": {
        "program": "Residente Temporal",
        "income": "~USD 4,300/month for prior 6 months OR ~USD 74,000 savings for prior 12 months",
        "fee": "Consular fee",
        "validity": "1 year, renewable up to 4 total",
        "available": "yes",
    },
    "costa_rica": {
        "program": "Estancia (Rentista para Trabajadores Remotos)",
        "income": "USD 3,000/month individual or USD 4,000/month family from outside Costa Rica",
        "fee": "Consular fee",
        "validity": "2 years (1+1); 180-day minimum presence to renew; foreign income tax-exempt",
        "available": "yes",
    },
    "georgia": {
        "program": "Remotely from Georgia + Right to Labour Activity (1 Mar 2026)",
        "income": "USD 2,000/month or USD 24,000 savings + insurance",
        "fee": "Free for most passports including Israeli (visa) + Right to Labour Activity permit fee",
        "validity": "365-day visa-free historically; from 1 March 2026 paid work also requires Right to Labour Activity permit",
        "available": "yes",
    },
    "uae": {
        "program": "Dubai Virtual Working Programme",
        "income": "USD 5,000/month + valid foreign employer (raised from $3,500 Apr 2026) + 6 months statements",
        "fee": "$611 + UAE-valid health insurance",
        "validity": "1 year, renewable",
        "available": "yes",
    },
    "indonesia": {
        "program": "B211A / E33G / KITAS / Second Home",
        "income": "—",
        "fee": "—",
        "validity": "—",
        "available": "no — Israeli citizens explicitly barred as of 2026",
    },
    "bali": {
        "program": "B211A / E33G / KITAS / Second Home",
        "income": "—",
        "fee": "—",
        "validity": "—",
        "available": "no — Israeli citizens explicitly barred as of 2026",
    },
    "usa": {
        "program": "No dedicated digital-nomad visa",
        "income": "—",
        "fee": "—",
        "validity": "ESTA visa-free 90 days (recent change for Israelis); B1/B2 for longer",
        "available": "limited — work on tourist/ESTA is technically prohibited",
    },
}


@dataclass
class Plan:
    user_situation: dict[str, str]
    visa: dict[str, str] = field(default_factory=dict)
    treaty_status: str = ""
    residency_strategy: str = ""
    actions_pre_departure: list[str] = field(default_factory=list)
    actions_living_abroad: list[str] = field(default_factory=list)
    actions_annual: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)


def normalize_destination(dest: str) -> str:
    return dest.lower().strip().replace(" ", "_").replace("-", "_")


def parse_duration(s: str) -> int:
    """Convert '6m' / '18m' / '2y' to months (int)."""
    s = s.lower().strip()
    if s.endswith("y"):
        return int(float(s[:-1]) * 12)
    if s.endswith("m"):
        return int(float(s[:-1]))
    return int(s)


def build_plan(
    shape: EmploymentShape,
    destination: str,
    duration_months: int,
    intent: ResidencyIntent,
) -> Plan:
    plan = Plan(user_situation={
        "employment": shape,
        "destination": destination,
        "duration_months": str(duration_months),
        "residency_intent": intent,
    })

    norm = normalize_destination(destination)
    plan.visa = VISA_DATA.get(norm, {
        "program": "Not in built-in table",
        "income": "Verify on destination embassy site",
        "fee": "Verify",
        "validity": "Verify",
        "available": "unknown",
    })

    if plan.visa.get("available") == "no":
        plan.flags.append(
            f"⚠ {destination.upper()} is NOT available to Israeli passport holders as of 2026. "
            "Pick a different destination (Thailand DTV, Spain DNV, Portugal D8, Georgia, etc.)."
        )

    is_full_treaty = norm in TOTALIZATION_FULL
    is_limited_treaty = norm in TOTALIZATION_LIMITED
    if is_full_treaty:
        plan.treaty_status = (
            f"{destination.title()} HAS a full bilateral social-security convention with Israel. "
            "File Form A1 / Certificate of Coverage with Bituach Leumi BEFORE departure."
        )
    elif is_limited_treaty:
        plan.treaty_status = (
            f"{destination.title()} has a LIMITED convention with Israel (Canada excludes Quebec). "
            "Coverage is narrower than full treaties — confirm scope with BTL international affairs."
        )
    else:
        plan.treaty_status = (
            f"{destination.title()} has NO bilateral social-security convention with Israel. "
            "An Israeli employee on Israeli payroll faces double social-security exposure here. "
            "An Israeli freelancer is unaffected (no employer to register)."
        )

    # Residency strategy
    if intent == "stay" or duration_months < 24:
        plan.residency_strategy = (
            "Default: stay an Israeli tax resident. Continue paying bituach leumi to keep "
            "kupat cholim active. File Form 1322/1325 annually with worldwide income."
        )
    elif intent == "cut":
        plan.residency_strategy = (
            "Cutting residency (nituk toshavut). MODEL Section 100A exit tax FIRST — "
            "deemed sale of all assets at FMV the day before residency ceases. "
            "Lose kupat cholim continuity; toshav chozer benefits require 6+ years out, "
            "toshav chozer vatik 10+ years out."
        )
    else:
        plan.residency_strategy = (
            "Undecided. For stays under 3 years, default to staying resident is almost always better. "
            "For 5+ year commitments, model Section 100A and toshav chozer benefits before deciding."
        )

    # Pre-departure actions
    plan.actions_pre_departure.extend([
        "Apply for the destination visa per the table above. Get apostille on civil documents at MFA / my.gov.il e-apostille.",
        "If staying tax resident: set up bituach leumi standing order (horaat keva) for the minimum monthly payment to keep kupat cholim alive.",
        "File 'הודעה על שהייה בחו״ל' notification with Bituach Leumi.",
        "Buy a long-stay insurance policy that explicitly covers REMOTE WORK (SafetyWing, Genki, or an Israeli policy with working-abroad rider). Standard travel insurance excludes work activity and long stays.",
        "Open a Wise multi-currency account if not already; consider Payoneer if clients pay via marketplaces; keep at least one Israeli credit card active for gov.il portal payments.",
        "ETIAS pre-authorization for any Schengen application travel (€7, valid 3 years).",
    ])

    # Employee branch
    if shape == "employee":
        if is_full_treaty:
            plan.actions_pre_departure.insert(
                1,
                "REQUIRED: file Form A1 / Certificate of Coverage with Bituach Leumi to exempt the Israeli employer from foreign social-security charges on the same wages."
            )
        plan.actions_pre_departure.append(
            "Negotiate a written 'working from abroad' addendum to the Israeli employment contract: "
            "days-cap, equipment, data security, sick days, return obligations, dismissal protections, "
            "tax equalization or gross-up clause, reservist call-up handling."
        )
        plan.actions_living_abroad.append(
            "Track days per country to stay under the 183-day permanent-establishment threshold "
            "(some countries are stricter). Keep a calendar log of arrival/departure dates."
        )
        plan.actions_living_abroad.append(
            "No client meetings in the host country, no signing authority used there, no commercial office in the employer's name, no local hires."
        )
        plan.flags.append(
            "Section 14, keren hishtalmut, and pension contributions all CONTINUE on Israeli payroll — they do not pause while abroad."
        )

    # Freelancer branch
    if shape == "freelancer":
        plan.actions_pre_departure.extend([
            "Issue VAT Section 30(a)(5) zero-rated invoices to foreign clients. Document the foreign-resident nature of each client (incorporation cert, foreign address, payment from foreign bank) in your VAT books.",
            "File W-8BEN with each US client to claim US-Israel treaty benefits and reduce 30% default withholding to the treaty rate. Form goes to the client, not the IRS; valid 3 years.",
            "Draft a bilingual EN/HE service agreement template with: parties + jurisdiction + IL governing law, IP assignment, NDA, USD/EUR payment terms, late-payment interest, termination + cure, Section 30 documentation hooks.",
        ])
        plan.actions_annual.append(
            "Periodic VAT report (Form 874): zero-rated revenue goes in the 0%-rate row; input VAT on related expenses still recoverable."
        )

    # Living-abroad common actions
    plan.actions_living_abroad.append(
        "Quarterly check: bituach leumi standing order is paid; kupat cholim status active; "
        "no surprise local-tax-residency triggers in the host country."
    )

    # Annual cycle
    plan.actions_annual.extend([
        "By 30 April of the following tax year: file Form 1301 (the main individual annual return) with Form 1322 (capital gains supplement) and Form 1325 (capital gains by tax rate) as needed.",
        "Apply foreign tax credit (זיכוי מס זר) under Sections 199-210 of the Income Tax Ordinance and any applicable bilateral treaty. Use the income-source basket system; excess credits carry forward up to 5 years per basket.",
        "If foreign income/assets cross the ITO sec. 131A trigger thresholds (verify current year on gov.il/en/service/itc5329b before filing): file Form 5329 disclosure listing each foreign account (Wise, Revolut, Payoneer, foreign bank).",
        "Convert all amounts to NIS at BOI שער יציג (representative rate) on the date of receipt for business income.",
    ])

    # Flags
    if duration_months >= 60:
        plan.flags.append(
            "Stay exceeds 5 years → BTL re-classifies you as non-resident unless you actively prove temporary stay. "
            "Schedule a year-4 BTL check-in to keep status."
        )
    if duration_months >= 12 and shape == "employee" and not is_full_treaty:
        plan.flags.append(
            "Employee on Israeli payroll + non-treaty country + 12+ months = high permanent-establishment risk for the employer. "
            "Brief HR/legal early."
        )
    if intent == "cut":
        plan.flags.append(
            "Section 100A exit tax can produce a very large bill on vested startup equity — model BEFORE filing nituk toshavut."
        )
    if duration_months <= 12 and intent == "stay":
        plan.flags.append(
            "Short, defined nomad stretch → simplest path. No relocation paperwork needed. Just keep bituach leumi alive."
        )

    return plan


def render_plan(plan: Plan) -> str:
    out = []
    out.append("=" * 70)
    out.append("ISRAELI DIGITAL NOMAD NAVIGATOR — Personalized plan")
    out.append("=" * 70)
    out.append("")
    out.append("USER SITUATION:")
    for k, v in plan.user_situation.items():
        out.append(f"  {k:<25} {v}")
    out.append("")
    out.append("VISA OPTION:")
    for k, v in plan.visa.items():
        out.append(f"  {k:<15} {v}")
    out.append("")
    out.append(f"BITUACH LEUMI TREATY: {plan.treaty_status}")
    out.append("")
    out.append(f"RESIDENCY STRATEGY: {plan.residency_strategy}")
    out.append("")
    out.append("PRE-DEPARTURE ACTIONS:")
    for i, a in enumerate(plan.actions_pre_departure, 1):
        out.append(f"  {i}. {a}")
    out.append("")
    out.append("WHILE ABROAD:")
    for i, a in enumerate(plan.actions_living_abroad, 1):
        out.append(f"  {i}. {a}")
    out.append("")
    out.append("ANNUAL CYCLE:")
    for i, a in enumerate(plan.actions_annual, 1):
        out.append(f"  {i}. {a}")
    out.append("")
    if plan.flags:
        out.append("⚠ FLAGS:")
        for f in plan.flags:
            out.append(f"  - {f}")
        out.append("")
    out.append("=" * 70)
    out.append("Pair this plan with a Roeh Cheshbon and a labor lawyer before filing.")
    out.append("Forms: 1322/1325 (annual), 1348 (residency declaration), 5329 (foreign assets), A1 (totalization).")
    out.append("=" * 70)
    return "\n".join(out)


def interactive() -> tuple[EmploymentShape, str, int, ResidencyIntent]:
    print("Israeli Digital Nomad Navigator — interactive setup")
    print()
    print("Employment shape:")
    print("  1. Israeli employee on tlush maskoret")
    print("  2. Osek murshe with foreign clients")
    print("  3. Mixed (employee + freelance)")
    print("  4. No current income")
    shape_in = input("Choose 1-4: ").strip()
    shape_map: dict[str, EmploymentShape] = {
        "1": "employee", "2": "freelancer", "3": "mixed", "4": "no_income",
    }
    shape = shape_map.get(shape_in, "employee")

    destination = input("Destination country (e.g., portugal, thailand, spain): ").strip()

    duration_in = input("Intended duration (e.g., 6m, 18m, 2y): ").strip()
    duration_months = parse_duration(duration_in)

    intent_in = input("Residency intent — stay Israeli resident, cut residency, or undecided? [stay/cut/undecided]: ").strip().lower()
    intent_map: dict[str, ResidencyIntent] = {
        "stay": "stay", "cut": "cut", "undecided": "undecided",
    }
    intent = intent_map.get(intent_in, "undecided")

    return shape, destination, duration_months, intent


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--shape", choices=["employee", "freelancer", "mixed", "no_income"])
    p.add_argument("--destination")
    p.add_argument("--duration", help="e.g., 6m, 18m, 2y")
    p.add_argument("--intent", choices=["stay", "cut", "undecided"], default="undecided")
    p.add_argument("--interactive", action="store_true")
    p.add_argument("--example", action="store_true",
                   help="Run a canned example: employee in Portugal for 6 months staying resident")
    args = p.parse_args()

    if args.example:
        plan = build_plan("employee", "portugal", 6, "stay")
        print(render_plan(plan))
        return

    if args.interactive or not (args.shape and args.destination and args.duration):
        shape, destination, duration_months, intent = interactive()
    else:
        shape = args.shape
        destination = args.destination
        duration_months = parse_duration(args.duration)
        intent = args.intent

    plan = build_plan(shape, destination, duration_months, intent)
    print(render_plan(plan))


if __name__ == "__main__":
    main()
