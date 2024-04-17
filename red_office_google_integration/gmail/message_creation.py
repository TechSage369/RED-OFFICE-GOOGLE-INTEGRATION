from email.message import EmailMessage
import pathlib
import mimetypes
import base64
import os
from red_office_google_integration.src.utils import handle_exception


class EmailCreation:
    '''
        Class for creating an email message.

        Args:
            header (dict): The email headers.
            body (str): The email body.
            subtype (str, optional): The MIME subtype. Defaults to 'plain'.

        Attributes:
            __mime_message (EmailMessage): The MIME message object.
            __header (dict): The email headers.
            __body (str): The email body.
            __subtype (str): The MIME subtype.

        Methods:
            __build(): Build the MIME message.
            add_file(file_path: pathlib.Path): Add a file as an attachment to the email.
            get_mime_message(): Get the MIME message object.
            get_mime_message_encoded(): Get the MIME message as a base64-encoded string.
    '''

    def __init__(self, header: dict, body: str, subtype: str = 'plain') -> None:
        '''
            Initialize the EmailCreation class.

            Args:
                header (dict): The email headers.
                body (str): The email body.
                subtype (str, optional): The MIME subtype. Defaults to 'plain'.
        '''
        self.__mime_message = EmailMessage()
        self.__header = header
        self.__body = body
        self.__subtype = subtype
        self.__build()

    def __build(self) -> None:
        '''
        Build the MIME message.
        '''
        # appending header to mime message
        for k, v in self.__header.items():
            self.__mime_message[k] = v
        self.__mime_message.set_content(self.__body, subtype=self.__subtype)

    @handle_exception
    def add_file(self, file_path: pathlib.Path) -> None:
        '''
            Add a file as an attachment to the email.

            Args:
                file_path (pathlib.Path): The path to the file.
        '''
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
        '''
            Get the MIME message object.

            Returns:
                EmailMessage: The MIME message object.
        '''
        return self.__mime_message

    def get_mime_message_encoded(self) -> str:
        '''
            Get the MIME message as a base64-encoded string.

            Returns:
                str: The base64-encoded MIME message.
        '''
        encoded_message = base64.urlsafe_b64encode(
            self.__mime_message.as_bytes()).decode()
        return encoded_message


if __name__ == '__main__':
    # header = {
    #     'To': 'techsage@gmail.com',
    #     'From': 'aadithya223@gmail.com',
    #     'Subject': 'Testing Gmail API v1',
    # }

    # body = "THis is just for testing <b> bold </b>"
    # subtype = 'html'
    # file_path = pathlib.Path('data.csv')

    # obj = EmailCreation(header, body, subtype)

    # obj.add_file(pathlib.Path('data.csv'))
    # obj.add_file(pathlib.Path('README.md'))

    # obj.get_mime_message()
    pass
