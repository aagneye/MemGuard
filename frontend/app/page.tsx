import Link from "next/link";

export default function LandingPage() {
  return (
    <main className="landing">
      <div className="landing-card">
        <h1>MemGuard</h1>
        <p>
          A trust-aware memory agent for "Acme Cloud Support." It remembers you across sessions — and refuses to be
          fooled by conflicting or poisoned facts.
        </p>
        <ul>
          <li>Persistent, cross-session memory recall</li>
          <li>Every fact scored for trust and provenance before it's acted on</li>
          <li>Conflicting and poisoned claims are flagged, never silently applied</li>
        </ul>
        <Link href="/demo" className="launch-button">
          Launch Demo
        </Link>
        <p className="muted">No login required. Pick a demo user once you're inside.</p>
      </div>
    </main>
  );
}
