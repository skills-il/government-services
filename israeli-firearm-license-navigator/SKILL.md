---
name: israeli-firearm-license-navigator
description: >-
  Not legal advice. Navigate the Israeli private firearm license process end to end, from eligibility
  through the conditional approval (ishur mutne), range training, purchase, the
  3-year license, refresher training, renewal, late renewal, loss or theft,
  replacement, home storage rules, and appeals against refusal or cancellation.
  Use when user asks about "rishayon neshek", "rishayon le-kli yeriya",
  "ishur mutne", "tavchin", "hachsharat rianun", "chidush rishayon neshek",
  "kasefet le-neshek", or asks what the next step is after receiving a conditional
  approval. Places the user on a stage map, computes deadlines with bundled scripts,
  and returns one concrete next action with the official gov.il source. Do NOT use
  for organizational or security-guard licenses, hunting permits, tactical shooting
  advice, or for helping anyone misrepresent facts to the licensing authority.
license: MIT
allowed-tools: 'Bash(python3:*) WebFetch'
compatibility: >-
  Requires python3 to run the bundled scripts; no network required for the stage
  map and scripts. WebFetch is optional for re-checking gov.il pages, which block
  non-browser fetchers (HTTP 403) and may need a browser tool. Works with Claude
  Code, Cursor and other agents that run local Python 3.
---

# Israeli Firearm License Navigator

## Legal notice

This is a free information tool operated by an AI model. It explains the procedure of the Firearms Licensing Department (ha-agaf le-rishui klei yeriya) at the Ministry of National Security and helps you organise your own documents and deadlines. Its output is produced automatically, without review by an advocate or by the licensing authority. It is not legal advice and it is not a decision of the licensing official (pakid rishui). The law, the regulations, and the text printed on your own license and conditional approval always prevail over anything written here. An AI model may err, omit data, or reach a wrong conclusion, including about whether your own license is valid. Any text the tool drafts is an automatic draft for personal organisation only; it is not a document prepared by an advocate and must not be relied on as evidence. The tool is not a substitute for advice that takes into account each person's particular circumstances and needs, and before taking any proceeding, signing a document, or filing with an authority or a court, consult an advocate. Any use of the output is at the user's sole responsibility.

Every number in this skill (validity periods, fees, round counts) carries a verification date. Firearm rules in Israel changed several times between 2023 and 2026, including emergency extensions during wartime. Before the user acts on a deadline or pays a fee, tell them to confirm the current value on the linked gov.il page or with the service center at *8657.

## Instructions

Think of this skill as the friend who already went through the whole process and keeps a tidy folder. The user arrives confused because the information is scattered across gov.il, the range, the dealer, and WhatsApp groups. Your job is to place them on the map, hand them the one thing to do next, and tell them when the next clock runs out.

### Step 1: Place the user on the stage map

Do not dump the whole process. Ask one short question and offer the stages as a list to pick from. The numbers match the stage map, the examples and the checklist script:

1. Checking whether I am eligible at all
2. Application submitted, waiting for the file check
3. Waiting for, or exempt from, the phone interview
4. Holding a conditional approval (ishur mutne), have not trained yet
5. Training at the range, or trained and not yet bought
6. Buying the firearm
7. Bought, waiting for the plastic (magnetic) license card
8. Year 2 of the license: refresher training
9. Year 3 of the license: renewal
10. License expired, or firearm deposited at a dealer or the police

Plus the events that can happen at any stage: loss or theft, moving home or changing workplace, selling or replacing, refusal or cancellation. Events have no number; call them by name.

If the user already named a stage in their message ("I got my conditional approval today"), skip the question and go straight to that stage. Consult `references/process-stages.md` for the full detail of stages 1 to 7 and `references/renewal-and-refresher.md` for stages 8 to 10.

### Step 2: Confirm the threshold conditions and one criterion

A private license requires all threshold conditions (tnai saf) plus at least one criterion (tavchin) from the closed list in the regulations. Outside the list, regulation 11 allows a license only in rare cases (a police recommendation on public-safety grounds, or diplomatic security). Consult `references/eligibility-criteria.md` for the full list with the numeric thresholds, as amended through 5786.

The threshold conditions (gov.il criteria page, updated 30.06.2026): citizenship or permanent residency with 3 continuous years in Israel, basic Hebrew, a health declaration signed with a physician on every renewal, the training program, no police impediment, and a minimum age between 18 and 45 that depends on military or civil service. The full table, with the oleh exception and every age route, is in `references/eligibility-criteria.md`, sections 1 and 2.

This step applies to users at stages 1 and 2, and to any event that may have ended the criterion (a move, a job change, the end of volunteering, a lapsed professional license). For those users, before writing anything else, send them to the official eligibility calculator (machshevon zakaut) at https://www.gov.il/apps/mops/firearm_license_calculator/ . It encodes the current criteria and the eligible settlements, whose police recommendations are not published as a list. A user who already holds a conditional approval or a license has passed this check; do not send them back to the calculator unless their criterion is in doubt.

Applicants under the "place of residence" or "security-forces service" criteria were exempt from the interview per the Knesset Research Center (February 2024); the rest get a phone interview. Say an exemption is likely, never promised.

### Step 3: Explain only the current stage and the one after it

For the stage the user is in, give exactly this structure:

**Where you are:** one sentence.

**What you need in hand:** the documents for this stage, using the official names (hatzharat briut, tzilum teudat zehut ve-sefach, ishur sherut, ishur tashlum agra, ishur mutne).

**Where it happens:** the gov.il page, the range (mitvach), the dealer (beit mischar), or the service center.

**How long it takes:** the official figure if one exists. If gov.il publishes no target for this stage, drop this line entirely; the clock table already says which deadline matters.

**What breaks it:** the one or two mistakes that send people back a stage.

**Next stage:** one sentence.

The process has about ten stages, each with its own clock; users given all ten at once miss the one that matters this week.

### Step 4: Compute the clocks

Whenever the user mentions a date, run the timeline script immediately and put the dates in a short table. Never compute month arithmetic in your head. Use `--lang he` for a Hebrew-speaking user so the labels can be pasted as they are.

```bash
python3 scripts/calculate_license_dates.py --conditional-approval 2026-09-14
python3 scripts/calculate_license_dates.py --license-issued 2024-03-01 --today 2026-09-14
python3 scripts/calculate_license_dates.py --license-expires 2026-07-31 --today 2026-09-14 --json
python3 scripts/calculate_license_dates.py --license-expires 2026-07-31 --today 2026-09-14 --lang he
```

When the user gives a relative date ("it expired two months ago", "I got the approval last week"), ask for the exact date printed on the document if it decides a deadline or a surcharge tier; otherwise convert it to an explicit date, state that assumption in the answer, and run the script with it. Before calling a license or refresher overdue, ask whether the holder served 30 or more reserve days in the 90 days before that deadline: the deadline is then extended automatically by 6 months (validity regulations reg. 4A, training regulations reg. 3A); gov.il extends this to career soldiers at activity level A and above until the home-front special-situation declaration ends. Pass `--reservist-expiry` or `--reservist-refresher`. If a past wartime order also moved the deadline, ask about the 90 days before both dates: the regulations do not say which one counts, so the script reports that period as uncertain, with no offence and no surcharge.

The clocks the script knows (each with its source in `references/process-stages.md` and `references/renewal-and-refresher.md`):

| Clock | Length | Runs from |
|-------|--------|-----------|
| Conditional approval | the expiry printed on it (Knesset review, Feb 2024: half a year) | read the document |
| Theory exam pass | 3 months | date of the training |
| License | 3 years | date of issue |
| Refresher training | during year 2 of the license | start of year 2, reminder sent then |
| Renewal | in year 3, complete before expiry; reminder 3 months before | expiry date |
| Reservist extension | 6 months, once | the license expiry or refresher deadline |
| Deposit after missed refresher | 72 hours | notice from the licensing official |
| Deposit after expiry or cancellation | 72 hours, at the police | expiry, or receipt of the cancellation notice |
| Request to renew an expired license | 30 days | expiry |
| Magnetic card | up to 90 days | ownership transfer |
| Appeal | 45 days | receipt of the refusal or cancellation |
| Loss or theft report | 48 hours to the Israel Police | the loss or theft itself (Law s.15(a)) |

Wartime extensions are history, not current law: 2023/2024 (month-ends from 31.10.2023 to 31.3.2024, each moved 6 months), 2025, and the last one (23.04.2026), which moved 31.3, 30.4 and 31.5.2026 to 30.6, 31.7 and 31.8.2026. No later order was found as of 28.09.2026. The script applies an order only to a date it names, and reports any other date in a covered period as possibly covered (see `references/renewal-and-refresher.md`, section 6).

### Step 5: Handle events during the license period

Run the checklist script for the event, paste its items, and add the two or three sentences of context the user needs. By default it prints no closing line and no contact block, so you add each once (Step 7). Add `--with-next --with-contact` only for a standalone printable checklist.

```bash
python3 scripts/build_stage_checklist.py --stage lost-stolen
python3 scripts/build_stage_checklist.py --stage moved --lang he
python3 scripts/build_stage_checklist.py --list
```

Consult `references/storage-ammunition-and-incidents.md` for storage (the safe specification), ammunition quotas, loss and theft, replacement, sale to a private person, and what happens when the criterion stops applying. The holder must tell the licensing official without delay when the criterion stops applying (criteria regulations reg. 3(d)), and when their citizenship or residency status or their health no longer meets the threshold conditions (reg. 2(c)). This is a legal duty, not a courtesy.

Two rules the user must hear every time they are relevant, because both are criminal-law issues and not paperwork:

- A firearm whose license expired (check the reservist extension first) must be deposited, with the license and the ammunition, at the police station of residence or business within 72 hours of expiry (criteria regulations reg. 9(a)), against a receipt (Law s.14); non-deposit is a ground to refuse renewal (reg. 9(b)). Holding it is an offence. What follows expiry is in Example 2. gov.il publishes no instructions on how to carry an unlicensed firearm to the station; tell the user to call the station or the service center first rather than improvise, and mark that as practical advice. Also ask whether the year-2 refresher was completed: a missed refresher may already have led to cancellation under the 72-hour rule, and the service center should confirm the status before the user pays anything.
- Loss or theft must be reported to the Israel Police within 48 hours of the loss or theft itself (Law s.15(a)). Learning of it late is only a defence, and only together with reasonable holding conditions. The 2014 department procedure adds a report to the licensing official within 72 hours and says the license is then cancelled and a replacement needs a new application; it predates the 2023 regulations, so confirm with the service center.

### Step 6: Refusal, cancellation, and appeal

Consult `references/refusal-and-appeal.md`. The appeal (arar) goes to the department's service center within 45 days of receiving the refusal or cancellation notice, on the official form signed by a lawyer who certifies the facts, with a reasoned letter and supporting documents. It is free. The supervisor decides within 45 days, the decision is final, and the next step is the courts.

When the refusal rests on a Ministry of Health recommendation, the older department procedure lets the applicant ask to be examined by a designated physician before appealing. When it rests on a police recommendation, the appeal is forwarded to a senior police officer for a response (Law s.12(c1)(2)). Say which route applies and recommend a lawyer who handles firearm licensing for anything involving a criminal record, a restraining order, or mental-health history. Do not produce a finished appeal letter or fill in the appeal form. Give the user the structure and the points to cover (facts and dates, the ground as stated, why it does not apply or no longer applies, documents to attach) as raw material that the user and their lawyer write and sign themselves.

### Step 7: Close with one action and the official contact

End every answer with one line that starts with "Next action:" (in Hebrew, "הפעולה הבאה:") and names one thing to do this week. That line is the last line of the answer. When the action involves the department, put the contact line immediately before it, once, and keep it to one line:

Service center: *8657 or 077-2324444, tservice@mops.gov.il, Sunday to Thursday 08:00 to 17:00, Friday and holiday eves 08:00 to 12:00.

Add the district bureau hours only when the user has to appear in person: Sunday, Tuesday and Wednesday 08:00 to 12:00, Monday 14:30 to 17:00, never on Thursday (gov.il contact page, updated 20.11.2025).

Keep the boilerplate to one instance per answer: one legal reminder, one "confirm on gov.il" sentence, one contact block, one closing line. "Next stage:" (Step 3) names the next stage; the closing line names the action; each appears once.

Offer, but do not push, a printed checklist for the stage and a reminder plan for the next clock.

## Voice and tone

Write like the friend who already went through this, not like the department. The structure in Step 3 stays fixed; the language around it is everyday speech.

- Second person. In Hebrew use the plural imperative so no gender is assumed ("תשלמו את האגרה ותקבעו מטווח"), never the passive official register ("יש לבצע תשלום אגרה ולתאם הכשרה").
- Sentences of about 15 words or fewer. One idea per paragraph. Three to five bullets, then the next action.
- Every bureaucratic term gets a plain gloss in parentheses the first time: "אישור מותנה (הפתק שמאפשר להתחיל: לשלם, להתאמן ולקנות)". The glossary in `references/glossary.md` has the terms; the gloss is yours.
- Take numbers, dates and document names from gov.il. Rewrite everything else in everyday words; never paste official phrasing.
- One sentence of reassurance or light humour at the top is fine. None when the user may be committing an offence (an expired license with the firearm at home, a lost firearm): there the tone is direct and short.

Before: "לאחר קבלת האישור המותנה יש לבצע תשלום אגרה בשירות התשלומים הממשלתי ולתאם הכשרה במטווח מורשה."

After: "יש לכם אישור מותנה? יופי, מכאן זה בידיים שלכם. שלמו את האגרה באתר התשלומים, ותקבעו מטווח לחודש הקרוב."

## Stage map

Use this table as the spine of every conversation. Sources: gov.il service pages read on 14.09.2026 and rechecked on 28.09.2026, the Knesset Research Center review of 13.02.2024, and the Firearms Regulations (Threshold Conditions and Criteria), 2023.

| # | Stage | What the user does | What the authority does | Clock |
|---|-------|--------------------|-------------------------|-------|
| 1 | Eligibility | Runs the calculator, picks a criterion, collects proof | Nothing yet | None |
| 2 | Application | Submits online after national identification with health declaration, ID and appendix, service confirmation, criterion documents | SMS with request number and handling time; checks the file; police and Health Ministry consulted | Not published (2014 procedure: 30 days from a complete file, about 45 more on police or Health delay) |
| 3 | Interview | Answers a phone interview, or is exempt | Decides on a conditional approval | None published |
| 4 | Conditional approval | Pays the fee (71 NIS per year of validity, so three times that for a 3-year license; reservists 50 percent off), books a range | Issues the approval with a payment voucher | Date printed on it |
| 5 | Training | 4.5 consecutive hours, theory exam at 70 percent, 80 practice rounds, 20-round qualification at 70 percent; a 2-hour shortened track exists for prior training | Range reports the result | Theory pass valid 3 months |
| 6 | Purchase | Buys from a dealer (dealer handles the transfer and the paper license) or from a private person (bill of sale, both parties identified before a lawyer, sent to tservice@mops.gov.il) | Registers the transfer | None published |
| 7 | Card | Installs the home safe, carries the paper license | Mails the magnetic card | Up to 90 days |
| 8 | Year 2 | Refresher: theory, 40 rounds, 10-round test at 70 percent | Sends a reminder at the start of year 2 | Miss it: deposit at a dealer within 72 hours of notice |
| 9 | Year 3 | Renewal at the range: fee, forms from the personal area, photo, health declaration, refresher | Sends a reminder 3 months before expiry, mails the new card | Until the expiry date |
| 10 | Expired | Deposits the firearm at the police, then files a request, which counts as a new application | Decides; applies the surcharge tiers if it renews | Deposit within 72 hours; surcharge grows at 6 and 12 months |

## Examples

### Example 1: Just received the conditional approval

User says: "קיבלתי היום רישיון מותנה, מה עושים עכשיו?"

Actions:
1. Place the user at stage 4 without asking. Note that the document is called an "ishur mutne" (conditional approval) and is not yet a license; it cannot be used to carry anything.
2. Ask for the expiry date printed on the approval and run `python3 scripts/calculate_license_dates.py --conditional-expires <that date>`; with only the issue date (`--conditional-approval 2026-09-14`) the script shows an estimate. Add that the theory pass is valid for only 3 months once the training is done.
3. Give the stage-4 block: pay the fee through the government payment service or the postal bank (71 NIS per year as of 04.01.2026, 50 percent off for an active reservist with the card), print the payment confirmation, book an authorised range, bring the payment confirmation, a copy of the health declaration and the approval, and train on the same model the user intends to buy.
4. Mention the shortened 2-hour track if the user served in a security body or trained at an authorised range in the last 3 years; gov.il does not say at which stage it is approved, so ask the service center before booking.
5. Close: "Next action: pay the fee today and book the range for this month, so the purchase is done well before the date printed on the approval."

Result: the user knows when the approval expires, has one thing to do this week, and understands the training must match the firearm they will buy.

### Example 2: License expired two months ago

User says: "my rishayon neshek expired at the end of July and I only noticed now, the gun is at home"

Actions:
1. Place the user at stage 10. First ask one question: did they serve 30 or more reserve days in the 90 days before expiry, or get an SMS about an extension? If so, the license was extended automatically by 6 months (validity regulations reg. 4A) and may still be valid.
2. Ask for the exact expiry date on the license; "end of July" becomes 2026-07-31 as a stated assumption. Run `python3 scripts/calculate_license_dates.py --license-expires 2026-07-31 --today 2026-09-28` (add `--reservist-expiry yes` if it applies). Without an extension the license expired two months ago: holding the firearm is an offence, and the deposit was due within 72 hours of expiry (reg. 9(a)).
3. Ask whether the year-2 refresher was completed. If it was missed, the license may already have been cancelled under the 72-hour rule, and the service center should confirm the status before anything is paid.
4. Explain what comes next: a request after expiry counts as a new application under the criteria in force today (reg. 8); the 30-day window for the official to renew an expired license (validity regulations reg. 5) has passed; the 10-year continuity route is lost once the license lapses (reg. 10). If renewal is approved, the surcharge is one annual fee.
5. Close: "Next action: call the police station of your residence or business for instructions and deposit the firearm, the license and the ammunition there today, against a receipt; then call *8657 about a new application."

Result: the user checks the reservist extension, stops committing an offence, and knows the next step is a new application, not a routine renewal.

### Example 3: Moved to another town

User says: "עברתי דירה ליישוב אחר, זה משנה משהו ברישיון?"

Actions:
1. Ask which criterion the license was issued under. If it is "place of residence" (makom megurim), moving can end the criterion, and the holder must report that to the licensing official without delay (reg. 3(d)). Explain what follows: the official writes to the holder, who has 30 days to prove it or to prove another criterion, and up to 6 months in total before the license is cancelled, with the firearm deposited at a dealer meanwhile. A pistol license held 10 continuous years under criteria 1 to 9 may still be renewed without the criterion while it is valid (reg. 10).
2. Whatever the criterion, tell the user to update their contact details with the department through the contact-update form (linked from the license-copy page), because the card and every reminder go to the address on file, and the plastic card goes to the address registered with the Population Authority.
3. Tell them to run the eligibility calculator with the new address and to relocate the safe to the new home under the same specification.
4. Close: "Next action: run the calculator with the new address today, and report the move to the department this week."

Result: the user knows whether the move threatens the criterion, meets the duty to report, and has updated the address before a reminder goes astray.

### Example 4: Refused because of a police recommendation

User says: "got a refusal letter, it says based on a police recommendation, what can I do"

Actions:
1. Place the user at "refusal". State the clock first: 45 days from receiving the letter to file the appeal with the service center.
2. Describe the appeal package from the gov.il appeal page: the official appeal form, filled in and signed by a lawyer who certifies the facts, a reasoned letter, and supporting documents; no fee; decision within 45 days; the decision is final and further challenge goes to court.
3. Explain that a police-based appeal goes to a senior police officer for a response (Law s.12(c1)(2)), so the letter should answer the specific ground (for example a closed complaint or an expired restraining order) with documents, not character references.
4. Recommend a lawyer who handles firearm licensing. Do not produce a finished appeal letter or fill in the appeal form; give the structure and the points to cover (facts and dates, the ground as stated, why it does not apply or no longer applies, documents to attach) as raw material that the user and their lawyer write and sign themselves.
5. Close: "Next action: book a lawyer this week and collect the documents, so the appeal is in before day 45."

Result: the user files a focused, timely appeal instead of a late, general one.

## Bundled Resources

### Scripts
- `scripts/calculate_license_dates.py` -- Every clock from one or more dates: refresher, renewal, reservist and past wartime extensions, post-expiry deadlines, surcharge tier, and an "uncertain" status while an unconfirmed extension may run. Stdlib only. Run: `python3 scripts/calculate_license_dates.py --help`
- `scripts/build_stage_checklist.py` -- Document and action checklist per stage or event, English or Hebrew, with the official page per item. Run: `python3 scripts/build_stage_checklist.py --list`

### References
- `references/eligibility-criteria.md` -- Threshold conditions, age rules, Amendment 25, the 16 criteria, affidavit forms, license limits. For eligibility questions.
- `references/process-stages.md` -- Stages 1 to 7: submission, interview, conditional approval, fees, training, purchase, safe, card.
- `references/renewal-and-refresher.md` -- Refresher, renewal, deposits, extensions (reservist and past wartime orders), expiry, copies, contact details.
- `references/storage-ammunition-and-incidents.md` -- Safe specification, ammunition, loss and theft, sale or replacement, criterion ceased.
- `references/refusal-and-appeal.md` -- Grounds for refusal or cancellation, the Health Ministry route, the appeal, when to send the user to a lawyer.
- `references/glossary.md` -- Hebrew terms with transliteration and plain meaning.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [Kolzchut (All-Rights)](https://agentskills.co.il/he/mcp/kolzchut) | Pulls the current Kol Zchut entry on the firearm license procedure, useful for cross-checking a deadline or fee the user disputes. |
| [Israel Law](https://agentskills.co.il/he/mcp/israel-law) | Retrieves the text of the Firearms Law, 1949, and its regulations when a letter cites a section (for example section 12(c1) on appeals or section 15 on loss). |

## Gotchas

- The document called "rishayon mutne" by users is officially an "ishur mutne" (conditional approval). It is not a license and does not permit carrying or holding a firearm. Agents that call it a license lead users to think they can collect the firearm before training.
- Two different 3-month clocks exist: the theory-exam pass (3 months from the training) and the renewal reminder (3 months before expiry). Agents conflate them. The conditional approval has its own expiry, printed on it.
- The refresher is in year 2 and the renewal in year 3; both involve a range visit, but only the renewal carries the fee, the photo, the personal-area forms, and a new card. Agents describe them as one event.
- Ammunition: gov.il (2020) says 50 rounds per the license conditions; late-2023 press reports describe 100. Tell the user to read their own license conditions (`references/storage-ammunition-and-incidents.md`, section 3).
- Several department procedures published under freedom of information are dated 1.4.2014 and predate the 2023 regulations. Use them for the shape of the process only; the regulations and the current gov.il page win.
- The plastic card goes to the address registered with the Population Authority (Misrad Hapnim) unless another address was given to the department. Agents tell users to update only one of the two.
- The purchase and the training must match: same type and same caliber as the firearm named on the training confirmation. A user who trains on one model and buys another is sent back to the range.
- Costs the sources do not publish: the range's training price, police storage charges, and the turnaround for a late request. Say "not published, ask the range or the service center". The license fee is published (71 NIS per year of validity, up to 3 years), and the reservist discount applies at first issue too.
- A private license may not be used for guarding work, and under criteria 13 to 16 carrying is allowed only for the professional or sport use it was issued for (regulation 5).

## Reference Links

Official sources for verifying and updating the information in this skill:

| Source | URL | What to Check |
|--------|-----|---------------|
| gov.il, private firearm license application | https://www.gov.il/he/service/issue_firearms_license_to_a_private_individual | Documents, interview, conditional approval, training hours, purchase, 90-day card |
| gov.il, threshold conditions and criteria | https://www.gov.il/he/pages/criteria_for | Age rules, Amendment 25, criterion-ceased rule, affidavit forms |
| gov.il, private license renewal | https://www.gov.il/he/service/private_firearm_license_renewal | Renewal timing, 72-hour deposit, reservist discount, temporary license |
| gov.il, fees | https://www.gov.il/he/pages/fa_license_fees | Current fee table and late-renewal surcharge tiers |
| gov.il, home storage requirements | https://www.gov.il/he/pages/firearm_storage | Safe specification and storage rules |
| gov.il, appeal against refusal or cancellation | https://www.gov.il/he/service/firearm_license_appeal | Appeal form, 45-day deadline, lawyer signature |
| Knesset Research and Information Center, private firearm licensing review (13.02.2024) | https://fs.knesset.gov.il/25/Committees/25_cs_mmm_5856055.pdf | Reported validity of the conditional approval, interview exemptions, statistics |
| Firearms Law, 1949 (Wikisource) | https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%9B%D7%9C%D7%99_%D7%94%D7%99%D7%A8%D7%99%D7%99%D7%94 | Section 12 (conditions, cancellation, appeal), section 14 (deposit), section 15 (loss and theft) |
| Firearms Regulations (Validity of Licenses), 2023 (Wikisource) | https://he.wikisource.org/wiki/%D7%AA%D7%A7%D7%A0%D7%95%D7%AA_%D7%9B%D7%9C%D7%99_%D7%94%D7%99%D7%A8%D7%99%D7%99%D7%94_(%D7%AA%D7%95%D7%A7%D7%A4%D7%9D_%D7%A9%D7%9C_%D7%A8%D7%99%D7%A9%D7%99%D7%95%D7%A0%D7%95%D7%AA) | Extension on request (reg. 4), reservist extension (reg. 4A), renewal after expiry (reg. 5) |
| Kol Zchut, obtaining a firearm carry license | https://www.kolzchut.org.il/he/%D7%94%D7%95%D7%A6%D7%90%D7%AA_%D7%A8%D7%99%D7%A9%D7%99%D7%95%D7%9F_%D7%9C%D7%A0%D7%A9%D7%99%D7%90%D7%AA_%D7%A0%D7%A9%D7%A7 | Plain-language summary, kept current by Kol Zchut editors |

## Troubleshooting

### Error: "The user does not know which stage they are in"
Cause: The user has a pile of SMS messages and PDFs.
Solution: Ask for the most recent document by name: an SMS with a request number (stage 2), a link to book a phone interview (stage 3), a document titled "ishur mutne" with a payment voucher (stage 4), a range confirmation (stage 5), a bill of sale or a paper license from the dealer (stage 6 or 7), a plastic card (stage 8 onward). Map the document to the stage and continue.

### Error: "A number in the skill conflicts with what the user sees on gov.il"
Cause: Fees, round counts and validity periods have changed several times since 2023, and emergency extensions were issued in 2023, 2024, 2025 and 2026.
Solution: gov.il wins. Quote the user's page, note the date on it, and tell them the skill's figure carried a verification date of 28.09.2026. If the user's page is newer, use their figure and flag the skill for an update.

### Error: "The gov.il page returns 403 or an empty body to WebFetch"
Cause: gov.il blocks non-browser fetchers, and several pages render their content with JavaScript.
Solution: Use a browser tool if one is available, wait 3 to 4 seconds after navigation, and read the article element. Otherwise send the user the link and ask them to paste the relevant paragraph.

### Error: "The user asks how to get around a criterion"
Cause: The user does not qualify under any criterion and wants a workaround, such as a fictitious workplace or an address they do not live at.
Solution: Decline. Explain that the criteria list is closed and that the application and the health declaration are signed by the applicant as true. Offer the legitimate alternatives: check every criterion with the calculator, ask whether a real change (a job in an eligible workplace, volunteering in a recognised rescue body for a year) would qualify them, or consult a lawyer about their specific case.
