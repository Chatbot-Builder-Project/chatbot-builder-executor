from loguru import logger
import os
import sys

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Remove the default handler
logger.remove()

# Console sink for a shorter summary
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    level=LOG_LEVEL,
    colorize=True,
)

# File sink for a detailed log
logger.add(
    "/app/logs/app.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    format="{time} | {level} | {message}",
    level=LOG_LEVEL,
    serialize=True,
)

__all__ = ["logger"]
