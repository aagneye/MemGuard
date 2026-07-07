"""Preset demo users for the public MemGuard demo.

These exist so judges/visitors can reset the whole demo cleanly by switching
users, without wiping real data or needing any login.
"""

DEMO_USERS: list[dict[str, str]] = [
    {"id": "demo_alice", "label": "Alice (Pro plan, IST)"},
    {"id": "demo_bob", "label": "Bob (fresh, no memories yet)"},
    {"id": "demo_carol", "label": "Carol (poisoning scenario seed)"},
]
