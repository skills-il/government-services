# Bituach Leumi reserve-pay rules: basis, supplement, tax and offsets

Companion to SKILL.md Step 3. Everything here concerns the **Bituach Leumi** salary-reimbursement
track only. The three IDF payments (tagmul nosaf, tagmul meyuchad, over-age tagmul) are a different
payer with different rules, and are documented in `2026-law-changes.md`.

## 1. The daily basis, by situation

| Situation | Daily basis |
|-----------|-------------|
| Employee | 3-month gross liable wage / 90, clamped to floor and ceiling |
| Under 60 days worked in those 3 months | Choose 3 of the last 6 months |
| Self-employed | Reported advances (מקדמות) / 90, recomputed on final assessment |
| **Not working, incl. students** | Flat NIS 328.76/day (NIS 9,863/month) |
| **Stopped salaried or self-employed work within 60 days of call-up** | The FORMER employment income, not the floor. Past 60 days, floor only |
| **Discharged from keva within 60 days** | May be paid at the keva salary |
| **On unemployment benefit above NIS 328.76/day** | Tagmul equals the unemployment rate, if still entitled during service |
| 2026 floor / ceiling | NIS 328.76 / NIS 1,730.33 per day (NIS 9,863 / NIS 51,910 per month) |

Source (non-workers, keva and unemployment rows), verbatim:

> סכום התשלום למי שלא עבדו לפני שנקראו למילואים (נכון ל-2026): 328.76 ₪ ליום, 9,863 ₪ לחודש.
> למי שנקראו למילואים בתוך 60 ימים אחרי שהפסיקו לעבוד כשכירים או כעצמאים התשלום יחושב לפי ההכנסה
> שהייתה להם מעבודה. מי שנקראו למילואים בתוך 60 ימים אחרי שהשתחררו מקבע עשויים לקבל תשלום בגובה
> השכר שקיבלו בשירות הקבע. למי שנקראו למילואים בתקופה שקיבלו דמי אבטלה בסכום גבוה יותר מ-328.76 ₪
> ליום, התשלום עבור המילואים יהיה בגובה דמי האבטלה, אם עדיין היו זכאים להם במהלך המילואים.

The keva row is hedged in the source (`עשויים`), so present it as a possibility to check, not an entitlement.

The three 60-day windows are date-sensitive and unrecoverable once missed. Always ask when the person
last worked before assuming the floor applies.

## 2. Multiple employers and mixed income

> את התשלום על השכר שמשלם המעסיק הראשי מקבלים דרך אותו מעסיק. על השכר משאר המעסיקים צריכים להגיש
> תביעה אישית ולצרף תלושי שכר מכל מקומות העבודה (כולל מהמעסיק הראשי).

Employed **and** self-employed: the basis is wage plus self-employment income. If either stream rose
by 20% or more, all work income is recomputed by that rise. The insured's BTL standing must actually
be `שכיר ועצמאי`. If a stream fell below the daily floor, file the personal self-employed claim
AFTER the employer's claim has been paid, to avoid creating a debt.

## 3. The 40% supplement: a remainder rule

BTL divides the service days by 7 and pays the supplement only on the REMAINDER.

| Remainder | Supplement |
|---|---|
| 0 | none |
| 1 | +0.4 day |
| 2 | +0.8 |
| 3 | +1.2 |
| 4 | +1.6 |
| 5 | +2.0 |
| 6 | +1 full day |

Consequences worth stating to a user: **20 days of service pays 21 days**, and **21 days of service
pays exactly 21** (remainder 0, nothing added). Multiplying every day by 1.4 overstates a 21-day
call-up by 40% (11,760 instead of 8,400 at a 400/day rate).

Known source defect: BTL's own worked-examples table has one row (120 to 122) that contradicts the
rule stated three lines above it (120 mod 7 = 1, which the rule pays as 120.4). The stated rule
reproduces 19 of their 20 rows, so the rule is used and the outlier treated as a typo. This decision
is also recorded in the miluim-daily-pay tool manifest.

## 4. Day counting: BTL vs IDF

These are **two different systems** and must not be merged.

| | BTL (payment) | IDF (shamap thresholds) |
|---|---|---|
| Half-day | Counts as **0.5 day** | A call-up FORMAT, not a credit unit. Accounting is in whole days |
| Short service | Paid as served | Every 8 hours (travel included) becomes one day; a partial day is entered as a full day |
| Single-day | Qualifies | Qualifies |

So the same day can be 0.5 for BTL pay and 1 for an IDF grant threshold. A skill that expresses
grant thresholds in shamap days but pay in BTL days must keep the two apart.

Also qualifying for BTL tagmul: training under חוק שירות עבודה בשעת-חירום (מל"ח).

**Not paid by BTL at all:** police, prison-service and Knesset-guard reservists are paid by the
Ministry of Finance.

## 5. Self-employed 25% compensation

An additional 25% on top of the tagmul, but the combined daily total may never exceed the maximum:

> סכום התגמול והפיצוי יחד, לא יעלה על התגמול המקסימלי

State the sequence once, and in this order:

1. Compute the daily basis for the situation (section 1 above).
2. Add the self-employed 25% to that DAILY figure, if applicable.
3. Cap the resulting daily figure at the ceiling (1,730.33), and floor it at 328.76.
4. Multiply by the paid-day count, which is the service days PLUS the remainder supplement from section 3.

The 40% supplement is a DAY COUNT, not a rate, so it never sits inside the daily
clamp. The cap binds the combined daily total of tagmul plus the 25% compensation,
which is what BTL means by `סכום התגמול והפיצוי יחד, לא יעלה על התגמול המקסימלי`.

## 6. Tax, contributions and debt offset

BTL transfers the payment **after deducting income tax**:

> המוסד לביטוח לאומי מעביר את התשלום אחרי שהוא מפחית ממנו מס הכנסה

This is the commonest reason a reservist believes they were short-paid: they reconcile a net deposit
against a gross formula. Contributions then settle by claim route:

| Claim route | Who deducts what |
|---|---|
| Via employer | The EMPLOYER deducts both BL and health contributions |
| Personal claim, working | BTL deducts health ONLY; the reservist must call branch collections to settle BL |
| Personal claim, not working | The reservist must call collections for BOTH BL and health |

**Debt offset is opt-in, not automatic:**

> מתשלום מילואים לא ינוכה חוב לביטוח הלאומי, אלא אם מקבל התשלום מבקש זאת

Never tell a reservist that arrears are blocking their payout and that clearing the debt will release
it. That is the inverse of the published rule and pushes them to settle a debt on a false premise.

Payment is made for the whole service period **including days absent through illness, leave or injury**:

> התשלום ניתן לאורך כל תקופת המילואים, כולל בימים שבהם משרתי המילואים נעדרו מהשירות בגלל מחלה, חופשה או פציעה

## 7. A rejected claim: the deadline that actually matters

The operative remedy against a BTL decision is a filing with the **regional Labour Court within 12
months of the day the decision was delivered**, under regulation 1(b) of תקנות הביטוח הלאומי
(מועדים להגשת תובענות), התש"ל-1969:

> החליט המוסד בתביעה ונמסרה לתובע הודעה על כך, תוגש תובענה לבית הדין לעבודה תוך שניים עשר חודשים
> מיום מסירת ההודעה לתובע

Section 396 of the National Insurance Law is only the enabling provision (`שר המשפטים... רשאי לקבוע
הוראות בדבר מועדים`) and sets no period. Do not cite it as the source of the 12 months.

**The 6-month figure is a different thing.** It is the window for asking **ועדת תביעות** to
re-examine a rejection. That committee `אינה מוסמכת לשנות את החלטתו של פקיד התביעות, אלא רק להמליץ
לו לשקול אותה מחדש`, and crucially it does **not** pause the court clock:

> הפנייה לוועדת התביעות לא דוחה את המועד הקבוע בחוק להגשת ערעור לבית הדין לעבודה

Stating only the 6 months, attached to the wrong body, tells a reservist at month 8 they are
time-barred when 4 months of remedy remain.

Related: regulation 1(a) allows a filing at the earliest **30 days** after the claim went to BTL if
BTL has not decided, which is the answer to "BTL has gone silent". An employer may file on an
employee's behalf within 12 months (regulation 2). Free Ministry of Justice legal aid is available
for the appeal with **no means test**, and section 397 of the National Insurance Law provides for
legal aid in Labour Court proceedings to which the Institute is a party. Second instance: 30 days to
בית הדין הארצי.
