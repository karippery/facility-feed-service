
import logging
import os


def setup_logging():
    """Set up structured logging for the application."""
    log_format = '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
    logging.basicConfig(
        format=log_format,
        level=logging.INFO,
        handlers=[logging.StreamHandler()]
    )
    logger = logging.getLogger(__name__)

    # Optionally, configure log file handling
    log_file = os.getenv("LOG_FILE", "app.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)
    return logger
