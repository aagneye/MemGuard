"use client";

import { groupMemoriesByConflict } from "../lib/conflictPairs";
import type { MemoryItem, ResolveAction } from "../lib/types";
import { SourceBadge, StatusBadge, TrustBadge } from "./TrustBadge";

type Props = {
  memories: MemoryItem[];
  onResolve: (memoryId: string, action: ResolveAction) => void;
};

export default function MemoryInspector({ memories, onResolve }: Props) {
  const { standalone, conflictPairs } = groupMemoriesByConflict(memories);

  return (
    <aside className="memory-panel">
      <h3>Memory Inspector</h3>
      <p className="muted">Live view of this user's stored memories — trust tier, source, and status.</p>

      {conflictPairs.map((pair) => (
        <div className="memory-card conflict-card" key={pair.oldMemory.id}>
          <div className="conflict-row">
            <span className="conflict-label">Old</span>
            <TrustBadge tier={pair.oldMemory.trust_tier} />
            <SourceBadge source={pair.oldMemory.source} />
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
          <div>
            <TrustBadge tier={memory.trust_tier} />
            <SourceBadge source={memory.source} />
            <StatusBadge status={memory.status} />
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
    </aside>
  );
}
