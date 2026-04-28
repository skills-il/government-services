# Red Track Yishuvim (§35 Border-Area Settlements)

The "red track" under section 35 of the Property Tax & Compensation Fund Law, 1961 (חוק מס רכוש וקרן פיצויים, תשכ"א-1961) covers indirect damage in `יישובי ספר` (border-area settlements). Businesses in red-track yishuvim get:

- No upper cap on the indirect-damage claim
- Direct profit losses are compensable, not just fixed costs and wages
- An advance payment of up to 100,000 NIS for March 2026 damages, available before the formal claim is finalized
- No minimum turnover-decline threshold (the 25% / 12.5% gate does not apply)

## Where the canonical list lives

The canonical, dynamically updated list of red-track yishuvim is maintained by the Israeli Tax Authority and published at:

https://www.gov.il/he/Departments/DynamicCollectors/compensation-tracks

The list shifts based on operational status - yishuvim are added when conflict reaches them and removed when the area is reclassified. Always verify against the live gov.il page before advising a user that their settlement is on the red list. The list as of mid-2026 covers most of the northern Galilee border strip and parts of the Gaza envelope (Otef Aza).

## How to check programmatically

The skill should NOT hard-code the yishuv list - it changes too often. Instead, surface the `compensation-tracks` URL to the user and have them confirm. If a more reliable check is needed, query Kol-Zchut at:

https://www.kolzchut.org.il - search for `יישוב ספר` or the specific yishuv name.

## Common northern red-track yishuvim (illustrative, not authoritative)

These are typically on the list during active northern conflict periods. Always verify on gov.il before relying on them:

- Shtula (שתולה)
- Manara (מנרה)
- Margaliot (מרגליות)
- Misgav Am (מסגב עם)
- Metulla (מטולה)
- Kfar Giladi (כפר גלעדי)
- Ma'ayan Baruch (מעיין ברוך)
- Kfar Yuval (כפר יובל)
- Yir'on (יראון)
- Avivim (אביבים)

## Gaza envelope (Otef Aza)

Within 7 km of the Gaza border, traditionally on the red list:

- Sderot (שדרות) - typically on the special-area or red track depending on regulation in force
- Netivot (נתיבות)
- Sha'ar HaNegev regional council yishuvim
- Eshkol regional council yishuvim
- Hof Ashkelon regional council yishuvim
- Sdot Negev regional council yishuvim

## Practical advice

If a user asks "am I on the red track?", do NOT rely on memory or this file. Tell them:

1. Open the live gov.il page at the URL above
2. Search for their yishuv by Hebrew name
3. If not found there, check kolzchut.org.il for confirmation
4. If still ambiguous, call the Tax Authority hotline at *4954 with their business address

Filing under the wrong track (red vs. nationwide) is a costly error. The red track's no-cap and no-floor benefits don't transfer to the nationwide track, so misclassification typically under-pays a true red-track business by 50%+ of the deserved grant.
