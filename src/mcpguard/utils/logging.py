from __future__ import annotations

import logging

# Module-level flag to track if setup  has been called
_configured: bool = False


def setup_logging(log_level: str, logfire_token: str | None) -> None:
    """Configure logging system with Logfire support."""
    global _configured
    if _configured:
        return

    # 2. Resolve log level safely
    level = getattr(logging, log_level.upper(), logging.INFO)

    # 3. Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # 4. Avoid duplicates handlers (extra safety beyond _configured)
    if not root_logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        root_logger.addHandler(console_handler)

    # 4. Optional Logfire setup (graceful failure)
    if logfire_token:
        try:
            import logfire  # type : ignore

            try:
                logfire.configure(token=logfire_token)
            except Exception as e:
                root_logger.debug(f"Failed to configure Logfire: {e}")
        except ImportError:
            root_logger.debug("Logfire not installed, using console logging.")

    # 5. Mark as configured
    _configured = True


def get_logger(name: str | None = None) -> logging.Logger:
    """Get a logger with the given name."""
    return logging.getLogger(name)
