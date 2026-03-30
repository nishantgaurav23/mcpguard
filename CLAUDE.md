# MCPGuard -- Claude Code Context

## Project
AI-powered MCP security auditor. Connects to MCP servers, performs comprehensive vulnerability scanning via a 4-layer detection pipeline (static rules -> schema heuristics -> LLM semantic analysis -> hash integrity), produces structured reports. Ships as both CLI tool (`pip install mcpguard`) AND an MCP server (usable from Claude Desktop, Cursor). PydanticAI for intelligent analysis, FastMCP for server mode, pydantic-evals for self-evaluation benchmark.
Stack: Python 3.10+ + PydanticAI + FastMCP + Typer + Rich. Deployment: PyPI + MCP Registry. Budget: under $20.

## Key Rules
- NEVER hardcode API keys. All secrets via .env -> src/mcpguard/models/config.py.
- NEVER execute code on target servers. Scan only, never exploit.
- NEVER store target server credentials. Read from config files only.
- NEVER exfiltrate scan data. Results stay local unless user explicitly exports.
- ALWAYS sanitize server responses before processing to prevent injection into MCPGuard's own LLM agent.
- Baseline files stored with 0600 permissions in `~/.mcpguard/`.
- LLM calls are SURGICAL -- rule-based checks first (zero cost), LLM only for ambiguous cases (~10-20%).
- Cost per scan target: <= $0.02. Most scans should be $0 (free tier).
- Immutable data: never mutate objects, always create new copies.
- Exit codes: 0 = clean, 1 = findings above threshold, 2 = scanner error.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Agent Framework | PydanticAI v1.70+ |
| MCP Server Building | FastMCP (via PydanticAI) |
| CLI Framework | Typer |
| Terminal Output | Rich |
| LLM (primary) | Gemini 2.5 Flash (free: 1,000 RPD) |
| LLM (fallback) | Groq Llama 3.3 70B (free: 14,400 RPD) |
| Evaluation | pydantic-evals (Dataset/Case/Evaluator pattern) |
| Observability | Pydantic Logfire (OTel, 10M spans/month free) |
| Hashing | hashlib (stdlib, SHA-256) |
| HTTP Client | httpx (async) |
| Testing | pytest + pytest-asyncio |
| Linting | ruff |
| Type Checking | mypy (strict) |
| CI/CD | GitHub Actions |
| Packaging | Hatchling + PyPI Trusted Publishers |

## Project Structure

```
mcpguard/
├── .claude/commands/        <- Spec-driven development commands
├── specs/                   <- Spec folders (spec.md + checklist.md each)
├── src/mcpguard/
│   ├── __init__.py          <- __version__
│   ├── cli.py               <- Typer CLI entry point
│   ├── mcp_server.py        <- FastMCP server mode
│   ├── scanner.py           <- Main scan orchestration
│   ├── agents/
│   │   ├── semantic_agent.py    <- PydanticAI semantic analyzer
│   │   └── report_agent.py      <- PydanticAI report generator
│   ├── detectors/
│   │   ├── __init__.py      <- Detector registry
│   │   ├── base.py          <- BaseDetector ABC
│   │   ├── poisoning.py     <- Tool description poisoning
│   │   ├── full_schema.py   <- CyberArk-style schema poisoning
│   │   ├── unicode.py       <- Invisible character detection
│   │   ├── credentials.py   <- Secret pattern matching
│   │   ├── ssrf.py          <- URL parameter analysis
│   │   ├── command_injection.py <- Shell metacharacter detection
│   │   ├── rug_pull.py      <- Hash-based tool pinning
│   │   ├── auth.py          <- OAuth 2.1 compliance
│   │   ├── transport.py     <- TLS/transport analysis
│   │   └── shadowing.py     <- Cross-server analysis
│   ├── models/
│   │   ├── findings.py      <- VulnerabilityFinding, ServerAuditReport
│   │   ├── config.py        <- ScanConfig, CLI config
│   │   └── semantic.py      <- SemanticAnalysis model
│   ├── formatters/
│   │   ├── rich_output.py   <- Rich terminal rendering
│   │   ├── json_output.py   <- JSON formatter
│   │   └── sarif.py         <- SARIF 2.1.0 generator
│   ├── rules/
│   │   ├── patterns.py      <- All regex patterns
│   │   ├── owasp_mapping.py <- OWASP MCP Top 10 mappings
│   │   └── cvss.py          <- Risk scoring logic
│   └── utils/
│       ├── hashing.py       <- SHA-256 tool hashing
│       ├── entropy.py       <- Shannon entropy calculation
│       └── config_loader.py <- MCP config file parsing
├── evaluation/
│   ├── benchmark.yaml       <- pydantic-evals dataset (50+ cases)
│   ├── fixtures/
│   │   ├── clean_server.py
│   │   ├── poisoned_server.py
│   │   ├── credential_leak_server.py
│   │   ├── ssrf_server.py
│   │   ├── injection_server.py
│   │   ├── unicode_server.py
│   │   └── no_auth_server.py
│   ├── run_eval.py
│   └── conftest.py
├── tests/
│   ├── test_detectors/
│   │   ├── test_poisoning.py
│   │   ├── test_full_schema.py
│   │   ├── test_credentials.py
│   │   ├── test_ssrf.py
│   │   ├── test_command_injection.py
│   │   ├── test_rug_pull.py
│   │   └── test_unicode.py
│   ├── test_scanner.py
│   ├── test_mcp_server.py
│   ├── test_formatters.py
│   └── test_cli.py
├── .github/workflows/
│   ├── ci.yml
│   ├── eval.yml
│   └── publish.yml
├── docs/
│   ├── rules.md
│   ├── owasp-mapping.md
│   └── ci-cd-integration.md
├── roadmap.md
├── design.md
├── requirements.md
├── pyproject.toml
└── LICENSE
```

## Spec Folder Convention

Each spec has a dedicated folder under `specs/`:
```
specs/spec-{number}-{short-name}/
  spec.md        <- detailed specification
  checklist.md   <- implementation progress tracker
```
Full spec index is in `roadmap.md`.

## Spec-Driven Development Commands

| Command | Invocation | Purpose |
|---------|------------|---------|
| **Start spec dev** | `/project:start-spec-dev S1.1 dependency-declaration` | Full lifecycle: create, check deps, implement, verify |
| **Create spec** | `/project:create-spec S1.1 dependency-declaration` | Creates spec.md + checklist.md in spec folder from roadmap |
| **Check deps** | `/project:check-spec-deps S4.1` | Verifies all prerequisite specs are implemented and tests pass |
| **Implement spec** | `/project:implement-spec S1.1` | TDD implementation following spec + checklist |
| **Verify spec** | `/project:verify-spec S1.1` | Post-implementation audit: tests, lint, outcomes, wiring |

## Commands

```bash
# Local (after Phase 1 is done)
make venv            # Create .venv at root
make install         # Install runtime deps
make install-dev     # Install + pytest/ruff/mypy
make check           # Lint + type-check + test + coverage
make test            # pytest with coverage
make lint            # ruff check + format
make typecheck       # mypy strict
make format          # ruff format
make eval            # Run pydantic-evals benchmark
make serve           # Start MCPGuard as MCP server
make scan            # Run CLI scan on example config
```

## Environment
- **venv**: `.venv` at project root (Python 3.10+)
- **Package manager**: `uv` -- single source of truth: `pyproject.toml`
- **Entry point**: `mcpguard` CLI via `[project.scripts]`

## Testing
- Run tests: `source .venv/bin/activate && python -m pytest tests/ -v --tb=short`
- All external services mocked (LLM APIs, MCP server connections, Logfire)
- Test fixtures: FastMCP-based vulnerable servers in evaluation/fixtures/
- pytest-asyncio for async test support
- A file is NEVER considered done until its tests pass
- 80% minimum coverage, enforced in CI

## Code Standards
- Async everywhere (async def, await, httpx.AsyncClient)
- Pydantic v2 models for all data in/out
- PydanticAI Agent for LLM calls (structured output, auto-retry)
- BaseDetector ABC for all detectors (uniform interface)
- try/except wraps all external calls -- never crash the scan
- Import order: stdlib -> third-party -> local (models, detectors, utils)
- structlog or Logfire for structured logging
- Ruff for linting and formatting
- mypy strict mode for type safety
- Immutable data patterns: never mutate, always create new

## Key Design Decisions

1. **Spec-driven development** -- every code file traces to a spec ID (S1.1, S2.1, etc.)
2. **TDD strictly enforced** -- tests before implementation, 80% coverage minimum
3. **4-layer detection pipeline** -- static rules (free) -> schema heuristics (free) -> LLM semantic (surgical) -> hash integrity (free)
4. **PydanticAI for intelligent analysis** -- type-safe structured outputs, auto-retry on validation failure
5. **FastMCP for dual-mode** -- CLI tool AND MCP server in one package
6. **pydantic-evals for self-evaluation** -- 50+ labeled benchmark cases, precision/recall/F1
7. **SARIF 2.1.0 output** -- GitHub Code Scanning compatible
8. **Typer + Rich for CLI** -- streaming findings, severity-colored tables
9. **SHA-256 hash pinning** -- deterministic rug pull detection
10. **Modular detector design** -- add new vulnerability classes without refactoring
11. **Immutable data** -- Pydantic models, no in-place mutation
12. **Graceful degradation** -- LLM unavailable -> rule-based only with warning
