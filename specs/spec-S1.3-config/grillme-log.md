# S1.3 Grillme Log -- ScanConfig + Settings

**Date:** 2026-04-01
**Difficulty:** Standard
**Verdict:** READY (14/15 SOLID, 1 PARTIAL)

---

## Phase 1: Problem Understanding (5/5 SOLID)

### Q1: What exactly are we solving?
**A:** Define a central, typed configuration system that loads environment variables securely and provides a consistent runtime config (ScanConfig) shared across all scanning components.

**Score: SOLID**

### Q2: Who/what is affected? Which parts read vs write?
**A:**
- **Scanner engine** -- Reads: target, severity_threshold, enable_llm, enable_auth_check, baseline_path. Writes: findings, llm_calls
- **LLM integration layer** -- Reads: enable_llm, API keys (via env-backed settings). Writes: llm_calls
- **Auth/Security checks** -- Reads: enable_auth_check. Writes: findings
- **Reporting/output layer** -- Reads: findings, llm_calls, baseline_path
- **Logging (S1.5)** -- Reads: env config (LOG_LEVEL, LOGFIRE_TOKEN). Must NOT write secrets

Key insight: ScanConfig is doing two jobs -- configuration (immutable intent) and execution state (mutable results). This tension must be handled carefully.

**Score: SOLID** -- Identified the critical config/state tension unprompted.

### Q3: What does success look like? Missing env vars?
**A:**
- `GEMINI_API_KEY` missing + `enable_llm=False` -> OK (not required)
- `GEMINI_API_KEY` missing + `enable_llm=True` -> Fail fast with clear error
- `GROQ_API_KEY` missing -> Same logic, optional unless explicitly used
- `LOGFIRE_TOKEN` missing -> Should NOT fail startup, logging degrades gracefully (console-only)

**Score: SOLID** -- Correct tiered approach.

### Q4: Immutability constraint vs mutable findings?
**A:** Split into:
1. **Immutable config** (`ScanConfig`): target, severity_threshold, enable_llm, enable_auth_check, baseline_path
2. **Mutable runtime state** (`ScanState`): findings, llm_calls

Why: prevents accidental mutation bugs, keeps config reproducible, enables easier testing + replay.

**Score: SOLID** -- Caught the trap in the roadmap description.

### Q5: Blast radius if config leaks secrets?
**A:**
- Logs (local + CI) expose secrets
- Logfire (external system) stores them
- Anyone with access gets full API misuse capability
- If .env fails to load: LLM calls fail at runtime, logging may silently degrade, scanner behavior becomes inconsistent
- If mutable config corrupts: results bleed across runs, hard to debug state bugs, non-deterministic scans

**Score: SOLID**

---

## Phase 2: Design Interrogation (4/5 SOLID, 1 PARTIAL)

### Q1: Architecture -- Pydantic v2 features for each class?
**A:**
- `ScanConfig`: `BaseModel` with `ConfigDict(frozen=True)` -- enforces immutability, makes config hashable/reproducible
- `ScanState`: `BaseModel` with `Field(default_factory=list)` -- mutable by design
- `Settings`: `BaseSettings` with `SettingsConfigDict(env_file=".env")` -- separate from ScanConfig
- File structure: all three in `src/mcpguard/models/config.py` (scope is small, avoid premature fragmentation)

**Score: SOLID**

### Q2: Data flow -- CLI to ScanConfig lifecycle?
**A:**
1. CLI parses arguments (Typer) -> `{enable_llm: False, severity_threshold: "high", target: "/path/to/config.json"}`
2. Load environment: `settings = Settings()` reads `.env`
3. Construct ScanConfig from CLI args (not from env -- env is for secrets/global config)
4. Override precedence: CLI args > .env > defaults
5. Validate config (severity valid, target exists, baseline path valid or allowed to not exist)
6. Create `ScanState()` fresh for each scan
7. Ownership: ScanConfig -> CLI/orchestrator, ScanState -> Scan engine

**Score: SOLID**

### Q3: Edge cases?
**A:**
1. `.env` missing vs empty -> OK, defaults used, only fail if required key needed later
2. CLI vs env conflict (e.g., `.env: ENABLE_LLM=true`, CLI: `--no-llm`) -> CLI wins, do not map env to ScanConfig directly
3. `baseline_path` doesn't exist (first scan) -> Should NOT fail, treat as empty baseline, create later during write phase

**Score: SOLID**

### Q4: Failure modes?
**A:**
- Invalid severity -> Use `Severity(str, Enum)`, Pydantic auto-validates
- baseline_path is a directory -> `@field_validator` rejects it
- API key with whitespace -> Validator strips with `.strip()`
- Never log raw API keys, never include in exceptions

**Score: PARTIAL** -- Missed `SecretStr` as the Pydantic-specific mechanism. Without `SecretStr`, ValidationError messages dump raw API key values into tracebacks. Need `SecretStr` type which masks in repr, str, and serialization automatically. `.get_secret_value()` required for access.

### Q5: Why Pydantic over dataclasses/dict? Why pydantic-settings?
**A:**
- dict: no validation, no typing, error-prone
- dataclass: no built-in validation, manual parsing
- Pydantic: type validation, field validators, env integration, clear error messages, serialization
- `python-dotenv`: manual loading, no typing, easy to forget
- `pydantic-settings`: native integration, typed env loading, centralized config, cleaner architecture

**Score: SOLID**

---

## Phase 3: Implementation Readiness (5/5 SOLID)

### Q1: Dependencies?
**A:** `pydantic-settings` is NOT in `pyproject.toml` currently. Must add `pydantic-settings>=2.2.0` explicitly. Never rely on transitive deps.

**Score: SOLID**

### Q2: Testing strategy?
**A:** 7 test functions:
- `test_settings_loads_from_env` -- monkeypatch.chdir to tmp_path with .env
- `test_settings_missing_env_file` -- assert all keys None
- `test_settings_strips_whitespace` -- monkeypatch.setenv with trailing newline
- `test_scan_config_is_frozen` -- pytest.raises on mutation
- `test_invalid_severity_raises` -- ValidationError on "critical"
- `test_baseline_path_must_not_be_directory` -- ValidationError
- `test_scan_state_defaults` -- empty findings, 0 llm_calls

Environment isolation via `tmp_path` + `monkeypatch.chdir()` + `monkeypatch.setenv()`.

**Score: SOLID**

### Q3: Integration points?
**A:**
- New: `src/mcpguard/models/config.py`, `tests/test_config.py`
- No changes to `cli.py` (later spec), no changes to `__init__.py` (keep minimal)

**Score: SOLID**

### Q4: Risk assessment?
**A:** Secret leakage via:
1. `logger.info(settings)` -> Pydantic prints `Settings(gemini_api_key='abc123')`
2. `raise ValueError(f"Invalid key: {settings.gemini_api_key}")` -> secret in exception
3. `print(settings.dict())` -> secret in output

Mitigation: `SecretStr` type masks in `.model_dump()`, requires `.get_secret_value()` for access.

**Score: SOLID**

### Q5: Definition of done?
**A:**
- Files: `src/mcpguard/models/config.py`, `tests/test_config.py`, update `pyproject.toml`
- 7 tests all passing
- `make check` green (ruff + mypy + pytest)
- Manual: `print(Settings())` shows no plaintext secrets

**Score: SOLID**

---

## Phase 3.5: Test Cases Gate (PARTIAL)

Wrote 10 tests covering all areas. Tests were comprehensive but used `hasattr` fallbacks for `SecretStr` that would pass even without `SecretStr` -- contradicting the stated design conviction that `SecretStr` is mandatory.

---

## Key Learnings

1. **Pydantic v2 validators require `@classmethod`** -- v1 didn't, v2 does. Easy to miss.
2. **`mode="before"` not `model="before"`** -- typo-prone parameter name.
3. **`SecretStr` is non-negotiable** for API keys -- without it, secrets leak into repr, tracebacks, and serialization.
4. **Split config from state** -- immutable intent (`ScanConfig`) + mutable accumulator (`ScanState`) solves the tension.
5. **Test convictions strictly** -- if you say SecretStr is required, the test should FAIL without it, not gracefully degrade.
6. **Enum member casing matters** -- `Severity.HIGH` (Python convention) vs `Severity.high` (value). Reference the member name, not the value.
