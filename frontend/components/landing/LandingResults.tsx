const STATS = [
  { value: "3", label: "Qwen calls per chat turn" },
  { value: "4", label: "Governance controls in-loop" },
  { value: "0", label: "Login required for /demo" },
];

export default function LandingResults() {
  return (
    <section className="lp-results" id="results">
      <p className="lp-kicker">RESULTS</p>
      <h2 className="lp-section-title">Built to show judges the algorithm.</h2>
      <div className="lp-results__grid">
        {STATS.map((s) => (
          <article key={s.label} className="lp-results__cell">
            <p className="lp-results__value">{s.value}</p>
            <p className="lp-results__label">{s.label}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
