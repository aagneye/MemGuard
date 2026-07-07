"""Poisoning detection — flags sensitive claims from low-trust sources.

Checks if a fact text contains keywords that would be dangerous if accepted
as true from an external document or unverified source.

Extended keyword list covers common memory injection attack patterns:
  - Entitlement escalation (refund, admin access, override)
  - Credential theft (password, token, key)
  - Billing manipulation (billing, plan-upgrade, charge-reversal)
  - Role/permission escalation (superuser, root, sudo)
"""

SENSITIVE_KEYWORDS = (
    "refund",
    "admin access",
    "administrator",
    "password",
    "billing",
    "plan-upgrade",
    "override",
    "overrule",
    "bypass",
    "superuser",
    "root access",
    "sudo",
    "grant access",
    "grant permission",
    "entitlement",
    "charge reversal",
    "chargeback",
    "waive fee",
)


def is_sensitive_claim(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in SENSITIVE_KEYWORDS)
