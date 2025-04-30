import sys

from loguru import logger
from typing import Optional

LOGGER_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
LOGGER_LEVEL = "INFO"

logger.remove()


def configure_logger(
    level: Optional[str] = None,
    format: Optional[str] = None,
    colorize: Optional[bool] = True,
):
    """Configure logger.

    Args:
        level (Optional[str]): Log level (default from settings).
        format (Optional[str]): Log format (default from settings).
        colorize (Optional[bool]): Colorize logger (default True).
    """
    logger.remove()
    logger.add(
        sink=sys.stderr,
        level=level or LOGGER_LEVEL,
        format=format or LOGGER_FORMAT,
        colorize=colorize,
    )


# # Configure logger with the default settings
# configure_logger()
