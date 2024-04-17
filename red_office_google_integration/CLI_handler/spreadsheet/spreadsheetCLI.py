
import click
import os
import json
import pandas as pd
from red_office_google_integration.spreadsheets.sheets import SpreadSheet
from red_office_google_integration.src.utils import handle_exception
"""
# Spread Sheet
"""


@click.group(help="Spreadsheet where you can perform actions on Google Spreadsheet events.")
def spreadsheet():
    pass


# _____________________________________________________get_data_cli_section____________________________________________________
@click.command(help="Retrieves data from a specified range in a Google Sheets spreadsheet.")
@click.argument('payload', type=str, required=True)
@click.option('-o', '--output', type=click.Path(writable=True, resolve_path=True), help='Output directory')
def get_data(payload, output):
    """
    """
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
    spreadsheetId = payload_data.get('spreadsheetId')
    range = payload_data.get('range')
    optionals = payload_data.get('optionals', {})
    spreadsheet = SpreadSheet(key.encode())

    res = spreadsheet.get_data(spreadsheetId, range, **optionals)
    print(json.dumps(res, indent=2))

    if output:
        save_to_file(res, output)
# _______________________________________________________________________________________________________________________

# get batch_batch_data


@click.command(help="Retrieves data from a multiple specified ranges in a Google Sheets spreadsheet.")
@click.argument('payload', type=str, required=True)
@click.option('-o', '--output', type=click.Path(writable=True, resolve_path=True), help='Output directory')
def get_batch_data(payload, output):
    """
    # Get_batch_data
    """
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
    spreadsheetId = payload_data.get('spreadsheetId')
    ranges = payload_data.get('ranges')
    optionals = payload_data.get('optionals', {})
    spreadsheet = SpreadSheet(key.encode())

    res = spreadsheet.get_batch_data(spreadsheetId, ranges, **optionals)
    print(json.dumps(res, indent=2))

    if output:
        save_to_file(res, output)


@click.command(help="update_values to specifed range in spreadsheet")
@click.argument('payload', type=str, required=True)
def update_values(payload):
    """
    # Update Values
    """
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
    spreadsheetId = payload_data.get('spreadsheetId')
    valueInputOption = payload_data.get('valueInputOption')
    range = payload_data.get('range')
    values = payload_data.get('values')
    optionals = payload_data.get('optionals', {})

    spreadsheet = SpreadSheet(key.encode())
    result = spreadsheet.update_values(
        spreadsheetId, range, valueInputOption, values, **optionals)

    print(json.dumps(result, indent=2))


@click.command(help="update_values to multiple specifed range in spreadsheet")
@click.argument('payload', type=str, required=True)
def batch_update_values(payload):
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
    spreadsheetId = payload_data.get('spreadsheetId')
    data = payload_data.get('data')
    valueInputOption = payload_data.get('valueInputOption')
    optionals = payload_data.get('optionals', {})

    spreadsheet = SpreadSheet(key.encode())
    result = spreadsheet.batch_update_values(
        spreadsheetId, valueInputOption, data, **optionals)
    print(json.dumps(result, indent=2))


@click.command(help="Append values to spreadsheet")
@click.argument('payload', type=str, required=True)
def append_data(payload):
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
    spreadsheetId = payload_data.get('spreadsheetId')
    valueInputOption = payload_data.get('valueInputOption')
    range = payload_data.get('range')
    values = payload_data.get('values')
    optionals = payload_data.get('optionals', {})

    spreadsheet = SpreadSheet(key.encode())
    result = spreadsheet.append_data(
        spreadsheetId, range, valueInputOption, values, **optionals)

    print(json.dumps(result, indent=2))


@handle_exception
def save_to_file(data, filename):
    df = pd.DataFrame(data)
    _, file_extension = os.path.splitext(filename)
    if file_extension.lower() == '.csv':
        df.to_csv(filename, index=False, header=False)
    elif file_extension.lower() == '.json':
        df.to_json(filename, indent=2, orient='records')
    else:
        raise click.BadParameter(
            "Output file must be either a CSV or JSON file. Unable to save")


spreadsheet.add_command(get_data)
spreadsheet.add_command(get_batch_data)
spreadsheet.add_command(update_values)
spreadsheet.add_command(batch_update_values)
spreadsheet.add_command(append_data)

if __name__ == "__main__":
    spreadsheet()
