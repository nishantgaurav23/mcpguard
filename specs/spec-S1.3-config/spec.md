# S1.3 -- ScanConfig + Settings

**Phase:** 1 -- Project Foundation
**Location:** `src/mcpguard/models/config.py`
**Depends On:** S1.1
**Status:** pending

---

## Goal

Define a central, typed configuration system: `Settings` loads secrets from `.env` via pydantic-settings, `ScanConfig` is a frozen (immutable) Pydantic model for scan parameters, `ScanState` is a mutable accumulator for runtime results. Secrets are never exposed in logs, repr, or error messages.

---

## Requirements

### R1: Severity Enum

- `Severity(str, Enum)` with values: `low`, `medium`, `high`
- Used as type for `ScanConfig.severity_threshold`

### R2: Settings (BaseSettings)

- Loads from `.env` file via `pydantic-settings`
- Fields: `gemini_api_key`, `groq_api_key`, `logfire_token` (all `SecretStr | None`, default `None`)
- Field: `log_level` (`str`, default `"INFO"`)
- `case_sensitive=False` in SettingsConfigDict
- Validator: strip whitespace/newlines from secret values before wrapping (`mode="before"`)
- Secrets NEVER appear in `repr()`, `str()`, or `model_dump()` output

### R3: ScanConfig (frozen BaseModel)

- `model_config = ConfigDict(frozen=True)` -- immutable after construction
- Fields:
  - `target: Path` -- path to target config or server
  - `severity_threshold: Severity` -- default `Severity.MEDIUM`
  - `enable_llm: bool` -- default `True`
  - `enable_auth_check: bool` -- default `True`
  - `baseline_path: Path | None` -- default `None`
- Validator on `baseline_path`: reject existing directories, allow nonexistent paths (first scan)

### R4: ScanState (mutable BaseModel)

- `findings: list` -- default empty via `Field(default_factory=list)`
- `llm_calls: int` -- default `0`
- Mutable by design (not frozen)

### R5: Dependency

- `pydantic-settings>=2.2.0` must be declared in `pyproject.toml` dependencies

---

## Acceptance Criteria

1. `from mcpguard.models.config import Settings, ScanConfig, ScanState, Severity` works
2. `Settings()` loads from `.env` when present, defaults to `None` when absent
3. `SecretStr` masks values in `repr(settings)` -- no plaintext secrets
4. `ScanConfig` is frozen -- mutation raises error
5. Invalid severity (e.g., `"critical"`) raises `ValidationError`
6. `baseline_path` rejects existing directories, allows nonexistent files
7. `ScanState` defaults to empty findings and 0 llm_calls
8. `ScanState` is mutable
9. `ruff check` and `mypy` pass on config.py

---

## Test Plan

- `test_settings_loads_from_env`
- `test_settings_missing_env_defaults_to_none`
- `test_settings_strips_whitespace`
- `test_settings_does_not_expose_secrets_in_repr`
- `test_settings_log_level_default`
- `test_scan_config_is_frozen`
- `test_invalid_severity_raises`
- `test_baseline_path_rejects_directory`
- `test_baseline_path_allows_nonexistent_file`
- `test_scan_state_defaults`
- `test_scan_state_is_mutable`
- `test_settings_secret_access_method`
- `test_severity_enum_values`
