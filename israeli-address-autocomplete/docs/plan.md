# Israeli Address Autocomplete Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for Israeli address formatting, validation, and geocoding using government data sources.

**Architecture:** Document/Asset Creation skill. Embeds Israeli address structure knowledge, city/street databases, and postal code mapping.

**Tech Stack:** SKILL.md, Python validation script, government address data references.

---

## Research

### Israeli Address System
- **Structure:** Street (rechov) + Number + City (ir/yishuv) + Postal Code (mikud)
- **Hebrew vs English:** Official addresses in Hebrew, transliteration varies
- **Postal codes:** 7 digits since 2013 (formerly 5)
- **Data sources:**
  - Israel Post: `https://www.israelpost.co.il` (postal code lookup)
  - CBS settlement list: Official list of all Israeli settlements/cities with codes
  - data.gov.il: Various address datasets
  - Google Maps Geocoding API: Supports Israeli addresses

### City/Settlement Codes
- CBS maintains official list of ~1,300 settlements (yishuvim)
- Each has a unique code (e.g., Tel Aviv = 5000, Jerusalem = 3000, Haifa = 4000)
- Important for government form filling and data joins

### Use Cases
1. **Format Israeli address** — Correct Hebrew address formatting
2. **Validate address** — Check if address exists (city + street + number)
3. **Postal code lookup** — Find 7-digit mikud for an address
4. **City code lookup** — Find CBS settlement code
5. **Address transliteration** — Hebrew to English and vice versa

---

## Build Steps

### Task 1: Create SKILL.md

```markdown
---
name: israeli-address-autocomplete
description: >-
  Format, validate, and geocode Israeli addresses including postal code (mikud)
  lookup and CBS city code resolution. Use when user asks about Israeli
  addresses, "ktovet", postal codes, "mikud", city codes, or needs to format
  addresses for Israeli forms and systems. Supports Hebrew address formatting
  and Hebrew-English transliteration. Do NOT use for non-Israeli addresses.
license: MIT
allowed-tools: "Bash(python:*) WebFetch"
compatibility: "Network access helpful for postal code and geocoding lookups."
metadata:
  author: skills-il
  version: 1.0.0
  category: government-services
  tags: [address, geocoding, postal-code, mikud, israel]
---

# Israeli Address Autocomplete

## Instructions

### Step 1: Parse Address Components
Israeli address format: `[Street Name] [Number], [City], [Postal Code]`
Hebrew: `[rechov] [mispar], [ir], [mikud]`

Example: rechov Rothschild 42, Tel Aviv-Yafo, 6688312

### Step 2: Validate Components
1. **City:** Check against CBS official settlement list (~1,300 entries)
2. **Street:** Verify street exists in the city (data.gov.il street database)
3. **Number:** Validate format (number, optional apartment/entrance)
4. **Postal code:** 7 digits, verify matches the address area

### Step 3: Lookup Missing Data
- **No postal code:** Look up via Israel Post website or reference data
- **No city code:** Look up in CBS settlement code table
- **No street:** Suggest closest matching streets in the city

### Step 4: Format Output
Provide address in:
- Hebrew (official format)
- English transliteration
- Structured data (JSON with components separated)

## Major City Codes Reference
| City | Hebrew | CBS Code | Area Code |
|------|--------|----------|-----------|
| Jerusalem | yerushalayim | 3000 | 02 |
| Tel Aviv-Yafo | tel aviv-yafo | 5000 | 03 |
| Haifa | haifa | 4000 | 04 |
| Rishon LeZion | rishon letzion | 8300 | 03 |
| Petah Tikva | petach tikva | 7900 | 03 |
| Ashdod | ashdod | 70 | 08 |
| Netanya | netanya | 7400 | 09 |
| Beer Sheva | beer sheva | 9000 | 08 |
| Holon | holon | 6600 | 03 |
| Bnei Brak | bnei brak | 6100 | 03 |

## Examples

### Example 1: Format Address
User says: "Format this address for a form: rothschild 42 tel aviv"
Result: Hebrew: rechov Rothschild 42, Tel Aviv-Yafo | Mikud: 6688312 | CBS Code: 5000

### Example 2: Find Postal Code
User says: "What's the mikud for Herzl 10, Haifa?"
Result: 7-digit postal code with area identification

## Troubleshooting

### Error: "Street not found"
Cause: Spelling variation or renamed street
Solution: Try common transliteration variants. Many streets have Hebrew-only official names.
```
