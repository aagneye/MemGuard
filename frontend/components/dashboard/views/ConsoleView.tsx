import Link from "next/link";

export default function ConsoleView() {
  return (
    <section>
      <h1 className="dash-view-title">Console</h1>
      <p className="dash-view-lede">
        Full chat + memory inspector lives on the dedicated demo route for the smoothest recording path.
      </p>
      <article className="dash-card">
        <h3>Open the live agent console</h3>
        <p className="muted">
          Chat, Memory Inspector, conflict resolve, and governance feed — same cream/maroon chrome via the
          shared navbar when you return here.
        </p>
        <Link href="/demo" className="btn btn-primary">
          Go to /demo
        </Link>
      </article>
    </section>
  );
}
