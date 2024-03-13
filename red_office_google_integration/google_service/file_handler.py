"""
    This module contains functions for encrypting and decrypting files, as well as a decorator function
    to create a temporary file that holds decrypted data and injects it into a function.
    This is especially useful for Google credentials, which require a file path and cannot use an encrypted file path.

    Functions:
        - decrypt_file(): Decrypts a file using a generated key.
        - provide_temp_decrypted_file_path(): Provides the temporary path for the decrypted file.
        - generate_key(): Generates a key for encryption and decryption.
        - encrypt_and_save_file(): Encrypts and saves a file.
    NOTE:
        when token is invalid or filenot exist we have to generate new one but when credentials dosen't exit or
        invalid throw error. so my function right now is not well structured
    TODO:
        Write unit tests
        
        OPTIONAL
            - encrypt_data
"""
from cryptography.fernet import Fernet, InvalidToken
import tempfile
import os
import pathlib
from typing import Any, Callable
from red_office_google_integration.src import setting


class FileError(Exception):
    """
        This exception is specifically designed for use with the `provide_temp_decrypted_file_path` decorator function. 
        The decorator function decrypts a token or credentials file, creates a temporary path, and passes it to the decorated function. 
        After the decorated function is executed, it destroys the decrypted file.

        In the case of a token, if there is a problem with the file, it raises a FileNotFoundError so that the GoogleCredential 
        can generate a new token. However, in the case of credentials, it must throw an error. 

        Usage in token:

        if type(path) == FileNotFoundError:
            get_new_token()

        Usage in credentials:

        if type(path) == FileNotFoundError:
            raise FileError("Credentials file not found")
    """

    def __init__(self, message="File error occured", *args: object) -> None:
        super().__init__(message, *args)
        self.message = message


def provide_temp_decrypted_file_path(encrypted_file_path: pathlib.Path, key: bytes) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator function that decrypts the data from the specified file path using the provided key,
    stores the decrypted data in a temporary file, and injects the temporary file path to the decorated function.
    The temporary file is deleted after the decorated function is executed.

    :param encrypted_file_path: The path to the encrypted file.
    :param key: The encryption/decryption key in bytes.
    :return: The wrapper function.

    Example:

    @provide_temp_decrypted_file_path(encrypted_filepath, key)
    def func(file_path: pathlib.Path):
        # your statement here
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
            except (FileNotFoundError, FileExistsError, PermissionError) as e:
                return func(FileError(f'FileError: {type(e).__name__} -> {os.path.basename(encrypted_file_path)}'), *args, **kwargs)
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


def decrypt_file(path: pathlib.Path, key: bytes) -> bytes:
    """
    Decrypts the data from the specified file path using the provided key.

    :param path: The path to the encrypted file.
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


class InitializeCredential:
    """
    A class for initializing and encrypting credential data and saving it to a file.

    Args:
    - cred_data (str): The credential data to be encrypted.
    - file_name (str): The name of the file to save the encrypted data.
    - key (bytes, optional): The encryption key. Defaults to a randomly generated key.

    Attributes:
    - encrypted_data (bytes): The encrypted credential data.
    - status (str): The status of the initialization process. Default is 'pending'.

    Methods:
    - initialize(): Encrypts the credential data and saves it to the specified file.
    - get_key(): Returns the encryption key.

    Example:
    ```
    credential = InitializeCredential(cred_data, file_name)
    credential.initialize()
    key = credential.get_key()
    ```
    """

    def __init__(self, cred_data: str, file_name: str, key: bytes = generate_key()) -> None:
        """
        Initialize the InitializeCredential class.

        Args:
            cred_data (str): The credential data to be encrypted.
            file_name (str): The name of the file to save the encrypted data.
            key (bytes, optional): The encryption key. Defaults to a randomly generated key.

        Attributes:
            encrypted_data (bytes): The encrypted credential data.
            status (str): The status of the initialization process. Default is 'pending'.
        """
        self.__key = key
        self.__cred_data = cred_data
        self.encrypted_data: bytes
        self.__file_path = setting.SECRET_DIRECTORY_PATH / file_name
        self.status = 'pending'

    def initialize(self):
        """
        Encrypts the credential data, saves it to the specified file, and updates the `encrypted_data`
        attribute with the encrypted data. It also sets the `status` attribute to 'success'.
        """
        encrypt_and_save_file(self.__file_path, self.__cred_data, self.__key)

        def get_raw_data(file_path: pathlib.Path) -> bytes:
            with open(file_path, 'rb') as f:
                return f.read()

        self.encrypted_data = get_raw_data(self.__file_path)
        self.status = 'success'

    def get_key(self):
        """
        Returns the encryption key.

        Returns: bytes: The encryption key.
        """
        return self.__key


if __name__ == '__main__':
    pass
