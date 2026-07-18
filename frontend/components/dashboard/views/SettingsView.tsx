"use client";

import { useState } from "react";

export default function SettingsView() {
  const [demoUser, setDemoUser] = useState("demo_alice");
  const [compact, setCompact] = useState(false);

  return (
    <section>
      <h1 className="dash-view-title">Settings</h1>
      <p className="dash-view-lede">Local demo preferences (browser only — no account required).</p>
      <article className="dash-card">
        <label className="dash-field">
          <span>Default demo user</span>
          <select value={demoUser} onChange={(e) => setDemoUser(e.target.value)}>
            <option value="demo_alice">demo_alice</option>
            <option value="demo_bob">demo_bob</option>
          </select>
        </label>
        <label className="dash-field dash-field--row">
          <input type="checkbox" checked={compact} onChange={(e) => setCompact(e.target.checked)} />
          <span>Compact cards</span>
        </label>
        <p className="muted" style={{ marginBottom: 0 }}>
          Provider and API keys are configured in <span className="dash-mono">.env</span> — see SETUP /
          PRODUCTION docs.
        </p>
      </article>
    </section>
  );
}
