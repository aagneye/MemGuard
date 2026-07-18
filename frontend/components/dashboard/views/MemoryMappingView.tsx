const NODES = [
  { id: "N1", label: "plan=Pro", tier: "HIGH", x: 18, y: 30 },
  { id: "N2", label: "tz=IST", tier: "HIGH", x: 55, y: 22 },
  { id: "N3", label: "plan=Free?", tier: "LOW", x: 72, y: 58 },
  { id: "N4", label: "email=…", tier: "MED", x: 32, y: 68 },
];

export default function MemoryMappingView() {
  return (
    <section>
      <h1 className="dash-view-title">Memory Mapping</h1>
      <p className="dash-view-lede">
        A spatial view of governed facts — trust tiers, edges for conflicts, maroon highlights for risk.
      </p>
      <article className="dash-card">
        <div className="mem-map">
          <svg viewBox="0 0 100 100" className="mem-map__svg" role="img" aria-label="Memory map">
            <line x1="22" y1="34" x2="70" y2="56" className="mem-map__edge mem-map__edge--conflict" />
            <line x1="22" y1="34" x2="55" y2="26" className="mem-map__edge" />
            <line x1="55" y1="26" x2="36" y2="68" className="mem-map__edge" />
            {NODES.map((n) => (
              <g key={n.id} transform={`translate(${n.x} ${n.y})`}>
                <circle r="6" className={`mem-map__node mem-map__node--${n.tier.toLowerCase()}`} />
                <text y="12" textAnchor="middle" className="mem-map__label">
                  {n.label}
                </text>
              </g>
            ))}
          </svg>
          <ul className="mem-map__legend">
            <li>
              <span className="mem-map__swatch mem-map__swatch--high" /> High trust
            </li>
            <li>
              <span className="mem-map__swatch mem-map__swatch--med" /> Medium
            </li>
            <li>
              <span className="mem-map__swatch mem-map__swatch--low" /> Low / contested
            </li>
          </ul>
        </div>
      </article>
    </section>
  );
}
