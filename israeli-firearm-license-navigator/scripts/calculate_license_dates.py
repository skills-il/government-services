#!/usr/bin/env python3
"""Compute the clocks of the Israeli private firearm license process.

Give one or more anchor dates and the script prints every deadline that
follows from them, with the source of each rule. Stdlib only.

Rules encoded (verification date 14.09.2026):
  * Conditional approval (ishur mutne) is valid 6 months
    (Knesset Research and Information Center, 13.02.2024).
  * Theory exam pass is valid 3 months from the training date (gov.il).
  * License is valid 3 years (gov.il).
  * Refresher training happens in year 2; reminder at the start of year 2 (gov.il).
  * Renewal window opens 3 months before expiry and closes at expiry (gov.il).
  * Late renewal surcharge tiers (gov.il fee page, updated 04.01.2026):
      up to 6 months: one annual fee; 6 to 12 months: three annual fees;
      over 12 months: four annual fees per year of delay or part of it.
  * Missed refresher: deposit at a dealer within 72 hours of notice (gov.il).
  * Emergency extension of 23.04.2026: refreshers and renewals due
    31.3.2026, 30.4.2026, 31.5.2026 extended to 30.6.2026, 31.7.2026, 31.8.2026.
    When an extension applies, the extended date is the effective deadline and
    the late-renewal delay is measured from it.
  * Appeal: 45 days from receipt of the refusal or cancellation (Law s.12(c1)).
  * Loss or theft: report to police within 48 hours (Law s.15(a)).

Usage:
  python calculate_license_dates.py --conditional-approval 2026-09-14
  python calculate_license_dates.py --license-issued 2024-03-01 --today 2026-09-14
  python calculate_license_dates.py --license-expires 2026-07-31 --today 2026-09-14 --json
  python calculate_license_dates.py --refusal-received 2026-09-01 --lang he
  python calculate_license_dates.py --help
"""

import argparse
import calendar
import datetime as dt
import json
import sys

ANNUAL_FEE_DEFAULT = 71  # NIS, gov.il fee table updated 04.01.2026

EXTENSIONS_2026 = {
    dt.date(2026, 3, 31): dt.date(2026, 6, 30),
    dt.date(2026, 4, 30): dt.date(2026, 7, 31),
    dt.date(2026, 5, 31): dt.date(2026, 8, 31),
}

LABELS = {
    "conditional_expires": {
        "en": "conditional approval expires",
        "he": "האישור המותנה פג",
    },
    "theory_expires": {
        "en": "theory exam pass expires",
        "he": "המבחן העיוני פג",
    },
    "card_expected": {
        "en": "magnetic card expected by",
        "he": "הכרטיס המגנטי צפוי עד",
    },
    "refresher_opens": {
        "en": "refresher window opens (year 2 starts, reminder sent)",
        "he": "חלון הריענון נפתח (תחילת שנה שנייה, נשלחת תזכורת)",
    },
    "refresher_closes": {
        "en": "refresher window closes (year 2 ends)",
        "he": "חלון הריענון נסגר (סוף שנה שנייה)",
    },
    "renewal_opens": {
        "en": "renewal window opens (3 months before expiry)",
        "he": "חלון החידוש נפתח (3 חודשים לפני הפקיעה)",
    },
    "license_expires": {
        "en": "license expires (renewal must be complete)",
        "he": "הרישיון פג (החידוש חייב להסתיים)",
    },
    "deposit_deadline": {
        "en": "deposit at a licensed dealer by (72 hours after notice)",
        "he": "הפקדה אצל סוחר מורשה עד (72 שעות מההודעה)",
    },
    "appeal_deadline": {
        "en": "appeal deadline (45 days from receipt)",
        "he": "מועד אחרון לערר (45 יום מהקבלה)",
    },
    "police_report": {
        "en": "police report deadline (48 hours)",
        "he": "מועד אחרון לדיווח למשטרה (48 שעות)",
    },
    "official_report": {
        "en": "licensing official report (72 hours, department procedure)",
        "he": "דיווח לפקיד הרישוי (72 שעות, נוהל האגף)",
    },
}

SOURCES = {
    "conditional_expires": {
        "en": "Knesset RIC review 13.02.2024: valid half a year; read the date on the document itself",
        "he": "סקירת מרכז המחקר של הכנסת 13.02.2024: תוקף חצי שנה; קראו את התאריך שעל המסמך עצמו",
    },
    "theory_expires": {
        "en": "gov.il training guide: theory pass valid 3 months from the training date",
        "he": "מדריך ההכשרות ב-gov.il: המבחן העיוני תקף 3 חודשים מיום ההכשרה",
    },
    "card_expected": {
        "en": "gov.il: magnetic license sent within 90 days of the ownership transfer",
        "he": "gov.il: הרישיון המגנטי נשלח בתוך 90 יום מהעברת הבעלות",
    },
    "refresher_opens": {
        "en": "gov.il refresher page: training in the second year of the license period",
        "he": "דף הריענון ב-gov.il: ההכשרה בשנה השנייה לתקופת הרישיון",
    },
    "refresher_closes": {
        "en": "gov.il refresher page; a missed refresher means deposit at a dealer within 72 hours of notice",
        "he": "דף הריענון ב-gov.il; ריענון שפוספס מחייב הפקדה אצל סוחר בתוך 72 שעות מההודעה",
    },
    "renewal_opens": {
        "en": "gov.il renewal page: reminder from 3 months before expiry",
        "he": "דף החידוש ב-gov.il: תזכורת משלושה חודשים לפני הפקיעה",
    },
    "license_expires": {
        "en": "gov.il: license valid 3 years; renewal is the holder's responsibility",
        "he": "gov.il: הרישיון תקף 3 שנים; החידוש באחריות בעל הרישיון",
    },
    "deposit_deadline": {
        "en": "gov.il: missed refresher, deposit within 72 hours of the licensing official's notice or the license is cancelled",
        "he": "gov.il: ריענון שפוספס, הפקדה בתוך 72 שעות מהודעת פקיד הרישוי אחרת הרישיון מבוטל",
    },
    "appeal_deadline": {
        "en": "Firearms Law s.12(c1) and gov.il appeal page: written appeal within 45 days of receiving the decision",
        "he": "סעיף 12(ג1) לחוק כלי הירייה ודף הערר ב-gov.il: ערר בכתב בתוך 45 יום מקבלת ההחלטה",
    },
    "police_report": {
        "en": "Firearms Law s.15(a): notify a police station no later than 48 hours after learning of the loss or theft",
        "he": "סעיף 15(א) לחוק כלי הירייה: הודעה לתחנת משטרה לא יאוחר מ-48 שעות מרגע שנודע על האובדן או הגניבה",
    },
    "official_report": {
        "en": "Department procedure 12.02.32 (2014): report to the licensing official within 72 hours",
        "he": "נוהל האגף 12.02.32 (2014): דיווח לפקיד הרישוי בתוך 72 שעות",
    },
}

TEXT = {
    "today": {"en": "Today", "he": "היום"},
    "clock": {"en": "Clock", "he": "שעון"},
    "date": {"en": "Date", "he": "תאריך"},
    "days": {"en": "Days", "he": "ימים"},
    "past": {"en": "past", "he": "עבר"},
    "extended": {"en": "extended to", "he": "הוארך עד"},
    "days_note": {
        "en": "Days: positive = days from today; negative = days ago.",
        "he": "ימים: חיובי = ימים מהיום; שלילי = ימים שעברו.",
    },
    "sources": {"en": "Sources", "he": "מקורות"},
    "late": {"en": "Late renewal", "he": "חידוש באיחור"},
    "months_late": {"en": "months late", "he": "חודשי איחור"},
    "measured_from": {"en": "measured from", "he": "נמדד מ"},
    "tier": {"en": "tier", "he": "מדרגה"},
    "surcharge": {"en": "surcharge", "he": "תוספת"},
    "surcharge_tail": {
        "en": "NIS on top of the renewal fee ({fee} NIS per year, up to 3 years)",
        "he": "ש\"ח מעבר לאגרת החידוש ({fee} ש\"ח לשנה, עד 3 שנים)",
    },
    "rule": {"en": "rule", "he": "כלל"},
    "late_rule": {
        "en": "gov.il fee page: deposit the firearm at the police immediately; surcharge added to the renewal fee",
        "he": "דף האגרות ב-gov.il: הפקידו את הכלי במשטרה מיד; התוספת נוספת לאגרת החידוש",
    },
    "notes": {"en": "Notes", "he": "הערות"},
    "footer": {
        "en": "Verification date of the rules: 14.09.2026. Confirm any figure on gov.il before acting.",
        "he": "תאריך אימות הכללים: 14.09.2026. אמתו כל נתון ב-gov.il לפני שפועלים.",
    },
    "note_conditional": {
        "en": "Inside these 6 months: pay the fee, train at an authorised range, buy the firearm, and register the transfer. "
              "The theory pass will be valid 3 months from the training date; give --training-date to compute it.",
        "he": "בתוך ששת החודשים: לשלם אגרה, לעבור הכשרה במטווח מורשה, לרכוש את הכלי ולרשום את ההעברה. "
              "המבחן העיוני יהיה תקף 3 חודשים מיום ההכשרה; תנו --training-date כדי לחשב אותו.",
    },
    "note_extension": {
        "en": "Emergency extension of 23.04.2026 applies to a date above: deadlines due 31.3, 30.4 and 31.5.2026 were extended to "
              "30.6, 31.7 and 31.8.2026 respectively. The extended date is used as the effective deadline. Confirm on gov.il news.",
        "he": "הארכת החירום מ-23.04.2026 חלה על תאריך למעלה: מועדים שחלו ב-31.3, 30.4 ו-31.5.2026 הוארכו ל-30.6, 31.7 ו-31.8.2026 "
              "בהתאמה. התאריך המוארך משמש כמועד הקובע. אמתו בדף החדשות של gov.il.",
    },
    "note_expired": {
        "en": "The license has expired. gov.il: holding a firearm without a valid license is a criminal offence; "
              "deposit it at the Israel Police immediately, then renew with the surcharge.",
        "he": "הרישיון פג. gov.il: החזקת כלי ירייה ללא רישיון בתוקף היא עבירה פלילית; הפקידו אותו במשטרת ישראל מיד ואז חדשו עם התוספת.",
    },
    "note_refresher_past": {
        "en": "The year-2 refresher window is in the past. Ask whether the refresher was completed; if not, the license may already "
              "have been cancelled under the 72-hour deposit rule, and the service center should confirm the status.",
        "he": "חלון הריענון של השנה השנייה עבר. שאלו אם הריענון בוצע; אם לא, ייתכן שהרישיון כבר בוטל לפי כלל 72 השעות, "
              "ומרכז השירות צריך לאשר את הסטטוס.",
    },
    "tier_not_late": {"en": "not late", "he": "לא באיחור"},
    "tier_1": {"en": "up to 6 months: one annual fee", "he": "עד 6 חודשים: אגרה שנתית אחת"},
    "tier_2": {"en": "6 to 12 months: three annual fees", "he": "6 עד 12 חודשים: שלוש אגרות שנתיות"},
    "tier_3": {
        "en": "over 12 months: four annual fees per year of delay or part ({years} year(s))",
        "he": "מעל 12 חודשים: ארבע אגרות שנתיות לכל שנת איחור או חלק ממנה ({years} שנים)",
    },
}


def add_months(d: dt.date, months: int) -> dt.date:
    """Add calendar months, clamping the day to the target month length."""
    month_index = d.month - 1 + months
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return dt.date(year, month, day)


def add_years(d: dt.date, years: int) -> dt.date:
    return add_months(d, 12 * years)


def parse_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a date in YYYY-MM-DD form")


def months_between(start: dt.date, end: dt.date) -> float:
    """Approximate months between two dates, whole months plus a day fraction."""
    whole = (end.year - start.year) * 12 + (end.month - start.month)
    anchor = add_months(start, whole)
    if anchor > end:
        whole -= 1
        anchor = add_months(start, whole)
    days_in_month = calendar.monthrange(anchor.year, anchor.month)[1]
    return whole + (end - anchor).days / days_in_month


def surcharge(delay_months: float, annual_fee: int, lang: str):
    """Return (tier label, surcharge in NIS) for a late renewal."""
    if delay_months <= 0:
        return TEXT["tier_not_late"][lang], 0
    if delay_months <= 6:
        return TEXT["tier_1"][lang], annual_fee
    if delay_months <= 12:
        return TEXT["tier_2"][lang], 3 * annual_fee
    years_of_delay = int(delay_months // 12) + (1 if delay_months % 12 > 0 else 0)
    return TEXT["tier_3"][lang].format(years=years_of_delay), 4 * annual_fee * years_of_delay


def fmt(d: dt.date) -> str:
    return d.strftime("%d.%m.%Y")


def build(args) -> dict:
    lang = args.lang
    today = args.today or dt.date.today()
    out = {"today": today.isoformat(), "lang": lang, "clocks": [], "notes": []}

    def clock(key, date, extended=None):
        effective = extended or date
        item = {
            "key": key,
            "clock": LABELS[key][lang],
            "date": date.isoformat(),
            "effective_date": effective.isoformat(),
            "days_from_today": (effective - today).days,
            "source": SOURCES[key][lang],
        }
        if extended:
            item["extended_to"] = extended.isoformat()
        out["clocks"].append(item)
        return effective

    if args.conditional_approval:
        clock("conditional_expires", add_months(args.conditional_approval, 6))
        out["notes"].append(TEXT["note_conditional"][lang])

    training = args.training_date or args.theory_exam
    if training:
        clock("theory_expires", add_months(training, 3))

    if args.transfer_date:
        clock("card_expected", args.transfer_date + dt.timedelta(days=90))

    expiry = None
    issued = None
    if args.license_issued:
        issued = args.license_issued
        expiry = add_years(issued, 3)
    if args.license_expires:
        expiry = args.license_expires
        if issued is None:
            issued = add_years(expiry, -3)

    if issued and expiry:
        year2_start = add_years(issued, 1)
        year2_end = add_years(issued, 2)
        clock("refresher_opens", year2_start)
        refresher_effective = clock("refresher_closes", year2_end, EXTENSIONS_2026.get(year2_end))
        clock("renewal_opens", add_months(expiry, -3))
        effective_expiry = clock("license_expires", expiry, EXTENSIONS_2026.get(expiry))
        if expiry in EXTENSIONS_2026 or year2_end in EXTENSIONS_2026:
            out["notes"].append(TEXT["note_extension"][lang])
        if today > refresher_effective and today <= effective_expiry:
            out["notes"].append(TEXT["note_refresher_past"][lang])
        if today > effective_expiry:
            delay = months_between(effective_expiry, today)
            tier, amount = surcharge(delay, args.annual_fee, lang)
            out["late_renewal"] = {
                "months_late": round(delay, 1),
                "measured_from": effective_expiry.isoformat(),
                "tier": tier,
                "surcharge_nis": amount,
                "renewal_fee_nis_per_year": args.annual_fee,
                "rule": TEXT["late_rule"][lang],
            }
            out["notes"].append(TEXT["note_expired"][lang])
            out["notes"].append(TEXT["note_refresher_past"][lang])

    if args.refresher_notice:
        clock("deposit_deadline", args.refresher_notice + dt.timedelta(days=3))

    if args.refusal_received:
        clock("appeal_deadline", args.refusal_received + dt.timedelta(days=45))

    if args.loss_discovered:
        clock("police_report", args.loss_discovered + dt.timedelta(days=2))
        clock("official_report", args.loss_discovered + dt.timedelta(days=3))

    if not out["clocks"]:
        raise SystemExit("Give at least one anchor date. Run with --help for the options.")

    out["clocks"].sort(key=lambda c: c["effective_date"])
    return out


def print_text(result: dict) -> None:
    lang = result["lang"]
    t = lambda k: TEXT[k][lang]  # noqa: E731
    today = dt.date.fromisoformat(result["today"])
    print(f"{t('today')}: {fmt(today)}")
    print(t("days_note"))
    print()
    print(f"{t('clock'):<58} {t('date'):<12} {t('days'):>6}  ")
    print("-" * 80)
    for c in result["clocks"]:
        eff = dt.date.fromisoformat(c["effective_date"])
        days = c["days_from_today"]
        flag = f"  ({t('past')})" if days < 0 else ""
        print(f"{c['clock']:<58} {fmt(eff):<12} {days:>6}{flag}")
        if c.get("extended_to"):
            orig = dt.date.fromisoformat(c["date"])
            print(f"    {t('extended')} {fmt(eff)}; {'original' if lang == 'en' else 'מקורי'} {fmt(orig)}")
    print()
    print(f"{t('sources')}:")
    for c in result["clocks"]:
        print(f"  * {c['clock']}: {c['source']}")
    if "late_renewal" in result:
        lr = result["late_renewal"]
        print()
        print(f"{t('late')}:")
        print(f"  {t('months_late')}: {lr['months_late']} ({t('measured_from')} {fmt(dt.date.fromisoformat(lr['measured_from']))})")
        print(f"  {t('tier')}: {lr['tier']}")
        print(f"  {t('surcharge')}: {lr['surcharge_nis']} " + t("surcharge_tail").format(fee=lr["renewal_fee_nis_per_year"]))
        print(f"  {t('rule')}: {lr['rule']}")
    if result["notes"]:
        print()
        print(f"{t('notes')}:")
        for n in result["notes"]:
            print(f"  * {n}")
    print()
    print(t("footer"))


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    p = argparse.ArgumentParser(
        description="Compute Israeli private firearm license deadlines from anchor dates.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --conditional-approval 2026-09-14\n"
            "  %(prog)s --license-issued 2024-03-01 --today 2026-09-14\n"
            "  %(prog)s --license-expires 2026-07-31 --today 2026-09-14 --json\n"
            "  %(prog)s --refusal-received 2026-09-01 --lang he\n"
        ),
    )
    p.add_argument("--conditional-approval", type=parse_date, help="date printed on the ishur mutne (YYYY-MM-DD)")
    p.add_argument("--training-date", type=parse_date, help="date of the range training; the theory pass runs 3 months from it")
    p.add_argument("--theory-exam", type=parse_date, help="alias of --training-date")
    p.add_argument("--transfer-date", type=parse_date, help="date of the ownership transfer (purchase)")
    p.add_argument("--license-issued", type=parse_date, help="date the 3-year license was issued")
    p.add_argument("--license-expires", type=parse_date, help="expiry date printed on the license")
    p.add_argument("--refresher-notice", type=parse_date, help="date the official's notice of a missed refresher was received")
    p.add_argument("--refusal-received", type=parse_date, help="date the refusal or cancellation letter was received")
    p.add_argument("--loss-discovered", type=parse_date, help="date the holder learned of loss or theft")
    p.add_argument("--today", type=parse_date, help="override today's date (YYYY-MM-DD)")
    p.add_argument("--annual-fee", type=int, default=ANNUAL_FEE_DEFAULT,
                   help=f"annual license fee in NIS for the surcharge tiers (default {ANNUAL_FEE_DEFAULT}, gov.il 04.01.2026)")
    p.add_argument("--lang", choices=["en", "he"], default="en", help="output language (default en)")
    p.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = p.parse_args(argv)

    result = build(args)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
