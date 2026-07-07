import type { DemoUser } from "./types";

/**
 * Fallback preset users, used only if the backend /demo/users call fails
 * (e.g. offline local dev without the backend running yet). Keeps the
 * dropdown usable so Screen A never renders empty.
 */
export const FALLBACK_DEMO_USERS: DemoUser[] = [
  { id: "demo_alice", label: "Alice (Pro plan, IST)" },
  { id: "demo_bob", label: "Bob (fresh, no memories yet)" },
  { id: "demo_carol", label: "Carol (poisoning scenario seed)" },
];
