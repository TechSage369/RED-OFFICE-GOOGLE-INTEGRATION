from red_office_google_integration.google_service.file_handler import InitializeCredential
from red_office_google_integration.src import setting
import click
import json
import os


'''
NOTE: Not Tested yet
'''


@click.command(help="Encrypts the credentials and saves the file.")
@click.argument('cred', type=str, required=True)
@click.option('-o', '--output', type=click.Path(writable=True, resolve_path=True), help='Output directory to save key')
@click.option('-k', '--key', type=click.Path(writable=True, resolve_path=True), help='Custom key file path (uses fernet)')
def init_cred(cred, output, key):
    """
    Encrypts the credentials using a fernet key and saves the file.

    Args:
        cred (str): Path to the credential file | in string.
        output (str): Path to the output directory where the encrypted file will be saved.
        key (str): Path to the key file used for encryption (fernet key by default).

    Returns:
        None
    """
    # Load cred from file or string
    if os.path.isfile(cred):
        with open(cred, 'r') as f:
            payload_data = json.load(f)
    else:
        try:
            payload_data = json.loads(cred)
        except json.JSONDecodeError:
            raise click.BadParameter(
                'Payload must be a valid JSON string or a path to a JSON file.')

    if key:
        result = InitializeCredential(
            cred, setting.DEFAULT_CREDENTIAL_FILE_NAME, key)
    else:
        result = InitializeCredential(
            cred, setting.DEFAULT_CREDENTIAL_FILE_NAME)

    if output:
        with open(output, 'w') as f:
            json.dump(result, f)
        click.echo(json.dumps(result))
    else:
        click.echo(json.dumps(result, indent=2))


if __name__ == "__main__":
    init_cred()
