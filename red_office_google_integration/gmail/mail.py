from googleapiclient.discovery import build
from red_office_google_integration.google_service.google_credentials_service import GoogleCredentialService  # noqa: E203,E402
from red_office_google_integration.src.utils import handle_exception
from red_office_google_integration.src import setting
from red_office_google_integration.gmail.message_creation import EmailCreation
import json
import pathlib
import base64


class Gmail:

    def __init__(self, key: bytes) -> None:
        '''
        Initialize the Gmail class.

        Args:
            key (bytes): The key used for authentication.
        '''
        self.__key = key
        self.__service = self.__build_service()

    @handle_exception
    def __build_service(self):
        '''
        Build and return the Google service.

        Returns:
            (cred): The Google service.
        '''
        cred = GoogleCredentialService(self.__key, setting.SCOPE_GMAIL,
                                       setting.FILE_NAME_GMAIL_TOKEN, setting.FILE_NAME_GMAIL_CREDENTIAL).get_service()
        return build("gmail", "v1", credentials=cred)

    @handle_exception
    def create_draft(self, body: EmailCreation, userId: str = 'me'):

        create_message = {
            'message': {"raw": body.get_mime_message_encoded()}
        }

        draft = (self.__service.users()
                 .drafts()
                 .create(userId=userId, body=create_message)
                 .execute()
                 )
        print(draft)

    @handle_exception
    def get_email_list(self, query: str, userId: str = 'me', **kwargs):
        results = self.__service.users().messages().list(
            userId=userId, q=query, **kwargs).execute()
        return results
        # print(json.dumps(results, indent=2))

    @handle_exception
    def get_email(self, id: str, userId: str = 'me', **kwargs):
        result = self.__service.users().messages().get(
            userId=userId, id=id, **kwargs).execute()
        return result
        # print(json.dumps(result, indent=2))

    @handle_exception
    def get_attachment_encoded(self, messageId: str, attachmentId: str, userId: str = 'me'):
        attachment = self.__service.users().messages().attachments().get(
            userId=userId, messageId=messageId, id=attachmentId).execute()
        file_data = attachment['data']
        return file_data


if __name__ == '__main__':
    k = "Lb-9cbIFCUCFcKSrWqRyEvEYuHAOB6pfMLpmHbrdnNA="

    obj_mail = Gmail(k.encode())


# _____________________test create draft with/without attachment______________
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
    # obj_mail.create_draft(obj)
# __________________________________________________________________________________

# _____________________test get email list______________________________
    # res = obj_mail.get_email_list(
    #     'has:attachment from:marc@beermann.io', maxResults=10)
    # print(json.dumps(res, indent=2))
# ____________________________________________________________________________________

    # res = obj_mail.get_email("18de4b53777de208")
    # print(json.dumps(res, indent=2))
# ____________________Get Attachment____________________________________
    attachmentId = "ANGjdJ8szlJ2FcznCdjtxqy8PeranCxq8ARdao4MiSzJy8-I-LKCnKyB-h7ZHo9FQBOxqtNWcTyZpu4e62-K1rZsGTAEnqJg3u23fVUGUyRDD_RbrvlcqWpc8k236EVQ31tDcUg6pjmRqNiYwOisoVBx-c3GdEH1MlvbKMNJeA9D1kZG3b8y65zzMuRqMQln82O-pIqpRNNKsG_40bYaDr2lf2HRGKrJKKih8bg-WwHGYfM6swBYfKmQJdHlr4GjhbgH9Eeck-QxIzeZMuU3gprC-UwFwgFokpl5UDXDypGtz-vnWnvkZCREENyWVvIu49mxH2R3JAS9WOG-HWSZ7E4llPFhGSvMM56dRbMCBV-TEEQQl4yVkSE9Z5rXKe3lrj72wMsjl8Dq0pWIoiok"
    data = obj_mail.get_attachment_encoded("18e2d871a1f36de7", attachmentId)
    print(base64.urlsafe_b64decode(data))
