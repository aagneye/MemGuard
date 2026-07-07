import { FALLBACK_DEMO_USERS } from "./demoUsers";
import type { ChatResponse, DemoUser, MemoryItem, ResolveAction } from "./types";

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({}));
    throw new Error(errorBody.detail ?? `Request to ${path} failed with ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export async function fetchDemoUsers(): Promise<DemoUser[]> {
  try {
    const res = await fetch(`${API_BASE}/demo/users`);
    if (!res.ok) return FALLBACK_DEMO_USERS;
    return (await res.json()) as DemoUser[];
  } catch {
    return FALLBACK_DEMO_USERS;
  }
}

export async function sendChatMessage(userId: string, sessionId: string, message: string): Promise<ChatResponse> {
  return postJson<ChatResponse>("/chat", { user_id: userId, session_id: sessionId, message });
}

export async function startNewSession(userId: string): Promise<string> {
  const res = await postJson<{ session_id: string }>("/session/new", { user_id: userId });
  return res.session_id;
}

export async function fetchMemories(userId: string): Promise<MemoryItem[]> {
  const res = await fetch(`${API_BASE}/memories?user_id=${encodeURIComponent(userId)}`);
  if (!res.ok) return [];
  return (await res.json()) as MemoryItem[];
}

export async function resolveMemory(
  memoryId: string,
  action: ResolveAction,
  supersedeFactText?: string
): Promise<{ ok: boolean; memory_id: string; status: string }> {
  return postJson(`/memories/${memoryId}/resolve`, {
    action,
    supersede_fact_text: supersedeFactText,
  });
}
