"use client";

import { useCallback, useEffect, useState } from "react";

import ActivityFeed from "../../components/ActivityFeed";
import ChatPanel from "../../components/ChatPanel";
import ErrorToast from "../../components/ErrorToast";
import MemoryInspector from "../../components/MemoryInspector";
import MemorySearchPanel from "../../components/MemorySearchPanel";
import TopBar from "../../components/TopBar";
import { fetchDemoUsers, fetchEvents, fetchMemories, resolveMemory, sendChatMessage, startNewSession } from "../../lib/api";
import { FALLBACK_DEMO_USERS } from "../../lib/demoUsers";
import type { ChatMessage, DemoUser, MemoryEvent, MemoryItem, ResolveAction } from "../../lib/types";

export default function DemoPage() {
  const [demoUsers, setDemoUsers] = useState<DemoUser[]>(FALLBACK_DEMO_USERS);
  const [activeUserId, setActiveUserId] = useState(FALLBACK_DEMO_USERS[0].id);
  const [sessionId, setSessionId] = useState("session_1");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [events, setEvents] = useState<MemoryEvent[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void fetchDemoUsers()
      .then((users) => {
        if (users.length > 0) {
          setDemoUsers(users);
          setActiveUserId(users[0].id);
        }
      })
      .catch(() => {
        // Backend may not be running — fallback users already set
      });
  }, []);

  const refreshMemories = useCallback(async (userId: string) => {
    try {
      const [mems, evts] = await Promise.all([fetchMemories(userId), fetchEvents(userId)]);
      setMemories(mems);
      setEvents(evts);
    } catch {
      // Memory panel shows stale data; non-fatal
    }
  }, []);

  useEffect(() => {
    void refreshMemories(activeUserId);
    setMessages([]);
  }, [activeUserId, refreshMemories]);

  async function handleSend(text: string) {
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    try {
      const payload = await sendChatMessage(activeUserId, sessionId, text);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: payload.reply, events: payload.memory_events },
      ]);
      await refreshMemories(activeUserId);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Backend unreachable — is the server running?";
      setError(msg);
      setMessages((prev) => prev.slice(0, -1));
    }
  }

  async function handleNewSession() {
    try {
      const nextSessionId = await startNewSession(activeUserId);
      setSessionId(nextSessionId);
      setMessages([]);
    } catch {
      setError("Could not create a new session.");
    }
  }

  async function handleResolve(memoryId: string, action: ResolveAction) {
    try {
      await resolveMemory(memoryId, action);
      await refreshMemories(activeUserId);
    } catch {
      setError("Failed to resolve memory conflict.");
    }
  }

  return (
    <main className="demo-shell">
      <TopBar
        demoUsers={demoUsers}
        activeUserId={activeUserId}
        sessionId={sessionId}
        onSwitchUser={setActiveUserId}
        onNewSession={handleNewSession}
        onResetDemo={() => { setMessages([]); void refreshMemories(activeUserId); }}
      />
      <div className="demo-body">
        <ChatPanel messages={messages} onSend={handleSend} />
        <div className="inspector-pane">
          <MemoryInspector memories={memories} onResolve={handleResolve} />
          <MemorySearchPanel userId={activeUserId} />
          <ActivityFeed events={events} />
        </div>
      </div>
      <ErrorToast message={error} onDismiss={() => setError(null)} />
    </main>
  );
}
