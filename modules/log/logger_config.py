import logging
from logging.handlers import RotatingFileHandler
import json
from pathlib import Path

'''
NOTE:
    - Didn't work `from ..config import BASE_DIR`
'''

'''
    # Logger configuration file

    Import this file and use logger

    Example:

    ```
    form this_file import logger

    logger.critical(f"Test")
    logger.error("Test")
    logger.debug("Test")
    logger.warning("Test")
    logger.info("Test")

    ```
'''

LOG_FILE_PATH = Path(__file__).resolve().parent / 'log.jsonl'


class JSONLinesFormatter(logging.Formatter):
    def format(self, record):
        message = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'line': record.lineno
        }
        return json.dumps(message)


# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Create a RotatingFileHandler with max size 5 MB
file_handler = RotatingFileHandler(
    LOG_FILE_PATH, maxBytes=1*1024*1024, backupCount=1)
file_handler.setLevel(logging.DEBUG)

# Set the formatter
formatter = JSONLinesFormatter()
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


if __name__ == '__main__':
    logger.critical(f"Test")
    logger.error("Test")
    logger.debug("Test")
    logger.warning("Test")
    logger.info("Test")
