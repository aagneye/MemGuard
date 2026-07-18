const ALERTS = [
  { level: "High", text: "Document claim attempted to override user plan" },
  { level: "Med", text: "Low-trust email fact awaiting confirmation" },
  { level: "Info", text: "Decay job scheduled for 3 preferences" },
];

export default function AlertsView() {
  return (
    <section>
      <h1 className="dash-view-title">Security Alerts</h1>
      <p className="dash-view-lede">Poisoning flags and sensitive claim reviews.</p>
      <div className="dash-grid">
        {ALERTS.map((a) => (
          <article key={a.text} className="dash-card">
            <p className="dash-mono" style={{ color: "var(--maroon)", margin: 0 }}>
              {a.level}
            </p>
            <p style={{ marginBottom: 0 }}>{a.text}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
