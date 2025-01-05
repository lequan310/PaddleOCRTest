import os
import logging
import sys
from logging import config
from pathlib import Path
from rich.logging import RichHandler
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.absolute()
LOGS_DIR = Path(BASE_DIR, "logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def select_info_only(record: logging.LogRecord) -> bool:
    return record.levelno == logging.INFO


def get_logger(name: str | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if len(logger.handlers):
        logger.handlers[0] = RichHandler(markup=True)
    else:
        logger.addHandler(RichHandler(markup=True))
    return logger


logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "minimal": {"format": "%(message)s"},
        "detailed": {
            "format": "%(levelname)s %(asctime)s [%(name)s:%(filename)s:%(funcName)s:%(lineno)d]\n%(message)s\n"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "minimal",
            "level": logging.DEBUG,
        },
        # Timed Rotating File Handlers for weekly log rotation. Use RotatingFileHandler for size based rotation.
        "info": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": Path(LOGS_DIR, "info.log"),
            "formatter": "detailed",
            "level": logging.INFO,
            "when": "W0",  # Rotate weekly on Monday
            "interval": 1,  # Rotate every week
            "backupCount": 4,
            "filters": [select_info_only],
        },
        "error": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": Path(LOGS_DIR, "error.log"),
            "formatter": "detailed",
            "level": logging.ERROR,
            "when": "W0",  # Rotate weekly on Monday
            "interval": 1,  # Rotate every week
            "backupCount": 4,
        },
    },
    "loggers": {
        "core.ocr": {
            "handlers": ["console", "info", "error"],
            "level": logging.DEBUG,
            "propagate": False,
        },
        "api.routes.ocr": {
            "handlers": ["console", "info", "error"],
            "level": logging.DEBUG,
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["info", "error"],
        "level": logging.DEBUG,
    },
}

config.dictConfig(logging_config)
