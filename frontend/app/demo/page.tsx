"use client";

import { useEffect, useState } from "react";

import ChatPanel from "../../components/ChatPanel";
import MemoryInspector from "../../components/MemoryInspector";
import TopBar from "../../components/TopBar";
import { fetchDemoUsers, fetchMemories, resolveMemory, sendChatMessage, startNewSession } from "../../lib/api";
import { FALLBACK_DEMO_USERS } from "../../lib/demoUsers";
import type { ChatMessage, DemoUser, MemoryItem, ResolveAction } from "../../lib/types";

export default function DemoPage() {
  const [demoUsers, setDemoUsers] = useState<DemoUser[]>(FALLBACK_DEMO_USERS);
  const [activeUserId, setActiveUserId] = useState(FALLBACK_DEMO_USERS[0].id);
  const [sessionId, setSessionId] = useState("session_1");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [memories, setMemories] = useState<MemoryItem[]>([]);

  useEffect(() => {
    void fetchDemoUsers().then((users) => {
      if (users.length > 0) {
        setDemoUsers(users);
        setActiveUserId(users[0].id);
      }
    });
  }, []);

  useEffect(() => {
    void refreshMemories(activeUserId);
    setMessages([]);
  }, [activeUserId]);

  async function refreshMemories(userId: string) {
    setMemories(await fetchMemories(userId));
  }

  async function handleSend(text: string) {
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    const payload = await sendChatMessage(activeUserId, sessionId, text);
    setMessages((prev) => [...prev, { role: "assistant", content: payload.reply, events: payload.memory_events }]);
    await refreshMemories(activeUserId);
  }

  async function handleNewSession() {
    const nextSessionId = await startNewSession(activeUserId);
    setSessionId(nextSessionId);
    setMessages([]);
  }

  async function handleResolve(memoryId: string, action: ResolveAction) {
    await resolveMemory(memoryId, action);
    await refreshMemories(activeUserId);
  }

  return (
    <main className="demo-shell">
      <TopBar
        demoUsers={demoUsers}
        activeUserId={activeUserId}
        onSwitchUser={setActiveUserId}
        onNewSession={handleNewSession}
      />
      <div className="demo-body">
        <ChatPanel messages={messages} onSend={handleSend} />
        <MemoryInspector memories={memories} onResolve={handleResolve} />
      </div>
    </main>
  );
}
