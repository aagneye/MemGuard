"use client";

import { groupMemoriesByConflict } from "../lib/conflictPairs";
import type { MemoryItem, ResolveAction } from "../lib/types";
import { SourceBadge, StatusBadge, TrustBadge } from "./TrustBadge";

type Props = {
  memories: MemoryItem[];
  onResolve: (memoryId: string, action: ResolveAction) => void;
};

function DecayBadge({ daysRemaining }: { daysRemaining: number | null }) {
  if (daysRemaining === null) return null;
  const days = Math.ceil(daysRemaining);
  const urgent = days <= 3;
  return (
    <span
      className="badge"
      style={{
        background: urgent ? "rgba(239,68,68,0.15)" : "rgba(100,116,139,0.2)",
        color: urgent ? "#f87171" : "#94a3b8",
        fontSize: "10px",
      }}
      title={`Expires in ~${days} day${days !== 1 ? "s" : ""}`}
    >
      ⏱ {days}d
    </span>
  );
}

export default function MemoryInspector({ memories, onResolve }: Props) {
  const { standalone, conflictPairs } = groupMemoriesByConflict(memories);

  return (
    <aside className="memory-panel">
      <h3>Memory Inspector</h3>
      <p className="muted">Live view of this user&apos;s stored memories — trust tier, source, and status.</p>

      {conflictPairs.map((pair) => (
        <div className="memory-card conflict-card" key={pair.oldMemory.id}>
          <div className="conflict-row">
            <span className="conflict-label">Old</span>
            <TrustBadge tier={pair.oldMemory.trust_tier} />
            <SourceBadge source={pair.oldMemory.source} />
            <DecayBadge daysRemaining={pair.oldMemory.days_remaining} />
          </div>
          <p>{pair.oldMemory.fact_text}</p>
          <div className="conflict-row">
            <span className="conflict-label">New</span>
            <TrustBadge tier={pair.newMemory.trust_tier} />
            <SourceBadge source={pair.newMemory.source} />
          </div>
          <p>{pair.newMemory.fact_text}</p>
          <div className="row">
            <button onClick={() => onResolve(pair.newMemory.id, "accept")}>Accept new</button>
            <button onClick={() => onResolve(pair.newMemory.id, "reject")}>Keep old</button>
          </div>
        </div>
      ))}

      {standalone.map((memory) => (
        <div className="memory-card" key={memory.id}>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "4px", alignItems: "center" }}>
            <TrustBadge tier={memory.trust_tier} />
            <SourceBadge source={memory.source} />
            <StatusBadge status={memory.status} />
            <DecayBadge daysRemaining={memory.days_remaining} />
          </div>
          <p>{memory.fact_text}</p>
          {memory.status === "conflicted" && (
            <div className="row">
              <button onClick={() => onResolve(memory.id, "accept")}>Accept</button>
              <button onClick={() => onResolve(memory.id, "reject")}>Reject</button>
            </div>
          )}
        </div>
      ))}

      {memories.length === 0 && <p className="muted">No memories yet for this user.</p>}

      <div className="trust-legend">
        <span style={{ color: "#4ade80" }}>■ High</span>
        <span style={{ color: "#facc15" }}>■ Medium</span>
        <span style={{ color: "#f87171" }}>■ Low</span>
        <span style={{ color: "#94a3b8", marginLeft: "8px" }}>⏱ = days until decay</span>
      </div>
    </aside>
  );
}
