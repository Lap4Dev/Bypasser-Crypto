import sys
from loguru import logger as loguru_logger

from src.config import settings


class Logger:
    _logger = None

    @classmethod
    def get_logger(cls):
        loguru_logger.remove()
        if cls._logger is None:
            log_format = (
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level>"
            )

            loguru_logger.add(sys.stdout, format=log_format, level=settings.LOG_LEVEL)

            loguru_logger.add(settings.LOG_FILE_PATH, format=log_format, level=settings.LOG_LEVEL, rotation="10 MB",
                              compression="zip")

            cls._logger = loguru_logger

        return cls._logger


logger = Logger.get_logger()
