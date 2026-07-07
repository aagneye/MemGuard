"use client";

import Script from "next/script";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID ?? "";

declare global {
  interface Window {
    google?: any;
  }
}

type AuthPayload = {
  token: string;
  user: { id: string; email: string; name: string; picture?: string | null };
};

export default function LandingPage() {
  const router = useRouter();
  const [error, setError] = useState("");

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("memguard_token") : null;
    if (token) router.push("/dashboard");
  }, [router]);

  async function onGoogleCredential(credential: string) {
    setError("");
    const res = await fetch(`${API_BASE}/auth/google/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ credential }),
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      setError(body.detail ?? "Sign-in failed");
      return;
    }
    const payload: AuthPayload = await res.json();
    localStorage.setItem("memguard_token", payload.token);
    localStorage.setItem("memguard_user", JSON.stringify(payload.user));
    router.push("/dashboard");
  }

  function renderGoogleButton() {
    if (!window.google || !GOOGLE_CLIENT_ID) return;
    window.google.accounts.id.initialize({
      client_id: GOOGLE_CLIENT_ID,
      callback: (response: { credential: string }) => void onGoogleCredential(response.credential),
    });
    window.google.accounts.id.renderButton(document.getElementById("google-signin"), {
      type: "standard",
      shape: "pill",
      theme: "outline",
      text: "signin_with",
      size: "large",
      width: 280,
    });
  }

  return (
    <main className="landing">
      <Script src="https://accounts.google.com/gsi/client" onLoad={renderGoogleButton} strategy="afterInteractive" />
      <div className="landing-card">
        <h1>MemGuard</h1>
        <p>Trust-aware memory guardrails for LLM agents.</p>
        <ul>
          <li>Persistent cross-session memory recall</li>
          <li>Poisoning/conflict detection before action</li>
          <li>Team workspace and memory operations dashboard</li>
        </ul>
        <div id="google-signin" />
        {!GOOGLE_CLIENT_ID && (
          <p className="muted">Set NEXT_PUBLIC_GOOGLE_CLIENT_ID to enable real Google Sign-In.</p>
        )}
        {error && <p className="error-text">{error}</p>}
      </div>
    </main>
  );
}
