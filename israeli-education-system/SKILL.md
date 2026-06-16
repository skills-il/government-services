---
name: israeli-education-system
description: Navigate the Israeli education system including Bagrut (matriculation) exams, psychometric entrance test (PET), university admissions, and Ministry of Education school data. Use when user asks about Israeli schools, Bagrut requirements, psychometric exam, "psichometri", Israeli university admissions, sekhem calculation, Israeli education levels, Hebrew education terms, or school data from Ministry of Education. Covers K-12 system, exam structure, and higher education admissions. Do NOT use for non-Israeli education systems or post-graduate academic research.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Requires network access for school data queries. No API keys needed for public education data.
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
- English 5 units: +25 bonus points (NOT +35; the +35 bonus is reserved for math)
- Sciences (Physics, Chemistry, Biology, Computer Science) 5 units: +25 each
- Extra-language 5 units (Arabic, French, etc.): +25
- Stacking rule at most universities: math 5yl combined with two science 5yl typically earns +30 per science instead of +25

Note: Exact bonus tables vary by university and program. The values above reflect the canonical 2026 cycle; verify the program's published bonus table before quoting a number to a user.

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
- No cap on retake attempts (NITE removed the prior 8-attempt limit years ago); the highest score counts.
- Available in Hebrew, Arabic, Russian, French, Spanish.
- Cost (2026): approximately 560 NIS standard registration (per the NITE price sheet); late registration adds a surcharge. Always verify the current sitting fee on nite.org.il/test-dates-and-prices before quoting.
- Popular prep courses: Kidum, High-Q, Yoel Geva, Psagot.

**IMPORTANT, December 2026 PET restructure:**
NITE is removing English from the main psychometric. From the December 2026 sitting onward:
- The PET shrinks to 2 sections (Verbal + Quantitative), ~2.5 hours total.
- English moves to a separate computerized test called **Amirnett** (אמירנט).
- The restructure affects admissions only from academic year תשפ"ח (starting October 2027); each institution decides whether to keep using the PET English score in the sekhem until then. Confirm the current schedule on nite.org.il before advising whether a student should sit the legacy 3-section format or the new structure. Universities that previously used the PET English score will gradually migrate to Amirnett.

### Step 4.5: English Placement Tests (Distinct from Bagrut English)

Bagrut English measures high-school proficiency. University English placement uses separate NITE tests, and many students don't realize they're different exams:

| Test | Hebrew | Purpose |
|------|--------|---------|
| Amir | אמי"ר | English-level placement (paper-based). Same content domain as the PET English section. Sat by students who skipped PET English or want to re-sit only English. |
| Amiram | אמיר"ם | Computerized equivalent of Amir; more frequent sittings, faster results. |
| Yael | יע"ל | Hebrew proficiency for non-Hebrew speakers. Required for most olim and international students. |

**English level brackets (universities place students into one of five tracks):**

| Bracket | Hebrew | Implication |
|---------|--------|-------------|
| Pre-Basic | טרום בסיסי | Must take Pre-Basic English course before degree starts |
| Basic | בסיסי | Must take Basic English course |
| Advanced A | מתקדמים א | Must take Advanced A English course |
| Advanced B | מתקדמים ב | Must take Advanced B English course |
| Exempt (Patur) | פטור | No English coursework required during the degree |

PET / Amir / Amiram English score determines the bracket. From December 2026, **Amirnett** replaces PET English as the standalone computerized English test. NITE source: nite.org.il/other-tests/amir, /amiram, /yael.

### Step 5: University Admissions

**Sekhem (composite admission score) calculation:**
Each university (and each faculty within a university) weights Bagrut and Psychometric differently, and weights shift between admission cycles. The illustrative ranges below are starting points only, always verify on the program's official admissions calculator before quoting a number to a user:
- Typical: 40% Bagrut + 60% Psychometric (varies by program)
- Technion: roughly 35% Bagrut + 65% Psychometric, with program-specific 5-unit-Math / 5-unit-English thresholds for CS and engineering
- Tel Aviv University: roughly 40% Bagrut + 60% Psychometric, with Bagrut average multiplied by ×1.25 in the formula. Medicine requires the centralized **MOR Multi-Mini Interview** on top of sekhem (see Step 5.5).
- Hebrew University, Ben-Gurion, Bar-Ilan, Haifa: each publishes its own per-faculty formula on its admissions site

**Major universities (11 CHE-recognized as of 2026):**
| University | Hebrew | City | Strengths |
|-----------|--------|------|-----------|
| Hebrew University | ha-universita ha-ivrit | Jerusalem | Research, humanities, sciences |
| Tel Aviv University | universitat tel aviv | Tel Aviv | Largest, diverse programs |
| Technion | ha-technion | Haifa | Engineering, CS, technology |
| Ben-Gurion University | universitat ben gurion | Beer Sheva | Engineering, desert research |
| University of Haifa | universitat haifa | Haifa | Social sciences, marine |
| Bar-Ilan University | universitat bar ilan | Ramat Gan | Law, social sciences |
| Weizmann Institute | machon weizmann | Rehovot | Graduate science only |
| Open University | ha-universita ha-ptuchah | Distance | Open admissions (no Bagrut/PET required for course enrollment) |
| Reichman University | universitat raichman | Herzliya | Business, law, government (granted university status by CHE in 2021; formerly IDC) |
| Ariel University | universitat ariel | Ariel | Engineering, sciences (granted university status in 2012) |
| University of Kiryat Shmona and the Galilee | universitat kiryat shmona ve-ha-galil | Kiryat Shmona | Biotech, education, psychology, nutrition (CHE-approved ~20 Jan 2026, effective 2026/27 academic year (תשפ"ז), 5-year provisional recognition; ex-Tel-Hai Academic College) |

**Approximate admission thresholds (sekhem):**
| Program | Top Universities | Mid-tier |
|---------|-----------------|----------|
| Medicine | 740+ | N/A |
| Computer Science | 700+ | 640+ |
| Law | 680+ | 620+ |
| Engineering | 660+ | 600+ |
| Business | 620+ | 560+ |
| Social Sciences | 560+ | 500+ |

### Step 5.5: Medicine Admissions (MOR Multi-Mini Interview)

Most Israeli medical schools (TAU, Hebrew U, BGU, Bar-Ilan/Tzfat, Technion, Ariel) require the **MOR** (מו"ר) selection process (a multi-station assessment center) administered centrally by NITE, in addition to sekhem:

- **Registration window**: spring to early summer (for 2026 the biographical-questionnaire registration ran in early-mid June; assessment centers run roughly late May to July) via nite.org.il/other-tests/mor. Verify the current cycle's exact dates.
- **Format**: in-person, multi-station Hebrew interviews
- **Capacity-limited**: registration closes well before the medical-school application deadline; missing this window means missing the entire admissions cycle for medicine
- **Hard pre-screen**: a student with sekhem 740+ who skips MOR is auto-rejected from medicine
- **Fee**: separate from PET, posted annually on nite.org.il
- No exemption for atuda candidates or olim, the MOR is required across the board

A student aiming for medicine who only optimizes Bagrut + Psychometric will fail admissions. Always flag MOR registration windows when advising medicine applicants.

### Step 6: Alternative Admission Routes

Not every path into Israeli higher education runs through Bagrut + Psychometric. The major alternatives:

**Mechina (pre-academic preparatory program):**
- Recognized mechinot are subsidized by the Ministry of Education for periphery residents, post-army, lone soldiers, olim chadashim, and single parents (Vaadat Hatziduk eligibility groups). Many students are entitled to fully-funded mechina but never apply because they default to PET prep.
- Completion grade above the program-specific threshold (often ≥85) substitutes for both Bagrut average AND psychometric in many programs. Verify per-program: not universal.
- Mechina-Aharei-Tzava (post-army mechina) is the most common route. References: gov.il/he/departments/general/pre_academic_preparatory_program; kolzchut.org.il "מכינה קדם-אקדמית".

**Atuda Akademait (IDF-sponsored academic deferral):**
- The IDF pays full tuition + monthly stipend in exchange for extended service after the degree (length depends on degree, typically 4-5 years post-graduation).
- Apply via Meitav (IDF Manpower Directorate); registration window opens around age 16.5, before the standard draft age. The Yom Hamiyunim (selection day) is held during high school.
- Atuda is a separate gate ON TOP of regular university admission, a student must be accepted both by the IDF AND the university.
- Strongly STEM-skewed: most slots are CS, engineering, math, physics. Reference: mitgaisim.idf.il/roles/מסלול-העתודה-האקדמית.

**Olim Chadashim (new immigrants):**
- Most universities exempt olim from the psychometric for the first 3 years post-aliyah. SAT, ACT, IB, or Bagrut Beinleumit are accepted as substitutes.
- Naale (Bagrut in Israel for diaspora teens) is recognized by all universities.
- Foreign credentials require evaluation (haarakhat te'uda) via the Ministry of Education.
- Student Authority (Minhal HaStudentim) provides tuition scholarships and dorm subsidies for first-degree olim. Reference: gov.il/he/departments/units/student_authority.

**Open University (Ha'Universita Ha'Petucha) "petuach" model:**
- Course enrollment is open to anyone, no Bagrut, no psychometric, no application form required.
- Students accumulate course credits; **120 credit points** (engineering degrees differ) with the required core completes a fully CHE-recognized first degree, equivalent in legal status to any other university degree.
- Strongest fit for older students, dropouts, working professionals, and students who failed the psychometric and prefer not to retake. Reference: openu.ac.il/registration.

**Elite IDF-academic programs (Mahalol):**
- **Talpiot** (IDF + Hebrew U Math/Physics/CS), **Havatzalot** (intelligence + BGU), **Brakim**, **Psagot**, **Tzameret** (medicine + IDF), separate selection processes parallel to standard admission, with multi-year service commitments.
- Application gates open in 11th grade for some (e.g., Talpiot Yom Hamiyunim). Students with the academic profile to apply often miss the window because the skill is treated as university-only.

### Step 7: Wartime 2023-2025 (Iron Swords) Accommodations

Bagrut and psychometric accommodations from "Charvot Barzel" / "Iron Swords" are still in effect for the 2025/26 cohort and likely later:
- **Bagrut**: ~15% extra time on written exams, ~20% material reduction, oral exams converted to internal grades for displaced students from north and south, reservists' children, and bereaved siblings.
- **Higher education**: free academic year for displaced students via Student Authority; tuition deferral for reservists; alternate "Bagrut Iron Swords" portfolio path for some cohorts.
- Filing deadlines apply via the school for Bagrut accommodations and via the Student Authority for tuition rights.
- Always check edu.gov.il/special/iron-swords for the current cohort's accommodations before assuming a standard Bagrut format for evacuee or reservist students.

### Step 8: Education Terminology Glossary
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
- `scripts/calculate_sekhem.py`, Calculate weighted Bagrut averages with 5-unit bonus points, estimate university admission composite scores (sekhem) for specific universities, interpret psychometric exam scores with percentile rankings, and display admission thresholds for popular programs. Supports subcommands: `bagrut`, `sekhem`, `psychometric`, `thresholds`. Run: `python scripts/calculate_sekhem.py --help`

### References
- `references/education-glossary.md`, Hebrew-English glossary of Israeli education terms covering system levels (gan through tichon), exam terminology (bagrut, yechidot limud, sekhem), education streams (mamlachti, charedi, aravi), mandatory Bagrut subject requirements, and all major universities with locations. Consult when translating education terms or explaining system structure.

## Gotchas
- The Israeli school year starts September 1, but end dates differ by level: elementary schools and kindergartens end June 30, while middle schools and high schools end **June 19** (e.g., 2025/26 cycle). Do NOT generalize "June 30" across all levels.
- Israeli high school matriculation exams (bagruyot) use a points system (yechidot limud, typically 3-5 units per subject). Agents may equate these to US AP exams or IB scores, which use different scales.
- The Israeli education system has multiple parallel tracks: State (mamlachti), State-Religious (mamlachti dati), Ultra-Orthodox (charedi), and Arab. Each has different curricula. Agents may assume a single national curriculum.
- Israeli universities have a separate admissions process from the US: SAT equivalent is the psychometric exam (psychometri), GPA is calculated differently (sekhem), and army service (sherut tzva'i) is factored into admissions.
- Bagrut English score does NOT determine university English placement. Universities use Amir / Amiram (and from December 2026, Amirnett) for English bracketing. A student with 5yl Bagrut English at 90 may still be placed in "Advanced A" and required to take an English course. See Step 4.5.
- Bagrut bonus tables: math 5yl earns +35 but English 5yl earns only +25. Treating English as a "+35 subject" inflates calculated sekhem and misleads students about admission chances.
- Medicine admissions are MOR-gated. A student with a 740+ sekhem who skipped MOR registration (spring to early summer) is auto-rejected from medicine for that admission cycle. See Step 5.5.
- The Iron Swords (Charvot Barzel) accommodations are still active for 2025/26 Bagrut: ~15% extra time, ~20% material reduction, oral conversions for displaced students. Do not assume standard format for evacuee or reservist students.

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

### Issue: "Student is olim and got told to sit the psychometric"
Cause: Olim chadashim are exempt from the psychometric for the first 3 years post-aliyah at most universities; SAT/ACT/IB/Bagrut Beinleumit substitute. The exemption is often missed because it is not the default admission path.
Solution: Confirm aliyah date, then advise applying via the Olim track at the target university and the Student Authority for tuition scholarship. See Step 6.

### Issue: "Student wants medicine but missed MOR registration"
Cause: MOR registration runs in spring to early summer (around May-June) and closes well before the medical-school application deadline. Students who only optimize sekhem assume "I'll worry about admissions later" and miss the window entirely.
Solution: There is no late MOR sitting. The student must wait a full year and register for the next MOR cycle. See Step 5.5.

## Recommended MCP Servers

For live school data lookups and education datasets from data.gov.il, pair this skill with one of these MCP servers:

- **data-gov-il** -- Query Israel's open data portal (data.gov.il) for school listings, enrollment statistics, and RAMA assessment data. Ideal for structured API queries when you need specific datasets by city, sector, or school type.
- **datagov-israel** -- Alternative data.gov.il MCP with built-in data visualization support. Use when you need to present school data as charts or compare statistics across districts.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| NITE (psychometric exam) | https://www.nite.org.il/ | Current sitting fee, registration windows, exam languages, score interpretation, December 2026 PET restructure (Amirnett) |
| NITE, Amir / Amiram / Yael | https://www.nite.org.il/other-tests/ | English placement (Amir, Amiram), Hebrew proficiency for non-Hebrew speakers (Yael), MOR for medicine |
| Ministry of Education | https://edu.gov.il/ | Current Bagrut requirements, unit thresholds, school year calendar |
| Iron Swords accommodations | https://edu.gov.il/special/iron-swords/ | Wartime Bagrut accommodations for evacuees, reservists, bereaved families |
| Council for Higher Education (CHE) | https://che.org.il/en/ | Authoritative list of recognized universities and accredited colleges (11 universities as of 2026) |
| Student Authority (Minhal HaStudentim) | https://www.gov.il/he/departments/units/student_authority | Olim tuition scholarship, dorm subsidies, foreign-credential evaluation |
| Pre-academic Mechina | https://www.gov.il/he/departments/general/pre_academic_preparatory_program | Mechina recognition list, eligibility for state-funded mechina (periphery, post-army, olim, lone soldiers) |
| Atuda Akademait (IDF) | https://www.mitgaisim.idf.il/roles/מסלול-העתודה-האקדמית/ | Atuda registration window, eligible degree fields, service commitment terms |
| data.gov.il | https://www.data.gov.il/ | Live school data, enrollment statistics, RAMA assessments |