---
name: israeli-vehicle-manager
description: "General information only. Not legal advice and not a vehicle appraisal. Manage vehicle ownership in Israel: annual test (test/טסט), registration renewal (chidush rishayon rechev), used car purchase checks, insurance requirements, and transfer of ownership. Use when a user asks about their vehicle test date, how to renew their car registration, what to check before buying a used car in Israel, or understanding Israeli car insurance types. Prevents costly surprises like failed tests, expired registrations, and liens on purchased vehicles."
license: MIT
---

# Israeli Vehicle Manager

## Legal notice

This is a free information tool operated by an AI model. It collects and explains procedures, fees and deadlines published by the Ministry of Transport and other state authorities. All of its output is produced automatically, with no involvement, review or approval by a lawyer, a vehicle appraiser or an insurance agent. The output is not legal advice and not a legal opinion, not an appraisal or professional valuation of the vehicle, and not insurance advice or insurance broking; it is general information only. It does not inspect the vehicle, does not perform the professional adjustments a pricelist or an appraiser performs, does not review your transaction documents, and does not search the Registrar of Pledges for you. An AI model may err, omit data, or present a wrong conclusion, and fees, tariffs and fines are updated from time to time. Do not rely on the output as evidence and do not submit it to an authority or a court. This tool is not a substitute for advice that takes into account the particular data and needs of each person; before signing a sale agreement, registering a transfer, buying a policy or waiving a claim, consult the appropriate licensed professional. Any use of the output is the user's sole responsibility.


## Problem

Owning a car in Israel means dealing with annual vehicle tests, registration renewals, insurance requirements, and complex paperwork. The process involves multiple government agencies, strict deadlines, and penalties that escalate quickly. A large share of vehicles fail the annual test, registration fees vary about sixfold by vehicle group, and used car buyers risk purchasing vehicles with hidden liens. This skill guides users through every aspect of vehicle management in Israel.

## Instructions

### Step 1: Identify What the User Needs

Israeli vehicle management falls into these categories:

| Need | Hebrew Term | Key Deadline |
|------|-------------|-------------|
| Annual vehicle test | טסט (test) | Before registration expiry |
| Registration renewal | חידוש רישיון רכב | Pay up to 60 days before expiry |
| Used car purchase | קניית רכב יד שנייה | Transfer immediately after the sale |
| Insurance | ביטוח רכב | Must be active before driving |
| Ownership transfer | העברת בעלות | Immediately after the sale |
| Taking a car off the road | ביטול רישום / הורדה מהכביש | Before the next licence year accrues |
| Disability-related reductions | רכב נכה | At renewal, and again on any transfer |

### Step 2: Annual Vehicle Test (טסט)

**Who needs a test:**
- All vehicles registered in Israel, annually
- **New private cars are exempt for the first 3 years** from initial registration
- New rental/leased vehicles are exempt for the first 2 years only
- Cars 15+ years old must have braking system checked at a licensed garage BEFORE the test

**Where to go:**
- Authorized Vehicle Inspection Stations (מכוני רישוי) across Israel
- Technotest is one of the largest national operators with branches across Israel
- Station locator: gov.il vehicle inspection service page
- TesTime (testime.co.il) is an online booking / check-in system built with the inspection stations: you pick a slot, pay the test tariff and upload documents in advance

**What is checked:** brakes (front and rear force, left/right balance, emergency brake, lines), steering play, lights (headlamp alignment and intensity, signals, brake lights, plate illumination), tyres (tread depth minimum 1.6mm, pressure, cracks, bulges), tailpipe emissions, suspension and undercarriage play, oil and water leaks, windscreen and wipers, and the required safety equipment (vest, inflated spare, warning triangle, tool kit). Item-by-item checklist in `references/test-preparation.md`.

**Common failure reasons** (a roughly one-in-three failure rate is widely reported, but the Ministry page that carried the statistic is no longer published, so treat the rate as indicative and the categories below as the substance):
- Minor defects: burned-out lights, missing safety equipment, worn wipers
- Tire issues: wrong size, age, insufficient tread depth
- Emissions failures or serious safety defects (brakes, steering, undercarriage)

**Costs** (price-controlled tariff, order effective 1 June 2026; this is separate from the annual licence fee):
- Private car, taxi, minibus, commercial up to 8,000 kg: 126.19 NIS (electric 106.32)
- Motorcycle: 79.71 NIS
- Retest after a failure: 29.86 NIS (electric 26.83, motorcycle 24.70)
- Optional pre-test at a private garage: priced by each garage, not regulated, so ask for a quote. Worth it on an older vehicle

Full tariff by vehicle type is in `references/license-fee-table.md`.

### Step 3: Registration Renewal (חידוש רישיון רכב)

**Not every vehicle is on a 12-month cycle, and a safety recall blocks renewal outright:**
- Renewal is required annually for every vehicle, including non-motorised vehicles, goods vehicles, taxis, trailers, buses, tractors and motorcycles
- **An old vehicle (rechev meyushan) must present an inspection certificate and renew every six months, not every year.** The Ministry service page states the rule without defining the age threshold, so do not guess one: check the expiry on the licence, which will show a six-month cycle if it applies, or ask the licensing bureau
- **A licence cannot be renewed while the vehicle is under an open safety recall (kri'a chozeret betichutit).** Clear the recall with the importer first
- The test cannot be performed until the fee payment has registered in the system, so pay before driving to the station

**Process:**
1. A renewal request is mailed at the start of the month before the month the licence expires. **There is no need to wait for it**, and the obligation runs from the expiry date printed on the licence whether or not it arrives. Pull the invoice yourself from the government personal area
2. Pay the annual license fee (can pay up to 60 days before expiry)
3. Take vehicle to authorized inspection station (unless exempt)
4. New license issued upon passing

**Payment channels:** the government personal area (updates immediately and issues the licence by email), the Ministry site, Apple Pay or Google Pay, self-service terminals (licence issued on the spot), the 5678* phone centre, bank transfer, or cash at an Israel Post branch. Up to 12 instalments. Where the printed form and the computerised system disagree, the system amount governs. Full list in `references/license-fee-table.md`.

**Annual license fees:**

The fee is set by exactly two variables, and the user can find both without leaving the room:

1. **Licence group (קבוצת רישוי), 1 to 7** - printed on the **left-hand side of the vehicle licence**. It reflects the model's consumer price when the model was first registered, not what the owner paid.
2. **Year of first road registration** - four bands: 2024-2026, 2021-2023, 2017-2020, 2016 and older. The fee falls as the vehicle ages.

Ask for the group off the licence rather than guessing from the car's value. The full April-2026 table (all 7 groups x 4 year bands, plus motorcycles by engine volume, disabled, collector and driving-school rates, and the reservist discount) is in `references/license-fee-table.md`. Fees are re-linked to the CPI every April, so confirm the current amount on the gov.il fee board before quoting it.

**April 2026 update:** the CPI-linked hike added 22 to 132 NIS per vehicle, by group and model year, from 1 April 2026.

**Israeli Public Broadcasting Corporation levy:** 139 NIS is added on top of the licence fee on the annual renewal invoice, and often surprises first-time renewers. (The fee board's general table separately lists a 135 NIS line for the same item; the amount on the renewal invoice is what gets paid.)

**EV note (2026):** From January 2026 the EV-specific discount on the annual registration fee was equalized with benzin vehicles. EVs still pay a lower annual test (mivchan rishyon) tariff of 106.32 NIS against 126.19, but the registration agra is now the standard rate.

**Reservist discount:** the fee board publishes a licence-fee discount for reservists by credit points: 70 NIS for 1 point, 141 for 1.5, 211 for 2.

**Insurance requirement:** Must have valid mandatory insurance (bituach chova) certificate to renew.

**Penalties for late renewal:**

| Delay | Consequence |
|-------|------------|
| Driving without a valid test | Graduated: 250 NIS + 6 points (up to 4 months expired); 1,000 NIS + 6 points (4 months to 1 year); court summons (over 1 year). Amounts are from a secondary legal source stated as of 2023 and were not confirmed against the primary set-fine schedule, so present them as an order of magnitude and tell the user to confirm the current amount on the notice |
| About 4 months after expiry | The licence can then be renewed only at the Penalties Collection Center (merkaz ligviyat knasot), not through the ordinary online flow |
| Reminder letters | A first letter to test and renew is sent about a month after expiry, a second at about two months, a third at about three |

### Step 4: Used Car Purchase Checks

Before buying a used car in Israel, verify these items:

**1. Vehicle history report:**
- Gov.il vehicle ownership report service
- Shows: model, transmission, AC, ABS, airbags, doors, ownership history
- Third-party services (Autoboom, CheckCar, both paid): mileage from last test, recall campaigns, structure changes
- **Look for a total-loss marking (אובדן גמור / אובדן להלכה).** A vehicle written off as a total loss is the trigger for deregistration in Step 6, so a car carrying that flag and still on the road needs an explanation from the seller. Ask the insurer you plan to use whether they will write comprehensive cover on it before you commit to a price, rather than assuming either way
- Check whether the vehicle is under an open safety recall. An open recall blocks the annual renewal

**2. Check for liens and encumbrances (עיקולים):**
- This is the buyer's sole responsibility
- The government personal area does display registered liens and pledges on the vehicle, but it is not the authoritative register for a pledge
- The authoritative register is the **Registrar of Pledges (רשם המשכונות)** at the Ministry of Justice. Search it separately through the Ministry of Justice online services; the gov.il service page for it has been renumbered more than once, so search by name rather than following an old bookmark
- A post office may process a transfer even where a lien exists, so a completed transfer is not proof the car is clean
- A registered pledge also **blocks** a transfer until the lender issues a release letter and the pledge is deleted. In an operating lease the leasing company is the owner, so the driver has nothing to transfer

**3. Pre-purchase inspection:**
- Available at authorized inspection stations
- Includes: brake/steering assessment, emissions, body/assembly visual inspection, electronics scan, chassis diagnostics
- Output: detailed report with findings and repair recommendations

**4. Estimate the value (מחירון / שווי רכב):**

Before you negotiate a used-car price, check the market value:
- Ministry of Transport official pricelist (free): https://carlistprice.mot.gov.il/ - the ministry's own reference price, used to compute the ownership-transfer fee. It is a conservative official figure and typically runs lower than the commercial price.
- מחירון לוי יצחק (levi-itzhak.co.il) - the commercial benchmark most dealers, insurers, and banks price against. It is a paid product, though some banks' and insurers' car-value pages surface a free single lookup.

Both give a BASE price for the model, year, and trim. The real value moves up or down from that base with:
- Ownership type: a private-hand (יד פרטית) car is worth more than an ex-company, rental, lease, driving-school, or taxi car.
- Number of previous owners: more owners lowers the value.
- Kilometrage relative to the average for the car's age: above-average km lowers it, below-average raises it.
- Structural change (שינוי מבנה): a non-original structural modification lowers value noticeably.
- Import path: a parallel or personal import (יבוא מקביל / יבוא אישי) is worth less than an official-importer car of the same model, year, and trim.
- Condition, and any accident or lien history (use the vehicle-history report and the Registrar of Pledges check above).

The exact adjustment percentages are part of the (proprietary) מחירון, so use the tools above for the number rather than a formula. This is an estimate to anchor a negotiation, not an official appraisal.

**5. Transfer of ownership (העברת בעלות):**

| Method | Cost | Requirements |
|--------|------|-------------|
| Online, government personal area | 235 NIS (motorcycle 70) | Both parties Israeli citizens, both logged in and authenticated at the same time |
| Post office | 257 NIS (motorcycle 87) | Both parties present in person with IDs |
| Registration to a licensed dealer | 43 NIS | Vehicle registered in the name of a trade-licence holder |
| Licensing bureau | Varies | One or both parties not Israeli citizens; company vehicles; **inheritance** (requires a succession or probate order) |

Fees effective 1 April 2026, from the Ministry of Transport fee board.

**Deadline:** Register the transfer the same day. The traffic regulations set **no express deadline** for a private party: תקנה 284 governs the procedure and states no time limit, and the widely-quoted "15 days" comes from תקנה 10, a residual clause supplying 15 days for any required act with no stated time. Do not cite it to תקנה 284. The six-business-day and seven-day figures that appear in תקנה 284(ג) bind only large trade-licence holders. What actually matters: the seller stays the registered owner, and therefore carries fines, tolls and liability, until the transfer is recorded.

**Protect against a fraudulent transfer:** since 27 July 2026 an owner can block post-office transfers of their vehicle from the government personal area, and lift the block at any time. The Ministry introduced it after dozens of identity-theft transfers. The usual scam: a "buyer" responds to a second-hand listing and asks for a photo of the vehicle licence, supposedly to price insurance or finance, then uses it to register the car to someone else while the real owner still has it. Never send a photo of a vehicle licence or ID to an unverified buyer, keep the block on while not selling, and transfer through the personal area rather than on paper.

**Online-transfer footgun:** the fee must be paid within about 10 minutes of finishing the online transfer flow. Miss that window and the transfer does not complete. Have card details ready before you start, so the payment step is not what stalls.

**Required documents:** Current vehicle license, IDs of buyer and seller, signed sale agreement.

### Step 5: Israeli Car Insurance

**Three main types:**

| Type | Hebrew | What It Covers | Required? |
|------|--------|----------------|-----------|
| Mandatory (bituach chova) | ביטוח חובה | Bodily injury to driver, passengers, pedestrians, and other road users | Yes, by law |
| Comprehensive (bituach makif) | ביטוח מקיף | Theft, fire, accident damage to your own vehicle, plus mandatory coverage | No (recommended) |
| Third party (tsad gimel) | ביטוח צד ג' | Damage to other vehicles/property, plus mandatory coverage | No |

**Mandatory insurance is required:**
- Must be active before driving
- Required for registration renewal
- Covers bodily injuries only (not property damage to your own vehicle)
- Provided by all insurance companies in Israel

**What mandatory insurance does NOT cover:** any property damage at all. It does not pay for the other party's car, and it does not pay for yours. A driver holding only chova who damages someone else's vehicle is personally liable for the full repair bill. This is the single most common misunderstanding about Israeli car insurance, and it is why third-party or comprehensive cover exists.

**If no insurer will quote you:** the Israeli Vehicle Insurance Pool (הפול, pool.org.il) sells mandatory insurance directly, so it is the place to send a driver who cannot get a quote on the open market.

**If the driver who hit you was uninsured or fled:** a statutory compensation fund (קרנית), established under the road-accident victims compensation law, exists for victims of an uninsured or hit-and-run driver. Tell the user a remedy exists rather than that they have none, and have them confirm current contact details before applying.

**What moves a chova premium:** driver age and licence seniority, engine volume, and claims history. A young or newly-licensed named driver is the largest single loading on a quote.

**Tips for comparing insurance:**
- Get quotes from multiple insurers (direct and through agents)
- Check the Insurance, Pension & Capital Market Authority website for price comparison data
- Consider deductible amounts (hashtatfut atzmit) when comparing prices
- No-claims discount (heenachot) accumulates over claim-free years

### Step 6: Taking a Car Off the Road (ביטול רישום)

When a vehicle is scrapped, dismantled or written off as a total loss, deregister it. Until the registration is cancelled the annual licence fee keeps accruing against the registered owner, and people routinely discover years later that a car they sent to a scrapyard is still theirs with a growing debt.

Key rules from the Ministry of Transport service:
- Applies to a vehicle that has gone out of use because it has aged out, been dismantled, or been declared a total loss
- **A vehicle carrying a lien, pledge, customs restriction or debts (7A / 8A) cannot be deregistered.** The restriction has to be cleared first, which is the same lien problem the used-car section covers
- If the licence had already expired and the vehicle was not in "deposit" (הפקדה) status, the pro-rata licence fee from the expiry date to the cancellation date is payable
- Filed through the government personal area, the business area, or a licensing bureau
- **If the car is only temporarily off the road, deposit the licence (הפקדת רישיון רכב) instead of deregistering.** Deposit stops the clock without ending the vehicle's registration, and it is also one of the grounds for a reduced fee or a fee refund
- A cancelled vehicle can be returned to roadworthiness later under a separate procedure

We could not find a currently active government scrappage grant. The Ministry scheme from the early 2010s is not published as running, and the pages that discuss it are secondary and contradict each other, so this is a negative finding rather than a confirmed position. Do not promise a grant, and do not flatly tell a user none exists either: point them at the Ministry to confirm. In practice, today it is private scrapyards that pay for a vehicle.

### Step 7: Disability-Related Reductions

- The annual licence fee for a vehicle registered to a person with a disability (רכב של נכה) is **30 NIS**, against 849 to 5,364 NIS for an ordinary private car. If a user mentions a disability, do not quote them the standard range
- A vehicle bought with a tax exemption or reduction can trigger **repayment of the tax difference on transfer**. The Israel Tax Authority publishes the calculation and it is linked from the ownership-transfer service. Check it before pricing such a car
- A reduced licence fee or a refund is applied for through a dedicated Ministry service. The grounds it lists are a disabled parking badge, theft, a deposited licence or a vehicle handed over for dismantling, and other reasons
- The disabled parking permit (תו חניה לנכה) is a separate application under the parking-for-the-disabled law, not part of vehicle registration

## Gotchas

1. **New car exemption is 3 years, not 2.** Private passenger vehicles are exempt from the annual test for the first 3 years from initial registration. Rental and leased vehicles are exempt for only 2 years. Agents often confuse these.

2. **Registration fees vary dramatically.** The annual license fee runs from 849 NIS to 5,364 NIS depending on licence group and the vehicle's year on the road (April-2026 table), a spread of about six times. Do not state a fixed fee without knowing the vehicle's price group. **EV purchase tax (mas knisa) rose to 48% from January 1, 2026** (compromise after the Treasury proposed 52%; was 45% prior). The EV tax-benefit ceiling for 2026 is approximately NIS 22,000. The 2025 ceiling was NIS 35,000 per the Tax Authority; a widely-quoted "down from NIS 30,000" figure refers to a proposal, not to what applied in 2025. Verify current figures at gov.il/taxes.gov.il since the ceiling and rate are politically sensitive and can shift mid-year.

   **Green rating drives the rest of the purchase tax.** Purchase tax on vehicles has been 83% since 2009, reduced by a shekel amount set by the vehicle's air-pollution grade (דירוג זיהום, 1 to 15, where 1 pollutes least and the reduction grows the cleaner the car is). The grade is printed on the vehicle licence and the green label. Electric vehicles were excluded from the 2025 trim to that benefit through the end of 2027. This grade, not the sticker price, is why two similarly-priced cars carry different tax.

3. **Liens are the buyer's problem, not the seller's.** The Ministry of Transport system does NOT show all liens on a vehicle. Always direct used car buyers to check with the Registrar of Pledges (רשם המשכונות) at the Ministry of Justice before completing a purchase.

4. **Do not delay the ownership transfer.** Register it the same day if you can. The seller remains legally responsible for the vehicle (fines, tolls, and liability) until the transfer is actually recorded, so a delay is the seller's risk, not the buyer's.

5. **Cars 15+ years old have extra requirements.** Before the annual test, these vehicles must have their braking system checked at a licensed garage and present confirmation at the inspection station.

6. **Light-electric-vehicle (kalanoit / e-scooter / e-bike) registration is mandatory since August 1, 2024.** E-bikes and e-scooters require registration with the Ministry of Transport plus a personal license plate. The plate is tied to the rider, not the vehicle. The Ministry fee board carries no licence-plate fee line for this, so treat the plate as a cost charged by the licensed installer rather than a government agra, and do not quote a figure. Minimum age is 16. Helmets are mandatory. Riding an unregistered light-electric vehicle on public roads is now a finable offense.

7. **Iron Swords reservist (miluim) protections.** During the active war-period (late 2023 through early 2024) the Ministry of Transport granted blanket deferrals on vehicle test and registration deadlines for reservists serving under Order 8. Outside that one-time window there is no standing automatic deferral by length of service, reservists who hit a deadline mid-call-up should still contact the Ministry of Transport service line because case-by-case extensions are sometimes granted, but should not assume automatic relief.

## Examples

### Example 1: "How much is my annual licence fee?"

Do not answer with the 849 to 5,364 NIS range. Ask for the **licence group printed on the left-hand side of the vehicle licence** and the **year the car first went on the road**, then read the single cell from `references/license-fee-table.md`. A group 3 car first registered in 2019 pays 1,487 NIS, plus the 139 NIS broadcasting levy, so about 1,626 NIS. Then say the table is re-linked to the CPI every April and point at the gov.il fee board to confirm. If the user mentions a disability, the figure is 30 NIS instead and the range is irrelevant.

### Example 2: "I'm buying a used car tomorrow, what do I check?"

Run the sequence, not a list of tips: pull the ownership report from gov.il, search the **Registrar of Pledges** for a pledge (the personal area is not the authoritative register, and a post-office transfer completing is not proof the car is clean), book a pre-purchase inspection at a licensing station, and anchor the price with carlistprice.mot.gov.il adjusted for ownership type, previous owners, kilometrage, structural change and import path. If a pledge exists, the sale is not dead but it cannot be registered until the lender releases it. Warn the buyer that an operating-lease car is owned by the leasing company.

### Example 3: "Someone asked for a photo of my vehicle licence before viewing the car"

This is the documented identity-theft pattern behind the July-2026 fraud-blocking service. Tell the user not to send it, to switch on the post-office transfer block in the government personal area, and to do any real sale through the personal area where both parties authenticate.

### Example 4: "My car has been sitting dead in the yard for two years"

The licence fee has been accruing against them the whole time. Route to **ביטול רישום** (deregistration), warn that it is blocked by any lien, pledge, customs restriction or 7A/8A debt, and that the pro-rata fee from the licence expiry to the cancellation date is payable if the vehicle was never placed in deposit status. Do not promise a scrappage grant; there is no current government scheme.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Ministry of Transport fee board | https://www.gov.il/he/pages/drivers-car-license-fee-boards | Annual licence fee by group and year, transfer fees, special-category and reservist rates |
| Licensing-station tariffs 2026 | https://www.gov.il/he/pages/2026-licensing-institute-rates | Test and retest prices by vehicle type (price-controlled order) |
| Ownership transfer service | https://www.gov.il/he/service/ownership-vehicles-transfer | Transfer, transfer cancellation, adding or removing a co-owner, transfer after death |
| Deregistration service | https://www.gov.il/he/service/request_to_cancel_vehicle_registration | Who may deregister, what blocks it, pro-rata fee on a lapsed licence |
| Fraud-blocking announcement | https://www.gov.il/he/pages/news-27_07_26 | The post-office transfer block and the scam pattern it addresses |
| Vehicle licence renewal | https://www.gov.il/he/service/car_licence_renewal | Who must renew, the six-month cycle for an old vehicle, recall block, payment channels |
| Licence deposit and cancellation of deposit | https://www.gov.il/he/service/request_to_deposit_vehicle_license | Taking a vehicle off the road temporarily |
| Reduced licence fee or fee refund | https://www.gov.il/he/service/exemptions_from_vehicle_license_fee | Disability badge, theft, deposited licence, vehicle handed for dismantling |
| Disabled parking badge | https://www.gov.il/he/service/disability_parking_badge | Application for a tav niche |
| Israeli Vehicle Insurance Pool | https://pool.org.il/ | Buying mandatory insurance when insurers refuse |
| Registrar of Pledges (רשם המשכונות) | Ministry of Justice online services. Search by name; the gov.il service slug has been renumbered and old bookmarks 404 | Authoritative search for a pledge on a vehicle |
| MOT official car pricelist | https://carlistprice.mot.gov.il/ | Reference value for a used car and the transfer-fee base |

Ministry of Transport call centre: 4515* (from abroad +972-3-9695678), Sunday to Thursday 07:00-20:00, Friday and holiday eves 07:00-13:00.

## Bundled Resources

### references/

- `test-preparation.md` -- Checklist for passing the annual vehicle test
- `ownership-transfer.md` -- Step-by-step guide for buying/selling a car in Israel, including fraud blocking, encumbered vehicles, inheritance, and how quickly the transfer must be registered
- `license-fee-table.md` -- Full April-2026 annual licence fee table (7 groups x 4 year bands), motorcycle and special-category rates, reservist discount, and the test/retest tariff

### scripts/

- `test-reminder.py` -- Days until (or past) the next test. Pass `--expiry-date YYYY-MM-DD` from the licence, which is authoritative; `--reg-date` is a labelled estimate. Reports OVERDUE with the matching penalty band. Standard library only

## Troubleshooting

### "My car failed the test (טסט)"
Failures are common. Get the failure report, fix the listed issues at any garage, and return for a retest. Common quick fixes: replace burned bulbs, add safety equipment, inflate spare tire, replace worn wipers.

### "I bought a car and discovered it has a lien"
First separate the two instruments, because the skill's own sources use them loosely: an עיקול is an attachment imposed in enforcement proceedings, while a שעבוד / משכון is a consensual pledge registered at the Registrar of Pledges. Which one you are facing changes where it is registered and how it is cleared.

A registered pledge is generally enforceable against the vehicle rather than against whoever owned it at the time, which is why the register matters. **Do not tell the buyer the car is lost.** A good-faith purchaser defence exists under the pledges law and whether it applies turns on the specific facts, including what was registered when and what the buyer checked. That question is for a lawyer, and it is the reason to consult one rather than a formality. Prevention remains far cheaper: search the Registrar of Pledges before paying.

### "My registration expired and I got fined"
Pay the fine and renew as soon as possible. The penalty is graduated: up to 4 months expired = 250 NIS + 6 license points; 4 months to 1 year = 1,000 NIS + 6 points; over 1 year = a court summons (which can carry a higher fine and license suspension). These amounts come from a secondary legal source stated as of 2023 and are not confirmed against the primary set-fine schedule, so treat them as the shape of the exposure rather than an exact quote, and read the amount off the notice itself. What is certain is that there is no grace period: even one day expired is an offence. From about four months past expiry the renewal is done at the Penalties Collection Center rather than online.

### "I want to sell my car but the buyer is not Israeli"
If one or both parties are not Israeli citizens, the transfer must be done at a licensing bureau (misrad harishui), not online or at the post office. Bring both IDs and the current vehicle license.
