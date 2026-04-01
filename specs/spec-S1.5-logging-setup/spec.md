# S1.5 -- Structured Logging Setup

**Phase:** 1 -- Project Foundation
**Location:** `src/mcpguard/utils/logging.py`
**Depends On:** S1.3
**Status:** pending

---

## Goal

Provide a centralized, structured logging system with optional Logfire observability. Configure once at startup, use everywhere via `get_logger()`. Graceful degradation when Logfire is unavailable.

---

## Requirements

### R1: setup_logging Function

- Signature: `setup_logging(log_level: str, logfire_token: str | None = None) -> None`
- Accepts primitives (not Settings object) to avoid circular imports
- Resolves log level via `getattr(logging, level.upper(), logging.INFO)` -- invalid levels fall back to INFO
- Configures root logger: sets level, adds StreamHandler with formatted output
- Idempotent: `_configured` module-level flag prevents duplicate setup
- Called exactly once at CLI startup

### R2: Optional Logfire Integration

- If `logfire_token` is provided, attempt `import logfire` and `logfire.configure(token=...)`
- Import failure (logfire not installed): log debug message, continue with console-only
- Configure failure (API unreachable, bad token): log debug message, continue with console-only
- Observability must NEVER break core functionality

### R3: get_logger Function

- Signature: `get_logger(name: str | None = None) -> logging.Logger`
- Wraps `logging.getLogger(name)` for consistent access across modules
- Pull-based: modules call `get_logger(__name__)`, no logger injection needed

### R4: Package Structure

- `src/mcpguard/utils/__init__.py` must exist (empty)
- No circular imports with `models/config.py`

---

## Acceptance Criteria

1. `setup_logging("DEBUG", None)` sets root logger to DEBUG
2. `setup_logging("VERBOSE", None)` falls back to INFO (invalid level)
3. Calling `setup_logging` twice does not duplicate handlers
4. Missing logfire import does not crash
5. Failed `logfire.configure()` does not crash
6. `get_logger(__name__)` returns a `logging.Logger` instance
7. ruff and mypy pass

---

## Test Plan

- `test_setup_logging_sets_log_level`
- `test_setup_logging_invalid_level_defaults_to_info`
- `test_setup_logging_idempotent`
- `test_setup_logging_logfire_import_failure`
- `test_setup_logging_logfire_config_failure`
- `test_get_logger_returns_logger`
- `test_logging_does_not_duplicate_handlers_across_tests`
