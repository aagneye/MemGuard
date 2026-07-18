import type { ReactNode } from "react";

export default function DashEmpty({ children }: { children: ReactNode }) {
  return <div className="dash-empty">{children}</div>;
}
