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
    python verdict_template.py --help                # print this help
"""

import re
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

# Keyword to source routing. Each route is a dict:
#   strong:  keywords that fire the route on their own
#   weak:    keywords that fire it only together with a "context" keyword
#            (so "2 billion shekels" is a budget claim, not an exchange-rate one)
#   context: the words that make a weak keyword count
# Multi-word phrases are matched first. English keywords match whole words only
# (so "rent" does not match "current", "bill" does not match "billion", "post"
# does not match "post-war"). Hebrew keywords match a whole word, optionally
# with one or two one-letter prefixes (ו ה ב ל מ ש כ) and a plural, construct,
# or possessive suffix.
PROVENANCE = "PROVENANCE first (not a data lookup): see SKILL.md Step 3a"

ROUTES = [
    dict(strong=["צילום מסך", "ציוץ", "צייץ", "צייצה", "פוסט", "סרטון", "הקלטה", "דיפפייק", "זיוף",
                 "מזויף", "מזויפת", "באקס", "בטוויטר",
                 "screenshot", "tweet", "tweeted", "post", "posted", "video", "clip", "photo", "audio",
                 "deepfake", "ai-generated", "doctored", "twitter"],
         weak=["תמונה", "image"],
         context=["ויראלי", "ויראלית", "וואטסאפ", "פייסבוק", "אינסטגרם", "טיקטוק", "רשת",
                  "viral", "whatsapp", "facebook", "instagram", "tiktok", "fake"],
         source=PROVENANCE, mcp="none",
         check="Settle attribution and authenticity before any figure: prior checks (Google Fact Check Explorer, "
               "The Whistle, FakeReporter), the original post, Wayback / archive.today, reverse-image search on "
               "keyframes (Google Lens, TinEye, Yandex, Bing). No original and no capture means אין מספיק נתונים, "
               "not לא נכון."),
    dict(strong=["סקר", "סקרים", "poll", "polls", "survey of the public"],
         source="The original poll publication", mcp="none",
         check="Institute, sample and population, field dates, margin of error, exact question wording. "
               "Never rate a poll against official data."),
    dict(strong=["שכר דירה", "שכר הדירה", "שכירות", "rent", "rents", "rental"],
         source="CBS CPI rent component (שכר דירה)", mcp="israel-statistics",
         check="Rent is a CPI component. Nadlan and the House Price Index cover purchases, not leases."),
    dict(strong=["דירה", "דיור", "נדלן", "נדל\"ן", "מחירי הדירות", "מחירי דירות",
                 "apartment", "apartments", "housing", "real estate", "home prices", "house prices"],
         source="CBS House Price Index + Nadlan recorded deals", mcp="nadlan",
         check="Recorded sold prices, not asking prices. National trend uses the CBS index."),
    dict(strong=["אינפלציה", "מדד", "מחיר", "יוקר המחיה", "יוקר",
                 "cpi", "inflation", "price", "prices", "cost of living"],
         source="Central Bureau of Statistics (CBS)", mcp="israel-statistics / israeli-cbs",
         check="CPI for the right month, year-over-year vs month-over-month. Across a base change use the CBS "
               "calculator or the chained series, never raw index points."),
    dict(strong=["תקציב", "הוצאה", "הוציאה", "הוציא", "הוציאו", "מכרז", "הקצאה", "הקצתה", "תמיכה",
                 "budget", "spending", "spent", "spend", "procurement", "subsidy", "subsidies", "allocated"],
         source="BudgetKey / OpenBudget", mcp="budgetkey / il-budget",
         check="Executed budget (ביצוע), not the original plan (תקציב מקורי)."),
    dict(strong=["שער יציג", "שער חליפין", "שער הדולר", "שער השקל", "שער האירו",
                 "exchange rate", "exchange rates", "currency"],
         weak=["דולר", "אירו", "שקל", "dollar", "euro", "shekel"],
         context=["מול", "שער", "נחלש", "התחזק", "שיא", "against", "versus", "vs", "weakened",
                  "strengthened", "record", "low", "high"],
         source="Bank of Israel representative rate", mcp="boi-exchange",
         check="Official representative rate (שער יציג) for the correct date, not a market spot rate."),
    dict(strong=["ריבית בנק ישראל", "ריבית", "interest rate", "interest rates", "policy rate"],
         weak=["rates", "rate"],
         context=["bank of israel", "בנק ישראל", "interest", "policy", "monetary", "raised", "cut",
                  "hiked", "lowered"],
         source="Bank of Israel monetary policy (interest rate announcements)", mcp="none",
         check="Use the Monetary Committee decision in force on the date. A mortgage rate is not the policy rate."),
    dict(strong=["עוני", "עניים", "אי שוויון", "poverty", "poor families", "inequality"],
         source="Bituach Leumi annual poverty and income-inequality report", mcp="none",
         check="Persons vs families vs children; the survey year lags the publication year."),
    dict(strong=["מבקר המדינה", "דוח המבקר", "comptroller"],
         source="State Comptroller reports", mcp="none",
         check="Quote the specific report chapter and its year."),
    dict(strong=["תוצר", "צמיחה", "גירעון", "חוב לאומי", "החוב הלאומי",
                 "gdp", "economic growth", "deficit", "national debt", "public debt"],
         source="Not yet mapped in this skill: find the official publisher's own release", mcp="none",
         check="Never use a news summary as the source. Provisional vs revised; deficit in % of GDP vs shekels. "
               "If no official release is found, return אין מספיק נתונים."),
    dict(strong=["בחירות", "מנדט", "מנדטים", "אחוז הצבעה", "אחוז ההצבעה", "מצביעים", "קלפי",
                 "election", "elections", "turnout", "seats", "ballot"],
         source="Central Elections Committee (data.gov.il); local-authority elections: Ministry of Interior",
         mcp="israel-elections",
         check="Official final results, not exit polls. Turnout denominator is eligible voters."),
    dict(strong=["עמותה", "תרומה", "מימון זר", "ישות מדינית זרה",
                 "amuta", "ngo", "ngos", "nonprofit", "donation", "donations", "foreign funding", "foreign-funded"],
         source="Ministry of Justice Corporations Authority (GuideStar; data.gov.il moj-amutot)",
         mcp="israel-amutot",
         check="The MoJ foreign-state-entity donations file covers state entities, not private foreign donors. "
               "Absence of a report is not proof. Party funding is the State Comptroller's regime."),
    dict(strong=["הצעת חוק", "חוק", "ועדה", "כנסת", "חבר כנסת", "חברי כנסת", "הצביע", "הצביעו", "מליאה",
                 "knesset", "bill", "bills", "committee", "legislation", "voted", "mk", "mks", "plenum"],
         source="Knesset OData (ParliamentInfo for bills and committees; OData V4 for plenum votes)",
         mcp="knesset",
         check="Per-MK plenum votes: OData V4 KNS_PlenumVote + KNS_PlenumVoteResult. נוכח is not a vote, and no "
               "row is not 'voted against'. The data.gov.il package הצבעות חברי הכנסת במליאה has no data files."),
    dict(strong=["אבטלה", "מובטלים", "שכר", "משכורת", "משכורות", "תעסוקה",
                 "unemployment", "unemployed", "wage", "wages", "salary", "salaries", "employment"],
         source="CBS labour-force survey (unemployment) / CBS average wage + Bituach Leumi (wages)",
         mcp="israel-statistics",
         check="CBS survey unemployment is not the Sherut HaTaasuka registered count. For wages, state the "
               "definition (per person or per job, average or median)."),
    dict(strong=["פשיעה", "רצח", "נרצחו", "אלימות", "crime", "murder", "murders", "homicide",
                 "תאונות דרכים", "הרוגים", "road deaths", "accidents",
                 "אוכלוסייה", "תושבים", "הגירה", "עולים חדשים", "העולים החדשים", "עלייה לישראל", "population", "immigration", "immigrants",
                 "בריאות", "תמותה", "health", "mortality", "vaccination",
                 "פיזה", "בגרות", "pisa", "bagrut", "רכבים", "vehicles", "cars"],
         source="See references/source-map.md (Police / CBS / PIBA / Ministry of Health / Education / Transport)",
         mcp="data-gov-il / israel-vehicles",
         check="Read the per-source pitfalls in source-map.md: definitions and denominators differ by source."),
]

HEB_PREFIXES = "והבלמשכ"
HEB_SUFFIXES = ("", "ים", "ות", "ה", "ת", "י", "ו", "ם", "ן", "ך", "נו")
# Words that look like a keyword after prefix stripping but mean something else.
HEB_FALSE_FRIENDS = {"משקל", "רחוק", "מחוק", "חוקר", "חוקרים", "נמדד", "שערוריה", "שערוריית",
                     "חובת", "חובה", "שכרון", "סקרן", "סקרנים", "סקרנות", "סקרנית"}
# Phrases removed before matching because they contain a keyword in another sense.
PHRASE_EXCLUSIONS = ["תמונת המצב", "תמונת מצב", "post-war", "post war", "postwar", "jerusalem post",
                     "washington post", "post office", "סקר כוח אדם",
                     "labour-force survey", "labor force survey"]


def _is_hebrew(word: str) -> bool:
    return any("\u0590" <= ch <= "\u05ff" for ch in word)


def _heb_token_matches(token: str, stem: str) -> bool:
    if token in HEB_FALSE_FRIENDS:
        return False
    for cut in range(0, 3):
        head, body = token[:cut], token[cut:]
        if any(c not in HEB_PREFIXES for c in head):
            break
        if body in HEB_FALSE_FRIENDS:
            return False
        for suf in HEB_SUFFIXES:
            if body == stem + suf:
                return True
            # Construct state of feminine nouns: עמותה -> עמותות / עמותת
            if stem.endswith("ה") and body == stem[:-1] + "ות" + suf.lstrip("ות"):
                return True
            if stem.endswith("ה") and body == stem[:-1] + "ת":
                return True
    return False


def _count_hits(text: str, keywords):
    """Return how many keywords match, consuming multi-word phrases first."""
    low = text.lower()
    hits = 0
    for kw in sorted(keywords, key=len, reverse=True):
        k = kw.lower()
        if " " in k or "-" in k:
            if _is_hebrew(k):
                found = k in low
            else:
                found = re.search(r"(?<![a-z0-9-])" + re.escape(k) + r"(?![a-z0-9-])", low) is not None
            if found:
                hits += 1
                low = low.replace(k, " ")
            continue
        if _is_hebrew(k):
            tokens = re.findall(r"[\u0590-\u05ff\"']+", low)
            if any(_heb_token_matches(t.strip("\"'"), k) for t in tokens):
                hits += 1
        elif re.search(r"(?<![a-z0-9-])" + re.escape(k) + r"(?![a-z0-9-])", low):
            hits += 1
    return hits


def print_scale():
    print("Verdict scale (The Whistle / המשרוקית):")
    for label, desc in VERDICT_SCALE:
        print(f"  {label:<18} {desc}")
    print("\nFor manipulated image / audio / video, platform labels also apply:")
    for label, desc in MEDIA_LABELS:
        print(f"  {label:<18} {desc}")


def _route_hits(text: str, route: dict) -> int:
    n = _count_hits(text, route["strong"])
    if route.get("weak") and _count_hits(text, route.get("context", [])):
        n += _count_hits(text, route["weak"])
    return n


def route(claim: str):
    text = claim.lower()
    for ph in PHRASE_EXCLUSIONS:
        text = text.replace(ph.lower(), " ")
    all_phrases = {ph.lower() for r in ROUTES for ph in r["strong"] if " " in ph}
    scored = []
    for order, r in enumerate(ROUTES):
        # Remove phrases that belong to OTHER routes, so "שכר דירה" (rent) is
        # not also read as "שכר" (wage).
        own = {k.lower() for k in r["strong"]}
        t = text
        for ph in sorted(all_phrases - own, key=len, reverse=True):
            t = t.replace(ph, " ")
        n = _route_hits(t, r)
        if n:
            # A screenshot or video is always settled first, whatever else matches.
            first = 0 if r["source"] == PROVENANCE else 1
            scored.append((first, -n, order, r))
    if not scored:
        print("Routing hint: no keyword match. Use data.gov.il (CKAN) as the catch-all,")
        print("or read references/source-map.md to pick the source by hand.")
        return
    scored.sort(key=lambda x: x[:3])
    print("Routing hint (verify, do not trust blindly; PRIMARY = settle this first):")
    for i, (_, _, _, r) in enumerate(scored):
        tag = "PRIMARY" if i == 0 else "also"
        print(f"  [{tag}] Source: {r['source']}")
        print(f"          MCP:    {r['mcp']}")
        print(f"          Check:  {r['check']}")


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


KNOWN_FLAGS = {"--scale", "--help", "-h"}


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print(__doc__)
        return
    if "--scale" in args:
        print_scale()
        return
    claim = " ".join(a for a in args if a not in KNOWN_FLAGS).strip()
    print_scale()
    if claim:
        print()
        route(claim)
    skeleton(claim)


if __name__ == "__main__":
    main()
