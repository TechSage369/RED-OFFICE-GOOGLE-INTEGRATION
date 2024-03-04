import os.path

from log.logger_config import logger
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import settings

'''

service = get_service() 

By calling get_services() will load credentials and build the service
'''
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


# File paths
TOKEN_FILE_PATH = settings.BASE_DIR / 'modules' / 'secrets' / 'token.json'


CREDENTIALS_FILE_PATH = settings.BASE_DIR / \
    'modules' / 'secrets' / 'credentials.json'


def get_service():
    '''
    Get a Google Calendar service object.

    Returns:
        Credentials: The Google Calendar service object.

    Raises:
        Exception: If there is an error loading the credentials.

    '''
    try:
        creds = load_credentials()
        service = build("calendar", "v3", credentials=creds)
        return service

    except Exception as e:
        logger.error(f"Error loading credentials from token.json: {e}")
        raise Exception(e)


def load_credentials():
    '''
    Load Google API credentials from a token file.

    Returns:
        Credentials: The loaded credentials object.

    Raises:
        Exception: If there is an error loading the credentials.
    '''
    creds = None

    if os.path.exists(TOKEN_FILE_PATH):
        try:
            creds = Credentials.from_authorized_user_file(
                TOKEN_FILE_PATH, SCOPES)
        except Exception as e:
            logger.error(f"Error loading credentials from token.json: {e}")
            raise Exception(e)

    if not creds or not creds.valid:
        creds = refresh_or_acquire_new_credentials(creds)

    return creds


def refresh_or_acquire_new_credentials(creds):
    '''
    Refresh expired credentials or acquire new credentials.

    Args:
        creds (Credentials): The current credentials object.

    Returns:
        Credentials: The refreshed or new credentials object.

    Raises:
        Exception: If there is an error refreshing or acquiring new credentials
    '''
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except HttpError as e:
            logger.error({'status_code': e.resp.status, 'message': e.resp})
            raise Exception(e)
    else:
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        except Exception as e:
            logger.error(f"Error running flow: {e}")
            raise Exception(e)

    save_credentials(creds)  # type: ignore
    return creds


def save_credentials(creds) -> None:
    '''
    Save credentials to a token file.

    Args:
        creds (Credentials): The credentials object to save.

    Raises:
        Exception: If there is an error saving the credentials.

    '''

    try:
        with open(TOKEN_FILE_PATH, "w") as token:
            token.write(creds.to_json())

    except Exception as e:
        logger.error(f"Error saving credentials to token.json: {e}")
        raise Exception("Error while saving credential to token.json")


if __name__ == "__main__":
    print(get_service())
