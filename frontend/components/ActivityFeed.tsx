"use client";

import type { MemoryEvent } from "../lib/types";

interface Props {
  events: MemoryEvent[];
}

const EVENT_ICON: Record<string, string> = {
  stored: "📌",
  conflict_detected: "⚠️",
  flagged_poisoning: "🛡️",
  resolved_accept: "✅",
  resolved_reject: "❌",
  touched: "🔄",
  expired: "⏱️",
};

const EVENT_COLOR: Record<string, string> = {
  stored: "#4ade80",
  conflict_detected: "#facc15",
  flagged_poisoning: "#f87171",
  resolved_accept: "#34d399",
  resolved_reject: "#94a3b8",
  touched: "#60a5fa",
  expired: "#94a3b8",
};

export default function ActivityFeed({ events }: Props) {
  const reversed = [...events].reverse();

  return (
    <section className="activity-feed">
      <h4 style={{ margin: "0 0 8px", fontSize: "13px", color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.06em" }}>
        Governance Log
      </h4>
      {reversed.length === 0 && <p className="muted" style={{ fontSize: "12px" }}>No events yet — send a message.</p>}
      <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "6px" }}>
        {reversed.map((event, idx) => (
          <li
            key={idx}
            style={{
              fontSize: "12px",
              display: "flex",
              gap: "6px",
              alignItems: "flex-start",
              color: EVENT_COLOR[event.event_type] ?? "#e2e8f0",
            }}
          >
            <span style={{ flexShrink: 0 }}>{EVENT_ICON[event.event_type] ?? "•"}</span>
            <span>
              <strong>{event.event_type.replace(/_/g, " ")}</strong>
              {event.fact ? (
                <span style={{ color: "#94a3b8" }}> — {event.fact.slice(0, 60)}{event.fact.length > 60 ? "…" : ""}</span>
              ) : null}
              {event.trust_tier ? (
                <span style={{ color: "#64748b" }}> [{event.trust_tier}]</span>
              ) : null}
            </span>
          </li>
        ))}
      </ul>
    </section>
  );
}
