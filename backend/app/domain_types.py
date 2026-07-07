from typing import Literal

TrustTier = Literal["high", "medium", "low"]
SourceType = Literal["user_stated", "tool_inferred", "document_extracted"]
MemoryStatus = Literal["active", "conflicted", "expired", "superseded"]
ResolveAction = Literal["accept", "reject", "supersede"]
