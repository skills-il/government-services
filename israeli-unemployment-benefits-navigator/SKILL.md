---
name: israeli-unemployment-benefits-navigator
description: "Walk a user through Israeli dmei avtala (דמי אבטלה / unemployment benefits) end to end: check eligibility under the 12-of-18 month qualifying period (tkufat akhshara; the 6-of-18 chal\"t variant applied only inside the Shaagat HaAri window, which closed 14.5.2026), calculate the 2026 progressive benefit, map max days by age and dependents (50 to 300), warn about the 90-day resignation wait, surface stackable benefits (hashlamat hachnasa, hachshara miktzoit, severance interaction), and generate a Sherut HaTaasuka and Bituach Leumi application checklist. Use when a user asks about dmei avtala, eligibility, how much avtala they will get, how to apply, was laid off, fired, or placed on chal\"t in Israel. Do NOT use for other Bituach Leumi programs (israeli-bituach-leumi), net salary (israeli-payroll-calculator), reservist pay (israeli-miluim-manager), aliyah benefits (israeli-aliyah-navigator), or employment contract review."
license: MIT
allowed-tools: ''
compatibility: Works with Claude, Claude Code, ChatGPT, Cursor. Optional pairing with kolzchut MCP for live rule lookups. No network required for standalone calculations.
---

# Israeli Unemployment Benefits Navigator

## Legal notice

This is a free information tool operated by an AI model. It helps you organise and complete forms for government authorities. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by an advocate, tax adviser, or accountant. The output is not legal, tax, or other professional advice. An AI model may err, omit data, or present a wrong conclusion.

A form submitted to an authority is a document whose contents are your responsibility, and incorrect details in it can carry liability. Check every field before filing, and do not file a form whose contents you do not understand. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and all use of its output is the user's sole responsibility.


## Problem
Every year tens of thousands of Israelis lose their job or are placed on unpaid leave (חל"ת) and leave avtala money on the table. Bituach Leumi publishes the progressive formula, the dependant test, the exclusion list and the payment deductions on five separate pages. Resigning without knowing about the 90-day wait, being a controlling shareholder and never being told that alone disqualifies you, or missing that a 22-year-old in regular service still counts as a dependant, all cost real shekels. This skill answers "Am I eligible? How much will I get? What do I do first?" in one pass, with a checklist the user can execute the same day.

> All ₪ amounts are 2026 figures (effective 01.01.2026), linked to inflation and re-linked each January. Cross-check btl.gov.il/benefits/Unemployment/Pages/hisuv.aspx before quoting a number.

## Instructions

### Step 1: Collect User Inputs

| Input | Required | Used for |
|-------|----------|----------|
| Reason employment ended | Yes | Fired / redundant / contract ended / resigned / retired / chal"t. Determines the start date |
| Last day of work | Yes | Anchors the 18-month lookback and the 90-day resignation clock |
| Age in years | Yes | Determines max days and the under-28 vs 28+ rate tier |
| Number of people you support | Yes | Determines the max-days bracket; test each against the tlui limbs in Step 4 |
| Average monthly gross salary over the last 6 months | Yes | Drives the progressive formula |
| Number of months worked as an employee in the last 18 | Yes | Verifies tkufat akhshara. **12 is the operative rule.** Only months between age 18 and 67 count |
| Osek, controlling shareholder, kibbutz member, in regular/national service, or a non-working student? | Yes | Any one of these is a hard exclusion from the unemployment branch, checked before anything else |
| Israeli resident? | Yes | Non-residents are ineligible |
| Registered at Sherut HaTaasuka? | Yes | If not, this is the first action |
| Gender and exact date of birth | If aged 57 to 67 | Women born 1.1.1960 or later get a 300-day track, and it splits at 60 |
| Worked abroad in the last 18 months? | If relevant | Only three treaty countries count; see Step 7 |
| Receiving another BL benefit? | Yes | Some cannot stack; some supplement |

### Step 2: Check Eligibility (tkufat akhshara)

Run the gates in order. Stop at the first failure and name the rule that blocks them.

| Gate | Rule | Fail action |
|------|------|-------------|
| Residency | Must be an Israeli resident (or hold a permanent / temporary residence permit) | Explain that non-residents and most foreign workers cannot claim dmei avtala |
| **Insured at all** | The excluded populations are outside the unemployment branch no matter how many salaried months they have: **osek**; **a controlling shareholder in a closely-held company, even when he draws a salary from it and contributions were paid**; a kibbutz or moshav-shitufi member unless employed outside the collective; a soldier in regular service or anyone in national/civil service, for that service; students and yeshiva students who are not employees | Stop here. This is the most-missed refusal: 12 clean salaried months and still no entitlement. Full list in `references/eligibility-rules.md` |
| Age | Between 20 and 67 | Above 67: explain kitzvat zikna instead. **Under 20 is not an automatic bar**: a closed exception list covers IDF dischargees, 24-month national-service completers, IDF-exempt or deferred claimants, and sole breadwinners, and a na'ar from 15 has a separate grant track. See `references/eligibility-rules.md`; do not tell an under-20 claimant they are simply ineligible |
| Qualifying period (standard) | At least 12 months of work as a salaried employee (shakhir) in the last 18 months. Only work months **between age 18 and 67** count | Explain that osek months do not count, that even one day in a month counts as a full month |
| Registration window | **Register now, not later.** Entitlement runs from the registration date; earlier days are lost, not backdated. Three months from the last workday is the outer backstop, not a target | Past it, the 18-month lookback starts from registration. Force-majeure waivers exist |
| In-person follow-up | After online registration at taasuka.gov.il, attend the local branch in person within 14 days | Missing the in-person visit voids the registration |

One day of salaried work makes a full qualifying month. Also counting: IDF service (up to 6 months), national service (up to 6, on conditions), miluim, the first 2 employer-insured chal"t months, paid vacation and holiday days (but NOT pidyon chufsha paid on severance), mourning days even if unpaid, sick leave, dmei pgia / dmei leda / shmirat herayon, and pay for failure to give notice (which blocks benefit for its period AND counts toward akhshara). Osek months do NOT. The 18-month window itself extends for approved training, illness with no sick pay, and maternity leave, each with a cap: see `references/eligibility-rules.md`.

**Self-employed to salaried trap.** Someone closes their osek, works as a shakhir 7 to 10 months, is fired, and is denied on under 12 months. Count only salaried months; one more can flip eligibility.

### Step 3: Check Waiting Period (reason for termination)

| Reason | Waiting period | Notes |
|--------|---------------|-------|
| Fired / laid off (pituin) | None | Full entitlement from day 1 |
| Made redundant, or a fixed-term contract ended | None | Same as fired |
| Dismissed without lawful prior notice | See notes | Entitlement is examined from the last payment day, or from the end of 30 days from the start of the notice, **whichever is earlier**. That paid period counts toward akhshara and carries no benefit |
| Employer bankrupt | None | Can claim unpaid wages from BL as well as avtala |
| Chal"t (unpaid leave) 30+ days, **employer-initiated** | None | Remaining vacation days are set off first: a 50-day chal"t with 20 vacation days left pays from **day 21**. The vacation balance does not shorten the chal"t and the employee need not consume it. Returning to work even for single days stops the benefit from the day of return |
| Chal"t the **employee** initiated | **Not eligible at all** | `מי שיצא לחל"ת מיוזמתו (גם אם החל"ת מוצדק) - לא יהיה זכאי לדמי אבטלה`. A disqualification, not a delay. Do not read it as a waiting period |
| Retirement before pension age, employer-initiated or under an early-retirement scheme | None | Entitled from the first day of attendance |
| Voluntary retirement before pension age | 90 days | Treated as resignation. **A woman retiring voluntarily after 62** is treated the same way, unless the retirement had justified cause |
| Resignation without justified cause | 90 days | The 90-day clock runs from the **day work ceased** (`מיום הפסקת העבודה`), not from the registration date. Calendar days, not work days. Register anyway during the wait. The wait delays the start; it does NOT reduce total max days |
| Resignation with justified cause (hitpatrut b'din mefuteret) | None | Must prove grounds. Bituach Leumi decides |
| Refused a suitable job offer from Sherut HaTaasuka | 90 days waiting + 30 days deducted from max-day total | Two separate penalties, applied every time: a 90-day delay AND a permanent 30-day cut in entitlement. See Step 7 for the two women's-track exceptions |
| Teacher on a shnat shabbaton | Not eligible | May not work more than a third of a post, so not available for offered work |

**What "suitable" means (s. 165):** job type matches the last 3 years or the claimant's training, the wage is at least the benefit otherwise due, and it needs no move of home (a 60 km test). The first two limbs relax by age; timings in `references/eligibility-rules.md`.

**Severance interaction.** Legal pitzuim do NOT delay or reduce avtala. What postpones it is vacation pay and pay in lieu of notice (up to one month). Ask how each was labelled on the payslip.

**Justified-cause resignation grounds (skip the 90-day wait).** The eight causes BL itself publishes; attach evidence for whichever applies. (1) Har'a muchashit in the conditions of employment, or circumstances making carrying on impossible. (2) Health, the claimant's **or a family member's** (spouse, parent, child, grandchild, brother, sister). (3) A change of home or workplace where the distance exceeds **60 km**, or **40 km for a mother of a child under 7**. (4) Sexual harassment at work. (5) A te'udat miktzoa holder working outside their trade who resigns to work in it. (6) Staying in a domestic-violence shelter. (7) Resignation from a **new** job held up to 6 months where no earlier entitlement was realised. (8) Resignation from a **second** job, where two jobs of similar scope were held, one left with justification, and the second continued up to 3 months. A pay cut is argued under limb 1; BL publishes no percentage test, so do not quote one.

### Step 4: Calculate Maximum Benefit Days

Use the age + dependents table. **A tlui is a statutory test, not a judgement call.** A **husband** counts at 70+, or 50+ with income no higher than 57% of the average wage, **₪7,848 a month (from 01.01.2026)**. A **wife** counts only if all three hold: married a year or bore his child; 45+ or has his child with her; income no higher than ₪7,848. A **child** counts if under 18; under 20 finishing secondary school or a bagrut, or learning-disabled in a BL-recognised framework; under 20 as an IDF pre-military shocher; under 21 volunteering for a public purpose up to 12 months with service deferred; or **under 24 in regular IDF service, national service, or atuda with service deferred**. Stepchildren, adopted children and a wholly-maintained grandchild count; a married minor does not. The under-24 limbs are the ones agents drop, and dropping one can cost a 30-year-old 38 days. Full text in `references/benefit-calculation-tables.md`.

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
| Discharged soldier, unemployment starting in the first year after release | Any | 70 |

Days must be used within 12 months of the 1st of the registration month; the women's track uses 18.

**Discharged soldiers and national-service completers.** Unemployment starting in the first year after release is capped at **70 days**, with a statutory daily minimum of **₪144.62**. Up to 6 months of regular service count toward akhshara. A national or civil service dischargee gets this track only after **24 months**, or as a woman who served 6+ months and married within 30 days of stopping; shorter service means ordinary rules.

**Vocational-training floor.** A trainee with **fewer than 12 years of schooling** whose maximum is under 138 days is paid for up to **138 days**. Do not flatten a low-schooling dischargee to 70.

**Repeat claimant (2+ claims in 4 years).** Under 40: all claims capped at **180%** of the maximum, and once 100% of days are used the daily maximum drops to **₪468.15**. 40 and over: no cap on the amount, but days paid in the rolling preceding 11 months are netted off monthly. Examples: `references/benefit-calculation-tables.md`.

### Step 5: Calculate Daily Benefit Amount

Based on the average daily wage over the last 6 full months of work.

**Step 5a: Average daily wage**
```
average_daily_wage = (gross salary over last 6 months) / 150
```
(150, not 180: BL assumes 25 working days per month over 6 months.)

**Step 5b: Apply the progressive formula for 2026**

Under 28 years old:

| Daily wage bracket | Rate |
|-------------------|------|
| Up to ₪207.50 | 60% |
| ₪207.50 to ₪311.25 | 40% on the portion above ₪207.50 |
| ₪311.25 to ₪415 | 35% on the portion above ₪311.25 |
| ₪415 to ₪2,075 | 25% on the portion above ₪415 |

Aged 28 and over:

| Daily wage bracket | Rate |
|-------------------|------|
| Up to ₪207.50 | 80% |
| ₪207.50 to ₪311.25 | 50% on the portion above ₪207.50 |
| ₪311.25 to ₪415 | 45% on the portion above ₪311.25 |
| ₪415 to ₪2,075 | 30% on the portion above ₪415 |



**Step 5c: Apply the 2026 daily ceilings**

- First 125 days of unemployment: maximum ₪550.76 per day
- Days 126-175: maximum ₪367.17 per day
- Days 176+: maximum ₪201.03 per day, but **ONLY for a woman aged 57 to 60** on the 300-day track. A woman aged **60 to 67** on the same 300-day track has **NO** day-176 cap: her tail stays at ₪367.17. Applying 201.03 to her understates her entitlement by (367.17 - 201.03) for each of the 125 days from day 176, up to **₪20,767.50** at the ceiling. A duration rule and its payment rule are not the same rule.
Cap the formula's output to these ceilings. For long entitlements the average drops after day 125: project the front and the tail separately, never the day-1 rate times total days.

**Step 5d: Payable days per month**

BL pays for the **"possible work days" in each calendar month, and those exclude Shabbat** (`ימים אלה אינם כוללים את ימי שבת`), so a real month carries about 26 payable days and moves month to month. Treat `daily * 25` as a conservative baseline. Do not confuse this with the 150 divisor, a separate convention.

**Step 5d-bis: The first 5 unemployment days are never paid**

No benefit is paid for the **first 5 unemployment days in each 4 consecutive months of attendance**, counted from the first attendance. These days are **not** deducted from the quota, so they cut the cash, not the entitlement. Over a 138-day or 175-day claim it bites two or three times. A projection that ignores it overstates month 1 by five days.

**Step 5d-ter: Hefreshim.** If the employer pays anything AFTER employment ended that relates to the **6 months used to build the average daily wage** (a late bonus, back-pay, a labour-court settlement), the base re-opens and the claimant may be owed a top-up on benefit already paid. Not automatic: they apply to their local BL branch.

**Step 5e: Deductions**

The gross benefit is taxed: income tax withheld at source (often near 0% for low earners after credits; a claimant holding an exemption or reduction certificate should file it with BL, or reclaim from the ITA), Bituach Leumi at the fixed minimum of **₪48 a month** (kolzchut still shows the older ₪32; btl.gov.il is authoritative), and mas briut. Low earners net close to 100%, mid-income about 85-90%, ceiling-hitters about 80-85%. Never promise the gross as take-home.

**Worked examples** for both age tiers, the long-entitlement projection, and the women's three-slice 300-day projection are in `references/benefit-calculation-tables.md`.

### Step 6: Generate the Application Checklist

Give the user a personalized, ordered checklist.

```
1. Register online at Sherut HaTaasuka
   URL: https://www.taasuka.gov.il
   - Register immediately; entitlement runs from the registration date
   - Bring: teudat zehut, last 3 payslips, termination letter

2. Visit your local branch in person within 14 days
   - The online registration is not valid without it
   - Bring: original teudat zehut, sefach, all docs from step 1

3. File the Bituach Leumi unemployment claim (form T1500)
   URL: https://www.btl.gov.il/Pages/default.aspx
   - Unified online form through gov.il national ID login; if not yet registered at Sherut HaTaasuka, the same form does both
   - File within 12 months of first attendance. Filing later pays only for the 12 months preceding the filing date
   - Required: bank details, a signed and stamped employer confirmation of the reason and date employment ended, and the 6 most recent payslips including the final month, from every employer. Check the employer transmitted Form 100 (your wage data); if not, attach an employer confirmation of period and wage, or 12 payslips out of the last 18
   - If the employer will not sign it: the affidavit substitute is not published on any reachable BTL page, so treat it as unconfirmed and call *6050

4. Attend scheduled reporting at Sherut HaTaasuka
   - Missing a day costs the benefit for every day since the last attendance
   - Accept "suitable" offers under the s. 165 test

5. Monitor the Bituach Leumi decision
   - Benefit is paid on or about the 12th of the month for the previous month's attendance days
   - Check the decision letter for any denial grounds

6. If denied or underpaid, appeal (irur)
   - Informal: local BL va'adat tvi'ot, with new evidence. Formal: Beit Din Ezorit L'Avoda
   - **Do not quote a deadline from memory.** The windows usually cited could not be confirmed on any reachable source. Read the deadline off the decision letter, which states it, or call *6050
   - Free legal aid runs through the Legal Aid Department (האגף לסיוע משפטי) at the Ministry of Justice, not the Public Defender, which is criminal only
```

### Step 7: Flag Common Denial Risks

Warn the user if any of these apply:

| Risk | What BL will do | How to avoid |
|------|-----------------|--------------|
| Resigned without justified cause | 90-day wait | Document justified grounds |
| Refused a suitable job, training or professional conversion from Sherut HaTaasuka | 90 days with no benefit from the day of refusal, every time, plus 30 days deducted from the quota. **Two published exceptions:** a woman aged 57-60 on the 300-day track who refuses training from **day 176 onward** forfeits her whole remaining balance, not 90+30; and a woman aged **60-67** on that track keeps receiving benefit as usual, the penalty does not apply to her at all | Do not refuse offers that meet the s. 165 suitability test, and do not quote the 90+30 penalty to a woman on the 300-day track without checking which side of 60 she is on |
| Registered late | Lookback shifts, may lose qualifying months | Register immediately; force-majeure waivers exist |
| Missed scheduled reporting | No benefit for the days between the previous and next attendance | Attend, or declare a new job so prior days are still paid |
| Self-employed (osek) during last 18 months | Freelance months do not count toward akhshara, and an osek is not insured for unemployment at all | Need 12 salaried months specifically. One more salaried month may flip eligibility |
| Worked for a family member | Denied unless arms-length employment is proven | Bring a dated contract, payslips predating any dispute, a bank-transfer wage trail rather than cash, a third-party witness, and proof tax, BL and pension were paid on time |
| Employer will not sign the termination confirmation | Claim stalls | File within the 12-month window with what you have and call *6050 |
| Working part-time | BL compares per day: wage / days worked against the daily benefit. Below it, you get the difference; at or above, nothing for those days | Report all income. For a few low-paying days, ask the lishka not to record unemployment days for them |
| Worked abroad in last 18 months | May fail akhshara | An Israeli employer plus a contract signed in Israel qualifies directly. Aggregation applies ONLY to the unemployment-branch treaty countries, **Austria, the Netherlands and Sweden**; the general treaties with the US, UK, Germany, France, Canada and Switzerland do NOT cover unemployment |

## Special Cases

### Shaagat HaAri 2026 Emergency Chal"t Regime [WINDOW CLOSED 14.5.2026]

**This window has closed and none of its concessions are available.** The defining period ran 28 Feb to 14 Apr 2026, extendable by joint ministerial order only to 14 May 2026. For any chal"t or job loss beginning after that date the **standard 12-of-18 rule is the only rule**. Ask about it only to classify an older claim, retroactive employer report, or appeal still in process.

The framework is חוק התוכנית לסיוע כלכלי (הוראת שעה) (תעסוקה), התשפ"ו-2026, recorded as **התקבל בכנסת ביום י״ג בניסן התשפ״ו (31 במרץ 2026)**. Kol-Zchut notes it can be re-activated by order for a future emergency through the end of 2027, so treat it as a dormant standby mechanism.

For a claim that did fall inside the window the concessions were akhshara cut to **6 months out of 18** (and to **3 out of 18** for named special populations), benefit from **day 1** with no 5-day deduction, no need to exhaust accrued vacation, and a bifurcated minimum chal"t length of **5 consecutive calendar days** only for chal"t starting 28.2.2026 or 1.3.2026 and **10 consecutive calendar days** otherwise. Every remaining rule, and the attachment each special population needs, is in `references/eligibility-rules.md`.

### Other Special Cases

Vocational training, hashlamat hachnasa (form 5320), miluim dismissal protection under s. 41a, the narrow work-abroad routes, maternity-leave edge cases, and sickness or a competing disability benefit are all in `references/eligibility-rules.md`. Sick days are the one most often got wrong: up to 30 are payable inside the unemployment period and **are** deducted from the quota.

## Bundled Resources

### References

| File | Purpose |
|------|---------|
| `references/eligibility-rules.md` | Exclusion list, extra qualifying months, window extensions, the eight justified causes, the closed Shaagat HaArie track |
| `references/benefit-calculation-tables.md` | Brackets, ceilings, dependant definitions, payable days, hefreshim, worked examples |
| `references/application-forms.md` | Forms, portals, contacts, appeals, and which are unverified |

### Scripts

| File | Purpose |
|------|---------|
| `scripts/avtala_calculator.py` | CLI calculator. Outputs eligibility, daily and monthly gross, estimated net, max days, the front-vs-tail projection, the unpaid first-5-day blocks, and the waiting period. Runs the exclusion gate first (`--not-insured`) and models the refusal penalty, the repeat-claimant reduction, the 138-day training floor, and the chal"t and retirement disqualifications |

## Recommended MCP Servers

| MCP | What it adds |
|-----|--------------|
| `kolzchut` (All-Rights) | Live rule text with legal citations, including avtala eligibility and exceptions |
| `israeli-cbs` | CBS salary and employment data, for comparing an expected benefit against regional wages |

Without them the skill works from the bundled tables; cross-check btl.gov.il before acting.

## Gotchas

1. **Skipping the exclusion gate.** A controlling shareholder in a closely-held company, an osek, a kibbutz member, or someone in regular or national service is outside the unemployment branch entirely. Twelve clean salaried months do not help them.

2. **Confusing qualifying months with calendar months.** One day of salaried work makes a full qualifying month. Count only months between age 18 and 67.

3. **Conflating the two penalties.** The 90-day resignation wait delays payment and does NOT reduce max days. Refusing a suitable offer does both: 90 days plus a permanent 30-day cut. The 90+30 penalty is not universal, see gotcha 8.

4. **Mixing up the under-28 and 28+ rate tables.** Under-28 rates (60/40/35/25%) are much lower than 28+ (80/50/45/30%). Agents routinely grab the wrong one for a 26-year-old.

5. **Applying the wrong daily ceiling past day 125.** After 125 payment days the ceiling drops from ₪550.76 to ₪367.17. Project the front and the tail separately.

6. **Projecting cash without the unpaid first 5 days.** The first 5 unemployment days in each 4 consecutive attendance months are never paid, and are not deducted from the quota. Agents quote a full first month and the user is five days short.

7. **Under-counting dependants.** A 22-year-old in regular IDF service, national service, or atuda is still a tlui. Missing one limb can drop a 30-year-old from 138 days to 100. "Single parent" is not automatically 3+.

8. **Quoting the refusal penalty to a woman on the 300-day track.** A woman aged 60-67 keeps her benefit in full when she refuses work or training. A woman aged 57-60 who refuses training from day 176 forfeits her entire remaining balance, which is worse than 90+30. Check which side of 60 she is on.

9. **Treating employee-initiated chal"t as a waiting period.** It is a full disqualification, however justified the leave. Only employer-initiated chal"t qualifies, and remaining vacation days are set off before payment starts.

10. **Telling an under-20 claimant they are ineligible.** Under 20 is not an automatic bar; a closed exception list applies, and a na'ar from 15 has a separate track.

11. **Promising gross as net.** The benefit is taxable: BL ₪48/month, health tax, income tax. Show gross AND estimated net.

12. **Assuming the 90-day resignation clock starts at registration.** BL counts it from the day work ceased: `אם הפסקת לעבוד מרצונך תוכל להתחיל לקבל דמי אבטלה רק לאחר שחלפו 90 יום מיום הפסקת העבודה`. Register immediately anyway.

13. **Telling the claimant Form 100 is the wrong document.** It is not. BTL asks the claimant to check the employer transmitted Form 100; only if not, attach an employer confirmation or 12 payslips out of 18. Form 126 is the employer's annual report to the assessor and is not on BTL's list.

14. **Quoting 2026 figures past January 2027.** Every ₪ value re-links with inflation each January.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| BL: how avtala is calculated | https://www.btl.gov.il/benefits/Unemployment/Pages/hisuv.aspx | Brackets, ceilings, ₪48 deduction |
| BL: eligibility | https://www.btl.gov.il/benefits/Unemployment/Pages/zakaut.aspx | The five conditions, the not-insured exclusion list |
| BL: reasons for stopping work | https://www.btl.gov.il/benefits/Unemployment/Pages/nesibothafsakatavoda.aspx | Start date by reason, the eight justified causes, chal"t, retirement |
| BL: extra qualifying months | https://www.btl.gov.il/benefits/Unemployment/Pages/DaysHaxhsharaAvt.aspx | What else counts toward the 12, window extensions, the three treaty countries |
| BL: maximum entitlement period | https://www.btl.gov.il/benefits/Unemployment/Pages/tkufat_zakaut.aspx | Max days grid, tlui definitions, repeat-claimant rules |
| BL: payment of the benefit | https://www.btl.gov.il/benefits/Unemployment/Pages/pay.aspx | Unpaid first 5 days, vacation pay, notice pay, refusal penalty, payable days |
| BL: income during unemployment | https://www.btl.gov.il/benefits/Unemployment/Pages/incomes.aspx | Per-day offsets for salaried, self-employed and pension income |
| BL: repeat claimant | https://www.btl.gov.il/benefits/Unemployment/Pages/MovtalHozer.aspx | The 180%/80% rule and the ₪468.15 cap |
| BL: women 57-67 | https://www.btl.gov.il/benefits/Unemployment/Pages/zecoyot-nasim.aspx | The 57-60 vs 60-67 split: the ₪201.03 cap and the refusal rules |
| Sherut HaTaasuka | https://www.taasuka.gov.il/applicants/dmeiavtala/ | Registration and attendance |

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Benefit amount looks too high | Wrong age tier, or the daily ceiling was not applied | Re-check 28+ vs under-28, then cap at ₪550.76 / ₪367.17 |
| Long-entitlement projection looks too high | Day-1 ceiling used for the whole period, or the unpaid first-5-days blocks were ignored | Project days 1-125 and 126+ separately, then subtract 5 unpaid days per 4 attendance months |
| Claimant has 12 clean salaried months and was still refused | Almost always an exclusion, not a shortfall | Check the exclusion gate, above all a controlling shareholding in their own closely-held company |
| Employer paid a bonus or settlement after the claim was decided | It covered the 6-month base period | The average daily wage re-opens. Apply to the local BL branch for hefreshim; it is not paid automatically |
| Claimant has only 11 qualifying months | Just short of the threshold | One more salaried month reaches 12. Check whether IDF service, miluim, dmei leda or the first 2 insured chal"t months close the gap |
| Resigner confused about the 90-day wait | Thinks they lose 90 days of entitlement | The wait delays the start, counted from the day work ceased, and does not reduce max days |
| Woman on the 300-day track quoted the wrong penalty or the wrong tail | The track splits at 60 | Under 60: ₪201.03 from day 176, and forfeiting the balance if she refuses training then. 60 and over: no day-176 cap and no refusal penalty |
| Chal"t claim refused outright | The leave was employee-initiated | That is a disqualification, not a delay. Confirm who initiated it before anything else |
| Benefit below expectation in the first month | The unpaid first 5 days, or vacation-day offset on a chal"t | Both are normal. Neither reduces the max-days quota |
| Returning Israeli denied for missing akhshara | Foreign months not counted, or the 18-month window was not extended | Aggregation covers only Austria, the Netherlands and Sweden. Separately, check whether approved training (up to 12 months), illness with no sick pay (up to 6), or maternity leave should have pushed the window back |
| Claim denied with no clear explanation | Decision letter unclear | Write to the local va'adat tvi'ot, then appeal to Beit Din Ezorit L'Avoda. Take the deadline from the decision letter; quoted windows are unverified |
