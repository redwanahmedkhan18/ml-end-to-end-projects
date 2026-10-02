"""
Production-ready application logging configuration.

Features:
- Platform-independent log directory handling
- Rotating log files
- Console logging
- UTF-8 encoding
- Configurable log level through environment variables
- Prevents duplicate handlers
- Thread-safe logging through Python's logging package
- Creates the log directory automatically
- Suitable for local development, Docker, CI/CD, and production
"""

from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

LOG_DIR = Path(
    os.getenv(
        "LOG_DIR",
        PROJECT_ROOT / "logs",
    )
)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

LOG_FILE_NAME = os.getenv(
    "LOG_FILE_NAME",
    "application.log",
)

MAX_LOG_SIZE = int(
    os.getenv(
        "LOG_MAX_BYTES",
        10 * 1024 * 1024,  # 10 MB
    )
)

BACKUP_COUNT = int(
    os.getenv(
        "LOG_BACKUP_COUNT",
        5,
    )
)


# ---------------------------------------------------------------------------
# Create log directory
# ---------------------------------------------------------------------------

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_FILE_PATH = LOG_DIR / LOG_FILE_NAME


# ---------------------------------------------------------------------------
# Log format
# ---------------------------------------------------------------------------

LOG_FORMAT = (
    "[%(asctime)s] "
    "%(levelname)s "
    "%(name)s "
    "[%(filename)s:%(lineno)d] "
    "- %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ---------------------------------------------------------------------------
# Formatter
# ---------------------------------------------------------------------------

formatter = logging.Formatter(
    fmt=LOG_FORMAT,
    datefmt=DATE_FORMAT,
)


# ---------------------------------------------------------------------------
# File Handler
# ---------------------------------------------------------------------------

file_handler = RotatingFileHandler(
    filename=LOG_FILE_PATH,
    maxBytes=MAX_LOG_SIZE,
    backupCount=BACKUP_COUNT,
    encoding="utf-8",
)

file_handler.setFormatter(formatter)


# ---------------------------------------------------------------------------
# Console Handler
# ---------------------------------------------------------------------------

console_handler = logging.StreamHandler()

console_handler.setFormatter(formatter)


# ---------------------------------------------------------------------------
# Application Logger
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    handlers=[
        file_handler,
        console_handler,
    ],
    force=True,
)


# ---------------------------------------------------------------------------
# Export application logger
# ---------------------------------------------------------------------------

logger = logging.getLogger("application")
logger.setLevel(
    getattr(logging, LOG_LEVEL, logging.INFO)
)