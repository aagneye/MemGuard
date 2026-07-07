# Contributing to MemGuard

Thank you for your interest in MemGuard! Contributions are welcome.

## Development Setup

```bash
bash scripts/setup.sh
```

Or manually:

```bash
# Backend
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Running Tests

```bash
cd backend && pytest tests/ -v
```

## Commit Conventions

We follow strict atomic commits. See [cursorrules](cursorrules) for the full rules.

Short version:
- One logical change per commit
- Format: `type(scope): short description`
- Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `style`
- Maximum 72 characters in the subject line

## Pull Request Guidelines

1. Keep PRs focused — one feature or bug fix per PR.
2. All tests must pass before review.
3. Update `CHANGELOG.md` with your changes.

## Architecture Notes

See `docs/ARCHITECTURE.md` for the full system design.

The key modules:
- `llm_extract.py` — 2nd Qwen call for structured fact extraction
- `llm_adjudicate.py` — 3rd Qwen call for conflict classification
- `service_memory.py` — orchestration of the full memory pipeline
- `mcp_server.py` — MCP tool server for Qwen agent integration
