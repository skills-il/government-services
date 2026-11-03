---
name: israeli-war-damage-claims
description: "Guide users through filing DIRECT property damage claims from rocket attacks and hostilities in Israel (Iron Swords and Shaagat HaAri 2026): documenting damage, filing with the Tax Authority Compensation Fund, home contents insurance, assessor visits, appeals. Use when user asks about physical property damage from war, rockets, missiles, 'nezek yashir', 'mas rechush', 'keren pitzuim', war damage claim, damaged apartment, broken windows from blast, or compensation for hostility damage. Covers fast track (up to NIS 30,000), regular track, optional contents insurance, and appeals (va'adot erar). Do NOT use for indirect/economic business damage like turnover decline or wage grants (use israeli-business-war-compensation), employee unpaid-leave dmei avtala (use israeli-unemployment-benefits-navigator), personal injury (israeli-bituach-leumi), ordinary road-accident car damage (private insurance), or general home insurance (israeli-insurance-comparator)."
license: MIT
---

# Israeli War Damage Claims

## Legal notice

This is a free information tool operated by an AI model. It explains the law and the procedure and helps you organise your own documents. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by an advocate. The output is not legal advice and not a legal opinion, but a general explanation and a template only: it does not read the full file of your matter, does not check current case law, and does not examine your specific circumstances. An AI model may err, omit data, or present a wrong conclusion.

Any text this tool drafts is an automatic draft for your personal preparation only. It is not a document prepared by an advocate and must not be relied on as evidence. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Before starting proceedings, signing a document, or filing with an authority or a court, consult an advocate. All use of its output is the user's sole responsibility.


## Problem

Claiming from the Tax Authority's Compensation Fund for rocket and missile damage involves two tracks, separate deadlines, and contents ceilings that vary by household. Some mistakes (repairing before the appraiser sees the damage, taking the fast track on a borderline claim) cannot be undone afterwards.

The direct-damage process here is the same across recent conflicts, Iron Swords, Operation Am K'Lavi (the war with Iran), and Shaagat HaAri (from 28 February 2026).

## Instructions

This skill ends in three artifacts the user can act on: a **claim calendar** (Step 2), a **contents claim worksheet** (Step 5), and, if needed, an **appeal preparation checklist** (Step 8). Collect the inputs first: the damage date, the address, what was damaged (structure, contents, vehicle, business property), the household composition, and whether the user bought the optional contents insurance before the damage.

### Step 1: Identify the Damage Type and Correct Track

| Damage Type | Hebrew Term | Who Compensates | Track |
|---|---|---|---|
| Structural damage (walls, roof, windows, doors) | נזק למבנה | Tax Authority Compensation Fund (קרן הפיצויים) | Regular or Fast |
| Home contents (furniture, electronics, appliances) | נזק לתכולה | Compensation Fund (capped per category by household size) | Regular or Fast |
| Contents above the ceiling | תכולה מעל התקרה | Optional contents insurance with the Tax Authority, only if bought BEFORE the damage | Insurance claim |
| Business equipment and stock | נזק לעסק | Compensation Fund (equipment at its pre-damage market value, stock at cost excluding VAT) | Regular or Fast |
| Vehicle damaged by a missile or shrapnel | נזק לרכב | Compensation Fund, not your car insurer | Regular track only (the fast track covers structure and contents only) |
| Personal items damaged while you were near the impact site | חפצים אישיים | Compensation Fund, with a police confirmation that the damage came from a hostile act | Fund staff on site or a Real Estate Taxation / Income Tax office |
| Glasses, hearing aid, walker or other medical aid | אביזר רפואי | Bituach Leumi (refund at Ministry of Health tariffs), not the Fund | Bituach Leumi claim |
| Economic loss (lost revenue, wages) | נזק עקיף | Separate indirect-damage track | **Use `israeli-business-war-compensation`** |

**Key distinction:** The Compensation Fund (under the Property Tax and Compensation Fund Law, 1961) handles direct physical damage. **Indirect economic damage is a completely separate process** with its own tracks, portals, forms and appeal routes (for Shaagat HaAri, an additional indirect-damage track for March and April 2026 was added to the 1961 Law as a temporary provision). If the loss is turnover decline, employee wages, or fixed business costs, route to `israeli-business-war-compensation` immediately.

### Step 2: Document the Damage and Build the Claim Calendar

**Do not repair, and do not clear debris, before the Fund's appraiser has seen it.** The Tax Authority guide: "אין לפנות ציוד, מלאי, פסולת או כל חפץ זר שנמצא בבית המגורים או בעסק, ללא תיאום מוקדם עם שמאי מטעם קרן הפיצויים. ניתן לפנות את הזכוכיות שנסדקו טרם הגעת צוותי קרן הפיצויים לאזור שנפגע. אסור לתקן ללא בדיקת שמאי." Cracked glass is the one thing you may clear first. The same rule applies to vehicles: repair at any garage, but only after the Fund's appraiser approves the repair.

**Mitigate what you safely can.** Regulation 7(ב) lets the director reduce compensation "אם נוכח כי הניזוק לא פעל באופן סביר להקטנת הנזק". Covering an opening against rain is mitigation; a full repair is not, and needs the appraiser first.

**Documentation checklist:**
1. Photograph all damage from multiple angles (wide shots and close-ups), and the whole apartment for context
2. Keep damaged items in place until the appraiser has seen them
3. Collect repair quotes from licensed professionals (at least 2 recommended)
4. Save receipts for any emergency work already done
5. Note the exact date and time of the damage event
6. Save Pikud HaOref alerts or news reports for that date as supporting evidence

**Fast track only:** do not take the claim photos in advance. They must be taken at the damage site AFTER the claim is opened, through a link sent by SMS (Step 4).

**The claim calendar (artifact 1).** Compute these dates from the user's damage date and hand them over as a list. Flag any date that has passed or falls within the next few days, and tell the user to file the notice and the claim together now:

| Deadline | Rule | Source |
|---|---|---|
| Notice of damage (הודעה על נזק) | Two weeks from the damage | Regulation 5(א); Tax Authority guide |
| The claim itself (תביעה לפיצויים) | Three months from the damage per the Tax Authority guide; the base regulation text says one month | Tax Authority guide; regulation 5(ב) |
| Fast-track invoice | 30 days from the fast-track payment, or the payment is clawed back | Tax Authority claim page |
| Appeal to the ועדת ערר | 30 days from delivery of the decision (the decision letter states the date that applies) | Regulation 11 |
| Appeal to the District Court | 30 days from receiving the committee's decision, on a question of law only | Regulation 12א |

Three rules to state alongside the calendar:
- **The notice and the claim are two separate filings.** Filing the notice does not file the claim. Plan for the shorter one-month figure and confirm on *4954 if in doubt.
- **Neither deadline is an automatic forfeiture.** Regulation 5(ג): "המנהל רשאי להאריך את המועדים... אם נוכח כי ישנה סיבה סבירה לכך". Ask for the extension BEFORE the deadline passes where you can. A refusal to extend can itself be appealed to the ועדת ערר.
- **The director has deadlines too.** Regulation 8(ב): the decision is to be sent "תוך ששה חדשים מיום הגשת התביעה". Regulation 8(ג): compensation is paid "תוך שלושים יום מיום ההחלטה". Regulation 8(ד) adds interest from 30 days after the damage until payment.
- **Ask for an advance.** While the amount is not yet fixed, regulation 13 lets the director guarantee a loan or pay "מקדמה שלא תעלה על 50% מסכום הפיצויים". Regulation 9(ג): any overpayment, advance included, is repaid within 90 days of a demand, with linkage and interest.

### Step 3: Choose Between Fast Track and Regular Track

| Feature | Fast Track (מסלול מהיר) | Regular Track (מסלול רגיל) |
|---|---|---|
| Maximum claim | NIS 30,000 | No fixed ceiling for structure or vehicles (paid on the actual damage, see Step 5); contents capped per category |
| What it covers | Structure, household contents, business equipment and stock. Not vehicles | Everything in Step 1 |
| Appraiser visit | Not required; only available if no appraiser has visited yet | Required |
| Decision time | Within 7 business days | Regulation 8(ב): up to 6 months from the claim |
| Limit | One claim per family per event; an owner of several properties can fast-track only one of them | No equivalent limit |
| Invoice | Must follow within 30 days of payment if only a quote was attached | Per the director's decision; payment may be conditioned on restoration (regulation 8(א)) |
| Appeal | **Only if the whole claim was rejected. A partial approval cannot be appealed** | Any decision can be appealed, including a partial approval |

**Fast track trade-offs to spell out to the user:**
- A fast-track claim is filed **instead of** a regular claim, and no further claim can be filed on the same event in the regular track. Check for every damaged item before submitting.
- Giving up the appeal on a partial award is the real cost. Someone with a borderline claim who might want to contest a low figure should prefer the regular track.
- A fast-track claim that is not approved is passed to the regular track, where an appraiser assesses it.
- **A damaged car too?** The fast track excludes vehicles, yet it bars a further regular claim on the same event. Before choosing it, confirm on *4954 that the vehicle claim stays open (how the Fund applies the bar to vehicles is not published).

**The fast track is opened per operation and then closed.** For Shaagat HaAri its filing deadline was 28.04.2026, after which only the regular track remained. **Never tell a user the fast track is open without checking the current status** on the Tax Authority claim page or *4954; if it is closed, the regular track is the only route.

**Switching tracks:** During Shaagat HaAri, people who had filed a regular claim from 28.02.2026 and had not yet had an appraiser visit could switch through the "מעבר מסלול" button in the claim.

### Step 4: File the Claim Online

**Filing:** the Tax Authority's online direct-damage claim (הגשת תביעה מקוונת - נזק ישיר) on gov.il, or the Compensation Fund's hotline *4954 (the Tax Authority guide names both). The claim page offers three routes: regular, fast, and a route without identification.

**Who can file:** the property (structure) owner, whoever is funding the restoration, and the owner of the damaged contents, including a tenant.

**Required information:**
1. Israeli ID number (Teudat Zehut)
2. Property address
3. Description of the damage and the amount claimed
4. Repair quotes that match the amount claimed
5. Bank account details in the claimant's name for payment
6. For a business's stock and equipment: purchase invoices for the stock and Form 11 (טופס י"א) for the equipment

**Vehicle claims** also need: the vehicle licence; a police confirmation that includes the vehicle number and the signature of a police investigator and officer; a power of attorney if the filer is not the owner; the leasing agreement for a long-term leased car or the rental agreement for a taxi; for a repair over NIS 10,000, the insurer's confirmation that no insurance claim was filed; and a cheque copy or bank confirmation of an account in the claimant's name.

**Fast track photos:** after the details are entered, the system sends an SMS link. Photos must be taken and uploaded from the damage site only, after that SMS. The Tax Authority checks the phone's location at upload time; photos taken earlier or uploaded elsewhere are not accepted and the claim is not completed.

**If the home is uninhabitable (לא ראויה למגורים).** The Fund's or the local authority's representatives refer the residents to alternative housing; if none has come yet, call the local authority's hotline. Whether it is uninhabitable is decided by a competent official of the local authority. For the Iran-war operations (Am K'Lavi and Shaagat HaAri), per the Tax Authority evacuee FAQ and Kol Zchut:
- Short term: a hotel arranged by the local authority and funded by the Fund, or self-evacuation with a payment of NIS 4,000 for up to two weeks.
- Long term: a rented alternative apartment, with the Fund paying rent matched to the damaged home; a continued hotel stay, conditional on a claim having been filed and approval; or self-evacuation. An owner-occupier who self-evacuates gets NIS 4,000 a month (single adult) or 5,000 (couple or single parent), plus 500 per child under 18 and 1,000 per additional adult, capped at 80% of comparable rent. A tenant gets the rent of the damaged apartment while still paying it. An owner who did not live in the apartment gets no alternative housing.
- Moving and brokerage costs are paid, against an invoice, only when the alternative-apartment option is chosen.
- How to claim the long-term payment: first file the structure claim, then send an online request through the Tax Authority's request system under "צירוף חוזה שכירות" (alternative apartment) or "הצהרה בגין פינוי עצמי" (self-evacuation). A tenant attaches the lease of the evacuated flat (plus the new lease, if any) and a signed declaration of when that lease ends and the rent they keep paying.
- Initial aid of NIS 500 per person evacuated, on top of the compensation; and, for Shaagat HaAri, a ban on dismissing an employee who had to evacuate, for 3 months from the evacuation.
These arrangements are set per operation. For any other event, check the Tax Authority's current guide before quoting them.

**Tenants:** if the home is uninhabitable, the tenant may cancel the lease, or keep it and may be exempt from rent for the period they cannot live there. But a tenant is entitled to alternative housing from the Tax Authority only while the lease is in force and rent is being paid. Lay out both choices before the tenant decides.

### Step 5: Build the Contents Claim Worksheet

Structure and vehicles are paid on the "actual damage" (הנזק הממשי, regulation 1): the drop in the property's value or the restoration cost, whichever is LOWER, plus the cost of reducing the damage. An older car whose repair would cost more than it was worth gets the drop in its value (the pre-damage value minus what the wreck is still worth), not the repair cost; ask the appraiser how the wreck is handled. The Fund pays only up to the actual damage, net of what an insurer or third party paid or owes for it (regulation 3), and property tax the claimant owes is deducted unless the director decides otherwise (regulation 4). **Household contents are capped per category** by תקנות מס רכוש וקרן פיצויים (תשלום פיצויים) (חפצים ביתיים), תשל"ג-1973. Each item is valued at its **repair cost, or, if it cannot be repaired, the price of a similar NEW item**, with no deduction for age.

The ceilings are re-indexed on 1 January and 1 July, and each column is published as applying "מיום" (from) its date. No source says whether the damage date or the claim date selects the column. If both fall in the same half-year, use that column. If they straddle 1 January or 1 July (damage in March 2026, claim after 1 July 2026), show both columns' ceilings and tell the user to ask the Fund which applies.

**Household-contents ceilings in shekels, column from 01.07.2026** (Tax Authority guide):

| Category | Single person | Married couple / single parent | Each child under 18 | Each adult living with a couple or single person |
|---|---|---|---|---|
| Furniture (רהיטים) | 14,168 | 24,502 | 4,953 | 7,243 |
| Clothing (בגדים) | 2,371 | 4,741 | 711 | 2,371 |
| Electrical appliances and electronics | 24,407 | 29,585 | 495 | 3,883 |
| **Other household items (חפץ ביתי אחר)** | 10,490 | 25,179 | 2,308 | 4,616 |
| **Total** | **51,436** | **84,007** | **8,467** | **18,113** |

The 01.01.2026 column (Kol Zchut) is in `references/compensation-ceilings.md`.

**How to build the worksheet (artifact 2):**
1. Pick the base column and add one child column per child under 18 and one adult column per additional adult in the home. The couple column is for a married couple, or a single parent: a parent not living with a partner who has at least one child under 18 living at home (regulation 1). A parent whose children are all 18 or over takes the single column plus one adult column per adult child. Goods of spouses and of household members living with them count as one owner's goods; unrelated co-residents (a roommate, a second family) and an unmarried couple should confirm with the Fund how they are counted, rather than being folded in as adult columns by default.
2. List every damaged item the household owns and uses personally, with its repair cost or new-replacement price, and put it in exactly one of the four categories. Leave out items the household does not own, such as a landlord's furniture. For an item used partly for work, such as a laptop, ask the appraiser whether it is claimed as a household item or as business equipment (valued at pre-damage market value). "Other household items" is the residual category: anything that is not furniture, clothing or an electrical appliance (a pot, a towel, a book, a toy) goes there, and it is the category claimants most often leave empty. Ask the appraiser about borderline items.
3. Strike excluded items: cash, cheques, jewellery (תכשיטים), artworks (חפצי אמנות) and antiques (עתיקות). The regulation defines a household item as "רהיטים, ביגוד, כלים, מכשירים לשימוש ביתי, ספרים ותקליטים, המצויים בבית מגוריו של אדם ואינם נכס כהגדרתו בחוק, למעט תכשיטים, חפצי אמנות ועתיקות".
4. For each category, show: the claimed total, the published ceiling, and by how much the claim exceeds the ceiling, if at all.
5. The ceilings are **per category and not interchangeable**: unused furniture headroom does not top up an over-ceiling electrical loss. Excess is recoverable only under the optional insurance, only for a category that was declared, and only if the declaration was made and paid before the damage (Step 6).

Output a table with one row per category (items, claimed, ceiling, above ceiling) and a total row, plus a line naming the column used and the household composition. **Do not state what the Fund will pay.** The amount is set by the Fund's appraiser and the director; the worksheet is the user's own organised list against the published ceilings.

### Step 6: Optional War Damage Contents Insurance

For contents worth more than the ceilings, the Tax Authority sells supplemental cover:
- Declared per category: only the categories on the declaration are insured, and for an insured category the insurance replaces the free cover rather than topping it up (regulation 4(ב))
- Premium: 0.3% per year of the additional value insured above the ceiling
- Maximum additional value: NIS 1,049,113 per the Tax Authority guide updated 01.07.2026 (Kol Zchut still shows 1,037,100 "נכון ל-2026", the earlier figure)
- Coverage starts after the premium is paid and the declaration accepted, and runs to 31.12 of that year, so it must be bought before the damage and renewed each year
- Keep the declaration form; the Fund may check that the declared items exist
- Bought through an online declaration form or at a Tax Authority office; help on *4954

### Step 7: After Filing

**Regular track:** claim acknowledged, appraiser visit (structure) or Fund assessment (vehicle), then the director's decision on entitlement, amount and restoration. For structural damage the user chooses between **self-restoration** (receive the money and hire their own professionals) and **restoration by a company working on behalf of the Fund**.

**Fast track:** decision within 7 business days. If only a quote was attached, the matching invoice is due within 30 days of payment.

**No decision for an unreasonable time:** write to Mas Rechush through the personal area on the Tax Authority site or call *4954. If there is still no decision, the ועדת ערר can be approached with the full facts (gov.il appeal page).

### Step 8: Appeal (ערר) and the Appeal Preparation Checklist

**Who hears it:** the ועדת ערר under regulation 12, a judicial body under the Ministry of Justice. It sits as **three members**: a chair who meets the qualifications of section 4 of the Courts Law (from the Justice Minister's list), a member from the Defence Minister's list, and a member from the Finance Minister's list, at least two of them not civil servants.

**What it can do:** regulation 12(ה), "לבטל, להפחית, לאשר או להגדיל את סכום הפיצויים". The committee can **reduce** the award as well as raise it. Tell the user this before they file.

**What can be appealed:** a final decision on the claim, a decision on an extension request, and a correction under regulation 9. A fast-track partial approval cannot be appealed (Step 3).

**The appeal preparation checklist (artifact 3).** The form is optional; gov.il lists what a written appeal must contain:
1. Full name and ID number; for a company, partnership or business, its name and ID number
2. Up-to-date phone number and an email address for decisions and hearing summonses
3. The Mas Rechush claim number
4. The compensation amount claimed
5. Detailed grounds in paragraphs. Give the user the candidate grounds that fit their facts as short points (which item, which figure, which rule, which evidence), for example: items the appraiser missed, a valuation below the repair or new-replacement price, a ceiling applied to structural damage, a wrong household composition
6. The decision being appealed, and every piece of evidence: independent quotes, a private appraiser's opinion, photos, the contents worksheet from Step 5

**Do not produce a finished appeal letter ready to file and do not fill in the appeal form.** Give the user the structure and the points to cover as raw material that the user writes and signs themselves. For a large or legally contested award, suggest consulting an advocate.

The user sends their appeal by email to **Ararim@taxes.gov.il** or by fax to **076-8090001**, within 30 days of delivery of the decision. Filing is free.

**What happens next:** Mas Rechush files a response within 60 days of receiving the appeal, then a hearing is set and the summons goes to the email address on the appeal. **Not attending the hearing can lead to the appeal being struck out.**

**Further appeal:** regulation 12א, "על החלטת ועדת הערר ניתן לערער, בבעיה משפטית, לבית המשפט המחוזי תוך 30 ימים". It is an appeal as of right, but on a question of law only, not on the amount as such. It is filed with the District Court for the area of the committee's address.

**Correction window:** regulation 9(א) lets the director correct a decision "תוך ארבע שנים מיום שניתנה" if new facts come to light or there was an error. The correction can go either way, and an overpayment is then reclaimed (regulation 9(ג)).

## Examples

### Example 1: Apartment damaged by rocket, fast track open
User says: "A missile hit near my building, all my windows are shattered and some furniture is destroyed. The damage looks well under the fast-track ceiling."

Actions:
1. Check the fast track is open for this event and no appraiser has visited; build the claim calendar
2. Warn: it replaces the regular claim, one claim per family per event, and a partial approval cannot be appealed
3. Open the claim, photograph at the site after the SMS link, upload photos and quotes
4. Decision within 7 business days; invoice within 30 days of payment if only a quote was attached

### Example 2: Major structural damage, contents worksheet
User says: "A rocket hit my building directly in August 2026. The walls are cracked, the ceiling collapsed in one room, and our contents are destroyed. We are a couple with two kids."

Actions:
1. Regular track. Do not clear debris or start repairs before the appraiser visits (cracked glass excepted)
2. Claim calendar from the damage date
3. Structure: compensated on the appraiser's assessment, with self-restoration or a Fund contractor
4. Contents worksheet on the 01.07.2026 column, couple plus 2 children:

| Category | Items | Claimed | Ceiling | Above ceiling |
|---|---|---|---|---|
| Electrical | TV 9,000, fridge 8,500, laptop 7,000, oven 5,000, washing machine 4,500 | 34,000 | 29,585 + 2 x 495 = 30,575 | 3,425 |
| Furniture | sofa 8,000, dining set 6,000 | 14,000 | 24,502 + 2 x 4,953 = 34,408 | 0 |
| Clothing | clothing 5,000 | 5,000 | 4,741 + 2 x 711 = 6,163 | 0 |
| Other | kitchenware 2,500, linens 1,500, toys 1,000 | 5,000 | 25,179 + 2 x 2,308 = 29,795 | 0 |
| **Total** | | **58,000** | **100,941** | **3,425** |

5. Point out that the 3,425 above the electrical ceiling is not covered by the free cover even though the furniture line has 20,408 of unused headroom, unless the family had declared the electrical category under the optional insurance before the damage. Suggest the insurance for the future.

### Example 3: Appeal a low award
User says: "My claim was approved but they paid roughly a third of what the damage is worth. How do I appeal?"

Actions:
1. Check how the claim was filed: a fast-track partial approval cannot be appealed. Regular-track decisions can be
2. Check the delivery date of the decision and compute the 30-day deadline
3. Warn that the committee may also reduce the award
4. Give the user the appeal checklist and the candidate grounds as points: claim number, amount claimed, the grounds that fit, the decision, quotes, a private appraiser's opinion, photos. The user writes and signs the appeal
5. The user emails it to Ararim@taxes.gov.il or faxes 076-8090001; expect a response from Mas Rechush within 60 days, then a hearing; attend it
6. If the committee errs on a point of law, a District Court appeal lies within 30 days

## Bundled Resources

### References
- `references/compensation-ceilings.md` -- both ceiling columns, the valuation rule and the optional insurance. Consult when building the contents worksheet.
- `references/claims-process-flowchart.md` -- the deadlines and the fast, regular and appeal flows. Consult when building the claim calendar or the appeal checklist.
- `references/domain-checklist.md` -- the coverage list this skill is reviewed against.

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Tax Authority direct-damage online claim | https://www.gov.il/he/service/online-direct-damage-claim | Which tracks are open now, fast-track rules |
| Tax Authority guide for civilians whose property was damaged | https://www.gov.il/he/Departments/Guides/guide-for-civilians-property-damaged-in-hostilities?chapterIndex=6 | Current contents-ceiling column, deadlines, vehicle documents |
| Tax Authority appeal service | https://www.gov.il/he/service/submission-of-appeal-committees-compensation-fund | Appeal channels, required contents, response time |
| War-damage regulations, 1973 | https://www.nevo.co.il/law_html/law01/273_020.htm | Reg 5 (deadlines), 7 (reduction), 8 (decision and payment), 9 (correction), 11 (appeal), 12 (committee), 12א (District Court) |
| Household-goods regulations, 1973 | https://www.nevo.co.il/law_html/law01/273_034.htm | Definition of a household item, per-category cap, indexation |
| Tax Authority evacuee FAQ | https://www.gov.il/he/pages/faq_evacuated | Alternative housing, how to claim long-term rent |
| Kol Zchut Q&A on war property damage | https://www.kolzchut.org.il/he/שאלות_ותשובות_למי_שרכושם_נפגע_במלחמה_או_בפעולת_איבה | Fast-track conditions, appeal on partial approval, tenants, business valuation |

## Gotchas

1. **Fast-track photo trap:** photos must be taken at the damage site after the SMS link arrives; the phone's location is checked at upload. Photos taken earlier or elsewhere are not accepted.

2. **Notice and claim are two separate filings.** The notice is due in two weeks, the claim in three months per the Tax Authority guide (one month in the base regulation). Neither is an automatic forfeiture: regulation 5(ג) lets the director extend both for a reasonable cause.

3. **The ceilings move twice a year, and not always upward.** Every furniture and electrical cell in the 01.07.2026 column is LOWER than in 01.01.2026 (clothing and other household items went up). Do not assume the newer table is bigger, and when the damage and the claim straddle an update date, show both columns.

4. **Four categories, not three, and none interchangeable.** "Other household items" (25,179 for a couple from 01.07.2026) is the line people forget. Unused headroom in one category never covers an excess in another.

5. **The fast track costs the appeal on a partial award, and the committee can cut an award.** Both are irreversible choices the user should hear about before filing.

6. **No repair before the appraiser.** Clearing debris or repairing first can leave the damage unprovable; only cracked glass may be cleared in advance.

## Troubleshooting

### Error: "Claim not completed -- photos not from the damage site"
Cause: the fast track requires photos taken in real time at the damage location after the SMS link; the Tax Authority compares the phone's location to the property's.
Solution: go to the site, open the link from the SMS, and take and upload fresh photos there. If the fast track has closed, file on the regular track.

### Error: "Missed the two-week notice deadline"
Cause: no notice was given within two weeks.
Solution: not an automatic forfeiture. File the notice and the claim now, state the reason for the delay (evacuation, hospitalisation, reserve call-up and mass events are typical), and ask for an extension under regulation 5(ג) in the same submission. If the extension is refused, that decision can be appealed to the ועדת ערר.

### Error: "Compensation amount seems too low"
Cause: either a contents ceiling was applied, or the assessment is below the repair or new-replacement price.
Solution: rebuild the Step 5 worksheet. If the shortfall is the ceiling, there is nothing to appeal unless the wrong column or household composition was used. If it is the valuation, prepare an appeal with the Step 8 checklist, on the regular track only.
