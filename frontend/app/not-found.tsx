import Link from "next/link";

export default function NotFound() {
  return (
    <main className="lp-hero">
      <p className="lp-kicker">404</p>
      <h1 className="lp-hero__title">Page not found</h1>
      <p className="lp-hero__lede">That route is not part of MemGuard.</p>
      <Link href="/" className="btn btn-primary">
        Back home
      </Link>
    </main>
  );
}
