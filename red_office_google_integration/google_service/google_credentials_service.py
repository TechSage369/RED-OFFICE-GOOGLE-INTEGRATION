import os
import pathlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build
from red_office_google_integration.google_service.file_handler import (provide_temp_decrypted_file_path,
                                                                       encrypt_and_save_file, FileError)
from red_office_google_integration.src import setting
from red_office_google_integration.src import utils
from typing import Any


class GoogleCalendarService:
    '''
    All the Google Credentials are packed inside this class

    ## Example
    ```
        google_cal_service = GoogleCalendarService(key)
        service = google_cal_service.get_service()

        Then

        service.events().insert(calendarId=calendarId, body=event_data).execute()
    ```
        TODO:
            - write unittest
            - more docs
            - optimization
        NOTE:
            - return type of ger_service is set to Any, Didn't find its return
                type of build, try to figure out
    '''

    def __init__(self, key: bytes) -> None:
        self.key = key
        self.scope = setting.SCOPE
        self.token_file_path = setting.SECRET_DIRECTORY_PATH / 'token.enc'
        self.credential_file_path = setting.SECRET_DIRECTORY_PATH / 'credentials.enc'
        self.build_type = setting.BUILD_TYPE

    @utils.handle_exception
    def get_service(self) -> Any:
        creds = self.load_credentials()
        service = build("calendar", "v3", credentials=creds)
        return service

    @utils.handle_exception
    def load_credentials(self):
        '''
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
                raise FileError(file_path)
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
