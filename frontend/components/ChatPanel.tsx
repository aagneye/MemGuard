"use client";

import { FormEvent, useState } from "react";

import type { ChatMessage } from "../lib/types";
import EmptyState from "./EmptyState";
import MemoryEventTag from "./MemoryEventTag";
import Spinner from "./Spinner";

type Props = {
  messages: ChatMessage[];
  onSend: (message: string) => Promise<void>;
};

export default function ChatPanel({ messages, onSend }: Props) {
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const text = draft.trim();
    if (!text || sending) return;
    setDraft("");
    setSending(true);
    try {
      await onSend(text);
    } finally {
      setSending(false);
    }
  }

  return (
    <section className="chat-panel">
      <div className="messages">
        {messages.length === 0 && (
          <EmptyState
            icon="🧠"
            title="No messages yet"
            description="Talk to the agent — it will remember facts about you across sessions."
            hint='Try: "I\'m on the Pro plan, my timezone is IST, please reply concisely."'
          />
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={`msg ${msg.role === "user" ? "user" : "bot"}`}>
            <strong>{msg.role === "user" ? "You" : "Acme Cloud Support"}:</strong> {msg.content}
            {msg.events?.map((event, eventIdx) => <MemoryEventTag key={eventIdx} event={event} />)}
          </div>
        ))}
        {sending && (
          <div className="msg bot">
            <Spinner size="sm" label="MemGuard is thinking…" />
          </div>
        )}
      </div>
      <form onSubmit={handleSubmit} className="row">
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="Type a message…"
          disabled={sending}
        />
        <button type="submit" disabled={sending}>
          {sending ? <Spinner size="sm" /> : "Send"}
        </button>
      </form>
    </section>
  );
}
