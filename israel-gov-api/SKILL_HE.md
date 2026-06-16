---
name: israel-gov-api
description: >-
  Discover, query, and analyze Israeli government open data from data.gov.il
  (CKAN API). Use when user asks about Israeli government data, "data.gov.il",
  government datasets, CBS statistics, or needs data about Israeli
  transportation, education, health, geography, economy, or environment.
  Supports dataset search, tabular data queries, and analysis guidance. Pair
  with the MCP servers listed below for direct tool access from your agent.
  Do NOT use for classified government data or data requiring security
  clearance.
license: MIT
allowed-tools: 'Bash(python:*) WebFetch'
compatibility: >-
  Requires network access for data.gov.il API. Enhanced by datagov-mcp or
  data-gov-il-mcp servers.
metadata:
  author: skills-il
  version: 1.3.0
  category: government-services
  tags:
    he:
      - ממשל
      - נתונים
      - CKAN
      - סטטיסטיקה
      - מידע-פתוח
      - ישראל
    en:
      - government
      - data
      - ckan
      - statistics
      - open-data
      - israel
  mcp-server: datagov-mcp
  display_name:
    he: ממשקי API ממשלתיים
    en: Israel Gov Api
  display_description:
    he: >-
      Wrapper על CKAN API של data.gov.il לגילוי, חיפוש ושאילתות על datasets
      ממשלתיים ישראליים פתוחים (תחבורה, חינוך, בריאות, סטטיסטיקה, נדל"ן,
      רכבים, עמותות ועוד). השתמשו כשמשתמש מבקש מידע פתוח מ-data.gov.il או
      שואל על datasets ממשלתיים, נתוני למ"ס, מרשם רכב, רשימת מוסדות חינוך
      או נתוני בריאות. הסקיל מסביר את שרשרת הקריאות הנכונה (package_search
      ואז package_show ואז datastore_search), מטפל בקידוד עברי ב-URL (חובה
      percent-encoding), בעקיפת ה-WAF ("Security Violation" כשמקבלים 403),
      ודפדוף בעזרת offset (data.gov.il לא תומך ב-keyset paging על _id).
      התאימו ל-MCP servers המתועדים למטה לגישה ישירה ככלים. אל תשתמשו
      ב-data.gov.il עבור APIs ממשלתיים סגורים או דורשי הזדהות, לאלה יש
      סקילים נפרדים.
    en: >-
      Discover, query, and analyze Israeli government open data from data.gov.il
      (CKAN API). Use when user asks about Israeli government data,
      "data.gov.il", government datasets, CBS statistics, or needs data about
      Israeli transportation, education, health, geography, economy, or
      environment. Supports dataset search, tabular data queries, and analysis
      guidance. Pair with the MCP servers listed below for direct tool access
      from your agent. Do NOT use for classified government data or data
      requiring security clearance.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - antigravity
---

# ממשקי API ממשלתיים - ישראל

## הוראות

### שלב 1: תבינו מה המשתמש צריך
תשאלו את המשתמש:
- **באיזה נושא?** (תחבורה, בריאות, חינוך, כלכלה וכו')
- **באיזה אזור?** (ארצי, עיר או אזור ספציפי, כתובת מסוימת)
- **באיזו תקופה?** (עכשיו, היסטורי, סדרה לאורך זמן)
- **באיזה פורמט?** (נתונים גולמיים, סטטיסטיקה מסכמת, ויזואליזציה)

### שלב 2: חיפוש datasets
תשתמשו ב-API של data.gov.il (מבוסס CKAN) כדי למצוא datasets רלוונטיים:

**חיפוש לפי מילת מפתח:**
```
GET https://data.gov.il/api/3/action/package_search?q=KEYWORD&rows=10
```

**חיפוש לפי ארגון (משרד ממשלתי):**
```
GET https://data.gov.il/api/3/action/package_search?fq=organization:MINISTRY_ID
```

**מזהי ארגונים נפוצים:**
| משרד | מזהה | שם באנגלית |
|------|------|------------|
| הלשכה המרכזית לסטטיסטיקה | lamas | Central Bureau of Statistics |
| משרד התחבורה | ministry_of_transport | Ministry of Transportation |
| משרד הבריאות | ministry-health | Ministry of Health |
| משרד החינוך | ministry_of_education | Ministry of Education |
| רשות המסים | taxes-authority | Israel Tax Authority |
| רשות מקרקעי ישראל | the_israel_lands_administration | Israel Land Authority |
| משרד הפנים | interior_affairs | Ministry of Interior |

### שלב 3: שליפה ושאילתה
אחרי שמצאתם את ה-dataset:

**קבלת פרטי dataset:**
```
GET https://data.gov.il/api/3/action/package_show?id=DATASET_ID
```

**שאילתה על נתונים טבלאיים (datastore):**
```
GET https://data.gov.il/api/3/action/datastore_search?resource_id=RESOURCE_ID&limit=100
```

**סינון לפי ערכי שדות:**
```
GET https://data.gov.il/api/3/action/datastore_search?resource_id=RESOURCE_ID&filters={"field_name":"value"}&limit=100
```

**בחירת שדות ספציפיים ומיון:**
```
GET https://data.gov.il/api/3/action/datastore_search?resource_id=RESOURCE_ID&fields=field1,field2&sort=field1 desc&limit=100
```

**חיפוש טקסט חופשי במשאב:**
```
GET https://data.gov.il/api/3/action/datastore_search?resource_id=RESOURCE_ID&q=search+term&limit=100
```

**שימו לב:** ה-endpoint `datastore_search_sql` לפעמים מושבת ב-data.gov.il (מחזיר 403 Forbidden). תשתמשו ב-`datastore_search` עם הפרמטרים `filters`, `fields`, `sort`, `q`, `limit` ו-`offset` במקום.

**טיפים:**
- שמות השדות בדרך כלל בעברית, תריצו `datastore_search` עם `limit=1` קודם כדי לראות את שמות השדות
- הפרמטר `filters` מקבל אובייקט JSON להתאמה מדויקת (למשל `filters={"city_code":"5000"}`)
- הפרמטר `q` לחיפוש טקסט חופשי בכל השדות
- ל-datasets גדולים, תשתמשו ב-`limit` ו-`offset` לדפדוף
- שדות תאריך מגיעים בפורמטים שונים, תבדקו את תיעוד ה-dataset

**דפדוף (pagination):**
- דפדוף offset עמוק נעשה איטי וכבד יותר ככל שמתקדמים ב-datasets גדולים. אין תקרה קשיחה (offset גבוה עדיין מחזיר נתונים), אבל העלות גדלה עם ה-offset.
- דפדפו עם `limit` + `offset`: התגובה מחזירה `_links.next` (כתובת הדף הבא מבוססת offset) שאפשר לעקוב אחריה, או להגדיל `offset` ידנית. ה-`filters` של data.gov.il עושה התאמה מדויקת בלבד, ולכן אין keyset/cursor paging על `_id`: `filters={"_id":">N"}` מחזיר `success:false`.
- לשליפות גדולות מאוד או של טבלה שלמה, הורידו את ה-CSV של המשאב ישירות (`resources[].url` מ-`package_show`) או השתמשו ב-`records_format=csv`, במקום לדפדף את כל הטבלה דרך ה-API.
- השדה `total` בתגובה הוא ספירה של כל הרשומות במשאב (לא רק בדף), השתמשו בו לתכנון מספר הדפים.
- הפרמטר `records_format` מקבל את הערכים `objects` (ברירת מחדל), `lists` (מערכים לפי מיקום), `csv` ו-`tsv`. `lists` ו-`csv` מהירים וזולים בהרבה לשליפות גדולות, כדאי בסטרימינג או חילוץ בכמויות.

### שלב 4: ניתוח והצגה
אחרי שיש לכם את הנתונים:
1. תסכמו את הממצאים העיקריים בשפה פשוטה
2. תחשבו סטטיסטיקות בסיסיות אם צריך (ממוצע, חציון, מגמות)
3. תציעו ויזואליזציות (תרשים עמודות, גרף קווי, מפה) שמתאימות לנתונים
4. תציינו את תאריך העדכון האחרון וכל הסתייגות רלוונטית
5. תספקו קישור ישיר ל-dataset ב-data.gov.il

### שלב 5: הצלבת נתונים (מתקדם)
כשמשלבים כמה datasets:
1. תזהו מפתחות משותפים (קוד יישוב, תאריך, קוד קטגוריה)
2. תשתמשו בקודים מנהליים ישראליים (קודי יישוב של הלמ"ס) לחיבור גיאוגרפי
3. שימו לב ששמות שדות בין datasets שונים לא תמיד זהים, תתאימו לפי תוכן ולא לפי שם
4. תתעדו את מקור הנתונים: אילו datasets תרמו לניתוח

## datasets נפוצים

מזהי המשאבים שלמטה אומתו ב-16/6/2026 מול ה-API החי דרך `datastore_search?resource_id=<id>&limit=1`. מזהי משאבים ב-data.gov.il כן משתנים בלי התראה, תאמתו אותם מחדש לפני שאתם מצטטים למשתמש.

| dataset | מזהה משאב | תיאור |
|---------|-----------|-------|
| כלי רכב פרטיים ומסחריים (רישוי) | `053cea08-09bc-40ec-8f7a-156f0677aff3` | מרשם מלא של לוחיות רישוי של כלי רכב פרטיים ומסחריים, כולל יצרן, דגם ושנה. כ-4.1 מיליון שורות. |
| כלי רכב ציבוריים | `cf29862d-ca25-4691-84f6-1be60dcb4a1e` | לוחיות רישוי של כלי רכב בתחבורה ציבורית פעילים (אוטובוסים, מוניות). כ-65 אלף שורות. |
| מוסדות חינוך (`mosdot`) | `5548fd63-5868-4053-ad81-98caddc5e232` | מאפייני מוסדות חינוך בפיקוח משרד החינוך. כ-120 אלף שורות. |
| עמותות רשומות | `be5b7935-3922-45d4-9638-08871b17ec95` | מרשם משרד המשפטים של עמותות וחברות לתועלת הציבור. כ-75 אלף שורות. |

לתחומים אחרים (GTFS תחבורה ציבורית, עסקאות נדל"ן, מדדי איכות בתי חולים, איכות אוויר), השתמשו ב-`package_search` כדי לגלות את ה-dataset הנוכחי, ואז ב-`package_show` כדי לקבל את `resources[].id` הפעיל. המזהים האלה מתחלפים כשה-dataset מתעדכן משנה לשנה.

## דוגמאות

### דוגמה 1: חיפוש נתוני בתי ספר (workflow מלא עם שרשור קריאות)
המשתמש אומר: "אני צריך נתונים על בתי ספר בתל אביב"

פעולות (אל תדלגו על שלבי האיתור, מזהי משאבים מתחלפים):

1. חיפוש datasets רלוונטיים:
   ```
   curl -s "https://data.gov.il/api/3/action/package_search?q=mosdot&rows=5"
   ```
2. בדיקת ה-dataset שנבחר ושליפת `resources[].id` הפעיל:
   ```
   curl -s "https://data.gov.il/api/3/action/package_show?id=mosdot" \
     | python3 -c "import sys,json; r=json.load(sys.stdin)['result']['resources']; [print(x['id'], x['format'], x.get('name','')) for x in r]"
   ```
3. הצצה לשמות שדות עם `limit=1`:
   ```
   curl -s "https://data.gov.il/api/3/action/datastore_search?resource_id=5548fd63-5868-4053-ad81-98caddc5e232&limit=1"
   ```
4. משאב המוסדות חושף את היישוב כשדה שם `שם ישוב` (טקסט שם היישוב, למשל `תל אביב - יפו`), לא כקוד מספרי. סננו לפי שם היישוב (או השתמשו ב-`q=` לחיפוש חופשי); עברית חייבת להיות מקודדת ב-percent-encoding:
   ```
   # חיפוש חופשי למוסדות בתל אביב (q = "תל אביב", מקודד)
   curl -s "https://data.gov.il/api/3/action/datastore_search?resource_id=5548fd63-5868-4053-ad81-98caddc5e232&q=%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91&limit=100"
   ```
   קוד היישוב המספרי של הלמ"ס (תל אביב-יפו 5000, חיפה 4000, ירושלים 3000) הוא השדה `סמל_ישוב`, אבל הוא נמצא ב-dataset היישובים של הלמ"ס (משאב `5c78e9fa-c2e2-4771-93ff-7f400a12f7ba`), לא במשאב המוסדות. בצעו join לפי שם היישוב כשצריך את הקוד.

תוצאה: רשימת בתי ספר מובנית עבור תל אביב (מספר, סוגים, גדלים).

### דוגמה 2: ניתוח מחירי דיור
המשתמש אומר: "הראה לי מגמות מחירי דיור בחיפה"

פעולות:
1. `package_search?q=nadlan` או `q=%D7%A2%D7%A1%D7%A7%D7%90%D7%95%D7%AA` כדי לאתר את ה-dataset של עסקאות נדל"ן ברשות המסים.
2. `package_show?id=<slug>` ושליפת מזהה המשאב של השנה העדכנית מתוך `resources[]`.
3. `datastore_search` עם סינון לקוד יישוב חיפה, מסודר לפי תאריך עסקה יורד.
4. קיבוץ לפי חודש, חישוב מחיר חציוני למטר רבוע, חישוב אחוז שינוי חודש מול חודש קודם.

תוצאה: מגמת מחירים חודשית לחיפה עם ניתוח.

### דוגמה 3: השוואת נתונים מוניציפליים
המשתמש אומר: "תשווי לי הוצאות חינוך בין ערים בישראל"

פעולות:
1. `package_search?q=%D7%AA%D7%A7%D7%A6%D7%99%D7%91%20%D7%97%D7%99%D7%A0%D7%95%D7%9A` (תקציב + חינוך בעברית, מקודד).
2. בחירת dataset של תקציבים מוניציפליים, `package_show` כדי לקבל את מזהה המשאב הפעיל.
3. `datastore_search` עם סינון לשורות בקטגוריית חינוך; דפדוף עם offset (או הורדת ה-CSV של המשאב) למשאבים גדולים.
4. נרמול לנפש בעזרת נתוני אוכלוסיה של `lamas` (למ"ס).

תוצאה: השוואה מדורגת של הוצאות חינוך לתלמיד בין רשויות מקומיות גדולות, כולל מקור הנתונים והשנה.

## משאבים מצורפים

### סקריפטים
- `scripts/query_datagov.py` -- חיפוש datasets, בדיקת משאבים והרצת שאילתות datastore ישירות מול ה-API של data.gov.il (CKAN) משורת הפקודה. תומך בפקודות משנה: `search`, `dataset`, `query`, `orgs`. להרצה: `python scripts/query_datagov.py --help`

### חומרי עזר
- `references/ckan-api-reference.md` -- קטלוג מלא של endpoints ל-API של data.gov.il (CKAN) כולל פרמטרי חיפוש, תחביר שאילתות datastore ומזהי ארגונים נפוצים. תסתכלו עליו כשאתם בונים קריאות API או מנסים לדבג תחביר של שאילתה.

## MCP servers מומלצים

תצמידו את הסקיל ל-MCP server כדי שהסוכן יוכל לקרוא ל-data.gov.il (או ל-dataset נגזר) ישירות ככלים, בלי לבנות קריאות HTTP ידנית.

| MCP | קישור | מה מקבלים |
|-----|-------|-----------|
| `datagov-israel` | https://agentskills.co.il/he/mcp/datagov-israel | גישה ישירה ככלי MCP ל-CKAN API של data.gov.il (search, package_show, datastore_search). |
| `data-gov-il` | https://agentskills.co.il/he/mcp/data-gov-il | MCP חלופי שעוטף את אותו CKAN API של data.gov.il. |
| `israel-vehicles` | https://agentskills.co.il/he/mcp/israel-vehicles | MCP ממוקד ל-dataset של רישוי כלי רכב (חיפוש לפי לוחית, יצרן, דגם, שנה). |
| `israel-amutot` | https://agentskills.co.il/he/mcp/israel-amutot | MCP ממוקד למרשם העמותות של משרד המשפטים. |
| `israel-elections` | https://agentskills.co.il/he/mcp/israel-elections | MCP ממוקד לנתוני תוצאות הבחירות בישראל. |

כשהסקיל מנחה את המשתמש דרך שאילתה, תעדיפו את ה-MCP הייעודי אם הוא מותקן; אחרת ליפלו ל-CKAN API הגולמי.

## מלכודות נפוצות
- ממשקי API ממשלתיים (data.gov.il) משנים תדיר כתובות URL ומבני endpoints בלי התראה. סוכנים לפעמים מקודדים endpoints שעבדו בחודש שעבר אבל עכשיו מחזירים 404. תאמתו מזהי משאבים מחדש עם `package_show` לפני שאתם מצטטים אותם.
- ה-API של data.gov.il מחזיר נתונים עם כותרות עמודות בעברית כברירת מחדל. סוכנים עלולים להיכשל בפענוח תגובות עם שמות לא-ASCII ב-JSON או CSV.
- ערכי סינון ופרמטרי `q` בעברית חייבים להיות מקודדים ב-UTF-8 percent-encoding. עברית גולמית ב-URL שוברת כמה לקוחות HTTP (חלק מהגרסאות של `curl`, גרסאות ישנות של `requests`, חלק מה-proxies). דוגמה: חיפוש "רכב" כ-`q=%D7%A8%D7%9B%D7%91`; סינון "חיפה" כ-`filters=%7B%22city%22%3A%22%D7%97%D7%99%D7%A4%D7%94%22%7D`.
- הגבלת הקצב ב-APIs ממשלתיים מחמירה ולא מתועדת. סוכנים ששולחים בקשות רצופות מהר ייחסמו. תוסיפו השהיות בין קריאות.
- תשובה 403 עם גוף `Security Violation` היא ה-WAF של data.gov.il שמסיים את ה-session, זה שונה מ-403 של הרשאה. שחזור: backoff אקספוננציאלי (10ש', 30ש', 60ש'), זריקת cookies של session ושליחה מחדש עם `User-Agent` חדש. אל תנסו שוב בלולאה צמודה, ה-WAF יאריך את החסימה.
- הרבה datasets ממשלתיים שומרים תאריכים בפורמט DD/MM/YYYY (הפורמט הישראלי), לא ISO 8601. סוכנים עלולים לפענח "01/02/2026" כ-1 בפברואר במקום 2 בינואר.
- דפדוף offset עמוק נעשה איטי יותר ב-datasets גדולים (אין תקרה קשיחה, אבל offset גבוה יקר). data.gov.il לא תומך ב-keyset paging על `_id` (ה-`filters` עושה התאמה מדויקת בלבד, כך ש-`{"_id":">N"}` נכשל); לשליפות מלאות, הורידו את ה-CSV של המשאב במקום לדפדף את כל הטבלה.

## קישורי עזר

| מקור | כתובת | מה לבדוק |
|------|-------|----------|
| פורטל data.gov.il | https://data.gov.il | קטלוג מידע פתוח ישראלי, ארגונים, datasets |
| תיעוד CKAN API | https://docs.ckan.org/en/latest/api/ | חתימות `package_search`, `package_show`, `datastore_search` |
| רשימת datasets | https://data.gov.il/dataset | חיפוש לפי ארגון ותגיות |
| הלשכה המרכזית לסטטיסטיקה | https://www.cbs.gov.il | מקור של הרבה מהסטטיסטיקות שמפורסמות ב-data.gov.il |
| נתוני בנק ישראל | https://www.boi.org.il | נתונים כלכליים ומוניטריים שלא נמצאים ב-data.gov.il |

## פתרון בעיות

### שגיאה: "Dataset not found"
סיבה: מונחי חיפוש ספציפיים מדי או בשפה לא נכונה
פתרון: תנסו מילות מפתח רחבות יותר בעברית. רוב הנתונים הממשלתיים הם בעברית.

### שגיאה: "Datastore not available"
סיבה: לא לכל המשאבים יש API של datastore מופעל
פתרון: תורידו את ה-CSV או Excel ישירות ותעבדו עליו מקומית.

### שגיאה: "403 Forbidden" בשאילתות SQL
סיבה: ה-endpoint `datastore_search_sql` לפעמים מושבת ב-data.gov.il
פתרון: תשתמשו ב-`datastore_search` עם `filters`, `fields`, `sort` ו-`q` במקום. לדוגמה: `datastore_search?resource_id=ID&filters={"city":"Haifa"}&fields=field1,field2&sort=field1 desc&limit=100`

### שגיאה: "Hebrew field names"
סיבה: רוב ה-datasets הממשלתיים משתמשים בשמות עמודות בעברית
פתרון: תריצו שאילתה ראשונה עם `limit=1` כדי לראות את כל שמות השדות, ואז תבנו שאילתות ממוקדות.
