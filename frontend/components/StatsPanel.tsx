"use client";

import { useEffect, useState } from "react";
import { API_BASE } from "../lib/api";

interface UserStats {
  total_memories: number;
  by_trust_tier: Record<string, number>;
  by_status: Record<string, number>;
  by_source: Record<string, number>;
  events_by_type: Record<string, number>;
}

interface Props {
  userId: string;
}

export default function StatsPanel({ userId }: Props) {
  const [stats, setStats] = useState<UserStats | null>(null);

  useEffect(() => {
    if (!userId) return;
    fetch(`${API_BASE}/stats?user_id=${encodeURIComponent(userId)}`)
      .then((r) => r.json())
      .then((data: UserStats) => setStats(data))
      .catch(() => {});
  }, [userId]);

  if (!stats) return null;

  return (
    <div
      style={{
        padding: "10px 16px",
        borderTop: "1px solid #1e293b",
        fontSize: "11px",
        color: "#64748b",
        display: "flex",
        gap: "16px",
        flexWrap: "wrap",
      }}
    >
      <span title="Total memories in store">
        <strong style={{ color: "#94a3b8" }}>{stats.total_memories}</strong> memories
      </span>
      <span title="Active memories">
        <strong style={{ color: "#4ade80" }}>{stats.by_status?.active ?? 0}</strong> active
      </span>
      <span title="Conflicted memories awaiting resolution">
        <strong style={{ color: "#facc15" }}>{stats.by_status?.conflicted ?? 0}</strong> conflicts
      </span>
      <span title="Flagged poisoning attempts">
        <strong style={{ color: "#f87171" }}>{stats.events_by_type?.flagged_poisoning ?? 0}</strong> flagged
      </span>
      <span title="Memories that have expired">
        <strong style={{ color: "#94a3b8" }}>{stats.by_status?.expired ?? 0}</strong> expired
      </span>
    </div>
  );
}
