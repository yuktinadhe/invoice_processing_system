from datetime import datetime

def validate_date(date_str: str) -> bool:
    """
    Check if date is valid (dd-mm-yyyy, dd/mm/yyyy, or Month dd, yyyy).
    """
    if not date_str:
        return False

    formats = ["%d-%m-%Y", "%d/%m/%Y", "%d-%m-%y", "%d/%m/%y", "%B %d, %Y"]
    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)
            return True
        except ValueError:
            continue
    return False


def validate_amount(amount_str: str) -> bool:
    """
    Check if amount is a valid number.
    """
    if not amount_str:
        return False
    try:
        float(amount_str.replace(",", "").replace("₹", "").replace("$", ""))
        return True
    except:
        return False
