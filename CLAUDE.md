# MCPGuard — Claude Code Context

## Project
AI-powered MCP security auditor. Connects to MCP servers, performs comprehensive vulnerability scanning via a 4-layer detection pipeline (static rules → schema heuristics → LLM semantic analysis → hash integrity), produces structured reports. Ships as both CLI tool (`pip install mcpguard`) AND an MCP server (usable from Claude Desktop, Cursor). PydanticAI for intelligent analysis, FastMCP for server mode, pydantic-evals for self-evaluation benchmark.

**Stack:** Python 3.10+ · PydanticAI · FastMCP · Typer · Rich · Gemini 2.5 Flash (primary LLM) · Groq Llama 3.3 70B (fallback)
**Budget:** Under $20 total. Cost per scan target ≤ $0.02, most scans $0.
**Packaging:** Hatchling + PyPI Trusted Publishers. Entry point: `mcpguard` CLI via `[project.scripts]`.

## Current State
<!-- UPDATE THIS as you complete specs -->
- **Last completed spec:** [S?.?]
- **Currently working on:** [S?.?]
- **Blocked on:** [nothing / describe blocker]
- **Tests passing:** [yes/no — run `make check` to verify]

## Hard Rules
- **NEVER** hardcode API keys. All secrets via `.env` → `src/mcpguard/models/config.py`.
- **NEVER** execute code on target servers. Scan only, never exploit.
- **NEVER** store target server credentials. Read from config files only.
- **NEVER** exfiltrate scan data. Results stay local unless user explicitly exports.
- **ALWAYS** sanitize server responses before processing to prevent injection into MCPGuard's own LLM agent.
- **ALWAYS** write tests before implementation. A file is NEVER done until its tests pass.
- Baseline files stored with `0600` permissions in `~/.mcpguard/`.
- LLM calls are SURGICAL — rule-based checks first (zero cost), LLM only for ambiguous cases (~10-20%).
- Immutable data: never mutate objects, always create new copies.
- Exit codes: `0` = clean, `1` = findings above threshold, `2` = scanner error.

## Workflows
- Before implementing any major design decision, run `/grill-me` to stress-test the plan.
- Use spec-driven development: every code file traces to a spec ID (S1.1, S2.1, etc.).
- Full spec index lives in `roadmap.md`. Each spec has a folder under `specs/`.
- Each spec folder contains: `spec.md`, `checklist.md`, and `learning-log.md` (all learning Q&A for that spec).

## Learning Content Convention

Learning content lives in exactly 2 places -- nowhere else:
- **`specs/{spec}/learning-log.md`** -- per-spec Q&A (grillme, predict, mimic, socratic, debug -- all append to ONE file per spec)
- **`docs/reviews/phase-{N}-review.md`** -- phase-level design review decisions

## Spec-Driven Development Commands

| Command | Invocation | Purpose |
|---------|------------|---------|
| Start spec dev | `/project:start-spec-dev S1.1 dependency-declaration` | Full lifecycle: create, check deps, implement, verify |
| Create spec | `/project:create-spec S1.1 dependency-declaration` | Creates spec.md + checklist.md from roadmap |
| Check deps | `/project:check-spec-deps S4.1` | Verify prerequisite specs are implemented and passing |
| Implement spec | `/project:implement-spec S1.1` | TDD implementation following spec + checklist |
| Verify spec | `/project:verify-spec S1.1` | Post-implementation audit: tests, lint, outcomes, wiring |

## Commands
```bash
make check           # Lint + type-check + test + coverage (run this before any PR)
make test            # pytest with coverage
make lint            # ruff check + format
make typecheck       # mypy strict
make eval            # Run pydantic-evals benchmark
make serve           # Start MCPGuard as MCP server
make scan            # Run CLI scan on example config
```

## Code Standards
- **Async everywhere**: `async def`, `await`, `httpx.AsyncClient`
- **Pydantic v2 models** for all data in/out
- **PydanticAI Agent** for LLM calls (structured output, auto-retry)
- **BaseDetector ABC** for all detectors (uniform interface)
- **Error handling**: `try/except` wraps all external calls — never crash the scan. On failure: log, return partial result with warning, continue scanning.
- **Graceful degradation**: LLM unavailable → rule-based only with warning.
- **Import order**: stdlib → third-party → local (models, detectors, utils)
- **Ruff** for linting/formatting. **mypy** strict mode.
- **80% minimum coverage**, enforced in CI.

## Commit & PR Conventions
- Commit format: `feat(detector): add SSRF URL parameter analysis` / `fix(scanner): handle timeout on unresponsive servers`
- Prefix with spec ID when applicable: `[S2.1] feat(detector): add poisoning detector`
- One spec per PR. PR description links to spec folder.

## Environment
- **venv**: `.venv` at project root (Python 3.10+)
- **Package manager**: `uv` — single source of truth: `pyproject.toml`
- **Testing**: `source .venv/bin/activate && python -m pytest tests/ -v --tb=short`
- All external services mocked in tests (LLM APIs, MCP connections, Logfire)

## Project Structure
See the full file tree in `docs/structure.md` or explore with `find src/mcpguard -name "*.py" | head -30`.

Key directories:
- `src/mcpguard/detectors/` — one file per vulnerability class, all extend `BaseDetector`
- `src/mcpguard/agents/` — PydanticAI agents (semantic analysis, report generation)
- `src/mcpguard/models/` — all Pydantic models (findings, config, semantic)
- `src/mcpguard/formatters/` — output formats (Rich, JSON, SARIF 2.1.0)
- `evaluation/` — pydantic-evals benchmark (50+ cases) + FastMCP fixture servers
- `specs/` — spec folders (`spec-{number}-{short-name}/spec.md` + `checklist.md`)