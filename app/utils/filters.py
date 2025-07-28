TRIGGER_KEYWORDS = [
    "refund", "warranty", "policy", "terms", "contract", "legal",
    "support hours", "delivery", "agreement", "invoice", "payment"
]

def needs_document_lookup(text: str) -> bool:
    if not text:
        return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in TRIGGER_KEYWORDS)
