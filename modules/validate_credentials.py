import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError, InvalidJsonError
from googleapiclient.discovery import build, Resource
import settings
from log.logger_config import logger
from typing import Any


SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_FILE_PATH = settings.BASE_DIR / 'modules' / 'secrets' / 'token.json'
CREDENTIALS_FILE_PATH = settings.BASE_DIR / \
    'modules' / 'secrets' / 'credentials.json'


def handle_exception(func):
    '''
    Note: Decorator Function

    it handles Exception for all the methods of GoogleCalendarService class
    '''

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HttpError as e:
            res = {'status': e.resp.status, 'message': 'HttpError'}
            logger.error(res)
            print(res)
            sys.exit(1)
        except InvalidJsonError as e:
            res = {'status': 'InvalidJsonError', 'message': e}
            logger.error(res)
            print(res)
            sys.exit(1)
        except TypeError as e:
            res = {'status': 'TypeError', 'message': e}
            logger.error(res)
            print(res)
            sys.exit(1)
        except (FileNotFoundError, FileExistsError) as e:
            res = {'status': 'Error With File', 'message': e}
            logger.error(res)
            print(res)
            sys.exit(1)
        except Exception as e:
            logger.critical(e)
            print({'status': 'Exception', 'message': e})
            sys.exit(1)
    return wrapper


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

    @handle_exception
    def get_service(self) -> Any:
        creds = self.load_credentials()
        service = build("calendar", "v3", credentials=creds)
        return service

    @handle_exception
    def load_credentials(self):
        creds = None
        if os.path.exists(self.TOKEN_FILE_PATH):
            creds = Credentials.from_authorized_user_file(
                self.TOKEN_FILE_PATH, self.SCOPES)

        if not creds or not creds.valid:
            creds = self.refresh_or_acquire_new_credentials(creds)
        return creds

    @handle_exception
    def refresh_or_acquire_new_credentials(self, creds):
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.CREDENTIALS_FILE_PATH, self.SCOPES)
            creds = flow.run_local_server(port=0)
            self.save_credentials(creds)

        return creds

    @handle_exception
    def save_credentials(self, creds):
        with open(self.TOKEN_FILE_PATH, "w") as token_file:
            token_file.write(creds.to_json())


if __name__ == "__main__":
    service = GoogleCalendarService()
    print(service.get_service())
