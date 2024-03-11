import logging
from logging.handlers import RotatingFileHandler
import json
from red_office_google_integration_calendar.src import setting


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

LOG_FILE = setting.LOG_DIRECTORY_PATH / 'log.jsonl'


class JSONLinesFormatter(logging.Formatter):
    """
    A custom formatter for logging that formats records as JSON lines.

    Usage:
    formatter = JSONLinesFormatter()
    file_handler.setFormatter(formatter)
    """

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


# Create a RotatingFileHandler with max size 1 MB
file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=1*1024*1024, backupCount=10)
file_handler.setLevel(logging.DEBUG)

# Set the formatter
formatter = JSONLinesFormatter()
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


if __name__ == '__main__':
    # Example usage
    logger.critical(f"Test")
    logger.error("Test")
    logger.debug("Test")
    logger.warning("Test")
    logger.info("Test")
