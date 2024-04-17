from red_office_google_integration.google_service.file_handler import InitializeCredential
from red_office_google_integration.src import setting
import click
import json
import os


'''
NOTE: 
'''


@click.command(help="Encrypts the credentials and saves the file.")
@click.argument('cred', type=str, required=True)
@click.option('-o', '--output', type=click.Path(writable=True, resolve_path=True), help='Output directory to save key')
@click.option('-k', '--key', type=click.STRING, help='Custom key in string')
def init_cred(cred, output, key: str) -> None:
    """
    Encrypts the credentials using a fernet key and saves the file.

    Args:
        cred (str): Path to the credential file | in string.
        output (filepath,optional): Path to the output directory where the encrypted file will be saved.
        key (str,optional): Path to the key file used for encryption (fernet key by default).

    Returns:
        None
    """
    # Load cred from file or string
    if os.path.isfile(cred):
        with open(cred, 'r') as f:
            cred = f.read()
    else:
        try:
            cred = json.loads(cred)
        except json.JSONDecodeError:
            raise click.BadParameter(
                'Payload must be a valid JSON string or a path to a JSON file.')
    if key:
        print(key)
        result = InitializeCredential(
            cred, setting.DEFAULT_CREDENTIAL_FILE_NAME, key.encode())
    else:
        result = InitializeCredential(
            cred, setting.DEFAULT_CREDENTIAL_FILE_NAME)

    result.initialize()

    result = {
        'status': result.status,
        'key': result.get_key().decode()
    }

    if output:
        with open(output, 'w') as f:
            json.dump(result, f)
        click.echo(json.dumps(result))
    else:
        click.echo(json.dumps(result, indent=2))


if __name__ == "__main__":
    init_cred()
