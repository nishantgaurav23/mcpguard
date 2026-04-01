# Phony Declarations
.PHONY: venv install install-dev lint typecheck format test check eval serve scan clean

# Environment
venv:
	@command -v uv >/dev/null 2>&1 || (echo "uv is required. Install from https://github.com/astral-sh/uv" && exit 1)
	@[ -d .venv ] || uv venv

install: venv
	uv sync

install-dev: venv
	uv sync --extra dev

# Quality

lint: install-dev
	uv run ruff check .
	uv run ruff format --check .

typecheck: install-dev
	uv run mypy src/

format: install-dev
	uv run ruff format .
	uv run ruff check . --fix

test: install-dev
	uv run pytest

check: lint typecheck test

# Place holders (future specs)

eval:
	@echo "Not implemented yet (depends on S10.1 -- pydantic-evals benchmark)"

serve:
	@echo "Not implemented yet (depends on S9.1 -- FastMCP server mode)"

scan:
	@echo "Not implemented yet (depends on S4.1 -- scan orchestration)"

clean:
	rm -rf .venv dist build .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
