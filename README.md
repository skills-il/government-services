# Government Services Skills

AI agent skills for Israeli government APIs, public services, and civic data.

Part of [Skills IL](https://github.com/skills-il) — curated AI agent skills for Israeli developers.

## Skills

| Skill | Description | Scripts | References |
|-------|-------------|---------|------------|
| [israel-gov-api](./israel-gov-api/) | Query Israeli government open data from data.gov.il (CKAN API). Transportation, education, health, geography, economy datasets. | `query_datagov.py` | 1 |
| [israeli-address-autocomplete](./israeli-address-autocomplete/) | Format, validate, and geocode Israeli addresses. Postal code (mikud) lookup and CBS city code resolution. | `lookup_address.py` | 1 |
| [israeli-bituach-leumi](./israeli-bituach-leumi/) | National Insurance benefits, eligibility, and contributions. 15+ programs: retirement, unemployment, maternity, disability. | `calculate_benefits.py` | 1 |
| [israeli-company-lookup](./israeli-company-lookup/) | Israeli company search and business entity types. Rasham HaChevarot integration, Ltd/amuta/partnership comparison. | `search_company.py` | 1 |
| [israeli-drug-database](./israeli-drug-database/) | Israeli pharmaceutical database: drug info, health basket coverage, generic alternatives, pricing, prescription requirements. | `lookup_drug.py` | 1 |
| [israeli-education-system](./israeli-education-system/) | Bagrut exams, psychometric test (PET), university admissions, sekhem calculator, school data. | `calculate_sekhem.py` | 1 |
| [israeli-election-data](./israeli-election-data/) | Knesset API: MK info, voting records, legislative bills, committees, parties, coalition data, election results. | `query_knesset.py` | 1 |
| [israeli-gov-form-automator](./israeli-gov-form-automator/) | Playwright browser automation for gov.il portals. PDF form filling, Teudat Zehut validation, Rashut HaMisim and Bituach Leumi forms. | `fill_form.py` | 1 |
| [israeli-health-data](./israeli-health-data/) | Health fund comparison (Clalit, Maccabi, Meuhedet, Leumit), patient rights, health basket (sal briut) coverage. | `compare_health_funds.py` | 1 |
| [israeli-land-tenders](./israeli-land-tenders/) | Israel Land Authority (RMI) tender search, land allocation guidance, bid process navigation, lottery (hagralah). | `search_tenders.py` | 1 |
| [israeli-public-transit](./israeli-public-transit/) | Bus, train, and light rail routing. Real-time arrivals, Rav-Kav fares, Shabbat schedules. Egged, Dan, Israel Railways. | `check_transit.py` | 1 |
| [israeli-real-estate](./israeli-real-estate/) | Israeli property data, mas rechisha (purchase tax) calculator, Tabu extracts, and rental agreement guidance. | `calculate_mas_rechisha.py` | 1 |
| [israeli-statistics](./israeli-statistics/) | CBS (Central Bureau of Statistics) data: CPI, housing price indices, GDP, unemployment, demographics. | `fetch_cbs_data.py` | 1 |
| [knesset-legislative-tracker](./knesset-legislative-tracker/) | Knesset Open Data API: bill tracking, committee sessions, MK voting records, tech-sector legislation alerts. | `fetch_knesset.py` | 1 |

## Install

```bash
# Claude Code - install a specific skill
claude install github:skills-il/government-services/israeli-bituach-leumi

# Or clone the full repo
git clone https://github.com/skills-il/government-services.git
```

## Contributing

See the org-level [Contributing Guide](https://github.com/skills-il/.github/blob/main/CONTRIBUTING.md).

## License

MIT

---

Built with care in Israel.
