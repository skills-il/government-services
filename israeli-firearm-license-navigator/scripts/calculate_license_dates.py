#!/usr/bin/env python3
"""Compute the clocks of the Israeli private firearm license process.

Give one or more anchor dates and the script prints every deadline that
follows from them, with the source of each rule. Stdlib only.

Rules encoded (verification date 28.09.2026):
  * Conditional approval (ishur mutne): the date on the document prevails. With
    only the issue date the script shows an ESTIMATE of 6 months, the validity
    reported by the Knesset Research and Information Center (13.02.2024);
    gov.il does not publish the value.
  * Theory exam pass is valid 3 months from the training date (gov.il).
  * License is valid 3 years (gov.il; validity regs reg. 3(b)(2)).
  * Refresher training happens in year 2; reminder at the start of year 2 (gov.il).
  * Renewal happens in year 3 and must be complete before expiry; gov.il sends
    a reminder from 3 months before expiry (it does not say renewal cannot
    start earlier).
  * Reservist extension: 30 or more reserve days in the 90 days before the
    license expiry extend the license once by 6 months (Firearms (Validity of
    Licenses) Regulations, reg. 4A); the same rule extends a refresher deadline
    (Firearms (Training) Regulations, reg. 3A). Pass --reservist-expiry and
    --reservist-refresher. While the answer is unknown, or a temporary order
    moved the deadline (the regulations do not say whether reg. 4A then counts
    from the original or the extended date), the script reports the period up
    to the latest possible date as "uncertain": no surcharge, no offence note.
  * Past wartime temporary orders (HISTORY; no later order found as of 28.09.2026):
    - 2023/2024 regulations (validity and training temporary orders): deadlines
      falling in 26.10.2023 (training: 31.10.2023) to 31.12.2023 and in
      31.01.2024 (training: 01.01.2024) to 31.03.2024 were extended "as follows";
      the texts give an extended date only for each month-end (31.10.2023 to
      30.04.2024 ... 31.03.2024 to 30.09.2024).
    - 2025 ("Am KeLavi", gov.il): 30.6.2025 and 31.7.2025 moved to 30.9.2025 and
      31.10.2025. 2026 (gov.il): 31.3, 30.4 and 31.5.2026 moved to 30.6, 31.7
      and 31.8.2026. The gov.il texts name month-end dates only.
    A deadline on a named date is treated as extended. Any other date inside a
    covered period (2023/2024) or covered month (2025/2026) is "possibly
    covered" and never charged a surcharge or called an offence while the
    possible extension runs.
  * After expiry: deposit the firearm, license and ammunition at the police
    within 72 hours (criteria regs, reg. 9(a)); a renewal request after expiry
    counts as a new application (reg. 8); the official may renew an expired
    license if the request came within 30 days of expiry (validity regs, reg. 5).
  * Late renewal surcharge tiers (gov.il fee page, updated 04.01.2026):
      up to 6 months: one annual fee; 6 to 12 months: three annual fees;
      over 12 months: four annual fees per year of delay or part of it.
  * Missed refresher: deposit at a dealer within 72 hours of notice (gov.il).
  * Appeal: 45 days from receipt of the refusal or cancellation (Law s.12(c1)).
  * Loss or theft: notify the Israel Police no later than 48 hours after the
    loss, destruction or theft itself (Law s.15(a)). The defence in s.15(a)
    needs BOTH a report within 48 hours of learning of it AND reasonable
    holding conditions. Department procedure 12.02.32 (2014): report to the
    licensing official within 72 hours.

Usage:
  python3 calculate_license_dates.py --conditional-approval 2026-09-14
  python3 calculate_license_dates.py --license-issued 2024-03-01 --today 2026-09-14
  python3 calculate_license_dates.py --license-expires 2026-07-31 --today 2026-09-28 --json
  python3 calculate_license_dates.py --license-expires 2026-07-31 --reservist-expiry yes
  python3 calculate_license_dates.py --loss-date 2026-09-27 --loss-discovered 2026-09-28
  python3 calculate_license_dates.py --refusal-received 2026-09-01 --lang he
  python3 calculate_license_dates.py --help
"""

import argparse
import calendar
import datetime as dt
import json
import sys

ANNUAL_FEE_DEFAULT = 71  # NIS, gov.il fee table updated 04.01.2026

# Past wartime temporary orders. HISTORY ONLY: the last extended deadline was
# 31.8.2026 and no later order was found as of 28.09.2026.
# Each entry: (applies_to, covered_from, covered_to, {named date: extended date},
# year label, kind). kind "period": the regulation text defines the covered
# period and names an extended date only for each month-end (validity and
# training temporary orders 5784-2023 and 5784-2024, Wikisource). kind "month":
# the gov.il notice names only the month-end dates; the rest of that month is
# treated as possibly covered (gov.il news 30.06.2025 / 14.07.2025, 23.04.2026).
D = dt.date
HISTORICAL_ORDERS = [
    ("license", D(2023, 10, 26), D(2023, 12, 31),
     {D(2023, 10, 31): D(2024, 4, 30), D(2023, 11, 30): D(2024, 5, 31), D(2023, 12, 31): D(2024, 6, 30)},
     "2023", "period"),
    ("refresher", D(2023, 10, 31), D(2023, 12, 31),
     {D(2023, 10, 31): D(2024, 4, 30), D(2023, 11, 30): D(2024, 5, 31), D(2023, 12, 31): D(2024, 6, 30)},
     "2023", "period"),
    ("license", D(2024, 1, 31), D(2024, 3, 31),
     {D(2024, 1, 31): D(2024, 7, 31), D(2024, 2, 29): D(2024, 8, 31), D(2024, 3, 31): D(2024, 9, 30)},
     "2024", "period"),
    ("refresher", D(2024, 1, 1), D(2024, 3, 31),
     {D(2024, 1, 31): D(2024, 7, 31), D(2024, 2, 29): D(2024, 8, 31), D(2024, 3, 31): D(2024, 9, 30)},
     "2024", "period"),
    ("both", D(2025, 6, 1), D(2025, 7, 31),
     {D(2025, 6, 30): D(2025, 9, 30), D(2025, 7, 31): D(2025, 10, 31)},
     "2025", "month"),
    ("both", D(2026, 3, 1), D(2026, 5, 31),
     {D(2026, 3, 31): D(2026, 6, 30), D(2026, 4, 30): D(2026, 7, 31), D(2026, 5, 31): D(2026, 8, 31)},
     "2026", "month"),
]

RESERVIST_MONTHS = 6  # validity regs reg. 4A; training regs reg. 3A


LABELS = {
    "conditional_expires": {
        "en": "conditional approval expires (date printed on it)",
        "he": "האישור המותנה פג (התאריך שמודפס עליו)",
    },
    "conditional_estimate": {
        "en": "conditional approval: ESTIMATED expiry (read the document)",
        "he": "אישור מותנה: פקיעה משוערת (קראו את המסמך)",
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
        "en": "renewal reminder sent (3 months before expiry; renew in year 3)",
        "he": "נשלחת תזכורת לחידוש (3 חודשים לפני הפקיעה; מחדשים בשנה השלישית)",
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
        "en": "police report deadline (48 hours after the loss itself)",
        "he": "מועד אחרון לדיווח למשטרה (48 שעות מהאובדן עצמו)",
    },
    "police_report_learned": {
        "en": "48 hours from learning of it (defence limb, 2014 procedure)",
        "he": "48 שעות מרגע שנודע (רכיב בהגנה, נוהל 2014)",
    },
    "official_report": {
        "en": "licensing official report (72 hours, department procedure)",
        "he": "דיווח לפקיד הרישוי (72 שעות, נוהל האגף)",
    },
    "license_possible": {
        "en": "latest date the license may still be valid (unconfirmed)",
        "he": "המועד המאוחר ביותר שבו הרישיון אולי עדיין בתוקף (לא מאושר)",
    },
    "refresher_possible": {
        "en": "latest possible refresher deadline (unconfirmed)",
        "he": "המועד המאוחר ביותר האפשרי לריענון (לא מאושר)",
    },
    "deposit_if_no_extension": {
        "en": "IF no extension applies: police deposit was due (72h after expiry)",
        "he": "אם לא חלה הארכה: מועד ההפקדה במשטרה (72 שעות מהפקיעה)",
    },
    "deposit_after_expiry": {
        "en": "deposit firearm, license, ammunition at police (72h after expiry)",
        "he": "הפקדת הכלי, הרישיון והתחמושת במשטרה (72 שעות מהפקיעה)",
    },
    "late_request": {
        "en": "last day to ask for renewal of an expired license (30 days)",
        "he": "יום אחרון לבקש חידוש של רישיון שפקע (30 יום)",
    },
    "late_request_if_extension": {
        "en": "IF an extension applied: last day to ask for renewal (30 days after the extended date)",
        "he": "אם חלה הארכה: יום אחרון לבקש חידוש (30 יום מהמועד המוארך)",
    },
    "late_request_if_no_extension": {
        "en": "IF no extension applies: last day to ask for renewal (30 days after expiry)",
        "he": "אם לא חלה הארכה: יום אחרון לבקש חידוש (30 יום מהפקיעה)",
    },
}

SOURCES = {
    "conditional_expires": {
        "en": "the date printed on the conditional approval itself",
        "he": "התאריך שמודפס על האישור המותנה עצמו",
    },
    "conditional_estimate": {
        "en": "estimate only: the Knesset RIC review (13.02.2024) reported a validity of half a year; gov.il does not publish it and a 2023 temporary order extended some approvals, so the date on the document prevails",
        "he": "הערכה בלבד: סקירת מרכז המחקר של הכנסת (13.02.2024) דיווחה על תוקף של חצי שנה; gov.il לא מפרסם את הערך והוראת שעה ב-2023 האריכה חלק מהאישורים, ולכן התאריך שעל המסמך קובע",
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
        "en": "gov.il renewal page: renewal in year 3; a reminder is sent from 3 months before expiry",
        "he": "דף החידוש ב-gov.il: החידוש בשנה השלישית; תזכורת נשלחת החל משלושה חודשים לפני הפקיעה",
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
        "en": "Firearms Law s.15(a): notify the Israel Police as early as possible and no later than 48 hours after the loss, destruction or theft",
        "he": "סעיף 15(א) לחוק כלי הירייה: הודעה למשטרת ישראל ככל המוקדם ולא יאוחר מ-48 שעות לאחר האבידה, ההשמדה או הגניבה",
    },
    "police_report_learned": {
        "en": "Law s.15(a)(1)-(2): no criminal liability only if BOTH the report came within 48 hours of learning of it AND the firearm was held in reasonable conditions; procedure 12.02.32 (2014) also counts from learning",
        "he": "סעיף 15(א)(1)-(2) לחוק: פטור מאחריות פלילית רק אם גם הדיווח נמסר בתוך 48 שעות מרגע שנודע וגם הכלי הוחזק בתנאים סבירים; גם נוהל 12.02.32 (2014) סופר מרגע שנודע",
    },
    "official_report": {
        "en": "Department procedure 12.02.32 (2014): report to the licensing official within 72 hours",
        "he": "נוהל האגף 12.02.32 (2014): דיווח לפקיד הרישוי בתוך 72 שעות",
    },
    "license_possible": {
        "en": "an extension that may apply but is not confirmed (reservist reg. 4A, a past temporary order, or both); confirm with the service center (*8657)",
        "he": "הארכה שאולי חלה אך אינה מאושרת (מילואים לפי תקנה 4א, הוראת שעה קודמת, או שתיהן); אמתו מול מרכז השירות (*8657)",
    },
    "refresher_possible": {
        "en": "an extension of the refresher deadline that may apply but is not confirmed (training regs reg. 3A, a past temporary order, or both)",
        "he": "הארכה של מועד הריענון שאולי חלה אך אינה מאושרת (תקנה 3א לתקנות ההכשרה, הוראת שעה קודמת, או שתיהן)",
    },
    "deposit_if_no_extension": {
        "en": "Criteria regs reg. 9(a): 72 hours from expiry; applies only if no extension kept the license valid",
        "he": "תקנה 9(א) לתקנות התבחינים: 72 שעות מהפקיעה; חל רק אם שום הארכה לא השאירה את הרישיון בתוקף",
    },
    "deposit_after_expiry": {
        "en": "Criteria regs reg. 9(a): deposit within 72 hours of expiry, at the police station of residence or business, against a receipt (Law s.14); non-deposit lets the official refuse renewal (reg. 9(b))",
        "he": "תקנה 9(א) לתקנות התבחינים: הפקדה בתוך 72 שעות מהפקיעה, בתחנת המשטרה של מקום המגורים או העסק, תמורת אישור קבלה (סעיף 14 לחוק); אי-הפקדה מאפשרת לדחות את בקשת החידוש (תקנה 9(ב))",
    },
    "late_request": {
        "en": "Validity regs reg. 5: the official may renew an expired license if persuaded it is justified and the request came within 30 days of expiry",
        "he": "תקנה 5 לתקנות תוקפם של רישיונות: פקיד הרישוי רשאי לחדש רישיון שפקע אם שוכנע שהדבר מוצדק והבקשה הוגשה בתוך 30 יום מהפקיעה",
    },
    "late_request_if_extension": {
        "en": "Validity regs reg. 5 counts 30 days from expiry; if an unconfirmed extension applied, expiry is the extended date",
        "he": "תקנה 5 לתקנות תוקפם של רישיונות סופרת 30 יום מהפקיעה; אם חלה הארכה שאינה מאושרת, הפקיעה היא המועד המוארך",
    },
    "late_request_if_no_extension": {
        "en": "Validity regs reg. 5: renewal of an expired license only if the request came within 30 days of expiry; applies only if no extension kept the license valid",
        "he": "תקנה 5 לתקנות תוקפם של רישיונות: חידוש רישיון שפקע רק אם הבקשה הוגשה בתוך 30 יום מהפקיעה; חל רק אם שום הארכה לא השאירה את הרישיון בתוקף",
    },
}

TEXT = {
    "today": {"en": "Today", "he": "היום"},
    "status": {"en": "License status", "he": "מצב הרישיון"},
    "status_valid": {"en": "valid on this date", "he": "בתוקף בתאריך זה"},
    "status_expired": {"en": "expired on the dates given; confirm with the service center (*8657)", "he": "פג לפי התאריכים שנמסרו; אמתו מול מרכז השירות (*8657)"},
    "status_uncertain": {"en": "unclear, an extension may still apply; ask the service center", "he": "לא ברור, ייתכן שעדיין חלה הארכה; שאלו את מרכז השירות"},
    "clock": {"en": "Clock", "he": "שעון"},
    "date": {"en": "Date", "he": "תאריך"},
    "days": {"en": "Days", "he": "ימים"},
    "past": {"en": "past", "he": "עבר"},
    "extended": {"en": "extended to", "he": "הוארך עד"},
    "original": {"en": "original", "he": "מקורי"},
    "days_note": {
        "en": "Days: positive = days from today; negative = days ago.",
        "he": "ימים: חיובי = ימים מהיום; שלילי = ימים שעברו.",
    },
    "sources": {"en": "Sources", "he": "מקורות"},
    "late": {"en": "Late renewal", "he": "חידוש באיחור"},
    "delay": {"en": "delay", "he": "איחור"},
    "delay_fmt": {"en": "{m} month(s) and {d} day(s)", "he": "{m} חודשים ו-{d} ימים"},
    "measured_from": {"en": "measured from", "he": "נמדד מ"},
    "tier": {"en": "tier", "he": "מדרגה"},
    "surcharge": {"en": "surcharge", "he": "תוספת"},
    "surcharge_tail": {
        "en": "NIS on top of the renewal fee ({fee} NIS per year, up to 3 years)",
        "he": "ש\"ח מעבר לאגרת החידוש ({fee} ש\"ח לשנה, עד 3 שנים)",
    },
    "rule": {"en": "rule", "he": "כלל"},
    "late_rule": {
        "en": "gov.il fee page: surcharge added to the renewal fee if renewal is approved; the firearm, license and ammunition go to the police within 72 hours of expiry (criteria regs reg. 9(a))",
        "he": "דף האגרות ב-gov.il: התוספת נוספת לאגרת החידוש אם החידוש מאושר; הכלי, הרישיון והתחמושת מופקדים במשטרה בתוך 72 שעות מהפקיעה (תקנה 9(א) לתקנות התבחינים)",
    },
    "notes": {"en": "Notes", "he": "הערות"},
    "footer": {
        "en": "Verification date of the rules: 28.09.2026. Confirm any figure on gov.il before acting.",
        "he": "תאריך אימות הכללים: 28.09.2026. אמתו כל נתון ב-gov.il לפני שפועלים.",
    },
    "note_conditional": {
        "en": "Before the approval expires (read the date printed on it): pay the fee, train at an authorised range, buy the firearm, and register the transfer. "
              "The theory pass will be valid 3 months from the training date; give --training-date to compute it.",
        "he": "לפני שהאישור פג (קראו את התאריך שמודפס עליו): לשלם אגרה, לעבור הכשרה במטווח מורשה, לרכוש את הכלי ולרשום את ההעברה. "
              "המבחן העיוני יהיה תקף 3 חודשים מיום ההכשרה; תנו --training-date כדי לחשב אותו.",
    },
    "note_conditional_estimate": {
        "en": "The conditional-approval date above is an ESTIMATE (issue date + 6 months, the validity the Knesset review reported in 2024). "
              "Use the expiry printed on the document; pass it with --conditional-expires.",
        "he": "תאריך האישור המותנה למעלה הוא הערכה (תאריך ההנפקה ועוד 6 חודשים, התוקף שדיווחה סקירת הכנסת ב-2024). "
              "השתמשו בתאריך הפקיעה שמודפס על המסמך; העבירו אותו עם --conditional-expires.",
    },
    "note_hist_exact": {
        "en": "History: the {year} wartime temporary order moved the {what} deadline of {orig} to {ext}. The script treats that deadline as {ext}. "
              "That order has expired; no later order was found as of 28.09.2026.",
        "he": "היסטוריה: הוראת השעה של {year} בזמן המלחמה דחתה את מועד ה{what} מ-{orig} ל-{ext}. הסקריפט מתייחס למועד הזה כאל {ext}. "
              "ההוראה פגה; נכון ל-28.09.2026 לא נמצאה הוראה מאוחרת יותר.",
    },
    "note_hist_period": {
        "en": "History: the {year} temporary order extended {what} deadlines falling between {start} and {end}, but names an extended date only for "
              "each month-end (for {orig}: {ext}). Your date ({yours}) is inside that period but is not a named date, so whether it was extended, "
              "and to when, is not stated. The script treats {ext} as possible, not confirmed; ask the service center (*8657). "
              "That order has expired; no later order was found as of 28.09.2026.",
        "he": "היסטוריה: הוראת השעה של {year} האריכה מועדי {what} שחלו בין {start} ל-{end}, אבל נוקבת בתאריך מוארך רק לכל סוף חודש "
              "(ל-{orig}: {ext}). המועד שלכם ({yours}) נמצא בתוך התקופה אך אינו תאריך שנקבע במפורש, ולכן לא נאמר אם הוארך ועד מתי. "
              "הסקריפט מתייחס ל-{ext} כאפשרי ולא כמאושר; שאלו את מרכז השירות (*8657). ההוראה פגה; נכון ל-28.09.2026 לא נמצאה הוראה מאוחרת יותר.",
    },
    "note_hist_month": {
        "en": "History: the {year} wartime temporary order extended {what} deadlines of {orig} to {ext}. The published text names only that month-end date, "
              "so it is not clear whether your {what} date ({yours}) was covered. The script treats {ext} as possible, not confirmed; ask the service center (*8657). "
              "That order has expired; no later order was found as of 28.09.2026.",
        "he": "היסטוריה: הוראת השעה של {year} בזמן המלחמה האריכה מועדי {what} של {orig} עד {ext}. הנוסח שפורסם נוקב רק בתאריך סוף החודש, "
              "ולכן לא ברור אם מועד ה{what} שלכם ({yours}) נכלל. הסקריפט מתייחס ל-{ext} כאפשרי ולא כמאושר; שאלו את מרכז השירות (*8657). "
              "ההוראה פגה; נכון ל-28.09.2026 לא נמצאה הוראה מאוחרת יותר.",
    },
    "note_uncertain": {
        "en": "Status unclear: the confirmed expiry ({cert}) has passed, but an extension that may apply runs to {ext}. Do not treat this as an offence or pay a surcharge "
              "before the service center confirms the status. If it confirms that no extension applies, the license expired on {cert} and the firearm, "
              "the license and the ammunition were due at the police within 72 hours of that date (criteria regs reg. 9(a)), and the official may renew it "
              "only if the request is filed by {req} (validity regs reg. 5); after that it counts as a new application (criteria regs reg. 8). "
              "Do not let {req} pass while waiting: contact the service center (*8657) before that date.",
        "he": "הסטטוס לא ברור: מועד הפקיעה המאושר ({cert}) עבר, אבל הארכה שאולי חלה נמשכת עד {ext}. אל תתייחסו לזה כעבירה ואל תשלמו תוספת "
              "לפני שמרכז השירות מאשר את הסטטוס. אם יתברר שלא חלה הארכה, הרישיון פג ב-{cert}, והכלי, הרישיון והתחמושת היו צריכים "
              "להגיע למשטרה בתוך 72 שעות מאותו מועד (תקנה 9(א) לתקנות התבחינים), ופקיד הרישוי רשאי לחדש אותו "
              "רק אם הבקשה הוגשה עד {req} (תקנה 5 לתקנות תוקפם של רישיונות); אחרי כן היא נחשבת לבקשה לרישיון חדש (תקנה 8 לתקנות התבחינים). "
              "אל תתנו ל-{req} לחלוף בזמן ההמתנה: פנו למרכז השירות (*8657) לפני המועד הזה.",
    },
    "note_alt_tier": {
        "en": "If an extension did apply, the delay is measured from {ext} instead: {delay}, {tier}, surcharge {amount} NIS.",
        "he": "אם חלה הארכה, האיחור נמדד מ-{ext}: {delay}, {tier}, תוספת {amount} ש\"ח.",
    },
    "note_reservist_applied": {
        "en": "Reservist extension applied to the {what}: 30 or more reserve days in the 90 days before {orig} extend it once by 6 months, to {ext} "
              "({src}). The department announces it by SMS; confirm you received one.",
        "he": "הארכת מילואים הוחלה על ה{what}: 30 ימי מילואים או יותר ב-90 הימים שלפני {orig} מאריכים אותו פעם אחת בשישה חודשים, עד {ext} "
              "({src}). האגף מודיע על כך במסרון; ודאו שקיבלתם.",
    },
    "note_reservist_ask": {
        "en": "Ask before treating the {what} as overdue: did the holder serve 30 or more reserve days in the 90 days before {windows}? If so, it is extended "
              "once by 6 months ({src}); the latest such date here is {ext}. gov.il (14.07.2025) says career soldiers in a qualifying role at activity level A "
              "and above get the same relief until the home-front special-situation declaration ends. Rerun with --reservist-{flag} yes or no.",
        "he": "שאלו לפני שמתייחסים ל{what} כבאיחור: האם בעל הרישיון שירת 30 ימי מילואים או יותר ב-90 הימים שלפני {windows}? אם כן, המועד מוארך "
              "פעם אחת בשישה חודשים ({src}); המועד המאוחר ביותר כזה כאן הוא {ext}. לפי gov.il (14.07.2025), עד לסיום ההכרזה על מצב מיוחד בעורף "
              "גם חיילי קבע בתפקיד המזכה ברמת פעילות א' ומעלה נהנים מאותה הקלה. הריצו שוב עם --reservist-{flag} yes או no.",
    },
    "note_combined": {
        "en": "A temporary order and the reservist extension both touch this {what}. The regulations do not say whether reg. 4A/3A then counts the 90 days "
              "and the 6 months from the original date ({orig}) or from the order's date ({order}). The script relies only on {cert} and treats the period "
              "up to {ext} as uncertain; confirm with the service center.",
        "he": "גם הוראת שעה וגם הארכת המילואים נוגעות ב{what} הזה. התקנות לא אומרות אם תקנה 4א/3א סופרת אז את 90 הימים ואת ששת החודשים "
              "מהמועד המקורי ({orig}) או ממועד הוראת השעה ({order}). הסקריפט מסתמך רק על {cert} ומתייחס לתקופה עד {ext} כלא ודאית; "
              "אמתו מול מרכז השירות.",
    },
    "note_renewal_window": {
        "en": "The renewal reminder period has started: renewal is done in year 3 and must be complete before expiry. If you cannot finish in time, ask the "
              "licensing official, with reasons, for an extension of up to 30 days at a time and 45 days in total (validity regs reg. 4). A pistol license "
              "held for 10 continuous years under criteria 1 to 9 may be renewed even without a current criterion, but only while it is still valid "
              "(criteria regs reg. 10).",
        "he": "תקופת התזכורת לחידוש התחילה: החידוש מתבצע בשנה השלישית וחייב להסתיים לפני הפקיעה. אם לא תספיקו, בקשו מפקיד הרישוי, בבקשה מנומקת, "
              "הארכה של עד 30 יום בכל פעם ועד 45 יום בסך הכול (תקנה 4 לתקנות תוקפם של רישיונות). רישיון לאקדח שמוחזק 10 שנים רצופות "
              "בתבחינים 1 עד 9 אפשר לחדש גם בלי תבחין עדכני, אבל רק כל עוד הרישיון בתוקף (תקנה 10 לתקנות התבחינים).",
    },
    "note_one_year": {
        "en": "More than a year has passed since {date}, the latest date the license may have been valid. Law s.16(a)(1) sets a specific, lighter penalty "
              "(6 months' imprisonment) for a breach of ss.4 or 5 that consists only of not renewing within one year of expiry, and Penal Law s.144(b1) takes "
              "such a non-renewal-only case out of the general weapons offences. The gov.il fee page says holding a firearm without a valid license is a "
              "criminal offence; do not read the one-year mark as the point where exposure starts. See a lawyer.",
        "he": "עברה יותר משנה מ-{date}, המועד המאוחר ביותר שבו הרישיון אולי היה בתוקף. סעיף 16(א)(1) לחוק קובע עונש ייחודי וקל יותר "
              "(מאסר שישה חודשים) למי שעובר על סעיפים 4 או 5 רק בכך שלא חידש את רישיונו בתוך שנה מהפקיעה, וסעיף 144(ב1) לחוק העונשין "
              "מוציא מקרה של אי-חידוש בלבד מעבירות הנשק הכלליות. לפי דף האגרות ב-gov.il, החזקת כלי ירייה ללא רישיון בתוקף היא עבירה פלילית; "
              "אל תבינו את ציון השנה כנקודה שבה החשיפה מתחילה. פנו לעורך דין.",
    },
    "note_one_year_cond": {
        "en": "If no extension applied, more than a year has passed since {cert}; if one applied, a year from {latest} ends on {end}. Law s.16(a)(1) "
              "sets a specific, lighter penalty (6 months' imprisonment) for a breach of ss.4 or 5 that consists only of not renewing within one year "
              "of expiry. See a lawyer.",
        "he": "אם לא חלה הארכה, עברה יותר משנה מ-{cert}; אם חלה, שנה מ-{latest} מסתיימת ב-{end}. סעיף 16(א)(1) לחוק קובע עונש ייחודי וקל יותר "
              "(מאסר שישה חודשים) למי שעובר על סעיפים 4 או 5 רק בכך שלא חידש את רישיונו בתוך שנה מהפקיעה. פנו לעורך דין.",
    },
    "note_expired": {
        "en": "Unless an extension the service center confirms applies, the license has expired. Holding the firearm without a valid license is a criminal "
              "offence (gov.il fee page). Deposit the firearm, the license and the ammunition at the police station of your residence or business, "
              "within 72 hours of expiry, and keep the receipt (criteria regs reg. 9(a), Law s.14). A request after expiry counts as a new application "
              "(reg. 8); the official may still renew if the request came within 30 days of expiry (validity regs reg. 5). If renewal is approved, the "
              "surcharge above applies. If you filed the renewal before expiry and are waiting for a decision, the sources do not say whether the "
              "surcharge applies; ask the service center.",
        "he": "אלא אם מרכז השירות מאשר שחלה הארכה, הרישיון פג. החזקת כלי ירייה ללא רישיון בתוקף היא עבירה פלילית (דף האגרות ב-gov.il). הפקידו את "
              "הכלי, הרישיון והתחמושת בתחנת המשטרה של מקום המגורים או העסק, בתוך 72 שעות מהפקיעה, ושמרו את אישור הקבלה (תקנה 9(א) לתקנות "
              "התבחינים, סעיף 14 לחוק). בקשה אחרי הפקיעה נחשבת לבקשה לרישיון חדש (תקנה 8); פקיד הרישוי רשאי עדיין לחדש אם הבקשה הוגשה "
              "בתוך 30 יום מהפקיעה (תקנה 5 לתקנות תוקפם של רישיונות). אם החידוש מאושר, חלה התוספת שלמעלה. אם הגשתם את החידוש לפני "
              "הפקיעה ואתם ממתינים להחלטה, המקורות לא אומרים אם התוספת חלה; שאלו את מרכז השירות.",
    },
    "note_gap_2024": {
        "en": "This expiry date falls between the two published 2023/2024 temporary orders for licenses (26.10.2023 to 31.12.2023, and 31.01.2024 "
              "to 31.03.2024), so the script applies no wartime extension to it. If you were told otherwise, confirm with the service center (*8657).",
        "he": "מועד הפקיעה הזה נופל בין שתי הוראות השעה שפורסמו לרישיונות ב-2023/2024 (26.10.2023 עד 31.12.2023, ו-31.01.2024 "
              "עד 31.03.2024), ולכן הסקריפט לא מחיל עליו הארכת מלחמה. אם נאמר לכם אחרת, אמתו מול מרכז השירות (*8657).",
    },
    "what_license": {"en": "license renewal", "he": "חידוש הרישיון"},
    "what_refresher": {"en": "refresher", "he": "ריענון"},
    "what_license_obj": {"en": "license", "he": "רישיון"},
    "what_refresher_obj": {"en": "refresher deadline", "he": "מועד הריענון"},
    "src_license": {"en": "validity regs reg. 4A", "he": "תקנה 4א לתקנות תוקפם של רישיונות"},
    "src_refresher": {"en": "training regs reg. 3A", "he": "תקנה 3א לתקנות ההכשרה"},
    "or": {"en": " or ", "he": " או "},
    "note_refresher_uncertain": {
        "en": "The year-2 refresher deadline ({cert}) has passed, but an extension that may apply runs to {ext}. Do not assume the refresher was missed or "
              "that the license was cancelled before the service center confirms it.",
        "he": "המועד האחרון לריענון של השנה השנייה ({cert}) עבר, אבל הארכה שאולי חלה נמשכת עד {ext}. אל תניחו שהריענון פוספס או "
              "שהרישיון בוטל לפני שמרכז השירות מאשר זאת.",
    },
    "note_refresher_past": {
        "en": "The year-2 refresher window is in the past. Ask whether the refresher was completed; if not, the license may already "
              "have been cancelled under the 72-hour deposit rule, and the service center should confirm the status.",
        "he": "חלון הריענון של השנה השנייה עבר. שאלו אם הריענון בוצע; אם לא, ייתכן שהרישיון כבר בוטל לפי כלל 72 השעות, "
              "ומרכז השירות צריך לאשר את הסטטוס.",
    },
    "note_loss": {
        "en": "Report to the Israel Police now. The Law counts the 48 hours from the loss, destruction or theft itself. Learning of it late helps only "
              "as a defence, and the defence needs BOTH a report within 48 hours of learning of it AND having held the firearm in reasonable conditions "
              "(Law s.15(a)(1)-(2)). If the license card itself was lost, the Law also requires telling the licensing official (s.15(b)).",
        "he": "דווחו למשטרת ישראל עכשיו. החוק סופר את 48 השעות מהאבידה, ההשמדה או הגניבה עצמה. העובדה שנודע לכם מאוחר מועילה רק "
              "כהגנה, וההגנה דורשת גם דיווח בתוך 48 שעות מרגע שנודע לכם וגם החזקה של הכלי בתנאים סבירים (סעיף 15(א)(1)-(2) לחוק). "
              "אם אבד כרטיס הרישיון עצמו, החוק מחייב גם להודיע לפקיד הרישוי (סעיף 15(ב)).",
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


def add_months_keep_month_end(d: dt.date, months: int) -> dt.date:
    """Like add_months, but a month-end date stays a month-end date (30.6 + 6 months
    = 31.12). Used only for the reservist extension, which runs 6 months "from the
    end of" the validity period; this reading is the one more favourable to the holder."""
    if d.day == calendar.monthrange(d.year, d.month)[1]:
        t = add_months(d.replace(day=1), months)
        return t.replace(day=calendar.monthrange(t.year, t.month)[1])
    return add_months(d, months)


def add_years(d: dt.date, years: int) -> dt.date:
    return add_months(d, 12 * years)


def parse_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a date in YYYY-MM-DD form")


def positive_int(value: str) -> int:
    try:
        n = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a whole number")
    if n <= 0:
        raise argparse.ArgumentTypeError("the annual fee must be a positive number of NIS")
    return n


def months_and_days(start: dt.date, end: dt.date):
    """Whole calendar months from start to end, plus the remaining days."""
    whole = (end.year - start.year) * 12 + (end.month - start.month)
    anchor = add_months(start, whole)
    if anchor > end:
        whole -= 1
        anchor = add_months(start, whole)
    return whole, (end - anchor).days


def months_between(start: dt.date, end: dt.date) -> float:
    """Approximate months between two dates, whole months plus a day fraction."""
    whole, days = months_and_days(start, end)
    anchor = add_months(start, whole)
    days_in_month = calendar.monthrange(anchor.year, anchor.month)[1]
    return whole + days / days_in_month


def delay_text(start: dt.date, end: dt.date, lang: str) -> str:
    m, d = months_and_days(start, end)
    return TEXT["delay_fmt"][lang].format(m=m, d=d)


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


def match_extension(deadline: dt.date, applies_to: str):
    """Return a dict describing a past temporary order that touches `deadline`, or None.

    kind "exact": the deadline is a date the order names; the extension applies.
    kind "period": inside the period a 2023/2024 regulation covers, but not a named date.
    kind "month": another day in a month a 2025/2026 gov.il notice covers."""
    for scope, start, end, mapping, year, kind in HISTORICAL_ORDERS:
        if scope not in ("both", applies_to):
            continue
        if not (start <= deadline <= end):
            continue
        if deadline in mapping:
            return {"kind": "exact", "orig": deadline, "ext": mapping[deadline], "year": year, "start": start, "end": end}
        for named, ext in mapping.items():
            if (named.year, named.month) == (deadline.year, deadline.month):
                return {"kind": kind, "orig": named, "ext": ext, "year": year, "start": start, "end": end}
    return None


def resolve_deadline(deadline: dt.date, reservist: str, which: str, lang: str, notes: list):
    """Work out the confirmed deadline and the latest date it may have been extended to.

    `which` is "license" or "refresher". Returns (certain, possible, ask) where
    `certain` is the date the script relies on, `possible` is a later date that may
    apply but is not confirmed (or None), and `ask` is the reservist question text
    to show if the deadline has passed and the answer is unknown (or None)."""
    what_key = "what_license" if which == "license" else "what_refresher"
    obj_key = "what_license_obj" if which == "license" else "what_refresher_obj"
    src = TEXT["src_license" if which == "license" else "src_refresher"][lang]
    flag = "expiry" if which == "license" else "refresher"

    certain = deadline
    possibles = []
    order_date = None
    hist = match_extension(deadline, which)
    if hist:
        if hist["kind"] == "exact":
            certain = order_date = hist["ext"]
            notes.append(TEXT["note_hist_exact"][lang].format(
                year=hist["year"], what=TEXT[what_key][lang], orig=fmt(hist["orig"]), ext=fmt(hist["ext"])))
        else:
            order_date = hist["ext"]
            possibles.append(hist["ext"])
            key = "note_hist_period" if hist["kind"] == "period" else "note_hist_month"
            notes.append(TEXT[key][lang].format(
                year=hist["year"], what=TEXT[what_key][lang], orig=fmt(hist["orig"]), ext=fmt(hist["ext"]),
                yours=fmt(deadline), start=fmt(hist["start"]), end=fmt(hist["end"])))

    res_orig = add_months_keep_month_end(deadline, RESERVIST_MONTHS)
    res_order = add_months_keep_month_end(order_date, RESERVIST_MONTHS) if order_date else None
    ask = None
    if reservist == "yes" and not hist:
        certain = res_orig
        notes.append(TEXT["note_reservist_applied"][lang].format(
            what=TEXT[obj_key][lang], orig=fmt(deadline), ext=fmt(res_orig), src=src))
    elif reservist in ("yes", "unknown"):
        possibles.append(res_orig)
        if res_order:
            possibles.append(res_order)
        if reservist == "yes":
            notes.append(TEXT["note_combined"][lang].format(
                what=TEXT[obj_key][lang], orig=fmt(deadline), order=fmt(order_date), cert=fmt(certain),
                ext=fmt(max([certain] + possibles))))
        else:
            windows = fmt(deadline) if not order_date else fmt(deadline) + TEXT["or"][lang] + fmt(order_date)
            ask = TEXT["note_reservist_ask"][lang].format(
                what=TEXT[obj_key][lang], windows=windows, src=src, ext=fmt(max(possibles)), flag=flag)

    latest = max([certain] + possibles)
    return certain, (latest if latest > certain else None), ask


def build(args) -> dict:
    lang = args.lang
    today = args.today or dt.date.today()
    out = {"today": today.isoformat(), "lang": lang, "clocks": [], "notes": []}

    def clock(key, date, effective=None):
        effective = effective or date
        item = {
            "key": key,
            "clock": LABELS[key][lang],
            "date": date.isoformat(),
            "effective_date": effective.isoformat(),
            "days_from_today": (effective - today).days,
            "source": SOURCES[key][lang],
        }
        if effective != date:
            item["extended_to"] = effective.isoformat()
        out["clocks"].append(item)
        return effective

    def note(text):
        if text not in out["notes"]:
            out["notes"].append(text)

    if args.conditional_expires:
        clock("conditional_expires", args.conditional_expires)
        note(TEXT["note_conditional"][lang])
    elif args.conditional_approval:
        clock("conditional_estimate", add_months(args.conditional_approval, 6))
        note(TEXT["note_conditional"][lang])
        note(TEXT["note_conditional_estimate"][lang])

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
        ref_cert, ref_possible, ref_ask = resolve_deadline(
            year2_end, args.reservist_refresher, "refresher", lang, out["notes"])
        clock("refresher_closes", year2_end, ref_cert)
        if ref_possible and today > ref_cert:
            clock("refresher_possible", ref_possible)
        ref_latest = ref_possible or ref_cert
        clock("renewal_opens", add_months(expiry, -3))
        exp_cert, exp_possible, exp_ask = resolve_deadline(
            expiry, args.reservist_expiry, "license", lang, out["notes"])
        clock("license_expires", expiry, exp_cert)
        if exp_possible and today > exp_cert:
            clock("license_possible", exp_possible)
        latest = exp_possible or exp_cert

        if add_months(expiry, -3) <= today <= exp_cert:
            note(TEXT["note_renewal_window"][lang])
        if today <= latest:
            if ref_cert < today <= ref_latest:
                if ref_ask:
                    note(ref_ask)
                note(TEXT["note_refresher_uncertain"][lang].format(cert=fmt(ref_cert), ext=fmt(ref_latest)))
            elif today > ref_latest:
                note(TEXT["note_refresher_past"][lang])

        if dt.date(2024, 1, 1) <= expiry <= dt.date(2024, 1, 30):
            note(TEXT["note_gap_2024"][lang])
        if today > exp_cert and exp_ask:
            note(exp_ask)

        if exp_cert < today <= latest:
            # A possible extension still runs: no offence flag, no surcharge.
            out["status"] = "uncertain"
            clock("deposit_if_no_extension", exp_cert + dt.timedelta(days=3))
            req = exp_cert + dt.timedelta(days=30)
            clock("late_request_if_no_extension", req)
            note(TEXT["note_uncertain"][lang].format(cert=fmt(exp_cert), ext=fmt(latest), req=fmt(req)))
        elif today > latest:
            out["status"] = "expired"
            clock("deposit_after_expiry", exp_cert + dt.timedelta(days=3))
            clock("late_request", exp_cert + dt.timedelta(days=30))
            delay = months_between(exp_cert, today)
            tier, amount = surcharge(delay, args.annual_fee, lang)
            m, d = months_and_days(exp_cert, today)
            out["late_renewal"] = {
                "months_late": round(delay, 2),
                "delay_months_days": [m, d],
                "delay_text": delay_text(exp_cert, today, lang),
                "measured_from": exp_cert.isoformat(),
                "tier": tier,
                "surcharge_nis": amount,
                "renewal_fee_nis_per_year": args.annual_fee,
                "rule": TEXT["late_rule"][lang],
            }
            if exp_possible:
                clock("late_request_if_extension", exp_possible + dt.timedelta(days=30))
                alt_delay = months_between(exp_possible, today)
                alt_tier, alt_amount = surcharge(alt_delay, args.annual_fee, lang)
                am, ad = months_and_days(exp_possible, today)
                out["late_renewal"]["if_extension_applied"] = {
                    "measured_from": exp_possible.isoformat(),
                    "months_late": round(alt_delay, 2),
                    "delay_months_days": [am, ad],
                    "tier": alt_tier,
                    "surcharge_nis": alt_amount,
                }
                note(TEXT["note_alt_tier"][lang].format(
                    ext=fmt(exp_possible), delay=delay_text(exp_possible, today, lang), tier=alt_tier, amount=alt_amount))
            note(TEXT["note_expired"][lang])
            note(TEXT["note_refresher_past"][lang])
            if today > add_years(latest, 1):
                note(TEXT["note_one_year"][lang].format(date=fmt(latest)))
            elif today > add_years(exp_cert, 1):
                note(TEXT["note_one_year_cond"][lang].format(
                    cert=fmt(exp_cert), latest=fmt(latest), end=fmt(add_years(latest, 1))))
        else:
            out["status"] = "valid"

    if args.refresher_notice:
        clock("deposit_deadline", args.refresher_notice + dt.timedelta(days=3))

    if args.refusal_received:
        clock("appeal_deadline", args.refusal_received + dt.timedelta(days=45))

    if args.loss_date or args.loss_discovered:
        if args.loss_date:
            clock("police_report", args.loss_date + dt.timedelta(days=2))
        if args.loss_discovered:
            clock("police_report_learned", args.loss_discovered + dt.timedelta(days=2))
        clock("official_report", (args.loss_discovered or args.loss_date) + dt.timedelta(days=3))
        note(TEXT["note_loss"][lang])

    if not out["clocks"]:
        raise SystemExit("Give at least one anchor date. Run with --help for the options.")

    out["clocks"].sort(key=lambda c: c["effective_date"])
    return out


def print_text(result: dict) -> None:
    lang = result["lang"]
    t = lambda k: TEXT[k][lang]  # noqa: E731
    today = dt.date.fromisoformat(result["today"])
    print(f"{t('today')}: {fmt(today)}")
    if result.get("status"):
        print(f"{t('status')}: {TEXT['status_' + result['status']][lang]}")
    print(t("days_note"))
    print()
    print(f"{t('clock'):<66} {t('date'):<12} {t('days'):>6}  ")
    print("-" * 88)
    for c in result["clocks"]:
        eff = dt.date.fromisoformat(c["effective_date"])
        days = c["days_from_today"]
        flag = f"  ({t('past')})" if days < 0 else ""
        print(f"{c['clock']:<66} {fmt(eff):<12} {days:>6}{flag}")
        if c.get("extended_to"):
            orig = dt.date.fromisoformat(c["date"])
            print(f"    {t('extended')} {fmt(eff)}; {t('original')} {fmt(orig)}")
    print()
    print(f"{t('sources')}:")
    for c in result["clocks"]:
        print(f"  * {c['clock']}: {c['source']}")
    if "late_renewal" in result:
        lr = result["late_renewal"]
        print()
        print(f"{t('late')}:")
        print(f"  {t('delay')}: {lr['delay_text']} ({t('measured_from')} {fmt(dt.date.fromisoformat(lr['measured_from']))})")
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
            "  %(prog)s --license-expires 2026-07-31 --today 2026-09-28 --json\n"
            "  %(prog)s --license-expires 2026-07-31 --today 2026-09-28 --reservist-expiry yes\n"
            "  %(prog)s --loss-date 2026-09-27 --loss-discovered 2026-09-28\n"
            "  %(prog)s --refusal-received 2026-09-01 --lang he\n"
        ),
    )
    p.add_argument("--conditional-approval", type=parse_date,
                   help="issue date of the ishur mutne (YYYY-MM-DD); gives only an ESTIMATED expiry")
    p.add_argument("--conditional-expires", type=parse_date,
                   help="expiry date printed on the ishur mutne (YYYY-MM-DD); preferred over --conditional-approval")
    p.add_argument("--training-date", type=parse_date, help="date of the range training; the theory pass runs 3 months from it")
    p.add_argument("--theory-exam", type=parse_date, help="alias of --training-date")
    p.add_argument("--transfer-date", type=parse_date, help="date of the ownership transfer (purchase)")
    p.add_argument("--license-issued", type=parse_date, help="date the 3-year license was issued")
    p.add_argument("--license-expires", type=parse_date, help="expiry date printed on the license")
    p.add_argument("--refresher-notice", type=parse_date, help="date the official's notice of a missed refresher was received")
    p.add_argument("--refusal-received", type=parse_date, help="date the refusal or cancellation letter was received")
    p.add_argument("--loss-date", type=parse_date, help="date the firearm was lost, destroyed or stolen (Law s.15(a) counts from it)")
    p.add_argument("--loss-discovered", type=parse_date, help="date the holder learned of the loss or theft")
    p.add_argument("--reservist-expiry", choices=["yes", "no", "unknown"], default="unknown",
                   help="30+ reserve days in the 90 days before the license expiry (validity regs reg. 4A); with a past temporary "
                        "order, before the original or the extended date")
    p.add_argument("--reservist-refresher", choices=["yes", "no", "unknown"], default="unknown",
                   help="30+ reserve days in the 90 days before the refresher deadline (training regs reg. 3A)")
    p.add_argument("--today", type=parse_date, help="override today's date (YYYY-MM-DD)")
    p.add_argument("--annual-fee", type=positive_int, default=ANNUAL_FEE_DEFAULT,
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
