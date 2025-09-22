import re

def extract_fields(text: str):
    """
    Extract key invoice fields from OCR text using regex patterns.
    """
    data = {"raw_text": text}

    # Invoice number
    match_no = re.search(r"(?:Invoice|Inv|Bill)\s*(?:No\.?|Number)?[:\s-]*([A-Za-z0-9\-\/]+)", text, re.IGNORECASE)
    if match_no:
        data["invoice_no"] = match_no.group(1)

    # Invoice date
    match_date = re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\w+\s+\d{1,2},\s*\d{4})", text)
    if match_date:
        data["invoice_date"] = match_date.group(1)

    # Subtotal
    match_sub = re.search(r"(?:Subtotal)[:\s]*[₹$]?\s*([0-9,]+\.?[0-9]*)", text, re.IGNORECASE)
    if match_sub:
        data["subtotal"] = match_sub.group(1)

    # Tax
    match_tax = re.search(r"(?:Tax)[:\s]*[₹$]?\s*([0-9,]+\.?[0-9]*)", text, re.IGNORECASE)
    if match_tax:
        data["tax"] = match_tax.group(1)

    # Total
    match_total = re.search(r"(?:Total|Amount\s*Due|Grand\s*Total)[:\s]*[₹$]?\s*([0-9,]+\.?[0-9]*)", text, re.IGNORECASE)
    if match_total:
        data["total"] = match_total.group(1)

    return data
