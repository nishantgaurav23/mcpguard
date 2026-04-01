# S1.5 -- Structured Logging Setup Checklist

## Implementation

- [x] src/mcpguard/utils/__init__.py exists
- [x] setup_logging: accepts log_level + logfire_token primitives
- [x] setup_logging: resolves level via getattr with INFO fallback
- [x] setup_logging: configures root logger with StreamHandler + Formatter
- [x] setup_logging: idempotent via _configured flag
- [x] setup_logging: optional logfire import inside function
- [x] setup_logging: try/except on logfire import (ImportError)
- [x] setup_logging: try/except on logfire.configure() (any Exception)
- [x] get_logger: wraps logging.getLogger(name)
- [x] No circular imports with config.py

## Testing

- [x] test_setup_logging_sets_log_level
- [x] test_setup_logging_invalid_level_defaults_to_info
- [x] test_setup_logging_idempotent
- [x] test_setup_logging_logfire_import_failure
- [x] test_setup_logging_logfire_config_failure
- [x] test_get_logger_returns_logger
- [x] test_logging_does_not_duplicate_handlers_across_tests

## Verification

- [x] All 7 tests pass
- [x] ruff check clean
- [x] mypy clean
- [x] Checklist complete
