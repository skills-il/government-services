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

**Mandatory Bagrut subjects** (Hebrew language, English, mathematics, Tanach, literature, history and civics, with their minimum unit counts): `references/education-glossary.md`.

**Requirements for certificate:**
- Pass every mandatory subject. The pass mark is commonly quoted as 55 or 56 out of 100 and we could not confirm which from a ministry page this cycle, so **do not tell a student their 55 is a fail**: send them to `parents.education.gov.il` or the school.
- Minimum 21 total study units (widely stated, not confirmed against a ministry page this cycle)
- Certificate name: Te'udat Bagrut

**Bagrut bonuses (mekadmei hatava) for university admission.**

**Quote the Technion table, because it is the only complete one published.** Verified on `admissions.technion.ac.il/calculation-of-the-median-grade` on 2026-08-27. Tel Aviv and the Hebrew University expose only a JavaScript calculator and publish no table at all, so any single "the bonus is X" figure for them is unsourced. Widely-repeated numbers such as a +35 maths bonus come from commercial prep companies, not from a university, and the Technion's published figure is **+30**. Do not state a universal bonus; state this table and tell the user to run their target program's own calculator.

Full table, plus the grade-60 condition, the mitzraf cluster rule and the maths double-weighting: `references/education-glossary.md`. The three figures to carry in your head: **5-unit maths is +30** (not the +35 prep companies quote), **the mitzraf levels maths and two qualifying sciences at +30 each**, and **the Technion counts maths units at double weight**, which moves a Technion sekhem more than any bonus does.

4-unit subjects earn a real bonus. Any tool or summary that only lists 5-unit bonuses silently scores a 4-unit student at zero.

### Step 4: Psychometric Exam (PET) Information

**Exam structure (this is the format UP TO AND INCLUDING the 2-3.9.2026 sitting; from December 2026 English is removed, see below):**
| Section | Hebrew | Score Range |
|---------|--------|-------------|
| Quantitative Reasoning | Chashiva Kamutit | 50-150 |
| Verbal Reasoning | Chashiva Miluliti | 50-150 |
| English | Anglit | 50-150 |

**Overall score:** 200-800, as a weighted composite of the three domains. The commonly cited mean is about **548** with a standard deviation of roughly 108 (a 2018 figure, so treat it as indicative). **From the December 2026 sitting the composite no longer includes English**, so a pre-December and a post-December score are not the same instrument.

**Score interpretation (approximate, and NOT an official NITE percentile table):**

NITE does not publish a score-to-percentile table we could verify, and the bands below are rules of thumb. The bundled script carries its own slightly different bands, so **do not present either as an official percentile** and do not tell a student their exact rank. What IS published is the shape of the distribution: roughly normal, mean about 548, standard deviation about 108.

| Score | Rough standing | Competitiveness |
|-------|-----------|-----------------|
| 740+ | Top few percent | Medicine, law at top universities |
| 680+ | Well above average | CS, engineering at Technion/TAU |
| 620+ | Above average | Many university programs |
| 550 | Around the mean | Some university, most colleges |
| Below 480 | Well below average | Consider mechina or retake |

**Key facts:**
- The highest score counts. (The retake-limit position is not stated on any current NITE page we could open, so do not tell a student there is "no cap"; point them at nite.org.il.)
- **Languages vary BY SITTING, and are narrower than usually assumed.** September 2026 and **December 2026** are Hebrew and Arabic only. April 2027 and July 2027 add a combined/English form, Russian and French. Spanish is not offered. Check the sitting, not the exam, and note that the December sitting a student books now has no Russian or French option.
- **Cost: read the price off the ROW for the sitting the student is actually taking.** On the NITE table read 2026-08-27, **665 NIS is the price cell of the 2-3.9.2026 sitting**, whose registration closed on 8.7.2026. The 4/6.12.2026, 18-19.4.2027 and 1.7.2027 rows carry **no published price at all**. So do not quote 665 as "the fee" to someone registering for December. (A previous version of this skill quoted 560, which was a different sitting's number and was wrong; the failure mode is lifting a price without checking its row.)
- **2026/27 sittings and their registration deadlines** (from the same table). The middle column is what a student needs today:

| Sitting | Registration closes | Scores reported |
|---|---|---|
| 2-3.9.2026 | 8.7.2026 (**closed**) | 18.10.2026 |
| 4 and 6.12.2026 | **14.10.2026 (still open as of late August 2026)** | 20.1.2027 |
| 18-19.4.2027 | 10.2.2027 | (see table) |
| 1.7.2027 | (see table) | (see table) |

**The December sitting reports on 20.1.2027, so it cannot serve a תשפ"ז application** that needed a score months earlier. It is a תשפ"ח instrument. Say which academic year a sitting can actually feed before telling a student to book it.
- Popular prep courses: Kidum, High-Q, Yoel Geva, Psagot.

**IMPORTANT, December 2026 PET restructure:**
NITE is removing English from the main psychometric. From the December 2026 sitting onward:
- The PET covers **two domains** (verbal and quantitative) across **five multiple-choice sections plus a writing task**, one of the five being an experimental section. It is **one hour shorter** than the eight-section format. Do not describe it as "2 sections" or quote a total duration; the sections and the domains are different counts.
- English moves to **Amirnet** (אמירנט), spelled with one t.
- **Amirnet is NOT new and does not start in December 2026.** It is live now, with its own registration and a **315 NIS** fee, and universities already accept it (the Hebrew University's reservist track for תשפ"ז accepted Amirnet results up to 30.07.2026). December 2026 is when the PET **drops** English, not when Amirnet begins.
- A student re-sitting Amirnet must wait **at least 35 days** between sittings.
- The restructure affects admissions only from academic year תשפ"ח (starting October 2027); each institution decides whether to keep using the PET English score in the sekhem until then.

### Step 4.5: English Placement Tests (Distinct from Bagrut English)

Bagrut English measures high-school proficiency. University English placement uses separate NITE tests, and many students don't realize they're different exams:

| Test | Hebrew | Purpose |
|------|--------|---------|
| Amirnet | אמירנט | **The** English placement test. Computerized, 315 NIS, minimum 35 days between sittings. This is the only English placement exam NITE currently lists. |
| Yael | יע"ל | Hebrew proficiency for non-Hebrew speakers. Required for most olim and international students. |
| Yaelnet | יעלנט | Computerized Hebrew-proficiency test, listed alongside Yael. |

**Amir (אמי"ר) and Amiram (אמיר"ם) are no longer separately bookable at NITE**, but they are not erased. NITE's current test index lists the psychometric, Amirnet, Yael, Yaelnet, MATAM, MOR/MIRKAM, MERAV and MEIMAD, with nothing named Amir or Amiram, and the old `/other-tests/amir` path now serves the Amirnet page. **University admissions pages still name them** and still honour existing scores against dated validity deadlines (the Technion's תשפ"ז timetable references אמי"ר). So: a student cannot book one today, an existing Amir/Amiram score may still count, and a Technion page naming אמי"ר is not a typo.

**English level brackets:** universities place students into one of five tracks, from Pre-Basic through Basic, Advanced A and Advanced B to Exempt (patur). Only Exempt means no English coursework during the degree. Full table: `references/education-glossary.md`.

A PET English score (for sittings before December 2026) or an Amirnet score determines the bracket. NITE source: `nite.org.il/other-tests/amirnet/` and the test index at `nite.org.il/other-tests/`.

### Step 5: University Admissions

**Sekhem (composite admission score) calculation. Every number in this section is UNSOURCED.** No Israeli university we could reach publishes a readable weighting table or threshold list; Tel Aviv exposes only a JavaScript calculator. The weights and thresholds below are illustrative starting points for framing a conversation, they disagree with each other and with the bundled script by design of their provenance, and none of them should be quoted to a student as a number. Always run the program's official calculator.

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

Israeli medical schools screen candidates through NITE-administered selection systems on top of the sekhem. Three points here are commonly stated wrongly, and the third changed in 2026.

- **There are THREE systems, not one:** מו"ר (MOR), מרק"ם (MIRKAM) and מר"ב (MERAV), for the six-year and four-year tracks. Naming only MOR to a candidate is incomplete; which one applies depends on the institution and track.
- **The candidate does not self-register into a window.** NITE's page states that the summons is sent by NITE **according to candidate lists supplied by the universities**. So the actionable advice is to apply to the medical school on time and watch for the summons, not to "register for MOR" as a separate step. An earlier version of this skill described a self-registration window; that model is not supported by NITE's own page.
- **From 2026 there is NO overall MOR score.** NITE reports each component separately (the personal-biographical questionnaire, the assessment centre, and the SHAUL questionnaire), and **each institution weights them under its own policy**. Never quote a single "MOR score" to a candidate, and never compare one across institutions.
- **Fees:** assessment centre **1,900 NIS**, personal-biographical questionnaire **450 NIS**, separate from the PET.
- **Dates:** NITE states that upcoming MOR and MIRKAM dates "will be published later". Do not present a previous cycle's dates as current; send the user to `nite.org.il/other-tests/mor-mirkam/`.
- Missing the process means missing the whole admissions cycle for medicine, and there is no exemption for atuda candidates or olim.

A student aiming for medicine who only optimizes Bagrut plus psychometric will fail admissions. Flag the selection process early, and check which of the three systems their target institution uses.

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
- Many institutions run an olim admission track, and some waive the PET in favour of SAT, ACT, IB or Bagrut Beinleumit. **The commonly quoted "exempt for 3 years at most universities" is not sourced here**, so do not state a blanket window: check the target institution's own olim page for its rule and its filing dates. Note also that a waiver of the PET does NOT waive **YAEL/YAELNET** Hebrew proficiency for a non-Hebrew speaker, and that test has its own deadline.
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

### Step 7: Iron Swords Accommodations (status differs between school and university)

Treat these two tracks separately, because as of 2026-08-27 they are in different states.

**Higher education: extended into תשפ"ז, and the mechanism is concrete.** The Hebrew University publishes an admissions-accommodations track for reservists for תשפ"ז, aimed at candidates serving in miluim during 2026, keyed to day counts with hard filing deadlines (for example a 60-day threshold routing to a later PET sitting, a 90-day threshold reaching the July PET and the summer Bagrut, and an Amirnet result accepted up to 30.07.2026), decided through an appeals committee. The Technion likewise lists accommodations for reservists and evacuees. So the correct advice is: go to the **target institution's** reservist-accommodations page, count the qualifying service days, and file before that institution's deadline. This is a per-institution appeals route, not a blanket national entitlement, and it is not the "free academic year" the earlier version of this skill described.

**Bagrut: unverified for תשפ"ז.** The Ministry of Education's own תשפ"ז opening FAQ, updated 25.08.2026, contains no mention of Iron Swords, evacuees or miluim accommodations. The extra-time and material-reduction figures quoted in earlier versions of this skill traced back to a local news site, not to the ministry. **Do not quote a percentage.** Tell the user to confirm the current cohort's accommodations with the school and with `parents.education.gov.il` (which is where the ministry's live parent-facing exam and accommodations content now lives).

**The old link is dead.** `edu.gov.il/special/iron-swords` redirects to a generic ministry landing page with no Iron Swords content, and `edu.gov.il` itself now redirects there too.

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

### Step 9: Timing, and the Routes Most Students Actually Take

**Establish WHERE IN THE YEAR the student is before giving advice.** This skill's mechanics are useless attached to the wrong date, and most of the gates below have no late option.

- **University registration has its own deadlines, separate from every exam.** The Technion publishes per-track registration windows for תשפ"ז at `admissions.technion.ac.il/registeration-dates/`, with **separate and earlier windows for medicine, architecture and landscape architecture**, and those tracks have no late registration at all. Read the target institution's timetable page; do not infer a deadline from the exam calendar.
- **Match the exam sitting to the admission year.** A PET reports roughly six weeks after the sitting (December 2026 reports 20.1.2027), so a sitting can be too late for the year the student is aiming at even though it is "this year's exam".
- **Bagrut re-sits (מועד ב' and שיפור ציון)** change a sekhem after the fact. Ask whether a re-sit is pending before treating a Bagrut average as final, and check the institution's rule on which grade counts and how late it accepts an updated certificate.

**Accommodations in examination arrangements (התאמות בדרכי היבחנות)** are the ordinary route for a student with a diagnosed learning disability, granted through the school and its accommodations committee. This is far more common than the wartime accommodations in Step 7, and the ministry publishes it as live parent-facing content on `parents.education.gov.il`. Route a learning-disability question there, not to Step 7.

**Colleges (מכללות) are where most Israeli undergraduates study, and this skill's tables are university-only.** Academic colleges, teaching colleges and technological colleges are CHE-accredited, and many admit on a Bagrut average alone or on an internal exam rather than a PET. Do NOT hand a student at 550 a university threshold table and stop: name the college route explicitly and send them to the specific institution's admissions page, because the sekhem weightings, bonus tables and thresholds in Step 5 do not apply to it.

**"Mechina" is ambiguous and the two meanings are unrelated.** Everything in Step 6 is **מכינה קדם-אקדמית** (pre-academic, substitutes for admission requirements, subsidised for the eligibility groups). **מכינה קדם-צבאית** is a pre-military gap-year programme: it is not academic, does not substitute for a Bagrut average and does not run through the same committee. A parent asking "should he do a mechina before the army" usually means the second. Ask which one before answering.

**Other routes worth naming rather than omitting:** external and adult Bagrut (בגרות אקסטרנית / למבוגרים) for someone completing a certificate after school, and תעודת גמר or a 12-years-of-schooling certificate for a student who will not complete a full Bagrut. Both come up constantly and neither is covered in detail here; confirm the current mechanics with the school or `parents.education.gov.il`.

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
1. Interpret the score as standing, not as a rank: 580 is slightly above the ~548 mean. Do NOT quote a percentile; NITE publishes no verifiable table.
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
- The Israeli school year opens on 1 September (unless that falls on Shabbat), but the END date differs by level: kindergartens and elementary schools finish **30 June**, while middle schools, high schools and grades 13-14 finish **20 June**. Verified against the ministry parents portal for תשפ"ז on 2026-08-27. Do NOT generalize "30 June" across all levels, and note that an earlier version of this skill said 19 June for secondary, which is wrong.
- The vacation calendar is published **per sector** (Jewish, Arab, Druze, Haredi, and recognized-but-unofficial each get their own table). There is no single national vacation list, so confirm which sector calendar applies before quoting a date.
- Israeli high school matriculation exams (bagruyot) use a points system (yechidot limud, typically 3-5 units per subject). Agents may equate these to US AP exams or IB scores, which use different scales.
- The Israeli education system has multiple parallel tracks: State (mamlachti), State-Religious (mamlachti dati), Ultra-Orthodox (charedi), and Arab. Each has different curricula. Agents may assume a single national curriculum.
- Israeli universities have a separate admissions process from the US: SAT equivalent is the psychometric exam (psychometri), GPA is calculated differently (sekhem), and army service (sherut tzva'i) is factored into admissions.
- Bagrut English score does NOT determine university English placement. Universities bracket on a PET English score or on **Amirnet**, which is the only English placement test NITE currently lists (Amir and Amiram are retired). A student with 5-unit Bagrut English at 90 may still be placed in "Advanced A" and required to take an English course. See Step 4.5.
- Bagrut bonus tables differ by university and only the Technion publishes a complete one. Its 5-unit maths bonus is **+30**, not the +35 that prep companies quote, and its cluster rule levels maths and two qualifying sciences at +30 each rather than keeping maths highest. Quoting a universal +35 inflates a calculated sekhem and misleads students about admission chances. 4-unit subjects earn +10, which summaries routinely drop entirely.
- Medicine admissions are gated by a NITE selection system (MOR, MIRKAM or MERAV depending on institution and track). A student with a 740+ sekhem who is not in that process is out of the cycle. Note the candidate does NOT self-register: NITE summons from university-supplied lists, so the actionable step is applying to the medical school on time. See Step 5.5.
- Iron Swords accommodations split by level and must not be quoted as percentages. For higher education they were extended into תשפ"ז as a per-institution reservist-accommodations route with day-count thresholds and filing deadlines. For Bagrut, the ministry's own תשפ"ז material does not mention them at all, and the extra-time and material-reduction percentages that circulate trace to local news rather than to the ministry. Send the user to the institution's own page and to `parents.education.gov.il`; do not state a percentage. See Step 7.

## Troubleshooting

### Issue: "School data not found"
Cause: City name may need Hebrew spelling, or dataset may be outdated
Solution: Search in Hebrew. Check data.gov.il for the most recent education dataset.

### Issue: "Sekhem calculation does not match university website"
Cause: Each university and program uses different weights and formulas
Solution: This skill provides estimates. For exact sekhem, use the specific university's admissions calculator (usually available on their website during application period).

### Issue: "Bagrut requirements changed"
Cause: Ministry of Education periodically updates requirements
Solution: check `parents.education.gov.il` for current Bagrut requirements and exam information. `edu.gov.il` now redirects to a generic gov.il landing page and no longer serves this content. The core mandatory subjects are stable, but unit requirements and elective options may change.

### Issue: "Student is olim and got told to sit the psychometric"
Cause: Olim chadashim are exempt from the psychometric for the first 3 years post-aliyah at most universities; SAT/ACT/IB/Bagrut Beinleumit substitute. The exemption is often missed because it is not the default admission path.
Solution: Confirm aliyah date, then advise applying via the Olim track at the target university and the Student Authority for tuition scholarship. See Step 6.

### Issue: "Student wants medicine but missed MOR registration"
Cause: the candidate is not in the selection process. NITE does not take self-registrations for MOR/MIRKAM: it summons candidates from lists the universities supply, and it has not published the upcoming cycle's dates. Students who only optimize sekhem assume "I'll worry about admissions later" and are never put on a list.
Solution: There is no late MOR sitting. The student must wait a full year and register for the next MOR cycle. See Step 5.5.

## Recommended MCP Servers

For live school data lookups and education datasets from data.gov.il, pair this skill with one of these MCP servers:

- **data-gov-il** -- Query Israel's open data portal (data.gov.il) for school listings, enrollment statistics, and RAMA assessment data. Ideal for structured API queries when you need specific datasets by city, sector, or school type.
- **datagov-israel** -- Alternative data.gov.il MCP with built-in data visualization support. Use when you need to present school data as charts or compare statistics across districts.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| NITE (psychometric exam) | https://www.nite.org.il/test-dates-and-prices/ | Current sitting fee, dates, per-sitting exam languages, registration deadlines |
| NITE test index | https://www.nite.org.il/other-tests/ | The current roster of NITE tests. Check here before naming an exam: Amir and Amiram are no longer listed |
| NITE, Amirnet | https://www.nite.org.il/other-tests/amirnet/ | English placement: fee, sittings, and the 35-day minimum interval between re-sits |
| NITE, MOR and MIRKAM | https://www.nite.org.il/other-tests/mor-mirkam/ | Medicine selection systems, component fees, and the 2026 change removing the overall score |
| Ministry of Education, parents portal | https://parents.education.gov.il/ | Bagrut exams and grades, accommodations in examination arrangements, school-year calendar and vacations, registration. This is the live surface; `edu.gov.il` redirects to a generic landing page |
| School-year calendar (per sector) | https://parents.education.gov.il/gov-education/vacations-camps-leisure/schedule | Opening and closing dates, and the separate vacation tables for the Jewish, Arab, Druze and Haredi sectors |
| Council for Higher Education (CHE) | https://che.org.il/en/ | Authoritative list of recognized universities and accredited colleges (11 universities as of 2026) |
| Student Authority (Minhal HaStudentim) | https://www.gov.il/he/departments/units/student_authority | Olim tuition scholarship, dorm subsidies, foreign-credential evaluation |
| Pre-academic Mechina | https://www.gov.il/he/departments/general/pre_academic_preparatory_program | Mechina recognition list, eligibility for state-funded mechina (periphery, post-army, olim, lone soldiers) |
| Atuda Akademait (IDF) | https://www.mitgaisim.idf.il/roles/מסלול-העתודה-האקדמית/ | Atuda registration window, eligible degree fields, service commitment terms |
| data.gov.il | https://www.data.gov.il/ | Live school data, enrollment statistics, RAMA assessments |