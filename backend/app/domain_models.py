from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from .domain_types import MemoryStatus, SourceType, TrustTier


def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


@dataclass
class FactCandidate:
    fact: str
    source_hint: SourceType
    confidence: float = 1.0


@dataclass
class MemoryEventRecord:
    event_type: str
    detail: dict
    created_at: datetime

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["created_at"] = self.created_at.isoformat()
        return payload


@dataclass
class MemoryView:
    id: str
    user_id: str
    fact_text: str
    trust_tier: TrustTier
    source: SourceType
    status: MemoryStatus
    ttl_days: int
    superseded_by: str | None
