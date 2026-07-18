const STEPS = [
  {
    id: "01",
    tag: "Ingest",
    title: "Capture what was said",
    body: "Each turn extracts durable facts with Qwen, not just chat transcript dumps.",
  },
  {
    id: "02",
    tag: "Score",
    title: "Assign trust + provenance",
    body: "User-stated facts score HIGH; tool and document claims sit lower until verified.",
  },
  {
    id: "03",
    tag: "Govern",
    title: "Detect conflicts + poison",
    body: "Competing claims are flagged; sensitive document injections are blocked from context.",
  },
  {
    id: "04",
    tag: "Decay",
    title: "Forget what went stale",
    body: "TTL and decay jobs drop expired memories so agents stop acting on old truths.",
  },
];

export default function LandingLoop() {
  return (
    <section className="lp-loop" id="loop">
      <p className="lp-kicker">THE CLOSED LOOP</p>
      <h2 className="lp-section-title">From utterance to governed memory.</h2>
      <p className="lp-section-lede">
        One pipeline per turn: chat, extract, adjudicate, store — with a human-readable governance trail.
      </p>
      <div className="lp-loop__rail">
        {STEPS.map((step) => (
          <article key={step.id} className="lp-loop__cell">
            <p className="lp-loop__meta">
              {step.id} / {step.tag}
            </p>
            <h3>{step.title}</h3>
            <p>{step.body}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
