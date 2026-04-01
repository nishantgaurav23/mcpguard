from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    gemini_api_key: SecretStr | None = None
    groq_api_key: SecretStr | None = None
    logfire_token: SecretStr | None = None
    log_level: str = "INFO"

    @field_validator("gemini_api_key", "groq_api_key", "logfire_token", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.strip()


class ScanConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    target: Path
    severity_threshold: Severity = Severity.MEDIUM
    enable_llm: bool = True
    enable_auth_check: bool = True
    baseline_path: Path | None = None

    @field_validator("baseline_path")
    @classmethod
    def validate_baseline_path(cls, v: Path | None) -> Path | None:
        if v is not None and v.exists() and v.is_dir():
            raise ValueError("baseline_path must be a file, not a directory")
        return v


class ScanState(BaseModel):
    findings: list[Any] = Field(default_factory=list)
    llm_calls: int = 0
