import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = { title: "Page Not Found" };

export default function NotFound() {
  return (
    <main
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: "16px",
        fontFamily: "Inter, Arial, sans-serif",
        background: "#0f172a",
        color: "#e2e8f0",
        textAlign: "center",
        padding: "24px",
      }}
    >
      <span style={{ fontSize: "64px" }}>🔍</span>
      <h1 style={{ fontSize: "32px", margin: 0, color: "#f1f5f9" }}>404 — Page not found</h1>
      <p style={{ color: "#94a3b8", maxWidth: 360 }}>
        This memory doesn&apos;t exist — or it decayed. Head back to the demo.
      </p>
      <Link
        href="/"
        style={{
          background: "#6366f1",
          color: "#fff",
          padding: "10px 24px",
          borderRadius: "8px",
          textDecoration: "none",
          fontWeight: 600,
        }}
      >
        Back to landing
      </Link>
    </main>
  );
}
