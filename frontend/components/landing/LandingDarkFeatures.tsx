const CARDS = [
  {
    label: "TRUST SCORING",
    title: "Every fact wears a tier",
    body: "HIGH / MEDIUM / LOW based on how the claim entered memory — not vibes.",
  },
  {
    label: "CONFLICT ENGINE",
    title: "Two-stage adjudication",
    body: "Fast similarity first, then Qwen decides agree, conflict, or duplicate.",
  },
  {
    label: "POISON GUARD",
    title: "Stop injected lies",
    body: "Document-sourced sensitive claims are flagged before they reach the prompt.",
  },
];

export default function LandingDarkFeatures() {
  return (
    <section className="lp-dark" id="features">
      <div className="lp-dark__inner">
        <p className="lp-kicker lp-kicker--cream">DIGITAL MEMORY TWIN</p>
        <h2 className="lp-dark__title">Governed recall, not a scrapbook.</h2>
        <p className="lp-dark__lede">
          MemGuard keeps a living map of what the agent believes — with trust, TTL, and an audit log.
        </p>
        <div className="lp-dark__grid">
          {CARDS.map((card) => (
            <article key={card.label} className="lp-dark__card">
              <p className="lp-dark__label">{card.label}</p>
              <h3>{card.title}</h3>
              <p>{card.body}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
