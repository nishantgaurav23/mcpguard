# S1.5 Grillme Log -- Structured Logging

**Date:** 2026-04-01
**Tier:** 2 (Standard Interview)
**Difficulty:** Standard
**Verdict:** READY (13/13 SOLID)

---

## Phase 1: Problem Understanding (4/4 SOLID)

### Q1: What's the problem in one sentence?
**A:** S1.5 provides a structured, centralized, context-aware logging system that supports tracing (spans), consistent formatting, and optional observability (Logfire), which basic print() or logging.getLogger() cannot provide.

**Score: SOLID**

### Q2: Who consumes this?
**A:** Infrastructure-level module used everywhere:
- Scan orchestrator: scan start/end, config snapshot, metrics
- Detectors: findings, rule triggers, skipped checks
- PydanticAI agents: prompt execution, latency, token usage (span context heavy)
- CLI: user actions, errors, progress
- Auth/security: failures, validation steps

Key insight: logging becomes the observability backbone for debugging, performance tracking, and cost monitoring.

**Score: SOLID**

### Q3: What does success look like? Graceful degradation?
**A:** Works with or without Logfire token:
- With token: logs sent to Logfire, spans tracked, structured logs enabled
- Without token: console-only, no tracing, but logging still works, app never crashes

LOG_LEVEL respected from .env, controls verbosity globally. Provide no-op span interface so callers can always use spans without worrying about backend.

**Score: SOLID**

### Q4: Circular import constraint?
**A:** Pass `log_level: str` and `logfire_token: str | None` as primitives instead of importing Settings. Keeps dependency arrow one-way. Caller (CLI) provides settings values.

**Score: SOLID**

---

## Phase 2: Design Interrogation (5/5 SOLID)

### Q1: Architecture / public API?
**A:**
- `setup_logging(log_level: str, logfire_token: str | None) -> None` -- configure once globally
- `get_logger(name: str | None = None) -> logging.Logger` -- wrapper for consistent usage

Returns nothing. Logging is a global side-effect system. Called exactly once at CLI startup.

**Score: SOLID**

### Q2: Data flow / startup sequence?
**A:** CLI starts -> Settings() loads .env -> setup_logging(log_level, logfire_token) -> logging configured globally -> rest of app runs. Deep modules access via `get_logger(__name__)`. Pull-based, not injected.

**Score: SOLID**

### Q3: Edge cases?
**A:**
1. Invalid LOG_LEVEL (e.g., "VERBOSE") -> `getattr(logging, level.upper(), logging.INFO)` fallback
2. setup_logging called twice -> idempotent check: `if logging.getLogger().handlers: return`
3. Logfire not installed -> `try: import logfire except ImportError: logfire = None`

**Score: SOLID**

### Q4: Failure modes?
**A:** Logfire API unreachable or configure() throws -> catch all exceptions, fall back to console logging. Principle: observability must NEVER break core functionality.

**Score: SOLID**

### Q5: Alternatives -- structlog needed?
**A:** No. Use stdlib logging + optional Logfire. Logfire already provides structured output. Avoid extra dependency, keep it simple for early-stage project. No structlog for now.

**Score: SOLID**

---

## Phase 3: Implementation Readiness (4/4 SOLID)

### Q1: Dependencies?
**A:** S1.3 (done). logfire already in pyproject.toml. No new packages. Must create `src/mcpguard/utils/__init__.py` (package doesn't exist yet).

**Score: SOLID**

### Q2: Testing strategy?
**A:** 5 tests with isolation via `_reset_logging()` helper (clear handlers, reset level). Mock Logfire via `monkeypatch.setitem(sys.modules, ...)`. FakeLogfire class for configure() failure simulation.

**Score: SOLID**

### Q3: Integration points?
**A:** 3 new files (utils/__init__.py, utils/logging.py, test file). No changes to cli.py or root __init__.py. Infrastructure only, wiring is a later spec.

**Score: SOLID**

### Q4: Definition of done?
**A:** 3 files created, 0 modified, 5+ tests passing, `make check` green (ruff + mypy + pytest).

**Score: SOLID**

---

## Phase 3.5: Test Cases Gate (SOLID)

Wrote 7 tests (exceeding the 5 described):
1. `test_setup_logging_sets_log_level` -- DEBUG level applied
2. `test_setup_logging_invalid_level_defaults_to_info` -- fallback on invalid level
3. `test_setup_logging_idempotent` -- no duplicate handlers on double call
4. `test_setup_logging_logfire_import_failure` -- no crash when logfire missing
5. `test_setup_logging_logfire_config_failure` -- no crash when configure() throws
6. `test_get_logger_returns_logger` -- returns stdlib Logger instance
7. `test_logging_does_not_duplicate_handlers_across_tests` -- handler isolation

All 7 confirmed RED (ModuleNotFoundError as expected).

---

## Key Learnings

1. **Logging is global side-effect** -- setup_logging returns nothing, get_logger is pull-based. "Configure once, use everywhere."
2. **Graceful degradation is concrete** -- with token: full export; without: console-only; never crash.
3. **Avoid circular imports** -- pass primitives (log_level, logfire_token) not Settings object. One-way dependency arrow.
4. **Idempotent setup** -- check for existing handlers before adding new ones. Critical for test isolation.
5. **No structlog** -- stdlib logging + optional Logfire is sufficient. Avoid unnecessary dependencies early.
6. **Module-level vs function-level import of logfire** -- test behavior depends on this implementation choice. Must be consistent.
