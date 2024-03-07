import sys
from googleapiclient.errors import HttpError, InvalidJsonError
from red_office_google_integration_calendar.log.log_handler import logger


def handle_exception(func):
    """
    A decorator that handles exceptions raised by the decorated function.
    Logs the exception and exits the program with an error code.

    :param func: The decorated function.
    :return: The wrapper function.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HttpError as e:
            error_message = f'HttpError: {e}'
        except InvalidJsonError as e:
            error_message = f'InvalidJsonError: {e}'
        except TypeError as e:
            error_message = f'TypeError: {e}'
        except (FileNotFoundError, FileExistsError) as e:
            error_message = f'Error With File: {e}'
        except Exception as e:
            error_message = f'Exception: {e}'
            logger.critical(error_message)
            sys.exit(1)

        res = {
            'status': 'Error',
            'function_name': func.__name__,
            'message': error_message
        }
        logger.error(res)
        print(res)
        sys.exit(1)

    return wrapper


if __name__ == '__main__':
    pass
