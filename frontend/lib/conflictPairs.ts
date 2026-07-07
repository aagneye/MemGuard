import type { MemoryItem } from "./types";

export type ConflictPair = { oldMemory: MemoryItem; newMemory: MemoryItem };
export type GroupedMemories = { standalone: MemoryItem[]; conflictPairs: ConflictPair[] };

/** Groups conflicted memory rows into old/new pairs so the UI can render
 * one "Accept new / Keep old" decision instead of two redundant rows. */
export function groupMemoriesByConflict(memories: MemoryItem[]): GroupedMemories {
  const byId = new Map(memories.map((m) => [m.id, m]));
  const seen = new Set<string>();
  const conflictPairs: ConflictPair[] = [];
  const standalone: MemoryItem[] = [];

  for (const memory of memories) {
    if (seen.has(memory.id)) continue;
    if (memory.status === "conflicted" && memory.conflicts_with && byId.has(memory.conflicts_with)) {
      const counterpart = byId.get(memory.conflicts_with)!;
      seen.add(memory.id);
      seen.add(counterpart.id);
      const [oldMemory, newMemory] =
        new Date(memory.created_at) <= new Date(counterpart.created_at) ? [memory, counterpart] : [counterpart, memory];
      conflictPairs.push({ oldMemory, newMemory });
      continue;
    }
    standalone.push(memory);
  }

  return { standalone, conflictPairs };
}
