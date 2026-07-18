import Link from "next/link";

type NavCtaProps = {
  primaryHref?: string;
  primaryLabel?: string;
  secondaryHref?: string;
  secondaryLabel?: string;
};

export default function NavCta({
  primaryHref = "/dashboard",
  primaryLabel = "Open dashboard",
  secondaryHref = "/demo",
  secondaryLabel = "Live demo",
}: NavCtaProps) {
  return (
    <div className="site-nav__actions">
      {secondaryHref && secondaryLabel ? (
        <Link href={secondaryHref} className="btn btn-secondary">
          {secondaryLabel}
        </Link>
      ) : null}
      <Link href={primaryHref} className="btn btn-primary">
        {primaryLabel}
      </Link>
    </div>
  );
}
