"""Structured console and rotating-file logging setup."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class StructuredFormatter(logging.Formatter):
    """Render stable, searchable key-value log records."""

    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)
        context = getattr(record, "context", {})
        details = " ".join(f"{key}={value!r}" for key, value in sorted(context.items()))
        return f"{base} {details}".rstrip()


def configure_logging(log_directory: Path, level: str) -> logging.Logger:
    """Configure and return the isolated JOCHEN X root logger."""
    logger = logging.getLogger("jochen_x")
    logger.handlers.clear()
    logger.setLevel(level)
    logger.propagate = False
    formatter = StructuredFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    file_handler = RotatingFileHandler(log_directory / "jochen_x.log", maxBytes=2_000_000,
                                       backupCount=5, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger
