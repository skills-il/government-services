#!/usr/bin/env python3
"""
Israeli Bituach Leumi (National Insurance) Benefit Calculator

Standalone utility for estimating Bituach Leumi benefit amounts including
old age pension, unemployment, maternity, child allowance, miluim, and
birth grant. All hardcoded amounts reflect 2026 official rates as published
in the January 2026 BTL benefits circular
(btl.gov.il/Publications/benefits_update/Documents/hozerkizba2026.pdf).

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
                      defer_years: int = 0, retirement_age: int = 67,
                      children: int = 0) -> None:
    """Estimate old age pension (kitzbat zikna)."""
    # 2026 base amounts
    base_single_under80 = 1838
    base_single_from80 = 1941
    base_couple = 2762

    print("=== Old Age Pension (Kitzbat Zikna) Estimate, 2026 rates ===\n")

    # Eligibility age. Men: 67. Women: 62 to 65 BY BIRTH YEAR (62 up to 1959, 63 for
    # 1962, 64 for 1966, and 65 only from birth-year 1970). This script does not take
    # a birth year, so it cannot decide eligibility for a woman: it warns instead.
    eligibility_age_men = 67

    if age < 62:
        print(f"Age {age}: Not yet eligible (the earliest retirement age is 62, "
              f"for women born up to 1959).")
        print("  Men are eligible at 67.")
        print("  Women: 62 to 65 by BIRTH YEAR (65 only from birth-year 1970). Check")
        print("  btl.gov.il/benefits/old_age/Pages/RetirementCalculation.aspx.")
        return

    if age < retirement_age:
        print(f"WARNING: at age {age} you have NOT reached the retirement age used here "
              f"({retirement_age}).")
        print("         Men: 67. Women: 62 to 65 BY BIRTH YEAR (65 only from 1970).")
        print("         Pass --retirement-age to set it. The figures below apply only")
        print("         once the retirement age is reached.\n")

    # The seniority supplement is 2% of the BASIC (individual) pension, and the spouse
    # and child increments are separate תוספות added ON TOP. So multiply the individual
    # rate by the seniority/deferral factors and add the increments flat, rather than
    # inflating the 924 spouse increment (which the couple headline rate 2,762 contains)
    # by the seniority factor.
    basic = base_single_from80 if age >= 80 else base_single_under80
    spouse_increment = 924 if status == "couple" else 0

    # Seniority supplement: 2% of the basic pension for EVERY full insured year,
    # counted from year ONE (BTL's own example: 15 insured years -> 30%). Capped at
    # 50%, which is reached at 25 years. It does NOT start at year 11.
    seniority_bonus = min(years_contributed * 0.02, 0.50)

    # Deferral bonus: +5% per year, paid up to age 70
    # Deferral is paid for years between RETIREMENT age and the eligibility age (70) in
    # which the pension was deferred because of work income. The cap is therefore
    # (70 - retirement age), NOT (70 - current age): a man retiring at 67 can defer at
    # most 3 years (+15%); a woman retiring at 62 can defer up to 8.
    max_defer_years = max(0, 70 - retirement_age)
    if defer_years > max_defer_years:
        print(f"NOTE: deferral is paid only between retirement age ({retirement_age}) "
              f"and 70, so the maximum here is {max_defer_years} year(s). "
              f"Capping {defer_years} -> {max_defer_years}.")
        defer_years = max_defer_years
    deferral_bonus = defer_years * 0.05

    # BTL levies the 5%/year deferral bonus on the FULL pension INCLUDING the seniority
    # supplement ("5% מסך הקצבה המלאה (כולל תוספת הוותק)"), so the two compound.
    child_supplement = 581 * min(children, 2)
    base = basic + spouse_increment  # headline rate before supplements (2,762 for a couple)
    estimated_monthly = basic * (1 + seniority_bonus) * (1 + deferral_bonus) \
        + spouse_increment + child_supplement

    print(f"Status: {status.title()}")
    print(f"Age: {age}")
    print(f"Years contributed: {years_contributed}")
    print(f"Deferral years: {defer_years}")
    print()
    print(f"Base amount (2026): {base:,.0f} NIS/month")
    print(f"Seniority bonus: +{seniority_bonus:.0%} ({years_contributed} insured years "
          "x 2%, counted from year one, capped at 50%)")
    print(f"Deferral bonus: +{deferral_bonus:.0%} ({defer_years} years, compounded on "
          f"the seniority-inflated pension)")
    if children:
        print(f"Child supplement: {child_supplement:,.0f} NIS "
              f"({min(children, 2)} child(ren) x 581, max 2)")
    print(f"Estimated monthly pension: {estimated_monthly:,.0f} NIS/month")
    print(f"Estimated annual pension: {estimated_monthly * 12:,.0f} NIS/year")
    print()
    print("NOTE: Most pensioners receive the full +50% seniority supplement, "
          "bringing the typical single rate to ~2,757 NIS.")
    print("NOTE: Between retirement age and 70 a GRADUATED work-income test applies.")
    print("      No spouse: full pension below 10,113 NIS/month; partial 10,113 to 14,402;")
    print("      none above 14,402. With a spouse: full below 13,484; partial to 20,082;")
    print("      none above 20,082. Pension income is NOT counted in this test.")
    print("Verify your specific case at btl.gov.il or call *6050.")
    print("Claim form: 480 (תביעה לקצבת אזרח ותיק).")


def calculate_unemployment(salary: float, age: int, months_employed: int,
                           has_dependents: bool = False,
                           is_woman_57_67_born_1960_plus: bool = False) -> None:
    """Estimate unemployment benefits (dmei avtala).

    has_dependents means 3 OR MORE dependent family members (spouse + children).
    """
    print("=== Unemployment Benefits (Dmei Avtala) Estimate, 2026 rates ===\n")

    if months_employed < 12:
        print(f"Months employed: {months_employed}")
        print("NOT ELIGIBLE: Minimum 12 months of employment in last 18 months required.")
        return

    # Maximum benefit days, per the official BTL/kolzchut table.
    # "Dependants" = 3 OR MORE dependent family members (spouse + children), not "any".
    if age < 25:
        duration_days = 138 if has_dependents else 50
    elif age < 28:
        duration_days = 138 if has_dependents else 67
    elif age < 35:
        duration_days = 138 if has_dependents else 100
    elif age < 45:
        duration_days = 175 if has_dependents else 138
    else:
        duration_days = 175  # 45+ is unconditional

    # Women aged 57-67 born 1960 or later get 300 days, usable over 18 months (not 12).
    if is_woman_57_67_born_1960_plus:
        if not 57 <= age <= 67:
            print(f"WARNING: --woman-57-67-born-1960-plus applies only at ages 57-67; "
                  f"age {age} is outside that range. Ignoring the flag.\n")
            is_woman_57_67_born_1960_plus = False
        else:
            duration_days = 300

    # 2026 caps (BTL: max 550.76/day for the first 125 payment days, 367.17/day from day 126)
    cap_first_period = 550.76
    cap_second_period = 367.17

    # Daily benefit is interpolated from BTL's OFFICIAL published tables
    # (btl.gov.il/benefits/Unemployment/Pages/sum.aspx, effective 01.01.2026).
    # BTL publishes TWO tables: the replacement rate is capped at 60% of the wage
    # for claimants under 28, and at 80% from age 28. Never apply one to the other.
    # Rows are (gross monthly salary, daily benefit).
    TABLE_UNDER_28 = [
        (3000, 72.0), (4000, 96.0), (5000, 120.0), (6000, 137.5), (7000, 153.5),
        (8000, 169.06), (9000, 183.06), (10000, 197.06), (12000, 218.56),
        (14000, 238.56), (16000, 258.56), (18000, 278.56), (20000, 298.56),
        (22000, 318.56), (24000, 338.56), (26000, 358.56), (28000, 378.56),
        (30000, 398.56), (32000, 418.56), (34000, 438.56), (36000, 458.56),
        (38000, 478.56), (40000, 498.56), (42000, 518.56), (45220, 550.76),
    ]
    TABLE_28_PLUS = [
        (3000, 96.0), (4000, 128.0), (5000, 160.0), (6000, 182.25), (7000, 202.25),
        (8000, 221.81), (9000, 239.81), (10000, 257.81), (11000, 272.06),
        (12000, 284.06), (13000, 296.06), (14000, 308.06), (15000, 320.06),
        (16000, 332.06), (17000, 344.06), (18000, 356.06), (19000, 368.06),
        (20000, 380.06), (21000, 392.06), (23000, 416.06), (25000, 440.06),
        (27000, 464.06), (29000, 488.06), (31000, 512.06), (33000, 536.06),
        (34225, 550.76),
    ]

    table = TABLE_UNDER_28 if age < 28 else TABLE_28_PLUS
    rate_ceiling = "60% of wage (under 28)" if age < 28 else "80% of wage (28+)"

    if salary <= table[0][0]:
        # Below the table's first row the ceiling rate applies directly.
        ceiling = 0.60 if age < 28 else 0.80
        first_rate = (salary / 25) * ceiling
    elif salary >= table[-1][0]:
        first_rate = cap_first_period
    else:
        first_rate = table[-1][1]
        for (s_lo, d_lo), (s_hi, d_hi) in zip(table, table[1:]):
            if s_lo <= salary <= s_hi:
                span = s_hi - s_lo
                first_rate = d_lo + (d_hi - d_lo) * ((salary - s_lo) / span if span else 0)
                break

    first_rate = min(first_rate, cap_first_period)

    first_period_days = min(125, duration_days)
    second_period_days = max(0, duration_days - 125)

    # 367.17 is a CAP from day 126, not a flat rate: a below-cap claimant keeps their own rate.
    second_rate = min(first_rate, cap_second_period)

    # Women 57-60 in the 300-day cohort have a FURTHER cap of 201.03/day from day 176.
    cap_third_period = 201.03
    third_period_days = 0
    third_rate = 0.0
    if is_woman_57_67_born_1960_plus and age < 60 and duration_days > 175:
        third_period_days = duration_days - 175
        third_rate = min(first_rate, cap_third_period)
        second_period_days = max(0, 175 - first_period_days)

    total_first = first_period_days * first_rate
    total_second = second_period_days * second_rate
    total_third = third_period_days * third_rate
    total_benefit = total_first + total_second + total_third

    waiting_days = 5

    print(f"Monthly salary: {salary:,.0f} NIS")
    print(f"Age: {age}")
    print(f"Has dependents: {'Yes' if has_dependents else 'No'}")
    print(f"Months employed: {months_employed}")
    print()
    print(f"Waiting period: {waiting_days} working days (terminations only; "
          "resignation triggers 90-day disqualification unless justified cause)")
    print(f"Benefit duration: {duration_days} days")
    if is_woman_57_67_born_1960_plus:
        print("      (women 57-67 born 1960+: 300 days, usable over 18 months, not 12)")
    print(f"Replacement-rate ceiling: {rate_ceiling}")
    print(f"First period ({first_period_days} days): {first_rate:,.2f} NIS/day "
          f"(cap {cap_first_period:,.2f} NIS/day)")
    if second_period_days > 0:
        print(f"Second period ({second_period_days} days): {second_rate:,.2f} NIS/day "
              f"(cap {cap_second_period:,.2f} NIS/day from day 126)")
    if third_period_days > 0:
        print(f"Third period ({third_period_days} days, from day 176): "
              f"{third_rate:,.2f} NIS/day (cap {cap_third_period:,.2f} NIS/day, "
              f"women 57-60)")
        print("      Refusing vocational training in the first 175 days: 90-day")
        print("      disqualification + 30 days struck off (300 -> 270).")
    print()
    print(f"Estimated total benefit: {total_benefit:,.0f} NIS")
    print(f"Estimated monthly equivalent: "
          f"{total_benefit / (duration_days / 25):,.0f} NIS/month")
    print()
    print("NOTE: Interpolated from the official BTL table at")
    print("      btl.gov.il/benefits/Unemployment/Pages/sum.aspx (01.01.2026).")
    print("      Actual amounts depend on precise salary history.")
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
        print(f"  2nd to 4th child (as applicable): {rate_middle} NIS/month each "
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
    print("Iron Swords annual bonus tiers add a grant that scales with cumulative")
    print("miluim days in the year. The tier table changes often: look it up at")
    print("btl.gov.il rather than relying on any figure quoted here.")
    print("Claim window: 7 years from end of service.")
    print("Form 509 for advance payment.")


def calculate_birth_grant(child_position: int, babies: int = 1) -> None:
    """Estimate one-time birth grant (ma'anak leida)."""
    print("=== Birth Grant (Ma'anak Leida) Estimate, 2026 rates ===\n")

    if babies >= 2:
        # Multiple births are BANDED: twins 10,514; triplets 15,771; +5,257 per extra baby.
        if babies == 2:
            amount = 10514
        else:
            amount = 15771 + 5257 * (babies - 3)
        print(f"Multiple birth ({babies} babies): {amount:,.0f} NIS (one-time grant)")
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
                                help="Years of deferred claiming (paid only between "
                                     "retirement age and 70)")
    pension_parser.add_argument("--retirement-age", type=int, default=67,
                                dest="retirement_age",
                                help="67 for men; for women 62-65 BY BIRTH YEAR "
                                     "(65 only from birth-year 1970)")
    pension_parser.add_argument("--children", type=int, default=0,
                                help="Dependent children (581 NIS each, max 2)")

    # Unemployment
    unemp_parser = subparsers.add_parser("unemployment", help="Unemployment estimate")
    unemp_parser.add_argument("--salary", type=float, required=True,
                              help="Last monthly salary (NIS)")
    unemp_parser.add_argument("--age", type=int, required=True, help="Current age")
    unemp_parser.add_argument("--months", type=int, required=True,
                              help="Months employed in last 18 months")
    unemp_parser.add_argument("--dependents", action="store_true",
                              help="3 OR MORE dependent family members (spouse + "
                                   "children). Do NOT set this for 1-2 dependants.")
    unemp_parser.add_argument("--woman-57-67-born-1960-plus", action="store_true",
                              dest="woman_57_67",
                              help="Woman aged 57-67 born in 1960 or later: 300 "
                                   "benefit days, usable over 18 months (not 12)")

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
    birth_parser.add_argument("--babies", type=int, default=1,
                              help="Babies in this birth: 2 = twins (10,514), "
                                   "3 = triplets (15,771), +5,257 for each beyond")

    args = parser.parse_args()

    if args.command == "pension":
        calculate_pension(args.age, args.status, args.years, args.defer,
                          args.retirement_age, args.children)
    elif args.command == "unemployment":
        calculate_unemployment(args.salary, args.age, args.months, args.dependents,
                               args.woman_57_67)
    elif args.command == "maternity":
        calculate_maternity(args.salary, args.months_employed)
    elif args.command == "child-allowance":
        calculate_child_allowance(args.children)
    elif args.command == "miluim":
        calculate_miluim(args.salary, args.days, args.self_employed)
    elif args.command == "birth-grant":
        calculate_birth_grant(args.child_position, args.babies)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
