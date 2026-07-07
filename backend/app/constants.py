"""Named constants used across the MemGuard backend.

Centralising magic numbers here makes them easy to find, reason about,
and tune without hunting through module-level variables.
"""

# Trust tier TTL defaults (days) — matches service_trust.py SOURCE_RULES
TTL_HIGH_TRUST_DAYS = 180
TTL_MEDIUM_TRUST_DAYS = 60
TTL_LOW_TRUST_DAYS = 14

# Conflict detection
CONFLICT_SIMILARITY_THRESHOLD = 0.85

# Session history window sent to the LLM
MAX_SESSION_HISTORY_TURNS = 10

# Embedding
EMBEDDING_DIMENSION = 1024
EMBEDDING_MODEL = "text-embedding-v3"

# Embedding cache
MAX_EMBED_CACHE_SIZE = 512

# Rate limiting
DEFAULT_RATE_LIMIT_RPM = 60

# Demo
DEMO_USERS_IDS = ("demo_alice", "demo_bob", "demo_carol")
