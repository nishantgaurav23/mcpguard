# S1.1 -- Dependency Declaration Checklist

## Implementation

- [x] pyproject.toml: build-system with hatchling
- [x] pyproject.toml: project metadata (name, version, description, license, python)
- [x] pyproject.toml: classifiers (Python versions, license)
- [x] pyproject.toml: runtime dependencies with minimum versions
- [x] pyproject.toml: python-dotenv added to runtime deps
- [x] pyproject.toml: dev dependencies under optional-dependencies
- [x] pyproject.toml: entry point (mcpguard = mcpguard.cli:app)
- [x] pyproject.toml: ruff config (line-length, target-version, lint select)
- [x] pyproject.toml: mypy config (strict mode)
- [x] pyproject.toml: pytest config (cov, asyncio_mode, testpaths)
- [x] pyproject.toml: hatch build targets for src layout
- [x] .env.example: all required env vars documented
- [x] Version consistency: pyproject.toml == __init__.py

## Testing

- [x] test_pyproject_structure (7 tests)
- [x] test_tool_config (3 tests)
- [x] test_version_consistency (1 test)
- [x] test_env_example (2 tests)
- [x] test_entry_point (3 tests)

## Verification

- [x] `pip install -e ".[dev]"` succeeds
- [x] `mcpguard` CLI responds
- [x] `ruff check src/` runs clean
- [x] `mypy src/mcpguard/` runs clean
- [x] `pytest tests/` discovers and runs tests
- [x] All 16 tests pass
- [x] Checklist complete
