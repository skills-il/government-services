#!/usr/bin/env python3
"""
Israeli Bituach Leumi (National Insurance) Benefit Calculator

Standalone utility for estimating Bituach Leumi benefit amounts including
old age pension, unemployment, maternity, child allowance, miluim, and
birth grant. All hardcoded amounts reflect 2026 official rates as published
in btl.gov.il/About/news/Pages/hadasaidkonkitzva2026.aspx.

Usage:
    python calculate_benefits.py pension --age 67 --status single
    python calculate_benefits.py unemployment --salary 15000 --age 35 --months 14
    python calculate_benefits.py maternity --salary 20000 --months-employed 12
    python calculate_benefits.py child-allowance --children 3
    python calculate_benefits.py miluim --salary 18000 --days 30
    python calculate_benefits.py birth-grant --child-position 1
"""

import argparse
import sys


# 2026 macroeconomic anchors (verify at btl.gov.il before relying on outputs).
AVERAGE_WAGE_BENEFITS = 13769  # section-2 average wage, NIS/month
DAILY_AVG_WAGE = AVERAGE_WAGE_BENEFITS / 25  # 550.76 NIS/day (working-days basis for unemployment cap)
MAX_INSURABLE = 51910  # NIS/month


def calculate_pension(age: int, status: str, years_contributed: int = 30,
                      defer_years: int = 0) -> None:
    """Estimate old age pension (kitzbat zikna)."""
    # 2026 base amounts
    base_single_under80 = 1838
    base_single_from80 = 1941
    base_couple = 2762

    print("=== Old Age Pension (Kitzbat Zikna) Estimate, 2026 rates ===\n")

    # Eligibility age
    eligibility_age_men = 67
    # Women: depends on birth-month cohort, currently 62-65, completes ~2032.
    eligibility_age_women_typical = 65

    if age < 62:
        print(f"Age {age}: Not yet eligible.")
        print(f"  Men eligible at: {eligibility_age_men}.")
        print(f"  Women eligible at: 62-65 (depends on birth cohort, "
              f"check btl.gov.il/benefits/old_age/Pages/RetirementCalculation.aspx).")
        return

    # Pick base
    if status == "couple":
        base = base_couple
    else:
        base = base_single_from80 if age >= 80 else base_single_under80

    # Seniority supplement: +2% per year starting from year 11, cap 50%
    seniority_years = max(0, years_contributed - 10)
    seniority_bonus = min(seniority_years * 0.02, 0.50)

    # Deferral bonus: +5% per year, paid up to age 70
    deferral_bonus = defer_years * 0.05

    total_bonus = seniority_bonus + deferral_bonus
    estimated_monthly = base * (1 + total_bonus)

    print(f"Status: {status.title()}")
    print(f"Age: {age}")
    print(f"Years contributed: {years_contributed}")
    print(f"Deferral years: {defer_years}")
    print()
    print(f"Base amount (2026): {base:,.0f} NIS/month")
    print(f"Seniority bonus: +{seniority_bonus:.0%} ({seniority_years} years beyond 10, "
          "capped at 50%)")
    print(f"Deferral bonus: +{deferral_bonus:.0%} ({defer_years} years)")
    print(f"Estimated monthly pension: {estimated_monthly:,.0f} NIS/month")
    print(f"Estimated annual pension: {estimated_monthly * 12:,.0f} NIS/year")
    print()
    print("NOTE: Most pensioners receive the full +50% seniority supplement, "
          "bringing the typical single rate to ~2,757 NIS.")
    print("NOTE: Income test applies between retirement age and 70 (single ~7,827 NIS, "
          "couple ~10,436 NIS).")
    print("Verify your specific case at btl.gov.il or call *6050.")
    print("Claim form: 480 (תביעה לקצבת אזרח ותיק).")


def calculate_unemployment(salary: float, age: int, months_employed: int,
                           has_dependents: bool = False) -> None:
    """Estimate unemployment benefits (dmei avtala)."""
    print("=== Unemployment Benefits (Dmei Avtala) Estimate, 2026 rates ===\n")

    if months_employed < 12:
        print(f"Months employed: {months_employed}")
        print("NOT ELIGIBLE: Minimum 12 months of employment in last 18 months required.")
        return

    # Duration based on age and dependents
    if age < 25:
        duration_days = 50
    elif age < 28:
        duration_days = 50 if not has_dependents else 67
    elif age < 35:
        duration_days = 67 if not has_dependents else 100
    elif age < 45:
        duration_days = 100 if not has_dependents else 138
    else:
        duration_days = 138 if not has_dependents else 175

    # 2026 caps
    cap_first_period = 550.76  # average wage 13,769 ÷ 25 working days
    cap_second_period = 367.17  # 2/3 daily avg wage

    daily_wage = salary / 25  # working days per month

    # Sliding scale by salary (simplified; real BTL uses bracketed tiers).
    # Average-wage anchor for benefit calcs:
    avg_wage = AVERAGE_WAGE_BENEFITS

    if salary <= avg_wage * 0.5:
        first_rate = daily_wage * 0.80
    elif salary <= avg_wage * 0.667:
        first_rate = daily_wage * 0.70
    elif salary <= avg_wage:
        first_rate = daily_wage * 0.60
    else:
        first_rate = daily_wage * 0.50

    first_rate = min(first_rate, cap_first_period)

    first_period_days = min(125, duration_days)
    second_period_days = max(0, duration_days - 125)

    total_first = first_period_days * first_rate
    total_second = second_period_days * cap_second_period
    total_benefit = total_first + total_second

    waiting_days = 5

    print(f"Monthly salary: {salary:,.0f} NIS")
    print(f"Age: {age}")
    print(f"Has dependents: {'Yes' if has_dependents else 'No'}")
    print(f"Months employed: {months_employed}")
    print()
    print(f"Waiting period: {waiting_days} working days (terminations only; "
          "resignation triggers 90-day disqualification unless justified cause)")
    print(f"Benefit duration: {duration_days} days")
    print(f"First period ({first_period_days} days): ~{first_rate:,.0f} NIS/day "
          f"(cap {cap_first_period:,.2f} NIS/day)")
    if second_period_days > 0:
        print(f"Second period ({second_period_days} days): "
              f"{cap_second_period:,.2f} NIS/day (2/3 daily avg wage)")
    print()
    print(f"Estimated total benefit: {total_benefit:,.0f} NIS")
    print(f"Estimated monthly equivalent: "
          f"{total_benefit / (duration_days / 25):,.0f} NIS/month")
    print()
    print("NOTE: Actual amounts depend on precise salary history and current rates.")
    print("Benefits subject to income tax.")
    print("Claim form: 1500 + employer attachment 1514.")
    print("File at: https://www.taasuka.gov.il/applicants/sharedform/ (combined "
          "with שירות התעסוקה registration).")


def calculate_maternity(salary: float, months_employed: int) -> None:
    """Estimate maternity benefits (dmei leida)."""
    print("=== Maternity Benefits (Dmei Leida) Estimate, 2026 rates ===\n")

    if months_employed < 6:
        print(f"Months employed: {months_employed}")
        print("NOT ELIGIBLE: Minimum 6 months of employment required.")
        return

    if months_employed >= 10:
        weeks = 15
    else:
        weeks = 8

    # 2026 cap
    max_daily = 1752.33
    daily_salary = salary / 30

    daily_benefit = min(daily_salary, max_daily)
    total_days = weeks * 7
    total_benefit = daily_benefit * total_days

    print(f"Monthly salary: {salary:,.0f} NIS")
    print(f"Months employed: {months_employed}")
    print()
    print(f"Leave duration: {weeks} weeks ({total_days} days)")
    print(f"Daily benefit: {daily_benefit:,.2f} NIS/day "
          f"(cap {max_daily:,.2f} NIS/day in 2026)")
    print(f"Total estimated benefit: {total_benefit:,.0f} NIS")
    print()
    print("Calculation base: last 3 months ÷ 90 OR last 6 months ÷ 180, "
          "whichever is higher (this script uses simplified salary÷30).")
    print("Multiple births: +3 weeks. Hospitalization extension if newborn "
          "hospitalized 15+ days.")
    print("Partner leave: 1 week dedicated, remaining weeks splittable.")
    print("Claim form: 355 (mother) or 356 (combined with birth grant).")


def calculate_child_allowance(num_children: int) -> None:
    """Estimate child allowance (kitzbat yeladim)."""
    print("=== Child Allowance (Kitzbat Yeladim) Estimate, 2026 rates ===\n")

    # 2026 tiered amounts: 1st 173, 2nd-4th 219 each, 5th+ 173
    rate_first = 173
    rate_middle = 219
    rate_high = 173

    if num_children <= 0:
        print("No children.")
        return
    if num_children == 1:
        total_monthly = rate_first
    elif num_children <= 4:
        total_monthly = rate_first + rate_middle * (num_children - 1)
    else:
        total_monthly = rate_first + rate_middle * 3 + rate_high * (num_children - 4)

    total_annual = total_monthly * 12

    print(f"Number of children: {num_children}")
    print(f"  1st child: {rate_first} NIS/month")
    if num_children >= 2:
        middle = min(num_children - 1, 3)
        print(f"  2nd to {min(num_children, 4)}th child: {rate_middle} NIS/month each "
              f"({middle} child{'ren' if middle > 1 else ''})")
    if num_children >= 5:
        print(f"  5th+ child: {rate_high} NIS/month each ({num_children - 4} children)")
    print(f"Total monthly: {total_monthly:,.0f} NIS/month")
    print(f"Total annual: {total_annual:,.0f} NIS/year")
    print()
    print("Saving-for-every-child (חיסכון לכל ילד): 58 NIS/month per child "
          "auto-deposited; parents may match for 116 NIS total.")
    print("Payment date: ~20th of each month, to the registered parent.")
    print("Filing: usually automatic from hospital. Manual claim: form 5025.")


def calculate_miluim(salary: float, days: int, is_self_employed: bool = False) -> None:
    """Estimate reserve-duty compensation (tashlumei miluim)."""
    print("=== Reserve Duty (Miluim) Compensation Estimate, 2026 rates ===\n")

    # 2026 caps and floors (miluim cap = max insurable 51,910 ÷ 30)
    daily_cap = 1730.33
    daily_min = 328.76

    # Daily wage = last 3 months gross / 90 (or for self-employed, prior-year /90)
    daily_wage = salary * 3 / 90  # if salary is monthly, this gives daily

    daily_compensation = min(max(daily_wage, daily_min), daily_cap)
    total_compensation = daily_compensation * days

    print(f"Monthly salary (or self-employed monthly equivalent): {salary:,.0f} NIS")
    print(f"Days of miluim: {days}")
    print(f"Status: {'Self-employed' if is_self_employed else 'Salaried (or below cap)'}")
    print()
    print(f"Daily compensation: {daily_compensation:,.2f} NIS/day")
    print(f"  Cap: {daily_cap:,.2f} NIS/day (2026)")
    print(f"  Minimum: {daily_min:,.2f} NIS/day (2026)")
    print(f"Total estimated compensation: {total_compensation:,.0f} NIS")
    print()
    if is_self_employed:
        print("Self-employed: file personal claim form 502.")
        print("Calculation base: prior-year tax assessment ÷ 90.")
    else:
        print("Salaried: employer pays salary as usual; BTL refunds employer via "
              "form 501. The reservist receives full salary, no separate BTL "
              "payment.")
        print("Below-cap salaried may file form 502 personally for any gap.")
    print()
    print("Iron Swords annual bonus tiers apply for >10 cumulative miluim days "
          "in the year (~2,000-10,000+ NIS depending on tier).")
    print("Claim window: 7 years from end of service.")
    print("Form 509 for advance payment.")


def calculate_birth_grant(child_position: int, twins: bool = False) -> None:
    """Estimate one-time birth grant (ma'anak leida)."""
    print("=== Birth Grant (Ma'anak Leida) Estimate, 2026 rates ===\n")

    if twins:
        amount = 10514
        print(f"Twins: {amount:,.0f} NIS (one-time grant)")
    elif child_position == 1:
        amount = 2103
        print(f"First child: {amount:,.0f} NIS (one-time grant)")
    elif child_position == 2:
        amount = 946
        print(f"Second child: {amount:,.0f} NIS (one-time grant)")
    elif child_position >= 3:
        amount = 631
        print(f"Third+ child: {amount:,.0f} NIS (one-time grant)")
    else:
        print(f"Invalid child position: {child_position}")
        return

    print()
    print("Hospitalization grant (ma'anak ishpuz) is paid directly to the hospital.")
    print("Hospital normally files automatically when the mother provides bank "
          "details on admission.")
    print("Combined claim: form 356 (birth grant + maternity allowance together).")


def main():
    parser = argparse.ArgumentParser(
        description="Israeli Bituach Leumi Benefit Calculator (2026 rates)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Benefit type")

    # Pension
    pension_parser = subparsers.add_parser("pension", help="Old age pension estimate")
    pension_parser.add_argument("--age", type=int, required=True, help="Current age")
    pension_parser.add_argument("--status", choices=["single", "couple"],
                                default="single", help="Marital status")
    pension_parser.add_argument("--years", type=int, default=30,
                                help="Years of NI contributions")
    pension_parser.add_argument("--defer", type=int, default=0,
                                help="Years of deferred claiming")

    # Unemployment
    unemp_parser = subparsers.add_parser("unemployment", help="Unemployment estimate")
    unemp_parser.add_argument("--salary", type=float, required=True,
                              help="Last monthly salary (NIS)")
    unemp_parser.add_argument("--age", type=int, required=True, help="Current age")
    unemp_parser.add_argument("--months", type=int, required=True,
                              help="Months employed in last 18 months")
    unemp_parser.add_argument("--dependents", action="store_true",
                              help="Has dependents")

    # Maternity
    mat_parser = subparsers.add_parser("maternity", help="Maternity benefit estimate")
    mat_parser.add_argument("--salary", type=float, required=True,
                            help="Monthly salary (NIS)")
    mat_parser.add_argument("--months-employed", type=int, required=True,
                            help="Months employed before due date")

    # Child allowance
    child_parser = subparsers.add_parser("child-allowance", help="Child allowance estimate")
    child_parser.add_argument("--children", type=int, required=True,
                              help="Number of children under 18")

    # Miluim
    miluim_parser = subparsers.add_parser("miluim", help="Reserve duty estimate")
    miluim_parser.add_argument("--salary", type=float, required=True,
                               help="Monthly salary or self-employed monthly equivalent (NIS)")
    miluim_parser.add_argument("--days", type=int, required=True,
                               help="Number of miluim days")
    miluim_parser.add_argument("--self-employed", action="store_true",
                               help="Self-employed reservist")

    # Birth grant
    birth_parser = subparsers.add_parser("birth-grant", help="One-time birth grant estimate")
    birth_parser.add_argument("--child-position", type=int, default=1,
                              help="1 for first child, 2 for second, 3+ for third or later")
    birth_parser.add_argument("--twins", action="store_true",
                              help="Multiple birth (twins)")

    args = parser.parse_args()

    if args.command == "pension":
        calculate_pension(args.age, args.status, args.years, args.defer)
    elif args.command == "unemployment":
        calculate_unemployment(args.salary, args.age, args.months, args.dependents)
    elif args.command == "maternity":
        calculate_maternity(args.salary, args.months_employed)
    elif args.command == "child-allowance":
        calculate_child_allowance(args.children)
    elif args.command == "miluim":
        calculate_miluim(args.salary, args.days, args.self_employed)
    elif args.command == "birth-grant":
        calculate_birth_grant(args.child_position, args.twins)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
