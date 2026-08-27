#!/usr/bin/env python3
"""
Israeli University Admissions Calculator

Calculate Bagrut averages (with 5-unit bonuses) and estimate
university admission composite scores (sekhem).

Usage:
    python calculate_sekhem.py bagrut --subjects '{"Math":{"units":5,"grade":90},"English":{"units":5,"grade":85}}'
    python calculate_sekhem.py sekhem --bagrut-avg 95 --psychometric 700
    python calculate_sekhem.py psychometric --score 650
    python calculate_sekhem.py thresholds
"""

import argparse
import json
import sys


# Bagrut bonus table, transcribed from the Technion's published table
# (admissions.technion.ac.il/calculation-of-the-median-grade, read 2026-08-27).
#
# The Technion is used because it is the only Israeli university that publishes
# a complete, readable bonus table. Tel Aviv and the Hebrew University expose
# only JavaScript calculators. The widely-quoted "+35 for 5-unit maths" comes
# from commercial prep companies, not from a university, and an earlier version
# of this script hardcoded it. The Technion's published maths bonus is +30.
#
# Two Technion rules this script DOES model: the >= 60 grade condition, and the
# mitzraf cluster bonus. One it does NOT: the double-weighting of maths units
# (5 units counted as 10) applied to every track except architecture, which
# moves a Technion sekhem more than the bonus does. Run the program's own
# calculator before quoting a number to a student.
FIVE_UNIT_BONUSES = {
    "Mathematics": 30,
    "Math": 30,
    "English": 25,
    "Physics": 25,
    "Chemistry": 25,
    "Biology": 25,
    "Computer Science": 25,
    "Arabic": 25,
    "Literature": 25,
    "Bible": 25,
    "History": 25,
    # French is NOT on the Technion's +25 language list; it falls to the
    # "additional subjects" tier.
    "French": 20,
}

# 4-unit subjects earn a real bonus, and omitting the tier silently scores a
# 4-unit student at zero (which an earlier version of this script did). But be
# careful how far this generalises: the Technion publishes +10 at 4 units for
# the "additional subjects" tables and for a gemer project, and does NOT
# publish a 4-unit rate for maths, the sciences, English or the recognized
# languages. Applying +10 to those is an extrapolation, so the script prints a
# warning whenever it does so.
FOUR_UNIT_BONUS = 10
FOUR_UNIT_UNPUBLISHED = {
    "Mathematics", "Math", "English", "Physics", "Chemistry", "Biology",
    "Computer Science", "Arabic",
}

# Subjects that count toward the mitzraf (cluster) bonus, which raises maths
# AND the qualifying partners to 30 each when 5-unit maths is combined with
# either two sciences or one science plus one technological subject.
MITZRAF_SCIENCES = {"Physics", "Chemistry", "Biology"}
MITZRAF_TECHNOLOGICAL = {
    "Computer Science", "Machine Control", "Electronics and Computers",
    "Engineering Sciences", "Biotechnology",
}
MITZRAF_BONUS = 30

# Rough standing by score. These are NOT official NITE percentiles: NITE does
# not publish a score-to-percentile table we could verify, and an earlier
# version of this script printed precise percentile ranks that contradicted the
# ones in SKILL.md. What IS published is the shape of the distribution, roughly
# normal with a mean near 548 and a standard deviation near 108, so the bands
# below are derived from that shape and described qualitatively on purpose.
PSYCHOMETRIC_STANDING = {
    800: "far above the mean (about 2.3 SD)",
    750: "well above the mean (about 1.9 SD)",
    740: "well above the mean (about 1.8 SD)",
    700: "above the mean (about 1.4 SD)",
    680: "above the mean (about 1.2 SD)",
    650: "above the mean (about 0.9 SD)",
    620: "somewhat above the mean (about 0.7 SD)",
    600: "somewhat above the mean (about 0.5 SD)",
    580: "slightly above the mean",
    550: "around the mean",
    530: "slightly below the mean",
    500: "below the mean (about 0.4 SD)",
    450: "well below the mean (about 0.9 SD)",
}

# Approximate admission thresholds
ADMISSION_THRESHOLDS = {
    "Medicine (Hebrew U)": 740,
    "Medicine (Technion)": 735,
    "Computer Science (Technion)": 700,
    "Computer Science (TAU)": 690,
    "Law (Hebrew U)": 690,
    "Law (TAU)": 680,
    "Electrical Engineering (Technion)": 680,
    "Engineering (BGU)": 640,
    "Business Admin (TAU)": 640,
    "Psychology (Hebrew U)": 660,
    "Business Admin (Bar-Ilan)": 600,
    "Social Sciences (Haifa)": 560,
    "Education (Various)": 520,
}

# University weight distributions (approximate)
UNIVERSITY_WEIGHTS = {
    "general": {"bagrut": 0.40, "psychometric": 0.60},
    "technion": {"bagrut": 0.35, "psychometric": 0.65},
    "hebrew_university": {"bagrut": 0.40, "psychometric": 0.60},
    "tel_aviv": {"bagrut": 0.40, "psychometric": 0.60},
    "ben_gurion": {"bagrut": 0.40, "psychometric": 0.60},
    "bar_ilan": {"bagrut": 0.45, "psychometric": 0.55},
    "haifa": {"bagrut": 0.45, "psychometric": 0.55},
}


def calculate_bagrut_average(subjects_json: str) -> None:
    """Calculate weighted Bagrut average with 5-unit bonuses."""
    try:
        subjects = json.loads(subjects_json)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format for subjects.", file=sys.stderr)
        print('Expected format: {"Subject":{"units":5,"grade":90}, ...}', file=sys.stderr)
        sys.exit(1)

    print("=== Bagrut Average Calculator ===\n")

    total_raw_weighted = 0
    total_boosted_weighted = 0
    total_units = 0
    total_bonus = 0

    # Decide the mitzraf (cluster) bonus BEFORE scoring, because it changes the
    # maths bonus as well as the partners'. It needs 5-unit maths at >= 60 plus
    # either two qualifying sciences or one science and one technological
    # subject, all at 5 units and >= 60. A gemer project never qualifies.
    def _eligible(names):
        return {
            n for n in names
            if subjects.get(n, {}).get("units") == 5
            and subjects.get(n, {}).get("grade", 0) >= 60
        }

    maths_names = {"Mathematics", "Math"}
    has_maths = bool(_eligible(maths_names))
    sciences = _eligible(MITZRAF_SCIENCES)
    technological = _eligible(MITZRAF_TECHNOLOGICAL)
    mitzraf_partners = set()
    if has_maths:
        if len(sciences) >= 2:
            mitzraf_partners = sciences
        elif len(sciences) >= 1 and len(technological) >= 1:
            mitzraf_partners = sciences | technological
    mitzraf_active = bool(mitzraf_partners)
    mitzraf_members = (
        (_eligible(maths_names) | mitzraf_partners) if mitzraf_active else set()
    )

    four_unit_extrapolated = set()

    print(f"{'Subject':<25} {'Units':>5} {'Grade':>5} {'Bonus':>5}")
    print("-" * 45)

    for name, data in subjects.items():
        units = data.get("units", 1)
        grade = data.get("grade", 0)
        bonus = 0

        # A bonus applies only from a final grade of 60 and up.
        if grade >= 60:
            if name in mitzraf_members:
                bonus = MITZRAF_BONUS
            elif units == 5 and name in FIVE_UNIT_BONUSES:
                bonus = FIVE_UNIT_BONUSES[name]
            elif units == 4 and name in FIVE_UNIT_BONUSES:
                bonus = FOUR_UNIT_BONUS
                if name in FOUR_UNIT_UNPUBLISHED:
                    four_unit_extrapolated.add(name)
            total_bonus += bonus

        # Canonical Israeli method: add the bonus to the subject grade, then take
        # the unit-weighted average: sum(units * (grade + bonus)) / sum(units).
        total_raw_weighted += grade * units
        total_boosted_weighted += (grade + bonus) * units
        total_units += units

        print(f"{name:<25} {units:>5} {grade:>5} {'+' + str(bonus) if bonus else '':>5}")

    print("-" * 45)

    if total_units == 0:
        print("No valid subjects provided.")
        return

    raw_average = total_raw_weighted / total_units
    boosted_average = total_boosted_weighted / total_units

    print(f"\nTotal units: {total_units}")
    print(f"Reaches the commonly-cited 21-unit floor: "
          f"{'Yes' if total_units >= 21 else 'No'} "
          "(the 21 figure is widely quoted but was not confirmed against a "
          "ministry page this cycle, so do not treat a No as a verdict)")
    print(f"Raw average: {raw_average:.1f}")
    if mitzraf_active:
        print(
            "Mitzraf (cluster) bonus applied: 5-unit maths plus "
            f"{', '.join(sorted(mitzraf_partners))} each scored at +{MITZRAF_BONUS}."
        )
    if four_unit_extrapolated:
        print(
            "WARNING: applied a +10 four-unit bonus to "
            f"{', '.join(sorted(four_unit_extrapolated))}, which the Technion does "
            "NOT publish a four-unit rate for. Treat those as estimates and check "
            "the program's own calculator."
        )
    print(f"Total bonus points: {total_bonus}")
    print(f"Boosted (bonus-weighted) average: {boosted_average:.1f}")
    print()
    print("NOTE: A bonus needs a final grade of 60+. 5-unit subjects take the\n      table value; 4-unit subjects on the same list take +10.")
    print("Bonus table is the Technion's published one (read 2026-08-27). Other")
    print("universities publish only calculators, so verify on the program's own.")
    print("NOT modelled here: the Technion double-weights maths UNITS (5 -> 10) in")
    print("the average for every track except architecture, which moves the result")
    print("more than the bonus does.")


def estimate_sekhem(bagrut_avg: float, psychometric: int,
                    university: str = "general") -> None:
    """Estimate university admission composite score."""
    print("=== Sekhem (Admission Score) Estimator ===\n")

    weights = UNIVERSITY_WEIGHTS.get(university, UNIVERSITY_WEIGHTS["general"])

    # NOT ANY UNIVERSITY'S FORMULA. The x8 factor is an arbitrary rescaling with
    # no published basis, and the per-university weights below are unsourced:
    # no Israeli university we could reach publishes a readable weighting table
    # (Tel Aviv exposes only a JavaScript calculator). A bonus-inflated Bagrut
    # average routinely exceeds 100, so the Bagrut leg can exceed 800 on its own
    # and outweigh a perfect psychometric. Treat the output as a rough relative
    # indicator only, never as an admission chance.
    bagrut_normalized = bagrut_avg * 8
    sekhem = (bagrut_normalized * weights["bagrut"]) + (psychometric * weights["psychometric"])

    print(f"Bagrut average: {bagrut_avg:.1f}")
    print(f"Psychometric score: {psychometric}")
    print(f"University weights: {university}")
    print(f"  Bagrut weight: {weights['bagrut']:.0%}")
    print(f"  Psychometric weight: {weights['psychometric']:.0%}")
    print()
    print(f"Bagrut component: {bagrut_normalized * weights['bagrut']:.1f}")
    print(f"Psychometric component: {psychometric * weights['psychometric']:.1f}")
    print(f"Indicative composite: {sekhem:.1f}")
    print()
    print("THIS IS NOT A UNIVERSITY'S SEKHEM AND NOT AN ADMISSION CHANCE.")
    print("The Bagrut-to-psychometric rescaling here has no published basis, and no")
    print("Israeli university publishes a readable weighting table, so the weights")
    print("above are estimates. Run the target program's own calculator.")
    print()
    print("This tool deliberately does NOT print an eligibility verdict per program.")
    print("An earlier version listed '[OK] Medicine', which was wrong twice over: the")
    print("thresholds were unsourced, and medicine admission is gated by a NITE")
    print("selection system (MOR / MIRKAM / MERAV) and by the institution's own")
    print("registration deadline, neither of which any composite score can satisfy.")


def interpret_psychometric(score: int) -> None:
    """Interpret a psychometric exam score."""
    print("=== Psychometric Score Interpretation ===\n")
    print(f"Score: {score}\n")

    # Find percentile
    closest = None
    for threshold in sorted(PSYCHOMETRIC_STANDING.keys(), reverse=True):
        if score >= threshold:
            closest = threshold
            break

    if closest:
        standing = PSYCHOMETRIC_STANDING[closest]
        print(f"Rough standing: {standing}")
        print("This is NOT an official percentile. NITE publishes no score-to-percentile")
        print("table we could verify; the mean is about 548 with an SD of about 108.")
    else:
        print("Score below reference range.")

    print()

    if score >= 740:
        assessment = "Excellent -- eligible for most competitive programs (medicine, law at top universities)"
    elif score >= 680:
        assessment = "Very good -- eligible for competitive programs (CS, engineering at Technion/TAU)"
    elif score >= 620:
        assessment = "Good -- eligible for many university programs"
    elif score >= 550:
        assessment = "Average -- eligible for some university programs, most colleges"
    elif score >= 480:
        assessment = "Below average -- limited university options, consider mechina or college"
    else:
        assessment = "Consider retaking with preparation course, or alternative pathways"

    print(f"Assessment: {assessment}")
    print()

    print("The highest score counts. The current retake-limit position is not stated on")
    print("any NITE page we could read, so do not assume there is no cap: check nite.org.il.")
    print("Languages vary BY SITTING: Sept 2026 was Hebrew and Arabic only;")
    print("April and July 2027 add a combined/English form, Russian and French.")
    print("Spanish is not offered. Check the sitting, not the exam.")
    print("Cost: 665 NIS standard registration (nite.org.il dates-and-prices,\n      read 2026-08-27); late registration adds a surcharge. Re-verify before quoting.")
    print()
    print("From December 2026 the PET drops English, covering two domains across five")
    print("multiple-choice sections plus a writing task, one hour shorter than before.")
    print("English moves to Amirnet, which already exists and is live now (315 NIS,")
    print("35-day minimum between sittings). Admissions impact starts from academic")
    print("year 5788 (October 2027). Verify on nite.org.il.")
    print()
    print("Popular prep courses: Kidum, High-Q, Yoel Geva, Psagot")
    print("Free practice: nite.org.il")


def show_thresholds() -> None:
    """Display admission thresholds for popular programs."""
    print("=== Approximate Admission Thresholds (Sekhem) ===\n")
    print(f"{'Program':<40} {'Threshold'}")
    print("-" * 55)

    for prog, thresh in sorted(ADMISSION_THRESHOLDS.items(), key=lambda x: -x[1]):
        bar = "#" * (thresh // 20)
        print(f"{prog:<40} {thresh:>5} {bar}")

    print()
    print("NOTE: Thresholds are approximate and change each admission cycle.")
    print("Check specific university websites for current requirements.")


def main():
    parser = argparse.ArgumentParser(
        description="Israeli University Admissions Calculator"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Bagrut average
    bag_parser = subparsers.add_parser("bagrut", help="Calculate Bagrut average")
    bag_parser.add_argument("--subjects", required=True,
                            help='JSON: {"Subject":{"units":5,"grade":90}, ...}')

    # Sekhem estimate
    sek_parser = subparsers.add_parser("sekhem", help="Estimate admission score")
    sek_parser.add_argument("--bagrut-avg", type=float, required=True,
                            help="Bagrut average (with bonuses)")
    sek_parser.add_argument("--psychometric", type=int, required=True,
                            help="Psychometric score (200-800)")
    sek_parser.add_argument("--university", default="general",
                            choices=list(UNIVERSITY_WEIGHTS.keys()),
                            help="University for weight calculation")

    # Psychometric interpretation
    psy_parser = subparsers.add_parser("psychometric", help="Interpret psychometric score")
    psy_parser.add_argument("--score", type=int, required=True,
                            help="Psychometric score (200-800)")

    # Thresholds
    subparsers.add_parser("thresholds", help="Show admission thresholds")

    args = parser.parse_args()

    if args.command == "bagrut":
        calculate_bagrut_average(args.subjects)
    elif args.command == "sekhem":
        estimate_sekhem(args.bagrut_avg, args.psychometric, args.university)
    elif args.command == "psychometric":
        interpret_psychometric(args.score)
    elif args.command == "thresholds":
        show_thresholds()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
