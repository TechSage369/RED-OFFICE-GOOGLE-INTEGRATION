
"""
Module for handling logging functionality.

This module sets up logging configuration using a custom JSONLinesFormatter and a RotatingFileHandler.
It provides a structured way to log messages with timestamps, log levels, messages, module names, and line numbers.

Example Usage:
```
    logger.critical("Critical message")
    logger.error("Error message")
    logger.debug("Debug message")
    logger.warning("Warning message")
    logger.info("Info message")
```
"""
import logging
from logging.handlers import RotatingFileHandler
import json
from red_office_google_integration.src import setting


LOG_FILE = setting.LOG_DIRECTORY_PATH / 'log.jsonl'


class JSONLinesFormatter(logging.Formatter):
    """
    A custom formatter for logging that formats records as JSON lines.

    Usage:
    formatter = JSONLinesFormatter()
    file_handler.setFormatter(formatter)
    """

    def format(self, record):
        """
        Format the log record as a JSON object.

        Args:
            record (LogRecord): The log record to be formatted.

        Returns:
            (str): JSON representation of the log record.
        """
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
