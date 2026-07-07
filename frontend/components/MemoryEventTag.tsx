"use client";

import type { MemoryEvent } from "../lib/types";

/** Inline tag shown under an agent reply — the whole point of Screen A:
 * memory writes/flags/conflicts must be visible, not silent. */
export default function MemoryEventTag({ event }: { event: MemoryEvent }) {
  if (event.type === "stored") {
    return (
      <div className="inline-tag inline-tag-stored">
        📌 remembered: "{event.fact}" ({event.trust_tier ?? "high"})
      </div>
    );
  }
  if (event.type === "flagged") {
    return (
      <div className="inline-tag inline-tag-flagged">
        ⚠️ flagged: "{event.fact}" — untrusted source, not acted on
      </div>
    );
  }
  return (
    <div className="inline-tag inline-tag-conflict">⚠️ flagged: conflicts with existing memory</div>
  );
}
