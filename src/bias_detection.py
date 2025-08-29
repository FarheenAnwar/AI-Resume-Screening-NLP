import re

BIAS_TERMS = ["young", "energetic", "native english", "recent graduate", "digital native"]

def detect_sensitive_terms(text):
    found = []
    for term in BIAS_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", text, re.IGNORECASE):
            found.append(term)
    return found

def debias_text(text):
    for term in BIAS_TERMS:
        text = re.sub(rf"\b{re.escape(term)}\b", "", text, flags=re.IGNORECASE)
    return text.strip()
