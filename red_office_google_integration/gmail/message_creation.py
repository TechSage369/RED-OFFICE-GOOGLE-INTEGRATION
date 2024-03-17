from email.message import EmailMessage
import pathlib
import mimetypes
import base64
import os
from red_office_google_integration.src.utils import handle_exception


class EmailCreation:
    def __init__(self, header: dict, body: str, subtype: str = 'plain') -> None:
        self.__mime_message = EmailMessage()
        self.__header = header
        self.__body = body
        self.__subtype = subtype
        self.__build()

    def __build(self) -> None:
        # appending header to mime message
        for k, v in self.__header.items():
            self.__mime_message[k] = v
        self.__mime_message.set_content(self.__body, subtype=self.__subtype)

    @handle_exception
    def add_file(self, file_path: pathlib.Path) -> None:
        # Guessing the MIME type
        attachment_filename = file_path
        mime_type, _ = mimetypes.guess_type(attachment_filename)

        if mime_type:  # Check if MIME type was successfully guessed
            maintype, subtype = mime_type.split("/")
        else:
            # Use a default MIME type in case guess_type fails
            maintype = 'application'
            subtype = 'octet-stream'

        with open(attachment_filename, "rb") as fp:
            attachment_data = fp.read()
            self.__mime_message.add_attachment(
                attachment_data, maintype, subtype, filename=os.path.basename(attachment_filename))

    def get_mime_message(self) -> EmailMessage:
        return self.__mime_message

    def get_mime_message_encoded(self) -> str:
        encoded_message = base64.urlsafe_b64encode(
            self.__mime_message.as_bytes()).decode()
        return encoded_message


if __name__ == '__main__':
    header = {
        'To': 'techsage@gmail.com',
        'From': 'aadithya223@gmail.com',
        'Subject': 'Testing Gmail API v1',
    }

    body = "THis is just for testing <b> bold </b>"
    subtype = 'html'
    file_path = pathlib.Path('data.csv')

    obj = EmailCreation(header, body, subtype)

    obj.add_file(pathlib.Path('data.csv'))
    obj.add_file(pathlib.Path('README.md'))

    obj.get_mime_message()
