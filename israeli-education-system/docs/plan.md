# Israeli Education System Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for navigating the Israeli education system — Bagrut (matriculation) requirements, university admissions including the psychometric exam, Ministry of Education school data, and Hebrew education terminology.

**Architecture:** MCP Enhancement skill (Category 3). Guides users through Israeli education data, admissions processes, and system structure with references to official Ministry of Education and academic institution resources.

**Tech Stack:** SKILL.md, references for Ministry of Education data, NITE (National Institute for Testing and Evaluation) psychometric info, and university admissions requirements.

---

## Research

### Israeli Education System Structure
- **Gan (גן):** Kindergarten, ages 3-6, last year mandatory (Gan Chova)
- **Yesodi (יסודי):** Elementary school, grades 1-6, ages 6-12
- **Chativat Beinayim (חטיבת ביניים):** Middle school, grades 7-9, ages 12-15
- **Tichon (תיכון):** High school, grades 10-12, ages 15-18
- **Compulsory education:** Ages 3-18 (extended to age 3 in recent years)
- **School year:** September 1 to June 30 (roughly)
- **Streams:** Mamlachti (state), Mamlachti-Dati (state-religious), Charedi (ultra-Orthodox), Arab

### Bagrut (בגרות) — Matriculation Exams
- **Purpose:** National high school exit exams, university entrance prerequisite
- **Grades 10-12:** Exams taken over 3 years
- **Unit system:** Each subject has 1-5 units (yechidot limud / יחידות לימוד)
  - 5 units (highest level, weighted bonus for university)
  - 3 units (standard level)
  - 1 unit (basic)
- **Mandatory subjects:**
  - Hebrew (Lashon / לשון): 2 units minimum
  - English: 3-5 units
  - Mathematics: 3-5 units
  - Tanach (Bible): 2 units
  - History/Civics (Ezrachut): 2 units
  - Hebrew Literature (Sifrut): 2 units
- **Electives:** Physics, Chemistry, Biology, Computer Science, Arabic, French, Art, Music, etc.
- **Minimum for certificate:** Pass all mandatory subjects + total 21 units minimum
- **Bagrut certificate:** Te'udat Bagrut (תעודת בגרות)
- **Grade range:** 0-100, passing is typically 56+

### Psychometric Exam (פסיכומטרי)
- **Official name:** Mivkhan Psichometri (PET — Psychometric Entrance Test)
- **Administered by:** NITE (National Institute for Testing and Evaluation / מכון ניטו)
- **Website:** nite.org.il
- **Purpose:** University admissions standardized test
- **Sections:**
  - Quantitative Reasoning (Chashiva Kamutit): Math, logic
  - Verbal Reasoning (Chashiva Miluliti): Hebrew reading, vocabulary
  - English: Reading comprehension, vocabulary
- **Score range:** 200-800 (average ~530)
- **Languages:** Hebrew, Arabic, Russian, French, Spanish, combined
- **Frequency:** Up to 3 times total; can be taken in different languages
- **Cost:** ~500 NIS per sitting
- **Prep courses:** Common in Israel — Kidum, Yoel Geva, Atid, Psagot

### University Admissions
- **Sekhem (סכם):** Weighted composite score combining:
  - Bagrut average (with bonus for 5-unit subjects)
  - Psychometric score
  - Weight varies by university and program
- **Major universities:**
  - Hebrew University (האוניברסיטה העברית) — Jerusalem
  - Tel Aviv University (אוניברסיטת תל אביב)
  - Technion (הטכניון) — Haifa
  - Ben-Gurion University (אוניברסיטת בן גוריון) — Be'er Sheva
  - University of Haifa (אוניברסיטת חיפה)
  - Bar-Ilan University (אוניברסיטת בר-אילן) — Ramat Gan
  - Weizmann Institute (מכון ויצמן) — Rehovot (graduate only)
  - Open University (האוניברסיטה הפתוחה) — distance learning
- **Colleges (Michlalot):** IDC Herzliya (Reichman), Shenkar, Sapir, etc.
- **Mechina (מכינה):** Preparatory program for those without full Bagrut

### Ministry of Education Data
- **School database:** data.gov.il has school listings with details
- **RAMA (ראמ"ה):** National Authority for Measurement and Evaluation — school assessments
- **Meitzav (מיצ"ב):** National standardized tests (grades 2, 5, 8)
- **School data includes:** Name, city, sector, level, student count, teacher count
- **Data portal:** edu.gov.il (Ministry of Education)

### Use Cases
1. **Bagrut guidance** — Understand requirements, subject selection, scoring
2. **Psychometric prep** — Exam structure, scoring, preparation resources
3. **University admissions** — Sekhem calculation, program requirements
4. **School data** — Find school information from Ministry of Education data
5. **Education terminology** — Hebrew-English education term translation

---

## Build Steps

### Task 1: Create SKILL.md

**Files:**
- Create: `repos/government-services/israeli-education-system/SKILL.md`

```markdown
---
name: israeli-education-system
description: >-
  Navigate the Israeli education system including Bagrut (matriculation) exams,
  psychometric entrance test (PET), university admissions, and Ministry of
  Education school data. Use when user asks about Israeli schools, Bagrut
  requirements, psychometric exam, "psichometri", Israeli university admissions,
  sekhem calculation, Israeli education levels, Hebrew education terms, or
  school data from Ministry of Education. Covers K-12 system, exam structure,
  and higher education admissions. Do NOT use for non-Israeli education systems
  or post-graduate academic research.
license: MIT
allowed-tools: "Bash(python:*) WebFetch"
compatibility: "Requires network access for school data queries. No API keys needed for public education data."
metadata:
  author: skills-il
  version: 1.0.0
  category: government-services
  tags: [education, bagrut, psychometric, university, schools, hebrew, israel]
---

# Israeli Education System

## Instructions

### Step 1: Identify Education Query Type

| Query Type | Data Source | Key Topics |
|-----------|------------|------------|
| Bagrut requirements | Ministry of Education | Subjects, units, passing grades |
| Psychometric exam | NITE (nite.org.il) | Sections, scoring, registration |
| University admissions | University websites | Sekhem, requirements by program |
| School lookup | data.gov.il | School details, location, sector |
| Grade conversion | Ministry standards | Bagrut scoring, bonus calculations |

### Step 2: Israeli Education System Overview

**System structure:**
```
Age 3-6:    Gan (גן) — Kindergarten
            └── Gan Chova (mandatory, age 5-6)

Age 6-12:   Yesodi (יסודי) — Elementary School
            └── Grades 1-6 (Kitah Aleph through Vav)

Age 12-15:  Chativat Beinayim (חטיבת ביניים) — Middle School
            └── Grades 7-9 (Kitah Zayin through Tet)

Age 15-18:  Tichon (תיכון) — High School
            └── Grades 10-12 (Kitah Yud through Yud-Bet)
            └── Bagrut exams during this period

Age 18-21:  Military Service (Sherut Tzva'i) — Most Israelis
            └── IDF, National Service, or exemption

Age 21+:    Higher Education (Haskalah Gvoha)
            └── University, College, Mechina
```

**Education streams (Zeramim):**
| Stream | Hebrew | Description |
|--------|--------|-------------|
| State (Mamlachti) | ממלכתי | Secular public education |
| State-Religious (Mamlachti-Dati) | ממלכתי-דתי | Religious public education |
| Ultra-Orthodox (Charedi) | חרדי | Independent religious schools |
| Arab | ערבי | Arabic-language schools |
| Druze | דרוזי | Druze community schools |

### Step 3: Bagrut (Matriculation) Guidance

**Mandatory Bagrut subjects:**
```python
bagrut_requirements = {
    "mandatory": [
        {"subject": "Hebrew Language (לשון)", "min_units": 2, "type": "exam"},
        {"subject": "English (אנגלית)", "min_units": 3, "max_units": 5, "type": "exam"},
        {"subject": "Mathematics (מתמטיקה)", "min_units": 3, "max_units": 5, "type": "exam"},
        {"subject": "Bible (תנ\"ך)", "min_units": 2, "type": "exam"},
        {"subject": "Literature (ספרות)", "min_units": 2, "type": "exam"},
        {"subject": "History (היסטוריה)", "min_units": 2, "type": "exam"},
        {"subject": "Civics (אזרחות)", "min_units": 2, "type": "exam"},
    ],
    "minimum_total_units": 21,
    "passing_grade": 56,  # out of 100
    "certificate": "Te'udat Bagrut (תעודת בגרות)",
}

# 5-unit bonuses for university admission
five_unit_bonus = {
    "Mathematics_5": 35,    # Bonus points added to Bagrut average
    "English_5": 35,
    "Physics_5": 25,
    "Chemistry_5": 25,
    "Biology_5": 25,
    "Computer_Science_5": 25,
    "Arabic_5": 25,
    "French_5": 25,
}
```

**Bagrut average calculation for university:**
```python
def calculate_bagrut_average(subjects: list) -> dict:
    """
    Calculate weighted Bagrut average for university admissions.
    subjects: list of dicts with 'name', 'units', 'grade'
    """
    total_weighted = 0
    total_units = 0
    bonus_points = 0

    for subj in subjects:
        weighted = subj["grade"] * subj["units"]
        total_weighted += weighted
        total_units += subj["units"]

        # 5-unit bonus
        if subj["units"] == 5:
            if subj["name"] in ["Mathematics", "English"]:
                bonus_points += 35
            else:
                bonus_points += 25

    raw_average = total_weighted / total_units if total_units > 0 else 0
    boosted_average = min(raw_average + (bonus_points / len(subjects)), 120)

    return {
        "raw_average": round(raw_average, 2),
        "bonus_points": bonus_points,
        "boosted_average": round(boosted_average, 2),
        "total_units": total_units,
        "meets_minimum_units": total_units >= 21,
    }
```

### Step 4: Psychometric Exam (PET) Information

**Exam structure:**
```
Psychometric Entrance Test (PET / מבחן פסיכומטרי)

Sections:
1. Quantitative Reasoning (חשיבה כמותית)
   - Mathematics, data analysis, logic
   - Score: 50-150

2. Verbal Reasoning (חשיבה מילולית)
   - Hebrew reading comprehension, analogies, sentence completion
   - Score: 50-150

3. English (אנגלית)
   - Reading comprehension, vocabulary, sentence completion
   - Score: 50-150

Combined Score: 200-800
Average score: ~530
Duration: ~2.5 hours
Languages available: Hebrew, Arabic, Russian, French, Spanish, Combined
Attempts: Maximum 3 total (can be in different languages)
```

**Score interpretation:**
```python
psychometric_percentiles = {
    800: "99.9th percentile — top 0.1%",
    750: "99th percentile — top 1%",
    700: "95th percentile — top 5%",
    650: "85th percentile — top 15%",
    600: "70th percentile — top 30%",
    550: "50th percentile — median",
    500: "35th percentile",
    450: "20th percentile",
}

def interpret_psychometric_score(score: int) -> str:
    """Interpret a psychometric score."""
    if score >= 740:
        return "Excellent — eligible for most competitive programs (medicine, law at top universities)"
    elif score >= 680:
        return "Very good — eligible for competitive programs (CS, engineering at Technion/TAU)"
    elif score >= 620:
        return "Good — eligible for many university programs"
    elif score >= 550:
        return "Average — eligible for some university programs, most colleges"
    elif score >= 480:
        return "Below average — limited university options, consider mechina or college"
    else:
        return "Consider retaking, prep course, or alternative pathways"
```

**Preparation resources:**
| Provider | Type | Hebrew Name | Notes |
|----------|------|-------------|-------|
| Kidum | Prep course | קידום | Largest provider |
| Yoel Geva | Prep course | יואל גבע | Popular, intensive |
| Atid | Prep course | עתיד | Various formats |
| Psagot | Prep course | פסגות | Online and in-person |
| NITE practice | Official | מכון ניטו | Free practice materials on nite.org.il |

### Step 5: University Admissions

**Sekhem (סכם) — Composite Admission Score:**
```python
def estimate_sekhem(bagrut_avg: float, psychometric: int,
                    university: str = "general") -> dict:
    """
    Estimate university admission composite score (Sekhem).
    Weights vary by university and program — this is approximate.
    """
    # Typical weight distributions (vary by institution)
    weights = {
        "general": {"bagrut": 0.4, "psychometric": 0.6},
        "technion": {"bagrut": 0.35, "psychometric": 0.65},
        "hebrew_university": {"bagrut": 0.4, "psychometric": 0.6},
        "tel_aviv": {"bagrut": 0.45, "psychometric": 0.55},
    }

    w = weights.get(university, weights["general"])

    # Normalize scores to similar scale
    bagrut_normalized = bagrut_avg * 8  # Scale ~100 to ~800
    sekhem = (bagrut_normalized * w["bagrut"]) + (psychometric * w["psychometric"])

    return {
        "estimated_sekhem": round(sekhem, 1),
        "bagrut_component": round(bagrut_normalized * w["bagrut"], 1),
        "psychometric_component": round(psychometric * w["psychometric"], 1),
        "weights_used": w,
        "note": "Actual sekhem calculation varies by university and program. Check specific program requirements."
    }
```

**Approximate admission thresholds (sekhem):**
| Program | University | Approx. Sekhem |
|---------|-----------|----------------|
| Medicine | Hebrew University | 740+ |
| Computer Science | Technion | 700+ |
| Law | Tel Aviv University | 680+ |
| Engineering | Ben-Gurion | 640+ |
| Business Admin | Bar-Ilan | 600+ |
| Social Sciences | University of Haifa | 560+ |
| Mechina (prep year) | Various | Below admission threshold |

### Step 6: School Data Lookup

**Query Ministry of Education school data:**
```python
import requests

def search_schools(city: str = "", school_type: str = ""):
    """Search Israeli school database via data.gov.il."""
    base_url = "https://data.gov.il/api/3/action/datastore_search"
    # School resource IDs vary — search for latest education dataset
    params = {
        "resource_id": "SCHOOL_RESOURCE_ID",  # Get from data.gov.il search
        "limit": 50,
    }

    filters = {}
    if city:
        filters["city_name"] = city  # May be in Hebrew
    if school_type:
        filters["school_type"] = school_type

    if filters:
        import json
        params["filters"] = json.dumps(filters)

    response = requests.get(base_url, params=params)
    return response.json()
```

**Education terminology glossary:**
| Hebrew | Transliteration | English |
|--------|----------------|---------|
| בגרות | Bagrut | Matriculation exams |
| יחידות לימוד | Yechidot Limud | Study units (credit level) |
| תעודת בגרות | Te'udat Bagrut | Matriculation certificate |
| פסיכומטרי | Psichometri | Psychometric entrance test |
| סכם | Sekhem | Composite admission score |
| מכינה | Mechina | Pre-academic preparatory program |
| מגמה | Megama | Major/specialization (high school) |
| כיתה | Kita | Class/grade |
| מורה | Moreh/Mora | Teacher (m/f) |
| מנהל | Menahel | Principal |
| בית ספר | Beit Sefer | School |
| אוניברסיטה | Universita | University |
| מכללה | Michlala | College |
| תואר ראשון | Toar Rishon | Bachelor's degree (BA/BSc) |
| תואר שני | Toar Sheni | Master's degree (MA/MSc) |
| דוקטורט | Doktorat | Doctorate (PhD) |
| מלגה | Milga | Scholarship |
| שכר לימוד | Schar Limud | Tuition |
| מעונות | Me'onot | Dormitories |

## Examples

### Example 1: Bagrut Planning
User says: "My daughter is starting 10th grade, what Bagrut subjects should she take?"
Actions:
1. List mandatory subjects and minimum units
2. Ask about her interests and university goals
3. Recommend elective subjects and unit levels
4. Explain 5-unit bonus system for university
5. Calculate estimated units and university readiness
Result: Personalized Bagrut subject plan with university admission context.

### Example 2: Psychometric Preparation
User says: "I got 580 on the psychometric, what are my university options?"
Actions:
1. Interpret score (slightly above average, ~55th percentile)
2. List eligible programs by university
3. Discuss retake strategy if higher score needed
4. Suggest preparation resources
5. Present alternative pathways (mechina, Open University)
Result: Realistic program options with improvement plan.

### Example 3: School Information
User says: "Find elementary schools in Ra'anana"
Actions:
1. Query data.gov.il for schools in Ra'anana
2. Filter by elementary level (Yesodi)
3. Present list with stream (Mamlachti, Mamlachti-Dati), size
4. Note any RAMA assessment data if available
Result: Structured school list for the requested city and level.

## Troubleshooting

### Issue: "School data not found"
Cause: City name may need Hebrew spelling, or dataset may be outdated
Solution: Search in Hebrew (e.g., "רעננה" instead of "Ra'anana"). Check data.gov.il for the most recent education dataset.

### Issue: "Sekhem calculation doesn't match university website"
Cause: Each university and program uses different weights and formulas
Solution: This skill provides estimates. For exact sekhem, use the specific university's admissions calculator (usually available on their website during application period).

### Issue: "Bagrut requirements changed"
Cause: Ministry of Education periodically updates requirements
Solution: Check edu.gov.il for the most current Bagrut requirements. The core mandatory subjects are stable, but unit requirements and elective options may change.
```

**Step 2: Create references**
- `references/bagrut-subjects-guide.md` — Complete list of Bagrut subjects with unit levels and exam details
- `references/university-admissions-table.md` — Admission requirements by university and popular programs
- `references/education-glossary.md` — Comprehensive Hebrew-English education terminology

**Step 3: Validate and commit**
