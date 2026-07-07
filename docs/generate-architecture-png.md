# Generate architecture-diagram.png

The hackathon submission requires an architecture diagram PNG embedded in the README.
The Mermaid source is in `docs/ARCHITECTURE.md`.

## Option 1: Mermaid CLI (recommended)

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i docs/ARCHITECTURE.md -o docs/architecture-diagram.png --theme dark
```

## Option 2: Online (mermaid.live)

1. Open https://mermaid.live
2. Paste the Mermaid diagram from `docs/ARCHITECTURE.md` §5
3. Export as PNG
4. Save to `docs/architecture-diagram.png`

## Option 3: GitHub Rendering

If the repo is public, Mermaid diagrams in Markdown render natively in GitHub.
No PNG generation needed if you link judges directly to the `ARCHITECTURE.md` file.

## Embed in README

Once generated, add to README.md:

```markdown
## Architecture

![MemGuard Architecture](docs/architecture-diagram.png)
```
