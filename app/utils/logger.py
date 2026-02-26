"""
Logger module — structured logging for the application.
"""

import logging
import sys
from typing import Optional

from app.config import settings


def get_logger(name: str = "flowbot", level: Optional[str] = None) -> logging.Logger:
    """
    Create and configure a logger instance.
    """
    if level is None:
        level = settings.LOG_LEVEL

    logger = logging.getLogger(name)
    logger.setLevel(level.upper())

    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger

    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level.upper())

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger


# Default logger
logger = get_logger()
