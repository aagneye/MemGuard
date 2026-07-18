import Link from "next/link";

export default function LandingHero() {
  return (
    <section className="lp-hero" id="top">
      <p className="lp-kicker">TRUST-AWARE MEMORY FOR AGENTS</p>
      <h1 className="lp-hero__title">
        Memory your agents can <span className="lp-accent">trust</span>.
      </h1>
      <p className="lp-hero__lede">
        MemGuard scores every fact for provenance, catches conflicts before they poison context,
        and decays stale claims — powered by Qwen on Alibaba Cloud.
      </p>
      <div className="lp-hero__actions">
        <Link href="/dashboard" className="btn btn-primary">
          Open dashboard
        </Link>
        <Link href="/demo" className="btn btn-secondary">
          See live demo
        </Link>
      </div>
      <p className="lp-hero__badge">Qwen Cloud Global AI Hackathon 2026 · Track 1 MemoryAgent</p>
    </section>
  );
}
