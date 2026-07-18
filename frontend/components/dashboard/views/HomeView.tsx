import Link from "next/link";

const TILES = [
  { label: "Active memories", value: "Live", note: "Inspect in Memory Mapping" },
  { label: "Governance", value: "On", note: "Conflict + decay enabled" },
  { label: "LLM provider", value: "Qwen / Ollama", note: "Set in .env" },
];

export default function HomeView() {
  return (
    <section>
      <h1 className="dash-view-title">Home</h1>
      <p className="dash-view-lede">
        MemGuard workspace overview — jump into mapping, governance, or the live console.
      </p>
      <div className="dash-grid dash-grid--3">
        {TILES.map((t) => (
          <article key={t.label} className="dash-card">
            <p className="muted" style={{ margin: 0 }}>
              {t.label}
            </p>
            <p className="dash-stat">{t.value}</p>
            <p className="muted" style={{ marginBottom: 0 }}>
              {t.note}
            </p>
          </article>
        ))}
      </div>
      <div className="dash-card" style={{ marginTop: 16 }}>
        <h3>Quick actions</h3>
        <div className="lp-hero__actions" style={{ justifyContent: "flex-start" }}>
          <Link href="/demo" className="btn btn-primary">
            Launch live console
          </Link>
          <a href="https://github.com/aagneye/MemGuard/blob/master/docs/ARCHITECTURE.md" className="btn btn-secondary">
            Architecture
          </a>
        </div>
      </div>
    </section>
  );
}
