const BARS = [
  { label: "HIGH", pct: 62 },
  { label: "MEDIUM", pct: 28 },
  { label: "LOW", pct: 10 },
];

export default function TrustAnalyticsView() {
  return (
    <section>
      <h1 className="dash-view-title">Trust Analytics</h1>
      <p className="dash-view-lede">Distribution of trust tiers across the active memory set.</p>
      <article className="dash-card">
        <div className="trust-bars">
          {BARS.map((b) => (
            <div key={b.label} className="trust-bars__row">
              <span className="dash-mono">{b.label}</span>
              <div className="trust-bars__track">
                <div className="trust-bars__fill" style={{ width: `${b.pct}%` }} />
              </div>
              <span className="dash-mono">{b.pct}%</span>
            </div>
          ))}
        </div>
      </article>
    </section>
  );
}
