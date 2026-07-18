const EVENTS = [
  { t: "store", d: "Saved fact · plan=Pro · trust HIGH" },
  { t: "conflict", d: "plan=Free vs plan=Pro flagged" },
  { t: "adjudicate", d: "Qwen marked conflict · awaiting resolve" },
  { t: "decay", d: "Expired stale preference (TTL)" },
];

export default function GovernanceView() {
  return (
    <section>
      <h1 className="dash-view-title">Governance</h1>
      <p className="dash-view-lede">Audit trail of store, conflict, poison, and decay decisions.</p>
      <div className="dash-grid">
        {EVENTS.map((e) => (
          <article key={e.d} className="dash-card">
            <p className="dash-mono" style={{ color: "var(--maroon)", margin: 0 }}>
              {e.t.toUpperCase()}
            </p>
            <p style={{ margin: "8px 0 0" }}>{e.d}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
