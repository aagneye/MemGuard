import SiteLogo from "./SiteLogo";
import NavLinks, { NavLinkItem } from "./NavLinks";
import NavCta from "./NavCta";

type SiteNavbarProps = {
  variant?: "landing" | "dashboard";
  links?: NavLinkItem[];
};

export default function SiteNavbar({ variant = "landing", links }: SiteNavbarProps) {
  const isDashboard = variant === "dashboard";

  return (
    <header className="site-nav" data-variant={variant}>
      <SiteLogo />
      {!isDashboard ? <NavLinks links={links} /> : <NavLinks links={links ?? []} />}
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
