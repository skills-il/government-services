#!/usr/bin/env python3
"""
Israeli Government Form Field Helper

Validates and populates common Israeli government form fields:
- Teudat Zehut (ID number) with check digit validation
- Israeli phone numbers (mobile and landline)
- Israeli addresses with mikud (postal code)
- Common form field templates, including who fills each form and who receives it

Usage:
    python fill_form.py --help
    python fill_form.py validate-tz 123456782
    python fill_form.py validate-phone 0521234567
    python fill_form.py validate-address --city "תל אביב" --street "רוטשילד" --number 1 --mikud 6688101
    python fill_form.py validate-iban IL620108000000099999999
    python fill_form.py form-fields --form tofes-101
    python fill_form.py form-fields --list
"""

import argparse
import json
import re
import sys


def validate_teudat_zehut(id_number: str) -> dict:
    """Validate Israeli Teudat Zehut (ID number) with check digit."""
    raw = id_number.strip()
    if not raw:
        return {"valid": False, "error": "Empty ID number", "input": id_number}
    id_str = raw.zfill(9)

    # ASCII digits only: str.isdigit() also accepts full-width and Arabic-Indic
    # digits, which a government portal would reject or mis-store.
    if len(id_str) != 9 or not re.fullmatch(r"[0-9]{9}", id_str):
        return {"valid": False, "error": "Must be 9 digits", "input": id_number}

    # Reject placeholder/test ID: 000000000 passes Luhn but is not a real ID
    if id_str == "000000000":
        return {
            "valid": False,
            "error": "Placeholder ID (all zeros) is not a real Teudat Zehut",
            "input": id_number,
        }

    total = 0
    for i, digit in enumerate(id_str):
        val = int(digit) * (1 + (i % 2))
        if val > 9:
            val -= 9
        total += val

    is_valid = total % 10 == 0
    return {
        "valid": is_valid,
        "formatted": id_str,
        "input": id_number,
        "error": None if is_valid else "Check digit validation failed",
    }


def validate_israeli_phone(phone: str) -> dict:
    """Validate Israeli phone number (mobile or landline)."""
    cleaned = re.sub(r"[\s\-\(\)]", "", phone.strip())

    # Convert international format to local
    cleaned = cleaned.replace(".", "")
    for prefix in ("+972", "00972", "972"):
        if cleaned.startswith(prefix):
            rest = cleaned[len(prefix):]
            # "+972-0-52..." keeps the trunk zero; drop it once.
            cleaned = rest if rest.startswith("0") else "0" + rest
            break

    # Format-level check against the Ministry of Communications numbering plan
    # (February 2023 edition). It validates structure only, NOT carrier or
    # whether the number is assigned:
    #   mobile      05R-NXX-XXXX  10 digits (any 05X; number portability means a
    #               prefix never identifies the carrier)
    #   geographic  0A-NXX-XXXX    9 digits, A in {2,3,4,8,9}, N = 2-9
    #   national    07P-NXX-XXXX  10 digits, P = 2-9, N = 2-9 (VoIP / cable lines)
    mobile_pattern = r"^05[0-9]{8}$"
    geographic_pattern = r"^0[23489][2-9][0-9]{6}$"
    national_pattern = r"^07[2-9][2-9][0-9]{6}$"

    if re.match(mobile_pattern, cleaned):
        formatted = f"{cleaned[:3]}-{cleaned[3:]}"
        phone_type = "mobile"
        international = f"+972-{cleaned[1:3]}-{cleaned[3:]}"
    elif re.match(national_pattern, cleaned):
        formatted = f"{cleaned[:3]}-{cleaned[3:]}"
        phone_type = "national (07X)"
        international = f"+972-{cleaned[1:3]}-{cleaned[3:]}"
    elif re.match(geographic_pattern, cleaned):
        formatted = f"{cleaned[:2]}-{cleaned[2:]}"
        phone_type = "landline"
        international = f"+972-{cleaned[1:2]}-{cleaned[2:]}"
    else:
        return {"valid": False, "error": "Invalid Israeli phone number", "input": phone}

    return {
        "valid": True,
        "formatted": formatted,
        "international": international,
        "type": phone_type,
        "input": phone,
    }


def validate_israeli_address(city: str, street: str, number: str, mikud: str = "", apartment: str = "") -> dict:
    """Validate Israeli address fields."""
    errors = []

    if not city or not city.strip():
        errors.append("City (yishuv) is required")

    if not street or not street.strip():
        errors.append("Street (rechov) is required")

    if not number or not number.strip():
        errors.append("House number is required")

    mikud_clean = mikud.strip().replace("-", "").replace(" ", "") if mikud else ""
    if mikud:
        if not re.fullmatch(r"[0-9]{7}", mikud_clean):
            errors.append("Mikud (postal code) must be 7 digits")

    if errors:
        return {"valid": False, "errors": errors}

    address_parts = [f"{street.strip()} {number.strip()}"]
    if apartment:
        address_parts[0] += f", דירה {apartment.strip()}"
    address_parts.append(city.strip())
    if mikud_clean:
        address_parts[-1] += f", {mikud_clean}"

    return {
        "valid": True,
        "formatted": "\n".join(address_parts),
        "fields": {
            "city": city.strip(),
            "street": street.strip(),
            "house_number": number.strip(),
            "apartment": apartment.strip() if apartment else None,
            "mikud": mikud_clean or None,
        },
    }


def validate_israeli_iban(iban: str) -> dict:
    """Validate Israeli IBAN.

    Israeli IBAN format: IL + 2 check digits + 3 bank + 3 branch + 13 account = 23 chars total.
    Used in Bituach Leumi grant claims, tax refund requests, salary forms.
    """
    cleaned = re.sub(r"\s+", "", iban.strip()).upper()

    if len(cleaned) != 23:
        return {
            "valid": False,
            "error": f"Israeli IBAN must be 23 characters, got {len(cleaned)}",
            "input": iban,
        }

    if not cleaned.startswith("IL"):
        return {"valid": False, "error": "Israeli IBAN must start with 'IL'", "input": iban}

    if not re.fullmatch(r"[0-9]{21}", cleaned[2:]):
        return {
            "valid": False,
            "error": "Characters after 'IL' must all be digits",
            "input": iban,
        }

    # ISO 13616 mod-97 check: move 4 leading chars to end, replace letters with digits
    rearranged = cleaned[4:] + cleaned[:4]
    numeric = ""
    for ch in rearranged:
        if ch.isalpha():
            numeric += str(ord(ch) - ord("A") + 10)
        else:
            numeric += ch
    is_valid = int(numeric) % 97 == 1

    return {
        "valid": is_valid,
        "formatted": cleaned,
        "bank": cleaned[4:7],
        "branch": cleaned[7:10],
        "account": cleaned[10:],
        "input": iban,
        "error": None if is_valid else "IBAN mod-97 check failed",
    }


# Common government form field mappings.
# "filled_by" says who completes the form. A form issued by someone else (106)
# is listed only so the agent can READ its figures; never fabricate one.
FORM_FIELDS = {
    "tofes-101": {
        "name": "Employee card and request for tax relief / טופס 101 (כרטיס עובד)",
        "filled_by": "employee or pensioner",
        "submitted_to": "the employer or pension payer (not the Tax Authority)",
        "deadline": "within 7 days of starting work or of the first salary (earlier of the two), every 1 January (some pensioners aged 70+ and allowance recipients may be exempt if nothing changed), and within 7 days of any change",
        "related": "Form 119 (academic degree / vocational certificate benefit) is attached to the 101",
        "attachments": "copy of Teudat Zehut + appendix (ספח) at the start of work or after a change, plus documents for each relief claimed",
        "note": "The employee declares facts; the employer's payroll computes credit points. Do not enter a credit-point number.",
        "fields": [
            {"name": "shem_prati", "label": "First Name / שם פרטי", "type": "text", "required": True},
            {"name": "shem_mishpacha", "label": "Last Name / שם משפחה", "type": "text", "required": True},
            {"name": "mispar_zehut", "label": "ID Number / מספר זהות", "type": "tz", "required": True},
            {"name": "taarich_leida", "label": "Date of Birth / תאריך לידה", "type": "date", "required": True},
            {"name": "matsav_mishpachti", "label": "Marital Status / מצב משפחתי", "type": "select", "required": True},
            {"name": "ktovet", "label": "Address / כתובת", "type": "address", "required": True},
            {"name": "telefon", "label": "Phone / טלפון", "type": "phone", "required": True},
            {"name": "maasik", "label": "Employer / מעסיק", "type": "text", "required": True},
            {"name": "yeladim", "label": "Children (declared facts) / ילדים", "type": "list", "required": False},
            {"name": "hachnasot_nosafot", "label": "Other income or second employer / הכנסות נוספות", "type": "select", "required": True},
        ],
    },
    "tofes-106": {
        "name": "Annual salary summary / טופס 106",
        "filled_by": "ISSUED BY THE EMPLOYER, read-only for the user",
        "submitted_to": "given by the employer to the employee",
        "note": "Never fill or invent a 106. Ask the employer for it and read its figures into the annual return.",
        "fields": [
            {"name": "shem_maasik", "label": "Employer Name / שם מעסיק", "type": "text", "required": True},
            {"name": "shnat_mas", "label": "Tax Year / שנת מס", "type": "number", "required": True},
            {"name": "sachar_bruto", "label": "Gross Salary / שכר ברוטו", "type": "number", "required": True},
            {"name": "mas_shnukai", "label": "Tax Deducted / מס שנוכה", "type": "number", "required": True},
        ],
    },
    "dmei-leida": {
        "name": "Maternity pay claim / תביעה לדמי לידה",
        "filled_by": "the mother; the employer completes its own section",
        "submitted_to": "Bituach Leumi (personal service ps.btl.gov.il)",
        "note": "Except after a home birth (which always needs a claim), check first whether payment is automatic (self-employed; employer with a Bituach Leumi arrangement files for her; pregnancy-preservation benefit up to the birth; unemployment pay up to a month before). File within 12 months of the first day of entitlement; the online form opens only after the birth. Each employer confirms work months and salary for the 10 months before she stopped working.",
        "fields": [
            {"name": "shem_prati", "label": "First Name / שם פרטי", "type": "text", "required": True},
            {"name": "mispar_zehut", "label": "ID Number / מספר זהות", "type": "tz", "required": True},
            {"name": "taarich_leida_yeled", "label": "Child Birth Date / תאריך לידת הילד", "type": "date", "required": True},
            {"name": "maasik", "label": "Employer / מעסיק", "type": "text", "required": True},
            {"name": "taarich_hafsakah", "label": "Work Stop Date / תאריך הפסקת עבודה", "type": "date", "required": True},
            {"name": "iban", "label": "Bank account the claim form asks for / חשבון הבנק שהטופס מבקש", "type": "iban", "required": True},
        ],
    },
    "rishum-chevra": {
        "name": "Company Registration / רישום חברה",
        "filled_by": "the founder, entering תאגידים ברשת through national identification",
        "submitted_to": "Companies Registrar (ica.justice.gov.il/IcaSite)",
        "note": "Prepare Hebrew name proposals in priority order (the 2017 smart-card manual required three; follow what the current form asks). Each shareholder and director then approves online.",
        "fields": [
            {"name": "shem_chevra_1", "label": "Company Name Option 1 / שם חברה 1", "type": "text", "required": True},
            {"name": "shem_chevra_2", "label": "Company Name Option 2 / שם חברה 2", "type": "text", "required": False},
            {"name": "shem_chevra_3", "label": "Company Name Option 3 / שם חברה 3", "type": "text", "required": False},
            {"name": "hon_meniayot", "label": "Share Capital / הון מניות", "type": "number", "required": True},
            {"name": "ktovet_chevra", "label": "Company Address / כתובת החברה", "type": "address", "required": True},
            {"name": "shem_meyased", "label": "Founder Name / שם מייסד", "type": "text", "required": True},
            {"name": "tz_meyased", "label": "Founder ID / ת.ז. מייסד", "type": "tz", "required": True},
        ],
    },
}


def get_form_fields(form_name: str) -> dict:
    """Get field definitions for a known government form."""
    if form_name in FORM_FIELDS:
        return FORM_FIELDS[form_name]
    return {"error": f"Unknown form: {form_name}", "available_forms": list(FORM_FIELDS.keys())}


def main():
    parser = argparse.ArgumentParser(description="Israeli Government Form Field Helper")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # validate-tz
    tz_parser = subparsers.add_parser("validate-tz", help="Validate Teudat Zehut number")
    tz_parser.add_argument("id_number", help="9-digit Israeli ID number")

    # validate-phone
    phone_parser = subparsers.add_parser("validate-phone", help="Validate Israeli phone number")
    phone_parser.add_argument("phone", help="Israeli phone number")

    # validate-address
    addr_parser = subparsers.add_parser("validate-address", help="Validate Israeli address")
    addr_parser.add_argument("--city", required=True, help="City name")
    addr_parser.add_argument("--street", required=True, help="Street name")
    addr_parser.add_argument("--number", required=True, help="House number")
    addr_parser.add_argument("--mikud", default="", help="Postal code (7 digits)")
    addr_parser.add_argument("--apartment", default="", help="Apartment number")

    # validate-iban
    iban_parser = subparsers.add_parser("validate-iban", help="Validate Israeli IBAN")
    iban_parser.add_argument("iban", help="Israeli IBAN (23 chars, starts with IL)")

    # form-fields
    form_parser = subparsers.add_parser("form-fields", help="Get form field definitions")
    form_parser.add_argument("--form", help="Form name (e.g., tofes-101)")
    form_parser.add_argument("--list", action="store_true", help="List available forms")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "validate-tz":
        result = validate_teudat_zehut(args.id_number)
    elif args.command == "validate-phone":
        result = validate_israeli_phone(args.phone)
    elif args.command == "validate-address":
        result = validate_israeli_address(args.city, args.street, args.number, args.mikud, args.apartment)
    elif args.command == "validate-iban":
        result = validate_israeli_iban(args.iban)
    elif args.command == "form-fields":
        if args.list or not args.form:
            result = {"available_forms": list(FORM_FIELDS.keys())}
        else:
            result = get_form_fields(args.form)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
