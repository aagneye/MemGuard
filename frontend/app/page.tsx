import Link from "next/link";

const FEATURES = [
  { icon: "🏷️", title: "Trust Scoring", desc: "Every memory gets a tier: HIGH (user said it), MEDIUM (tool inferred), LOW (document extracted)." },
  { icon: "⚔️", title: "Conflict Detection", desc: "Two-stage pipeline — keyword + vector similarity, then Qwen adjudicates agree/conflict/duplicate." },
  { icon: "🛡️", title: "Poisoning Prevention", desc: "Document-extracted sensitive claims are flagged before they reach the agent's context." },
  { icon: "⏱️", title: "Decay + TTL", desc: "Every fact has a time-to-live. Stale memories expire automatically — or on demand." },
  { icon: "🔗", title: "MCP Integration", desc: "search_memory and write_memory exposed as MCP tools for Qwen Cloud agent orchestration." },
  { icon: "📊", title: "Governance Log", desc: "Every stored, conflicted, flagged, and resolved event is logged and visible to the human." },
];

export default function LandingPage() {
  return (
    <main className="landing">
      <div className="landing-card">
        <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "8px" }}>
          <span style={{ fontSize: "48px" }}>🧠</span>
          <div>
            <h1 style={{ margin: 0, fontSize: "32px", color: "#f1f5f9" }}>MemGuard</h1>
            <p style={{ margin: 0, color: "#6366f1", fontWeight: 600, fontSize: "14px" }}>
              Trust-Aware Memory Agent · Qwen Cloud Hackathon 2026
            </p>
          </div>
        </div>

        <p style={{ color: "#cbd5e1", fontSize: "16px", lineHeight: 1.6, margin: "16px 0" }}>
          AI agents that remember things across sessions face a real threat: <strong style={{ color: "#f87171" }}>memory poisoning</strong>.
          MemGuard scores every memory for trust and provenance, catches conflicting claims before acting on them,
          and forgets what&apos;s gone stale — powered by three Qwen LLM calls per turn.
        </p>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "12px",
            margin: "24px 0",
          }}
        >
          {FEATURES.map((f) => (
            <div
              key={f.title}
              style={{
                background: "#0f172a",
                border: "1px solid #1e293b",
                borderRadius: "10px",
                padding: "14px",
              }}
            >
              <div style={{ fontSize: "24px", marginBottom: "6px" }}>{f.icon}</div>
              <strong style={{ color: "#e2e8f0", fontSize: "13px" }}>{f.title}</strong>
              <p style={{ color: "#64748b", fontSize: "12px", margin: "4px 0 0", lineHeight: 1.5 }}>{f.desc}</p>
            </div>
          ))}
        </div>

        <div style={{ display: "flex", gap: "12px", flexWrap: "wrap", justifyContent: "center", marginTop: "24px" }}>
          <Link href="/demo" className="launch-button">
            Launch Demo →
          </Link>
          <a
            href="https://github.com/aagneye/MemGuard"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              background: "#1e293b",
              color: "#e2e8f0",
              padding: "12px 24px",
              borderRadius: "8px",
              textDecoration: "none",
              fontWeight: 600,
              fontSize: "15px",
              border: "1px solid #334155",
            }}
          >
            GitHub
          </a>
        </div>

        <p className="muted" style={{ marginTop: "16px" }}>
          No login required · Built with Qwen (qwen-plus + text-embedding-v3) · MIT License
        </p>
      </div>
    </main>
  );
}
