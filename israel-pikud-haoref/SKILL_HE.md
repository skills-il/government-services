---
name: israel-pikud-haoref
description: >-
  Integrate with Israel's Home Front Command (Pikud HaOref) real-time alert
  system — rocket alerts, earthquake warnings, and civil defense notifications.
  Use this skill when working with oref.org.il APIs, "Tzeva Adom", "Red Alert
  Israel", "פיקוד העורף", "צבע אדום", "pikud haoref", real-time alert
  monitoring, or any integration with Israel's civil defense infrastructure.
  Do NOT use for non-Israeli civil defense systems, US/UK weather alerts,
  or generic push-notification frameworks.
license: MIT
allowed-tools: 'Bash(curl:*) Bash(python:*) Bash(node:*) WebFetch'
compatibility: >-
  Code examples require network access. The official oref.org.il API geo-blocks
  non-Israeli IPs; deploy on GCP me-west1 (Tel Aviv) or use Tzofar alternative
  endpoints (no geo-blocking) for historical data.
metadata:
  author: noypearl
  version: 1.0.0
  category: government-services
  tags:
    he:
      - התרעות
      - פיקוד-העורף
      - צבע-אדום
      - טילים
      - חירום
      - ישראל
    en:
      - alerts
      - red-alert
      - israel
      - pikud-haoref
      - tzeva-adom
      - oref
      - civil-defence
  display_name:
    he: פיקוד העורף - התרעות בזמן אמת
    en: Pikud HaOref Red Alert
  display_description:
    he: >-
      שילוב מערכת ההתרעות של פיקוד העורף — התרעות טילים, רעידות אדמה ועדכוני
      הגנה אזרחית בזמן אמת. השתמש כאשר עובדים עם oref.org.il, "צבע אדום",
      "פיקוד העורף", "Red Alert", ובוט התרעות.
    en: >-
      Integrate with Israel's Home Front Command (Pikud HaOref) real-time alert
      system — rocket alerts, earthquake warnings, and civil defense
      notifications. Use for oref.org.il APIs, "Tzeva Adom", "Red Alert Israel",
      "פיקוד העורף", "צבע אדום", and Israeli civil defense integrations.
      Do NOT use for non-Israeli civil defense or generic push-notification
      frameworks.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - openclaw
    - antigravity
---

# שילוב מערכת ההתרעות של פיקוד העורף

## הוראות שימוש

### שלב 1: הבהרת מטרת השימוש

שאל את המשתמש מה הוא רוצה לבנות:

- **ניטור בזמן אמת** — סקירה (polling) של `alerts.json` כל 1–2 שניות
- **בוט התרעות** — Telegram, Slack, Discord (השימוש הנפוץ ביותר)
- **ניתוח היסטורי** — שאילתה של `AlertsHistory.json` או `GetAlarmsHistory.aspx`
- **לוח בקרה / מפה** — ממסר SSE או WebSocket עם לקוח Leaflet.js
- **Home Assistant** — הפניה ל-`oref_alert` דרך HACS או `RedAlert` דרך AppDaemon
- **התרעות לפי מיקום ספציפי** — cities.json עם חיפוש תת-מחרוזת בשמות עבריים

### שלב 2: טיפול בחסימה גיאוגרפית מראש

**קריטי:** ממשק ה-API הרשמי של oref.org.il עשוי לחסום כתובות IP שאינן ישראליות (חסימה מבוססת CDN/Akamai). זהו הגורם הנפוץ ביותר לשגיאות 403 בלתי צפויות. בדוק את הסביבה שלך תחילה — החסימה אינה עקבית תמיד עבור IPs שאינם ישראליים.

**פתרון עוקף:** פרוס על GCP `me-west1` (אזור תל אביב). שים לב: `e2-micro` אינו זכאי לשכבה חינמית ב-`me-west1`, אך הוא האפשרות הזולה ביותר עם כתובת IP ישראלית.

```bash
# Deploy to GCP Tel Aviv region for an Israeli IP
gcloud compute instances create pikud-haoref \
  --zone=me-west1-a \
  --machine-type=e2-micro \
  --image-family=debian-12 \
  --image-project=debian-cloud \
  --tags=http-server

gcloud compute firewall-rules create allow-pikud-haoref \
  --allow=tcp:8000-8002 --target-tags=http-server
```

**חלופה (ללא חסימה גיאוגרפית):** השתמש ב-endpoints של Tzofar (`api.tzevaadom.co.il`) לנתונים היסטוריים. אזהרה: Tzofar אינו כולל התרעות מקדימות (קטגוריה 14) ואינו כולל הודעות סיום אירוע (קטגוריה 13).

### שלב 3: בחירת גישת שילוב

- **שליטה מלאה / תלויות מינימליות** → HTTP fetch ישיר (ראה דפוסים להלן)
- **Node.js עם העשרת ערים** → `pikud-haoref-api` (npm) — כולל מסד נתוני cities.json
- **Python עם callbacks** → `python-red-alert` (pip)
- **Home Assistant** → אינטגרציית `oref_alert` דרך HACS
- **שילוב עוזר AI** → שרת MCP `pikud-a-oref-mcp`

---

## תיעוד ממשק ה-API

### התרעות בזמן אמת

סקירה כל 1–2 שניות. זהו צילום מצב מידי — התרעות מופיעות רק בזמן שצופר פעיל (שניות עד ~דקה).

```
GET https://www.oref.org.il/warningMessages/alert/alerts.json
```

**כותרות HTTP נדרשות:**
```
Referer: https://www.oref.org.il/
X-Requested-With: XMLHttpRequest
Accept: application/json
```

**תגובה כאשר התרעה פעילה:**
```json
{
  "id": "134168709720000000",
  "cat": "1",
  "title": "ירי רקטות וטילים",
  "data": ["תל אביב - מרכז העיר", "רמת גן - מערב"],
  "desc": "היכנסו למרחב המוגן ושהו בו 10 דקות"
}
```

**שדות התגובה:**

| שדה | סוג | תיאור |
|-----|-----|--------|
| `id` | string | מזהה התרעה ייחודי — לשימוש בהכחדת כפילויות |
| `cat` | string | מספר קטגוריה (ראה טבלה להלן) |
| `title` | string | סוג ההתרעה בעברית |
| `data` | string[] | שמות ישובים מושפעים בעברית |
| `desc` | string | הוראות הגנה בעברית |

**תגובה כאשר אין התרעה:** HTTP 200 עם גוף ריק `""` — ייתכן ויופיע BOM של UTF-8 (`\uFEFF`) לפניו. יש תמיד לנקות את ה-BOM לפני JSON.parse. אין לטפל בתגובה ריקה כשגיאה.

**⚠️ `alerts.json` ריק אינו אומר "מצב תקין".** התרעות נעלמות מה-endpoint הזה תוך שניות. כדי לקבוע אם מצב עדיין פעיל, יש לבדוק גם את endpoint ההיסטוריה לאיתור רשומת קטגוריה 13 "האירוע הסתיים" תואמת.

### היסטוריית התרעות

**ראשי (מומלץ — יציב יותר תחת עומס):**
```
GET https://alerts-history.oref.org.il/Shared/Ajax/GetAlarmsHistory.aspx?lang=he&mode=1
```

**גיבוי:**
```
GET https://www.oref.org.il/warningMessages/alert/History/AlertsHistory.json
```

שניהם מוגבלים ל-**3,000 רשומות ללא עימוד וללא סינון לפי תאריך**. בעת עימות פעיל, 3,000 רשומות עלולות להתמלא תוך פחות משעתיים. שדה `data` בהיסטוריה הוא **מחרוזת מופרדת בפסיקים**, לא מערך (שלא כמו ה-endpoint של זמן אמת).

```json
[{
  "alertDate": "2024-10-15 14:32:00",
  "title": "ירי רקטות וטילים",
  "data": "אשדוד - א,ב,ד,ה",
  "category": 1
}]
```

כל חותמות הזמן הן ב**שעון ישראל (`Asia/Jerusalem`)** — לטיפול בשינויי שעון קיץ השתמש ב-`zoneinfo.ZoneInfo("Asia/Jerusalem")` ב-Python 3.9 ומעלה.

### קטגוריות התרעה

```
GET https://www.oref.org.il/alerts/alertCategories.json
```

| קטגוריה | סוג |
|----------|-----|
| 1 | ירי רקטות וטילים |
| 2 | חדירת כלי טיס עוין |
| 3 | רעידת אדמה |
| 4 | צונאמי |
| 5 | אירוע רדיולוגי |
| 6 | חומרים מסוכנים |
| 7 | חדירת מחבלים |
| 13 | האירוע הסתיים — אות "מצב תקין" סמכותי לפי ישוב |
| 14 | בדקות הקרובות צפויות להתקבל התרעות — התרעה מקדימה |
| 101–107 | שווי תרגיל לקטגוריות 1–7 — סנן אלא אם כן רוצה נתוני תרגיל |

---

## דפוסי מימוש

### 1. לולאת סקירה — Node.js (`pikud-haoref-api`)

```javascript
// npm install pikud-haoref-api
// NOTE: Deploy on GCP me-west1 (Tel Aviv) if you get 403 geo-blocked errors

const { HaOrefClient } = require('pikud-haoref-api');

const client = new HaOrefClient({
  intervalMs: 2000,   // poll every 2 seconds
  language: 'he',    // or 'en' for English city names
});

client.on('alert', async (alert) => {
  // alert.cities — city names resolved via cities.json
  // alert.countdown — seconds to shelter per city
  console.log(`התרעה: ${alert.title} ב-${alert.cities.join(', ')}`);
});

client.on('error', (err) => console.error('Poll error:', err));
client.start();
```

### 2. לולאת סקירה — Python (`python-red-alert`)

```python
# pip install python-red-alert
# NOTE: Deploy on GCP me-west1 (Tel Aviv) if you get 403 geo-blocked errors

from red_alert import RedAlert

ra = RedAlert(interval=2)  # poll every 2 seconds

@ra.on_alert
def handle_alert(alert):
    print(f"התרעה: {alert.title} ב-{', '.join(alert.areas)}")

ra.start()  # blocking; use ra.start_async() with aiohttp for async
```

### 3. Fetch ישיר עם ניקוי BOM — JavaScript

```javascript
// NOTE: Deploy on GCP me-west1 (Tel Aviv) if you get 403 geo-blocked errors

const ENDPOINT = 'https://www.oref.org.il/warningMessages/alert/alerts.json';
const HEADERS = {
  'Referer': 'https://www.oref.org.il/',
  'X-Requested-With': 'XMLHttpRequest',
  'Accept': 'application/json',
};

const seen = new Set();

async function pollAlerts() {
  try {
    const res  = await fetch(ENDPOINT, { headers: HEADERS });
    const raw  = await res.text();
    const text = raw.replace(/^\uFEFF/, '').trim(); // strip UTF-8 BOM
    if (!text || text === '[]') return;             // no active alert — not an error
    const alert = JSON.parse(text);
    if (alert.id && !seen.has(alert.id)) {
      seen.add(alert.id);
      console.log(`התרעה: ${alert.title}`, alert.data);
    }
  } catch (err) {
    console.error('Poll error:', err.message);
  }
}

setInterval(pollAlerts, 2000);
pollAlerts();
```

### 4. Fetch ישיר עם ניקוי BOM — Python

```python
import requests, json, time

# NOTE: Deploy on GCP me-west1 (Tel Aviv) if you get 403 geo-blocked errors
# For async, replace requests with aiohttp and use asyncio

ENDPOINT = 'https://www.oref.org.il/warningMessages/alert/alerts.json'
HEADERS  = {
    'Referer': 'https://www.oref.org.il/',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0',
}

seen_ids = set()

def poll():
    try:
        resp = requests.get(ENDPOINT, headers=HEADERS, timeout=5)
        text = resp.text.lstrip('\ufeff').strip()   # strip UTF-8 BOM
        if not text or text == '[]':
            return  # no active alert — not an error
        alert = json.loads(text)
        if alert.get('id') and alert['id'] not in seen_ids:
            seen_ids.add(alert['id'])
            print(f"התרעה: {alert['title']} ב-{', '.join(alert['data'])}")
    except Exception as e:
        print(f'Poll error: {e}')

while True:
    poll()
    time.sleep(2)
```

### 5. התרעה בבוט Telegram

```python
import requests as rq

# NOTE: Deploy on GCP me-west1 (Tel Aviv) if you get 403 geo-blocked errors
# Store BOT_TOKEN and CHAT_ID in environment variables, not in source code

BOT_TOKEN = "your-bot-token"   # from @BotFather
CHAT_ID   = "your-chat-id"     # channel or user chat ID

def notify_telegram(alert):
    cities = ", ".join(alert["data"])
    text   = f"🚨 {alert['title']}\n📍 {cities}\n⚠️ {alert['desc']}"
    rq.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text},
        timeout=5,
    )

# Wire into the polling loop above — replace print(...) with notify_telegram(alert)
```

עבור Slack (incoming webhook) ו-Discord (webhook), אותו דפוס חל — החלף את יעד `rq.post` ופורמט ה-payload.

### 6. סינון לפי ערים מרובות

```python
# NOTE: Deploy on GCP me-west1 (Tel Aviv) if you get 403 geo-blocked errors

WATCHED = {
    "Tel Aviv HQ":          ["תל אביב"],
    "Haifa R&D":            ["חיפה"],
    "Beer Sheva warehouse": ["באר שבע"],
}

def on_new_alert(alert):
    affected = alert.get("data", [])
    for office, hebrew_names in WATCHED.items():
        for name in hebrew_names:
            # Substring match handles "תל אביב - מרכז העיר" when watching "תל אביב"
            if any(name in loc for loc in affected):
                notify_team(office, alert)  # your notification function
                break
```

### 7. שאילתת היסטוריית התרעות

```python
import requests, json

# NOTE: Deploy on GCP me-west1 (Tel Aviv) if you get 403 geo-blocked errors
# GetAlarmsHistory.aspx is more reliable than AlertsHistory.json under heavy load

HISTORY_URL = (
    "https://alerts-history.oref.org.il/Shared/Ajax/GetAlarmsHistory.aspx"
    "?lang=he&mode=1"
)
HEADERS = {
    "Referer": "https://www.oref.org.il/",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json",
}

resp    = requests.get(HISTORY_URL, headers=HEADERS, timeout=10)
text    = resp.text.lstrip('\ufeff').strip()  # strip UTF-8 BOM
history = json.loads(text)                    # list of alert records

# Filter rockets (cat 1) mentioning Tel Aviv in the last ~3,000 records
rockets = [
    h for h in history
    if h.get("category") == 1 and "תל אביב" in h.get("data", "")
]
print(f"נמצאו {len(rockets)} התרעות רקטות עבור תל אביב")
```

---

## נתוני מיקום — cities.json

חבילת npm `pikud-haoref-api` כוללת `cities.json`: ~1,500 ישובים ישראליים עם שמות רב-לשוניים, קואורדינטות GPS, שיוכי אזור, וזמני הגנה.

```json
{
  "id": 511,
  "name": "אבו גוש",
  "name_en": "Abu Ghosh",
  "name_ru": "Абу Гош",
  "name_ar": "أبو غوش",
  "zone": "שפלת יהודה",
  "zone_en": "Judean Lowlands",
  "lat": 31.80686,
  "lng": 35.11038,
  "countdown": 90,
  "value": "אבו גוש"
}
```

**שדות מפתח:**

- `countdown` — שניות למרחב המוגן (0 עבור ישובי עוטף עזה, עד 90 עבור הצפון). יש תמיד לדווח על זה — קריטי לבטיחות חיים.
- `value` — לשימוש להתאמה מול רשומות מערך `data` בהתרעה.
- `lat` / `lng` — לסמנים במפה ולשאילתות קרבה.

**אסטרטגיית התאמה:** מחרוזות מיקום בהתרעה כוללות סיומות תת-אזור (למשל `"תל אביב - מרכז העיר"`). השתמש ב**חיפוש תת-מחרוזת** (`"תל אביב" in loc`) ולא בהשוואה מדויקת.

**פתרון אנגלית לעברית:** חפש ב-`name_en` עם התאמה מקורבת. השתמש ב-`name_ru` / `name_ar` עבור דוברי רוסית וערבית.

---

## ספריות קהילתיות

| שפה | ספרייה | התקנה | הערות |
|-----|---------|--------|-------|
| Node.js | `pikud-haoref-api` | `npm install pikud-haoref-api` | כולל cities.json, שמות ערים באנגלית, זמני הגנה |
| Python | `python-red-alert` | `pip install python-red-alert` | מבוסס callbacks; תומך ב-async דרך `aiohttp` |
| C# | `RedAlert` | NuGet | תמיכה רב-לשונית (עברית/אנגלית/רוסית/ערבית) |
| Docker | `orefAlerts` | Docker Hub | poller בקונטיינר עם פלט webhook |
| שרת MCP | `pikud-a-oref-mcp` | ראה repo | שילוב עוזר AI דרך FastAPI SSE על פורט 8000 |
| Home Assistant | `oref_alert` | HACS | הגדרה אוטומטית לפי מיקום הבית; ישות `sensor.oref_alert` |
| Home Assistant | `RedAlert` | AppDaemon | אוטומציות מבוססות סקריפט עם שליטה מדויקת |

---

## טיפול בשגיאות

| מצב | משמעות | פעולה |
|-----|---------|--------|
| HTTP 403 | חסימה גיאוגרפית, או חסר פלח `/alert/` בנתיב ה-URL | פרוס על GCP me-west1; ודא ש-URL כולל את הפלח `/alert/` |
| HTTP 200, גוף ריק | אין התרעה פעילה | מצב תקין — אל תזרוק שגיאה |
| `\uFEFF` בתחילה | UTF-8 BOM | נקה עם `.lstrip('\ufeff')` לפני JSON.parse |
| JSON פגום | שחיתות אקראית ב-endpoint ההיסטוריה תחת עומס | נסה שנית לאחר 2–3 שניות |
| היסטוריה מחזירה גוף ריק | `AlertsHistory.json` מידרדר תחת עומס בעת עימות | עבור ל-`GetAlarmsHistory.aspx` על `alerts-history.oref.org.il` |

---

## הערות אבטחה

- לא נדרש אימות לאף endpoint — API ציבורי לקריאה בלבד.
- לא מעורב מידע אישי.
- אין סודות לנהל עבור ה-API של פיקוד העורף עצמו.
- אחסן `BOT_TOKEN` של Telegram, webhook URLs של Slack ו-Discord במשתני סביבה — לעולם אל תכתב אותם קשה בקוד המקור.
- הגבל סקירות ל-1–2 שניות; סקירה מהירה יותר מסכנת חסימת IP.

---

## דוגמאות

### דוגמה 1: בוט Telegram להתרעות רקטות

1. טפל בחסימה גיאוגרפית מראש — הצע GCP me-west1 או בדיקה מקומית תחילה.
2. השתמש בדפוס 4 (לולאת סקירה Python גולמית) עם `on_new_alert` שקורא לדפוס 5 (התרעת Telegram).
3. סנן לפי `alert.get("cat") == "1"` אם רוצים רקטות/טילים בלבד.
4. הצע אחסון `BOT_TOKEN` ו-`CHAT_ID` בקובץ `.env`.
5. תוצאה: בוט פועל באזור תל אביב, שולח הודעה בכל התרעה חדשה.

### דוגמה 2: "האם יש התרעה באשקלון עכשיו?"

1. משוך `alerts.json` ונקה BOM.
2. חפש תת-מחרוזת `"אשקלון"` במערך `data` — מטפל בתת-אזורים `"אשקלון - צפון"`, `"אשקלון - דרום"`.
3. בדוק גם היסטוריה לוודא שלא התקבל קטגוריה 13 "האירוע הסתיים" לאשקלון מאז ההתרעה האחרונה מסוגים 1–7.
4. דווח על זמן ההגנה: אשקלון = 30 שניות (`countdown: 30` ב-cities.json).

### דוגמה 3: לוח בקרה של מפה חיה

1. צד שרת: לולאת סקירה → הפצה דרך SSE או WebSocket (אל תאפשר לדפדפנים לפנות ישירות ל-oref.org.il).
2. צד לקוח: Leaflet.js + אריחי OpenStreetMap + סמנים ממוקמים לפי `lat`/`lng` מ-cities.json.
3. הוסף לכל tooltip שם אזור (`zone`) וזמן הגנה (`countdown`).
4. עדכן סמנים בזמן אמת; הסר סמנים לאחר קבלת קטגוריה 13 "האירוע הסתיים".

### דוגמה 4: שילוב ב-Home Assistant

1. התקן `oref_alert` דרך HACS בממשק Home Assistant.
2. הגדר עם עיר הבית — האינטגרציה פותרת אוטומטית שמות מיקום בעברית.
3. ישויות: `sensor.oref_alert` (מצב התרעה נוכחי) ו-`sensor.oref_alert_time_to_shelter` (ספירה לאחור בשניות).
4. אוטומציות נפוצות: הבהוב אורות חכמים באדום, השהיית מדיה, נעילת דלתות, הכרזה דרך רמקולים חכמים.

### דוגמה 5: ניתוח היסטורי (שבוע האחרון)

1. החלט אם צריך התרעות מקדימות (קטגוריה 14) — אם כן, חייב להיות poller רציף שפעל; אין מקור רטרואקטיבי.
2. להתרעות איום בלבד: משוך `GetAlarmsHistory.aspx?lang=he&mode=1`.
3. בתקופות עצימות, 3,000 רשומות עשויות לכסות כמה שעות בלבד — השתמש בארכיב Tzofar לחלונות ארוכים יותר (ראה `references/alternative-data-sources.md`).
4. נרמל חותמות זמן לאזור זמן `Asia/Jerusalem` לפני קיבוץ לפי יום/שעה.

---

## משאבים מצורפים

### סקריפטים

- `scripts/poll_alerts.py` — כלי שורת פקודה לסקירת התרעות פיקוד העורף בזמן אמת. תומך בסינון לפי עיר, קטגוריה ופורמט פלט (טקסט רגיל או JSON). כולל ניקוי BOM וכחדת כפילויות. הפעל: `python scripts/poll_alerts.py --help`

### חומרי עזר

- `references/alternative-data-sources.md` — endpoints של Tzofar (tzevaadom.co.il), מיפוי קטגוריות בין oref ל-Tzofar, פרויקטי ארכיב קהילתיים, ואסטרטגיות לנתונים היסטוריים מעבר למגבלת 3,000 הרשומות. עיין כאשר צריך נתונים היסטוריים ישנים משעות ספורות, או חלופה ללא חסימה גיאוגרפית.
- `references/community-libraries.md` — מדריך מפורט לכל הספריות הקהילתיות: `pikud-haoref-api` (Node.js), `python-red-alert`, `RedAlert` (C#), `orefAlerts` (Docker), `pikud-a-oref-mcp` (MCP), ואינטגרציות Home Assistant. כולל פקודות התקנה, חתימות API ומגבלות ידועות. עיין כאשר בוחרים ספרייה או מאבחנים בעיות ספציפיות לספרייה.

---

## מלכודות נפוצות

- **UTF-8 BOM** — ה-endpoint של זמן אמת פולט לעתים `\uFEFF` לפני ה-JSON. נקה עם `.lstrip('\ufeff')` (Python) או `.replace(/^\uFEFF/, '')` (JS) לפני כל JSON.parse.
- **גוף ריק ≠ שגיאה** — HTTP 200 עם גוף ריק אומר אין התרעה פעילה. טפל בהחזרה מוקדמת.
- **סוג שדה `data` שונה לפי endpoint** — זמן אמת: מערך מחרוזות. היסטוריה: מחרוזת מופרדת בפסיקים. אל תניח פורמט אחד בקוד משותף.
- **מגבלת 3,000 רשומות בהיסטוריה** — אין עימוד. במרץ 2026, המגבלה נוצלה תוך ~97 דקות. השתמש בארכיב Tzofar או ב-poller עצמאי רציף להיסטוריה ארוכה יותר.
- **התרעות מקדימות קטגוריה 14 אינן זמינות רטרואקטיבית** — Tzofar אינו כולל אותן. הדרך היחידה לנתוני התרעה מקדימה היסטוריים היא הפעלת poller רציף לפני התקופה הנדרשת.
- **אזור זמן ישראל** — כל חותמות הזמן של oref הן ב-`Asia/Jerusalem` (שעון ישראל מקומי), לא UTC. השתמש ב-`zoneinfo.ZoneInfo("Asia/Jerusalem")` ב-Python 3.9 ומעלה.
- **התרעות תרגיל** — קטגוריות 101–107 הן שווי תרגיל של 1–7. סנן אותן אלא אם כן רוצה נתוני תרגיל.
- **נתיב ה-URL — פלח `/alert/` נדרש** — `/warningMessages/alert/alerts.json` ✓ — `/warningMessages/alerts.json` → 403.
- **התרעות מרובות בו-זמנית** — בעת מטחים, מספר סוגי התרעות יכולים להיות פעילים בו-זמנית. תמיד טפל ב-`data` כמערך.
- **אל תפציץ את ה-API** — סקירה מרבית כל 1–2 שניות. בקשות עודפות מסכנות חסימת IP.

---

## פתרון בעיות

### שגיאה: "403 Forbidden" מ-oref.org.il

**סיבה א׳:** חסימה גיאוגרפית — כתובת IP שאינה ישראלית.
**פתרון:** פרוס על GCP `me-west1` (תל אביב). נסה מקומית תחילה — החסימה אינה תמיד עקבית.
**סיבה ב׳:** חסר פלח `/alert/` בנתיב ה-URL.
**פתרון:** ודא שה-URL הוא `https://www.oref.org.il/warningMessages/alert/alerts.json`.

### שגיאה: "JSON parse error" או "Unexpected token"

**סיבה:** UTF-8 BOM `\uFEFF` בתחילת התגובה, או JSON פגום אקראי מ-endpoint ההיסטוריה.
**פתרון:** נקה BOM לפני פענוח. אם מ-endpoint ההיסטוריה — נסה שנית לאחר 2–3 שניות.

### שגיאה: "ההיסטוריה תמיד מחזירה גוף ריק"

**סיבה:** `AlertsHistory.json` מידרדר תחת עומס שרת כבד בעת עימות.
**פתרון:** עבור ל-`GetAlarmsHistory.aspx` על `alerts-history.oref.org.il` — תת-הדומיין הזה נשאר זמין בזמן הסלמה.

### שגיאה: "עיר לא נמצאת בנתוני ההתרעה"

**סיבה:** רשומות `data` בהתרעה כוללות סיומות תת-אזור (למשל `"תל אביב - מרכז העיר"`).
**פתרון:** השתמש בחיפוש תת-מחרוזת ולא בהשוואה מדויקת: `"תל אביב" in location_string`.

### חשש: "ההתרעה נעלמה מ-alerts.json לאחר 10 שניות"

**סיבה:** צפוי — `alerts.json` הוא צילום מצב חי, לא סטטוס מתמשך.
**פתרון:** כחד כפילויות לפי `id`. אחסן התרעות מקומית כשמופיעות. השתמש ב-endpoint ההיסטוריה לתפיסת כל דבר שפוספס בין סקירות.

---

## קרדיט

ידע API, פרטי endpoints, דפוסי טיפול ב-BOM, עקיפות חסימה גיאוגרפית ואזכורי ספריות קהילתיות נגזרו מה-plugin של Claude [yaniv-golan/pikud-haoref-alerts](https://github.com/yaniv-golan/pikud-haoref-alerts) מאת Yaniv Golan (MIT).
