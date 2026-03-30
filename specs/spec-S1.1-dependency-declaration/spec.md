# S1.1 -- Dependency Declaration

**Phase:** 1 -- Project Foundation
**Location:** `pyproject.toml`, `.env.example`
**Depends On:** --
**Status:** pending

---

## Goal

Declare all runtime and development dependencies in `pyproject.toml` using Hatchling build backend with src-layout. Provide `.env.example` documenting all required environment variables.

---

## Requirements

### R1: pyproject.toml -- Build System

- Build backend: `hatchling`
- `[build-system]` requires `hatchling`
- `[tool.hatch.build.targets.wheel]` packages = `["src/mcpguard"]`

### R2: pyproject.toml -- Project Metadata

- `name = "mcpguard"`
- `version` matches `src/mcpguard/__init__.py:__version__`
- `description` is a short summary
- `readme = "README.md"`
- `license = {text = "MIT"}`
- `requires-python = ">=3.10"`
- `classifiers` include Python version and license trove classifiers

### R3: pyproject.toml -- Runtime Dependencies

All pinned with minimum versions:

| Package | Minimum | Purpose |
|---------|---------|---------|
| `pydantic-ai[mcp]` | `>=1.70` | Agent framework + MCP client/server |
| `typer` | `>=0.12.0` | CLI framework |
| `rich` | `>=13.0.0` | Terminal output |
| `httpx` | `>=0.27.0` | Async HTTP client |
| `logfire` | `>=0.3.0` | Observability |
| `python-dotenv` | `>=1.0.0` | .env file loading |

### R4: pyproject.toml -- Dev Dependencies

Under `[project.optional-dependencies] dev`:

| Package | Minimum | Purpose |
|---------|---------|---------|
| `pytest` | `>=8.0.0` | Test runner |
| `pytest-asyncio` | `>=0.23.0` | Async test support |
| `pytest-cov` | `>=4.0.0` | Coverage reporting |
| `ruff` | `>=0.5.0` | Linting + formatting |
| `mypy` | `>=1.10.0` | Type checking |

### R5: pyproject.toml -- Entry Point

```toml
[project.scripts]
mcpguard = "mcpguard.cli:app"
```

### R6: pyproject.toml -- Tool Configuration

- **ruff**: `line-length = 100`, `target-version = "py310"`, select `["E", "F", "I", "UP", "B"]`
- **mypy**: `python_version = "3.10"`, `strict = true`
- **pytest**: `addopts = "--cov=mcpguard --cov-report=term-missing"`, `asyncio_mode = "auto"`, `testpaths = ["tests"]`

### R7: .env.example

Document all environment variables with empty values:

```
GEMINI_API_KEY=
GROQ_API_KEY=
LOGFIRE_TOKEN=
LOG_LEVEL=INFO
```

---

## Acceptance Criteria

1. `pip install -e .` succeeds in a clean venv
2. `pip install -e ".[dev]"` installs all dev tools
3. `mcpguard` CLI entry point is available after install
4. `python -c "import mcpguard; print(mcpguard.__version__)"` prints version
5. `ruff check src/` runs without config errors
6. `mypy src/mcpguard/` runs without config errors
7. `pytest tests/` runs and discovers tests
8. `.env.example` documents all required env vars
9. Version in pyproject.toml matches `__init__.py`

---

## Test Plan

- `test_pyproject_structure`: Validate pyproject.toml has all required sections
- `test_dependencies_installable`: Verify `pip install -e ".[dev]"` succeeds
- `test_entry_point`: Verify `mcpguard` CLI is registered
- `test_version_consistency`: `pyproject.toml` version == `__init__.py` version
- `test_env_example_keys`: `.env.example` contains all required keys
- `test_ruff_config`: ruff runs with configured rules
- `test_mypy_config`: mypy runs in strict mode
