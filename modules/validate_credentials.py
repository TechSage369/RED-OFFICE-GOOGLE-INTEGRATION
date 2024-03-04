import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build, Resource
import settings
from log.logger_config import logger
from typing import Any


SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_FILE_PATH = settings.BASE_DIR / 'modules' / 'secrets' / 'token.json'
CREDENTIALS_FILE_PATH = settings.BASE_DIR / \
    'modules' / 'secrets' / 'credentials.json'


class GoogleCalendarService:
    '''
    All the Google Credentials are packed inside this class

    ## Example
    ```
        google_cal_service = GoogleCalendarService()
        service = google_cal_service.get_service()

        Then

        service.events().insert(calendarId=calendarId, body=event_data).execute()
    ```

    '''

    def __init__(self) -> None:
        self.SCOPES = SCOPES
        self.TOKEN_FILE_PATH = TOKEN_FILE_PATH
        self.CREDENTIALS_FILE_PATH = CREDENTIALS_FILE_PATH
        self.logger = logger

    def get_service(self) -> Any:
        try:
            creds = self.load_credentials()
            service = build("calendar", "v3", credentials=creds)
            return service
        except Exception as e:
            self.handle_error('Exception', f'An exception occurred: {e}')

    def load_credentials(self):
        creds = None
        if not os.path.exists(self.TOKEN_FILE_PATH):
            self.handle_error(
                'FileNotFound', f'file ({self.TOKEN_FILE_PATH}) not found')

        try:
            creds = Credentials.from_authorized_user_file(
                self.TOKEN_FILE_PATH, self.SCOPES)
        except Exception as e:
            self.handle_error('CredentialsError',
                              f'Error loading credentials: {e}')

        if not creds or not creds.valid:
            creds = self.refresh_or_acquire_new_credentials(creds)
        return creds

    def refresh_or_acquire_new_credentials(self, creds):
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except HttpError as e:
                self.handle_error(
                    'HttpError', f'HTTP error occurred during refresh: {e}')
            except Exception as e:
                self.handle_error(
                    'RefreshError', f'Error refreshing credentials: {e}')
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_FILE_PATH, self.SCOPES)
                creds = flow.run_local_server(port=0)
                self.save_credentials(creds)
            except Exception as e:
                self.handle_error('FlowError', f'Error running flow: {e}')

        return creds

    def save_credentials(self, creds):
        try:
            with open(self.TOKEN_FILE_PATH, "w") as token_file:
                token_file.write(creds.to_json())
        except Exception as e:
            self.handle_error('SaveCredentialsError',
                              f'Error saving credentials to token.json: {e}')

    def handle_error(self, error_type, error_message):
        print({'status': error_type, 'message': error_message})
        self.logger.error({'status': error_type, 'message': error_message})
        sys.exit(1)


if __name__ == "__main__":
    service = GoogleCalendarService()
    print(service.get_service())
