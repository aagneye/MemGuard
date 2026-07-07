#!/usr/bin/env python3
"""Export a user's memories to JSON or CSV for offline review.

Usage:
  python scripts/export_memories.py --user-id demo_alice --format json
  python scripts/export_memories.py --user-id demo_alice --format csv --output alice.csv
"""
import argparse
import csv
import json
import sys

try:
    import httpx
except ImportError:
    print("Run: pip install httpx")
    sys.exit(1)


def export_memories(base_url: str, user_id: str, fmt: str, output: str | None) -> None:
    client = httpx.Client(base_url=base_url, timeout=15.0)
    r = client.get("/memories", params={"user_id": user_id})
    r.raise_for_status()
    memories = r.json()

    if not memories:
        print(f"No memories found for user '{user_id}'.")
        return

    if fmt == "json":
        content = json.dumps(memories, indent=2)
        if output:
            with open(output, "w") as f:
                f.write(content)
            print(f"Exported {len(memories)} memories to {output}")
        else:
            print(content)

    elif fmt == "csv":
        fields = ["id", "user_id", "fact_text", "trust_tier", "source", "status", "ttl_days", "created_at", "days_remaining"]
        rows = [{k: m.get(k, "") for k in fields} for m in memories]

        if output:
            with open(output, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            print(f"Exported {len(memories)} memories to {output}")
        else:
            writer = csv.DictWriter(sys.stdout, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export MemGuard memories")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    parser.add_argument("--base-url", default="http://localhost:8000")
    args = parser.parse_args()
    export_memories(args.base_url, args.user_id, args.format, args.output)
