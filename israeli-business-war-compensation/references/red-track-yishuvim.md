# Red Track Yishuvim (§35 Border-Area Settlements)

The "red track" under section 35 of the Property Tax & Compensation Fund Law, 1961 (חוק מס רכוש וקרן פיצויים, תשכ"א-1961) covers indirect damage in `יישובי ספר` (border-area settlements). Businesses in red-track yishuvim get:

- No upper cap on the indirect-damage claim
- Direct profit losses are compensable, not just fixed costs and wages
- Border settlements have a dedicated frontier advance page (gov.il/he/service/pay-advances-to-business-owners-in-frontier-roaring-lion). Do NOT use the nationwide advance page (request-for-dvance-dealers-shaagat-haari), which is explicitly scoped to businesses across the country EXCEPT קו העימות settlements
- No minimum turnover-decline threshold (the 25% decline gate does not apply)

## Where the canonical list lives

The canonical, dynamically updated list of red-track yishuvim is maintained by the Israeli Tax Authority and published at:

https://www.gov.il/he/Departments/DynamicCollectors/compensation-tracks

The list shifts based on operational status - yishuvim are added when conflict reaches them and removed when the area is reclassified. Always verify against the live gov.il page before advising a user that their settlement is on the red list. The list as of mid-2026 covers most of the northern Galilee border strip and parts of the Gaza envelope (Otef Aza).

## How to check programmatically

The skill should NOT hard-code the yishuv list - it changes too often. Instead, surface the `compensation-tracks` URL to the user and have them confirm. If a more reliable check is needed, query Kol-Zchut at:

https://www.kolzchut.org.il - search for `יישוב ספר` or the specific yishuv name.

## Common northern red-track yishuvim (illustrative, not authoritative)

These are typically on the list during active northern conflict periods. Always verify on gov.il before relying on them:

- Shtula (שתולה)
- Manara (מנרה)
- Margaliot (מרגליות)
- Misgav Am (מסגב עם)
- Metulla (מטולה)
- Kfar Giladi (כפר גלעדי)
- Ma'ayan Baruch (מעיין ברוך)
- Kfar Yuval (כפר יובל)
- Yir'on (יראון)
- Avivim (אביבים)

## Gaza envelope (Otef Aza)

Within 7 km of the Gaza border, traditionally on the red list:

- Sderot (שדרות) - typically on the special-area or red track depending on regulation in force
- Netivot (נתיבות)
- Sha'ar HaNegev regional council yishuvim
- Eshkol regional council yishuvim
- Hof Ashkelon regional council yishuvim
- Sdot Negev regional council yishuvim

## Practical advice

If a user asks "am I on the red track?", do NOT rely on memory or this file. Tell them:

1. Open the live gov.il page at the URL above
2. Search for their yishuv by Hebrew name
3. If not found there, check kolzchut.org.il for confirmation
4. If still ambiguous, call the Tax Authority hotline at *4954 with their business address

Filing under the wrong track (red vs. nationwide) is a costly error. The red track's no-cap and no-floor benefits don't transfer to the nationwide track, so misclassification typically under-pays a true red-track business by 50%+ of the deserved grant.


## Northern 100% tracks (moved out of SKILL.md 2026-08-19)

Three 100% tracks are available, mutually exclusive:
- **מסלול מחזורים (turnover track)** - compensation reflects lost profit from the full turnover decline; covers 100% of the lost profit.
- **מסלול אדום (red track)** - owner must prove specific income that would have been earned absent the war and gets full reimbursement of that proven amount.
- **מסלול חקלאות (agriculture track)** - a dedicated north sub-track for farming operations, paying 13,615 ₪ per worker employed in agricultural land in the special area (capped at 5M ₪ per farmer for the whole eligibility period); route agricultural callers here rather than the general turnover track.

Walk through the applicable tracks with the caller and pick the higher-yielding option. Salaried employees in these yishuvim get 100% of their wage (not 75%). Note: the request-for-dvance-dealers-shaagat-haari advance portal is for nationwide businesses EXCEPT קו העימות settlements, so a border business does NOT use it - border settlements have a separate frontier advance portal (pay-advances-to-business-owners-in-frontier-roaring-lion), on top of their uncapped red/turnover compensation. The north tracks have later filing windows than the nationwide track (red ~31.08.2026; turnover/wage/agriculture ~24.09.2026) - verify the live date on the track's gov.il page.

## מסלולי 100% בצפון (הועבר מ-SKILL_HE.md ב-19.08.2026)

שלושה מסלולי 100% זמינים, בלעדיים זה לזה:
- **מסלול מחזורים** - הפיצוי משקף את הרווח שנמנע מהירידה המלאה במחזור; מכסה 100% מהרווח שאבד.
- **מסלול אדום** - בעל העסק חייב להוכיח הכנסה ספציפית שהיתה אמורה להיכנס אילולא המלחמה ומקבל החזר מלא על הסכום המוכח.
- **מסלול חקלאות** - מסלול צפוני ייעודי לעסקים חקלאיים, פיצוי של 13,615 ש"ח לכל עובד המועסק בשטחים חקלאיים באזור המיוחד (עד תקרה של 5 מיליון ש"ח לחקלאי לכל תקופת הזכאות); לנתב מתקשרים חקלאיים לכאן ולא למסלול המחזורים הכללי.

לעבור על המסלולים הרלוונטיים עם המתקשר ולבחור את התשואה הגבוהה. שכירים ביישובים האלה מקבלים 100% מהשכר (לא 75%). לתשומת לב: פורטל המקדמה request-for-dvance-dealers-shaagat-haari הוא לעוסקים בכל הארץ מלבד יישובי קו העימות, ולכן עסק בגבול אינו משתמש בו - ליישובי קו העימות יש פורטל מקדמה נפרד (pay-advances-to-business-owners-in-frontier-roaring-lion), נוסף על הפיצוי המלא ללא תקרה במסלול האדום/מחזורים. חלונות ההגשה בצפון מאוחרים מהמסלול הארצי (אדום ~31.08.2026; מחזורים/שכר/חקלאות ~24.09.2026) - לאמת את התאריך החי בדף gov.il של המסלול.
