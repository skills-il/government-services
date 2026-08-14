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
Cause: Voluntary resignation triggers a 90-day disqualification.
Solution: If the resignation was for justified cause (relocation following spouse, family-care, hazardous-conditions, deterioration of work conditions, fixed-term contract end), file an appeal with form 7810 within 60 days. Document the cause carefully.
