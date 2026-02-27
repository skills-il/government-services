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
allowed-tools: 'Bash(python:*) WebFetch'
compatibility: >-
  Requires network access for school data queries. No API keys needed for public
  education data.
metadata:
  author: skills-il
  version: 1.0.0
  category: government-services
  tags:
    - education
    - bagrut
    - psychometric
    - university
    - schools
    - hebrew
    - israel
  display_name:
    he: מערכת חינוך ישראלית
    en: Israeli Education System
  display_description:
    he: 'בגרויות, פסיכומטרי, קבלה לאוניברסיטאות ומידע על מוסדות לימוד'
    en: >-
      Navigate the Israeli education system including Bagrut (matriculation)
      exams, psychometric entrance test (PET), university admissions, and
      Ministry of Education school data. Use when user asks about Israeli
      schools, Bagrut requirements, psychometric exam, "psichometri", Israeli
      university admissions, sekhem calculation, Israeli education levels,
      Hebrew education terms, or school data from Ministry of Education. Covers
      K-12 system, exam structure, and higher education admissions. Do NOT use
      for non-Israeli education systems or post-graduate academic research.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - openclaw
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
Age 3-6:    Gan -- Kindergarten
            Gan Chova (mandatory, age 5-6)

Age 6-12:   Yesodi -- Elementary School
            Grades 1-6 (Kitah Aleph through Vav)

Age 12-15:  Chativat Beinayim -- Middle School
            Grades 7-9 (Kitah Zayin through Tet)

Age 15-18:  Tichon -- High School
            Grades 10-12 (Kitah Yud through Yud-Bet)
            Bagrut exams during this period

Age 18-21:  Military Service (Sherut Tzva'i) -- Most Israelis
            IDF, National Service, or exemption

Age 21+:    Higher Education (Haskalah Gvoha)
            University, College, Mechina
```

**Education streams (Zeramim):**
| Stream | Hebrew | Description |
|--------|--------|-------------|
| State (Mamlachti) | mamlachti | Secular public education |
| State-Religious (Mamlachti-Dati) | mamlachti-dati | Religious public education |
| Ultra-Orthodox (Charedi) | charedi | Independent religious schools |
| Arab | aravi | Arabic-language schools |
| Druze | druzi | Druze community schools |

### Step 3: Bagrut (Matriculation) Guidance

**Mandatory Bagrut subjects:**
| Subject | Hebrew | Min Units |
|---------|--------|-----------|
| Hebrew Language | Lashon | 2 |
| English | Anglit | 3-5 |
| Mathematics | Matematika | 3-5 |
| Bible | Tanach | 2 |
| Literature | Sifrut | 2 |
| History | Historia | 2 |
| Civics | Ezrachut | 2 |

**Requirements for certificate:**
- Pass all mandatory subjects (56+ out of 100)
- Minimum 21 total study units
- Certificate name: Te'udat Bagrut

**5-unit bonuses for university admission:**
- Mathematics 5 units: +35 bonus points
- English 5 units: +35 bonus points
- Science/Language 5 units: +25 bonus points each

### Step 4: Psychometric Exam (PET) Information

**Exam structure:**
| Section | Hebrew | Score Range |
|---------|--------|-------------|
| Quantitative Reasoning | Chashiva Kamutit | 50-150 |
| Verbal Reasoning | Chashiva Miluliti | 50-150 |
| English | Anglit | 50-150 |

**Overall score:** 200-800 (average ~530)

**Score interpretation:**
| Score | Percentile | Competitiveness |
|-------|-----------|-----------------|
| 740+ | 99th | Medicine, law at top universities |
| 680+ | 95th | CS, engineering at Technion/TAU |
| 620+ | 85th | Many university programs |
| 550 | 50th | Some university, most colleges |
| Below 480 | Below 20th | Consider mechina or retake |

**Key facts:**
- Maximum 3 attempts total
- Available in Hebrew, Arabic, Russian, French, Spanish
- Cost: ~500 NIS per sitting
- Popular prep courses: Kidum, Yoel Geva, Atid, Psagot

### Step 5: University Admissions

**Sekhem (composite admission score) calculation:**
Each university weights Bagrut and Psychometric differently:
- Typical: 40% Bagrut + 60% Psychometric (varies by program)
- Technion: 35% Bagrut + 65% Psychometric
- Tel Aviv University: 45% Bagrut + 55% Psychometric

**Major universities:**
| University | Hebrew | City | Strengths |
|-----------|--------|------|-----------|
| Hebrew University | ha-universita ha-ivrit | Jerusalem | Research, humanities, sciences |
| Tel Aviv University | universitat tel aviv | Tel Aviv | Largest, diverse programs |
| Technion | ha-technion | Haifa | Engineering, CS, technology |
| Ben-Gurion University | universitat ben gurion | Beer Sheva | Engineering, desert research |
| University of Haifa | universitat haifa | Haifa | Social sciences, marine |
| Bar-Ilan University | universitat bar ilan | Ramat Gan | Law, social sciences |
| Weizmann Institute | machon weizmann | Rehovot | Graduate science only |
| Open University | ha-universita ha-ptuchah | Distance | Open admissions |

**Approximate admission thresholds (sekhem):**
| Program | Top Universities | Mid-tier |
|---------|-----------------|----------|
| Medicine | 740+ | N/A |
| Computer Science | 700+ | 640+ |
| Law | 680+ | 620+ |
| Engineering | 660+ | 600+ |
| Business | 620+ | 560+ |
| Social Sciences | 560+ | 500+ |

### Step 6: Education Terminology Glossary
| Hebrew | Transliteration | English |
|--------|----------------|---------|
| bagrut | Bagrut | Matriculation exams |
| yechidot limud | Yechidot Limud | Study units (credit level) |
| teudat bagrut | Te'udat Bagrut | Matriculation certificate |
| psichometri | Psichometri | Psychometric entrance test |
| sekhem | Sekhem | Composite admission score |
| mechina | Mechina | Pre-academic preparatory program |
| megama | Megama | Major/specialization (high school) |
| kita | Kita | Class/grade |
| moreh/mora | Moreh/Mora | Teacher (m/f) |
| menahel | Menahel | Principal |
| beit sefer | Beit Sefer | School |
| universita | Universita | University |
| michlala | Michlala | College |
| toar rishon | Toar Rishon | Bachelor's degree |
| toar sheni | Toar Sheni | Master's degree |
| doktorat | Doktorat | Doctorate (PhD) |
| milga | Milga | Scholarship |
| schar limud | Schar Limud | Tuition |
| meonot | Me'onot | Dormitories |

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

## Bundled Resources

### Scripts
- `scripts/calculate_sekhem.py` — Calculate weighted Bagrut averages with 5-unit bonus points, estimate university admission composite scores (sekhem) for specific universities, interpret psychometric exam scores with percentile rankings, and display admission thresholds for popular programs. Supports subcommands: `bagrut`, `sekhem`, `psychometric`, `thresholds`. Run: `python scripts/calculate_sekhem.py --help`

### References
- `references/education-glossary.md` — Hebrew-English glossary of Israeli education terms covering system levels (gan through tichon), exam terminology (bagrut, yechidot limud, sekhem), education streams (mamlachti, charedi, aravi), mandatory Bagrut subject requirements, and all major universities with locations. Consult when translating education terms or explaining system structure.

## Troubleshooting

### Issue: "School data not found"
Cause: City name may need Hebrew spelling, or dataset may be outdated
Solution: Search in Hebrew. Check data.gov.il for the most recent education dataset.

### Issue: "Sekhem calculation does not match university website"
Cause: Each university and program uses different weights and formulas
Solution: This skill provides estimates. For exact sekhem, use the specific university's admissions calculator (usually available on their website during application period).

### Issue: "Bagrut requirements changed"
Cause: Ministry of Education periodically updates requirements
Solution: Check edu.gov.il for the most current Bagrut requirements. The core mandatory subjects are stable, but unit requirements and elective options may change.