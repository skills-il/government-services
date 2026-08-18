# Eligibility Decision Tree

Three independent agencies decide three independent questions. Run the user through each branch separately, do not collapse them.

## Branch 1 - Misrad HaAliyah V'HaKlita ("תעודת תושב חוזר")

This is the certificate that unlocks ministry assistance (absorption services, Hebrew programs, employment counseling, customs window opens here).

```
Is the user a returning scientist / academic researcher / business entrepreneur?
├── Yes → use the 5-year residence threshold (scientists and entrepreneurs both need ≥ 5 years abroad).
│         Visits-test applies over 5 years for scientists, 3 years for entrepreneurs.
└── No  → use the standard 2-year residence threshold; visits-test applies over the last 2 years.

Standard track:
Israeli citizen, age 17+ at return?
├── No  → not eligible
└── Yes → Lived abroad continuously for at least 2 years (5 for scientists/entrepreneurs)?
          ├── No  → not eligible for Misrad HaAliyah certificate (other branches may still apply)
          └── Yes → In the visits window (2 / 3 / 5 years per the question above), visited Israel no more than 4 months in any single year?
                    ├── No  → likely ineligible; ministry will examine center-of-life
                    └── Yes → Was absence as an emissary of the State / WZO / Jewish Agency / JNF / Keren HaYesod / UJA / Israel Bonds?
                              ├── Yes, and less than 5 years since end of mission → not eligible
                              └── No (or 5+ years post-mission)            → Did you ever receive returnee assistance before?
                                                                              ├── Yes, less than 10 years ago → not eligible
                                                                              └── Otherwise                  → ELIGIBLE - apply at gov.il/he/service/application_for_recognition_as_returning_resident
```

Source: https://www.gov.il/en/pages/returning_residents_whois (updated 27.10.2024).

Notes:
- "Returning scientist" and "business entrepreneur" tracks need 5 years abroad, not 2; visits-test extends to 5 years (scientists) or 3 years (entrepreneurs) per the same gov.il source.
- Shorter (מקוצר) track via Misrad HaAliyah exists for users abroad 5 years or more; details on the BL kviattoshavut page (https://www.btl.gov.il/Audience/toshavChozer/Pages/kviattoshavut.aspx).
- Eligibility window for ministry services = 24 months from date of return. Assured income (havtachat hachnasa) = 12 months.

## Branch 2 - Mas Hachnasa (Tax Authority)

This decides which tax-benefit basket the returnee gets. Driven by years as a *foreign tax resident*, not by years physically abroad.

```
Years as a continuous foreign tax resident before return?
├── < 6 years  → no special returnee tax benefits (regular Israeli tax resident from re-entry day)
├── 6-9 years  → "תושב חוזר רגיל" - partial benefits (5-year exemption on foreign passive income from assets purchased while abroad; 10-year exemption on capital gains on those assets)
└── ≥ 10 years → "תושב חוזר ותיק" - full basket (Section 14 ten-year exemption on foreign income and capital gains; near-oleh-chadash treatment)
```

Sources:
- https://www.kolzchut.org.il/he/%D7%AA%D7%95%D7%A9%D7%91_%D7%97%D7%95%D7%96%D7%A8 (definitions)
- https://www.kolzchut.org.il/he/%D7%94%D7%98%D7%91%D7%95%D7%AA_%D7%91%D7%9E%D7%A1_%D7%9C%D7%AA%D7%95%D7%A9%D7%91%D7%99%D7%9D_%D7%97%D7%95%D7%96%D7%A8%D7%99%D7%9D_%D7%A9%D7%A9%D7%94%D7%95_%D7%91%D7%97%D7%95%22%D7%9C_%D7%9E%D7%A2%D7%9C_10_%D7%A9%D7%A0%D7%99%D7%9D

Hard handoff: numerical tax math, Form 1348 drafting, and the 2026 reporting-obligation change live in the sister skill `israeli-toshav-chozer-vatik-tax-planner`. This skill only flags which track the user is in.

Historical note: a temporary 6-year-equals-vatik Hora'at Sha'ah track existed for those who returned during the temporary-order window that closed at the end of 2009. It was not extended. Anyone returning today on the "vatik" basket needs 10 years. (Exact start year of the Hora'at Sha'ah varies in different secondary write-ups; confirm at answer time before quoting a date range.)

## Branch 3 - Bituach Leumi (BL residency)

BL decides residency by center-of-life via Form 628 ("שאלון לקביעת תושבות"), not by counting years.

```
Filed Form 628 at a BL branch (or via personal online area)?
├── No  → file it; until then you are not formally a BL resident
└── Yes → BL determines residency based on family, home, employment, social ties
          ├── Recognized as resident   → re-classification effective; waiting period for health services starts
          └── Not recognized            → can re-file with additional evidence
```

Source: https://www.btl.gov.il/Audience/toshavChozer/Pages/default.aspx ; https://www.kolzchut.org.il/he/%D7%93%D7%9E%D7%99_%D7%91%D7%99%D7%98%D7%95%D7%97_%D7%9C%D7%90%D7%95%D7%9E%D7%99_%D7%9C%D7%AA%D7%95%D7%A9%D7%91%D7%99%D7%9D_%D7%97%D7%95%D7%96%D7%A8%D7%99%D7%9D.

Once recognized:
- Health-services waiting period = 1 month per year of absence (minimum 2 months for anyone abroad 12+ months, maximum 6 months).
- Pidyon (redemption) = 16,860 NIS in 2026, payable in one shot or up to 6 installments.
- Benefits unavailable on day one: maternity allowance, unemployment (dmei avtala), employer insolvency. These need accumulated work periods after recognition.

## Decision summary

A returnee can fall in different brackets across the three branches. Examples:
- 3 years abroad: eligible for Misrad HaAliyah certificate (≥ 2 years), no Mas Hachnasa returnee benefits (< 6 years), BL residency restored on Form 628.
- 8 years abroad: eligible everywhere; gets "regular" tax benefits (6-9 year basket).
- 12 years abroad: eligible everywhere; gets "vatik" tax basket (≥ 10 years).
