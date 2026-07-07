SENSITIVE_KEYWORDS = ("refund", "admin access", "password", "billing", "plan-upgrade")


def is_sensitive_claim(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in SENSITIVE_KEYWORDS)
