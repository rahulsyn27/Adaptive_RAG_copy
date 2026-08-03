"""
Logger configuration for the application.
"""

import logging

from src.core.config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

__all__ = ["logger"]