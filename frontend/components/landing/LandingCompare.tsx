export default function LandingCompare() {
  return (
    <section className="lp-compare" id="compare">
      <h2 className="lp-section-title">
        Power your agents to <span className="lp-accent">decide</span> with governed memory.
      </h2>
      <div className="lp-compare__grid">
        <article className="lp-compare-card">
          <span className="lp-compare-card__badge lp-compare-card__badge--muted">WITHOUT MEMGUARD</span>
          <pre className="lp-compare-card__code">{`GPT → "User is on Free plan."
No source. No timestamp. No trust.`}</pre>
          <p className="lp-compare-card__foot">No provenance. Estimated range. Easy to poison.</p>
        </article>
        <article className="lp-compare-card lp-compare-card--live">
          <div className="lp-compare-card__top">
            <span className="lp-compare-card__badge lp-compare-card__badge--accent">WITH MEMGUARD</span>
            <span className="lp-live">
              <span className="lp-live__dot" /> LIVE
            </span>
          </div>
          <pre className="lp-compare-card__code">{`memguard.recall("plan")
→ { fact: "Pro plan", trust: "HIGH",
    source: "user", seen: "2026-07-18" }`}</pre>
          <p className="lp-compare-card__foot lp-compare-card__foot--ok">
            Provenance, trust tier, TTL, conflict check.
          </p>
        </article>
      </div>
    </section>
  );
}
