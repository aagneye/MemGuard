"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

type EventItem = { event_type: string; detail: Record<string, unknown> };
type MemoryItem = {
  id: string;
  fact_text: string;
  trust_tier: "high" | "medium" | "low";
  source: string;
  status: "active" | "conflicted" | "expired" | "superseded";
};
type TeamInvite = { id: string; email: string; invited_by: string; status: string; created_at: string };
type TeamItem = { id: string; name: string; owner_user_id: string; members: string[]; invites: TeamInvite[] };
type UserProfile = { id: string; email: string; name: string; picture?: string | null };

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<UserProfile | null>(null);
  const [userId, setUserId] = useState("");
  const [sessionId, setSessionId] = useState("session_1");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Array<{ role: "user" | "bot"; content: string }>>([]);
  const [events, setEvents] = useState<EventItem[]>([]);
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [teams, setTeams] = useState<TeamItem[]>([]);
  const [teamName, setTeamName] = useState("");
  const [inviteEmail, setInviteEmail] = useState("");
  const [selectedTeamId, setSelectedTeamId] = useState("");

  const conflicted = useMemo(() => memories.filter((m) => m.status === "conflicted"), [memories]);

  useEffect(() => {
    const token = localStorage.getItem("memguard_token");
    const rawUser = localStorage.getItem("memguard_user");
    if (!token || !rawUser) {
      router.push("/");
      return;
    }
    const parsed = JSON.parse(rawUser) as UserProfile;
    setUser(parsed);
    setUserId(parsed.id);
  }, [router]);

  async function loadMemories(uid = userId) {
    if (!uid) return;
    const res = await fetch(`${API_BASE}/memories?user_id=${encodeURIComponent(uid)}`);
    if (res.ok) setMemories(await res.json());
  }

  async function loadTeams(uid = userId) {
    if (!uid) return;
    const res = await fetch(`${API_BASE}/teams?user_id=${encodeURIComponent(uid)}`);
    if (!res.ok) return;
    const data: TeamItem[] = await res.json();
    setTeams(data);
    if (!selectedTeamId && data.length > 0) setSelectedTeamId(data[0].id);
  }

  useEffect(() => {
    if (!userId) return;
    void loadMemories(userId);
    void loadTeams(userId);
  }, [userId]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!message.trim()) return;
    const userMsg = message.trim();
    setMessage("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, session_id: sessionId, message: userMsg }),
    });
    if (!res.ok) return;
    const payload = await res.json();
    setMessages((prev) => [...prev, { role: "bot", content: payload.reply }]);
    setEvents(payload.memory_events ?? []);
    await loadMemories();
  }

  async function resolve(memoryId: string, action: "accept" | "reject" | "supersede") {
    const body: Record<string, string> = { action };
    if (action === "supersede") {
      const text = window.prompt("New fact text");
      if (!text) return;
      body.supersede_fact_text = text;
    }
    await fetch(`${API_BASE}/memories/${memoryId}/resolve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    await loadMemories();
  }

  async function createTeam() {
    if (!teamName.trim() || !userId) return;
    await fetch(`${API_BASE}/teams`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: teamName.trim(), owner_user_id: userId }),
    });
    setTeamName("");
    await loadTeams();
  }

  async function inviteMember() {
    if (!selectedTeamId || !inviteEmail.trim() || !userId) return;
    await fetch(`${API_BASE}/teams/${selectedTeamId}/invite`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: inviteEmail.trim(), invited_by: userId }),
    });
    setInviteEmail("");
    await loadTeams();
  }

  function logout() {
    localStorage.removeItem("memguard_token");
    localStorage.removeItem("memguard_user");
    router.push("/");
  }

  return (
    <main className="dashboard-shell">
      <aside className="drawer">
        <h3>MemGuard</h3>
        <p className="muted">{user?.name ?? "User"}</p>
        <button onClick={logout}>Logout</button>
        <hr />
        <h4>Workspace</h4>
        <p className="muted">Create teams and invite members.</p>
        <input value={teamName} onChange={(e) => setTeamName(e.target.value)} placeholder="New team name" />
        <button onClick={createTeam}>Create Team</button>
        <select value={selectedTeamId} onChange={(e) => setSelectedTeamId(e.target.value)}>
          <option value="">Select Team</option>
          {teams.map((team) => (
            <option key={team.id} value={team.id}>
              {team.name}
            </option>
          ))}
        </select>
        <input value={inviteEmail} onChange={(e) => setInviteEmail(e.target.value)} placeholder="Invite email" />
        <button onClick={inviteMember}>Send Invite</button>
        <hr />
        <h4>Drawer Ideas</h4>
        <ul className="small-list">
          <li>Profile settings</li>
          <li>API keys and usage</li>
          <li>Memory policy controls</li>
          <li>Audit and event logs</li>
          <li>Billing and plan</li>
        </ul>
      </aside>

      <section className="chat-panel">
        <h2>Agent Console</h2>
        <div className="row">
          <input value={userId} onChange={(e) => setUserId(e.target.value)} placeholder="user id" />
          <select value={sessionId} onChange={(e) => setSessionId(e.target.value)}>
            <option value="session_1">Session 1</option>
            <option value="session_2">Session 2</option>
            <option value="session_3">Session 3</option>
          </select>
        </div>
        <div className="messages">
          {messages.map((msg, idx) => (
            <div key={idx} className={`msg ${msg.role}`}>
              <strong>{msg.role === "user" ? "You" : "MemGuard"}:</strong> {msg.content}
            </div>
          ))}
        </div>
        <form onSubmit={onSubmit} className="row">
          <input value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Type message..." />
          <button type="submit">Send</button>
        </form>
      </section>

      <aside className="memory-panel">
        <h3>Memory Inspector</h3>
        {memories.map((m) => (
          <div className="memory-card" key={m.id}>
            <div>
              <span className={`tag ${m.trust_tier}`}>{m.trust_tier}</span>
              <span className="tag">{m.source}</span>
              <span className="tag">{m.status}</span>
            </div>
            <p>{m.fact_text}</p>
            {m.status === "conflicted" && (
              <div className="row">
                <button onClick={() => void resolve(m.id, "accept")}>Accept</button>
                <button onClick={() => void resolve(m.id, "reject")}>Reject</button>
                <button onClick={() => void resolve(m.id, "supersede")}>Supersede</button>
              </div>
            )}
          </div>
        ))}
        <h4>Latest Events</h4>
        {events.map((e, idx) => (
          <div key={idx} className="memory-card">
            <strong>{e.event_type}</strong>
            <pre style={{ whiteSpace: "pre-wrap", margin: 0 }}>{JSON.stringify(e.detail, null, 2)}</pre>
          </div>
        ))}
        <h4>Pending Review Count</h4>
        <p>{conflicted.length}</p>
      </aside>
    </main>
  );
}
