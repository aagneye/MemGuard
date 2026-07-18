export type DrawerId =
  | "home"
  | "console"
  | "memory"
  | "governance"
  | "conflicts"
  | "trust"
  | "alerts"
  | "activity"
  | "settings";

export type DrawerItemDef = {
  id: DrawerId;
  label: string;
  hint: string;
};

export const DRAWER_ITEMS: DrawerItemDef[] = [
  { id: "home", label: "Home", hint: "Overview & health" },
  { id: "console", label: "Console", hint: "Live agent chat" },
  { id: "memory", label: "Memory Mapping", hint: "Visual memory map" },
  { id: "governance", label: "Governance", hint: "Event audit trail" },
  { id: "conflicts", label: "Conflicts", hint: "Resolve clashes" },
  { id: "trust", label: "Trust Analytics", hint: "Tier distribution" },
  { id: "alerts", label: "Security Alerts", hint: "Poison flags" },
  { id: "activity", label: "Activity", hint: "Process monitor" },
  { id: "settings", label: "Settings", hint: "Demo preferences" },
];
