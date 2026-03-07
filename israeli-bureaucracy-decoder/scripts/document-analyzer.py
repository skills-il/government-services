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
    python document-analyzer.py --help
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import Optional


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
            r"מע\"?מ",
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
            r"ב[\"״]ל",
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
        "name_en": "Interior Ministry / Population and Immigration Authority",
        "patterns": [
            r"משרד הפנים",
            r"רשות האוכלוסין",
            r"לשכת רישום",
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
            r"רישום מקרקעין",
            r"לשכת הרישום",
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
            r"בית\s*משפט",
            r"בית\s*דין",
            r"תביעות\s*קטנות",
        ],
        "ref_patterns": [
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
        "urgency": "HIGH",
        "default_deadline_days": 30,
    },
    "objection_decision": {
        "name_he": "החלטה בהשגה",
        "name_en": "Objection Decision",
        "patterns": [r"החלטה בהשגה", r"תשובה להשגה"],
        "urgency": "HIGH",
        "default_deadline_days": 30,
    },
    "benefit_approval": {
        "name_he": "אישור גמלה / תביעה",
        "name_en": "Benefit Approval",
        "patterns": [r"אושר[הו]", r"תביעתך אושרה", r"זכאי"],
        "urgency": "LOW",
        "default_deadline_days": None,
    },
    "benefit_denial": {
        "name_he": "דחיית תביעה",
        "name_en": "Benefit Denial",
        "patterns": [r"נדח[תה]", r"תביעתך נדחתה", r"לא זכאי"],
        "urgency": "HIGH",
        "default_deadline_days": 365,
    },
    "debt_notice": {
        "name_he": "הודעת חוב / דרישת תשלום",
        "name_en": "Debt Notice",
        "patterns": [r"חוב", r"דרישת תשלום", r"יתרת חובה", r"סכום לתשלום"],
        "urgency": "HIGH",
        "default_deadline_days": 30,
    },
    "court_summons": {
        "name_he": "הזמנה לדין",
        "name_en": "Court Summons",
        "patterns": [r"הזמנה לדין", r"מוזמן בזה", r"להתייצב"],
        "urgency": "URGENT",
        "default_deadline_days": 30,
    },
    "claim": {
        "name_he": "כתב תביעה",
        "name_en": "Statement of Claim",
        "patterns": [r"כתב תביעה", r"התובע", r"הנתבע"],
        "urgency": "URGENT",
        "default_deadline_days": 30,
    },
    "judgment": {
        "name_he": "פסק דין",
        "name_en": "Judgment",
        "patterns": [r"פסק דין", r"ניתן בזה פסק"],
        "urgency": "HIGH",
        "default_deadline_days": 45,
    },
    "seizure_notice": {
        "name_he": "הודעת עיקול",
        "name_en": "Seizure/Lien Notice",
        "patterns": [r"עיקול", r"צו עיקול"],
        "urgency": "URGENT",
        "default_deadline_days": 20,
    },
    "enforcement_warning": {
        "name_he": "אזהרה (הוצאה לפועל)",
        "name_en": "Enforcement Warning",
        "patterns": [r"אזהרה", r"הוצאה לפועל"],
        "urgency": "URGENT",
        "default_deadline_days": 20,
    },
    "arnona_notice": {
        "name_he": "הודעת ארנונה",
        "name_en": "Arnona (Property Tax) Notice",
        "patterns": [r"ארנונה", r"שובר תשלום"],
        "urgency": "MEDIUM",
        "default_deadline_days": 60,
    },
    "discount_decision": {
        "name_he": "החלטה בעניין הנחה",
        "name_en": "Discount Decision",
        "patterns": [r"הנחה", r"ועדת הנחות"],
        "urgency": "LOW",
        "default_deadline_days": None,
    },
    "building_violation": {
        "name_he": "הודעה על חריגת בנייה",
        "name_en": "Building Violation Notice",
        "patterns": [r"חריגת בני", r"צו הריסה", r"עבירת בני"],
        "urgency": "URGENT",
        "default_deadline_days": 30,
    },
    "zoning_notice": {
        "name_he": "הודעה על תוכנית בניין עיר",
        "name_en": "Zoning/Planning Notice",
        "patterns": [r'תב"ע', r"תוכנית בניין עיר", r"הפקדת תוכנית"],
        "urgency": "MEDIUM",
        "default_deadline_days": 60,
    },
    "refund_notice": {
        "name_he": "הודעה על החזר",
        "name_en": "Refund Notice",
        "patterns": [r"החזר", r"זיכוי", r"יוחזר לחשבונך"],
        "urgency": "LOW",
        "default_deadline_days": None,
    },
    "information_request": {
        "name_he": "בקשה להשלמת מסמכים / בירורים",
        "name_en": "Information/Document Request",
        "patterns": [r"השלמת מסמכים", r"מכתב בירורים", r"נא להמציא", r"נא לצרף"],
        "urgency": "MEDIUM",
        "default_deadline_days": 30,
    },
    "reserve_duty": {
        "name_he": "צו מילואים / תגמולי מילואים",
        "name_en": "Reserve Duty Order/Compensation",
        "patterns": [r"מילואים", r"צו 8", r"תגמולי מילואים", r"דמי מילואים"],
        "urgency": "MEDIUM",
        "default_deadline_days": None,
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


def identify_sender(text: str) -> tuple[Optional[str], Optional[str], str]:
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
        return body["name_he"], body["name_en"], confidence
    return None, None, "LOW"


def identify_document_type(text: str) -> tuple[Optional[str], Optional[str], str, Optional[int]]:
    """Identify the type of document."""
    best_match = None
    best_score = 0

    for doc_id, doc_info in DOCUMENT_TYPES.items():
        score = 0
        for pattern in doc_info["patterns"]:
            matches = re.findall(pattern, text)
            score += len(matches)

        if score > best_score:
            best_score = score
            best_match = doc_id

    if best_match and best_score >= 1:
        doc = DOCUMENT_TYPES[best_match]
        return (
            doc["name_he"],
            doc["name_en"],
            doc["urgency"],
            doc["default_deadline_days"],
        )
    return None, None, "UNKNOWN", None


def extract_monetary_amounts(text: str) -> list[str]:
    """Extract monetary amounts from the document."""
    amounts = []

    # NIS amounts with various formats
    nis_patterns = [
        r"(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:ש[\"״]ח|שקלים|שקל|NIS|ILS|₪)",
        r"(?:ש[\"״]ח|שקלים|שקל|NIS|ILS|₪)\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",
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
        r"(?:תיק|אסמכתא|מס['׳]?)\s*[:.]?\s*(\d[\d/-]{4,})",
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
        if re.search(hebrew_name, text):
            # Try to find specific section numbers
            section_pattern = rf"סעיף\s*(\d+[א-ת]?(?:\(\d+\))?)\s*(?:ל|של\s*)?{hebrew_name}"
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
                general_pattern = rf"{hebrew_name}.*?סעיף\s*(\d+[א-ת]?)"
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


def extract_deadlines(text: str) -> list[dict]:
    """Extract deadline information from the document."""
    deadlines = []

    # Patterns like "within X days"
    day_patterns = [
        (r"תוך\s*(\d+)\s*ימים?\s*(?:מ(?:יום|קבלת|תאריך))?", "days from"),
        (r"לא\s*יאוחר\s*מ[- ]?(\d{1,2}[/.]\d{1,2}[/.]\d{2,4})", "by date"),
        (r"עד\s*(?:ליום|לתאריך)?\s*(\d{1,2}[/.]\d{1,2}[/.]\d{2,4})", "by date"),
        (r"(?:בתוך|תוך)\s*(\d+)\s*(?:חודשים|חודש)", "months from"),
    ]

    for pattern, dtype in day_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            deadlines.append({
                "type": dtype,
                "value": match,
                "raw_context": _get_context(text, match, 50),
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


def _get_context(text: str, match: str, window: int = 50) -> str:
    """Get surrounding context for a match."""
    idx = text.find(match)
    if idx == -1:
        return ""
    start = max(0, idx - window)
    end = min(len(text), idx + len(match) + window)
    return text[start:end].strip()


def analyze_document(text: str) -> AnalysisResult:
    """Main analysis function. Extracts all structured information."""
    result = AnalysisResult()

    # Identify sender
    sender_he, sender_en, sender_confidence = identify_sender(text)
    result.sender = sender_he
    result.sender_en = sender_en

    # Identify document type
    doc_he, doc_en, urgency, default_deadline = identify_document_type(text)
    result.document_type = doc_he
    result.document_type_en = doc_en
    result.urgency = urgency

    # Extract structured data
    result.monetary_amounts = extract_monetary_amounts(text)
    result.dates_found = extract_dates(text)
    result.reference_numbers = extract_reference_numbers(text)
    result.laws_referenced = extract_laws(text)
    result.deadlines = extract_deadlines(text)
    result.consequences = extract_consequences(text)
    result.required_actions = extract_required_actions(text)

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
    if not result.deadlines and default_deadline:
        result.notes.append(
            f"No explicit deadline found, but this document type typically has a {default_deadline}-day response window."
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


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Israeli government documents and extract structured information.",
        epilog="Example: python document-analyzer.py --file letter.txt --format json",
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--text",
        type=str,
        help="Document text to analyze (paste directly)",
    )
    input_group.add_argument(
        "--file",
        type=str,
        help="Path to a text file containing the document",
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    # Get document text
    if args.file:
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
