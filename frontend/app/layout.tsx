import "./globals.css";
import { ReactNode } from "react";

export const metadata = {
  title: "MemGuard",
  description: "Trust-aware memory agent demo",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
