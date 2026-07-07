"use client";

import { FormEvent, useState } from "react";
import type { MemoryItem } from "../lib/types";
import { API_BASE } from "../lib/api";
import Spinner from "./Spinner";

interface Props {
  userId: string;
}

export default function MemorySearchPanel({ userId }: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<MemoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  async function handleSearch(e: FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setSearched(false);
    try {
      const res = await fetch(
        `${API_BASE}/memories/search?user_id=${encodeURIComponent(userId)}&q=${encodeURIComponent(query)}&top_k=5`
      );
      if (res.ok) {
        setResults(await res.json());
      }
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
      setSearched(true);
    }
  }

  return (
    <div className="memory-search-panel">
      <h4
        style={{
          margin: "0 0 8px",
          fontSize: "13px",
          color: "#94a3b8",
          textTransform: "uppercase",
          letterSpacing: "0.06em",
        }}
      >
        Search Memories
      </h4>
      <form onSubmit={handleSearch} style={{ display: "flex", gap: "6px" }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search user's memories…"
          style={{ flex: 1, fontSize: "13px", padding: "6px 8px" }}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !query.trim()} style={{ fontSize: "13px", padding: "6px 12px" }}>
          {loading ? <Spinner size="sm" /> : "Search"}
        </button>
      </form>
      {searched && results.length === 0 && (
        <p className="muted" style={{ fontSize: "12px", marginTop: "6px" }}>
          No matching memories found.
        </p>
      )}
      {results.length > 0 && (
        <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0", display: "flex", flexDirection: "column", gap: "4px" }}>
          {results.map((m) => (
            <li
              key={m.id}
              style={{
                fontSize: "12px",
                padding: "6px 8px",
                background: "#0f172a",
                borderRadius: "6px",
                border: "1px solid #1e293b",
              }}
            >
              <span
                style={{
                  color: m.trust_tier === "high" ? "#4ade80" : m.trust_tier === "medium" ? "#facc15" : "#f87171",
                  fontWeight: 700,
                  marginRight: "6px",
                }}
              >
                [{m.trust_tier.toUpperCase()}]
              </span>
              {m.fact_text}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
