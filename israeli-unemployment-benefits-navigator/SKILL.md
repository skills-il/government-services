---
name: israeli-unemployment-benefits-navigator
description: "Walk a user through Israeli dmei avtala (דמי אבטלה / unemployment benefits) end to end: check eligibility under the 12-of-18 month qualifying period (tkufat akhshara, or 6-of-18 during Shaagat HaArie chal\"t), calculate the 2026 progressive benefit, map max days by age and dependents (50 to 300), warn about the 90-day resignation wait, surface stackable benefits (hashlamat hachnasa, hachshara miktzoit, severance interaction), and generate a Sherut HaTaasuka and Bituach Leumi application checklist. Use when a user asks about dmei avtala, eligibility, how much avtala they will get, how to apply, was laid off, fired, or placed on chal\"t in Israel. Do NOT use for other Bituach Leumi programs (israeli-bituach-leumi), net salary (israeli-payroll-calculator), reservist pay (israeli-miluim-manager), aliyah benefits (israeli-aliyah-navigator), or employment contract review."
license: MIT
allowed-tools: ''
compatibility: Works with Claude, Claude Code, ChatGPT, Cursor. Optional pairing with kolzchut MCP for live rule lookups. No network required for standalone calculations.
---

# Israeli Unemployment Benefits Navigator

## Problem
Every year, tens of thousands of Israelis lose their job or are placed on unpaid leave (חל"ת) and leave avtala money on the table because the rules are dense, the qualifying period is easy to miscount, and the Bituach Leumi website buries the progressive benefit formula under links. Resigning without knowing about the 90-day waiting period, registering late at Sherut HaTaasuka, or forgetting that only 12 salaried months out of the last 18 qualify, all cost real shekels. A separate set of users miss out on stackable benefits (hashlamat hachnasa for low earners, vocational training stipends, the 2026 שאגת הארי emergency 6-of-18 track) because nobody told them. This skill gives a clear "Am I eligible? How much will I get? What do I do first?" answer in one pass, with a personalized application checklist the user can execute the same day.

> All ₪ amounts in this skill are 2026 figures (effective 01.01.2026) and are linked to inflation. They re-link in January 2027. Always cross-check against btl.gov.il/benefits/Unemployment/Pages/hisuv.aspx for the current year before quoting numbers to a user.

## Instructions

### Step 1: Collect User Inputs

| Input | Required | Used for |
|-------|----------|----------|
| Reason employment ended | Yes | Fired / laid off / made redundant / resigned / chal"t. Determines the 90-day waiting period |
| Last day of work | Yes | Starts the 3-month registration clock and anchors the 18-month lookback |
| Age in years | Yes | Determines max benefit days and the under-28 vs 28+ benefit rate tier |
| Number of people you support (spouse + children) | Yes | Determines max benefit days bracket |
| Average monthly gross salary over the last 6 months | Yes | Drives benefit amount via the progressive tier formula |
| Number of months worked as an employee in the last 18 | Yes | Verifies tkufat akhshara (12 standard, 6 if on chal"t during Shaagat HaArie defining period) |
| Israeli resident? | Yes | Non-residents are ineligible |
| Already registered at Sherut HaTaasuka? | Yes | If not, this is the first action |
| Gender and exact date of birth | If aged 57 to 67 | Women born 1960 or later get a special 300-day track |
| On chal"t between 28 Feb 2026 and 14 May 2026? | Yes if chal"t | Triggers the Shaagat HaArie emergency track (see Special Cases) |
| Worked abroad in the last 18 months in a treaty country (US, UK, EU, CA)? | Yes if relevant | Foreign months may count via bilateral social-security treaty (form בל/627) |
| Currently receiving any other Bituach Leumi benefit (nechut, leda, hashlamat hachnasa)? | Yes | Some benefits cannot stack; some can supplement |

### Step 2: Check Eligibility (tkufat akhshara)

Run the eligibility gate in this order. Stop at the first failure and tell the user exactly which rule blocks them.

| Gate | Rule | Fail action |
|------|------|-------------|
| Residency | Must be an Israeli resident | Explain that non-residents and most foreign workers cannot claim dmei avtala |
| Age | Between 20 and 67 | Below 20: not eligible. Above 67: explain kiztavat zikna instead |
| Qualifying period (standard) | At least 12 months of work as a salaried employee (shakhir) in the last 18 months | Explain that osek months do not count, that even one day in a month counts as a full month |
| Qualifying period (Shaagat HaArie chal"t) | At least 6 months of salaried work in the last 18 months IF the chal"t falls inside the 28 Feb to 14 May 2026 defining period | Use the emergency track; see Special Cases |
| Registration window | Must register at Sherut HaTaasuka within 3 months of the last day of work | If outside window, eligibility may still exist but the 18-month lookback starts from registration; force-majeure waivers (hekel mizvad) exist for hospitalization, miluim, or being abroad for emergency |
| In-person follow-up | After online registration at taasuka.gov.il, attend the local branch in person within 14 days | Missing the in-person visit voids the registration |

Under Israeli law, a month with even a single day of salaried work counts as a full qualifying month. Mandatory IDF service, paid parental leave (dmei leda), miluim days, and paid sick leave from the employer all count toward the qualifying period. Osek (self-employed) months do NOT count toward standard akhshara, even if Bituach Leumi was paid.

**Self-employed to salaried trap.** A frequent rejection: someone closes their osek murshe, becomes a shakhir for 7 to 10 months, then gets fired. They have under 12 qualifying months and are denied. If a user lists recent osek months, count only the salaried months in the 18-month window; if it is under 12, advise waiting until they reach 12 (one extra month of salaried work can flip eligibility).

### Step 3: Check Waiting Period (reason for termination)

| Reason | Waiting period | Notes |
|--------|---------------|-------|
| Fired / laid off (pituin) | None | Full entitlement from day 1 |
| Made redundant | None | Same as fired |
| Employer bankrupt | None | Employee can claim both unpaid wages from Bituach Leumi and dmei avtala |
| Chal"t (unpaid leave) 30+ days, standard | None | Standard chalat rules |
| Chal"t 5+ days during Shaagat HaArie defining period | None | Emergency track, paid from day 1; no need to exhaust vacation first |
| Resignation without justified cause | 90 days | The 90-day clock runs from the registration date, not the last day of work. Calendar days, not work days. The wait delays the start; it does NOT reduce total max days |
| Resignation with justified cause (hitpatrut b'din mefuteret) | None | Must prove grounds. Bituach Leumi decides |
| Refused a suitable job offer from Sherut HaTaasuka | 90 days waiting + 30 days deducted from max-day total | Two separate penalties: a 90-day delay AND a permanent 30-day reduction in entitlement |

**What "suitable" means (post-2024 BL clarification):** salary within 25% of prior wage, commute under 60 minutes (or remote-eligible), profession within one degree of prior role. After day 60 of unemployment, the suitability test relaxes (claimants are expected to broaden their search).

**Severance pay (pitzuei piturin) interaction.** Legal pitzuim do NOT delay or reduce avtala. Adam meritzon (severance beyond the legal floor, e.g., generous "golden parachute") CAN postpone the start by the equivalent number of months under National Insurance Law s. 174 ("tashlumei avoda"). Ask the user if they received any payment beyond the standard pitzuim formula.

**Justified-cause resignation grounds (skip the 90-day wait):** documented health deterioration (must be from a rofeh tasukati / occupational physician, not a regular GP), 25%+ unilateral cut in pay over a 6-month window (excluding voluntary bonus reductions), forced relocation, sexual harassment with documented complaint (Tikkun 232 of 2023 shifted some burden of proof onto BL for harassment and wage-delay cases), spouse's job moves to another city, marriage relocation, return from leda when employer refuses to restore the role.

### Step 4: Calculate Maximum Benefit Days

Use the age + dependents table. "Dependents" = spouse + children the user supports. A working spouse earning above ~½ the average wage may not count as a tlui (BL evaluates per case).

| Age at start of unemployment | Dependents | Max days |
|------------------------------|-----------|----------|
| 20-25 | 0, 1, or 2 | 50 |
| 20-25 | 3 or more | 138 |
| 25-28 | 0, 1, or 2 | 67 |
| 25-28 | 3 or more | 138 |
| 28-35 | 0, 1, or 2 | 100 |
| 28-35 | 3 or more | 138 |
| 35-45 | 0, 1, or 2 | 138 |
| 35-45 | 3 or more | 175 |
| 45-67 | Any | 175 |
| Women 57-67 born 1960 or later | Any | 300 (special track, 18-month window) |

The maximum days must be used within 12 months from the 1st of the registration month. The special women's track uses 18 months instead of 12.

### Step 5: Calculate Daily Benefit Amount

The daily benefit is based on the user's average daily wage over the last 6 full months of work.

**Step 5a: Average daily wage**
```
average_daily_wage = (gross salary over last 6 months) / 150
```
(The divisor is 150, not 180, because Bituach Leumi assumes 25 working days per month * 6 months.)

**Step 5b: Apply the progressive formula for 2026**

Under 28 years old:

| Daily wage bracket | Rate |
|-------------------|------|
| Up to ₪207.50 | 60% |
| ₪207.50 to ₪311 | 40% on the portion above ₪207.50 |
| ₪311 to ₪415 | 35% on the portion above ₪311 |
| ₪415 to daily ceiling | 25% on the portion above ₪415 |

Aged 28 and over:

| Daily wage bracket | Rate |
|-------------------|------|
| Up to ₪207.50 | 80% |
| ₪207.50 to ₪311 | 50% on the portion above ₪207.50 |
| ₪311 to ₪415 | 45% on the portion above ₪311 |
| ₪415 to daily ceiling | 30% on the portion above ₪415 |

Sum each bracket contribution to get the gross daily benefit.

**Step 5c: Apply the 2026 daily ceilings**

- First 125 days of unemployment: maximum ₪550.76 per day
- Day 126 onwards: maximum ₪367.17 per day
- Cap whatever the formula produces to these ceilings

For long entitlements (138, 175, 300 days), the average daily benefit drops once the user crosses day 125. Do not multiply the day-1 rate by total max days; project the front portion at the higher ceiling and the tail at the lower ceiling.

**Step 5d: Payment cadence (5-weeks-per-month quirk)**

Bituach Leumi pays per "reporting weeks" (chodesh dmei avtala = 4 or 5 weeks depending on Sundays in the month), not per calendar month. Roughly four months a year contain a 5-week BL month, producing about 31 paid days. When projecting cash flow for the user, label the figure "approximate monthly" and show daily * 25 as a baseline only.

**Step 5e: Deductions**

The gross benefit is taxed like income:
- Income tax at the user's marginal rate (often near 0% for low-wage earners after credits/zikui)
- Bituach Leumi: fixed ₪48 per month as of 2026 (effective 01.01.2026; kolzchut.org.il still displays the older ₪32 figure, btl.gov.il is authoritative)
- Mas briut (health tax)

The net amount the user actually receives is the gross benefit minus these deductions. Rule of thumb: low-income claimants net close to 100%, mid-income about 85-90%, high-income (hitting ceilings) about 80-85%. Do not promise the user the gross number as take-home.

**Worked example (28+ earner making ₪15,000/month gross):**

```
6-month gross total: 15000 * 6 = 90,000
average_daily_wage: 90000 / 150 = 600

Bracket 1 (up to 207.50): 207.50 * 80% = 166.00
Bracket 2 (207.50 to 311): (311 - 207.50) * 50% = 51.75
Bracket 3 (311 to 415): (415 - 311) * 45% = 46.80
Bracket 4 (415 to 600): (600 - 415) * 30% = 55.50
daily_gross: 166.00 + 51.75 + 46.80 + 55.50 = 320.05

Ceiling check: 320.05 < 550.76 (ok for first 125 days)
Approx monthly gross (25 working days): 320.05 * 25 = 8,001.25
Net (after BL 48, health, marginal tax): typically ~85-90% of gross
```

### Step 6: Generate the Application Checklist

Give the user a personalized, ordered checklist. Each step references a real form or portal.

```
1. Register online at Sherut HaTaasuka
   URL: https://www.taasuka.gov.il
   - Required within 3 months of last workday
   - Bring: teudat zehut, last 3 payslips, termination letter

2. Visit your local Sherut HaTaasuka branch in person within 14 days
   - The online registration is not valid without this in-person follow-up
   - Bring: original teudat zehut, sefach, all docs from step 1
   - Output: dorsh avoda status, scheduled reporting days

3. File the Bituach Leumi unemployment claim
   URL: https://www.btl.gov.il
   - Unified online form through gov.il national ID login
   - Required: bank details, termination letter, 6 most recent payslips, FORM 126 (annual employer summary, NOT the monthly Form 100), completed Form 1514 from employer
   - If the employer refuses to fill Form 1514: under BL חוזר אבטלה 1342, a tatzhir + 3 payslips + bank statements showing wage transfers can substitute

4. Attend scheduled reporting (harshama) at Sherut HaTaasuka
   - Attend every scheduled meeting or face suspension
   - Apply to the required number of jobs per reporting period
   - Accept "suitable" offers under the 25%/60-min/profession test (relaxes after day 60)

5. Monitor the Bituach Leumi decision
   - First payment typically lands 30-45 days after registration
   - Check decision letter for any denial grounds

6. If denied or underpaid, file an appeal (irur)
   - Step A (informal): write to your local BL branch va'adat tvi'ot within 6 months of the decision, attach new evidence
   - Step B (formal): file at Beit Din Ezorit L'Avoda within 12 months of the original decision
   - If appealing a Va'adat Ararim ruling specifically, the deadline drops to 60 days
   - Free legal aid: Hasneguria HaMishpatit (Public Defender) for low-income claimants
```

### Step 7: Flag Common Denial Risks

Warn the user if any of these apply to their case:

| Risk | What Bituach Leumi will do | How to avoid |
|------|---------------------------|--------------|
| Resigned without justified cause | 90-day waiting period | Document any justified grounds and provide evidence |
| Refused a suitable job from Sherut HaTaasuka | 90-day wait + 30-day deduction from max days | Do not refuse offers that match the 25%/60-min/profession test |
| Did not register within 3 months | Lookback shifts, may lose qualifying months | Register immediately. If late due to hospitalization, miluim, or emergency travel, request a hekel mizvad waiver in writing |
| Missed scheduled reporting | Benefits suspended for the period | Always attend or reschedule in advance |
| Self-employed (osek) during last 18 months | Freelance months do not count toward standard akhshara | Need 12 salaried months specifically (or 6 under Shaagat HaArie chal"t track). One more salaried month may flip eligibility |
| Worked for a family member | Benefits denied unless arms-length employment is proven | Need all 5: payslips dated 12+ months pre-dispute, bank-transfer trail (no cash), third-party witness to actual work, dated employment contract, employer paid tax+BL+pension on time. BL חוזר 1287 |
| Employer refuses to fill Form 1514 | Claim stalls | Substitute with tatzhir + 3 payslips + bank statements (חוזר 1342) |
| Working part-time during unemployment | Benefit reduced (~75% of part-time gross is deducted from that month's avtala) | Report all income. Below the BL kotzbat patur (small-earnings exemption), reduction may not apply, verify thresholds |
| Worked abroad in last 18 months, returned to Israel | Fails standard akhshara | If country has bilateral SS treaty (US, UK, EU, CA, CH, others), submit form בל/627 to count foreign months |

## Special Cases

### Shaagat HaArie 2026 Emergency Chal"t Regime

Codified in חוק התוכנית לסיוע כלכלי (הוראת שעה)(תעסוקה), התשפ"ו-2026 (passed 30-31 March 2026). Applies if the user is on chal"t between 28 Feb 2026 and 14 Apr 2026 (extendable by joint Finance and Labor minister order to 14 May 2026).

| Standard track | Shaagat HaArie chal"t track |
|----------------|-----------------------------|
| 12 months akhshara out of 18 | 6 months out of 18 |
| Min 30-day chal"t to qualify | 5-day chal"t qualifies (retroactively reduced from 14 to 10 to 5) |
| 5-day deduction at start of payments | Avtala from day 1 of chal"t |
| Must exhaust accrued vacation first | No need to exhaust accrued vacation |
| Sherut HaTaasuka in-person within 14 days | Sherut HaTaasuka offices were closed 28 Feb-9 Apr 2026, registration window extended; rights preserved during closure |

Bonus payments are also available for workers aged 67+ under the same act. Verify final extension date and any further parameter changes at btl.gov.il/StateOfEmergency/ShaagatHari/Pages/halat-shaagatHari1.aspx before quoting numbers.

### Vocational Training (hachshara miktzoit) During Unemployment

Claimants placed in an approved Sherut HaTaasuka training program (kursim mukarim, maslulei mahalehet) keep receiving avtala throughout the program, and may receive an enhanced stipend (dmei kiyum) in addition. Days spent in training do NOT consume max-days the same way active job-seeking days do, verify with the case worker before assuming.

Refusing an assigned training course is treated like refusing a job offer: 90-day waiting penalty + 30-day deduction. Encourage the user to attend.

### Stacking with Hashlamat Hachnasa (Income Supplementation)

Avtala benefits below the household subsistence threshold can be topped up with hashlamat hachnasa for low earners with dependents (especially single parents, families with 3+ children). Typical supplementation is ₪1,500 to ₪2,000 per month. File via Bituach Leumi form 5320. Do not assume this is automatic, the claimant has to apply separately.

### Reservists, Returning Israelis, Foreign Treaty Workers

- **Laid off during or shortly after long miluim service.** Hok Khayalim Meshukhrarim s. 41a forbids dismissal during miluim and 30 days after. The avtala registration window is extended for the miluim period; a hekel mizvad waiver is granted on request.
- **Worked abroad recently.** If the user worked in a country with a bilateral social-security treaty (US, UK, Germany, France, Canada, Switzerland, Belgium, Netherlands, Czech Republic, Bulgaria, Sweden, Austria, Finland, Romania, Uruguay, others), foreign months can count toward akhshara via form בל/627. Bring the foreign country's social-insurance statement.
- **Foreign workers on permit.** Generally not entitled, with narrow exceptions for some Palestinian workers and caregivers.

### Maternity Leave Edge Cases

- Months on dmei leda count toward akhshara.
- The 60-day post-leda period is a protected period under Hok Avoda Nashim s. 9. Firing during this window without a Labor Ministry permit is illegal, register as fired AND consider a separate labor-court complaint.
- Extending leda with chofesh lelo tashlum (CHALAT) up to 12 months does not break tkufat akhshara.
- Drawing dmei leda blocks avtala for the leda period; switch carefully when leda ends.

### Sickness or Disability During Avtala

- Cannot draw both avtala and dmei machala simultaneously. Report sickness to BL within the reporting cadence; switch to sick-pay status. Some sick days still consume avtala max-days.
- Receiving full nechut klalit (75%+) blocks avtala. Partial disability (under 75%) sometimes allows partial avtala, case by case.

## Bundled Resources

### References

| File | Purpose |
|------|---------|
| `references/eligibility-rules.md` | Full eligibility rule table including Shaagat HaArie track, treaty months, edge cases |
| `references/benefit-calculation-tables.md` | 2026 progressive brackets, ceilings, payment cadence, worked examples |
| `references/application-forms.md` | Bituach Leumi and Sherut HaTaasuka forms, portals, contact numbers, appeal process |

### Scripts

| File | Purpose |
|------|---------|
| `scripts/avtala_calculator.py` | Command-line calculator. Inputs: age, dependents, 6-month salary, termination reason, residency. Outputs: eligibility, daily/monthly gross, estimated net, max days, average daily over the full entitlement (front-loaded vs tail), waiting period |

## Recommended MCP Servers

| MCP | When to pair | Purpose |
|-----|--------------|---------|
| `kolzchut` (All-Rights) | For authoritative rule text with legal citations | Pulls live content from Kolzchut's database of Israeli social rights, including dmei avtala eligibility and exceptions |
| `israeli-cbs` | If comparing expected benefit against regional wages | Central Bureau of Statistics salary and employment data |

If neither MCP is installed, the skill still works from the built-in reference tables, but the user should cross-check numbers against kolzchut.org.il or btl.gov.il before taking action.

## Gotchas

1. **Confusing qualifying months with calendar months.** One day of salaried work in a month counts as a full month. Agents often miscount because they assume 30 days equals 1 month. Use the "any paid day in the month" rule.

2. **Telling a resigner they get 90 days of nothing AND 90 fewer days total.** The 90-day waiting period blocks payments for 90 calendar days, but does NOT reduce total max days. Refusing a suitable job DOES both: 90 wait + 30-day deduction. Do not conflate them.

3. **Mixing up the under-28 and 28+ rate tables.** The under-28 rates are significantly lower (60/40/35/25%) than the 28+ rates (80/50/45/30%). Agents often grab the wrong table for a 26-year-old.

4. **Ignoring the 3-month registration window AND the 14-day in-person follow-up.** Online registration alone is invalid. The user must show up in person at the local Sherut HaTaasuka branch within 14 days. Force-majeure waivers exist (hospitalization, miluim, abroad for emergency).

5. **Applying the wrong daily ceiling past day 125.** After 125 days, the ceiling drops from ₪550.76 to ₪367.17. Agents keep using the higher number and overstate the back portion of long entitlements.

6. **Counting osek (freelance) months as qualifying.** Only salaried (shakhir) work counts toward standard akhshara. A year of freelance equals zero qualifying months.

7. **Promising the gross amount as net.** Benefits are taxable. Take-home is always lower (BL ₪48/month, health tax, income tax at marginal rate). Show gross AND estimated net.

8. **Telling someone the BL pays neat calendar months.** BL pays per reporting weeks (chodesh dmei avtala). Some months have 5 reporting weeks (about 31 paid days), some have 4 (about 25). Daily * 25 is an approximation, not a guarantee.

9. **Quoting 2026 figures past Jan 2027.** All ₪ values re-link with inflation each January. Always check btl.gov.il for the current year before stating numbers.

10. **Assuming the 90-day clock starts when work ended.** It starts on the registration date at Sherut HaTaasuka, calendar days. A delayed registration delays the clock too.

11. **Recommending Form 100 instead of Form 126.** Form 100 is monthly withholding (per payslip). BL needs Form 126 (annual employer summary). Bringing Form 100 alone causes rejection.

12. **Treating "single parent" as automatic 3+ dependents.** This shortcut appears in some BL guidance but the actual tlui count depends on the children supported. A single parent with 1 child counts as 2 tluyim, not 3+. Count actual dependents.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Bituach Leumi: how avtala is calculated (authoritative) | https://www.btl.gov.il/benefits/Unemployment/Pages/hisuv.aspx | Brackets, ceilings, ₪48 deduction |
| Bituach Leumi: eligibility | https://www.btl.gov.il/benefits/Unemployment/Pages/zakaut.aspx | Authoritative eligibility rules |
| Bituach Leumi: maximum entitlement period | https://www.btl.gov.il/benefits/Unemployment/Pages/tkufat_zakaut.aspx | Max days table including women's 300-day track |
| Bituach Leumi: Shaagat HaArie chal"t framework | https://www.btl.gov.il/StateOfEmergency/ShaagatHari/Pages/halat-shaagatHari1.aspx | Emergency 6-of-18, 5-day chal"t, day-1 payment |
| Bituach Leumi: reasons for stopping work | https://www.btl.gov.il/benefits/Unemployment/Pages/nesibothafsakatavoda.aspx | Resignation, refused-offer, justified-cause rules |
| Kolzchut: dmei avtala (right) | https://www.kolzchut.org.il/he/%D7%93%D7%9E%D7%99_%D7%90%D7%91%D7%98%D7%9C%D7%94 | Plain-language rules and exceptions in Hebrew |
| Kolzchut: qualifying period (tkufat akhshara) | https://www.kolzchut.org.il/he/%D7%AA%D7%A7%D7%95%D7%A4%D7%AA_%D7%90%D7%9B%D7%A9%D7%A8%D7%94_%D7%9C%D7%93%D7%9E%D7%99_%D7%90%D7%91%D7%98%D7%9C%D7%94 | How months are counted |
| Kolzchut: maximum days by age and dependents | https://www.kolzchut.org.il/he/%D7%9E%D7%A1%D7%A4%D7%A8_%D7%94%D7%99%D7%9E%D7%99%D7%9D_%D7%94%D7%9E%D7%99%D7%A8%D7%91%D7%99_%D7%9C%D7%A7%D7%91%D7%9C%D7%AA_%D7%93%D7%9E%D7%99_%D7%90%D7%91%D7%98%D7%9C%D7%94 | Max days table |
| Sherut HaTaasuka: applicant info | https://www.taasuka.gov.il/applicants/dmeiavtala/ | Registration steps |
| Bituach Leumi: special benefits for women 57-67 | https://www.btl.gov.il/benefits/Unemployment/Pages/zecoyot-nasim.aspx | 300-day track rules |

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Benefit amount looks too high | Did not apply the daily ceiling or used wrong age tier | Re-check age is 28+ vs under-28, apply ₪550.76 / ₪367.17 ceilings |
| Benefit projection over a long entitlement looks too high | Used day-1 ceiling for the entire period | After day 125 the ceiling drops to ₪367.17. Project front and tail separately |
| User has only 11 qualifying months | Just short of the 12-month threshold | Explain the rule. If they can wait one more month of salaried work, they reach 12. If they were on chal"t in the Shaagat HaArie defining period, only 6 months may be needed |
| Resigner confused about 90-day wait | Thinks they lose 90 days of total entitlement | Clarify: the 90-day wait delays the start (from registration date, not termination date), but does not reduce total max days. Refusing a job offer adds a 30-day reduction on top |
| User was fired from a family member's business | Bituach Leumi rejects as non-arms-length | Need all 5: dated employment contract, payslips predating dispute by 12+ months, bank-transfer wage trail, third-party witness, employer paid tax+BL+pension on time (חוזר 1287) |
| Employer refuses to provide Form 1514 | Claim stalls without employer cooperation | Per חוזר אבטלה 1342, substitute with a tatzhir + 3 payslips + bank statements showing wage transfers |
| Calculation shows benefit below minimum wage | Low salary user | Confirm tier 1 at the correct rate (80% for 28+, 60% for under 28). Still may be low, consider hashlamat hachnasa stacking (form 5320) |
| Returning Israeli denied for missing akhshara | Foreign months not counted | If country has a social-security treaty with Israel, file form בל/627 and attach the foreign social-insurance statement |
| Late registration due to hospitalization or miluim | Standard 3-month window missed | Request a hekel mizvad waiver in writing to the local BL branch with documentation |
| Claim denied with no clear explanation | Decision letter unclear | Step 1: write to local va'adat tvi'ot within 6 months. Step 2: appeal to Beit Din Ezorit L'Avoda within 12 months. Va'adat Ararim ruling appeals: 60 days only |
