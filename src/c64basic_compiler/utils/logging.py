import sys

from loguru import logger

LOGGER_FORMAT = "<green>{name}</green>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
LOGGER_LEVEL = "INFO"

logger.remove()


def configure_logger(
    level: str | None = None,
    format: str | None = None,
    colorize: bool | None = True,
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
