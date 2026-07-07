import type { MemorySource, MemoryStatus, TrustTier } from "../lib/types";

export function TrustBadge({ tier }: { tier: TrustTier }) {
  return <span className={`tag ${tier}`}>{tier.toUpperCase()}</span>;
}

export function SourceBadge({ source }: { source: MemorySource }) {
  return <span className="tag">{source.replace("_", " ")}</span>;
}

export function StatusBadge({ status }: { status: MemoryStatus }) {
  return <span className="tag">{status}</span>;
}
