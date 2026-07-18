import SiteLogo from "./SiteLogo";
import NavLinks, { NavLinkItem } from "./NavLinks";
import NavCta from "./NavCta";
import { LANDING_NAV } from "./landingNav";

type SiteNavbarProps = {
  variant?: "landing" | "dashboard";
  links?: NavLinkItem[];
};

export default function SiteNavbar({ variant = "landing", links }: SiteNavbarProps) {
  const isDashboard = variant === "dashboard";
  const resolvedLinks: NavLinkItem[] = links
    ? links
    : isDashboard
      ? []
      : LANDING_NAV.map((l) => ({ href: l.href, label: l.label }));

  return (
    <header className="site-nav" data-variant={variant}>
      <SiteLogo />
      <NavLinks links={resolvedLinks} />
      {isDashboard ? (
        <NavCta
          primaryHref="/demo"
          primaryLabel="Open console"
          secondaryHref="/"
          secondaryLabel="Landing"
        />
      ) : (
        <NavCta />
      )}
    </header>
  );
}
