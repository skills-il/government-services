---
name: israel-gov-api
description: >-
  Discover, query, and analyze Israeli government open data from data.gov.il
  (CKAN API). Use when user asks about Israeli government data, "data.gov.il",
  government datasets, CBS statistics, or needs data about Israeli
  transportation, education, health, geography, economy, or environment.
  Supports dataset search, tabular data queries, and analysis guidance. Enhances
  existing datagov-mcp and data-gov-il-mcp servers with workflow best practices.
  Do NOT use for classified government data or data requiring security
  clearance.
license: MIT
allowed-tools: 'Bash(python:*) WebFetch'
compatibility: >-
  Requires network access for data.gov.il API. Enhanced by datagov-mcp or
  data-gov-il-mcp servers.
metadata:
  author: skills-il
  version: 1.2.0
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
    he: גישה למידע ממשלתי פתוח מתוך data.gov.il
    en: >-
      Discover, query, and analyze Israeli government open data from data.gov.il
      (CKAN API). Use when user asks about Israeli government data,
      "data.gov.il", government datasets, CBS statistics, or needs data about
      Israeli transportation, education, health, geography, economy, or
      environment. Supports dataset search, tabular data queries, and analysis
      guidance. Enhances existing datagov-mcp and data-gov-il-mcp servers with
      workflow best practices. Do NOT use for classified government data or data
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

| dataset | מזהה משאב | תדירות עדכון | תיאור |
|-------------|-----------|--------------|-------|
| נתוני תחבורה ציבורית GTFS | שונים | יומי | לוחות זמנים ומסלולי אוטובוסים ורכבות |
| רשימת בתי ספר | שונים | שנתי | כל בתי הספר עם פרטים מלאים |
| איכות בתי חולים | שונים | רבעוני | מדדי איכות של משרד הבריאות |
| מחירי נדל"ן | שונים | חודשי | מחירי עסקאות מרשות המסים |
| מרשם עסקים | שונים | יומי | עסקים פעילים |
| איכות אוויר | שונים | שעתי | תחנות ניטור סביבתי |

## דוגמאות

### דוגמה 1: חיפוש נתוני בתי ספר
המשתמש אומר: "אני צריך נתונים על בתי ספר בתל אביב"
פעולות:
1. חיפוש: `package_search?q=schools+tel+aviv`
2. איתור dataset חינוך וקבלת מזהה המשאב
3. שאילתה: סינון לפי קוד יישוב של תל אביב (5000)
4. הצגה: מספר בתי ספר, סוגים, גדלים
תוצאה: נתוני בתי ספר מובנים עבור תל אביב

### דוגמה 2: ניתוח מחירי דיור
המשתמש אומר: "הראה לי מגמות מחירי דיור בחיפה"
פעולות:
1. איתור dataset עסקאות נדל"ן של רשות המסים
2. סינון לפי קוד יישוב חיפה, 12 חודשים אחרונים
3. חישוב מחיר חציוני למטר רבוע לפי חודש
4. הצגת מגמה עם אחוזי שינוי
תוצאה: מגמת מחירים חודשית לחיפה עם ניתוח

## משאבים מצורפים

### סקריפטים
- `scripts/query_datagov.py` — חיפוש datasets, בדיקת משאבים והרצת שאילתות datastore ישירות מול ה-API של data.gov.il (CKAN) משורת הפקודה. תומך בפקודות משנה: `search`, `dataset`, `query`, `orgs`. להרצה: `python scripts/query_datagov.py --help`

### חומרי עזר
- `references/ckan-api-reference.md` — קטלוג מלא של endpoints ל-API של data.gov.il (CKAN) כולל פרמטרי חיפוש, תחביר שאילתות datastore ומזהי ארגונים נפוצים. תסתכלו עליו כשאתם בונים קריאות API או מנסים לדבג תחביר של שאילתה.

## מלכודות נפוצות
- ממשקי API ממשלתיים (data.gov.il) משנים תדיר כתובות URL ומבני endpoints בלי התראה. סוכנים לפעמים מקודדים endpoints שעבדו בחודש שעבר אבל עכשיו מחזירים 404.
- ה-API של data.gov.il מחזיר נתונים עם כותרות עמודות בעברית כברירת מחדל. סוכנים עלולים להיכשל בפענוח תגובות עם שמות לא-ASCII ב-JSON או CSV.
- הגבלת הקצב ב-APIs ממשלתיים מחמירה ולא מתועדת. סוכנים ששולחים בקשות רצופות מהר ייחסמו. תוסיפו השהיות בין קריאות.
- הרבה datasets ממשלתיים שומרים תאריכים בפורמט DD/MM/YYYY (הפורמט הישראלי), לא ISO 8601. סוכנים עלולים לפענח "01/02/2026" כ-1 בפברואר במקום 2 בינואר.

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
