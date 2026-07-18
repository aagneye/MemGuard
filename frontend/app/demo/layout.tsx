import SiteNavbar from "../../components/nav/SiteNavbar";
import { ReactNode } from "react";

export const metadata = {
  title: "Demo",
  description: "MemGuard live console — chat, memory inspector, governance log.",
};

const DEMO_LINKS = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/#compare", label: "Compare" },
  { href: "/#proof", label: "Proof" },
];

export default function DemoLayout({ children }: { children: ReactNode }) {
  return (
    <div className="demo-layout">
      <SiteNavbar
        variant="dashboard"
        links={DEMO_LINKS}
      />
      {children}
    </div>
  );
}
