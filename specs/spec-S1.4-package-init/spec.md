# S1.4 -- Package Initialization

**Phase:** 1 -- Project Foundation
**Location:** `src/mcpguard/__init__.py`, `src/mcpguard/__main__.py`
**Depends On:** S1.1
**Status:** pending

---

## Goal

Ensure the mcpguard package is correctly structured for both installed entry point (`mcpguard`) and module execution (`python -m mcpguard`). Single source of truth for CLI delegation, no side effects on import, minimal public API surface.

---

## Requirements

### R1: __init__.py -- Minimal Public API

- Export only `__version__`
- No re-exports of internal modules (ScanConfig, Settings, etc.)
- No side effects on import

### R2: __main__.py -- Guarded Module Execution

- Import `app` from `mcpguard.cli`
- Execute `app()` only inside `if __name__ == "__main__":` guard
- No duplicated CLI logic -- delegation only
- Safe to import without triggering CLI execution

### R3: Execution Path Equivalence

- `mcpguard` (entry point) and `python -m mcpguard` must invoke the same CLI app
- No divergence in behavior between the two paths

---

## Acceptance Criteria

1. `import mcpguard.__main__` does NOT execute CLI or raise SystemExit
2. `python -m mcpguard --help` returns exit code 0 with help text
3. `__main__.app is cli.app` (identity check -- same object, no duplication)
4. `__init__.py` exports only `__version__`
5. ruff and mypy pass

---

## Test Plan

- `test_main_import_has_no_side_effects`
- `test_python_module_execution_runs_cli`
- `test_main_delegates_to_cli_app`
