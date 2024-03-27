import click
import os
import json
import base64
import mimetypes

from pyparsing import Any
from red_office_google_integration.gmail.mail import Gmail
from red_office_google_integration.gmail.message_creation import EmailCreation

from red_office_google_integration.src.utils import handle_exception
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@click.group(help="Gmail Where you can perform mail action")
def mail():
    pass


# ____________________________________Create draft CLI____________________________________________________

@click.command(help="Create Draft Email")
@click.argument('payload', type=str, required=True)
@click.option('-a', '--attachment', multiple=True, type=click.Path(writable=True, resolve_path=True), help='attachment file')
def create_draft(payload, attachment):
    if os.path.isfile(payload):
        with open(payload, 'r') as f:
            payload_data = json.load(f)
    else:
        try:
            payload_data = json.loads(payload)
        except json.JSONDecodeError:
            raise click.BadParameter(
                'Payload must be a valid JSON string or a path to a JSON file.')

    key = payload_data.get('key')
    header = payload_data.get('header')
    body = payload_data.get('body')
    subtype = payload_data.get('subtype', "plain")
    userid = payload_data.get('userId', 'me')

    email_message = EmailCreation(
        header, body, subtype)  # Creating email payload
    if attachment:
        for a in attachment:
            if os.path.isfile(a):
                email_message.add_file(a)
            else:
                raise click.BadParameter(f"file dosent exist {a}")

    gmail = Gmail(key.encode())

    result = gmail.create_draft(email_message, userid)
    print(json.dumps(result, indent=2))
# _____________________________________________________________________________________________________________________

# _____________________Get Email________________________________________


@click.command(help="Get email")
@click.argument('payload', type=str, required=True)
def get_email(payload):
    if os.path.isfile(payload):
        with open(payload, 'r') as f:
            payload_data = json.load(f)
    else:
        try:
            payload_data = json.loads(payload)
        except json.JSONDecodeError:
            raise click.BadParameter(
                'Payload must be a valid JSON string or a path to a JSON file.')

    key = payload_data.get('key')
    message_id = payload_data.get('messageId')
    user_id = payload_data.get('userId', 'me')
    optionals = payload_data.get('optionals', {})

    mail = Gmail(key.encode())
    result = mail.get_email(message_id, user_id, **optionals)
    print(json.dumps(result, indent=2))

# ______________________________________________________________________________________________________________________

# _______________________________Download Attachment_____________________________________________________


@click.command(help="Download Attachment")
@click.argument('payload', type=str, required=True)
@click.option('-o', '--output', type=click.Path(file_okay=False, dir_okay=True, writable=True, resolve_path=True), help='Output directory', required=True)
def download_attachment(payload, output):
    if os.path.isfile(payload):
        with open(payload, 'r') as f:
            payload_data = json.load(f)
    else:
        try:
            payload_data = json.loads(payload)
        except json.JSONDecodeError:
            raise click.BadParameter(
                'Payload must be a valid JSON string or a path to a JSON file.')

    print(output)

    key = payload_data.get('key')
    message_id = payload_data.get('messageId')
    user_id = payload_data.get('userId', 'me')
    optionals = payload_data.get('optionals', {})

    mail = Gmail(key.encode())

    message = mail.get_email(message_id, user_id, **optionals)

    for part in message['payload']['parts']:
        data: str
        if part['filename']:
            if 'data' in part['body']:
                data = part['data']['body']
            else:
                attachment_id = part['body']['attachmentId']
                data = mail.get_attachment_encoded(
                    message_id, attachment_id)
            filename = part['filename']
            file_data = base64.urlsafe_b64decode(data.encode())
            save_attachment(output, filename, file_data)
            print(filename)


@handle_exception
def save_attachment(directory_name, filename, data: bytes):
    with open(os.path.join(directory_name, filename), 'wb') as f:
        f.write(data)


@click.command(help="List email through query parameter")
@click.argument('payload', type=str, required=True)
def get_email_list(payload):
    if os.path.isfile(payload):
        with open(payload, 'r') as f:
            payload_data = json.load(f)
    else:
        try:
            payload_data = json.loads(payload)
        except json.JSONDecodeError:
            raise click.BadParameter(
                'Payload must be a valid JSON string or a path to a JSON file.')

    key = payload_data.get('key')
    query = payload_data.get('query', '')
    user_id = payload_data.get('userId', 'me')
    optionals = payload_data.get('optionals', {})

    mail = Gmail(key.encode())
    result = mail.get_email_list(query, user_id, **optionals)
    print(json.dumps(result, indent=2))


mail.add_command(create_draft)
mail.add_command(download_attachment)
mail.add_command(get_email)
mail.add_command(get_email_list)
