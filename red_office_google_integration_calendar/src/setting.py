from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

# directory Path for storing encrypted credentials and token
SECRET_DIRECTORY_PATH = BASE_DIR / 'google_service' / 'secrets'

# Directory path for storing log files
LOG_DIRECTORY_PATH = BASE_DIR / 'log'

# with this scope you can perform all the calendar events opetations
SCOPE = ["https://www.googleapis.com/auth/calendar.events"]
BUILD_TYPE = "calendar"


if __name__ == '__main__':
    # print(type(LOG_DIRECTORY_PATH))
    pass
