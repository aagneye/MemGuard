"""Internal domain models — not part of the API schema.

These dataclasses represent intermediate states used during processing
within the governance pipeline (extract → trust → conflict → persist).
"""
from dataclasses import dataclass

from .domain_types import SourceType


@dataclass
class FactCandidate:
    fact: str
    source_hint: SourceType
    confidence: float = 1.0


@dataclass
class MemoryEventRecord:
    user_id: str
    event_type: str
    detail: dict


@dataclass
class MemoryView:
    id: str
    fact_text: str
    trust_tier: str
    source: str
    status: str


@dataclass
class ResolveResult:
    memory_id: str
    new_status: str
    counterpart_id: str | None = None
    counterpart_new_status: str | None = None
