"""Tests for S1.1 -- Dependency Declaration."""

from __future__ import annotations

import importlib
import pathlib
import subprocess
import sys

import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PYPROJECT = ROOT / "pyproject.toml"
ENV_EXAMPLE = ROOT / ".env.example"


def _load_pyproject() -> dict:
    with open(PYPROJECT, "rb") as f:
        return tomllib.load(f)


class TestPyprojectStructure:
    """Validate pyproject.toml has all required sections."""

    def test_build_system(self) -> None:
        data = _load_pyproject()
        bs = data["build-system"]
        assert "hatchling" in bs["requires"]
        assert bs["build-backend"] == "hatchling.build"

    def test_project_metadata(self) -> None:
        data = _load_pyproject()
        proj = data["project"]
        assert proj["name"] == "mcpguard"
        assert "version" in proj
        assert proj["requires-python"] == ">=3.10"
        assert proj["license"] == {"text": "MIT"}
        assert proj["readme"] == "README.md"

    def test_classifiers_present(self) -> None:
        data = _load_pyproject()
        classifiers = data["project"].get("classifiers", [])
        assert any("Python :: 3.10" in c for c in classifiers)
        assert any("MIT" in c for c in classifiers)

    def test_runtime_dependencies(self) -> None:
        data = _load_pyproject()
        deps = data["project"]["dependencies"]
        dep_names = [d.split(">")[0].split("[")[0].lower() for d in deps]
        required = ["pydantic-ai", "typer", "rich", "httpx", "logfire", "python-dotenv"]
        for req in required:
            assert req in dep_names, f"Missing runtime dep: {req}"

    def test_dev_dependencies(self) -> None:
        data = _load_pyproject()
        dev_deps = data["project"]["optional-dependencies"]["dev"]
        dep_names = [d.split(">")[0].split("[")[0].lower() for d in dev_deps]
        required = ["pytest", "pytest-asyncio", "pytest-cov", "ruff", "mypy"]
        for req in required:
            assert req in dep_names, f"Missing dev dep: {req}"

    def test_entry_point(self) -> None:
        data = _load_pyproject()
        scripts = data["project"]["scripts"]
        assert scripts["mcpguard"] == "mcpguard.cli:app"

    def test_hatch_src_layout(self) -> None:
        data = _load_pyproject()
        packages = data["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"]
        assert "src/mcpguard" in packages


class TestToolConfig:
    """Validate tool configuration sections."""

    def test_ruff_config(self) -> None:
        data = _load_pyproject()
        ruff = data["tool"]["ruff"]
        assert ruff["line-length"] == 100
        assert ruff["target-version"] == "py310"
        assert "E" in ruff["lint"]["select"]
        assert "F" in ruff["lint"]["select"]

    def test_mypy_config(self) -> None:
        data = _load_pyproject()
        mypy = data["tool"]["mypy"]
        assert mypy["python_version"] == "3.10"
        assert mypy["strict"] is True

    def test_pytest_config(self) -> None:
        data = _load_pyproject()
        pytest_cfg = data["tool"]["pytest"]["ini_options"]
        assert "cov" in pytest_cfg["addopts"]
        assert pytest_cfg["asyncio_mode"] == "auto"
        assert "tests" in pytest_cfg["testpaths"]


class TestVersionConsistency:
    """Version in pyproject.toml must match __init__.py."""

    def test_version_match(self) -> None:
        data = _load_pyproject()
        toml_version = data["project"]["version"]
        mcpguard = importlib.import_module("mcpguard")
        assert mcpguard.__version__ == toml_version


class TestEnvExample:
    """Validate .env.example contains required keys."""

    def test_env_example_exists(self) -> None:
        assert ENV_EXAMPLE.exists()

    def test_required_keys(self) -> None:
        content = ENV_EXAMPLE.read_text()
        required_keys = ["GEMINI_API_KEY", "GROQ_API_KEY", "LOGFIRE_TOKEN", "LOG_LEVEL"]
        for key in required_keys:
            assert key in content, f"Missing env var: {key}"


class TestEntryPoint:
    """Verify the CLI entry point works."""

    def test_mcpguard_importable(self) -> None:
        import mcpguard

        assert hasattr(mcpguard, "__version__")

    def test_cli_app_importable(self) -> None:
        from mcpguard.cli import app

        assert app is not None

    def test_mcpguard_help(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "mcpguard", "--help"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        # Typer may return 0 for --help
        assert result.returncode == 0 or "Usage" in result.stdout or "MCPGuard" in result.stdout
