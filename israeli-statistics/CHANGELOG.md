# Changelog

## 1.3.0 - 2026-08-18

Reworked the snapshot from embedded values to fetch-always for every series the CBS API serves, so the fastest-moving figures can no longer go stale in the file. Corrected four stale or wrong figures: CPI now July 2026 (index 105.1, +0.3% monthly, +1.5% annual), unemployment 3.1% and participation 62.2% for July 2026 (both had been five months behind at February 2026), housing -1.5% year-on-year for May 2026, and full-year 2025 GDP growth 2.9%, which CBS had revised down from an initial 3.1% while the skill still carried 3.0%.

Removed a dead instruction: the skill and its script both told the agent to fetch CPI component weights from the API catalog endpoint, which returns only chapter names and index codes and has no weights at all. Replaced the broken data.gov.il browse link, whose /organization/ and /dataset routes now return AccessDenied, with the CKAN API path that still works.

Added the four input-cost index codes the catalog exposes but the skill never named (commercial building 800010, paving and bridging 240010, agriculture 260010, alongside residential 200010), because Israeli construction and infrastructure contracts are commonly linked to those rather than to the CPI, and pointed at the official CBS linkage calculator. Documented the exact CPI release rule including the Friday and holiday-eve exception that moves publication to 14:00. Rent guidance no longer asserts that a falling index means falling rent: it now requires reading the base-index definition and any floor clause first.

## 1.2.2 - 2026-08-11

Refreshed the CPI snapshot from April to June 2026 (annual 1.6%, monthly 0.0%, index 104.8 on the 2024 average base) against the CBS index API. The April figures were correct when written; they were simply two releases behind.

