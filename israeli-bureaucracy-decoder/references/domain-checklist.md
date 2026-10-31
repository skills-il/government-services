# Domain checklist: israeli-bureaucracy-decoder (government-services)

Drafted 2026-10-29. Scope: decode an Israeli government letter into who sent it, what it says, what action is required and by when, plus the correct appeal venue and window. The skill computes no amounts. Its core risk is a wrong deadline, a wrong venue or a wrong form number, so every row below names its source.

Verification legend: [V] = statute or official page text read on 2026-10-29 (statute text on he.wikisource.org, btl.gov.il, gov.il). [M] = verified in an earlier cycle by browser render (kolzchut, gov.il). [U] = unverified on a primary source; the skill must not state it as fact until checked.

Cross-cutting rule for every row: the clock runs from the trigger the statute names (service / המצאה, receipt / קבלה / נמסרה, publication, or knowledge, whichever the text says), never from the date printed on the letter. Where a statute says "whichever is earliest" (e.g. Entry into Israel Law s.13כד(ב), administrative courts reg. 3(ב)), the skill must say so.

## Must cover (core)

### 1. Execution Office (לשכת ההוצאה לפועל)

| # | Letter / trigger | Window and action | Venue | Source |
|---|---|---|---|---|
| 1.1 | אזהרה in a **judgment** file (פסק דין) | 20 days from service to comply, or pay by instalments under a payment order, or request a payment order. No התנגדות route against a judgment. | Execution Office (registrar) | חוק ההוצאה לפועל s.7(א) [V] |
| 1.2 | אזהרה in a **bill / cheque** file (שטר) | התנגדות within 30 days of service of the אזהרה: filing stays execution and moves the case to court | Court with jurisdiction, filed through the Execution Office | חוק ההוצאה לפועל s.81א(ג), (ג1) [V] |
| 1.3 | אזהרה in a **fixed-sum claim** file (תביעה על סכום קצוב, up to 75,000 NIS on filing) | התנגדות within 30 days of service, with an affidavit; stays execution, case moves to court. | Court, via the Execution Office | חוק ההוצאה לפועל s.81א1(א), (ד)(1)-(2), (ה)(1) [V] |
| 1.4 | Every other Execution Office letter (payment order, ability examination, restrictions, registrar decisions, mortgage realisation) | Name the file type and the letter, then route to the `israeli-hotzaa-lapoal-debtor` skill for the procedure | Execution Office | delegated |

### 2. Tax Authority (רשות המסים)

| # | Letter / trigger | Window and action | Venue | Source |
|---|---|---|---|---|
| 2.1 | Income tax assessment (שומה לפי מיטב השפיטה) | השגה in writing with exact reasons, within 30 days of service of the assessment notice | פקיד השומה | פקודת מס הכנסה s.150(א) [V] |
| 2.2 | Income tax order / decision on השגה (צו לפי s.152(ב)) | Appeal within 30 days of delivery of the order | בית המשפט המחוזי | פקודת מס הכנסה s.153 [V]; תקנות בית משפט (ערעורים בעניני מס הכנסה) reg. 2 [V] |
| 2.3 | Deficit fine (קנס גירעון, s.191) | Treated as an assessment, so the s.150 30-day השגה applies | פקיד השומה | פקודת מס הכנסה s.191 with ss.149-152 [V] |
| 2.4 | Late-filing fine (s.188) | No statutory השגה route found. Do NOT state a 30-day appeal window. Route is a cancellation / relief request at the officer's discretion. | פקיד השומה | פקודת מס הכנסה s.188 [V]; discretion route [U] |
| 2.5 | VAT assessment (שומה) | השגה in writing with reasons within 30 days of service, or a later date the director allowed. No decision within one year means the השגה is accepted. Appeal from the director\'s decision to the District Court (s.83). | מנהל מע"מ | חוק מס ערך מוסף ss.76(ב), 81א, 82(א), 82(ד) [V] |
| 2.8 | Real-estate tax assessment (מיסוי מקרקעין: שבח / רכישה) | השגה within 30 days of delivery of the assessment notice | מנהל מיסוי מקרקעין | חוק מיסוי מקרקעין s.87(א) [V] |
| 2.9 | Real-estate tax decision on השגה | ערר within 30 days of delivery | ועדת ערר | חוק מיסוי מקרקעין s.88 [V] |
| 2.10 | Form-number recognition on Tax Authority letters | 101, 106, 116, 119, 135 (short return, refund up to 6 years), 1301, 1214 (companies), 7000 (real-estate declaration within 30 days), 821 (VAT file opening). Never call 135 the self-employed return or 1214 an employee refund. | n/a | gov.il ITA service pages [V]; ITO s.160; חוק מיסוי מקרקעין s.73(א) [V] |

### 3. Bituach Leumi (המוסד לביטוח לאומי)

| # | Letter / trigger | Window and action | Venue | Source |
|---|---|---|---|---|
| 3.1 | Rejection of a benefit claim (דחיית תביעה) | Claim to the regional labour court within 12 months of receiving the decision. Exception: מזונות decisions, 6 months. | בית הדין האזורי לעבודה | btl.gov.il appeals page [V] |
| 3.2 | Medical committee decision, **general disability** (נכות כללית) | ערר in writing with reasons within 60 days of written notice; only if under 80% medical disability. | ועדה רפואית לעררים | btl.gov.il erurNechut [V] |
| 3.3 | Medical committee decision, **work injury** (נפגעי עבודה) | ערר within 30 days of written notice; reasons may follow within 60 days. Do NOT reuse the 60-day general-disability figure. | ועדה רפואית לעררים | btl.gov.il erurNechutMeavoda [V] |
| 3.4 | Decision of a medical appeals committee (both tracks) | Appeal on a question of law only, within 60 days of notice | בית הדין האזורי לעבודה | btl.gov.il erurNechut / erurNechutMeavoda [V] |
| 3.5 | BTL form numbers on letters | 7801 general disability claim, 211 work-injury claim (12 months from injury), 1500 unemployment (12 months from first Employment Service report), 355 / 360 maternity, 5025 child allowance, 480 old age, 502 reserve duty (non-salaried), 580 hostile action | n/a | btl.gov.il forms index [V] |

### 4. Municipality: arnona and municipal fines (רשות מקומית)

| # | Letter / trigger | Window and action | Venue | Source |
|---|---|---|---|---|
| 4.1 | Arnona payment notice (הודעת תשלום / שומה) on grounds in s.3 (area, classification, use, not the holder) | השגה within 90 days of receiving the payment notice | מנהל הארנונה | חוק הרשויות המקומיות (ערר על קביעת ארנונה כללית) s.3(א) [V] |
| 4.2 | No answer from מנהל הארנונה | Must answer within 60 days; silence = השגה accepted, unless the appeals committee extended by up to 30 days | n/a | same law s.4 [V] |
| 4.3 | Answer of מנהל הארנונה | ערר within 30 days of delivery of the answer | ועדת ערר לענייני ארנונה | same law s.6(א) [V] |
| 4.4 | Decision of the arnona appeals committee | ערעור מינהלי within 60 days (no other deadline set) | בית משפט לעניינים מינהליים | same law s.6(ב) [V]; תקנות בתי משפט לעניינים מינהליים (סדרי דין) reg. 23(ב) [V] |
| 4.5 | Fine notice (הודעת תשלום קנס: parking, municipal by-law, police traffic ticket) | Pay within 90 days of service, OR request cancellation from the prosecutor within **30 days**, OR give notice of wish to be tried within 90 days. | Prosecutor (תובע), or the court if the user asks to be tried | חוק סדר הדין הפלילי s.229(א) [V] |

### 5. Interior Ministry / PIBA (רשות האוכלוסין וההגירה)

| # | Letter / trigger | Window and action | Venue | Source |
|---|---|---|---|---|
| 5.1 | Refusal of a visa, status or entry decision that the Entry into Israel Law sends to the Appeals Tribunal | ערר within 30 days of publication, notice or knowledge, whichever is earliest | בית הדין לעררים (Appeals Tribunal) | חוק הכניסה לישראל s.13כד(ב) [V] |
| 5.2 | Final Appeals Tribunal decision | Appeal as of right within 45 days | בית משפט לעניינים מינהליים | חוק הכניסה לישראל s.13לא(א) [V] |
| 5.3 | PIBA decision outside the Appeals Tribunal route (e.g. population registry) | Administrative petition within 45 days of publication, notice or knowledge, whichever is earliest, unless another law sets a deadline | בית משפט לעניינים מינהליים | תקנות בתי משפט לעניינים מינהליים (סדרי דין) reg. 3(ב) [V] |
| 5.4 | Identify the sender correctly | PIBA is a unit of the Interior Ministry and runs passports, ID cards and the population registry | n/a | gov.il population_and_immigration_authority [V] |

### 6. Land Registry (לשכת רישום המקרקעין / טאבו) and condominium superintendent

| # | Letter / trigger | Window and action | Venue | Source |
|---|---|---|---|---|
| 6.1 | Decision of a registrar (רשם) or superintendent (מפקח) on a registration matter | ערר within **15 days** of delivery (or of knowledge if not delivered). | הממונה על המרשם | חוק המקרקעין s.121 [V]; תקנות המקרקעין (ניהול ורישום) reg. 74 [V] |
| 6.2 | Decision of הממונה על המרשם (including on a ערר) | Appeal within **15 days** | בית המשפט המחוזי where the land lies | חוק המקרקעין s.122 [V]; תקנות המקרקעין (ניהול ורישום) reg. 76(א) [V] |

### 7. Courts (summons, claims, judgments)

| # | Letter / trigger | Window and action | Venue | Source |
|---|---|---|---|---|
| 7.1 | Small-claims summons (תביעה קטנה) | כתב הגנה within 30 days of service of the summons | בית משפט לתביעות קטנות | תקנות שיפוט בתביעות קטנות (סדרי דין) reg. 4(ב) [V] |
| 7.2 | Small-claims judgment | Leave to appeal within 15 days of the judgment; **30 days** for proceedings opened on or after 11.4.2025. Ask the user when the claim was opened. | בית המשפט המחוזי | same regulations reg. 16(א) [V] |
| 7.3 | Civil statement of claim (Magistrate / District) | כתב הגנה within 60 days of service | Court that issued it | תקנות סדר הדין האזרחי, התשע"ט-2018 reg. 9(ב) [V] |
| 7.4 | Civil judgment or decision | Appeal within 60 days of service (not 45) | Next instance | same regulations reg. 137(א) [V] |
| 7.5 | Administrative decision with no statutory appeal route | Petition within 45 days (publication / notice / knowledge, earliest); extendable by the court | בית משפט לעניינים מינהליים | תקנות בתי משפט לעניינים מינהליים reg. 3(ב)-(ג) [V] |

### 8. Planning and building committees (ועדה מקומית / מחוזית)

| # | Letter / trigger | Window and action | Venue | Source |
|---|---|---|---|---|
| 8.1 | Refusal or rejection of a building permit application | ערר within 30 days of service of the refusal | ועדת ערר (district) | חוק התכנון והבניה s.152(א)(1) [V] |
| 8.2 | Notice of a deposited plan (הודעה על הפקדת תכנית) | התנגדות within **two months** of publication (not "60 days"); the planning body may extend to three months | Planning body that deposited the plan | same law ss.100, 102 [V] |
| 8.3 | Notice of a request for הקלה, שימוש חורג or subdivision deviation | התנגדות within 15 days of publication, or of personal delivery for those served | ועדה מקומית | same law s.149(א)(1) [V] |
| 8.5 | Betterment levy assessment (שומת היטל השבחה) | ערר within 45 days of the assessment coming to the payer's knowledge | ועדת ערר לפיצויים ולהיטל השבחה | חוק התכנון והבניה, Third Schedule [V] |
| 8.4 | Administrative demolition order (צו הריסה מינהלי) | Request to cancel within 15 days of service; filing does NOT stay the order. Venue depends on the issuer: Magistrate Court for national unit / district chair / district planner; בית המשפט לעניינים מקומיים for local committee chair or engineer. | as stated | same law ss.228(א)-(ג), 229 [V] |

## Should cover (advanced)

| # | Item | Why it matters | Source |
|---|---|---|---|
| S1 | Tax collection warrant (פקודת המסים (גביה)) used by tax and arnona collectors: seizure of movables without court order once the debt is 15 days past due and a written demand was sent | Letters titled "דרישה" or "התראה לפני עיקול" from municipalities or the Tax Authority; the user needs to know a seizure can follow without a court | פקודת המסים (גביה) ss.4-5 [V]; contest route [U] |
| S2 | Execution Office debt above / below the insolvency forum threshold (an index-linked threshold set under the Insolvency and Economic Rehabilitation Law; check the current figure) | A heavy-debt letter should route to the right insolvency forum | [M] |
| S3 | Fixed-sum and bill objection vs judgment file: detect the file type from the אזהרה wording before giving any window | This is the most common wrong-deadline failure (applying 30 days to a judgment file or 20 days to a bill file) | חוק ההוצאה לפועל ss.7(א), 81א(ג1), 81א1(ה)(1) [V] |
| S4 | Income tax s.147 review by the Director within one year after the assessment and objection periods | Taxpayers who missed the 30-day השגה ask what is left | פקודת מס הכנסה s.147 [V] |
| S5 | Tax refund window: 6 years (e.g. in 2026, years 2020-2025) on Form 135 | Letters inviting a refund claim | ITO s.160; gov.il itc135 [V] |
| S6 | Annual return deadlines for tax year 2025: 29.5.2026 paper, 30.6.2026 online, 31.7.2026 companies | Reminder letters from פקיד השומה | gov.il annual report 2025 page [V] |
| S7 | Freedom of Information response clock when the user wants their own file: 30 days, +30, +60 reasoned, 120 max | Useful when a letter cites a decision the user never received | חוק חופש המידע s.7(ב)-(ג) [V] |
| S8 | What comes after a first appeal (further appeal usually needs leave) | Users ask "what next" after losing the first appeal | [U] |
| S9 | Real-estate declaration (Form 7000) 30 days from the sale | Letters from מיסוי מקרקעין about a late declaration | חוק מיסוי מקרקעין s.73(א) [V] |
| S10 | Extensions: which windows can be extended and by whom (VAT s.82(א) director; Land Registry ממונה reg. 74(ב); administrative courts reg. 3(ג)) | Users who are already late need to know whether any door is open, phrased as "ask, not guaranteed" | sources as cited [V] |
| S11 | Labour-court defence window for a BTL or employment suit | Some BTL letters are court papers, not decisions | [U] |
| S13 | Decision on a judicial demolition order (צו הריסה שיפוטי) venue | Distinct from the administrative order in 8.4 | [U] |
| S14 | Reserve duty and BTL figures that appear on letters (minimum 328.76 NIS/day from 1.1.2026) | Read only, never computed | btl.gov.il forms index [V] |

## Out of scope (explicit)

- Execution Office procedure beyond the first אזהרה window (payment orders, ability examination, פרעתי, restrictions and their cancellation, registrar decisions and appeals, mortgage realisation, insolvency thresholds). Delegated to the `israeli-hotzaa-lapoal-debtor` skill, which carries the forms and clocks. Reviewed 2026-10-29: users do ask, and the decoder answers by naming the file type and routing.
- VAT books-refusal appeals and other VAT procedure beyond the s.82 השגה and s.83 appeal. Route to an accountant; the `israeli-vat-reporting` skill covers reporting.
- Condominium superintendent (מפקח על רישום מקרקעין) disputes in a בית משותף: the appeal period sits in regulations not verified this cycle. Route to `israeli-building-committee` and a lawyer.
- The betterment-levy שמאי מכריע procedure and the appeal on a levy schedule (לוח שומה): the decoder gives the 45-day ערר (row 8.5) and refers to a licensed appraiser for the rest.
- Medical-negligence and other special civil tracks with their own defence periods.

- Drafting an השגה, ערר, התנגדות, appeal, petition or any court pleading for filing. The skill explains the route, the venue and the window; drafting a filing for a specific case is reserved work product and is covered by the skill's legal notice (see the `legal-review` gate). A plain-language outline of what the user should tell a lawyer is fine; a filing-ready document is not.
- Computing tax, arnona, betterment levy, fines, interest, linkage, benefit amounts or protected-wage figures. Route to the tax, BTL, arnona and Hotzaa LaPoal skills and to the /tools calculators.
- OCR of scanned letters or photos. The skill works on text the user pastes or that the host agent already extracted; it must say when the text is incomplete rather than guess missing dates or file numbers.
- Predicting the outcome of an appeal or advising whether to file.
- Contacting any authority, filing online, or logging into personal areas (login.gov.il, secapp.taxes.gov.il, the Execution Office site) on the user's behalf.
- Non-Israeli authorities, and letters from private bodies (banks, insurers, debt collectors) except where they are a stage of an Execution Office file.
- Criminal indictments and police investigations beyond the fine-notice track in row 4.5.

## Authoritative sources

Statutes and regulations (he.wikisource.org raw statute text, read 2026-10-29):
- חוק ההוצאה לפועל, התשכ"ז-1967. (he.wikisource.org)
- תקנות ההוצאה לפועל, התש"ם-1979. (he.wikisource.org)
- פקודת מס הכנסה. (he.wikisource.org)
- תקנות בית משפט (ערעורים בעניני מס הכנסה), התשל"ט-1978. (he.wikisource.org)
- חוק מס ערך מוסף, התשל"ו-1975. (he.wikisource.org)
- חוק מיסוי מקרקעין (שבח ורכישה), התשכ"ג-1963. (he.wikisource.org)
- חוק הרשויות המקומיות (ערר על קביעת ארנונה כללית), התשל"ו-1976. (he.wikisource.org)
- חוק סדר הדין הפלילי [נוסח משולב], התשמ"ב-1982. (he.wikisource.org)
- חוק הכניסה לישראל, התשי"ב-1952. (he.wikisource.org)
- תקנות בתי משפט לעניינים מינהליים (סדרי דין), התשס"א-2000. (he.wikisource.org)
- חוק המקרקעין, התשכ"ט-1969. (he.wikisource.org)
- תקנות המקרקעין (ניהול ורישום), התשע"ב-2011. (he.wikisource.org)
- חוק התכנון והבניה, התשכ"ה-1965. (he.wikisource.org)
- תקנות שיפוט בתביעות קטנות (סדרי דין), התשל"ז-1976. (he.wikisource.org)
- תקנות סדר הדין האזרחי, התשע"ט-2018. (he.wikisource.org)
- פקודת המסים (גביה). (he.wikisource.org)
- חוק חופש המידע, התשנ"ח-1998. (he.wikisource.org)

Official pages:
- BTL appeals to the labour court (12 months, מזונות 6 months): btl.gov.il, "ערעור על החלטות המוסד לביטוח לאומי / בתי הדין האזוריים לעבודה"
- BTL medical-committee ערר, general disability: https://www.btl.gov.il/benefits/vaadotRefuiyot/erurVadot/Pages/erurNechut.aspx
- BTL medical-committee ערר, work injury: https://www.btl.gov.il/benefits/vaadotRefuiyot/erurVadot/Pages/erurNechutMeavoda.aspx
- BTL forms index: the "טפסים ואישורים" section of btl.gov.il
- Tax Authority service pages: https://www.gov.il/he/service/itc101 , /itc-106 , /itc135 , /tax-coordination-online , /real-estate-tax-7000 , /vat-821 , /reporting-and-payment-2025-annual-tax-report-for-individuals
- PIBA office page: https://www.gov.il/he/departments/population_and_immigration_authority
- Planning Administration: https://www.gov.il/he/departments/iplan
- Kol Zchut (browser render only, 403 to plain fetch): Execution Office debtor pages, arnona, small claims. Secondary source, use only to locate the statute.

Open items before publication ([U] rows): VAT appeal window to the District Court (2.6), late-filing-fine relief route (2.4), condominium superintendent appeal window (6.3), contest route for a tax-collection seizure (S1), labour-court defence window (S11), judicial demolition order venue (S13).
