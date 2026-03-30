# S1.1 Dependency Declaration -- Predict First Q&A

**Date**: 2026-03-30
**Strategy**: /learn-predict (Strategy 1 -- Predict First)
**Mode**: B) Architecture Review
**Spec**: S1.1 Dependency Declaration

---

## Questions Asked

### Q1: What files will you create, and what goes in each one?

**My Answer**:
- `pyproject.toml` -- build-system (hatchling), [project] metadata + runtime deps, [project.scripts] entry point, [project.optional-dependencies] dev deps, tooling configs (ruff, mypy, pytest)
- `.env.example` -- GEMINI_API_KEY, GROQ_API_KEY, LOGFIRE_TOKEN, LOG_LEVEL=INFO. No defaults for secrets.
- `README.md` -- minimal project description (implicit requirement)
- `.gitignore` -- .venv/, __pycache__/, .env, .pytest_cache/, .mypy_cache/, .coverage (implicit requirement)

**Score**: SOLID

**Feedback**: All correct files identified. Caught implicit files (README, .gitignore) that spec doesn't list. One mistake: wrote `[PROJECT]` instead of `[project]` -- TOML is case-sensitive.

---

### Q2: How will you structure the dependency declarations?

**My Answer**:
- Use minimum version pins (`>=`), not exact pins
- Let `uv` resolve and lock via `uv.lock` for reproducibility
- Runtime deps in `[project.dependencies]`, dev deps in `[project.optional-dependencies.dev]`
- Install with `uv pip install -e .[dev]`
- hatchling = build backend, uv = dependency resolution + env management (different roles)
- Add `requires-python = ">=3.11, <3.13"`

**Score**: PARTIAL

**Feedback**:
- Strategy is sound (minimum versions + lockfile + separation)
- **Mistake**: `requires-python` should be `>=3.10` not `>=3.11` -- CLAUDE.md explicitly says Python 3.10+
- **Mistake**: `pydantic-ai[mcp]>=0.0.0` is placeholder -- should be `>=1.70` per CLAUDE.md
- Upper bound `<3.13` is debatable -- blocks newer Python users without known incompatibility

---

### Q3: What decisions about entry point and package layout?

**My Answer**:
- Structure: `src/mcpguard/__init__.py` + `src/mcpguard/cli.py`
- cli.py: Typer app instance, `@app.command()` decorator
- Entry point: `mcpguard = "mcpguard.cli:app"`
- `__init__.py`: `__version__ = "0.1.0"`
- .env loading via `pydantic_settings.BaseSettings` with `env_file = ".env"`

**Score**: PARTIAL

**Feedback**:
- Correct Typer wiring and __init__.py content
- **Critical miss**: src-layout requires hatchling configuration:
  ```toml
  [tool.hatch.build.targets.wheel]
  packages = ["src/mcpguard"]
  ```
  Without this, `pip install -e .` installs nothing and `mcpguard` command fails with `ModuleNotFoundError`
- `pydantic_settings` is a separate package (not included in pydantic-ai). Would need to add to deps. Also, .env loading belongs in S1.3 scope, not S1.1.

---

## Key Lessons Learned

1. **src-layout always needs build config** -- hatchling doesn't auto-discover packages under `src/`. Must explicitly declare `packages = ["src/mcpguard"]`.
2. **Check version requirements against project docs** -- CLAUDE.md said 3.10+, I wrote 3.11. Always cross-reference.
3. **TOML is case-sensitive** -- `[project]` not `[PROJECT]`.
4. **Scope boundaries matter** -- pydantic_settings/.env loading is S1.3, not S1.1. Don't pull in dependencies that belong to later specs.
5. **Placeholder versions are not acceptable** -- look up actual minimum versions from project docs.

---

## What I Got Right

- File list including implicit requirements
- Dependency separation strategy (runtime vs dev)
- uv vs hatchling role distinction
- Typer entry point wiring pattern
- Empty secrets in .env.example (no defaults)

## What I Missed

- src-layout hatchling config (critical)
- Python version mismatch (3.10 vs 3.11)
- pydantic-ai actual minimum version (1.70)
- TOML case sensitivity
- Scope creep (pulling pydantic_settings into S1.1)

---

## Phase 2: Implementation Review (Signatures + Hints)

**Date**: 2026-03-30

After receiving function signatures and one-line hints, I implemented all 6 files.

### First Submission Issues

| File | Result | Issues Found |
|------|--------|-------------|
| `pyproject.toml` | 3 typos | `adopts` -> `addopts`, `python-version` -> `python_version`, missing `[mcp]` extra |
| `src/mcpguard/__init__.py` | PERFECT | -- |
| `src/mcpguard/cli.py` | PERFECT | -- |
| `.env.example` | PERFECT | All keys empty, LOG_LEVEL=INFO default |
| `.gitignore` | PERFECT | Thorough with section headers |
| `README.md` | PERFECT | Minimal and sufficient |

### After Fixes

All 6 files PERFECT. Verification commands passed:
- `uv pip install -e ".[dev]"` -- installed successfully
- `mcpguard --help` -- entry point works
- `python -c "from mcpguard import __version__"` -- import works
- `ruff check src/` -- clean
- `mypy src/` -- clean
- `pytest tests/ -v` -- passes

### Implementation Lessons

1. **Typos in config keys are silent failures** -- `adopts` vs `addopts` won't error, pytest just ignores it. Always double-check tool config key names.
2. **mypy uses underscores** -- `python_version` not `python-version`. Different tools have different naming conventions in TOML.
3. **Don't forget extras** -- `pydantic-ai[mcp]` not `pydantic-ai`. The MCP client/server support is an optional extra.
4. **Permission settings can block .env.example** -- `Read(.env.*)` deny rule catches `.env.example` too. Narrowed to `Read(.env)` only.

### Overall Assessment

- Prediction phase: caught most architecture decisions, missed src-layout config and version details
- Implementation phase: got structure right on first try, 3 typos in pyproject.toml config keys
- Progression: ready for Phase 2 (signatures + hints) on similar packaging tasks, Phase 1 still needed for unfamiliar patterns (PydanticAI agents, FastMCP)
