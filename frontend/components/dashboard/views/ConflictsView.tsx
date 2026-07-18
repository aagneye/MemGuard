export default function ConflictsView() {
  return (
    <section>
      <h1 className="dash-view-title">Conflicts</h1>
      <p className="dash-view-lede">Resolve competing memories before the agent acts on them.</p>
      <article className="dash-card">
        <div className="conflict-pair">
          <div>
            <p className="muted">Older claim</p>
            <p className="dash-mono">plan = Free</p>
          </div>
          <div className="conflict-pair__vs">vs</div>
          <div>
            <p className="muted">Newer claim</p>
            <p className="dash-mono">plan = Pro</p>
          </div>
        </div>
        <div className="lp-hero__actions" style={{ justifyContent: "flex-start", marginTop: 16 }}>
          <button type="button" className="btn btn-primary">
            Accept newer
          </button>
          <button type="button" className="btn btn-secondary">
            Keep older
          </button>
          <button type="button" className="btn btn-secondary">
            Supersede both
          </button>
        </div>
        <p className="muted" style={{ marginTop: 14, marginBottom: 0 }}>
          Live resolve controls are available in the demo console Memory Inspector.
        </p>
      </article>
    </section>
  );
}
