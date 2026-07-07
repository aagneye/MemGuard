"""Preset demo users for the public hackathon demo.

These users are pre-seeded by scripts/seed_demo_data.py to demonstrate
each of the 5 demo beats without requiring a real user account.
"""
from typing import TypedDict


class DemoUserDict(TypedDict):
    id: str
    label: str
    description: str


DEMO_USERS: list[DemoUserDict] = [
    {
        "id": "demo_alice",
        "label": "Alice (Support Tier Demo)",
        "description": "Primary demo user — has Pro plan, IST timezone, concise preference pre-loaded.",
    },
    {
        "id": "demo_bob",
        "label": "Bob (Fresh User)",
        "description": "Clean slate — no memories. Use to demonstrate first-session capture.",
    },
    {
        "id": "demo_carol",
        "label": "Carol (Poisoning Demo)",
        "description": "Has a pre-loaded poisoning attempt from a forwarded email document.",
    },
]
