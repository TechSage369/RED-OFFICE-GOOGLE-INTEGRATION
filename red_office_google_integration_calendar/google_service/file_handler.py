from cryptography.fernet import Fernet, InvalidToken
import tempfile
import os
import pathlib
from typing import Any, Callable
from red_office_google_integration_calendar.src import setting
'''
This module contains functions for encrypting and decrypting files, as well as a decorator function
to create a temporary file that holds decrypted data and injects it into a function.
This is especially useful for Google credentials, which require a file path and cannot use an encrypted file path.

Functions:
    - decrypt_file
    - provide_temp_decrypted_file_path
    - generate_key
    - encrypt_and_save_file
NOTE:
    when token is invalid or filenot exist we have to generate new one but when credentials dosen't exit or
    invalid throw error. so my function right now is not well structured
TODO:
    Write unit tests
    
    OPTIONAL
        - encrypt_data
'''


def decrypt_file(path: pathlib.Path, key: bytes) -> bytes:
    """
    Decrypts the data from the specified file path using the provided key.

        - param path: The path to the encrypted file.
        - param key: The encryption/decryption key.
        - return: The decrypted data.
    """
    try:
        cipher = Fernet(key)
        with open(path, 'rb') as f:
            data = f.read()
        decrypted_data = cipher.decrypt(data)
        return decrypted_data
    except InvalidToken:
        raise InvalidToken("Invalid key or corrupted file")
    except Exception as e:
        raise Exception(f"Something went wrong while decryption: {e}")


def provide_temp_decrypted_file_path(encrypted_file_path: pathlib.Path, key: bytes) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator function that decrypts the data from the specified file path using the provided key,
    stores the decrypted data in a temporary file, and injects the temporary file path to the decorated function.
    The temporary file is deleted after the decorated function is executed.

        - param encrypted_file_path: The path to the encrypted file.
        - param key: The encryption/decryption key.
        - return: The wrapper function.

    ### Example:
    ```
    @provide_temp_decrypted_file_path(encrypted_filepath, key)
    def func(file_path: pathlib.Path):
        # your statement here
    ```
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        The actual decorator that injects the temporary file path to the decorated function.

        :param func: The function to be decorated.
        :return: The wrapper function.
        """
        def wrapper(*args, **kwargs):
            # Create a temporary file to store the decrypted data
            temp_decrypted_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file_path = None
            cipher = Fernet(key)
            try:
                with open(encrypted_file_path, 'rb') as f:
                    data = f.read()
                    decrypted_data = cipher.decrypt(data)

                # Write the decrypted data to the temporary file
                temp_decrypted_file.write(decrypted_data)
                temp_decrypted_file.flush()
                temp_file_path = temp_decrypted_file.name

                # Inject the temporary file path to the decorated function
                return func(pathlib.Path(temp_file_path), *args, **kwargs)
            except (FileNotFoundError, FileExistsError):
                return func(None, *args, **kwargs)

            finally:
                # Close and delete the temporary file
                if temp_file_path is not None:
                    temp_decrypted_file.close()
                    os.remove(temp_file_path)

        return wrapper
    return decorator


def generate_key() -> bytes:
    """
    Generates a Fernet key.

    :return: A Fernet key in bytes format.
    """
    return Fernet.generate_key()


def encrypt_and_save_file(file_path: pathlib.Path, data: str, key: bytes) -> None:
    """
    Encrypts the provided data and saves it to the specified file path.

    :param file_path: The path to save the encrypted data.
    :param data: The data to encrypt and save.
    :param key: The encryption/decryption key.
    """
    cipher = Fernet(key)
    with open(file_path, 'wb') as f:
        encrypted_data = cipher.encrypt(data.encode())
        f.write(encrypted_data)


class InitializeCredential:
    def __init__(self, cred_data: str) -> None:
        self.__key = generate_key()
        self.__cred_data = cred_data
        self.encrypted_data: bytes
        self.__file_path = setting.SECRET_DIRECTORY_PATH / 'credentials.enc'
        self.status = 'pending'

    def initialize(self):
        encrypt_and_save_file(self.__file_path, self.__cred_data, self.__key)

        def get_raw_data(file_path: pathlib.Path) -> bytes:
            with open(file_path, 'rb') as f:
                return f.read()

        self.encrypted_data = get_raw_data(self.__file_path)
        self.status = 'success'

    def get_key(self):
        return self.__key


if __name__ == '__main__':
    # pass
    from red_office_google_integration_calendar.src import setting

    f_path = setting.SECRET_DIRECTORY_PATH / 'credentials.enc'
    key = b'Lb-9cbIFCUCFcKSrWqRyEvEYuHAOB6pfMLpmHbrdnNA='

    # data = "What the helwwl"
    # encrypt_and_save_file(f_path, data, key)

    @provide_temp_decrypted_file_path(f_path, key)
    def func(file_path):
        print(file_path)
        with open(file_path, 'rb') as f:
            data = f.read()

        print(data)
    func()
