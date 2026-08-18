# The 6 Permitted Pre-5-Year Withdrawal Purposes (Deep Dive)

Statutory source (verbatim from hachvana.mod.gov.il/GrantAndDeposit):

> "לימודים אקדמיים, הכשרה מקצועית, נישואין, הקמת עסק, לימודי נהיגה ורכישת דירה, בית או קרקע לבניית בית"

Translation: "academic studies, vocational training, marriage, starting a business, driving lessons, and purchasing an apartment, house, or land for building a house"

**Closed list.** Any purpose not in this list is rejected automatically by the hachvana system pre-5y. The most common rejection is rental, only purchase qualifies.

---

## Purpose 1: Academic Studies (לימודים אקדמיים)

**Definition.** Tuition at a recognized academic institution. Verify recognition (e.g., for the Israeli higher-education framework) and for abroad studies verify with Mishrad HaChinuch before withdrawing.

**Evidence required:**
- Acceptance letter (מכתב קבלה) from the institution
- Tuition invoice (חשבון שכר לימוד) or proof of registration for the relevant academic year
- For abroad studies: verify recognition status before submitting

**Pikadon stacking with Mimadim LiLimudim scholarship.** If the user is also eligible for Mimadim (under Tikkun 25 December 2023, 100% tuition for lochem and special populations), the Pikadon can be used for living, dorm, and book expenses NOT covered by the scholarship.

**Common rejection causes (verify with hachvana before assuming):**
- Pre-academic preparation (mechina), kolzchut lists mechina kdam-akademit as eligible under purpose #1 when recognized; do not blanket-reject. Verify recognition for the specific mechina.
- Yeshiva / kollel, typically not eligible as academic studies; verify with hachvana.
- "Bonus" non-degree single-course audits at universities, verify case-by-case.

---

## Purpose 2: Vocational / Professional Training (הכשרה מקצועית)

**Definition.** Course/program from a recognized vocational provider that leads to an occupation. Hachvana publishes a catalog of MoD-recognized hachshara mikzo'i programs (cyber, programming, mechanics, electricians, paramedics, accounting trainee, real-estate broker training, etc.).

**Evidence required:**
- Course registration confirmation from a recognized provider
- Payment receipt (the Pikadon will reimburse against actual paid expenses)

**MoD subsidy stacking.** Many vocational courses are partially subsidized by hachvana directly (a substantial portion of course cost depending on track). Pikadon can cover the remaining user contribution. Verify the exact subsidy band on hachvana.mod.gov.il for each course before assuming a specific coverage level.

**Common rejection causes:**
- Hobby courses (cooking, photography for personal use), not recognized as professional training
- Online courses from unrecognized providers (random Udemy courses), must be MoD-recognized provider

---

## Purpose 3: Driving Lessons (לימודי נהיגה)

**Definition.** Lessons toward a driver's license (rishyon nehiga) at a licensed instructor/driving school.

**Evidence required:**
- Receipts from the licensed teacher or driving school

**Practical notes:**
- No documented public minimum number of lessons threshold
- Includes both manual and automatic license tracks
- Test fees may or may not be eligible, verify with hachvana before submitting

---

## Purpose 4: Starting / Investing in a Business (הקמת עסק)

**Definition.** Capital expenditure to establish a new business OR substantial investment in an existing business owned by the discharged soldier.

**Evidence required:**
- Osek Patur or Osek Murshe registration certificate
- Itemized business setup expenses: equipment, lease deposit, registration fees, professional services (accountant, lawyer setup)
- Business plan or proof of operation (optional but speeds approval)

**Reference:** For Osek registration and freelancer setup, route the user to `israeli-freelancer-ops`.

**Common rejection causes:**
- "Pay myself a salary", Pikadon cannot be withdrawn as personal income to the business owner
- Stock investments / crypto / passive investment, not "starting a business"
- Buying inventory for resale without a registered business, register Osek first

---

## Purpose 5: Marriage (נישואין)

**Definition.** Wedding expenses for the discharged soldier's own marriage.

**Evidence required:** EITHER:
- Teudat Nisuin (marriage certificate), if already married
- Wedding hall contract + vendor receipts (catering, photographer, band, dress, etc.), if pre-wedding

**Practical notes:**
- Works pre- or post-wedding within the 5-year window
- Both partners can each withdraw from their own Pikadon (each has their own deposit)
- For co-purchased first apartments specifically, each partner can withdraw their Pikadon against their share of the purchase, combining Pikadonim for a down payment is a common newlywed pattern
- Common-law partnership (yeduim be'tzibur): verify documentation requirements with hachvana

---

## Purpose 6: Apartment / House / Land Purchase (רכישת דירה / בית / קרקע לבניית בית)

**Definition.** Purchase of residential real estate OR land for building a residence. **Rental is explicitly NOT included.**

**Evidence required:**
- Signed purchase agreement (חוזה רכישה חתום), not a draft or "expression of interest"
- For land purchase: deed/registration showing intent for residential construction

**Common rejection causes (most user mistakes):**
- Rental contract (chozeh schirut), REJECTED. Rental is not a permitted purpose
- Commercial property purchase, only residential qualifies
- Co-buying with a non-relative, verify ownership structure with hachvana

**Mortgage interaction:**
- Pikadon can be used as part of the down payment (mashkanta first-payment)
- Note: Mishrad HaShikun also offers veteran mortgage discount points based on weighted scoring including service, route to `israeli-mortgage-comparator` + future `israeli-real-estate` for the mortgage side
- This skill does NOT model mortgage math

---

## Summary table

| # | Hebrew | English | Key evidence | Most common mistake |
|---|---|---|---|---|
| 1 | לימודים אקדמיים | Academic studies | Acceptance + tuition invoice | Yeshiva / non-MALAG institution |
| 2 | הכשרה מקצועית | Vocational training | Course registration + receipt | Hobby course / non-recognized provider |
| 3 | לימודי נהיגה | Driving lessons | Driving school receipts | (Few rejection cases) |
| 4 | הקמת עסק | Starting a business | Osek registration + expenses | Treating as personal income |
| 5 | נישואין | Marriage | Teudat Nisuin OR vendor receipts | (Few rejection cases) |
| 6 | רכישת דירה/בית/קרקע | Real estate purchase | Signed purchase agreement | **Trying to use for rental** |

If the user has a purpose NOT in this list, the options are: (a) wait for the 5-year auto-transfer (any use), (b) use the unrestricted discharge grant instead, or (c) re-frame the expense as one of the 6 (e.g., enrolling in studies to free other cash for the actual need).
