export type TrustTier = "high" | "medium" | "low";
export type MemorySource = "user_stated" | "tool_inferred" | "document_extracted";
export type MemoryStatus = "active" | "conflicted" | "expired" | "superseded";
export type MemoryEventType = "stored" | "flagged" | "conflict";

export type DemoUser = {
  id: string;
  label: string;
};

export type MemoryEvent = {
  event_type: string;
  type: MemoryEventType;
  fact: string;
  trust_tier: TrustTier | null;
  detail: Record<string, unknown>;
};

export type MemoryItem = {
  id: string;
  user_id: string;
  fact_text: string;
  trust_tier: TrustTier;
  source: MemorySource;
  status: MemoryStatus;
  ttl_days: number;
  superseded_by: string | null;
  conflicts_with: string | null;
  created_at: string;
  days_remaining: number | null;
};

export type ChatResponse = {
  reply: string;
  memory_events: MemoryEvent[];
};

export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  events?: MemoryEvent[];
};

export type ResolveAction = "accept" | "reject" | "supersede";
