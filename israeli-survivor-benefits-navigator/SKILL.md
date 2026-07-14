---
name: israeli-survivor-benefits-navigator
description: "Ties together every benefit a death triggers in Israel: assesses who is eligible for the Bituach Leumi survivor's allowance, estimates the monthly amount from the current rate table, and maps each benefit to its exact form and institution. Use when someone died and the family needs to know what to claim from Bituach Leumi, the pension fund, and insurance. Do NOT use for burial logistics, closing accounts, or asset transfer (estate settlement), for writing a will or getting a succession order, or for general non-death Bituach Leumi questions."
license: MIT
---

# Israeli Survivor Benefits Navigator

## Problem

When someone dies in Israel, the family is usually entitled to several payments at once, but almost none of them arrive automatically. The survivor's allowance from Bituach Leumi, the survivor's pension from the deceased's pension fund, and life-insurance or provident-fund payouts each have a different form, a different institution, and a different deadline, and many families never claim money they are owed. This skill maps the whole maze: it checks who is eligible, estimates the monthly survivor's allowance from the current rate table, and lists the exact forms to file with each institution.

## Instructions

You produce three deliverables: (1) an eligibility report, (2) an estimated monthly survivor's-allowance amount, and (3) a filing checklist mapping each benefit to its form and institution. All figures below are effective 01.01.2026 and are re-indexed every January, so verify the current-year amount at btl.gov.il before quoting it. Never invent a figure.

### Step 1: Establish the facts you need

Ask for: who died and their relationship to the survivor; whether the survivor is a widow or widower and their age; the number and ages of children; whether the death was work-related (a work accident or occupational disease); whether the deceased had a pension fund, provident fund (kupat gemel), or life-insurance policy; and whether the survivor already receives an old-age (vatik) pension.

### Step 2: Who is a "she'er" (eligibility)

The Bituach Leumi survivor's allowance requires ALL of: the deceased was insured for survivors' insurance at death, completed a qualifying (akhshara) period, the claimant is counted among the deceased's she'erim, and there are no insurance-contribution arrears.

**Who counts as a widow/widower.** A widow or widower is a spouse who was either MARRIED to the deceased OR a common-law partner (ידוע/ה בציבור, including a same-sex partner) who lived with the deceased under one roof, and who meets one of these: they were married or cohabiting for at least 1 year before the death; OR at least 6 months if she/he was 55 or older when the deceased died; OR they had a shared child with the deceased (a shared child waives the duration requirement).

- A **widow** is entitled by law, with no income test.
- A **widower without dependent children** is subject to an income test: entitled if total income is up to 7,848 NIS, after deducting 2,093 NIS from income from work, pension, or a monthly income first paid at retirement age.
- **Orphans (child cutoffs):** a child up to age 18; up to age 20 if completing secondary school or in a pre-military mechina; up to age 21 while doing national or community service (sherut leumi). These cutoffs drive the child increment in the allowance.

**Qualifying (akhshara) period.** The deceased must have accrued one of: 12 insurance months in the year immediately before death; OR 24 insurance months (consecutive or not) in the 5 years before death; OR 60 insurance months in the 10 years before death; OR 144 insurance months in total; OR the resident-ratio route (60 insurance months since first becoming an Israeli resident, provided the uninsured months do not exceed the insured months). No akhshara is required at all when the deceased was an insured worker and died within a year of becoming a resident, died before age 19, was the primary breadwinner, or (for a woman) died within a year of divorce or widowhood.

**File within 12 months.** The survivor's-allowance claim should be filed no later than 12 months from the date of death. If it is filed later, the allowance can be paid retroactively only for a period of up to 12 months, so late filing forfeits earlier back-payment. Do not let a family delay the claim.

### Step 3: Estimate the survivor's allowance (ordinary track)

Use the current rate table. The amount is set by the widow(er)'s age and the number of children with them:

| Category | Monthly base (NIS) |
|---|---|
| Widow(er) aged 40-50, no children | 1,381 |
| Widow(er) aged 50+, no children | 1,838 |
| Widow(er) aged 80+ | 1,941 |
| Widow(er) with one child | 2,700 |
| Widow(er) with two children | 3,562 |
| Each additional child (beyond two) | +862 |
| Half the childless-50+ allowance (old-age-pension interaction, see below) | 919 |

Per-orphan bases in special cases (parent not entitled: 1,142 for a single child, 862 each when more than one; orphan of both parents: 2,284 per child). There is no cap on the number of eligible children.

**Orphan subsistence allowance (dmei michya, דמי מחיה) -- a SEPARATE monthly payment on top of the allowance, and the one families most often miss.** It is paid for an orphan who is studying, from 9th grade (after 8 years of compulsory schooling) until age 20, at least 24 weekly hours in a school, university, college, vocational institution, or yeshiva gvoha, and whose upkeep is not at state expense. The amount depends on whether the parent draws the survivor's allowance:

| Situation | Monthly dmei michya (NIS) |
|---|---|
| The family IS paid a survivor's allowance (with the child increment) | 683 |
| The family is NOT paid a survivor's allowance | 946 |

An orphan of both parents drawing two survivors' allowances gets dmei michya TWICE. Payment is income-tested on the parent's and the orphan's income: the ceiling for full dmei michya for a parent with one qualifying orphan is 15,697 NIS gross a month, plus 964 for each additional child. Claim on form 2910. A widow(er) can claim dmei michya for a child even when no child increment is paid for that child.

**Old-age (vatik) pension interaction.** A widow(er) who is entitled to both an old-age pension and a survivor's allowance is paid the old-age pension **in full PLUS half of the survivor's allowance** (if they accrued the old-age qualifying period as an insured worker). The 919 figure is specifically half of the childless-50+ base (half of 1,838). A widow(er) WITH children is paid half of the higher with-children rate, so 919 is NOT a universal half-allowance figure. A widowed homemaker who reached the absolute pension age is not paid the extra half and instead chooses the higher of the two allowances.

Then add the **seniority increment (tosefet vetek)**: 2% of the base per full insurance year the deceased accrued (from the first year), up to a maximum of 50%. A full insurance year is 12 insurance months.

A widow(er) **under 40 with no children** usually gets a one-time **survivor grant** (36 monthly allowances) rather than a monthly allowance. This is not absolute. The under-40 childless survivor still gets a **monthly** allowance if she/he is pregnant with, or later bears, the deceased's child (a shared child means she/he is treated as a widow(er) with a child, entitled from the date of death), and, in the work-related-death (dependents') track, if she was unable to support herself from work at the time of the death (she is then paid a monthly allowance regardless of her age, as if she were 50). So do not flatly rule out a monthly amount here: present the grant as the usual outcome, note these exception paths, and point to Bituach Leumi for the determination.

Run `scripts/estimate_survivor_allowance.py --age <age> --orphans <n> --seniority-years <y>` to produce the estimate (add `--exception-eligible` for the under-40 childless case when an exception above applies). Present it clearly as an estimate only.

### Step 4: Work-related death branch (dependents' allowance)

If the death resulted from a work accident or occupational disease, the family claims the **dependents' allowance (kitzvat tluyim)** instead of the survivor's allowance. It is higher, has no income test, and you cannot receive both for the same death. It is a percentage of a full (100%) work-disability pension, which is 75% of the deceased's wage in the three months before the injury (capped so the full pension does not exceed 39,428 NIS):

| Family | Rate of full work-disability pension |
|---|---|
| Widow(er) + 1 child | 80% |
| Widow(er) + 2 children | 90% |
| Widow(er) + 3 or more children | 100% |
| Widow(er) 40-50, no children | 40% |
| Widow(er) 50+, no children | 60% |
| Widow under 40, no children | one-time grant of 60% x 36 |

Run the estimator with `--work-related --wage <deceased monthly gross wage>`.

### Step 5: One-time grants and burial

- **Death grant (menak petira)**: one-time 10,514 NIS to the spouse of a deceased who received old-age, income-support, general-disability, special-services, work-injury, survivors, or prisoners-of-Zion benefits (to the child if no spouse). Usually automatic; the survivor's-allowance claim (form 410) already includes it.
- **Survivor grant (menak she'erim)**: one-time = 36 monthly allowances, for a widow(er) under 40 with no children (and certain income cases).
- **Marriage grant (menak nisuim) on remarriage**: remarriage (or entering a new common-law relationship) TERMINATES the survivor's allowance. In exchange the widow(er) receives a one-time marriage grant equal to 36 monthly allowances, paid in two installments: 18 monthly allowances after the marriage, and the remaining 18 about two years later. The allowance can instead be CONTINUED if the new spouse is 60 or older or cannot support himself and his income is below the ceiling (7,848 NIS), and it is REINSTATED if the widow(er) divorces (or starts divorce proceedings) within 10 years of remarrying. Report a remarriage on form 408.
- **Burial fees (dmei kvura)**: Bituach Leumi pays burial costs and customary services directly to the Chevra Kadisha, so basic burial is free to the family.

### Step 6: Pension fund and insurance (separate from Bituach Leumi)

- **Pension-fund survivor's pension (pensiyat she'erim)**: claim directly from the deceased's pension fund. Typically about 60% of the deceased's salary/pension to the spouse for life and about 40% to orphans until 21 in a new comprehensive fund, but the exact rates and eligible survivors are set by the fund's takanon, so verify with the fund. Use "הר הביטוח" (Har HaBituach, run by the Capital Market Authority, at https://harb.cma.gov.il/) to locate all of the deceased's insurance policies and pension products, and "הר הכסף" (Har HaKesef, at https://itur.mof.gov.il/) to trace lost or dormant pension savings, life-insurance policies, and bank accounts.
- **Provident fund / life insurance (kupat gemel, keren hishtalmut, bituach chayim)**: claim directly from the manager/insurer. Under section 147 of the Inheritance Law these sums are outside the estate and go to the registered beneficiaries (motavim) in the policy, overriding the will. If no beneficiary is registered, the money falls into the estate and needs a succession/probate order.

### Step 7: Build the filing checklist

Map each applicable benefit to its form and institution (see `references/forms-and-filing.md`): survivor's allowance → form 410 (Bituach Leumi, also covers the death grant); special survivors' allowance → 4506; orphan living allowance → 2910; income supplement → 430; dependents' allowance (work-related) → 213; pension → the pension fund; gemel/insurance → the manager/insurer.

For any complex case (contested eligibility, work-injury proof, large estates, disputed beneficiaries), recommend consulting a pension advisor or a lawyer. State the facts, but do not tell the user they can skip professional advice.

## Bundled Resources

- `references/survivor-allowance-rates.md`: the full current-year rate table with source URLs and the 01.01.2026 effective date.
- `references/forms-and-filing.md`: each benefit mapped to its Bituach Leumi form number and institution.
- `references/domain-checklist.md`: the Must/Should/Out-of-scope coverage contract for this domain.
- `scripts/estimate_survivor_allowance.py`: estimates the monthly amount from the encoded rate table (`--help`, `--example`).
- `evidence.json`: every figure and claim with its verbatim official-source snippet.

## Recommended MCP Servers

| MCP Server | Slug | Why |
|---|---|---|
| Kol-Zchut (All Rights) | `kolzchut` | Look up plain-language survivors' rights pages (widow/orphan definitions, related benefits) to cross-check eligibility. |

## Reference Links

- Bituach Leumi survivors section (index): https://www.btl.gov.il/benefits/Survivors_%20Insurance/Pages/default.aspx
- Survivor's allowance amounts (widow/widower): https://www.btl.gov.il/benefits/Survivors_%20Insurance/shiuraihakizba/Pages/k.almanim.aspx
- Dependents' allowance (work-related death) rates: https://www.btl.gov.il/benefits/Work_Injury/זכויות%20בני%20משפחה%20של%20נפטר%20מפגיעה%20בעבודה/Pages/שיעורי%20הגמלה.aspx
- Bituach Leumi survivor's-allowance eligibility check: https://www.btl.gov.il/Simulators/Pages/SherimCalc.aspx
- Kol-Zchut survivor's allowance: https://www.kolzchut.org.il/he/קצבת_שאירים
- Har HaBituach (insurance + pension locator, Capital Market Authority): https://harb.cma.gov.il/
- Har HaKesef (lost pension savings, life-insurance policies, and bank accounts, Finance Ministry): https://itur.mof.gov.il/
- Section 147 of the Inheritance Law (beneficiaries vs the estate): https://he.wikisource.org/wiki/חוק_הירושה

## Gotchas

- Do not confuse the **survivor's allowance (קצבת שאירים)** with the **dependents' allowance (קצבת תלויים)**. The dependents' allowance is the work-related-death track only, it is higher, it has no income test, and you cannot receive both for the same death.
- Benefits do not start automatically (with narrow exceptions like the death grant and burial fees). Almost everything requires an active claim, on a specific form, to a specific institution.
- Never use one flat allowance figure. The amount depends on the widow(er)'s age band AND the number of children AND the seniority increment; use the full table.
- For a provident fund, pension fund, or life-insurance policy, the **registered beneficiary designation overrides the will** (section 147). Do not assume the money follows the will or the heirs.
- A widow(er) already drawing an old-age (vatik) pension is paid the old-age pension IN FULL PLUS half of the survivor's allowance (not "half instead of both"). The 919 NIS figure is only half of the childless-50+ base; a widow(er) with children gets half of the higher with-children rate. A widowed homemaker at absolute pension age instead picks the higher of the two. Check the applicable base before estimating.
- Remarriage (or a new common-law relationship) ends the survivor's allowance and triggers a one-time marriage grant of 36 monthly allowances (paid 18 + 18, the second part about two years later). The allowance continues if the new spouse is 60+ or cannot support himself with income below the ceiling, and is reinstated on divorce within 10 years of remarrying.
- File the survivor's-allowance claim within 12 months of the death. Later filing limits back-payment to the last 12 months.

## Troubleshooting

- If a current-year amount cannot be confirmed on btl.gov.il, present the eligibility and forms but omit the number and point the user to the official calculator; never guess a figure.
- If the user asks about burial logistics, death certificates, closing bank accounts, notifying institutions, or transferring assets, route them to `israeli-estate-settlement-navigator`.
- If the user asks how to write a will or obtain a succession (ירושה) or probate (קיום צוואה) order, route them to `israeli-wills-inheritance`.
- If the question is about general, non-death Bituach Leumi navigation, route to `israeli-bituach-leumi`; for pension planning while alive, route to `israeli-pension-advisor`.
- For contested eligibility, work-injury proof, or disputed beneficiaries, recommend a pension advisor or lawyer.
