import type { Metadata, Viewport } from "next";
import "./globals.css";
import { ReactNode } from "react";

export const metadata: Metadata = {
  title: {
    default: "MemGuard — Trust-Aware Memory Agent",
    template: "%s | MemGuard",
  },
  description:
    "MemGuard is an open-source trust-aware memory agent for AI assistants. " +
    "It scores every memory for provenance and trust, detects conflicts, and guards against poisoning.",
  keywords: ["AI memory", "trust scoring", "memory agent", "LLM safety", "Qwen", "MemGuard"],
  authors: [{ name: "MemGuard" }],
  openGraph: {
    title: "MemGuard — Trust-Aware Memory Agent",
    description: "Guard your AI's memory from hallucinations, conflicts, and poisoning attacks.",
    type: "website",
    url: "https://github.com/aagneye/MemGuard",
  },
  twitter: {
    card: "summary_large_image",
    title: "MemGuard",
    description: "Trust-Aware Memory Agent for AI Assistants — Qwen Cloud Hackathon 2026",
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#0f172a",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
