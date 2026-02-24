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


# 5-unit bonus points for university admissions
FIVE_UNIT_BONUSES = {
    "Mathematics": 35,
    "Math": 35,
    "English": 35,
    "Physics": 25,
    "Chemistry": 25,
    "Biology": 25,
    "Computer Science": 25,
    "Arabic": 25,
    "French": 25,
}

# Psychometric score percentile mapping
PSYCHOMETRIC_PERCENTILES = {
    800: ("99.9th", "Top 0.1%"),
    750: ("99th", "Top 1%"),
    740: ("98th", "Top 2%"),
    700: ("95th", "Top 5%"),
    680: ("92nd", "Top 8%"),
    650: ("85th", "Top 15%"),
    620: ("78th", "Top 22%"),
    600: ("70th", "Top 30%"),
    580: ("60th", "Top 40%"),
    550: ("50th", "Median"),
    530: ("45th", "Average"),
    500: ("35th", "Below average"),
    450: ("20th", "Lower quintile"),
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
    "tel_aviv": {"bagrut": 0.45, "psychometric": 0.55},
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

    total_weighted = 0
    total_units = 0
    total_bonus = 0
    num_subjects = len(subjects)

    print(f"{'Subject':<25} {'Units':>5} {'Grade':>5} {'Bonus':>5}")
    print("-" * 45)

    for name, data in subjects.items():
        units = data.get("units", 1)
        grade = data.get("grade", 0)
        bonus = 0

        if units == 5 and name in FIVE_UNIT_BONUSES:
            bonus = FIVE_UNIT_BONUSES[name]
            total_bonus += bonus

        total_weighted += grade * units
        total_units += units

        print(f"{name:<25} {units:>5} {grade:>5} {'+' + str(bonus) if bonus else '':>5}")

    print("-" * 45)

    if total_units == 0:
        print("No valid subjects provided.")
        return

    raw_average = total_weighted / total_units
    # Bonus is typically added as points to the average (divided by number of subjects)
    bonus_contribution = total_bonus / num_subjects if num_subjects > 0 else 0
    boosted_average = min(raw_average + bonus_contribution, 120)

    print(f"\nTotal units: {total_units}")
    print(f"Meets minimum (21 units): {'Yes' if total_units >= 21 else 'No'}")
    print(f"Raw average: {raw_average:.1f}")
    print(f"5-unit bonus points: {total_bonus}")
    print(f"Boosted average: {boosted_average:.1f}")
    print()
    print("NOTE: Exact bonus calculation varies by university.")


def estimate_sekhem(bagrut_avg: float, psychometric: int,
                    university: str = "general") -> None:
    """Estimate university admission composite score."""
    print("=== Sekhem (Admission Score) Estimator ===\n")

    weights = UNIVERSITY_WEIGHTS.get(university, UNIVERSITY_WEIGHTS["general"])

    # Normalize Bagrut to similar scale as psychometric (roughly x8)
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
    print(f"Estimated sekhem: {sekhem:.1f}")
    print()

    # Find matching programs
    print("Potentially eligible programs (approximate):")
    eligible = [(prog, thresh) for prog, thresh in ADMISSION_THRESHOLDS.items()
                if sekhem >= thresh]
    borderline = [(prog, thresh) for prog, thresh in ADMISSION_THRESHOLDS.items()
                  if thresh - 20 <= sekhem < thresh]

    if eligible:
        for prog, thresh in sorted(eligible, key=lambda x: -x[1]):
            margin = sekhem - thresh
            print(f"  [OK]  {prog} (threshold ~{thresh}, margin +{margin:.0f})")

    if borderline:
        print("\nBorderline (within 20 points):")
        for prog, thresh in sorted(borderline, key=lambda x: -x[1]):
            gap = thresh - sekhem
            print(f"  [??]  {prog} (threshold ~{thresh}, gap -{gap:.0f})")

    print()
    print("NOTE: Actual thresholds change yearly. Check specific program requirements.")


def interpret_psychometric(score: int) -> None:
    """Interpret a psychometric exam score."""
    print("=== Psychometric Score Interpretation ===\n")
    print(f"Score: {score}\n")

    # Find percentile
    closest = None
    for threshold in sorted(PSYCHOMETRIC_PERCENTILES.keys(), reverse=True):
        if score >= threshold:
            closest = threshold
            break

    if closest:
        percentile, description = PSYCHOMETRIC_PERCENTILES[closest]
        print(f"Approximate percentile: {percentile} ({description})")
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

    remaining_attempts = 3  # Maximum total attempts
    print(f"Maximum attempts: {remaining_attempts} total")
    print("Available in: Hebrew, Arabic, Russian, French, Spanish")
    print("Cost: ~500 NIS per sitting")
    print()
    print("Popular prep courses: Kidum, Yoel Geva, Atid, Psagot")
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
