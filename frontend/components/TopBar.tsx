"use client";

import type { DemoUser } from "../lib/types";
import { API_BASE } from "../lib/api";

type Props = {
  demoUsers: DemoUser[];
  activeUserId: string;
  sessionId: string;
  onSwitchUser: (userId: string) => void;
  onNewSession: () => void;
  onResetDemo?: () => void;
};

export default function TopBar({ demoUsers, activeUserId, sessionId, onSwitchUser, onNewSession, onResetDemo }: Props) {
  async function handleReset() {
    try {
      await fetch(`${API_BASE}/demo/reset`, { method: "POST" });
      onResetDemo?.();
    } catch {
      // Best-effort reset
    }
  }

  return (
    <div className="topbar">
      <div className="topbar-title">
        <span className="topbar-badge">Acme Cloud Support</span>
        <span className="muted">MemGuard — Trust-Aware Memory Agent</span>
        <span
          className="muted"
          style={{ fontSize: "11px", color: "#475569", fontFamily: "monospace" }}
          title="Current session ID"
        >
          {sessionId}
        </span>
      </div>
      <div className="topbar-controls">
        <select value={activeUserId} onChange={(e) => onSwitchUser(e.target.value)} aria-label="Switch demo user">
          {demoUsers.map((user) => (
            <option key={user.id} value={user.id}>
              {user.label}
            </option>
          ))}
        </select>
        <button onClick={onNewSession} title="Starts a new session_id, keeps the same user_id">
          New Session
        </button>
        <button
          onClick={handleReset}
          title="Clear all demo user memories and events"
          style={{ background: "rgba(239,68,68,0.15)", color: "#f87171", border: "1px solid #f87171" }}
        >
          Reset Demo
        </button>
      </div>
    </div>
  );
}
