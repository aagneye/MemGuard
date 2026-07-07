import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Demo",
  description: "MemGuard live demo — chat with a trust-aware memory agent that scores, conflicts, and forgets.",
};

export default function DemoLayout({ children }: { children: ReactNode }) {
  return children;
}
