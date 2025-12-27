"""
Logging setup for the scraper
"""

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only add handlers if logger doesn't have any
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        # Format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
