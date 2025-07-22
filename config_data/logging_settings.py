import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config_data.initial_settings import PathParams, LogParams


def configure_logger(module_name: str, logfile: Path = PathParams.bot_logfile):
    logger = logging.getLogger(module_name)
    logger.setLevel(LogParams.loglevel)

    handler = RotatingFileHandler(
        filename=logfile,
        mode=LogParams.log_file_mode,
        maxBytes=LogParams.log_max_size * 1024 * 1024,
        backupCount=LogParams.backup_count,
        encoding=LogParams.logs_encoding,
    )

    formatter = logging.Formatter("%(name)s:%(lineno)d %(asctime)s %(levelname)s %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info(
        f"Configure:  module {module_name} logger update conf with write to {logfile}")

    return logger
