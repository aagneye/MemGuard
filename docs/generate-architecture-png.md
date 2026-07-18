# Generate / refresh architecture-diagram.png

The hackathon submission requires an architecture diagram PNG showing how **Qwen Cloud** connects to the **backend**, **data layer**, and **frontend**.

## Canonical files

| File | Role |
|---|---|
| [`architecture-diagram.png`](architecture-diagram.png) | Submission PNG (embedded in root README) |
| [`ARCHITECTURE_DIAGRAM.md`](ARCHITECTURE_DIAGRAM.md) | Code-mapped explanation for judges |
| [`architecture-diagram-overview.mmd`](architecture-diagram-overview.mmd) | High-level Mermaid |
| [`architecture-diagram.mmd`](architecture-diagram.mmd) | Deep module-level Mermaid |

## Regenerate PNG from Mermaid (optional)

```bash
npx --yes @mermaid-js/mermaid-cli \
  -i docs/architecture-diagram-overview.mmd \
  -o docs/architecture-diagram.png \
  -b white \
  -w 1920 \
  -H 1080
```

Then confirm the root README still embeds:

```markdown
![MemGuard System Architecture](docs/architecture-diagram.png)
```

## Devpost tip

Upload `docs/architecture-diagram.png` (or link the GitHub raw URL) as the architecture diagram attachment, and point reviewers at `docs/ARCHITECTURE_DIAGRAM.md` for the layer → source-file map.
