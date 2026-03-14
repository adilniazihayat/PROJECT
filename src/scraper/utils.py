import re
from urllib.parse import urljoin

def clean_price(price_str):
    """Normalize price to numeric float."""
    if not price_str:
        return 0.0
    # Remove currency symbols and non-numeric characters except for the decimal point
    cleaned = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def resolve_url(base_url, relative_url):
    """Resolve relative links to absolute URLs."""
    return urljoin(base_url, relative_url)

def clean_text(text):
    """Clean whitespace and handle missing text."""
    if not text:
        return ""
    return " ".join(text.split())
