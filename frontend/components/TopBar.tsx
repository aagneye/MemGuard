"use client";

import type { DemoUser } from "../lib/types";

type Props = {
  demoUsers: DemoUser[];
  activeUserId: string;
  onSwitchUser: (userId: string) => void;
  onNewSession: () => void;
};

export default function TopBar({ demoUsers, activeUserId, onSwitchUser, onNewSession }: Props) {
  return (
    <div className="topbar">
      <div className="topbar-title">
        <span className="topbar-badge">Acme Cloud Support</span>
        <span className="muted">Trust-aware memory agent demo</span>
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
      </div>
    </div>
  );
}
