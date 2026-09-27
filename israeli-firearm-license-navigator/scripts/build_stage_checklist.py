#!/usr/bin/env python3
"""Print the document and action checklist for a stage of the Israeli private
firearm license process, in English or Hebrew. Stdlib only.

Verification date of the content: 28.09.2026 (gov.il service pages, Knesset RIC
review of 13.02.2024, Firearms Law, the 2023 criteria regulations as amended
through 5786, the validity-of-licenses regulations and the training regulations).

Usage:
  python3 build_stage_checklist.py --list
  python3 build_stage_checklist.py --stage conditional
  python3 build_stage_checklist.py --stage renewal --lang he
  python3 build_stage_checklist.py --stage lost-stolen --json
"""

import argparse
import json
import sys

GOV = {
    "apply": "https://www.gov.il/he/service/issue_firearms_license_to_a_private_individual",
    "criteria": "https://www.gov.il/he/pages/criteria_for",
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
    "ranges": "https://www.gov.il/he/pages/firearm_firing_range_2025",
    "dealers": "https://www.gov.il/he/pages/gunshops_listing",
    "law": "https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%9B%D7%9C%D7%99_%D7%94%D7%99%D7%A8%D7%99%D7%99%D7%94",
    "regs": "https://he.wikisource.org/wiki/%D7%AA%D7%A7%D7%A0%D7%95%D7%AA_%D7%9B%D7%9C%D7%99_%D7%94%D7%99%D7%A8%D7%99%D7%99%D7%94_(%D7%AA%D7%A0%D7%90%D7%99_%D7%A1%D7%A3_%D7%95%D7%AA%D7%91%D7%97%D7%99%D7%A0%D7%99%D7%9D_%D7%9C%D7%A7%D7%91%D7%9C%D7%AA_%D7%A8%D7%99%D7%A9%D7%99%D7%95%D7%9F_%D7%A4%D7%A8%D7%98%D7%99_%D7%9C%D7%9B%D7%9C%D7%99_%D7%99%D7%A8%D7%99%D7%99%D7%94_%D7%95%D7%94%D7%95%D7%A8%D7%90%D7%95%D7%AA_%D7%A0%D7%95%D7%A1%D7%A4%D7%95%D7%AA)",
    "validity": "https://he.wikisource.org/wiki/%D7%AA%D7%A7%D7%A0%D7%95%D7%AA_%D7%9B%D7%9C%D7%99_%D7%94%D7%99%D7%A8%D7%99%D7%99%D7%94_(%D7%AA%D7%95%D7%A7%D7%A4%D7%9D_%D7%A9%D7%9C_%D7%A8%D7%99%D7%A9%D7%99%D7%95%D7%A0%D7%95%D7%AA)",
    "reservist_news": "https://www.gov.il/he/pages/14_7_25",
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
            {"en": "If you served in a security body or trained at an authorised range in the last 3 years, ask early about the shortened 2-hour training and prepare the certificate; gov.il does not say at which stage it is approved.", "he": "אם שירתתם בגוף ביטחוני או עברתם הכשרה במטווח מורשה בשלוש השנים האחרונות, שאלו מוקדם על הכשרה מקוצרת של שעתיים והכינו את האישור; gov.il לא מציין באיזה שלב היא מאושרת.", "url": GOV["apply"]},
        ],
        "next": {"en": "Receive the conditional approval (ishur mutne) with a payment voucher.", "he": "קבלו את האישור המותנה עם שובר תשלום."},
    },
    "conditional": {
        "title": {"en": "Stage 4: Holding a conditional approval (ishur mutne)", "he": "שלב 4: בידכם אישור מותנה"},
        "items": [
            {"en": "Read the expiry date printed on the approval and do everything below before it. The Knesset review (2024) reported a validity of half a year; the date on your document prevails.", "he": "קראו את תאריך הפקיעה שמודפס על האישור ובצעו את כל מה שלמטה לפניו. סקירת הכנסת (2024) דיווחה על תוקף של חצי שנה; התאריך שעל המסמך שלכם קובע.", "url": None},
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
            {"en": "Shortened track (if approved): 2 hours, theory exam, 20 practice rounds, 10-round qualification.", "he": "מסלול מקוצר (אם אושר): שעתיים, מבחן עיוני, אימון 20 כדורים, מבחן הסמכה של 10 כדורים.", "url": GOV["apply"]},
            {"en": "Failing the theory exam blocks the practical part; a failed candidate may retrain.", "he": "כישלון במבחן העיוני חוסם את החלק המעשי; מי שנכשל רשאי לבצע הכשרה נוספת.", "url": None},
            {"en": "Keep the range's training confirmation; it names the firearm type and caliber you may buy.", "he": "שמרו את אישור ההכשרה מהמטווח; הוא מציין את סוג הכלי והקליבר שמותר לכם לרכוש.", "url": None},
        ],
        "next": {"en": "Buy the firearm within the 3-month theory window and before the approval's expiry date.", "he": "רכשו את הכלי בתוך חלון שלושת החודשים של המבחן העיוני ולפני תאריך הפקיעה של האישור."},
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
            {"en": "Reservist: 30 or more reserve days in the 90 days before the refresher deadline extend it once by 6 months (training regulations, reg. 3A); the department sends an SMS.", "he": "משרתי מילואים: 30 ימי מילואים או יותר ב-90 הימים שלפני המועד האחרון לריענון מאריכים אותו פעם אחת בשישה חודשים (תקנה 3א לתקנות ההכשרה); האגף שולח מסרון.", "url": GOV["reservist_news"]},
            {"en": "Missed it: deposit the firearm at a licensed dealer within 72 hours of the official's notice, or the license is cancelled.", "he": "פספסתם: הפקידו את הכלי אצל סוחר מורשה בתוך 72 שעות מהודעת פקיד הרישוי, אחרת הרישיון יבוטל.", "url": GOV["refresher"]},
            {"en": "Custody at a dealer (Law s.14c, written for a voluntary deposit for a fixed period): custody fees, no return while the license has lapsed, and a year after the custody period ends the dealer may sell it (after a registered letter at least 14 days ahead) or hand it to the police. Whether all of this governs a deposit forced by a missed refresher is not stated; ask the service center.", "he": "משמורת אצל סוחר (סעיף 14ג לחוק, שנכתב על מסירה מרצון לתקופה קצובה): דמי משמורת, אין החזרה כל עוד הרישיון פקע, ושנה אחרי תום תקופת המשמורת הסוחר רשאי למכור את הכלי (אחרי מכתב רשום לפחות 14 יום מראש) או למסור אותו למשטרה. לא נאמר אם כל זה חל גם על הפקדה שנכפתה בגלל ריענון שפוספס; שאלו את מרכז השירות.", "url": GOV["law"]},
        ],
        "next": {"en": "Year 3: renewal, complete before expiry; a reminder comes 3 months before.", "he": "שנה שלישית: חידוש שחייב להסתיים לפני הפקיעה; תזכורת מגיעה שלושה חודשים לפני."},
    },
    "renewal": {
        "title": {"en": "Stage 9 (year 3): Renewal", "he": "שלב 9 (שנה שלישית): חידוש רישיון"},
        "items": [
            {"en": "Sign in to the personal area, open the firearms tab and download the personal list of forms.", "he": "היכנסו לאזור האישי, פתחו את לשונית כלי ירייה והורידו את רשימת הטפסים האישית.", "url": GOV["renewal"]},
            {"en": "Pay the renewal fee (71 NIS per year as of 04.01.2026; active reservists 50 percent off if renewed by the set date).", "he": "שלמו את אגרת החידוש (71 ש\"ח לשנה נכון ל-04.01.2026; משרתי מילואים פעילים 50 אחוז הנחה אם החידוש בוצע במועד).", "url": GOV["fees"]},
            {"en": "Sign a new health declaration; it is required on every renewal.", "he": "חתמו על הצהרת בריאות חדשה; היא נדרשת בכל חידוש.", "url": GOV["criteria"]},
            {"en": "Go to an authorised range with the payment confirmation and documents; have your photo taken; complete the renewal refresher.", "he": "גשו למטווח מורשה עם אישור התשלום והמסמכים; הצטלמו; השלימו את הכשרת הריענון לחידוש.", "url": GOV["renewal"]},
            {"en": "Receive the temporary license signed by the range; the plastic card goes to the Population Authority address unless you gave another.", "he": "קבלו רישיון זמני חתום על ידי המטווח; הכרטיס הקבוע נשלח לכתובת שברשות האוכלוסין אלא אם מסרתם כתובת אחרת.", "url": GOV["renewal"]},
            {"en": "Finish before the expiry date; renewal is your responsibility. If you cannot, ask the licensing official, with reasons, for an extension of up to 30 days at a time, 45 days in total (validity regulations, reg. 4). A reservist with 30 or more reserve days in the 90 days before expiry gets 6 more months automatically (reg. 4A); gov.il (14.07.2025) extends this to career soldiers in a qualifying role at activity level A and above until the home-front special-situation declaration ends.", "he": "סיימו לפני תאריך הפקיעה; החידוש באחריותכם. אם לא תספיקו, בקשו מפקיד הרישוי, בבקשה מנומקת, הארכה של עד 30 יום בכל פעם ועד 45 יום בסך הכול (תקנה 4 לתקנות תוקפם של רישיונות). משרת מילואים עם 30 ימי מילואים או יותר ב-90 הימים שלפני הפקיעה מקבל אוטומטית שישה חודשים נוספים (תקנה 4א); לפי gov.il (14.07.2025), עד לסיום ההכרזה על מצב מיוחד בעורף ההקלה חלה גם על חיילי קבע בתפקיד המזכה ברמת פעילות א' ומעלה.", "url": GOV["validity"]},
            {"en": "Held a pistol license for 10 continuous years under criteria 1 to 9? The official may renew it even if the criterion no longer holds, but only while the license is still valid (criteria regulations, reg. 10). Letting it lapse loses this route.", "he": "מחזיקים ברישיון לאקדח 10 שנים רצופות בתבחינים 1 עד 9? פקיד הרישוי רשאי לחדש גם אם התבחין כבר לא מתקיים, אבל רק כל עוד הרישיון בתוקף (תקנה 10 לתקנות התבחינים). מי שנותן לרישיון לפקוע מאבד את המסלול הזה.", "url": GOV["regs"]},
        ],
        "next": {"en": "New 3-year cycle.", "he": "מחזור חדש של שלוש שנים."},
    },
    "expired": {
        "title": {"en": "Stage 10: License expired", "he": "שלב 10: הרישיון פג"},
        "items": [
            {"en": "First check that it really expired: 30 or more reserve days in the 90 days before expiry extend the license automatically by 6 months (validity regulations, reg. 4A), announced by SMS; gov.il (14.07.2025) gives the same relief to career soldiers in a qualifying role at activity level A and above until the home-front special-situation declaration ends. If a past wartime order also moved your date, the regulations do not say which date the 90 days count from; ask the service center before assuming it expired.", "he": "קודם בדקו שהוא באמת פג: 30 ימי מילואים או יותר ב-90 הימים שלפני הפקיעה מאריכים את הרישיון אוטומטית בשישה חודשים (תקנה 4א לתקנות תוקפם של רישיונות), בהודעה במסרון; לפי gov.il (14.07.2025) אותה הקלה ניתנת לחיילי קבע בתפקיד המזכה ברמת פעילות א' ומעלה עד לסיום ההכרזה על מצב מיוחד בעורף. אם גם הוראת שעה קודמת דחתה את המועד שלכם, התקנות לא אומרות מאיזה מועד נספרים 90 הימים; שאלו את מרכז השירות לפני שמניחים שהרישיון פג.", "url": GOV["reservist_news"]},
            {"en": "If it expired: deposit the firearm, the license and the ammunition at the police station of your residence or business within 72 hours of expiry (criteria regulations, reg. 9(a)). Holding it without a valid license is a criminal offence (gov.il fee page).", "he": "אם פג: הפקידו את הכלי, הרישיון והתחמושת בתחנת המשטרה של מקום המגורים או העסק בתוך 72 שעות מהפקיעה (תקנה 9(א) לתקנות התבחינים). החזקה ללא רישיון בתוקף היא עבירה פלילית (דף האגרות ב-gov.il).", "url": GOV["regs"]},
            {"en": "Before travelling with the firearm to the station, call the station or the service center for instructions; gov.il does not publish transport instructions for this case (practical advice from this skill).", "he": "לפני שנוסעים עם הכלי לתחנה, התקשרו לתחנה או למרכז השירות לקבלת הנחיות; gov.il לא מפרסם הנחיות הובלה למקרה הזה (עצה מעשית של הסקיל).", "url": GOV["contact"]},
            {"en": "Get the receipt for the deposit and keep it; the Law gives you that right (s.14). Not depositing lets the official refuse a renewal request (reg. 9(b)).", "he": "קבלו אישור קבלה על ההפקדה ושמרו אותו; החוק מקנה לכם אותו (סעיף 14). אי-הפקדה מאפשרת לפקיד הרישוי לדחות בקשת חידוש (תקנה 9(ב)).", "url": GOV["law"]},
            {"en": "A request filed after expiry counts as a new application (criteria regulations, reg. 8). The official may still renew an expired license if the request came within 30 days of expiry (validity regulations, reg. 5). Ask the service center how your file will be handled.", "he": "בקשה שמוגשת אחרי הפקיעה נחשבת לבקשה לרישיון חדש (תקנה 8 לתקנות התבחינים). פקיד הרישוי רשאי עדיין לחדש רישיון שפקע אם הבקשה הוגשה בתוך 30 יום מהפקיעה (תקנה 5 לתקנות תוקפם של רישיונות). שאלו את מרכז השירות איך יטופל התיק שלכם.", "url": GOV["validity"]},
            {"en": "Say whether the year-2 refresher was done; if it was missed, the license may already have been cancelled under the 72-hour rule, and the service center should confirm the status.", "he": "ציינו אם ריענון השנה השנייה בוצע; אם פוספס, ייתכן שהרישיון כבר בוטל לפי כלל 72 השעות, ומרכז השירות צריך לאשר את הסטטוס.", "url": GOV["refresher"]},
            {"en": "If renewal is approved, expect a surcharge on top of the renewal fee: up to 6 months late, one annual fee; 6 to 12 months, three annual fees; over 12 months, four annual fees per year of delay. Law s.16(a)(1) sets a specific, lighter penalty (6 months' imprisonment) for a breach that consists only of not renewing within one year of expiry; holding without a valid license is an offence in any case (gov.il fee page). Ask a lawyer how it applies to you.", "he": "אם החידוש מאושר, צפו לתוספת אגרה מעבר לאגרת החידוש: איחור עד שישה חודשים, אגרה שנתית אחת; שישה עד 12 חודשים, שלוש אגרות שנתיות; מעל 12 חודשים, ארבע אגרות שנתיות לכל שנת איחור. סעיף 16(א)(1) לחוק קובע עונש ייחודי וקל יותר (מאסר שישה חודשים) לעבירה שכל כולה אי-חידוש בתוך שנה מהפקיעה; החזקה ללא רישיון בתוקף היא עבירה בכל מקרה (דף האגרות ב-gov.il). שאלו עורך דין איך זה חל עליכם.", "url": GOV["fees"]},
            {"en": "Past wartime extensions (license deadlines from 26.10.2023 to 31.12.2023 and from 31.1.2024 to 31.3.2024, refresher deadlines from 31.10.2023 to 31.3.2024, each named month-end moved by 6 months; June and July 2025; March to May 2026) have all expired; the last extended deadline was 31.8.2026. If your date fell in one of those periods, run the calculator and ask the service center whether it was covered.", "he": "הארכות החירום שהיו (מועדי רישיון מ-26.10.2023 עד 31.12.2023 ומ-31.1.2024 עד 31.3.2024, מועדי ריענון מ-31.10.2023 עד 31.3.2024, כל סוף חודש שנקבע נדחה בשישה חודשים; יוני ויולי 2025; מרץ עד מאי 2026) פגו כולן; המועד המוארך האחרון היה 31.8.2026. אם המועד שלכם חל באחת התקופות האלה, הריצו את המחשבון ושאלו את מרכז השירות אם הוא נכלל.", "url": GOV["renewal"]},
            {"en": "Not renewing? Within 18 months of expiry you may ask to keep the firearm permanently deactivated as a memento (criteria regulations, reg. 12); that is a separate procedure.", "he": "לא מחדשים? בתוך 18 חודשים מהפקיעה אפשר לבקש להחזיק את הכלי מושבת לצמיתות למזכרת (תקנה 12 לתקנות התבחינים); זה הליך נפרד.", "url": GOV["regs"]},
        ],
        "next": {"en": "Deposit first, then ask the service center about a new application.", "he": "קודם מפקידים, ואז שואלים את מרכז השירות על בקשה חדשה."},
    },
    "lost-stolen": {
        "title": {"en": "Firearm lost or stolen", "he": "כלי הירייה אבד או נגנב"},
        "items": [
            {"en": "Report to the Israel Police as early as possible and no later than 48 hours after the loss or theft itself (Firearms Law s.15(a)). Learning of it late is only a defence, and the defence needs both a report within 48 hours of learning of it and having held the firearm in reasonable conditions. Get the report number.", "he": "דווחו למשטרת ישראל מוקדם ככל האפשר ולא יאוחר מ-48 שעות לאחר האבידה או הגניבה עצמה (סעיף 15(א) לחוק כלי הירייה). העובדה שנודע לכם מאוחר היא רק הגנה, וההגנה דורשת גם דיווח בתוך 48 שעות מרגע שנודע לכם וגם החזקה של הכלי בתנאים סבירים. קבלו מספר אירוע.", "url": GOV["law"]},
            {"en": "Report to the licensing official within 72 hours (department procedure 12.02.32) by email with your ID number.", "he": "דווחו לפקיד הרישוי בתוך 72 שעות (נוהל האגף 12.02.32) בדוא\"ל עם מספר הזהות.", "url": GOV["contact"]},
            {"en": "The 2014 procedure (12.02.32) says loss or theft leads to cancellation by registered letter and a demand to return the license card. It predates the 2023 regulations; ask the service center how your file will be handled. If the license card itself was lost, the Law requires telling the licensing official (s.15(b)).", "he": "נוהל 2014 (12.02.32) קובע שאובדן או גניבה מביאים לביטול הרישיון במכתב רשום ולדרישה להחזיר את כרטיס הרישיון. הנוהל קודם לתקנות 2023; שאלו את מרכז השירות איך יטופל התיק שלכם. אם אבד כרטיס הרישיון עצמו, החוק מחייב להודיע לפקיד הרישוי (סעיף 15(ב)).", "url": None},
            {"en": "Under the same 2014 procedure, a replacement firearm needs a new application under a currently valid criterion; a grandfathered basis does not count.", "he": "לפי אותו נוהל מ-2014, כלי חלופי מחייב בקשה חדשה בתבחין תקף כיום; תבחין משמר אינו מזכה.", "url": GOV["apply"]},
        ],
        "next": {"en": "If you want a replacement, start again at stage 1.", "he": "אם רוצים כלי חלופי, מתחילים מחדש משלב 1."},
    },
    "moved": {
        "title": {"en": "Moved home or changed workplace", "he": "עברתם דירה או החלפתם מקום עבודה"},
        "items": [
            {"en": "Run the calculator with the new address or workplace; the residence and workplace criteria depend on a police recommendation per place.", "he": "הריצו את המחשבון עם הכתובת או מקום העבודה החדשים; תבחיני המגורים והעבודה תלויים בהמלצת משטרה לכל מקום.", "url": GOV["calculator"]},
            {"en": "If the criterion no longer holds, you must tell the licensing official without delay (criteria regulations, reg. 3(d)). The same duty applies if your citizenship or residency status, or your health, no longer meets the threshold conditions (reg. 2(c)).", "he": "אם התבחין כבר לא מתקיים, חובה להודיע על כך לפקיד הרישוי בלא דיחוי (תקנה 3(ד) לתקנות התבחינים). אותה חובה חלה אם מעמד האזרחות או התושבות, או מצב הבריאות שלכם, כבר לא עומדים בתנאי הסף (תקנה 2(ג)).", "url": GOV["regs"]},
            {"en": "After the official's written notice you have 30 days to prove the criterion; if not proven by then, the firearm and ammunition are deposited at a licensed dealer and you may prove another criterion within up to 6 months of the first notice, after which the license is cancelled.", "he": "לאחר הודעה בכתב מפקיד הרישוי יש 30 יום להוכיח את התבחין; אם לא הוכח עד אז, הכלי והתחמושת מופקדים אצל סוחר מורשה ואפשר להוכיח תבחין אחר בתוך עד שישה חודשים מההודעה הראשונה, ואחר כך הרישיון מבוטל.", "url": GOV["criteria"]},
            {"en": "Held a pistol license for 10 continuous years under criteria 1 to 9? At renewal the official may renew it even without the criterion, as long as the license is still valid (reg. 10).", "he": "מחזיקים ברישיון לאקדח 10 שנים רצופות בתבחינים 1 עד 9? בחידוש פקיד הרישוי רשאי לחדש גם בלי התבחין, כל עוד הרישיון בתוקף (תקנה 10).", "url": GOV["regs"]},
            {"en": "Update contact details with the department through the contact-update form, and the address at the Population Authority; the card and reminders go to those.", "he": "עדכנו פרטי התקשרות באגף דרך טופס עדכון הפרטים, ואת הכתובת ברשות האוכלוסין; הכרטיס והתזכורות נשלחים לשם.", "url": GOV["contact_update"]},
            {"en": "Reinstall the safe in the new home to the same specification.", "he": "התקינו את הכספת מחדש בבית החדש לפי אותה הנחיה.", "url": GOV["storage"]},
        ],
        "next": {"en": "Report the change to the department this week.", "he": "דווחו לאגף על השינוי השבוע."},
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
            {"en": "If it is a cancellation, deposit the firearms, the license and the ammunition at the police station of your residence or business within 72 hours of receiving the notice, against a receipt (criteria regulations, reg. 9(a); Law s.14), or sooner if the letter says so.", "he": "אם מדובר בביטול, הפקידו את כלי הירייה, הרישיון והתחמושת בתחנת המשטרה של מקום המגורים או העסק בתוך 72 שעות מקבלת ההודעה, תמורת אישור קבלה (תקנה 9(א) לתקנות התבחינים; סעיף 14 לחוק), או מוקדם יותר אם המכתב מורה כך.", "url": GOV["regs"]},
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
    tail = ("Verification date 28.09.2026. Confirm figures on the linked gov.il page before acting."
            if lang == "en" else
            "תאריך אימות 28.09.2026. אמתו את הנתונים בדף gov.il המקושר לפני שפועלים.")
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
