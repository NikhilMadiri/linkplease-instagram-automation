"""Centralized standard-library logging configuration."""

import logging

from app.config import get_settings

logger = logging.getLogger("linkplease")


def configure_logging() -> None:
    """Configure consistent process-wide logging once at application startup."""
    logging.basicConfig(
        level=getattr(logging, get_settings().log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
