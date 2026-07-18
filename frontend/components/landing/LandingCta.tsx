import Link from "next/link";

export default function LandingCta() {
  return (
    <section className="lp-cta" id="cta">
      <h2 className="lp-section-title">Ship the demo. Prove the governance.</h2>
      <p className="lp-section-lede">
        Open the dashboard for memory mapping, or jump straight into the live console.
      </p>
      <div className="lp-hero__actions">
        <Link href="/dashboard" className="btn btn-primary">
          Enter dashboard
        </Link>
        <a
          className="btn btn-secondary"
          href="https://github.com/aagneye/MemGuard"
          target="_blank"
          rel="noopener noreferrer"
        >
          View source
        </a>
      </div>
    </section>
  );
}
