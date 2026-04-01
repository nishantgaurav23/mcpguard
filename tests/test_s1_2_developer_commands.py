"""Tests for S1.2 -- Developer Commands (Makefile)."""

from __future__ import annotations

import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAKEFILE = ROOT / "Makefile"


def _read_makefile() -> str:
    return MAKEFILE.read_text()


class TestMakefileStructure:
    """Validate Makefile exists and has correct structure."""

    def test_makefile_exists(self) -> None:
        assert MAKEFILE.exists()

    def test_phony_targets(self) -> None:
        content = _read_makefile()
        phony_line = ""
        for line in content.splitlines():
            if line.startswith(".PHONY:"):
                phony_line += line
        required = [
            "venv",
            "install",
            "install-dev",
            "lint",
            "typecheck",
            "format",
            "test",
            "check",
            "eval",
            "serve",
            "scan",
            "clean",
        ]
        for target in required:
            assert target in phony_line, f"Missing .PHONY target: {target}"

    def test_required_targets(self) -> None:
        content = _read_makefile()
        required = [
            "venv",
            "install",
            "install-dev",
            "lint",
            "typecheck",
            "format",
            "test",
            "check",
            "eval",
            "serve",
            "scan",
            "clean",
        ]
        for target in required:
            pattern = rf"^{re.escape(target)}:"
            assert re.search(pattern, content, re.MULTILINE), f"Missing target: {target}"

    def test_check_depends_on_lint_typecheck_test(self) -> None:
        content = _read_makefile()
        match = re.search(r"^check:(.+)$", content, re.MULTILINE)
        assert match is not None, "check target not found"
        deps = match.group(1)
        assert "lint" in deps
        assert "typecheck" in deps
        assert "test" in deps


class TestMakeTargetsRun:
    """Validate that key make targets execute successfully.

    These tests call the underlying tools directly (not via make)
    to avoid recursive make invocations and venv re-creation overhead.
    """

    def test_ruff_check_runs(self) -> None:
        """Validates the same command that `make lint` runs."""
        result = subprocess.run(
            [str(ROOT / ".venv" / "bin" / "ruff"), "check", "src/", "tests/"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"ruff check failed:\n{result.stdout}"

    def test_ruff_format_check_runs(self) -> None:
        """Validates the format check that `make lint` runs."""
        result = subprocess.run(
            [str(ROOT / ".venv" / "bin" / "ruff"), "format", "--check", "src/", "tests/"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"ruff format check failed:\n{result.stdout}"

    def test_mypy_runs(self) -> None:
        """Validates the same command that `make typecheck` runs."""
        result = subprocess.run(
            [str(ROOT / ".venv" / "bin" / "mypy"), "src/mcpguard/"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert result.returncode == 0, f"mypy failed:\n{result.stdout}"


class TestPlaceholderTargets:
    """Placeholder targets print informative messages."""

    def test_eval_placeholder(self) -> None:
        result = subprocess.run(
            ["make", "--no-print-directory", "eval"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert "not implemented" in result.stdout.lower() or "S10" in result.stdout

    def test_serve_placeholder(self) -> None:
        result = subprocess.run(
            ["make", "--no-print-directory", "serve"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert "not implemented" in result.stdout.lower() or "S9" in result.stdout

    def test_scan_placeholder(self) -> None:
        result = subprocess.run(
            ["make", "--no-print-directory", "scan"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert "not implemented" in result.stdout.lower() or "S4" in result.stdout
