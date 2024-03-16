import pathlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from red_office_google_integration.google_service.file_handler import (provide_temp_decrypted_file_path,
                                                                       encrypt_and_save_file, FileError)
from red_office_google_integration.src import setting
from red_office_google_integration.src import utils
from typing import Any


class GoogleCredentialService:
    '''
        A class for managing Google Calendar API credentials and interacting with the service.

        Args:
            key (bytes): The encryption key.
            scope (list[str]): The Google API scope.
            token_file_name (str): The name of the file containing the token.
            credential_file_name (str): The name of the file containing the credentials.

        Methods:
            get_service(): Retrieves the Google Calendar service.
            load_credentials(): Loads the Google Calendar API credentials.
            refresh_or_acquire_new_token(): Refreshes or acquires a new Google Calendar API token.
            save_token(): Saves the Google Calendar API token.

        Example:
        ```
        google_cal_service = GoogleCalendarService(key, scope, 'token.json', 'credentials.json')
        service = google_cal_service.get_service()
        service.events().insert(calendarId=calendarId, body=event_data).execute()
        ```

        TODO:
            - Write unit tests.
            - Add more documentation.
            - Optimize the code.
    '''

    def __init__(self, key: bytes, scope: list[str], token_file_name: str, credential_file_name: str) -> None:
        """
            Initializes a new instance of the GoogleCalendarService class.

            Args:
                key (bytes): The encryption key.
                scope (list[str]): The Google API scope.
                token_file_name (str): The name of the file containing the token.
                credential_file_name (str): The name of the file containing the credentials.

            Returns:
                None
        """
        self.key = key
        self.scope = scope
        self.token_file_path = setting.SECRET_DIRECTORY_PATH / token_file_name
        self.credential_file_path = setting.SECRET_DIRECTORY_PATH / credential_file_name

    @utils.handle_exception
    def get_service(self) -> Credentials:
        '''
        NOTE: I couldn't find what datatype it reurns so I set to Any
        Retrieves the Google Calendar service credentials.

        Returns:
            Any: The Google Calendar service credentials. 

        '''
        creds = self.load_credentials()
        return creds

    @utils.handle_exception
    def load_credentials(self):
        '''
            Loads the credentials from the specified token file, decrypting it if necessary, and handles token expiration.

            Returns:
                Credentials: The loaded and decrypted Google OAuth2 credentials.
        NOTE: to pass provide_temp_decrypted_file_path used inner function so we can pass selfs
        '''
        @provide_temp_decrypted_file_path(self.token_file_path, self.key)
        def inner_func(token_path: pathlib.Path | FileError):
            creds = None
            if type(token_path) != FileError:
                creds = Credentials.from_authorized_user_file(
                    token_path, self.scope)
            if not creds or not creds.valid:
                creds = self.refresh_or_acquire_new_token(creds)
            return creds
        return inner_func()

    @utils.handle_exception
    def refresh_or_acquire_new_token(self, creds):
        @provide_temp_decrypted_file_path(self.credential_file_path, self.key)
        def inner_func(file_path, inner_creds):
            if type(file_path) == FileError:
                raise FileError(f"{file_path}")
            if inner_creds and inner_creds.expired and inner_creds.refresh_token:
                inner_creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    file_path, self.scope)
                inner_creds = flow.run_local_server(port=0)
                self.save_token(inner_creds.to_json())
            return inner_creds

        return inner_func(creds)

    @utils.handle_exception
    def save_token(self, creds):
        encrypt_and_save_file(self.token_file_path, creds, self.key)


if __name__ == "__main__":
    pass
