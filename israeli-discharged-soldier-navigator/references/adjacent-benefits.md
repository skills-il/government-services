# Adjacent discharged-soldier benefits, verified detail

Everything here is delivered by a body OTHER than the MoD Department and Fund for Discharged
Soldiers, so it sits outside the Pikadon / grant / Mimadim core of this skill. The skill's Step
8.5 table carries the one-line version and routes; this file carries the conditions that decide
whether the user actually gets the money. Verified 2026-08-27 against Kol Zchut.

## The routing table (moved out of SKILL.md Step 8.5, 2026-08-27)

| Benefit | Who delivers it | Route, and the condition that most often kills it |
|---|---|---|
| מענק עבודה נדרשת, **11,461 NIS (2026)** for 6 full months in a defined sector within 24 months of discharge. Largest non-Pikadon cash benefit, and taxable | Bituach Leumi (Tofes 1521) | `israeli-bituach-leumi`. Claim within **42 months** of discharge |
| Dmei avtala, max 70 days where the unemployment period starts in year 1 | Bituach Leumi | `israeli-unemployment-benefits-navigator` |
| Arnona exemption, up to 4 months | Local authority | Not automatic, and **not available while living in a parent's home** |
| 2-month BL + health-contribution exemption | Bituach Leumi, automatic | Only while not working, non-work income at or below 688 NIS/month (2026) |
| Free public transport, 1 year | Rav-Kav / transit operator | **Load the "discharged" Rav-Kav profile within 60 days of discharge** or it is lost |
| תוספת משכנתא, +1% of entitlement per service month, joint cap 46% single / 65% couple | Ministry of Housing | `israeli-mortgage-comparator` |
| פיקדון 2000, dormant balances (service ended after 01.01.1995 or began before 31.12.2000) | Department and Fund | Check the personal area, then email the Fund |
| Free legal aid on discharged-soldier rights | Ministry of Justice | Use on a refused re-employment or a disputed denial |
| "Bahatzda" benefits card | Independent | hachvana.mod.gov.il |
| Service data wrong (Pikadon or grant does not match service type or length) | IDF soldiers: the IDF "שער לעתיד" directorate, WhatsApp 03-7374789 or atid@digital.idf.il (hachvana, 2026-10-18). SLE completers: the National-Civic Service Authority, or the Department on *5266 | The Department cannot reclassify service. Until v1.5.0 this row said 1111 ext 5, which Kol Zchut still prints; hachvana now names שער לעתיד. |
| Pikadon inheritance | Department and Fund | Heirs are eligible where the soldier died **during service OR after discharge** ("שנפטרו בתקופת השירות או לאחר השחרור"). The heirs apply to the Department and Fund. (An earlier version routed a death in service to Mador Mishpachot Shakulot; no source supports that, so it was removed on 2026-10-18.) |


## Menak Avoda Nidreshet (מענק עבודה נדרשת, formerly "avoda mueddefet")

Paid by Bituach Leumi on Tofes 1521.

| Rule | Detail |
|---|---|
| Amount | 11,461 NIS in 2026 for the full 6 months |
| Qualifying work | Agriculture, construction, industry and crafts, petrol stations, hotels, care of people with disabilities. Clerical roles are excluded even inside a qualifying employer |
| Period | At least 6 full months, consecutive or not, within 24 months of discharge, full-time, at least 150 working days |
| Partial grant | 7,641 NIS in 2026 for at least 4 months in agriculture (100 working days), or for work found unsuitable before 6 months |
| Started late | Someone whose first qualifying work begins more than 12 months after discharge must ALSO be eligible for unemployment benefit on the day they start |
| Offset | Unemployment benefit drawn in the 11 months before the qualifying work is deducted from the grant |
| Claim deadline | 42 months from discharge, and only after completing the minimum work period |
| Tax | The grant is taxable and Bituach Leumi does not withhold. Budget for it |
| Reserve duty | Reserve-duty days extend the 24-month window |
| SLE | Available to those who completed 24 months of national or national-civic service |

## Dmei Avtala (unemployment benefit)

- 70 days maximum where the unemployment period begins in the first year after discharge.
- 138 days for someone without 12 years of schooling who is in approved vocational training.
- Minimum daily rate 141.48 NIS in 2026.
- Up to 6 months of service count toward the qualifying employment period.
- A discharge for "i-hatama" (אי-התאמה) disqualifies.

## Arnona exemption

Up to 4 months from discharge from compulsory service. 100% on 70 m2, or 90 m2 where 5 or more
people live in the dwelling.

**Two conditions that disqualify most applicants and that the skill must state up front:** it is
NOT automatic (apply to the municipal arnona collection department on a discount-request form),
and the discharged soldier must live in a dwelling they own or rent. Living in a parent's home
does not qualify, which is the situation most 21-year-olds are actually in.

There is a route for that case, and it is worth surfacing rather than stopping at "not
entitled": the PARENTS may be exempt if they show the municipality that the soldier supported
them before service and that they cannot support themselves during the soldier's entitlement
period. Where a discharged soldier shares a rental with flatmates who are not entitled, the
municipality decides how the exemption is apportioned, so check locally. Some municipalities
grant the discount retroactively.

Source: https://www.kolzchut.org.il/he/פטור_מארנונה_לחיילים_בשירות_חובה_וחיילים_משוחררים

## Two-month BL and health-insurance exemption

Exempt from national-insurance and health-insurance contributions for the two months following
the month of discharge. Applied automatically, but only where the person is not working as an
employee or self-employed, has non-work income of no more than 688 NIS a month (2026), and
served at least two thirds of the required service. Keva discharges are excluded.

## Free public transport

One year, but the clock and the trap are both in the fine print: the entitlement runs for a year
from discharge or from the day the "discharged" profile is loaded onto the Rav-Kav card or the
app, whichever is LATER, **and the profile must be loaded within 60 days of discharge**. Miss the
60 days and the benefit is lost outright. Loading the profile needs a copy of the discharge
certificate and an ID or driving licence, and approval takes up to 5 business days, so a user at
day 55 should be told to do it today. Legal basis: צו פיקוח על מחירי מצרכים ושירותים (מחירי
נסיעה בקווי שירות באוטובוסים ומחירי נסיעה ברכבת מקומית), תשפ"ב-2022, section 7(a)(13).

Source: https://www.kolzchut.org.il/he/פטור_מתשלום_על_נסיעה_בתחבורה_ציבורית_לחיילים_משוחררים_ומסיימי_שירות_לאומי-אזרחי

## Mortgage supplement (תוספת משכנתא)

+1% of the basic Ministry of Housing mortgage entitlement per full month of compulsory or
national-civic service (civic service capped at 12 months' worth). It stacks with the active-
reservist supplement, and the two together cannot exceed 46% for a single person or 65% for a
couple who both qualify. Requires a Ministry of Housing eligibility certificate. Route the
mortgage itself to `israeli-mortgage-comparator`.

## Pikadon 2000 (dormant balances)

Someone who ended service after 01.01.1995, or began service before 31.12.2000, may still have
an unused Pikadon balance. Check the personal area, then email the Fund to release it.

## Free Ministry of Justice legal aid

Free legal aid is available specifically on discharged-soldier rights. The natural triggers are
an employer refusing re-employment under the return-to-work statute and a benefit denied on a
ground the user disputes.

## Return to the pre-draft employer (moved from SKILL.md Step 8.6, 2026-10-18)

**Chok Chayalim Meshuchrarim (Hachzara LaAvoda), 5709-1949** gives a discharged soldier the right to go back to their pre-conscription employer. It carries the shortest deadline in the domain and is routinely missed, because it runs from the discharge date and not from when the user starts job-hunting.

It applies to a "permanent employee" there, or someone who worked **6 continuous months** before conscription, and who did **not** take severance on leaving. Service counts as accrued seniority, and the employer must re-employ them for **6 months** on the same job and terms, or the best available if that is impossible.

**The deadline is a written request between 15 days before discharge and 30 days after.** Miss that 45-day window and the right lapses. Name a start date within 30 days of the request and copy the employment bureau and the workers' committee. A workers' organisation may file it on the soldier's behalf.

A refusal on the named date is not the end: where the employer cannot take them that day they may be taken on "בתוך שנה מהיום שהגיש את הבקשה, במועד האפשרי המוקדם ביותר". On a refusal, the statute's forum is a **ועדת תעסוקה**: s.21 lets anyone who claims their rights under the law were breached apply to one, and s.23 allows an appeal to the regional labour court within 20 days. Kol Zchut also points to free Ministry of Justice legal aid. (Checked against the statute on nevo, https://www.nevo.co.il/law_html/law01/150_001.htm, on 2026-10-18. The employer burden-of-proof claim was removed because no source supported it.) Someone who resigned on conscription after 12 months there gets severance instead, and taking it ends this right.

Source: https://www.kolzchut.org.il/he/חזרה_לעבודה_של_חייל_משוחרר ("ניתן להגיש את הבקשה בתקופה שבין 15 יום לפני מועד שחרורו של החייל מצה"ל ועד 30 יום לאחר מועד השחרור"). Re-checked 2026-10-18, no change.
