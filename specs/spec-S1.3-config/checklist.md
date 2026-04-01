# S1.3 -- ScanConfig + Settings Checklist

## Implementation

- [x] pyproject.toml: pydantic-settings>=2.2.0 in dependencies
- [x] src/mcpguard/models/__init__.py exists (package init)
- [x] Severity enum (low, medium, high)
- [x] Settings: BaseSettings with SettingsConfigDict(env_file, case_sensitive)
- [x] Settings: SecretStr for all API keys
- [x] Settings: strip_whitespace validator (mode="before", @classmethod)
- [x] Settings: log_level with default "INFO"
- [x] ScanConfig: frozen=True via ConfigDict
- [x] ScanConfig: target, severity_threshold, enable_llm, enable_auth_check, baseline_path
- [x] ScanConfig: severity_threshold defaults to Severity.MEDIUM
- [x] ScanConfig: baseline_path validator (reject dirs, allow nonexistent)
- [x] ScanState: findings with default_factory, llm_calls default 0
- [x] No unused imports

## Testing

- [x] test_settings_loads_from_env
- [x] test_settings_missing_env_file
- [x] test_settings_strips_whitespace
- [x] test_settings_does_not_expose_secrets_in_repr
- [x] test_settings_log_level_default
- [x] test_scan_config_is_frozen
- [x] test_invalid_severity_raises
- [x] test_baseline_path_rejects_directory
- [x] test_baseline_path_allows_nonexistent_file
- [x] test_scan_state_defaults
- [x] test_scan_state_is_mutable
- [x] test_settings_secret_access_method
- [x] test_severity_enum_values

## Verification

- [x] All 13 tests pass
- [x] ruff check clean
- [x] mypy clean (strict)
- [x] config.py 100% coverage
- [x] No secrets in repr/logs
- [x] Checklist complete
