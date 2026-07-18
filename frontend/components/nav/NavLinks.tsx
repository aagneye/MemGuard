export type NavLinkItem = { href: string; label: string };

const DEFAULT_LINKS: NavLinkItem[] = [
  { href: "/#loop", label: "The loop" },
  { href: "/#compare", label: "Compare" },
  { href: "/#audience", label: "Who it's for" },
  { href: "/#proof", label: "Proof" },
  { href: "/#results", label: "Results" },
];

export default function NavLinks({ links = DEFAULT_LINKS }: { links?: NavLinkItem[] }) {
  return (
    <ul className="site-nav__links">
      {links.map((link) => (
        <li key={link.href}>
          <a href={link.href}>{link.label}</a>
        </li>
      ))}
    </ul>
  );
}
