# tests/test_s1_3_config.py


import pytest
from pydantic import ValidationError

# These imports will fail right now (expected RED)
from mcpguard.models.config import ScanConfig, ScanState, Settings, Severity

# ── Settings Tests ─────────────────────────────────────


def test_settings_loads_from_env(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("GEMINI_API_KEY=test_key\n")

    monkeypatch.chdir(tmp_path)

    settings = Settings()
    # Expect SecretStr-like behavior OR plain string depending on implementation
    value = (
        settings.gemini_api_key.get_secret_value()
        if hasattr(settings.gemini_api_key, "get_secret_value")
        else settings.gemini_api_key
    )
    assert value == "test_key"


def test_settings_missing_env_file(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    settings = Settings()

    assert settings.gemini_api_key is None
    assert settings.groq_api_key is None
    assert settings.logfire_token is None


def test_settings_strips_whitespace(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "abc\n")

    settings = Settings()

    value = (
        settings.gemini_api_key.get_secret_value()
        if hasattr(settings.gemini_api_key, "get_secret_value")
        else settings.gemini_api_key
    )
    assert value == "abc"


def test_settings_does_not_expose_secrets_in_repr(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "supersecret")

    settings = Settings()

    representation = repr(settings)

    assert "supersecret" not in representation


def test_settings_log_level_default():
    settings = Settings()
    assert settings.log_level == "INFO"


# ── ScanConfig Tests ───────────────────────────────────


def test_scan_config_is_frozen(tmp_path):
    config = ScanConfig(
        target=tmp_path,
        severity_threshold="high",
        enable_llm=False,
        enable_auth_check=True,
        baseline_path=None,
    )

    with pytest.raises((TypeError, ValidationError)):
        config.severity_threshold = "low"


def test_invalid_severity_raises(tmp_path):
    with pytest.raises(ValidationError):
        ScanConfig(
            target=tmp_path,
            severity_threshold="critical",
            enable_llm=False,
            enable_auth_check=True,
            baseline_path=None,
        )


def test_baseline_path_rejects_directory(tmp_path):
    with pytest.raises(ValidationError):
        ScanConfig(
            target=tmp_path,
            severity_threshold=Severity.HIGH,
            enable_llm=False,
            enable_auth_check=True,
            baseline_path=tmp_path,
        )


def test_baseline_path_allows_nonexistent_file(tmp_path):
    path = tmp_path / "baseline.json"

    config = ScanConfig(
        target=tmp_path,
        severity_threshold=Severity.HIGH,
        enable_llm=False,
        enable_auth_check=True,
        baseline_path=path,
    )
    assert config.baseline_path == path


# ── ScanState Tests ────────────────────────────────────


def test_scan_state_defaults():
    state = ScanState()

    assert state.findings == []
    assert state.llm_calls == 0


def test_scan_state_is_mutable():
    state = ScanState()

    state.findings.append("issue")
    state.llm_calls += 1

    assert state.findings == ["issue"]
    assert state.llm_calls == 1


# ── Security / Secret Handling Tests ───────────────────


def test_settings_secret_access_method(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "supersecret")

    settings = Settings()

    if hasattr(settings.gemini_api_key, "get_secret_value"):
        assert settings.gemini_api_key.get_secret_value() == "supersecret"
    else:
        # fallback if not using SecretStr (test will still pass but flags weaker security)
        assert settings.gemini_api_key == "supersecret"


# ── Severity Enum Tests ────────────────────────────────


def test_severity_enum_values():
    values = {s.value for s in Severity}

    assert values == {"low", "medium", "high"}
