import logging
import sys

# NOTE:
# We import inside tests (not at top) so that monkeypatching sys.modules works properly


def _reset_logging():
    """Helper to reset global logging state between tests."""
    root = logging.getLogger()
    for handler in list(root.handlers):
        root.removeHandler(handler)
    root.setLevel(logging.NOTSET)
    # Reset module-level _configured flag so setup_logging runs again
    import mcpguard.utils.logging as _log_mod

    _log_mod._configured = False


# ── Core Behavior ─────────────────────────────────────


def test_setup_logging_sets_log_level(monkeypatch):
    _reset_logging()

    from mcpguard.utils.logging import setup_logging

    setup_logging("DEBUG", None)

    assert logging.getLogger().level == logging.DEBUG


def test_setup_logging_invalid_level_defaults_to_info(monkeypatch):
    _reset_logging()

    from mcpguard.utils.logging import setup_logging

    setup_logging("VERBOSE", None)

    assert logging.getLogger().level == logging.INFO


# ── Idempotency ───────────────────────────────────────


def test_setup_logging_idempotent(monkeypatch):
    _reset_logging()

    from mcpguard.utils.logging import setup_logging

    setup_logging("INFO", None)
    handlers_before = len(logging.getLogger().handlers)

    setup_logging("INFO", None)
    handlers_after = len(logging.getLogger().handlers)

    assert handlers_before == handlers_after


# ── Logfire Fallback: Import Failure ──────────────────


def test_setup_logging_logfire_import_failure(monkeypatch):
    _reset_logging()

    # Simulate logfire not installed
    monkeypatch.setitem(sys.modules, "logfire", None)

    from mcpguard.utils.logging import setup_logging

    # Should not raise
    setup_logging("INFO", "fake-token")

    logger = logging.getLogger(__name__)
    logger.info("test message")  # should work without crashing


# ── Logfire Fallback: configure() Failure ─────────────


def test_setup_logging_logfire_config_failure(monkeypatch):
    _reset_logging()

    class FakeLogfire:
        @staticmethod
        def configure(*args, **kwargs):
            raise RuntimeError("Logfire failure")

    monkeypatch.setitem(sys.modules, "logfire", FakeLogfire)

    from mcpguard.utils.logging import setup_logging

    # Should not raise even if configure fails
    setup_logging("INFO", "fake-token")

    logger = logging.getLogger(__name__)
    logger.info("test message")  # still works


# ── Logger Access ─────────────────────────────────────


def test_get_logger_returns_logger(monkeypatch):
    _reset_logging()

    from mcpguard.utils.logging import get_logger, setup_logging

    setup_logging("INFO", None)

    logger = get_logger(__name__)

    assert isinstance(logger, logging.Logger)


# ── Global State Isolation Check ──────────────────────


def test_logging_does_not_duplicate_handlers_across_tests(monkeypatch):
    _reset_logging()

    from mcpguard.utils.logging import setup_logging

    setup_logging("INFO", None)
    count_1 = len(logging.getLogger().handlers)

    _reset_logging()

    setup_logging("INFO", None)
    count_2 = len(logging.getLogger().handlers)

    assert count_1 == count_2
