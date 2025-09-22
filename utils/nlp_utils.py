import re

def extract_fields(text: str):
    data = {"raw_text": text}

    # Invoice number (look for "No:" followed by alphanum)
    match_no = re.search(r"(?:Invoice|Inv|Bill)\s*(?:No\.?|Number)?[:\s-]*([A-Za-z0-9\-\/]+)", text, re.IGNORECASE)
    if match_no:
        data["invoice_no"] = match_no.group(1)

    # Invoice date (dd-mm-yyyy or dd/mm/yyyy or Month dd, yyyy)
    match_date = re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\w+\s+\d{1,2},\s*\d{4})", text)
    if match_date:
        data["invoice_date"] = match_date.group(1)

    # Total amount
    match_total = re.search(r"(?:Total|Amount\s*Due|Grand\s*Total)[:\s]*[₹$]?\s*([0-9,]+\.?[0-9]*)", text, re.IGNORECASE)
    if match_total:
        try:
            data["total"] = float(match_total.group(1).replace(",", ""))
        except:
            data["total"] = match_total.group(1)

    return data
