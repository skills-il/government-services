# CBS Data Guide

## Central Bureau of Statistics (CBS)
- URL: https://www.cbs.gov.il
- English: https://www.cbs.gov.il/en
- Price Indices API (canonical for economic series): https://api.cbs.gov.il/index
- Data portal: data.gov.il (organization: lamas)

## Where the data lives
- **Price and economic time series** (CPI, housing prices, producer prices, building input costs) come from the **CBS Price Indices API** at `api.cbs.gov.il/index`. List all indices: `api.cbs.gov.il/index/catalog/catalog?format=json`. Fetch one series: `api.cbs.gov.il/index/data/price?id=<mainCode>&format=json` (CPI is code `120010`, apartment prices `40010`, producer prices `170030`).
- **data.gov.il organization `lamas`** hosts a small set of CBS datasets (census tabulations, localities, traffic accidents). It does **NOT** host the CPI / GDP / unemployment time series. Use the `lamas` slug (not `cbs`) when searching data.gov.il.
- GDP, unemployment, population, and foreign-trade series are published as CBS tables at `cbs.gov.il` and are not all exposed via a public API.

## Publication Schedule
| Indicator | Frequency | Typical Release |
|-----------|-----------|-----------------|
| CPI | Monthly | ~15th of following month |
| Housing Price Index | Monthly | ~6 weeks after month (plus a richer quarterly transactions report) |
| GDP | Quarterly | ~6 weeks after quarter |
| Unemployment | Monthly | ~4 weeks after month |
| Population | Annual | Mid-year |
| Building starts | Monthly | ~6 weeks after month |
| Foreign trade | Monthly | ~4 weeks after month |

## CPI Components
| Component | Weight (~%) |
|-----------|-------------|
| Housing (rents) | 25% |
| Transportation | 17% |
| Food | 16% |
| Education and culture | 8% |
| Health | 6% |
| Furniture and household | 5% |
| Clothing and footwear | 3% |
| Other | 20% |

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
