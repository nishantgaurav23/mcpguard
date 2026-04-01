import subprocess
import sys


def test_main_import_has_no_side_effects():
    """Import mcpguard.__main__ without triggering CLI execution or SystemExit."""
    import mcpguard.__main__  # should not raise or execute CLI

    assert hasattr(mcpguard.__main__, "app")


def test_python_module_execution_runs_cli():
    """Verify `python -m mcpguard` runs the CLI app correctly."""
    result = subprocess.run(
        [sys.executable, "-m", "mcpguard", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0 or "Usage" in result.stdout or "MCPGuard" in result.stdout


def test_main_delegates_to_cli_app():
    """Verify __main__.py delegates cleanly to cli.app."""
    import mcpguard.__main__
    from mcpguard.cli import app

    assert mcpguard.__main__.app is app
