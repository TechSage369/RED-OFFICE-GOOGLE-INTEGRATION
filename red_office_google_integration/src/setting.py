'''
    Contains Settings for this project
'''
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


# default Credential filename
DEFAULT_CREDENTIAL_FILE_NAME = 'credential.enc'

# directory Path for storing encrypted credentials and token
SECRET_DIRECTORY_PATH = BASE_DIR / 'google_service' / 'secrets'

# Directory path for storing log files
LOG_DIRECTORY_PATH = BASE_DIR / 'log'


# Settings for Calander Events
# with this scope you can perform all the calendar events opetations
SCOPE_CALENDAR = ["https://www.googleapis.com/auth/calendar.events"]
FILE_NAME_CALENDAR_TOKEN = 'calendar_token.enc'
FILE_NAME_CALENDAR_CREDENTIAL = DEFAULT_CREDENTIAL_FILE_NAME


# Sheets Setting
SCOPE_SPREADSHEETS = ["https://www.googleapis.com/auth/spreadsheets"]
FILE_NAME_SPREADSHEETS_TOKEN = 'spreadsheet_token.enc'
FILE_NAME_SPREADSHEETS_CREDENTIAL = DEFAULT_CREDENTIAL_FILE_NAME


if __name__ == '__main__':
    # print(type(LOG_DIRECTORY_PATH))
    pass
