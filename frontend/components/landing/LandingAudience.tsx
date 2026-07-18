const POINTS = [
  {
    n: "1",
    title: "Support agents",
    body: "Remember plan, timezone, and prefs without hallucinating upgrades.",
  },
  {
    n: "2",
    title: "Ops copilots",
    body: "Keep entity facts with provenance when tools disagree with humans.",
  },
  {
    n: "3",
    title: "Hackathon demos",
    body: "Show judges conflict + decay live — MemoryAgent track ready.",
  },
  {
    n: "4",
    title: "Safety-minded teams",
    body: "Inspect, supersede, and expire memories with a visible governance trail.",
  },
];

export default function LandingAudience() {
  return (
    <section className="lp-audience" id="audience">
      <p className="lp-kicker">WHO IT&apos;S FOR</p>
      <div className="lp-audience__grid">
        <div>
          <h2 className="lp-section-title">Built for people who run agent memory.</h2>
          <ol className="lp-audience__list">
            {POINTS.map((p) => (
              <li key={p.n}>
                <span className="lp-audience__n">{p.n}</span>
                <div>
                  <strong>{p.title}</strong>
                  <p>{p.body}</p>
                </div>
              </li>
            ))}
          </ol>
        </div>
        <aside className="lp-audience__panel">
          <span className="lp-pill">AUTO-GOVERNED</span>
          <p className="lp-audience__panel-kicker">MEMGUARD · DEMO</p>
          <p className="lp-mono">mem_42 · trust HIGH</p>
          <p className="lp-audience__panel-title">User timezone is IST · Pro plan</p>
          <ul className="lp-check">
            <li>Source: user utterance</li>
            <li>Conflict scan: clear</li>
            <li>TTL: 30 days</li>
          </ul>
          <div className="lp-audience__panel-foot">
            <span>Verifying against prior facts…</span>
            <span className="lp-accent-mono">trust 0.94</span>
          </div>
        </aside>
      </div>
    </section>
  );
}
