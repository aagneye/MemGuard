const ROWS = [
  { pid: "extract", cpu: "12%", state: "idle" },
  { pid: "adjudicate", cpu: "4%", state: "idle" },
  { pid: "decay", cpu: "1%", state: "scheduled" },
  { pid: "embed", cpu: "8%", state: "warm" },
];

export default function ActivityView() {
  return (
    <section>
      <h1 className="dash-view-title">Activity</h1>
      <p className="dash-view-lede">Lightweight process monitor for memory pipeline stages.</p>
      <article className="dash-card">
        <table className="dash-table">
          <thead>
            <tr>
              <th>Stage</th>
              <th>Load</th>
              <th>State</th>
            </tr>
          </thead>
          <tbody>
            {ROWS.map((r) => (
              <tr key={r.pid}>
                <td className="dash-mono">{r.pid}</td>
                <td>{r.cpu}</td>
                <td>{r.state}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </article>
    </section>
  );
}
