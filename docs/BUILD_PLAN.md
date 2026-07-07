# MemGuard — Build Plan

Deadline: **Jul 10, 2026 @ 2:30 AM GMT+5:30**. Plan authored: Jul 7, 2026. That's roughly **2.5 focused days**, so the plan below is scoped to protect the 5 demo beats first and treat everything else (MCP, RDS, Nginx/TLS polish) as explicit stretch goals that can be cut without damaging the core score.

Priority order if time runs out, cut from the bottom: MCP stretch → RDS stretch → Nginx/TLS polish → decay scheduler (check-on-read alone is fine) → activity feed styling polish. **Never cut**: the 5 demo beats, the Alibaba Cloud deployment, the README + architecture diagram.

---

## Day 1 (Jul 7) — Skeleton + deploy + happy path

**Morning**
- [ ] Scaffold repo per `docs/PROJECT_STRUCTURE.md`: backend (FastAPI), frontend (Next.js), `infra/docker-compose.yml`.
- [ ] Postgres+pgvector and Redis running locally via docker-compose; `memories` + `memory_events` tables migrated.
- [ ] `LLMProvider` interface + `OllamaProvider` implementation; verify a bare chat round-trip locally with `qwen2.5:7b`.
- [ ] `QwenProvider` implementation against DashScope; verify with the curl smoke test from `SETUP.md`, then via the app with `LLM_PROVIDER=qwen`.

**Afternoon — deploy immediately, don't wait for features**
- [ ] Provision Alibaba Cloud ECS, install Docker, ship the current skeleton (even just `/health` + a bare `/chat`).
- [ ] Confirm publicly reachable, **record the Alibaba Cloud deployment proof video now** while it's simple to show cleanly.
- [ ] `POST /chat` end-to-end: retrieve (empty at first) → prompt → Qwen reply → naive fact extraction → write to `memories` with a hardcoded trust tier. This is the ugly-but-working spine everything else attaches to.

**Evening**
- [ ] Trust scorer (`governance/trust_scorer.py`): source → tier/ttl table, confidence downgrade rule.
- [ ] `GET /memories` endpoint returning tiered results.
- [ ] Wire session memory (Redis) into the chat prompt so multi-turn context within a session works.

## Day 2 (Jul 8) — Governance depth + UI

**Morning**
- [ ] Conflict detector stage 1 (pgvector cosine similarity query) + stage 2 (LLM adjudication call) + decision table (agree/conflict/duplicate/unrelated).
- [ ] Poisoning special case: sensitive-keyword allowlist forcing `document_extracted` facts touching billing/admin/refund/password into `conflicted` + `flagged_poisoning` immediately.
- [ ] `POST /memories/{id}/resolve` (accept/reject/supersede), with `memory_events` rows written on every transition.

**Afternoon**
- [ ] Decay: check-on-read expiry query wired into both `GET /memories` and the `/chat` retrieval step; `DEMO_TIME_SCALE` env wired through.
- [ ] Frontend: chat panel + session switcher (dropdown to fake "Session 2" against the same `user_id`).
- [ ] Frontend: Memory Inspector — Active list, Pending Review list, Activity Feed, trust-tier badges.

**Evening**
- [ ] Run `scripts/replay_demo_beats.py` against the deployed (Qwen-backed) instance — fix every rough edge found here, this script IS your rehearsal.
- [ ] `scripts/seed_demo_user.py` to get a clean, repeatable starting state for recording.
- [ ] If ahead of schedule: MCP stretch (`search_memory`/`write_memory` tools) or RDS swap. If behind: skip straight to Day 3.

## Day 3 (Jul 9, into early Jul 10) — Record, document, submit

**Morning/Afternoon**
- [ ] Reset demo user state on the deployed instance; do 2-3 full dry runs of the 5 beats before recording.
- [ ] Record the **3-minute demo video** covering all 5 beats in order (Section 3 of `ARCHITECTURE.md`), Memory Inspector visible throughout. Upload to YouTube/Vimeo, set public.
- [ ] Finalize `README.md`: pitch, embedded architecture diagram, setup quickstart (link to `docs/SETUP.md`), feature/functionality description, track declaration ("Track 1 — MemoryAgent"), links to both videos.
- [ ] Export the mermaid diagram from `docs/ARCHITECTURE.md` to `docs/architecture-diagram.png` and embed it in the README.
- [ ] Verify GitHub repo is public, license file present and visible in the "About" section.

**Final pass (before Jul 10, 2:30 AM GMT+5:30)**
- [ ] Go through `docs/SUBMISSION_CHECKLIST.md` line by line.
- [ ] Submit on Devpost with track = Track 1: MemoryAgent.
- [ ] (Optional, only if time remains) Publish a short blog/social post about the build for the Blog Post Prize.
