import sys
from googleapiclient.errors import HttpError
from red_office_google_integration.log.log_handler import logger
import json
from typing import Callable, Any
'''
NOTE: change exception handler documentation
'''


def handle_exception(func: Callable[..., Any]):
    '''
    Decorator function for exception handling.

    This decorator function is used for exception handling in various modules of the project.
    It catches specific exceptions, logs them using the project's logger, prints the error message (in dict format),
    and exits the program with a status code of 1.

    Parameters:
        func (function): The function to be decorated.

    Returns:
        wrapper (function): The wrapped function with exception handling logic.

    Exceptions Handled:
        - HttpError: Handles Google API HTTP errors, extracting relevant information such as status code and message.
        - InvalidJsonError, TypeError, FileNotFoundError, FileExistsError, InvalidToken: Handles specific errors with custom error messages.
        - Exception: Handles all other exceptions with a generic error message.

    Logging:
        Logs the error message using the project's logger with the following format:
            {
                'status': <Exception Type>,
                'status_code': <HTTP Status Code if applicable>,
                'message': <Exception Message>,
                'function_name': <Name of the Function where the Exception Occurred>
            }

    Usage:
    ```
    @handle_exception
    def my_function():
        # Function code that may raise exceptions
        pass
    ```
    '''
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HttpError as e:
            error_message = {
                'status': type(e).__name__,
                'status_code': e.resp.status,
                'message': e._get_reason(),
                'function_name': func.__name__
            }
        # except (InvalidJsonError, TypeError, FileNotFoundError, FileExistsError, InvalidToken) as e:
        #     error_message = {
        #         'status': type(e).__name__,
        #         'message': str(e),
        #         'function_name': func.__name__
        #     }
        except Exception as e:
            error_message = {
                'status': type(e).__name__,
                'message': str(e),
                'function_name': func.__name__
            }

        logger.error(error_message)
        print(json.dumps(error_message))
        sys.exit(1)

    return wrapper


if __name__ == '__main__':
    @handle_exception
    def test():
        raise FileNotFoundError('blah blah')

    test()
