from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

# File Path for storing encrypted credentials and token
SECRET_FILE_PATH = BASE_DIR / 'google_service' / 'secrets'

#
LOG_FILE_PATH = BASE_DIR / 'log'

SCOPE = ["https://www.googleapis.com/auth/calendar"]
BUILD_TYPE = "calendar"


if __name__ == '__main__':
    print(SECRET_FILE_PATH)
