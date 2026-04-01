"""Module entry point for `python -m mcpguard` execution."""

from mcpguard.cli import app

# Guard: only execute when run as `python -m mcpguard`, not on import
if __name__ == "__main__":
    app()
