"use client";

import { useState } from "react";
import SiteNavbar from "../nav/SiteNavbar";
import DashboardDrawer from "./DashboardDrawer";
import { DrawerId } from "./drawerItems";
import HomeView from "./views/HomeView";
import ConsoleView from "./views/ConsoleView";
import MemoryMappingView from "./views/MemoryMappingView";
import GovernanceView from "./views/GovernanceView";
import ConflictsView from "./views/ConflictsView";
import TrustAnalyticsView from "./views/TrustAnalyticsView";
import AlertsView from "./views/AlertsView";
import ActivityView from "./views/ActivityView";
import SettingsView from "./views/SettingsView";

const DASH_LINKS = [
  { href: "/dashboard", label: "Workspace" },
  { href: "/demo", label: "Console" },
  { href: "/#proof", label: "Proof" },
];

function renderView(id: DrawerId) {
  switch (id) {
    case "home":
      return <HomeView />;
    case "console":
      return <ConsoleView />;
    case "memory":
      return <MemoryMappingView />;
    case "governance":
      return <GovernanceView />;
    case "conflicts":
      return <ConflictsView />;
    case "trust":
      return <TrustAnalyticsView />;
    case "alerts":
      return <AlertsView />;
    case "activity":
      return <ActivityView />;
    case "settings":
      return <SettingsView />;
    default:
      return <HomeView />;
  }
}

export default function DashboardShell() {
  const [active, setActive] = useState<DrawerId>("home");
  const [drawerOpen, setDrawerOpen] = useState(false);

  return (
    <div className="dash-shell">
      <SiteNavbar variant="dashboard" links={DASH_LINKS} />
      <div className="dash-body">
        <DashboardDrawer
          active={active}
          onSelect={setActive}
          open={drawerOpen}
          onClose={() => setDrawerOpen(false)}
        />
        <main className="dash-main">
          <button
            type="button"
            className="btn btn-secondary dash-menu-btn"
            onClick={() => setDrawerOpen(true)}
          >
            Menu
          </button>
          {renderView(active)}
        </main>
      </div>
    </div>
  );
}
