#!/usr/bin/env python3
"""Print the document and action checklist for a stage of the Israeli private
firearm license process, in English or Hebrew. Stdlib only.

Verification date of the content: 14.09.2026 (gov.il service pages, Knesset RIC
review of 13.02.2024, Firearms Law and 2023 regulations).

Usage:
  python build_stage_checklist.py --list
  python build_stage_checklist.py --stage conditional
  python build_stage_checklist.py --stage renewal --lang he
  python build_stage_checklist.py --stage lost-stolen --json
"""

import argparse
import json
import sys

GOV = {
    "apply": "https://www.gov.il/he/service/issue_firearms_license_to_a_private_individual",
    "criteria": "https://www.gov.il/he/pages/firearm_licensing_criteria",
    "calculator": "https://www.gov.il/apps/mops/firearm_license_calculator/",
    "form": "https://auth.govforms.gov.il/mw/forms/WeaponLicense@mops.gov.il",
    "renewal": "https://www.gov.il/he/service/private_firearm_license_renewal",
    "refresher": "https://www.gov.il/he/service/refresher-training",
    "fees": "https://www.gov.il/he/pages/fa_license_fees",
    "storage": "https://www.gov.il/he/pages/firearm_storage",
    "ammo": "https://www.gov.il/he/pages/firearm-ammunition-regulations",
    "appeal": "https://www.gov.il/he/service/firearm_license_appeal",
    "copy": "https://www.gov.il/he/service/get_firearm_license_copy",
    "sale": "https://www.gov.il/he/service/sale_of_firearms",
    "replace": "https://www.gov.il/he/service/changing_firearms",
    "contact": "https://www.gov.il/he/pages/firearm_contact_us",
    "contact_update": "https://auth.govforms.gov.il/mw/forms/form19@mops.gov.il",
    "ranges": "https://www.gov.il/he/Departments/publications/reports/firearm_firing_range",
    "dealers": "https://www.gov.il/he/Departments/publications/reports/firearm_merchants",
    "law": "https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%9B%D7%9C%D7%99_%D7%94%D7%99%D7%A8%D7%99%D7%99%D7%94",
}

CONTACT_EN = "Service center: *8657 or 077-2324444, tservice@mops.gov.il, Sun-Thu 08:00-17:00, Fri and holiday eves 08:00-12:00."
CONTACT_HE = "מרכז שירות ומידע: *8657 או 077-2324444, tservice@mops.gov.il, ימים א' עד ה' 08:00 עד 17:00, ימי ו' וערבי חג 08:00 עד 12:00."

STAGES = {
    "eligibility": {
        "title": {"en": "Stage 1: Eligibility check", "he": "שלב 1: בדיקת זכאות"},
        "items": [
            {"en": "Run the official eligibility calculator with your real address, service history and age.", "he": "הריצו את מחשבון הזכאות הרשמי עם הכתובת, נתוני השירות והגיל האמיתיים שלכם.", "url": GOV["calculator"]},
            {"en": "Confirm every threshold condition: status and 3 years of residence, basic Hebrew, physician-signed health declaration, age rule for your service.", "he": "ודאו עמידה בכל תנאי הסף: מעמד ושלוש שנות מגורים, עברית בסיסית, הצהרת בריאות חתומה על ידי רופא, כלל הגיל המתאים לשירות שלכם.", "url": GOV["criteria"]},
            {"en": "Pick one criterion from the closed list and download its affidavit form from the criteria page.", "he": "בחרו תבחין אחד מהרשימה הסגורה והורידו את טופס התצהיר שלו מדף התבחינים.", "url": GOV["criteria"]},
            {"en": "Order service confirmations on the IDF approvals site (Chrome) or the national or civil service site.", "he": "הזמינו אישורי שירות באתר האישורים של צה\"ל (בדפדפן כרום) או באתר השירות הלאומי-אזרחי.", "url": GOV["apply"]},
        ],
        "next": {"en": "Submit the online application.", "he": "הגישו את הבקשה המקוונת."},
    },
    "application": {
        "title": {"en": "Stage 2: Online application", "he": "שלב 2: הגשת בקשה מקוונת"},
        "items": [
            {"en": "Health declaration signed by your family physician (PDF on the application page).", "he": "הצהרת בריאות חתומה על ידי רופא המשפחה (קובץ PDF בדף הבקשה).", "url": GOV["apply"]},
            {"en": "Copy of identity card and appendix (sefach).", "he": "צילום תעודת זהות וספח.", "url": None},
            {"en": "Confirmation of military, national or civil service, or exemption.", "he": "אישור שירות צבאי, לאומי או אזרחי, או פטור משירות.", "url": None},
            {"en": "Supporting documents for the criterion (affidavit, employer or body confirmation, professional license).", "he": "מסמכים תומכים לתבחין (תצהיר, אישור מעסיק או גוף, רישיון מקצועי).", "url": GOV["criteria"]},
            {"en": "Sign in through the national identification system and submit the form; keep the SMS with the request number.", "he": "היכנסו דרך מערכת ההזדהות הלאומית והגישו את הטופס; שמרו את המסרון עם מספר הבקשה.", "url": GOV["form"]},
            {"en": "Track progress in the government personal area.", "he": "עקבו אחר הטיפול באזור האישי הממשלתי.", "url": None},
        ],
        "next": {"en": "Wait for an interview exemption or an SMS link to book a phone interview.", "he": "המתינו לפטור מראיון או למסרון עם קישור לזימון ראיון טלפוני."},
    },
    "interview": {
        "title": {"en": "Stage 3: Phone interview", "he": "שלב 3: ראיון טלפוני"},
        "items": [
            {"en": "Book the slot from the SMS link; residence and security-service criteria are often exempt.", "he": "קבעו תור דרך הקישור במסרון; תבחיני מגורים ושירות בכוחות הביטחון לרוב פטורים.", "url": GOV["apply"]},
            {"en": "Have the application and documents in front of you; the call clarifies the application data.", "he": "החזיקו את הבקשה והמסמכים מולכם; השיחה מבררת את נתוני הבקשה.", "url": None},
            {"en": "If you served in a security body or trained at an authorised range in the last 3 years, ask for the shortened 2-hour training and prepare the certificate.", "he": "אם שירתתם בגוף ביטחוני או עברתם הכשרה במטווח מורשה בשלוש השנים האחרונות, בקשו הכשרה מקוצרת של שעתיים והכינו את האישור.", "url": GOV["apply"]},
        ],
        "next": {"en": "Receive the conditional approval (ishur mutne) with a payment voucher.", "he": "קבלו את האישור המותנה עם שובר תשלום."},
    },
    "conditional": {
        "title": {"en": "Stage 4: Holding a conditional approval (ishur mutne)", "he": "שלב 4: בידכם אישור מותנה"},
        "items": [
            {"en": "Note the date on the approval; the Knesset review puts its validity at half a year. Everything below must fit inside it.", "he": "רשמו את התאריך שעל האישור; לפי סקירת הכנסת תוקפו חצי שנה. כל מה שלמטה חייב להסתיים בתוכו.", "url": None},
            {"en": "Pay the fee through the government payment service or the postal bank: 71 NIS per year or part of a year as of 04.01.2026, computed per year of validity up to 3 years, so a 3-year license is three times the annual fee; the voucher shows the amount. Reservists get 50 percent off on presenting the eligibility card (gov.il application page). Print the confirmation.", "he": "שלמו את האגרה בשירות התשלומים הממשלתי או בבנק הדואר: 71 ש\"ח לשנה או לחלק ממנה נכון ל-04.01.2026, מחושב לפי שנות התוקף עד 3 שנים, כך שרישיון לשלוש שנים הוא פי שלושה מהאגרה השנתית; הסכום מופיע על השובר. משרתי מילואים מקבלים 50 אחוז הנחה בהצגת תעודת הזכאות (דף הבקשה ב-gov.il). הדפיסו את האישור.", "url": GOV["fees"]},
            {"en": "Range training has its own price, which gov.il does not publish; ask the range when booking.", "he": "להכשרה במטווח יש מחיר משלה, ש-gov.il לא מפרסם; שאלו את המטווח בעת קביעת התור.", "url": GOV["ranges"]},
            {"en": "Choose an authorised range from the gov.il list and book the initial training.", "he": "בחרו מטווח מורשה מרשימת gov.il וקבעו את ההכשרה הראשונית.", "url": GOV["ranges"]},
            {"en": "Bring to the range: payment confirmation, a copy of the health declaration, the conditional approval.", "he": "הביאו למטווח: אישור תשלום, העתק הצהרת הבריאות, האישור המותנה.", "url": GOV["apply"]},
            {"en": "Decide which firearm you will buy before training; the training must be on an identical model and caliber.", "he": "החליטו איזה כלי תרכשו לפני ההכשרה; ההכשרה חייבת להיות על כלי זהה בדגם ובקליבר.", "url": None},
        ],
        "next": {"en": "Complete the training; the theory pass is valid 3 months.", "he": "השלימו את ההכשרה; המבחן העיוני תקף שלושה חודשים."},
    },
    "training": {
        "title": {"en": "Stage 5: Range training", "he": "שלב 5: הכשרה במטווח"},
        "items": [
            {"en": "Regular track: 4.5 consecutive hours, theory exam at 70 percent, 80 practice rounds, 20-round qualification at 70 percent.", "he": "מסלול רגיל: 4.5 שעות ברצף, מבחן עיוני בציון 70 אחוז, אימון 80 כדורים, מבחן הסמכה של 20 כדורים בציון 70 אחוז.", "url": GOV["apply"]},
            {"en": "Shortened track (if approved at the interview): 2 hours, theory exam, 20 practice rounds, 10-round qualification.", "he": "מסלול מקוצר (אם אושר בראיון): שעתיים, מבחן עיוני, אימון 20 כדורים, מבחן הסמכה של 10 כדורים.", "url": GOV["apply"]},
            {"en": "Failing the theory exam blocks the practical part; a failed candidate may retrain.", "he": "כישלון במבחן העיוני חוסם את החלק המעשי; מי שנכשל רשאי לבצע הכשרה נוספת.", "url": None},
            {"en": "Keep the range's training confirmation; it names the firearm type and caliber you may buy.", "he": "שמרו את אישור ההכשרה מהמטווח; הוא מציין את סוג הכלי והקליבר שמותר לכם לרכוש.", "url": None},
        ],
        "next": {"en": "Buy the firearm within the 3-month theory window and the 6-month approval window.", "he": "רכשו את הכלי בתוך חלון שלושת החודשים של המבחן העיוני וחלון ששת החודשים של האישור."},
    },
    "purchase": {
        "title": {"en": "Stage 6: Buying the firearm", "he": "שלב 6: רכישת כלי הירייה"},
        "items": [
            {"en": "From a dealer: the dealer does the ownership transfer, hands over firearm and ammunition, and issues the paper license.", "he": "מבית מסחר: הסוחר מבצע את העברת הבעלות, מוסר את הכלי והתחמושת ומנפיק את רישיון הנייר.", "url": GOV["dealers"]},
            {"en": "From a private person: bill of sale with both parties identified before a lawyer, emailed to Tservice@mops.gov.il; buyer brings approval, payment confirmation, training confirmation (same type and caliber); seller brings a valid license card.", "he": "מאדם פרטי: שטר מכר עם הזדהות שני הצדדים בפני עורך דין, נשלח בדוא\"ל ל-Tservice@mops.gov.il; הקונה מביא אישור מותנה, אישור תשלום ואישור הכשרה (אותו סוג וקליבר); המוכר מביא כרטיס רישיון בתוקף.", "url": GOV["sale"]},
            {"en": "The bill of sale must state the ammunition quantity transferred; buy the rest from a dealer with its own bill of sale.", "he": "בשטר המכר יש לציין את כמות התחמושת המועברת; את היתרה קונים מבית מסחר עם שטר מכר נפרד.", "url": GOV["ammo"]},
            {"en": "Buy and install a home safe that meets the gov.il specification before bringing the firearm home.", "he": "רכשו והתקינו כספת ביתית העומדת בהנחיות gov.il לפני שמביאים את הכלי הביתה.", "url": GOV["storage"]},
        ],
        "next": {"en": "Carry the paper license; the plastic card arrives within 90 days.", "he": "שאו את רישיון הנייר; הכרטיס הקבוע מגיע בתוך 90 יום."},
    },
    "waiting-card": {
        "title": {"en": "Stage 7: Waiting for the magnetic card", "he": "שלב 7: ממתינים לכרטיס הקבוע"},
        "items": [
            {"en": "The paper license from the dealer or range is your authority to carry until the card arrives.", "he": "רישיון הנייר מהסוחר או מהמטווח הוא האסמכתא שלכם לנשיאה עד שהכרטיס מגיע.", "url": GOV["apply"]},
            {"en": "The card is mailed within 90 days of the transfer to the address on file at the department.", "he": "הכרטיס נשלח בתוך 90 יום מהעברת הבעלות לכתובת הרשומה באגף.", "url": GOV["apply"]},
            {"en": "If 90 days passed (and under 6 months, same address), call the service center to check eligibility for a free card; otherwise request a copy for the fee.", "he": "אם עברו 90 יום (ופחות משישה חודשים, אותה כתובת), התקשרו למרכז השירות לבדיקת זכאות לכרטיס ללא עלות; אחרת בקשו העתק בתשלום אגרה.", "url": GOV["copy"]},
            {"en": "Update your contact details with the department if anything changed.", "he": "עדכנו פרטי התקשרות באגף אם משהו השתנה.", "url": GOV["contact_update"]},
        ],
        "next": {"en": "Year 2: periodic refresher training.", "he": "שנה שנייה: הכשרת ריענון תקופתית."},
    },
    "refresher": {
        "title": {"en": "Stage 8 (year 2): Periodic refresher training", "he": "שלב 8 (שנה שנייה): הכשרת ריענון תקופתית"},
        "items": [
            {"en": "A reminder arrives at the start of year 2 by mail and electronically; do not wait for it if you know the date.", "he": "תזכורת נשלחת בתחילת השנה השנייה בדואר ובאמצעים דיגיטליים; אל תחכו לה אם התאריך ידוע לכם.", "url": GOV["refresher"]},
            {"en": "Print the refresher confirmation form and bring a health declaration of the license holder (updated one if your details changed).", "he": "הדפיסו את טופס אישור הריענון והביאו הצהרת בריאות של מחזיק הרישיון (מעודכנת אם הפרטים השתנו).", "url": GOV["refresher"]},
            {"en": "Content: theory, 40 practice rounds, 10-round qualification at 70 percent; retakes within 30 days of the first attempt.", "he": "תוכן: עיוני, אימון 40 כדורים, מבחן הסמכה של 10 כדורים בציון 70 אחוז; הכשרות נוספות בתוך 30 יום מהניסיון הראשון.", "url": GOV["refresher"]},
            {"en": "Carry the signed confirmation whenever you carry the firearm.", "he": "שאו את האישור החתום בכל עת שאתם נושאים את הכלי.", "url": None},
            {"en": "Missed it: deposit the firearm at a licensed dealer within 72 hours of the official's notice, or the license is cancelled.", "he": "פספסתם: הפקידו את הכלי אצל סוחר מורשה בתוך 72 שעות מהודעת פקיד הרישוי, אחרת הרישיון יבוטל.", "url": GOV["refresher"]},
        ],
        "next": {"en": "Year 3: renewal from 3 months before expiry.", "he": "שנה שלישית: חידוש החל משלושה חודשים לפני הפקיעה."},
    },
    "renewal": {
        "title": {"en": "Stage 9 (year 3): Renewal", "he": "שלב 9 (שנה שלישית): חידוש רישיון"},
        "items": [
            {"en": "Sign in to the personal area, open the firearms tab and download the personal list of forms.", "he": "היכנסו לאזור האישי, פתחו את לשונית כלי ירייה והורידו את רשימת הטפסים האישית.", "url": GOV["renewal"]},
            {"en": "Pay the renewal fee (71 NIS per year as of 04.01.2026; active reservists 50 percent off if renewed by the set date).", "he": "שלמו את אגרת החידוש (71 ש\"ח לשנה נכון ל-04.01.2026; משרתי מילואים פעילים 50 אחוז הנחה אם החידוש בוצע במועד).", "url": GOV["fees"]},
            {"en": "Sign a new health declaration; it is required on every renewal.", "he": "חתמו על הצהרת בריאות חדשה; היא נדרשת בכל חידוש.", "url": GOV["criteria"]},
            {"en": "Go to an authorised range with the payment confirmation and documents; have your photo taken; complete the renewal refresher.", "he": "גשו למטווח מורשה עם אישור התשלום והמסמכים; הצטלמו; השלימו את הכשרת הריענון לחידוש.", "url": GOV["renewal"]},
            {"en": "Receive the temporary license signed by the range; the plastic card goes to the Population Authority address unless you gave another.", "he": "קבלו רישיון זמני חתום על ידי המטווח; הכרטיס הקבוע נשלח לכתובת שברשות האוכלוסין אלא אם מסרתם כתובת אחרת.", "url": GOV["renewal"]},
            {"en": "Finish before the expiry date; renewal is your responsibility.", "he": "סיימו לפני תאריך הפקיעה; החידוש באחריותכם.", "url": GOV["renewal"]},
        ],
        "next": {"en": "New 3-year cycle.", "he": "מחזור חדש של שלוש שנים."},
    },
    "expired": {
        "title": {"en": "Stage 10: License expired", "he": "שלב 10: הרישיון פג"},
        "items": [
            {"en": "Deposit the firearm at the Israel Police immediately; holding it without a valid license is a criminal offence (gov.il fee page).", "he": "הפקידו את הכלי במשטרת ישראל מיד; החזקת כלי ירייה ללא רישיון בתוקף היא עבירה פלילית (דף האגרות ב-gov.il).", "url": GOV["fees"]},
            {"en": "Before travelling with the firearm to the station, call the station or the service center for instructions; gov.il does not publish transport instructions for this case (practical advice from this skill).", "he": "לפני שנוסעים עם הכלי לתחנה, התקשרו לתחנה או למרכז השירות לקבלת הנחיות; gov.il לא מפרסם הנחיות הובלה למקרה הזה (עצה מעשית של הסקיל).", "url": GOV["contact"]},
            {"en": "Ask for written confirmation of the deposit and keep it (practical advice; not a gov.il requirement).", "he": "בקשו אישור בכתב על ההפקדה ושמרו אותו (עצה מעשית; לא דרישה של gov.il).", "url": None},
            {"en": "Say whether the year-2 refresher was done; if it was missed, the license may already have been cancelled under the 72-hour rule, and the service center should confirm the status.", "he": "ציינו אם ריענון השנה השנייה בוצע; אם פוספס, ייתכן שהרישיון כבר בוטל לפי כלל 72 השעות, ומרכז השירות צריך לאשר את הסטטוס.", "url": GOV["refresher"]},
            {"en": "Check that a valid criterion still applies (calculator), then call the service center with your ID number to open the renewal.", "he": "בדקו שתבחין תקף עדיין מתקיים (מחשבון), ואז התקשרו למרכז השירות עם מספר הזהות לפתיחת החידוש.", "url": GOV["calculator"]},
            {"en": "Expect a surcharge on top of the renewal fee: up to 6 months late, one annual fee; 6 to 12 months, three annual fees; over 12 months, four annual fees per year of delay.", "he": "צפו לתוספת אגרה מעבר לאגרת החידוש: איחור עד שישה חודשים, אגרה שנתית אחת; שישה עד 12 חודשים, שלוש אגרות שנתיות; מעל 12 חודשים, ארבע אגרות שנתיות לכל שנת איחור.", "url": GOV["fees"]},
            {"en": "Check the gov.il news page for an emergency extension covering your date before paying (the 23.04.2026 order moved March to May 2026 deadlines to June to August 2026).", "he": "בדקו בדף החדשות של gov.il אם הוראת שעה מאריכה את המועד שלכם לפני התשלום (הוראת 23.04.2026 דחתה מועדים ממרץ עד מאי 2026 ליוני עד אוגוסט 2026).", "url": GOV["renewal"]},
        ],
        "next": {"en": "Renew at the range once the department approves.", "he": "חדשו במטווח לאחר אישור האגף."},
    },
    "lost-stolen": {
        "title": {"en": "Firearm lost or stolen", "he": "כלי הירייה אבד או נגנב"},
        "items": [
            {"en": "Report to a police station as early as possible and no later than 48 hours after learning of it (Firearms Law s.15(a)). Get the report number.", "he": "דווחו לתחנת משטרה מוקדם ככל האפשר ולא יאוחר מ-48 שעות מרגע שנודע לכם (סעיף 15(א) לחוק כלי הירייה). קבלו מספר אירוע.", "url": GOV["law"]},
            {"en": "Report to the licensing official within 72 hours (department procedure 12.02.32) by email with your ID number.", "he": "דווחו לפקיד הרישוי בתוך 72 שעות (נוהל האגף 12.02.32) בדוא\"ל עם מספר הזהות.", "url": GOV["contact"]},
            {"en": "Expect cancellation of the license by registered letter and a demand to return the license card.", "he": "צפו לביטול הרישיון במכתב רשום ולדרישה להחזיר את כרטיס הרישיון.", "url": None},
            {"en": "A replacement firearm needs a new application under a currently valid criterion; a grandfathered basis does not count.", "he": "כלי חלופי מחייב בקשה חדשה בתבחין תקף כיום; תבחין משמר אינו מזכה.", "url": GOV["apply"]},
        ],
        "next": {"en": "If you want a replacement, start again at stage 1.", "he": "אם רוצים כלי חלופי, מתחילים מחדש משלב 1."},
    },
    "moved": {
        "title": {"en": "Moved home or changed workplace", "he": "עברתם דירה או החלפתם מקום עבודה"},
        "items": [
            {"en": "Run the calculator with the new address or workplace; the residence and workplace criteria depend on a police recommendation per place.", "he": "הריצו את המחשבון עם הכתובת או מקום העבודה החדשים; תבחיני המגורים והעבודה תלויים בהמלצת משטרה לכל מקום.", "url": GOV["calculator"]},
            {"en": "If the criterion no longer holds: after the official's written notice you have 30 days to prove it; if not proven by then, the firearm and ammunition are deposited at a licensed dealer and you may prove another criterion within up to 6 months of the first notice, after which the license is cancelled.", "he": "אם התבחין חדל להתקיים: לאחר הודעה בכתב מפקיד הרישוי יש 30 יום להוכיח אותו; אם לא הוכח עד אז, הכלי והתחמושת מופקדים אצל סוחר מורשה ואפשר להוכיח תבחין אחר בתוך עד שישה חודשים מההודעה הראשונה, ואחר כך הרישיון מבוטל.", "url": GOV["criteria"]},
            {"en": "The sources describe a notice initiated by the official; no published rule says the holder must report a move on their own. Contacting the department early is practical advice from this skill, not a cited duty.", "he": "המקורות מתארים הודעה שיוזם פקיד הרישוי; אין כלל מפורסם שמחייב את המחזיק לדווח על מעבר מיוזמתו. פנייה מוקדמת לאגף היא עצה מעשית של הסקיל, לא חובה מצוטטת.", "url": None},
            {"en": "Update contact details with the department (form 19) and the address at the Population Authority; the card and reminders go to those.", "he": "עדכנו פרטי התקשרות באגף (טופס 19) ואת הכתובת ברשות האוכלוסין; הכרטיס והתזכורות נשלחים לשם.", "url": GOV["contact_update"]},
            {"en": "Reinstall the safe in the new home to the same specification.", "he": "התקינו את הכספת מחדש בבית החדש לפי אותה הנחיה.", "url": GOV["storage"]},
        ],
        "next": {"en": "If the new place qualifies, send the update this week.", "he": "אם המקום החדש מזכה, שלחו את העדכון השבוע."},
    },
    "sell-or-replace": {
        "title": {"en": "Selling or replacing the firearm", "he": "מכירה או החלפה של כלי הירייה"},
        "items": [
            {"en": "Replacement: use the replacement request form and, for a private counterpart, the private bill of sale (gov.il replacement page). Fee 71 NIS (04.01.2026).", "he": "החלפה: השתמשו בטופס הבקשה להחלפה, ומול אדם פרטי בשטר המכר לאדם פרטי (דף ההחלפה ב-gov.il). אגרה 71 ש\"ח (04.01.2026).", "url": GOV["replace"]},
            {"en": "Sale to a private person: seller brings the valid license card; buyer brings approval, payment and training confirmation on the same type and caliber; bill of sale emailed to Tservice@mops.gov.il after identification before a lawyer.", "he": "מכירה לאדם פרטי: המוכר מביא כרטיס רישיון בתוקף; הקונה מביא אישור מותנה, אישור תשלום ואישור הכשרה על אותו סוג וקליבר; שטר המכר נשלח בדוא\"ל ל-Tservice@mops.gov.il לאחר הזדהות בפני עורך דין.", "url": GOV["sale"]},
            {"en": "State the ammunition quantity on the bill of sale.", "he": "ציינו את כמות התחמושת בשטר המכר.", "url": GOV["ammo"]},
            {"en": "If your firearm is deposited at the police, check with the licensing bureau for a debt before selling.", "he": "אם הכלי שלכם מופקד במשטרה, בדקו מול לשכת הרישוי אם קיים חוב לפני המכירה.", "url": GOV["sale"]},
        ],
        "next": {"en": "The buyer's card arrives within 90 days of the transfer.", "he": "הכרטיס של הקונה מגיע בתוך 90 יום מהעברת הבעלות."},
    },
    "refused-or-cancelled": {
        "title": {"en": "Refusal or cancellation", "he": "סירוב או ביטול"},
        "items": [
            {"en": "Note the date you received the letter; the appeal must reach the service center within 45 days of it.", "he": "רשמו את תאריך קבלת המכתב; הערר חייב להגיע למרכז השירות בתוך 45 יום ממנו.", "url": GOV["appeal"]},
            {"en": "If it is a cancellation, deposit all firearms at the nearest police station immediately as the letter instructs.", "he": "אם מדובר בביטול, הפקידו מיד את כל כלי הירייה בתחנת המשטרה הקרובה כפי שהמכתב מורה.", "url": None},
            {"en": "Download the appeal form; it must be completed and signed by a lawyer certifying the data. Attach a reasoned letter and documents. No fee.", "he": "הורידו את טופס הערר; יש למלא אותו ולהחתים עורך דין על נכונות הנתונים. צרפו מכתב מנומק ומסמכים. ללא עלות.", "url": GOV["appeal"]},
            {"en": "Health Ministry ground: ask first to be examined by the designated physician; police ground: address the specific matter with documents.", "he": "עילה של משרד הבריאות: בקשו קודם להיבדק אצל הרופא הבודק; עילה משטרתית: התייחסו לעניין הספציפי עם מסמכים.", "url": None},
            {"en": "Decision within 45 days; it is final, and the next step is the courts. Court-order cancellations go to the court, not the department.", "he": "החלטה בתוך 45 יום; היא סופית והשלב הבא הוא בית המשפט. ביטול מכוח צו בית משפט מטופל בבית המשפט ולא באגף.", "url": GOV["appeal"]},
        ],
        "next": {"en": "Book a lawyer this week and collect the documents.", "he": "קבעו עורך דין השבוע ואספו את המסמכים."},
    },
}


def render(stage_key: str, lang: str, with_next: bool = False, with_contact: bool = False) -> str:
    """Checklist text. By default only the title, the items and a one-line source
    footer, so the agent can paste it and still close the answer with its own
    single 'Next action:' line and one contact block (SKILL.md Step 7)."""
    stage = STAGES[stage_key]
    lines = [stage["title"][lang], "=" * len(stage["title"][lang]), ""]
    for i, item in enumerate(stage["items"], 1):
        lines.append(f"[ ] {i}. {item[lang]}")
        if item.get("url"):
            lines.append(f"       {item['url']}")
    if with_next:
        lines.append("")
        nxt = "Next action: " if lang == "en" else "הפעולה הבאה: "
        lines.append(nxt + stage["next"][lang])
    if with_contact:
        lines.append("")
        lines.append(CONTACT_EN if lang == "en" else CONTACT_HE)
    lines.append("")
    tail = ("Verification date 14.09.2026. Confirm figures on the linked gov.il page before acting."
            if lang == "en" else
            "תאריך אימות 14.09.2026. אמתו את הנתונים בדף gov.il המקושר לפני שפועלים.")
    lines.append(tail)
    return "\n".join(lines)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    p = argparse.ArgumentParser(
        description="Checklist for a stage of the Israeli private firearm license process.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=("Examples:\n  %(prog)s --list\n  %(prog)s --stage conditional\n  %(prog)s --stage renewal --lang he\n"
                "  %(prog)s --stage expired --lang he --with-next --with-contact\n"),
    )
    p.add_argument("--stage", choices=sorted(STAGES.keys()), help="stage or event")
    p.add_argument("--lang", choices=["en", "he"], default="en", help="output language (default en)")
    p.add_argument("--list", action="store_true", help="list the available stages and exit")
    p.add_argument("--json", action="store_true", help="print the stage as JSON")
    p.add_argument("--with-next", action="store_true", help="append the suggested 'Next action' line")
    p.add_argument("--with-contact", action="store_true", help="append the department contact block")
    args = p.parse_args(argv)

    if args.list:
        for key in STAGES:
            print(f"{key:<22} {STAGES[key]['title']['en']}  |  {STAGES[key]['title']['he']}")
        return

    if not args.stage:
        p.error("choose --stage or use --list")

    if args.json:
        stage = STAGES[args.stage]
        print(json.dumps({"stage": args.stage, "lang": args.lang,
                          "title": stage["title"][args.lang],
                          "items": [{"text": i[args.lang], "url": i.get("url")} for i in stage["items"]],
                          "next": stage["next"][args.lang]}, ensure_ascii=False, indent=2))
        return

    print(render(args.stage, args.lang, args.with_next, args.with_contact))


if __name__ == "__main__":
    main()
