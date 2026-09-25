# Troubleshooting

### Error: "Not enough qualifying months"
Cause: insufficient contribution history (תקופת אכשרה).
Solution: check the per-program qualifying-period table in `references/benefit-programs.md`. Military service, maternity leave and miluim count as qualifying months. Olim have special rules; for old-age the 60-month minimum can be waived via מענק מותנה.

### Error: "Benefit amounts don't match expected values"
Cause: BTL reissues benefit amounts each 1 January, and individual tables are sometimes reissued mid-year (the long-term-care income test was reissued effective 1 April 2026).
Solution: Verify against the current benefits circular at https://www.btl.gov.il/Publications/benefits_update/Pages/default.aspx (the January 2026 edition is `Documents/hozerkizba2026.pdf`), against the specific benefit page, or via *6050. Amounts in this skill follow the January 2026 circular.

### Error: "Form not found at the URL I tried"
Cause: the forms path uses a SPACE, not a hyphen. The hyphenated form 404s; the live path is `btl.gov.il/טפסים ואישורים/...` (encoded `%20`).
Solution: use the form-search at https://www.btl.gov.il/טפסים%20ואישורים/FormSearch/Pages/default.aspx. PDF originals are at `btl.gov.il/טפסים%20ואישורים/Documents/T<form-number>.pdf` (e.g. `T355.pdf`).

### Error: "I resigned and was denied unemployment"
Cause: after a voluntary resignation, unemployment is paid only from 90 days after leaving work. It is a delay, not a loss of the entitlement.
Solution: if the resignation was for a justified cause (see the list in `references/benefit-programs.md`), payment starts from the first registration day; attach documents proving the cause. The end of a fixed-term contract is not a resignation at all. If the claim is still rejected, appeal to the regional labour court within 12 months of the written decision (a request to a claims committee, where available, does not extend that deadline). Form 7810 is NOT this route: it is the ערר form for a medical diagnosis, incapacity degree or dependence level. Document the cause carefully.
