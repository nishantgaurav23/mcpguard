# S1.2 -- Developer Commands

**Phase:** 1 -- Project Foundation
**Location:** `Makefile`
**Depends On:** --
**Status:** pending

---

## Goal

Provide a Makefile with all developer workflow targets: environment setup, quality checks, testing, formatting, and placeholder targets for future specs.

---

## Requirements

### R1: Environment Targets

- `make venv` -- Create virtual environment using `uv`
- `make install` -- Install runtime dependencies
- `make install-dev` -- Install runtime + dev dependencies

### R2: Quality Targets

- `make lint` -- Run `ruff check` and `ruff format --check`
- `make typecheck` -- Run `mypy` in strict mode
- `make format` -- Auto-format with `ruff format` and `ruff check --fix`

### R3: Testing Targets

- `make test` -- Run pytest with coverage
- `make check` -- Run lint + typecheck + test (all quality gates)

### R4: Placeholder Targets

- `make eval` -- Placeholder for pydantic-evals benchmark (S10.1)
- `make serve` -- Placeholder for FastMCP server mode (S9.1)
- `make scan` -- Placeholder for CLI scan (S4.1)

### R5: Utility Targets

- `make clean` -- Remove all generated artifacts (.venv, dist, caches, etc.)

### R6: Phony Declarations

All targets declared as `.PHONY` to avoid conflicts with filenames.

---

## Acceptance Criteria

1. `make venv` creates a `.venv` directory (requires `uv`)
2. `make install-dev` installs all dependencies
3. `make lint` runs ruff checks
4. `make typecheck` runs mypy in strict mode
5. `make test` runs pytest with coverage
6. `make check` runs all three quality gates in sequence
7. `make format` auto-formats code
8. `make clean` removes all generated artifacts
9. Placeholder targets print informative messages
10. All targets are declared `.PHONY`

---

## Test Plan

- `test_makefile_exists`: Verify Makefile exists at project root
- `test_phony_targets`: All expected targets declared in .PHONY
- `test_required_targets`: All required targets exist (venv, install, install-dev, lint, typecheck, format, test, check, eval, serve, scan, clean)
- `test_check_depends_on_lint_typecheck_test`: `check` target depends on lint, typecheck, test
- `test_make_lint_runs`: `make lint` executes successfully
- `test_make_typecheck_runs`: `make typecheck` executes successfully
- `test_make_test_runs`: `make test` executes successfully
- `test_placeholder_targets`: eval, serve, scan print placeholder messages
