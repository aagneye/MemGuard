# MemGuard — Frontend & Customer-Facing Spec (Addendum)

Companion to `docs/ARCHITECTURE.md`. This is the source of truth for the public-facing demo site — no login system, no payment, no API keys required from a visitor.

## Screens

**Screen A — Chat (`/demo`, left panel)**
- Top bar: agent name ("Acme Cloud Support"), "New Session" button (new `session_id`, same `user_id` — proves cross-session recall), "Switch Demo User" dropdown (preset fake users, clean reset for judges).
- Each agent reply that touched memory shows an inline tag: `📌 remembered: "..."` or `⚠️ flagged: ...`.

**Screen B — Memory Inspector (`/demo`, right panel, always visible)**
- Live list of the current user's stored memories: fact text, trust tier badge (HIGH/MEDIUM/LOW, color-coded), source, status.
- Conflicted rows render as a paired card with **Accept new** / **Keep old** buttons, wired to `POST /memories/{id}/resolve`.

**Screen C — Landing (`/`)**
- Static "What is MemGuard" + "Launch Demo" button. No auth. Clean opening shot for the demo video.

## Frontend ↔ Backend contract

| Method | Path | Body | Returns |
|---|---|---|---|
| POST | `/chat` | `{ user_id, session_id, message }` | `{ reply, memory_events: [{ type: "stored"\|"flagged"\|"conflict", fact, trust_tier }] }` |
| GET | `/memories?user_id=` | — | `[{ id, fact_text, trust_tier, source, status, conflicts_with, created_at }]` |
| POST | `/memories/{id}/resolve` | `{ action: "accept"\|"reject"\|"supersede" }` | `{ id, status }` |
| POST | `/session/new` | `{ user_id }` | `{ session_id }` |
| GET | `/demo/users` | — | `[{ id, label }]` (preset demo users for the switch-user dropdown) |

No auth needed for the hackathon build. `user_id` is picked from the demo dropdown and passed in plainly.

## Where the Qwen Cloud key lives

Backend `.env` only — never sent to the browser, never in frontend code, never committed:

```env
QWEN_API_KEY=sk-xxxxx
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
```

## Hosting

- Backend must be on Alibaba Cloud (submission requirement).
- Frontend can be static-built and served from the same ECS instance, or from a free static host (Vercel/Netlify) — either is fine.

## Implementation notes (this repo)

- Conflicted memory pairs are cross-linked server-side (`conflicts_with`) so resolving one side of a conflict automatically resolves its counterpart in the opposite direction — this is what makes "Accept new / Keep old" a single clean decision instead of two independent row-level actions.
- `/auth/*`, `/teams/*`, and `/dashboard` exist as an optional bonus workspace layer (team creation/invites) built ahead of this addendum spec. They are **not** part of the judged public demo flow and are not linked from the landing page — the judged flow is `/` → `/demo`, no login.
