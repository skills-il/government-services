---
name: israeli-returning-resident-navigator
description: >-
  Process navigator for Israelis returning home (תושב חוזר / toshav chozer) after years abroad.
  Use when a user asks about coming back to Israel after working overseas, "חזרתי לארץ",
  "אני תושב חוזר", "ביטוח לאומי לתושב חוזר", "האם אני תושב חוזר ותיק", restoring kupat cholim,
  Form 628, reactivating an Israeli driver's license, the toshav-chozer certificate from
  Misrad HaAliyah V'HaKlita, or the order of operations in the first 90 days back.
  Disambiguates the three independent eligibility tracks (Misrad HaAliyah 2-year threshold,
  Mas Hachnasa 6-year regular / 10-year vatik, Bituach Leumi center-of-life via Form 628).
  Do NOT use for new immigrants (olim chadashim, use israeli-aliyah-navigator), Israelis
  leaving Israel (use israeli-relocation-abroad), Section 14 tax math or Form 1348 drafting
  (use israeli-toshav-chozer-vatik-tax-planner), vehicle import or household-shipment customs
  (use israeli-returning-resident-customs-vehicle), or binding tax / legal advice.
license: MIT
---

# Israeli Returning Resident Navigator

## Problem

Israelis returning home after years abroad get routinely confused with olim chadashim, and AI agents make this mistake even more often: they quote oleh sal-klita figures, conflate the 6-year and 10-year tax tracks, or assume Bituach Leumi residency is automatic. The result is missed customs windows, surprise BL debt, longer-than-needed kupat cholim waiting periods, and lost retroactive benefits. Three independent agencies (Misrad HaAliyah V'HaKlita, Mas Hachnasa, Bituach Leumi) decide three independent questions on three different timelines, and this skill walks the returnee through each one in the right order.

## Instructions

### Step 1: Disambiguate before answering

Always separate the three eligibility questions before quoting numbers. The thresholds are NOT interchangeable:

- **Misrad HaAliyah V'HaKlita certificate** ("תעודת תושב חוזר"), the gate-key for ministry assistance and customs. Threshold: at least 2 years abroad for an Israeli citizen aged 17+ at return, who did not visit Israel for more than 4 months in any single year during the last 2 years before return. Returning scientists and business entrepreneurs need at least 5 years abroad, with the visits-test applied over 5 years for scientists and 3 years for entrepreneurs (source: gov.il "Who is a Returning Resident", updated 27.10.2024).
- **Mas Hachnasa tax basket**, threshold is years as a *foreign tax resident*, not years physically abroad. 6 consecutive years for the regular returnee basket; 10 consecutive years for the vatik (long-term) basket with Section 14 ten-year exemption (source: kolzchut "תושב חוזר").
- **Bituach Leumi residency**, decided independently by Form 628 ("שאלון לקביעת תושבות") on a center-of-life test, not by counting years (source: btl.gov.il toshavChozer landing).

If the user asks "am I a toshav chozer?", reply with all three answers, labelled by agency. Do not collapse them.

### Step 1.5: Special tracks (scientists, entrepreneurs, preferred-country list)

Before running the decision tree, ask whether any of these apply:

- **Returning scientist / academic researcher**: eligible for assistance from the Center for Integration in Science following at least 5 years abroad (source: gov.il "Who is a Returning Resident", same page).
- **Business entrepreneur**: eligible following at least 5 years abroad, with the visits-test applied over 3 years rather than 2 (source: same gov.il page).
- **Preferred-country / shorter Misrad HaAliyah track via BL**: someone abroad 5 years or more can apply for residency through Misrad HaAliyah on a shorter (מקוצר) track (source: btl.gov.il "קביעת תושבות לתושב חוזר", https://www.btl.gov.il/Audience/toshavChozer/Pages/kviattoshavut.aspx). Verify the current list at the gov.il Misrad HaAliyah page at answer time; do not invent country names.

### Step 2: Run the eligibility decision tree

Walk the user through `references/eligibility-decision-tree.md`. Or, if running locally, hand them `scripts/check-eligibility.py`:

```bash
python3 scripts/check-eligibility.py \
  --years-abroad 8 \
  --foreign-tax-resident yes \
  --israeli-citizen yes \
  --age-at-return 35 \
  --visited-over-4mo-any-year no \
  --emissary no \
  --prev-returnee-assistance no
```

The script prints one paragraph per agency and links to the source page for each threshold. It is a routing aid, never a substitute for legal/tax advice.

### Step 3: Misrad HaAliyah V'HaKlita registration

1. Apply online at https://www.gov.il/he/service/application_for_recognition_as_returning_resident . Two paths: "זכאות עקרונית" (principle check) or "מעמד תושב חוזר" (status request).
2. Outcome: a "תעודת תושב חוזר" certificate. The local Misrad HaAliyah office (find via gov.il branch finder) issues it after reviewing passport entry/exit stamps and Misrad HaPnim records.
3. Phone the service center on \*2994 or 03-9733333 (Sun-Thu 8:00-18:00, languages: Hebrew, Russian, English, French, Spanish, Amharic). WhatsApp: https://wa.me/972733972114 .
4. Windows that start the day the user returns to Israel: ministry assistance = 24 months; assured income (havtachat hachnasa) = 12 months; customs = 9 months (see sister customs skill).
5. Benefit basket flagged by the certificate (eligibility per category is confirmed at the local Misrad HaAliyah office): reduced taxes on household-goods imports, business start-up assistance, income-tax benefits (handed off to the tax-planner skill), **Acclimatization Year ("שנת הסתגלות" / Shnat Histaglut)**, employment and professional retraining support, education and childcare assistance, and **discounted El Al airfares with expanded luggage allowance** for the qualifying return flight. The "Acclimatization Year" is a *tax-residency election* with its own deadline (Section 14(b) + Form 1130, must be filed within 90 days of arrival); for the tax mechanics route the user to `israeli-toshav-chozer-vatik-tax-planner`. The El Al benefit is booked through the airline's returning-resident channel before purchasing the flight, not retroactively.

### Step 3.5: Children born abroad, register at Misrad HaPnim first

Israeli-citizen children born outside Israel must be registered at Misrad HaPnim (רישום לידת חוץ) BEFORE Bituach Leumi or any kupat cholim flow can be opened for them. Without a Misrad HaPnim record there is no Israeli ID number, and BL cannot open a residency case. Confirm the current form name at the local Misrad HaPnim branch or at gov.il at answer time; do not invent a form number.

### Step 4: Bituach Leumi re-classification

1. Submit Form 628 ("שאלון לקביעת תושבות לתושב חוזר") at any BL branch, or through the personal online area. Bring passport with entry/exit stamps, foreign tax returns or work permits, lease/mortgage to demonstrate center of life. Form 628 can be filed by a representative with power-of-attorney (ייפוי כוח), useful for returnees still finishing a job transition abroad (operational note, confirm with the branch).
2. If the user did not pay BL contributions while abroad, BL may demand back-payment ("רצף ביטוחי" continuity); have the user ask explicitly at the branch before submitting.
3. After recognition, the following benefits are NOT available on day one and only kick in after accumulated work periods: maternity allowance, unemployment (dmei avtala), employer insolvency. Source: kolzchut "דמי ביטוח לאומי לתושבים חוזרים" (updated 03.03.2025).
4. BL phone: \*6050 (Israel) or 04-8812345 (landing page). The international-callers line is +972-8-936-9669, Sun-Thu 8:00-15:00, service in Hebrew, English, and Russian (source: https://www.btl.gov.il/snifim/mokdimrashi/Pages/abroad.aspx).

### Step 5: Kupat cholim re-enrollment and the waiting period

1. The choice of kupah (Clalit / Maccabi / Meuhedet / Leumit) is made on the BL registration form, together with residency determination.
2. Waiting period for health services = 1 month per year of absence, minimum 2 months (חודשיים) for anyone abroad 12+ months, maximum 6 months (source: kolzchut "הצטרפות תושב חוזר לביטוח בריאות", updated 15.01.2026).
3. Definitions to quote precisely: "year of absence" = 12-month period with 183+ days outside Israel; "waiting month" = 25 consecutive days of residence in Israel (trips abroad shorter than 25 days don't count toward completing the waiting period).
4. **Pidyon** (waiting-period redemption): 16,860 NIS in 2026, one-time or up to 6 equal installments. Even during the waiting period the returnee pays health insurance premiums based on income.
5. If the returnee has urgent medical needs in month 1, the pidyon usually pays for itself fast; if not, riding out the waiting period and carrying private travel medical insurance for the gap is the cheaper path.

### Step 6: Driver's license

1. Expired Israeli license: book a Misrad HaRishui appointment with proof of driving abroad (foreign license, insurance records). Usually no driving test required.
2. Foreign license only: convert within 5 years of return. The foreign license must be a permanent license issued at least 6 months before entering Israel, AND the holder must have at least 5 years of driving experience on it. Source: kolzchut "המרת רישיון נהיגה זר לרישיון נהיגה ישראלי".

### Step 7: Family, children and Hebrew

1. Returnee children may qualify for partial gan/preschool fee assistance in the first year back. Verify with the local municipality's חינוך department on arrival; the specifics depend on the locality (source: kolzchut "תושבים חוזרים" landing, updated 08.05.2026).
2. Hebrew: digital Hebrew learning resources from Misrad HaAliyah for returnees and their children, plus local ulpan options. The Misrad HaAliyah service center (\*2994) can point users to the current program names.
3. **Important: returnees do NOT receive the full oleh-chadash Sal Klita grant.** Misrad HaAliyah benefits for returnees are partial absorption support. Do not promise sal-klita figures from the aliyah world.
4. **Returnees aged 17-28 who left Israel as minors must coordinate with Meitav** (the IDF recruitment authority) on arrival. Unresolved military-service obligations can block license issuance, passport renewal, and other services. The user should contact Meitav directly to clarify status (operational note, confirm at the local Meitav office).

### Step 8: Pension and keren hishtalmut

1. The existing pension fund and keren hishtalmut accounts continue to exist. Contact the fund's customer service to confirm status. Pension funds may have re-activation rules that depend on the length of the contribution gap; the exact threshold (and whether a fresh enrolment is needed) is fund-specific, so call the fund's customer service for their rules.
2. Coordinate with a new Israeli employer: ensure new pension deposits go to the same fund where the rules permit, to maintain seniority. Detailed fund-by-fund rules are outside this skill, refer the user to the fund's service center or to `israeli-pension-advisor`.

### Step 9: Hand off the tax math

If the user starts asking about Section 14, Form 1348, the 10-year exemption, or the 2026 reporting-obligation change for vatikim: STOP and hand off to `israeli-toshav-chozer-vatik-tax-planner`. This skill flags which tax track they're in; it does not compute the tax.

### Step 10: Hand off customs / vehicle

If the user starts asking about household shipments, the 9-month customs window mechanics, Meches forms, or vehicle import quotas: hand off to `israeli-returning-resident-customs-vehicle`. This skill only flags the 9-month deadline.

## Examples

### Example 1: User confuses oleh and toshav chozer

User: "אני חוזר לישראל אחרי 12 שנה בקנדה. כמה כסף אקבל בסל קליטה?"

Actions:
1. Clarify: returnees do NOT get the oleh-chadash Sal Klita grant. Their benefit basket is different.
2. Identify the likely tax track (vatik, ≥ 10 years) and offer to hand the tax math to `israeli-toshav-chozer-vatik-tax-planner`.
3. List the actual returnee benefit categories: Misrad HaAliyah certificate (employment counselling, professional retraining, customs window), tax basket, BL re-classification, kupat cholim waiting period.

Result: user understands the right mental model and books an appointment at the local Misrad HaAliyah office.

### Example 2: Decision tree against a 3-year absence

User: "הייתי 3 שנים בברלין. אני תושב חוזר?"

Actions:
1. Run the three-branch check.
2. Branch 1 (Misrad HaAliyah): yes, 3 years ≥ 2, eligible for the certificate.
3. Branch 2 (Mas Hachnasa): no special returnee tax basket (3 < 6 years).
4. Branch 3 (BL): file Form 628 to re-establish residency; waiting period for health services likely 3 months.

Result: user submits the online Misrad HaAliyah form, calls BL on \*6050 to schedule Form 628 submission, decides to wait 3 months rather than pay the 16,860 NIS pidyon.

### Example 3: Family with school-age children returning mid-year

User: "אנחנו חוזרים בקיץ אחרי 7 שנים בבוסטון. ילדים בני 6 ו-9. מה הסדר?"

Actions:
1. Confirm Misrad HaAliyah eligibility (7 ≥ 2) and Mas Hachnasa track (7 in the 6-9 regular basket).
2. Week 1 list: address update at Misrad HaPnim, bank account, Misrad HaAliyah online application.
3. Children: register at the local municipality's חינוך department for the next school year; flag "דע עברית" if Hebrew has weakened.
4. Month 2: BL Form 628 (likely 6-month waiting period; consider pidyon if anyone in the family has chronic care needs).
5. Customs reminder: 9-month clock starts on entry day. Hand off to `israeli-returning-resident-customs-vehicle` if shipping containers or a car.

Result: user gets a sequenced checklist instead of guessing the order, and avoids missing the customs window.

## Bundled Resources

### References
- `references/domain-checklist.md`, Must-cover / Should-cover / Out-of-scope items with cited URLs. Consult before answering any returnee question.
- `references/eligibility-decision-tree.md`, three-branch decision tree (Misrad HaAliyah, Mas Hachnasa, BL). Consult to disambiguate eligibility.
- `references/first-90-days-checklist.md`, ordered list of agencies and steps for the first 90 days back. Consult when the user asks "what should I do first?".

### Scripts
- `scripts/check-eligibility.py`, CLI router that prints which of the three tracks a user likely qualifies for. Run: `python3 scripts/check-eligibility.py --help`. No tax math; sources cited inline.

## Recommended MCP Servers

None currently in the directory map cleanly to this domain. Misrad HaAliyah and Bituach Leumi do not currently publish public MCP endpoints. If/when an MCP wraps the gov.il personal area or BL contributor status, link it here.

## Gotchas

1. **Confusing oleh chadash with toshav chozer.** Returnees do NOT get the full Sal Klita basket and do NOT qualify under Chok HaShvut. Use `israeli-aliyah-navigator` for olim.
2. **Quoting "5 years" for the vatik tax exemption.** Vatik is 10 years, not 5. The 5-year figure is the regular returnee exemption on foreign passive income from assets bought while abroad. Different bracket, different math.
3. **Skipping the foreign-tax-resident requirement.** Mas Hachnasa benefits depend on having been a foreign *tax resident*, not just physically abroad. Someone who lived abroad but kept Israel as their center of life may not qualify for any tax basket.
4. **Promising children's Sal Klita.** Returnee children get partial absorption support (gan fee reduction in some municipalities, "דע עברית", absorption counselling) but NOT the olim grant set. Don't quote oleh figures.
5. **Forgetting Form 628 isn't automatic.** BL doesn't reclassify the returnee just because Misrad HaPnim updated the address. The Form 628 step is independent and gates the kupat cholim waiting-period clock.
6. **Missing the customs 9-month window.** It starts on the date of return. Even if the user came back to "look around", that's day zero. Hand off to `israeli-returning-resident-customs-vehicle` early.
7. **Quoting unverified phone hours or office addresses.** Always confirm against gov.il and btl.gov.il at answer time. Service-center hours change.
8. **Forgetting Meitav for returnees aged 17-28.** Anyone who left Israel as a minor must clear their IDF/Meitav status on return. An open obligation can block license issuance, passport renewal, and travel. Send them to Meitav before they walk into Misrad HaRishui.

## Reference Links

| Source | URL |
|---|---|
| Misrad HaAliyah, Who is a returning resident (EN) | https://www.gov.il/en/pages/returning_residents_whois |
| Misrad HaAliyah, Apply for returning-resident status (HE) | https://www.gov.il/he/service/application_for_recognition_as_returning_resident |
| Bituach Leumi, Returning residents landing | https://www.btl.gov.il/Audience/toshavChozer/Pages/default.aspx |
| Kol Zchut, Returning resident definition | https://www.kolzchut.org.il/he/%D7%AA%D7%95%D7%A9%D7%91_%D7%97%D7%95%D7%96%D7%A8 |
| Kol Zchut, BL contributions for returnees | https://www.kolzchut.org.il/he/%D7%93%D7%9E%D7%99_%D7%91%D7%99%D7%98%D7%95%D7%97_%D7%9C%D7%90%D7%95%D7%9E%D7%99_%D7%9C%D7%AA%D7%95%D7%A9%D7%91%D7%99%D7%9D_%D7%97%D7%95%D7%96%D7%A8%D7%99%D7%9D |
| Kol Zchut, Joining kupat cholim as returnee | https://www.kolzchut.org.il/he/%D7%94%D7%A6%D7%98%D7%A8%D7%A4%D7%95%D7%AA_%D7%AA%D7%95%D7%A9%D7%91_%D7%97%D7%95%D7%96%D7%A8_%D7%9C%D7%91%D7%99%D7%98%D7%95%D7%97_%D7%91%D7%A8%D7%99%D7%90%D7%95%D7%AA |
| Shivat Zion, Toshav Chozer overview (EN) | https://shivatzion-support.freshdesk.com/en/support/solutions/articles/501000348813-returning-resident-toshav-chozer |
| Shivat Zion, Acclimatization Year (EN) | https://shivatzion-support.freshdesk.com/en/support/solutions/articles/501000348784 |
| Shivat Zion, Returning Israelis knowledge base root | https://shivatzion-support.freshdesk.com/en/support/solutions/501000223548 |

## Troubleshooting

### "BL is asking for back-payment of dmei bituach for years I was abroad."
Cause: someone who was classified as an Israeli resident for BL purposes while abroad (e.g., kept paying contributions, or BL never deregistered the user) may owe back-contributions plus interest.
Solution: ask BL to provide a written "דרישת חוב" with breakdown by year. Negotiate via the BL branch or with a lawyer specialising in BL appeals; pidyon-like installment payment plans exist.

### "My foreign driver's license is from a country not on the conversion list."
Cause: the Israeli conversion regime depends on bilateral arrangements. Some licenses convert without test; others require theory + practical.
Solution: check the Misrad HaTachbura conversion-by-country list and, if no conversion path, plan for a full Israeli test.

### "I returned, applied for the certificate, and Misrad HaAliyah said I'm not eligible because I visited Israel 5 months in year X."
Cause: the 4-months-per-year-in-the-last-2-years rule was tripped.
Solution: appeal with documentation (work obligations, family events). If the appeal fails, the user is still an Israeli resident for BL and Mas Hachnasa purposes; only the ministry-services certificate is blocked. The other two branches are independent.

### "I'm vatik and people online say I don't have to report anything."
Cause: that was true historically. As of returns/settlements on or after 01.01.2026, vatik retains the tax exemption but loses the reporting exemption; full disclosure of foreign assets and income to Mas Hachnasa is now required.
Solution: hand off to `israeli-toshav-chozer-vatik-tax-planner` for the actual reporting forms and timelines.
