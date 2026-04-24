---
name: israeli-relocation-abroad
description: "End-to-end guide for Israelis relocating abroad for work (רילוקיישן), covering before, during, and after the move plus return planning. Use when user asks about Israeli relocation, moving abroad from Israel, yom nituk toshavut, Israeli tax residency while abroad, Bituach Leumi from abroad, kupat cholim during relocation, toshav chozer (returning resident) benefits, vehicle import on return, or apostille for Israeli documents. Covers Israeli tax residency tests (Form 1348), Bituach Leumi continuity, kupat cholim, pension funds and keren hishtalmut, Israeli apartment rental vs sale, apostille via the Foreign Ministry, and the 10-year tax exemption for toshav chozer vatik. Prevents costly mistakes like losing kupat cholim on return, paying double Bituach Leumi, or missing returning-resident benefits. Do NOT use for aliyah to Israel (use israeli-aliyah-navigator), tourist visas, binding tax advice, or destination-country immigration like H-1B or UK Skilled Worker visas."
license: MIT
---

# Israeli Relocation Abroad Navigator

## Problem

Israelis relocating abroad for work (רילוקיישן) face a tangled web of Israeli regulations that follow them across borders: Bituach Leumi contributions, kupat cholim continuity, tax residency status, pension funds, and apartment rental tax. Most relocation packages ignore the Israeli side entirely, and decisions made (or missed) in the first 90 days often cost thousands of shekels and trigger a waiting period on health coverage when the family eventually returns. This skill gives a personalized, phased checklist so nothing falls through the cracks.

## Instructions

### Step 1: Assess the Relocation Situation

Before giving guidance, gather the facts that drive every downstream recommendation.

| Factor | Why it matters |
|--------|----------------|
| Stage (pre-move, just moved, living abroad X years, planning return) | Determines which phase of the checklist applies |
| Destination country | Treaty vs non-treaty affects Bituach Leumi exemption and double taxation |
| Family status and ages | Affects apartment rental strategy and school record apostille needs |
| Intended duration (2 years, 5 years, permanent) | Drives whether to stay a tax resident or cut residency (nituk toshavut) |
| Employer type (Israeli employer sending you, foreign employer hiring you, self-employed) | Determines tax residency, payroll, and pension treatment |
| Owned apartment in Israel | Triggers rental vs sell decision and Israeli landlord tax choice |

Once you have those, generate a personalized phased plan:

```bash
python scripts/relocation-checklist.py --stage pre_move --destination usa --duration 4y --owns_apartment yes
```

### Step 2: Tax Residency Determination

This is the most consequential decision. Israeli tax residency is tested by **days** and by **center of life**, independently of citizenship.

**Days test (presumption of Israeli residency):**
- 183+ days in Israel in the tax year, OR
- 30+ days in Israel in the tax year AND 425+ days total over that year plus the two preceding years

**Center of life test:** Even if you fail the days test one way or the other, the Tax Authority looks at where your family, home, work, social ties, and economic interests are. This can override the days count in either direction.

**Form 1348 (Residency Declaration):** If you meet the days test but claim your center of life is abroad, you must file Form 1348 with your annual return. The Tax Authority decides whether to accept the claim. Getting a "ruling" (pre-approved status) from the Tax Authority avoids surprises later.

**Key choices:**

| Strategy | When it fits | Implication |
|----------|--------------|-------------|
| Stay an Israeli tax resident | Short relocation (<3 years), plan to return, Israeli employer | Report worldwide income in Israel, claim foreign tax credit |
| Cut residency (nituk toshavut) | Long or open-ended move, foreign employer, family moves with you | No Israeli tax on foreign income, but lose toshav chozer benefits unless you stay out 6+ years (toshav chozer) or 10+ years (toshav chozer vatik) |

Run `scripts/residency-check.py` to walk through the decision with the user's specifics. The script is a guidance tool, not a legal opinion -- always recommend a tax advisor (yo'etz mas) for the final call.

### Step 3: Pre-Move Financial Checklist

Two to three months before the flight is the right window for most of this.

**Bituach Leumi (National Insurance) and health insurance:**

An Israeli who stays a tax resident must keep paying Bituach Leumi and health insurance (dmei briut) while abroad, even with zero income. This is how you keep continuous kupat cholim coverage and avoid a waiting period on return.

- Contribution rates on reported income abroad: 7% National Insurance + 5% health insurance (on amounts above the reduced-rate ceiling, lower rates below)
- **2026 minimums (Bituach Leumi, effective 01.01.2026):**
  - Non-treaty country, no income: ₪266/month combined (NI + health)
  - Treaty country (USA, UK, most of EU, Canada), paying social security locally: ₪123/month (health only)
- Open a standing order (horaat keva) before leaving so payments don't lapse
- In countries with a bilateral social security agreement (USA, UK, most of EU, Canada), if you pay social security there on employment income, you are exempt from Israeli NI on that income and pay only the ₪123/month Israeli health insurance

If you formally cut residency (nituk toshavut), you stop paying Bituach Leumi but you also lose kupat cholim and restart a waiting period when you return (see Step 6).

**Kupat cholim continuity:** The practical rule: keep paying Bituach Leumi = your kupat cholim membership stays active and you can resume care on any visit or return. Do not "cancel" your kupat cholim. Notify them of the foreign address so correspondence still reaches you.

**Pension funds and keren hishtalmut:**

| Instrument | Options while abroad | What most people do |
|-----------|---------------------|---------------------|
| Comprehensive pension fund (pensia mekifa) | Freeze (no contributions), self-pay at minimum, withdraw (heavy tax penalty) | Freeze the fund. Contributions stop, accumulated balance keeps investing |
| Keren hishtalmut | Continue via new Israeli employer contribution (rare abroad), freeze, or withdraw after 6 years | Freeze. Do not withdraw early -- triggers 47% tax |
| Kupat gemel / finance | Freeze | Same |

For all three, confirm in writing with the fund that the policy is frozen, not cancelled. Ask whether management fees continue on the frozen balance (some funds charge, some don't).

**Banking:**
- Notify your Israeli bank you are moving abroad. They will tag the account for FATCA/CRS reporting to your destination country's tax authority
- Request a power of attorney (yipui koach) template in case you need a family member to handle a transfer while you are away
- Keep at least one Israeli debit or credit card active -- many government portals only accept Israeli cards for payment

### Step 4: Pre-Move Administrative Checklist

**Apostille on documents at the Foreign Ministry:**

For any Israeli public document you may need abroad (marriage certificate, birth certificates, academic diplomas, criminal record extract), get an apostille stamp. The confusing part: different documents go to different places.

| Document type | Apostille authority | Location |
|---------------|--------------------|----------|
| Interior Ministry documents (birth, marriage, divorce, death certificates) | Ministry of Foreign Affairs, Authentication Branch | Yitzhak Rabin Blvd 9, Kiryat HaLeom, Jerusalem |
| Court orders and rulings | Court secretariat | Any court in Israel |
| Notarized translations | Court secretariat | Any court in Israel |
| University diplomas | First notarize and translate, then court secretariat for the notarization | Any court |

Court-issued apostille stamps cost **41 NIS per stamp** (updated 01.01.2026, was ₪35 through 2025). Budget for one per language per document (translations often need their own apostille).

**Driver's license:** Apply for an International Driving Permit (IDP, rishayon binleumi) at a MEMSI office before leaving. It is valid for 1 year and is required on top of your Israeli license in most countries.

**Israeli apartment (if owned or rented):**

| Situation | Main considerations |
|-----------|---------------------|
| Own an apartment, decide to rent it out | Choose Israeli landlord tax track: the 10% flat-rate track (mislul 10%) with no deductions, or the ordinary progressive track with deductions. Most expats pick the 10% track for simplicity. Sign a property management agreement (revenue-only or full management) |
| Own and decide to sell | Get a mas shevach (betterment tax) estimate before listing; expat sellers may still qualify for single-home exemption |
| Rent from a landlord and leave mid-lease | Check the lease for early-exit clause. Standard Israeli leases allow a mofe (substitute tenant) but require landlord approval |

**Employer exit (if Israeli employer):**
- Final payslip: confirm whether unused vacation (yimei chofesh) is paid out or carried (most companies pay out)
- **Tofes 161:** the severance/retirement form. Your employer files this when employment ends even if it is not retirement. You sign it to choose what happens with the pitzuim (severance) portion of your pension -- withdraw now with tax, or keep it inside the fund for tax deferral (ritza)
- Vested options / RSUs: confirm the exercise window post-termination (usually 90 days) and the tax treatment under Section 102 vs Section 3(i)
- Bonus clawback: read the contract. Some companies claw back a signing or retention bonus if you leave within X months

### Step 5: First-Year Abroad

**Tax year one (most complex year):** In the first calendar year abroad, you are usually a tax resident of both countries for part of the year. File in both, use tie-breaker rules in the relevant tax treaty, and claim the foreign tax credit to avoid double taxation. Start with a dual-qualified accountant before you sign anything.

**Bituach Leumi payment rhythm:** Log in quarterly at btl.gov.il to confirm payments went through. A missed year is not the end of the world, but requires catch-up payments and produces a "hole" in coverage.

**Israeli voting:** Israel does not offer absentee voting for regular citizens abroad. You must be in Israel on election day to vote (with very narrow exceptions for diplomatic staff). Plan accordingly around Knesset elections.

**Stay reachable to Israeli government systems:**
- Keep an active Israeli phone number on a cheap prepaid plan. Many .gov.il portals send OTP codes to Israeli mobile numbers only
- Keep your personal area (ezor ishi) password on btl.gov.il and mas.gov.il up to date
- Register a forwarding address with Doar Israel if you expect paper mail

### Step 6: Return Planning (Toshav Chozer)

If you stayed out long enough and did not maintain Israeli tax residency, Israeli law gives you meaningful benefits on return.

**Two tiers of returning resident:**

| Status | Definition | Main benefit |
|--------|------------|-------------|
| Toshav Chozer (regular) | Foreign resident 6+ consecutive years | 5-year exemption from tax on foreign-source passive income (interest, dividends, royalties, pensions) and 10 years on specific foreign financial assets |
| Toshav Chozer Vatik (veteran) | Foreign resident 10+ consecutive years | 10-year exemption from Israeli tax on all foreign-source income and gains from foreign assets -- under Section 14 of the Income Tax Ordinance. Same treatment as a new immigrant |

**2026 change to reporting:** For anyone becoming an Israeli resident from January 1, 2026 onward, the 10-year exemption from reporting foreign income and assets was repealed. The tax exemption itself is unchanged -- you still pay no Israeli tax on foreign income during the 10 years -- but you must now file an annual return disclosing it. People who became residents before January 1, 2026 keep both exemptions.

**Customs and belongings:**
- Household goods and personal effects can be imported duty-free as a returning resident, subject to "personal use, not commercial" quantity limits
- **Vehicle:** A toshav chozer may personally import a vehicle manufactured up to 48 months before import (regular residents are capped at 24 months), within 9 months of entering Israel. There is no tax exemption on the vehicle itself -- you pay full purchase tax and VAT -- only the age limit is relaxed
- Consult `references/toshav-chozer-customs.md` for the full quantity rules

**Kupat cholim waiting period:** If you cut residency and stopped paying Bituach Leumi, returning to Israel triggers a waiting period before kupat cholim coverage resumes (2 months per year of absence, up to 6 months max). You can buy a redemption (pidyon) to cancel the wait -- a one-time payment equal to 12 minimum monthly contributions. This is the biggest argument for keeping up Bituach Leumi even when abroad: avoid the return waiting period.

## Examples

### Example 1: Tech Worker Relocating to the Bay Area for 4 Years

User says: "I got an offer at a US tech company, moving to San Francisco in 3 months with my wife and 2 kids. What do I need to do?"

Actions:
1. Gather situation: destination USA (treaty country), duration 4 years, family of 4, Israeli-owned 4-room apartment in Ramat Gan, pension fund at Menora Mivtachim
2. Residency decision: 4 years is borderline. Since kids are with them and there is no clear Israeli home, recommend considering formal nituk toshavut and documenting it (will qualify as regular toshav chozer on return at year 6+). Flag the Form 1348 option if they keep ties
3. Generate pre-move checklist: Bituach Leumi continuation via standing order if staying resident, or formal exit if cutting; apartment rental with 10% landlord tax track; apostille on marriage and children's birth certificates
4. Pension fund: freeze the comprehensive fund and keren hishtalmut, do not withdraw (withdrawal triggers ~47% tax)
5. School records: apostille teudat gmar for kids in case of re-enrollment abroad
6. Budget for relocation: apostille stamps ~164 NIS (marriage + 2 birth + 1 diploma at ₪41 each, 2026 rate), IDP 80 NIS, property management 5-8% of monthly rent

Result: 12-week phased checklist with financial estimates and a flagged decision point for tax residency to review with an accountant.

### Example 2: Already in London Two Years, Missing Bituach Leumi Payments

User says: "I moved to London in 2024 for a job, didn't set up anything with Bituach Leumi. My lawyer says I owe them money. What's the story?"

Actions:
1. Identify they remained Israeli tax resident (no Form 1348 filed, family stayed) -- so Bituach Leumi is owed
2. Explain the UK-Israel social security agreement: if they pay UK National Insurance on employment, they are exempt from Israeli NI on that income and owe only health insurance (123 NIS/month minimum in 2026)
3. Walk through catching up: log in at btl.gov.il, request a balance statement (ishur yitra), pay the outstanding health insurance for 2024-2025
4. Warn: unpaid health insurance produces a debt (chov) but does not necessarily trigger a kupat cholim waiting period as long as it is cleared. Past a certain debt, Bituach Leumi can pursue collection through chiyuv
5. Set up standing order for future months

Result: A quantified back-payment plan and a forward payment rhythm that keeps kupat cholim clean.

### Example 3: Returning After 6 Years in New York

User says: "We're moving back to Israel next summer after 6 years in New York. What benefits do I get and what do I need to prepare?"

Actions:
1. Confirm 6+ consecutive years abroad = regular toshav chozer (not yet vatik which needs 10+ years)
2. Explain 5-year exemption on foreign passive income (dividends, interest, royalties) and 10-year exemption on gains from specific foreign assets held prior to return
3. Customs: personal effects duty-free, vehicle import window 9 months from entry, vehicle may be up to 48 months old from manufacturing
4. **Critical:** if Bituach Leumi payments were stopped, plan the kupat cholim return. Compare two paths: (a) wait up to 6 months uninsured, with private bridge insurance, or (b) pay the redemption (pidyon) equal to 12 minimum contributions and get immediate coverage
5. Tax residency restart: file as Israeli resident from day of physical return. The 2026 reporting rule applies if the return date is January 1, 2026 or later
6. Schedule a session with a CPA who specializes in toshav chozer 2-3 months before return to claim benefits correctly

Result: A return plan with customs timeline, tax benefit claim list, and a decision on the kupat cholim redemption.

## Bundled Resources

### Scripts
- `scripts/relocation-checklist.py` -- Generates a phased checklist (pre-move, first 90 days abroad, ongoing, return) based on stage, destination, duration, and family situation. Run: `python scripts/relocation-checklist.py --help`
- `scripts/residency-check.py` -- Walks through the Israeli tax residency days test and center-of-life questions and outputs a status recommendation. Run: `python scripts/residency-check.py --help`

### References
- `references/bituach-leumi-abroad.md` -- Contribution rules for Israelis abroad: minimum payments, treaty country exemptions, standing order setup, catching up on missed payments
- `references/toshav-chozer-customs.md` -- Customs and vehicle import rules for returning residents: quantity limits on household goods, vehicle age window, paperwork sequence

## Recommended MCP Servers

Pair this skill with `data-gov-il` or `datagov-israel` MCP servers to pull live government form links, agency contact data, and open datasets from data.gov.il.

| MCP | When to use |
|-----|-------------|
| `data-gov-il` | Look up the current URL for Rashut HaMisim forms (1301, 1348) or Bituach Leumi forms when the user needs a direct link |
| `datagov-israel` | When charting Israeli cost-of-living or emigration statistics as context for a relocation decision |

Both MCPs are optional -- this skill works without them, but pairing gives live data.

## Gotchas

- Agents often assume an Israeli who leaves the country is automatically a non-resident for tax purposes. They are not -- residency is tested by days plus center of life, and requires an active declaration (Form 1348) to contest the presumption. The default for an Israeli on a 2-year relocation is "still a resident."
- Agents may confuse Bituach Leumi with kupat cholim. They are linked but separate: Bituach Leumi collects the health insurance tax that funds kupat cholim. Stopping Bituach Leumi payments is what triggers the kupat cholim waiting period on return, not "suspending" the kupat cholim itself.
- Apostille stamps come from the **Ministry of Foreign Affairs** (for Interior Ministry documents) or from court secretariats (for notarized documents), not from Misrad HaPnim (Interior Ministry). Agents frequently send users to the wrong place.
- The "10-year tax exemption" for toshav chozer vatik requires **10 consecutive years** as a foreign resident. Short visits back to Israel can break the count if the Tax Authority considers them substantial. Agents may quote the 10-year benefit without checking continuity.
- Toshav chozer vehicle import is not a tax exemption. Agents often claim "tax-free vehicle for returning residents" -- in fact the benefit is only a relaxed age window (48 months from manufacturing instead of 24), not a tax discount.
- The 2026 reporting rule (effective January 1, 2026) applies to who becomes a resident on or after that date. Agents may confuse this with the tax exemption itself, which is unchanged.

## Reference Links

| Source | URL | What to check |
|--------|-----|----------------|
| Bituach Leumi -- Israelis abroad | https://www.btl.gov.il/Insurance/Living_abroad/Pages/default.aspx | Current contribution rates and minimum health insurance amount |
| Kol-Zchut -- National insurance while abroad | https://www.kolzchut.org.il/he/%D7%93%D7%9E%D7%99_%D7%91%D7%99%D7%98%D7%95%D7%97_%D7%9C%D7%90%D7%95%D7%9E%D7%99_%D7%95%D7%93%D7%9E%D7%99_%D7%91%D7%99%D7%98%D7%95%D7%97_%D7%91%D7%A8%D7%99%D7%90%D7%95%D7%AA_%D7%9C%D7%AA%D7%95%D7%A9%D7%91_%D7%99%D7%A9%D7%A8%D7%90%D7%9C_%D7%94%D7%A9%D7%95%D7%94%D7%94_%D7%91%D7%97%D7%95%22%D7%9C | Payment procedure and treaty country exemptions |
| Kol-Zchut -- Returning resident benefits | https://www.kolzchut.org.il/he/%D7%AA%D7%95%D7%A9%D7%91%D7%99%D7%9D_%D7%97%D7%95%D7%96%D7%A8%D7%99%D7%9D | Toshav chozer and toshav chozer vatik eligibility and rights |
| PwC Tax Summaries -- Israel tax administration | https://taxsummaries.pwc.com/israel/individual/tax-administration | Annual filing process and Form 1301 details |
| PwC Tax Summaries -- Israel individual residence | https://taxsummaries.pwc.com/israel/individual/residence | Days test and center-of-life test details |
| Kol-Zchut -- Vehicle import for returning residents | https://www.kolzchut.org.il/he/%D7%99%D7%91%D7%95%D7%90_%D7%90%D7%99%D7%A9%D7%99_%D7%A9%D7%9C_%D7%A8%D7%9B%D7%91_%D7%9C%D7%AA%D7%95%D7%A9%D7%91%D7%99%D7%9D_%D7%95%D7%A1%D7%98%D7%95%D7%93%D7%A0%D7%98%D7%99%D7%9D_%D7%97%D7%95%D7%96%D7%A8%D7%99%D7%9D | Vehicle age limits and 9-month import window |

## Troubleshooting

### Error: "User wants to know if they are still an Israeli tax resident after 2 years abroad"
Cause: Ambiguous residency status; depends on days count and center of life, not just time abroad.
Solution: Walk through `scripts/residency-check.py` with the user's actual days in Israel and family/home situation. Flag whether Form 1348 is needed. Always recommend a qualified accountant for the final answer and consider requesting a Tax Authority ruling.

### Error: "Kupat cholim says there is a waiting period when trying to resume care on visit"
Cause: Bituach Leumi payments were stopped or not set up correctly during the relocation.
Solution: Log in at btl.gov.il, check the personal area (ezor ishi) for outstanding balance. Clear the debt. If the user formally cut residency, they may need to pay the redemption (pidyon) equal to 12 minimum contributions for immediate coverage on return.

### Error: "Need to apostille an Israeli birth certificate from abroad"
Cause: The user is no longer in Israel but needs an apostilled document.
Solution: Two paths -- (1) authorize a family member in Israel with power of attorney to get the document from Misrad HaPnim and the apostille from Misrad HaChutz, or (2) use a paid apostille service in Israel that handles end-to-end. Budget 41 NIS per court apostille (2026 rate) plus the service fee.

### Error: "Severance / pitzuim treatment at exit from Israeli employer is unclear"
Cause: User signed a Tofes 161 incorrectly or did not understand the ritza (tax deferral) option.
Solution: If still within the time window, contact the employer and the pension fund to correct the declaration. The choice is: withdraw pitzuim now and pay tax, or keep it in the fund for tax deferral until retirement. The right answer depends on career stage and cash needs abroad. Recommend an accountant who specializes in employment-related taxation.
