from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_FILE_PATH = BASE_DIR / 'google_service' / 'secrets'

if __name__ == '__main__':
    print(SECRET_FILE_PATH)
