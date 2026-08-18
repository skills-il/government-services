# CBS Data Guide

## Central Bureau of Statistics (CBS)
- URL: https://www.cbs.gov.il
- English: https://www.cbs.gov.il/en
- Price Indices API (canonical for economic series): https://api.cbs.gov.il/index
- Data portal: data.gov.il (organization: lamas)

## Where the data lives
- **Price and economic time series** (CPI, housing prices, producer prices, building input costs) come from the **CBS Price Indices API** at `api.cbs.gov.il/index`. List all indices: `api.cbs.gov.il/index/catalog/catalog?format=json`. Fetch one series: `api.cbs.gov.il/index/data/price?id={mainCode}&format=json` (CPI is code `120010`, apartment prices `40010`, producer prices `170030`, residential building input `200010`, commercial building input `800010`, paving and bridging input `240010`, agricultural input `260010`). Choose the code the contract itself names: a construction contract indexed to the CPI rather than to a building-input index tracks a different series entirely.
- **data.gov.il organization `lamas`** hosts a small set of CBS datasets (census tabulations, localities, traffic accidents). It does **NOT** host the CPI / GDP / unemployment time series. Use the `lamas` slug (not `cbs`) when searching data.gov.il.
- GDP, unemployment, population, and foreign-trade series are published as CBS tables at `cbs.gov.il` and are not all exposed via a public API.

## Publication Schedule
| Indicator | Frequency | Typical Release |
|-----------|-----------|-----------------|
| CPI | Monthly | 15th of following month, 18:30; moved to the preceding Friday / holiday eve at 14:00 when the 15th is a Friday, Saturday, holiday, or holiday eve |
| Housing Price Index | Monthly | 2-3 months after the reference month (plus a richer quarterly transactions report). In mid-August 2026 the latest published month was May 2026 |
| GDP | Quarterly | ~6 weeks after quarter |
| Unemployment | Monthly | ~4 weeks after month |
| Population | Annual | Mid-year |
| Building starts | Monthly | ~6 weeks after month |
| Foreign trade | Monthly | ~4 weeks after month |

## CPI Components
The CPI basket is split into consumption groups: housing (rents), transportation, food, education and culture, health, furniture and household, clothing and footwear, and miscellaneous. CBS re-sets and republishes the weight of each group with the index, so never quote a weight from memory. The Price Indices API does NOT carry the weights: its catalog endpoint returns only chapter names and index codes. Take the current breakdown from the CBS publications reached via the Main Price Indices hub (https://www.cbs.gov.il/en/Pages/Main%20Price%20Indices.aspx). If you cannot find a weight there, say so rather than supplying a number.

## Rent Adjustment Formula
```
New Rent = Old Rent * (Current CPI / CPI at contract signing)
```

## Table Number Reference
| Subject | Tables | Description |
|---------|--------|-------------|
| Population | 2.x | Size, demographics |
| Migration | 4.x | Immigration, emigration |
| Prices | 12.x | CPI, housing, PPI |
| Labor | 12.x | Employment, wages |
| National accounts | 16.x | GDP, growth |
| Construction | 19.x | Building activity |
| Foreign trade | 16.x | Exports, imports |
