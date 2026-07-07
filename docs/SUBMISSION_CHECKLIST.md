# MemGuard — Submission Checklist

Maps Devpost's stated requirements directly to what will exist in this repo. Walk this top-to-bottom right before submitting.

- [ ] **Public GitHub repo** with an OSS license (MIT recommended) visible in the "About" section — set repo visibility and add `LICENSE` on day 1, don't leave it private during the build.
- [ ] **Working code + setup instructions** — `README.md` links to `docs/SETUP.md`; a fresh clone + `.env` fill-in + the commands in `SETUP.md` §4 must actually work.
- [ ] **Alibaba Cloud deployment proof** — short recording, separate from the demo video, showing the backend running on the ECS instance (public IP reachable + `docker ps`/`curl` on the box). Linked in the submission to `infra/alibaba-cloud/ecs-setup.md` (or `docker-compose.prod.yml` / RDS setup, secrets redacted).
- [ ] **Architecture diagram** — `docs/architecture-diagram.png`, exported from the mermaid source in `docs/ARCHITECTURE.md`, embedded in the README.
- [ ] **~3 minute demo video**, public on YouTube/Vimeo/Facebook, covering all 5 beats from `ARCHITECTURE.md` §3: high-trust capture → cross-session recall → poisoning refusal → conflict detection & resolve → decay.
- [ ] **Text description** of features/functionality — pulled from the pitch + demo scenario sections of `ARCHITECTURE.md`, adapted for the Devpost submission form.
- [ ] **Track declared**: Track 1 — MemoryAgent.
- [ ] **(Optional) Blog/social post** about the build journey, for the Blog Post Prize eligibility.

## Judging-criteria self-check (do this before recording, not after)

- [ ] **Technical Depth (30%)** — can I point to, on screen: the dual LLM provider switch, the two-stage conflict detector, and (if built) the MCP tool server?
- [ ] **Innovation (30%)** — does the Memory Inspector visibly show trust tiers, provenance, and the supersede-not-overwrite lifecycle, not just a plain chat log?
- [ ] **Problem Value (25%)** — does the video explicitly say the words "memory poisoning" and tie it back to a real, named, current threat (OWASP Top 10 for Agentic Applications), not just "we prevent bad data"?
- [ ] **Presentation (15%)** — is the Activity Feed / governance logic actually visible and narrated during the demo, or is it hidden behind a static chat UI?
