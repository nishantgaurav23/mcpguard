# S1.2 -- Developer Commands Checklist

## Implementation

- [x] Makefile: .PHONY declarations for all targets
- [x] Makefile: venv target (uv venv)
- [x] Makefile: install target (uv sync)
- [x] Makefile: install-dev target (uv sync --extra dev)
- [x] Makefile: lint target (ruff check + format --check)
- [x] Makefile: typecheck target (mypy strict)
- [x] Makefile: format target (ruff format + check --fix)
- [x] Makefile: test target (pytest with coverage)
- [x] Makefile: check target (lint + typecheck + test)
- [x] Makefile: eval placeholder
- [x] Makefile: serve placeholder
- [x] Makefile: scan placeholder
- [x] Makefile: clean target

## Testing

- [x] test_makefile_exists
- [x] test_phony_targets
- [x] test_required_targets
- [x] test_check_depends_on_lint_typecheck_test
- [x] test_ruff_check_runs
- [x] test_ruff_format_check_runs
- [x] test_mypy_runs
- [x] test_eval_placeholder
- [x] test_serve_placeholder
- [x] test_scan_placeholder

## Verification

- [x] All 10 tests pass
- [x] Lint clean
- [x] Mypy clean
- [x] Checklist complete
