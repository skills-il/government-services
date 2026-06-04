#!/usr/bin/env python3
"""
verdict_template.py - scaffold a fact-check verdict for an Israeli public claim.

This script produces STRUCTURE ONLY. It never invents a figure. It prints the
verdict scale, a fillable verdict skeleton, and a best-guess routing hint for
which official source can settle the claim. The agent must pull the real figure
from that source (MCP tool or official page) and fill the skeleton. If no source
confirms the figure, the verdict stays "אין מספיק נתונים".

Usage:
    python verdict_template.py                       # print the scale + an empty skeleton
    python verdict_template.py "claim text here"     # also print a routing hint
    python verdict_template.py --scale               # print only the verdict scale
"""

import sys

VERDICT_SCALE = [
    ("נכון", "The statement is true in its near-entirety."),
    ("לא מדויק", "Substantial parts of the statement are wrong."),
    ("מטעה", "Creates a false impression or takes facts out of context, even if a raw number is technically correct."),
    ("לא נכון", "The statement is false."),
    ("לשיפוטכם", "Too complex for a single definitive score. Lay out the data and let the reader judge."),
    ("אין מספיק נתונים", "No authoritative source confirms or refutes it. The anti-fabrication fallback, not a failure."),
]

MEDIA_LABELS = [
    ("עבר שינוי", "Edited or synthesized image, audio, or video."),
    ("לא נכון חלקית", "Contains some factual inaccuracies."),
    ("חסר הקשר", "Implies a false claim without stating it outright."),
    ("סאטירה", "Irony, exaggeration, or absurdity, not literal."),
]

# Keyword to source routing. Keys are matched against the claim text (Hebrew and
# English). Each value is (source name, MCP slugs, what to check).
ROUTES = [
    (["אינפלציה", "מדד", "מחיר", "יוקר", "cpi", "inflation", "price", "cost of living"],
     "Central Bureau of Statistics (CBS)", "israel-statistics / israeli-cbs",
     "CPI / price index for the right month, year-over-year vs month-over-month, base year."),
    (["תקציב", "הוצאה", "מכרז", "הקצאה", "budget", "spending", "procurement", "subsidy"],
     "BudgetKey / OpenBudget", "budgetkey / il-budget",
     "Executed budget (ביצוע), not the original plan (תקציב מקורי)."),
    (["דולר", "שער", "שקל", "מטבע", "exchange", "shekel", "dollar", "euro", "currency"],
     "Bank of Israel representative rate", "boi-exchange",
     "Official representative rate (שער יציג) for the correct date, not a market spot rate."),
    (["חוק", "הצעת חוק", "ועדה", "כנסת", "knesset", "bill", "committee", "legislation"],
     "Knesset ParliamentInfo OData", "knesset",
     "Bill status and committee data. Per-MK plenum votes are NOT here, use the Knesset plenum-votes dataset on data.gov.il (הצבעות חברי הכנסת במליאה)."),
    (["בחירות", "מנדט", "אחוז הצבעה", "מצביעים", "election", "turnout", "seats", "votes"],
     "Central Elections Committee (data.gov.il)", "israel-elections",
     "Official final results, not exit polls. Turnout denominator is eligible voters."),
    (["דירה", "נדל", "מחיר דיור", "שכירות", "apartment", "housing", "real estate", "rent"],
     "CBS House Price Index + Nadlan recorded deals", "nadlan",
     "Recorded sold prices, not asking prices. National trend uses the CBS index."),
    (["עמותה", "תרומה", "מימון זר", "amuta", "ngo", "donation", "foreign funding"],
     "Ministry of Justice Corporations Authority", "israel-amutot",
     "Disclosure threshold and known under-reporting. Absence of a report is not proof."),
    (["אבטלה", "שכר", "תעסוקה", "unemployment", "wage", "salary", "employment"],
     "CBS labour-force survey + Bituach Leumi", "israel-statistics",
     "CBS survey unemployment is not the Sherut HaTaasuka registered count."),
]


def print_scale():
    print("Verdict scale (The Whistle / המשרוקית):")
    for label, desc in VERDICT_SCALE:
        print(f"  {label:<18} {desc}")
    print("\nFor manipulated image / audio / video, platform labels also apply:")
    for label, desc in MEDIA_LABELS:
        print(f"  {label:<18} {desc}")


def route(claim: str):
    low = claim.lower()
    hits = []
    for keywords, source, mcp, check in ROUTES:
        if any(k.lower() in low for k in keywords):
            hits.append((source, mcp, check))
    if not hits:
        print("Routing hint: no keyword match. Use data.gov.il (CKAN) as the catch-all,")
        print("or read references/source-map.md to pick the source by hand.")
        return
    print("Routing hint (verify, do not trust blindly):")
    for source, mcp, check in hits:
        print(f"  Source: {source}")
        print(f"  MCP:    {mcp}")
        print(f"  Check:  {check}")


def skeleton(claim: str):
    shown = claim if claim else "<the claim as stated, one line>"
    print("\nFill this skeleton ONLY with a figure you actually pulled this session:")
    print("-" * 60)
    print(f"טענה: {shown}")
    print("פסיקה: <one label from the scale above>")
    print("מה הנתונים מראים: <the authoritative figure, quoted verbatim>")
    print("מקור: <source name>, <dataset / page>, <reference period>, נמשך ב-<date>")
    print("הערת הקשר: <one line if context changes the picture, else omit>")
    print("-" * 60)
    print("If you could not pull a confirming figure, the verdict is: אין מספיק נתונים")


def main():
    args = [a for a in sys.argv[1:]]
    if "--scale" in args:
        print_scale()
        return
    claim = " ".join(a for a in args if not a.startswith("--")).strip()
    print_scale()
    if claim:
        print()
        route(claim)
    skeleton(claim)


if __name__ == "__main__":
    main()
