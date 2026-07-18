export default function LandingProof() {
  return (
    <section className="lp-proof" id="proof">
      <div className="lp-proof__inner">
        <div>
          <p className="lp-kicker lp-kicker--cream">VISIBILITY &amp; GOVERNANCE</p>
          <h2 className="lp-proof__title">Proof your reviewers can read.</h2>
          <p>
            Every store, conflict, poison flag, and decay event is logged. The dashboard maps memories
            visually so judges see the algorithm — not just a chat box.
          </p>
          <p>
            Backend on Alibaba Cloud ECS, reasoning via DashScope-compatible Qwen, optional Postgres /
            Tair for retrieval — see Production docs for deployment proof.
          </p>
        </div>
        <aside className="lp-proof__card">
          <div className="lp-proof__card-head">
            <span>TRUST VS BASELINE</span>
            <span className="lp-accent-mono">+38%</span>
          </div>
          <h3>Conflicts caught before act.</h3>
          <svg className="lp-proof__chart" viewBox="0 0 320 140" role="img" aria-label="Trust trend chart">
            <path
              d="M10 110 C60 105, 90 90, 130 70 S200 40, 310 28"
              fill="none"
              stroke="rgba(247,246,240,0.25)"
              strokeWidth="2"
              strokeDasharray="6 6"
            />
            <path
              d="M10 120 C70 118, 100 100, 140 78 S220 45, 310 35"
              fill="url(#mgFill)"
              stroke="var(--maroon)"
              strokeWidth="2.5"
            />
            <defs>
              <linearGradient id="mgFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="rgba(122,36,48,0.45)" />
                <stop offset="100%" stopColor="rgba(122,36,48,0)" />
              </linearGradient>
            </defs>
          </svg>
          <div className="lp-proof__legend">
            <span>Predicted ungoverned</span>
            <span>Actual with MemGuard</span>
          </div>
        </aside>
      </div>
    </section>
  );
}
