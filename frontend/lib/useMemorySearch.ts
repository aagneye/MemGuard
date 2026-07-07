"use client";

import { useState, useCallback } from "react";
import type { MemoryItem } from "./types";
import { API_BASE } from "./api";

interface UseMemorySearchResult {
  results: MemoryItem[];
  loading: boolean;
  searched: boolean;
  search: (userId: string, query: string, topK?: number) => Promise<void>;
  clear: () => void;
}

export function useMemorySearch(): UseMemorySearchResult {
  const [results, setResults] = useState<MemoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const search = useCallback(async (userId: string, query: string, topK = 5) => {
    if (!query.trim()) return;
    setLoading(true);
    setSearched(false);
    try {
      const res = await fetch(
        `${API_BASE}/memories/search?user_id=${encodeURIComponent(userId)}&q=${encodeURIComponent(query)}&top_k=${topK}`
      );
      if (res.ok) {
        setResults(await res.json());
      } else {
        setResults([]);
      }
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
      setSearched(true);
    }
  }, []);

  const clear = useCallback(() => {
    setResults([]);
    setSearched(false);
  }, []);

  return { results, loading, searched, search, clear };
}
