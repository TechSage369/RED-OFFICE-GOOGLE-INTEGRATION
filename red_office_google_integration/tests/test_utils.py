import unittest
from unittest.mock import patch, MagicMock
from red_office_google_integration.src.utils import handle_exception


class TestHandleException(unittest.TestCase):
    '''

    # TestHandleException
    `This class contains unit tests for the handle_exception decorator function,
    which is designed to be used across various modules to handle exceptions.`

    Test Cases
    test_handle_exception

    - Tests the handle_exception decorator function by:
        - Defining a test function that raises a ValueError.
        - Decorating the test function with handle_exception.
        - Calling the decorated test function.
        - Asserting that the logger.error method was called with the correct arguments.
        - Asserting that sys.exit was called with the correct code.`

    TODO
    - test_handle_exception_for_success: 
        - Test the handle_exception decorator for successful execution.
    - test_handle_exception_for_unknown_exception:
        - Test the handle_exception decorator for an unknown exception.
    - test_handle_exception_for_httperror:
        - Test the handle_exception decorator for an HTTPError.
    - test_handle_exception_for_exception_inside_function:
        - Test the handle_exception decorator for an exception raised inside the decorated function.
    - test_handle_exception_raise:
        - Test the handle_exception decorator for an exception that should be raised.
    '''

    @patch('red_office_google_integration.src.utils.sys.exit')
    @patch('red_office_google_integration.log.log_handler.logger.error')
    def test_handle_exception(self, mock_logger_error, mock_sys_exit):

        # Define a test function that will raise an exception
        @handle_exception
        def test_function_on_value_error():
            raise ValueError("Test Error")
        # Call the test function
        test_function_on_value_error()
        # Check that logger.error was called with the correct arguments
        mock_logger_error.assert_called_once_with({
            'status': 'ValueError',
            'message': 'Test Error',
            'function_name': 'test_function_on_value_error'
        })
        # Check that sys.exit was called with the correct code
        mock_sys_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
