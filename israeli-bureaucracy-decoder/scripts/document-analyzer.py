#!/usr/bin/env python3
"""
Israeli Government Document Analyzer

Extracts structured information from Israeli government document text:
- Sending body identification
- Document type classification
- Required actions and deadlines
- Consequences of inaction
- Relevant laws and regulations

Usage:
    python document-analyzer.py --text "document text here"
    python document-analyzer.py --file path/to/document.txt
    python document-analyzer.py --file path/to/letter.pdf   (needs pdftotext)
    python document-analyzer.py --help
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import Optional


# Hebrew prefixes (ה, ו, ב, כ, ל, מ, ש) attach to the word, so a plain \b boundary
# misses "החוב" while a bare substring matches "חובה". hw() builds a pattern that
# allows up to two prefix letters and forbids any other Hebrew letter around it.
def hw(word: str) -> str:
    return rf"(?<![א-ת])(?:[הובכלמש]{{0,2}}){word}(?![א-ת])"


# --- Government body identification patterns ---

GOVERNMENT_BODIES = {
    "tax_authority": {
        "name_he": "רשות המסים בישראל",
        "name_en": "Israel Tax Authority",
        "patterns": [
            r"רשות המסים",
            r"מס הכנסה",
            r"פקיד שומה",
            r"אגף המכס",
            r"מע[\"״]מ",  # needs the quote: a bare "מעמ" is the start of "מעמד" (status)
            r"נציבות מס הכנסה",
        ],
        "ref_patterns": [
            r"תיק\s*\d{7,9}",
            r"שומה\s*מס['׳]?\s*\d+",
        ],
    },
    "national_insurance": {
        "name_he": "המוסד לביטוח לאומי",
        "name_en": "National Insurance Institute (Bituach Leumi)",
        "patterns": [
            r"ביטוח לאומי",
            r"המוסד לביטוח",
            r"ב[\"״]ל(?!\s*\d)",  # "ב\"ל 12345" is a Labour Court case number, not the sender
            r"btl\.gov\.il",
        ],
        "ref_patterns": [
            r"תביעה\s*מס['׳]?\s*\d+",
            r"בל/\d+",
        ],
    },
    "municipality": {
        "name_he": "עירייה / רשות מקומית",
        "name_en": "Municipality / Local Authority",
        "patterns": [
            r"עירי[יה]ת",
            r"מועצה מקומית",
            r"מועצה אזורית",
            r"אגף הגבייה",
            r"מחלקת הארנונה",
            r"ארנונה",
        ],
        "ref_patterns": [
            r"חשבון\s*נכס\s*\d+",
            r"מס['׳]?\s*נכס\s*\d+",
        ],
    },
    "interior_ministry": {
        "name_he": "משרד הפנים / רשות האוכלוסין וההגירה",
        "name_en": "Population and Immigration Authority (PIBA, Interior Ministry)",
        "patterns": [
            r"משרד הפנים",
            r"רשות האוכלוסין",
            r"לשכת רישום(?! המקרקעין)",
            r"אוכלוסין והגירה",
        ],
        "ref_patterns": [
            r"בקשה\s*מס['׳]?\s*\d+",
        ],
    },
    "land_registry": {
        "name_he": "לשכת רישום המקרקעין (טאבו)",
        "name_en": "Land Registry (Tabu)",
        "patterns": [
            r"טאבו",
            r"רישום (?:ה)?מקרקעין",
            r"לשכת הרישום",
            r"הממונה על המרשם",
            r"רשם המקרקעין",
        ],
        "ref_patterns": [
            r"גוש\s*\d+",
            r"חלקה\s*\d+",
        ],
    },
    "court": {
        "name_he": "בית משפט",
        "name_en": "Court",
        "patterns": [
            r"בית\s*(?:ה)?משפט",
            r"בית\s*(?:ה)?דין",
            r"תביעות\s*קטנות",
            r"בית הדין (?:האזורי |הארצי )?לעבודה",
        ],
        "ref_patterns": [
            r"ב[\"״]ל\s*\d+",  # Labour Court case number in a Bituach Leumi suit
            r"ת[\"״]?[אפק]\s*\d+",
            r"תמ[\"״]?ש\s*\d+",
        ],
    },
    "enforcement_authority": {
        "name_he": "רשות האכיפה והגבייה (הוצאה לפועל)",
        "name_en": "Enforcement and Collection Authority",
        "patterns": [
            r"הוצאה לפועל",
            r"רשות האכיפה",
            r"הוצל[\"״]?פ",
            r"(?<!הערת )(?<!הערות )אזהרה",
            r"הנך החייב",
        ],
        "ref_patterns": [
            r"תיק\s*הוצל[\"״]?פ\s*\d+",
        ],
    },
    "planning_committee": {
        "name_he": "ועדה לתכנון ובנייה",
        "name_en": "Planning and Building Committee",
        "patterns": [
            r"תכנון ובני[יה]",
            r"ועדה מקומית",
            r"ועדה מחוזית",
            r"היתר בני[יה]",
        ],
        "ref_patterns": [],
    },
    "idf": {
        "name_he": 'צה"ל',
        "name_en": "Israel Defense Forces",
        "patterns": [
            r"צה[\"״]?ל",
            r"צבא הגנה",
            r"צו\s*8",
            r"מילואים",
        ],
        "ref_patterns": [],
    },
}

# --- Document type patterns ---

DOCUMENT_TYPES = {
    "tax_assessment": {
        "name_he": "שומת מס",
        "name_en": "Tax Assessment",
        "patterns": [r"שומה", r"שומת מס", r"מיטב השפיטה"],
        "urgency": "URGENT",
        "typical_window": 'Income Tax Ordinance s.150: a written objection (השגה) within 30 days of service of the assessment.',
    },
    "objection_decision": {
        "name_he": "החלטה בהשגה",
        "name_en": "Objection Decision",
        "patterns": [r"החלטה בהשגה", r"תשובה להשגה"],
        "strong": [r"צו לפי סעיף 152", r"השגתך", r"לערער על הצו", r"החלטה בהשגה"],
        "urgency": "URGENT",
        "typical_window": 'An objection decision under s.152: appeal to the District Court; use the period stated in the letter.',
    },
    "benefit_approval": {
        "name_he": "אישור גמלה / תביעה",
        "name_en": "Benefit Approval",
        "patterns": [r"אושר[הו]", r"תביעתך אושרה", r"(?<!לא )(?<!אינך )(?<!אינו )(?<!אינה )זכאי"],
        "urgency": "LOW",
        "typical_window": None,
    },
    "benefit_denial": {
        "name_he": "דחיית תביעה",
        "name_en": "Benefit Denial",
        "patterns": [r"נדח[תה]", r"תביעתך נדחתה", r"(?:לא|אינך|אינו|אינה)\s+זכאי"],
        "urgency": "HIGH",
        "typical_window": "Bituach Leumi: 12 months to appeal to the regional Labor Court (6 months for alimony decisions). A medical-committee decision has its own, shorter ערר window (60 days general disability, 30 days work injury).",
    },
    "debt_notice": {
        "name_he": "הודעת חוב / דרישת תשלום",
        "name_en": "Debt Notice",
        "patterns": [hw("חוב"), r"דרישת תשלום", r"יתרת חוב", r"סכום לתשלום"],
        "urgency": "HIGH",
        "typical_window": None,
    },
    "court_summons": {
        "name_he": "הזמנה לדין",
        "name_en": "Court Summons",
        "patterns": [r"הזמנה לדין", r"מוזמן בזה", r"להתייצב"],
        "urgency": "URGENT",
        "typical_window": None,
    },
    "claim": {
        "name_he": "כתב תביעה",
        "name_en": "Statement of Claim",
        "patterns": [r"כתב תביעה", r"התובע", r"הנתבע"],
        "strong": [r"להגיש כתב הגנה", r"^\s*כתב תביעה\s*$"],
        "urgency": "URGENT",
        "typical_window": 'Statement of defence: 60 days from service in Magistrate and District courts (Civil Procedure Regulations 2018, reg. 9), 30 days in Small Claims. Check the summons.',
    },
    "judgment": {
        "name_he": "פסק דין",
        "name_en": "Judgment",
        "patterns": [r"(?<!ב)פסק דין(?! בהיעדר)", r"ניתן בזה פסק"],
        "strong": [r"^\s*פסק דין\s*\.?\s*$", r"ניתן בזה פסק", r"הנתבע ישלם", r"התביעה (?:מתקבלת|נדחית|התקבלה|נדחתה)"],
        "urgency": "HIGH",
        "typical_window": 'Civil appeal: 60 days from service of the judgment (Civil Procedure Regulations 2018, reg. 137).',
    },
    "seizure_notice": {
        "name_he": "הודעת עיקול",
        "name_en": "Seizure/Lien Notice",
        "patterns": [r"עיקול", r"צו עיקול"],
        "urgency": "URGENT",
        "typical_window": None,
    },
    "enforcement_warning": {
        "name_he": "אזהרה (הוצאה לפועל)",
        "name_en": "Enforcement Warning",
        # "הערת אזהרה" is a Land Registry caveat, not an execution warning.
        "patterns": [r"(?<!הערת )(?<!הערות )אזהרה", r"הוצאה לפועל"],
        "urgency": "URGENT",
        "typical_window": "Execution Office: on a judgment file, 20 days from service of the אזהרה to pay, arrange instalments or ask for a payment order; on a bill or cheque (שטר) file or a fixed-sum claim file, 30 days to file an התנגדות. Use the period printed on the אזהרה itself.",
    },
    "arnona_notice": {
        "name_he": "הודעת ארנונה",
        "name_en": "Arnona (Property Tax) Notice",
        "patterns": [r"ארנונה", r"שובר תשלום"],
        "urgency": "MEDIUM",
        "typical_window": "Arnona: השגה to the arnona manager within 90 days of receiving the payment notice; ערר on the manager's answer within 30 days.",
    },
    "discount_decision": {
        "name_he": "החלטה בעניין הנחה",
        "name_en": "Discount Decision",
        "patterns": [r"הנחה", r"ועדת הנחות"],
        "urgency": "LOW",
        "typical_window": None,
    },
    "building_violation": {
        "name_he": "הודעה על חריגת בנייה",
        "name_en": "Building Violation Notice",
        "patterns": [r"חריגת בני", r"צו הריסה", r"עבירת בני"],
        "urgency": "URGENT",
        "typical_window": 'Administrative demolition order: a request to cancel it goes to the court within 15 days of service (Planning and Building Law s.228).',
    },
    "zoning_notice": {
        "name_he": "הודעה על תוכנית בניין עיר",
        "name_en": "Zoning/Planning Notice",
        "patterns": [r'תב"ע', r"תוכנית בניין עיר", r"הפקדת תוכנית"],
        "urgency": "MEDIUM",
        "typical_window": 'Deposited plan: objections within two months of publication of the deposit notice (s.102), unless the notice sets a longer period.',
    },
    "refund_notice": {
        "name_he": "הודעה על החזר",
        "name_en": "Refund Notice",
        "patterns": [r"החזר", r"זיכוי", r"יוחזר לחשבונך"],
        "urgency": "LOW",
        "typical_window": None,
    },
    "information_request": {
        "name_he": "בקשה להשלמת מסמכים / בירורים",
        "name_en": "Information/Document Request",
        "patterns": [r"השלמת מסמכים", r"מכתב בירורים", r"נא להמציא", r"נא לצרף"],
        "urgency": "MEDIUM",
        "typical_window": None,
    },
    "medical_committee": {
        "name_he": "החלטת ועדה רפואית",
        "name_en": "Medical Committee Decision",
        "patterns": [r"ועדה רפואית", r"אחוזי נכות", r"נכות רפואית"],
        "strong": [r"ועדה רפואית לעררים", r"החלטת (?:ה)?ועדה (?:ה)?רפואית"],
        "urgency": "URGENT",
        "typical_window": "Medical-committee ערר: 60 days for general disability, 30 days for a work injury (reasons may follow within 60). Ask which track the decision is on.",
    },
    "fine_notice": {
        "name_he": "הודעת תשלום קנס",
        "name_en": "Fine Notice (parking, by-law, traffic)",
        "patterns": [r"קנס", r"להישפט", r"עבירת חניה", r"דוח חניה"],
        "strong": [r"הודעת תשלום קנס", r"בקשה לביטול (?:ה)?(?:קנס|דוח)"],
        "urgency": "URGENT",
        "typical_window": "Fine notice (Criminal Procedure Law s.229): a request to cancel goes to the prosecutor within 30 days of service; pay, or give notice of wanting to be tried, within 90 days.",
    },
    "registry_decision": {
        "name_he": "החלטת רשם המקרקעין",
        "name_en": "Land Registrar Decision",
        "patterns": [r"החלטת הרשם", r"רשם המקרקעין"],
        "strong": [r"הממונה על המרשם", r"ערר לממונה"],
        "urgency": "URGENT",
        "typical_window": "Land Registry: ערר to the Registrar Supervisor (הממונה על המרשם) within 15 days of delivery or of learning of the decision (reg. 74); then District Court within 15 days (reg. 76).",
    },
    "betterment_levy": {
        "name_he": "שומת היטל השבחה",
        "name_en": "Betterment Levy Assessment",
        "patterns": [r"היטל השבחה"],
        "strong": [r"שומת היטל השבחה", r"ועדת ערר לפיצויים ולהיטל השבחה"],
        "urgency": "HIGH",
        "typical_window": "Betterment levy: ערר to the Compensation and Betterment Levy Appeals Committee within 45 days of the assessment coming to the payer's knowledge (Planning and Building Law, Third Schedule).",
    },
    "caveat_notice": {
        "name_he": "הודעה על רישום הערת אזהרה",
        "name_en": "Land Registry Caveat Notice",
        "patterns": [r"הערת אזהרה", r"הערות אזהרה"],
        "urgency": "MEDIUM",
        "typical_window": None,
    },
    "status_decision": {
        "name_he": "החלטה בעניין מעמד / אשרה",
        "name_en": "Status / Visa Decision",
        "patterns": [hw("מעמד"), r"בית הדין לעררים", r"הסדרת מעמד", r"הארכת אשרה"],
        "urgency": "HIGH",
        "typical_window": "PIBA decisions under the Entry into Israel Law: ערר to the Appeals Tribunal (בית הדין לעררים) within 30 days of publication of the decision, notice of it, or learning of it, whichever is earliest.",
    },
    "reserve_duty": {
        "name_he": "צו מילואים / תגמולי מילואים",
        "name_en": "Reserve Duty Order/Compensation",
        "patterns": [r"מילואים", r"צו 8", r"תגמולי מילואים", r"דמי מילואים"],
        "urgency": "MEDIUM",
        "typical_window": None,
    },
}

# --- Law reference patterns ---

KNOWN_LAWS = {
    r"פקודת מס הכנסה": "Income Tax Ordinance",
    r"חוק הביטוח הלאומי": "National Insurance Law",
    r"חוק מס ערך מוסף": "Value Added Tax Law",
    r"חוק התכנון והבנייה": "Planning and Building Law",
    r"חוק ההוצאה לפועל": "Execution Law",
    r"חוק בתי המשפט": "Courts Law",
    r"חוק המקרקעין": "Land Law",
    r"חוק הגנת הדייר": "Tenant Protection Law",
    r"פקודת העיריות": "Municipalities Ordinance",
    r"חוק רישוי עסקים": "Business Licensing Law",
    r"חוק הכניסה לישראל": "Entry into Israel Law",
    r"חוק האזרחות": "Citizenship Law",
    r"חוק השבות": "Law of Return",
}


@dataclass
class AnalysisResult:
    """Structured result of document analysis."""

    sender: Optional[str] = None
    sender_en: Optional[str] = None
    document_type: Optional[str] = None
    document_type_en: Optional[str] = None
    urgency: str = "UNKNOWN"
    subject_summary: str = ""
    required_actions: list = field(default_factory=list)
    deadlines: list = field(default_factory=list)
    consequences: list = field(default_factory=list)
    monetary_amounts: list = field(default_factory=list)
    laws_referenced: list = field(default_factory=list)
    reference_numbers: list = field(default_factory=list)
    dates_found: list = field(default_factory=list)
    confidence: str = "LOW"
    notes: list = field(default_factory=list)


def identify_sender(text: str) -> tuple[Optional[str], Optional[str], str, Optional[str]]:
    """Identify the government body that sent the document."""
    best_match = None
    best_score = 0

    for body_id, body_info in GOVERNMENT_BODIES.items():
        score = 0
        for pattern in body_info["patterns"]:
            matches = re.findall(pattern, text)
            score += len(matches) * 2

        for pattern in body_info["ref_patterns"]:
            matches = re.findall(pattern, text)
            score += len(matches) * 3  # Reference numbers are strong signals

        if score > best_score:
            best_score = score
            best_match = body_id

    if best_match and best_score >= 2:
        body = GOVERNMENT_BODIES[best_match]
        confidence = "HIGH" if best_score >= 6 else "MEDIUM" if best_score >= 3 else "LOW"
        return body["name_he"], body["name_en"], confidence, best_match
    return None, None, "LOW", None


# Windows that belong to one sender only. Quoting Bituach Leumi's 12-month
# Labor Court route on a Land Registry refusal is worse than quoting nothing.
WINDOW_SENDERS = {
    "benefit_denial": {"national_insurance"},
    "tax_assessment": {"tax_authority"},
    "objection_decision": {"tax_authority", "municipality"},
    "status_decision": {"interior_ministry"},
    "enforcement_warning": {"enforcement_authority"},
    "arnona_notice": {"municipality"},
    "registry_decision": {"land_registry"},
    "fine_notice": {"municipality"},
}

# Notes that must be shown even when the letter states its own deadline, because
# the letter usually prints only the longest period (90 days to pay a fine).
ALWAYS_NOTE = {"fine_notice"}


def refine_window(doc_id: Optional[str], sender_id: Optional[str], text: str,
                  window: Optional[str]) -> Optional[str]:
    """Pick the window that matches this sender and sub-type, or fall back to a neutral note."""
    if doc_id is None:
        return window
    if sender_id == "interior_ministry" and re.search(r"מרשם האוכלוסין", text) and doc_id in ("benefit_denial", "status_decision"):
        return ("Population-registry decision: unless the decision is one the Entry into Israel Law sends to the Appeals Tribunal, the route is an administrative petition "
                "within 45 days of publication, notice or learning of it, whichever is earliest (administrative courts reg. 3).")
    has_ = lambda p: re.search(p, text) is not None
    if sender_id == "tax_authority" and doc_id in ("fine_notice", "tax_assessment") and has_(r"קנס"):
        if has_(r"גרעון|גירעון|סעיף 191"):
            return "Tax deficiency fine: treated as an assessment, so a written השגה within 30 days of service applies (Income Tax Ordinance s.150). This is not a parking-fine route."
        return "Tax Authority fine (for example late filing): this is not a parking-fine route. Read the letter for its review route and get professional advice; do not assume the 30-day השגה applies."
    if doc_id == "fine_notice" and sender_id is None and has_(r"הודעת תשלום קנס"):
        return window
    if doc_id == "benefit_denial" and sender_id == "planning_committee" and has_(r"היתר"):
        return "Permit refusal: ערר to the district appeals committee (ועדת ערר) within 30 days of service of the refusal (Planning and Building Law s.152)."
    if sender_id == "municipality" and doc_id in ("debt_notice", "arnona_notice") and has_(r"ארנונה") and not has_(r"תשובה להשגה|השגתך|ועדת (?:ה)?ערר"):
        return "Arnona payment notice: השגה to the arnona manager within 90 days of receiving it, on the grounds the law allows (area, classification, use, or not being the holder)."
    if sender_id == "enforcement_authority" and has_(r"החלטת (?:ה)?רשם|רשם ההוצאה לפועל החליט|החלטה\s*:"):
        return "Execution Office registrar decision: appeal to the Magistrate Court within 20 days of the decision (or of service if given in your absence), usually by leave; in a family-matter file, to the Family Court as of right (Execution Law s.80; regulations reg. 120)."
    if sender_id == "interior_ministry" and doc_id == "benefit_denial" and has_(r"אשר[הת]|מעמד|אזרחות|איחוד משפחות|תושבות"):
        return DOCUMENT_TYPES["status_decision"]["typical_window"]
    if doc_id in WINDOW_SENDERS and sender_id and sender_id not in WINDOW_SENDERS[doc_id]:
        return "The window depends on the sender and the letter type; use the period stated in the letter."
    has = lambda p: re.search(p, text) is not None
    if doc_id in ("tax_assessment", "objection_decision"):
        if has(r"מיסוי מקרקעין|מס שבח|מס רכישה"):
            return ("Taxes on Land: השגה within 30 days of delivery of the assessment (s.87); on the director's decision, ערר to the appeals committee within 30 days (s.88)."
                    if doc_id == "tax_assessment" else
                    "Taxes on Land: ערר on the director's decision to the appeals committee within 30 days of delivery (s.88).")
        if has(r"מע[\"״]מ|מס ערך מוסף") and not has(r"פקודת מס הכנסה"):
            return ("VAT: a reasoned השגה to the VAT director within 30 days of service (VAT Law s.82); no decision within a year means it is deemed accepted."
                    if doc_id == "tax_assessment" else
                    "VAT: appeal the director's decision on the השגה to the District Court (s.83); use the period stated in the decision.")
        if doc_id == "objection_decision" and sender_id == "tax_authority":
            return "Income tax: appeal the order (צו) to the District Court within 30 days of delivery (s.153; appeal regulations reg. 2). Do NOT file another השגה."
    if doc_id == "arnona_notice" and has(r"תשובה להשגה|השגתך|ועדת (?:ה)?ערר"):
        return "Arnona: ערר on the manager's answer to the appeals committee within 30 days of delivery of the answer (s.6)."
    if doc_id == "objection_decision" and sender_id == "municipality":
        return "Arnona: ערר on the manager's answer to the appeals committee within 30 days of delivery of the answer (s.6)."
    if doc_id == "medical_committee":
        if has(r"נפגע(?:י)? עבודה|פגיעה בעבודה|תאונת עבודה"):
            return "Work injury: ערר within 30 days of the written notice; the reasons may follow within 60 days."
        if has(r"נכות כללית"):
            return "General disability: ערר in writing with reasons within 60 days of the written notice."
    if doc_id == "judgment":
        if has(r"בית הדין (?:האזורי )?לעבודה"):
            return "Labour Court judgment: appeal to the National Labour Court within 30 days of the hearing or of service, unless another law sets a different period; some cases need leave first. The civil 60-day rule does not apply."
        if has(r"תביעות קטנות|ת[\"״]ק"):
            return "Small Claims judgment: leave to appeal to the District Court within 15 days of the judgment, or 30 days in proceedings opened on or after 11.4.2025 (reg. 16). Ask when the claim was opened."
    if doc_id == "claim" and has(r"תביעות קטנות|ת[\"״]ק"):
        return "Small Claims: statement of defence within 30 days of service of the summons."
    if doc_id == "enforcement_warning":
        bill = has(r"שטר|שיק|צ'ק|סכום קצוב")
        judgment = has(r"פסק דין|פסק הדין")
        if judgment and not bill:
            return "Judgment file: 20 days from service of the אזהרה to pay, arrange instalments or ask for a payment order (Execution Law s.7)."
        if bill and not judgment:
            return "Bill, cheque or fixed-sum claim file: 30 days from service of the אזהרה to file an התנגדות (s.81א / s.81א1)."
    return window


def identify_document_type(text: str) -> tuple[Optional[str], Optional[str], str, Optional[str], Optional[str]]:
    """Identify the type of document."""
    best_match = None
    best_score = 0

    for doc_id, doc_info in DOCUMENT_TYPES.items():
        score = 0
        for pattern in doc_info["patterns"]:
            matches = re.findall(pattern, text)
            score += len(matches)
        # A phrase that only one document type uses outweighs words such as
        # "התובע" / "הנתבע" that appear in claims and judgments alike.
        for pattern in doc_info.get("strong", []):
            score += 3 * len(re.findall(pattern, text, re.M))

        if score > best_score:
            best_score = score
            best_match = doc_id

    if best_match and best_score >= 1:
        doc = DOCUMENT_TYPES[best_match]
        return (
            doc["name_he"],
            doc["name_en"],
            doc["urgency"],
            doc["typical_window"],
            best_match,
        )
    return None, None, "UNKNOWN", None, None


def extract_monetary_amounts(text: str) -> list[str]:
    """Extract monetary amounts from the document."""
    amounts = []

    # NIS amounts with various formats
    # A stray ":" or "," between the number and the currency is how pdftotext
    # reorders "סכום: 18,450 ש\"ח" from an RTL PDF ("18,450 :ש\"ח").
    cur = r"(?:ש[\"״]ח|ש''ח|שקלים|שקל|NIS|ILS|₪)"
    nis_patterns = [
        r"(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*[:,]?\s*" + cur,
        cur + r"\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",
        r"סך\s*(?:של\s*)?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",
    ]

    for pattern in nis_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            amounts.append(f"{match} NIS")

    return list(set(amounts))


def extract_dates(text: str) -> list[str]:
    """Extract dates from the document."""
    dates = []

    # Hebrew date format: DD/MM/YYYY or DD.MM.YYYY
    date_patterns = [
        r"(\d{1,2}[/.]\d{1,2}[/.]\d{2,4})",
        r"(\d{1,2}\s+(?:בינואר|בפברואר|במרץ|באפריל|במאי|ביוני|ביולי|באוגוסט|בספטמבר|באוקטובר|בנובמבר|בדצמבר)\s+\d{4})",
        r"(\d{1,2}\s+(?:ינואר|פברואר|מרץ|אפריל|מאי|יוני|יולי|אוגוסט|ספטמבר|אוקטובר|נובמבר|דצמבר)\s+\d{4})",
    ]

    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        dates.extend(matches)

    return list(set(dates))


def extract_reference_numbers(text: str) -> list[str]:
    """Extract reference numbers and file numbers."""
    refs = []

    ref_patterns = [
        r"(?:תיק|אסמכתא|מס['׳]?)\s*(?:הוצל[\"״]?פ\s*)?[:.]?\s*(\d[\d/-]{4,})",
        r"(?:ת[\"״]?[אפק]|תמ[\"״]?ש)\s*(\d[\d/-]+)",
        r"(?:גוש|חלקה)\s*(\d+)",
        r"בל/(\d+)",
    ]

    for pattern in ref_patterns:
        matches = re.findall(pattern, text)
        refs.extend(matches)

    return list(set(refs))


def extract_laws(text: str) -> list[dict]:
    """Extract references to laws and regulations."""
    laws = []

    for hebrew_name, english_name in KNOWN_LAWS.items():
        # PDF extraction wraps a law name across lines, so match any whitespace.
        law_re = hebrew_name.replace(" ", r"\s+")
        if re.search(law_re, text):
            # Try to find specific section numbers
            # A Hebrew letter after the number is a sub-section ("145א") only when no
            # further letter follows: in "150לפקודת" the "ל" is the next word's prefix.
            section_pattern = rf"סעיף\s*(\d+(?:[א-ת](?![א-ת]))?(?:\(\d+\))?)\s*(?:ל|של\s*)?{law_re}"
            sections = re.findall(section_pattern, text)

            if sections:
                for section in sections:
                    laws.append({
                        "law_he": hebrew_name,
                        "law_en": english_name,
                        "section": section,
                    })
            else:
                # Also check for general section references near the law name
                general_pattern = rf"{law_re}.*?סעיף\s*(\d+(?:[א-ת](?![א-ת]))?)"
                general_sections = re.findall(general_pattern, text[:500])
                if general_sections:
                    for section in general_sections:
                        laws.append({
                            "law_he": hebrew_name,
                            "law_en": english_name,
                            "section": section,
                        })
                else:
                    laws.append({
                        "law_he": hebrew_name,
                        "law_en": english_name,
                        "section": None,
                    })

    return laws


HEBREW_NUMBER_WORDS = {
    "שבעה": 7, "עשרה": 10, "ארבעה עשר": 14, "חמישה עשר": 15, "עשרים": 20,
    "עשרים ואחד": 21, "שלושים": 30, "ארבעים וחמישה": 45, "שישים": 60, "ששים": 60,
    "תשעים": 90, "מאה ועשרים": 120,
}
_NUM = r"(\d+|" + "|".join(sorted(HEBREW_NUMBER_WORDS, key=len, reverse=True)) + r")"


def extract_deadlines(text: str) -> list[dict]:
    """Extract deadline information from the document."""
    deadlines = []

    # "within X days" written as digits or words: "תוך 30 יום", "בתוך 20 ימים",
    # "תוך שלושים ימים". "יום" (singular after a number) is the common form.
    day_patterns = [
        (rf"(?:ב)?תוך\s*{_NUM}\s*(?:ימים|יום|ימי עבודה)", "days from"),
        (r"לא\s*יאוחר\s*מ[- ]?(\d{1,2}[/.]\d{1,2}[/.]\d{2,4})", "by date"),
        (r"עד\s*(?:ליום|לתאריך)?\s*(\d{1,2}[/.]\d{1,2}[/.]\d{2,4})", "by date"),
        (rf"(?:ב)?תוך\s*{_NUM}\s*(?:חודשים|חודש)", "months from"),
    ]

    for pattern, dtype in day_patterns:
        for m in re.finditer(pattern, text):
            value = m.group(1)
            value = str(HEBREW_NUMBER_WORDS.get(value, value))
            start, end = max(0, m.start() - 50), min(len(text), m.end() + 50)
            deadlines.append({
                "type": dtype,
                "value": value,
                # Context from the match position, not text.find(value): "12"
                # would otherwise land inside a date like 12.10.2026.
                "raw_context": text[start:end].strip(),
            })

    return deadlines


def extract_consequences(text: str) -> list[str]:
    """Extract consequences of inaction."""
    consequences = []

    consequence_patterns = [
        r"אי[- ]?עמידה.*?(?:תגרום|יגרום|עלול|עלולה).*?[.;]",
        r"(?:במידה ולא|אם לא)\s+.*?[.;]",
        r"(?:ייחשב|תיחשב)\s+.*?[.;]",
        r"(?:קנס|עיקול|הליכים)\s+.*?[.;]",
        r"פסק דין בהיעדר.*?[.;]",
    ]

    for pattern in consequence_patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            cleaned = match.strip()
            if len(cleaned) > 10:
                consequences.append(cleaned[:200])

    return consequences


def extract_required_actions(text: str) -> list[str]:
    """Extract required actions from the document."""
    actions = []

    action_patterns = [
        r"(?:עליך|עלייך|הנך מתבקש|הנך מתבקשת|נא|יש)\s+(?:ל|להגיש|לשלם|להתייצב|לפנות|למלא|להגיב|לצרף|להמציא).*?[.;]",
        r"(?:חובה|נדרש|נדרשת)\s+.*?[.;]",
        r"(?:יש להגיש|יש לשלם|יש להתייצב|יש לפנות)\s+.*?[.;]",
    ]

    for pattern in action_patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            cleaned = match.strip()
            if len(cleaned) > 10:
                actions.append(cleaned[:200])

    return actions


# Bidi control marks that pdftotext and copy-paste from RTL viewers insert around
# numbers and punctuation. Left in place they sit between "תוך" and "30", or
# between "ש\"ח" and the amount, and every pattern below silently misses.
_BIDI_CONTROLS = dict.fromkeys(map(ord, "\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069\ufeff"), None)
_FINALS = "ךםןףץ"


def normalize_text(text: str) -> tuple[str, list[str]]:
    """Clean text extracted from PDFs or RTL viewers. Returns (text, notes)."""
    notes = []
    cleaned = text.translate(_BIDI_CONTROLS).replace("\u00a0", " ")
    if cleaned != text.replace("\u00a0", " "):
        notes.append("Removed invisible bidi control characters (typical of PDF text extraction).")

    words = re.findall(r"[א-ת]{2,}", cleaned)
    if len(words) >= 8:
        starts_final = sum(1 for w in words if w[0] in _FINALS)
        ends_final = sum(1 for w in words if w[-1] in _FINALS)
        # A final letter can only END a Hebrew word. Many words starting with one
        # means each line was extracted character-reversed (visual order).
        if starts_final > ends_final:
            def unreverse(line: str) -> str:
                r = line[::-1]
                return re.sub(r"[0-9A-Za-z][0-9A-Za-z.,/:\-]*", lambda m: m.group(0)[::-1], r)
            cleaned = "\n".join(unreverse(l) for l in cleaned.splitlines())
            notes.append("Text looked character-reversed (visual-order PDF); each line was re-reversed. Verify amounts and dates against the original.")

    lines = [l for l in cleaned.splitlines() if l.strip()]
    misplaced = sum(1 for l in lines if re.match(r"^\s*[.,:;]\s*[א-ת]", l) or re.match(r"^\s*[.,:;]?\s*[\d,./-]+\s*[א-ת]", l))
    if lines and misplaced >= max(2, len(lines) // 4):
        notes.append("Text looks like a visual-order PDF dump (punctuation and numbers at the start of lines). Numbers may be detached from their words: re-extract with `pdftotext -layout`, or read amounts and deadlines from the original letter.")
    return cleaned, notes


def analyze_document(text: str) -> AnalysisResult:
    """Main analysis function. Extracts all structured information."""
    result = AnalysisResult()
    text, norm_notes = normalize_text(text)
    result.notes.extend(norm_notes)

    # Identify sender
    sender_he, sender_en, sender_confidence, sender_id = identify_sender(text)
    result.sender = sender_he
    result.sender_en = sender_en

    # Identify document type
    doc_he, doc_en, urgency, typical_window, doc_id = identify_document_type(text)
    # "Approval" is only safe to report as good news on a Bituach Leumi letter.
    # Elsewhere ("התנגדותך נדחתה והתכנית אושרה") it can hide an adverse decision.
    if doc_id == "benefit_approval" and sender_id != "national_insurance":
        doc_he, doc_en, urgency = "החלטה (לא מסווגת)", "Unclassified Decision", "HIGH"
        doc_id = None
        typical_window = "Could not classify this decision safely. Read the letter for any appeal or objection window before treating it as good news."
    typical_window = refine_window(doc_id, sender_id, text, typical_window)
    # A refusal from anyone other than Bituach Leumi is not a "benefit" denial.
    if doc_id == "benefit_denial" and sender_id and sender_id != "national_insurance":
        doc_he, doc_en = "החלטת סירוב / דחייה", "Refusal / Rejection Decision"
    if sender_id == "tax_authority" and doc_id in ("fine_notice", "tax_assessment") and re.search(r"קנס", text):
        doc_he, doc_en = "קנס מרשות המסים", "Tax Authority Fine"
    if sender_id == "enforcement_authority" and typical_window and typical_window.startswith("Execution Office registrar decision"):
        doc_he, doc_en = "החלטת רשם ההוצאה לפועל", "Execution Office Registrar Decision"
    # Short statutory windows make the letter URGENT even when none is quoted.
    if typical_window and re.search(r"within (?:15|20|30) days", typical_window) and urgency in ("HIGH", "MEDIUM", "LOW", "UNKNOWN"):
        urgency = "URGENT"
    result.document_type = doc_he
    result.document_type_en = doc_en
    result.urgency = urgency

    if doc_id is None and typical_window and typical_window.startswith("Could not classify"):
        result.notes.append(typical_window)
        typical_window = None

    # Extract structured data
    result.monetary_amounts = extract_monetary_amounts(text)
    result.dates_found = extract_dates(text)
    result.reference_numbers = extract_reference_numbers(text)
    result.laws_referenced = extract_laws(text)
    result.deadlines = extract_deadlines(text)
    result.consequences = extract_consequences(text)
    result.required_actions = extract_required_actions(text)

    # A stated window of 30 days or less makes the letter URGENT whatever its type.
    day_windows = [int(d["value"]) for d in result.deadlines
                   if d["type"] == "days from" and d["value"].isdigit()]
    if day_windows and min(day_windows) <= 30 and result.urgency in ("LOW", "MEDIUM", "HIGH", "UNKNOWN"):
        result.urgency = "URGENT"

    # Determine overall confidence
    signals = sum([
        1 if result.sender else 0,
        1 if result.document_type else 0,
        1 if result.deadlines else 0,
        1 if result.laws_referenced else 0,
        1 if result.reference_numbers else 0,
    ])
    result.confidence = "HIGH" if signals >= 4 else "MEDIUM" if signals >= 2 else "LOW"

    # Add helpful notes
    if result.urgency == "URGENT":
        result.notes.append(
            "This document appears to be URGENT. Recommend immediate professional consultation."
        )
    if typical_window and (not result.deadlines or doc_id in ALWAYS_NOTE):
        result.notes.append(
            ("No explicit deadline found in the text. " if not result.deadlines else "Also note: ")
            + f"Typical rule for this document type: {typical_window} Check what the period is counted from (service, receipt, or learning of the decision), not the date printed on the letter."
        )
    if not result.sender:
        result.notes.append(
            "Could not identify the sending body. Check the letterhead, return address, or envelope."
        )

    return result


def format_output(result: AnalysisResult, output_format: str = "text") -> str:
    """Format the analysis result for display."""
    if output_format == "json":
        return json.dumps(asdict(result), ensure_ascii=False, indent=2)

    lines = []
    lines.append("=" * 60)
    lines.append("  ISRAELI GOVERNMENT DOCUMENT ANALYSIS")
    lines.append("=" * 60)
    lines.append("")

    # Sender
    if result.sender:
        lines.append(f"SENDER: {result.sender}")
        lines.append(f"        ({result.sender_en})")
    else:
        lines.append("SENDER: Could not identify (check letterhead/envelope)")
    lines.append("")

    # Document type
    if result.document_type:
        lines.append(f"DOCUMENT TYPE: {result.document_type}")
        lines.append(f"               ({result.document_type_en})")
    else:
        lines.append("DOCUMENT TYPE: Could not determine")
    lines.append("")

    # Urgency
    urgency_display = {
        "URGENT": "URGENT (act immediately)",
        "HIGH": "HIGH (respond within the stated deadline)",
        "MEDIUM": "MEDIUM (action needed but not immediately critical)",
        "LOW": "LOW (informational, usually no action required)",
        "UNKNOWN": "UNKNOWN (review carefully to determine urgency)",
    }
    lines.append(f"URGENCY: {urgency_display.get(result.urgency, result.urgency)}")
    lines.append(f"CONFIDENCE: {result.confidence}")
    lines.append("")

    # Reference numbers
    if result.reference_numbers:
        lines.append("REFERENCE NUMBERS:")
        for ref in result.reference_numbers:
            lines.append(f"  - {ref}")
        lines.append("")

    # Monetary amounts
    if result.monetary_amounts:
        lines.append("MONETARY AMOUNTS FOUND:")
        for amount in result.monetary_amounts:
            lines.append(f"  - {amount}")
        lines.append("")

    # Dates
    if result.dates_found:
        lines.append("DATES FOUND:")
        for date in result.dates_found:
            lines.append(f"  - {date}")
        lines.append("")

    # Deadlines
    if result.deadlines:
        lines.append("DEADLINES:")
        for deadline in result.deadlines:
            lines.append(f"  - {deadline['type']}: {deadline['value']}")
            if deadline.get("raw_context"):
                lines.append(f"    Context: ...{deadline['raw_context']}...")
        lines.append("")

    # Required actions
    if result.required_actions:
        lines.append("REQUIRED ACTIONS:")
        for i, action in enumerate(result.required_actions, 1):
            lines.append(f"  {i}. {action}")
        lines.append("")

    # Consequences
    if result.consequences:
        lines.append("CONSEQUENCES OF INACTION:")
        for consequence in result.consequences:
            lines.append(f"  - {consequence}")
        lines.append("")

    # Laws referenced
    if result.laws_referenced:
        lines.append("LAWS REFERENCED:")
        for law in result.laws_referenced:
            section = f", Section {law['section']}" if law.get("section") else ""
            lines.append(f"  - {law['law_he']} ({law['law_en']}{section})")
        lines.append("")

    # Notes
    if result.notes:
        lines.append("NOTES:")
        for note in result.notes:
            lines.append(f"  * {note}")
        lines.append("")

    lines.append("=" * 60)
    lines.append("NOTE: This analysis is automated and may not capture all")
    lines.append("nuances. For legal or financial decisions, always consult")
    lines.append("a qualified professional (lawyer, accountant, etc.).")
    lines.append("=" * 60)

    return "\n".join(lines)


# Regression letters for the windows most likely to be confused. Run: --self-test
SELF_TESTS = [
    ("Tax Authority late-filing fine is not a parking fine", 'רשות המסים בישראל פקיד שומה חיפה. הנדון: קנס על אי הגשת דו"ח במועד לפי פקודת מס הכנסה.', "Tax Authority Fine", "not a parking-fine route"),
    ("Deficiency fine follows the 30-day objection", 'רשות המסים בישראל פקיד שומה חיפה. הנדון: קנס גירעון לפי סעיף 191 לפקודת מס הכנסה.', None, "30 days"),
    ("Labour Court judgment is not the civil 60-day appeal", 'בית הדין האזורי לעבודה בתל אביב. ב"ל 12345-01-25. פסק דין. התביעה נגד המוסד לביטוח לאומי נדחית.', "Judgment", "National Labour Court within 30 days"),
    ("Fine notice printing 90 days still shows the 30-day cancellation", 'עיריית חיפה. הודעת תשלום קנס בגין עבירת חניה. יש לשלם תוך 90 ימים או להגיש בקשה לביטול.', "Fine Notice", "within 30 days"),
    ("Planning permit refusal gets the 30-day ערר", 'הוועדה המקומית לתכנון ובנייה רמת גן. החלטה בבקשה להיתר בניה. הבקשה נדחתה.', None, "within 30 days"),
    ("Arnona payment notice gets the 90-day השגה", 'עיריית חולון. הודעת תשלום ארנונה לשנת 2026. סכום לתשלום מפורט בשובר.', None, "within 90 days"),
    ("Rejected planning objection is never LOW", 'הוועדה המחוזית לתכנון ובניה מרכז. החלטה בהתנגדויות. התנגדותך נדחתה והתכנית אושרה בכפוף לתיקונים.', None, None),
    ("Execution warning on a judgment file is 20 days", 'לשכת ההוצאה לפועל. אזהרה. הנך החייב בתיק על פי פסק דין שניתן בבית משפט השלום.', "Enforcement Warning", "20 days"),
    ("Land Registry caveat is not an execution warning", 'לשכת רישום המקרקעין. הודעה על רישום הערת אזהרה לטובת בנק על הנכס.', "Land Registry Caveat Notice", None),
    ("Deadline written as 'תוך 30 יום' is found", 'רשות המסים בישראל. הודעת שומה. הנך רשאי להגיש השגה תוך 30 יום.', "Tax Assessment", None),
]


def run_self_tests() -> int:
    failed = 0
    for name, letter, want_type, want_note in SELF_TESTS:
        r = analyze_document(letter)
        notes = " ".join(r.notes)
        ok = (want_type is None or (r.document_type_en or "").startswith(want_type))
        ok = ok and (want_note is None or want_note in notes)
        if "never LOW" in name:
            ok = ok and r.urgency != "LOW"
        if "30 יום" in name:
            ok = ok and any(d["value"] == "30" for d in r.deadlines)
        print(("PASS " if ok else "FAIL ") + name)
        failed += 0 if ok else 1
    print(f"{len(SELF_TESTS) - failed}/{len(SELF_TESTS)} passed")
    return 1 if failed else 0


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Israeli government documents and extract structured information.",
        epilog="Example: python document-analyzer.py --file letter.txt --format json",
    )

    if "--self-test" in sys.argv[1:]:
        sys.exit(run_self_tests())

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--text",
        type=str,
        help="Document text to analyze (paste directly)",
    )
    input_group.add_argument(
        "--file",
        type=str,
        help="Path to a text file (UTF-8 or windows-1255) or a PDF with a text layer",
    )

    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run the built-in regression letters and exit",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    # Get document text
    if args.file and args.file.lower().endswith(".pdf"):
        if not shutil.which("pdftotext"):
            print("Error: reading a PDF needs pdftotext (poppler). Install it, or paste the text with --text.", file=sys.stderr)
            sys.exit(1)
        # pdftotext applies the bidi algorithm, so Hebrew comes out in logical
        # order; its control marks are stripped in normalize_text().
        proc = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", args.file, "-"],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"Error reading PDF: {proc.stderr.strip()}", file=sys.stderr)
            sys.exit(1)
        text = proc.stdout
        if not text.strip():
            print("Error: the PDF has no text layer (a scanned image). Run OCR first, or paste the text.", file=sys.stderr)
            sys.exit(1)
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(args.file, "r", encoding="windows-1255") as f:
                    text = f.read()
            except Exception as e:
                print(f"Error reading file: {e}", file=sys.stderr)
                sys.exit(1)
    else:
        text = args.text

    if not text or not text.strip():
        print("Error: Document text is empty.", file=sys.stderr)
        sys.exit(1)

    # Analyze
    result = analyze_document(text)

    # Output
    print(format_output(result, args.format))


if __name__ == "__main__":
    main()
