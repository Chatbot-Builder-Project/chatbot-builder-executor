import sentry_sdk
from loguru import logger
import os
import sys

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_LOG_LEVEL = os.getenv("SENTRY_LOG_LEVEL", "ERROR")
SENTRY_ENVIRONMENT = os.getenv("SENTRY_ENVIRONMENT", "development")

# Initialize Sentry
sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0,
    _experiments={
        "continuous_profiling_auto_start": True,
    },
    environment=SENTRY_ENVIRONMENT
)

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

# Sentry sink
if SENTRY_ENVIRONMENT != "development":
    def sentry_sink(message):
        if message.record["level"].name in (SENTRY_LOG_LEVEL, "CRITICAL"):
            sentry_sdk.capture_message(message)


    logger.add(sentry_sink, level=SENTRY_LOG_LEVEL)

__all__ = ["logger"]
