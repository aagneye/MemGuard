"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

type EventItem = { event_type: string; detail: Record<string, unknown> };
type MemoryItem = {
  id: string;
  fact_text: string;
  trust_tier: "high" | "medium" | "low";
  source: string;
  status: "active" | "conflicted" | "expired" | "superseded";
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

export default function Home() {
  const [userId, setUserId] = useState("demo_user");
  const [sessionId, setSessionId] = useState("session_1");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Array<{ role: "user" | "bot"; content: string }>>([]);
  const [events, setEvents] = useState<EventItem[]>([]);
  const [memories, setMemories] = useState<MemoryItem[]>([]);

  const conflicted = useMemo(() => memories.filter((m) => m.status === "conflicted"), [memories]);

  async function loadMemories() {
    const res = await fetch(`${API_BASE}/memories?user_id=${encodeURIComponent(userId)}`);
    if (res.ok) {
      setMemories(await res.json());
    }
  }

  useEffect(() => {
    void loadMemories();
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

  return (
    <main className="container">
      <section className="chat-panel">
        <h2>MemGuard Chat</h2>
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
        <p>Active + conflicted memories with trust/source labels.</p>
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

        <h4>Latest Memory Events</h4>
        {events.length === 0 && <p>No events yet.</p>}
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
