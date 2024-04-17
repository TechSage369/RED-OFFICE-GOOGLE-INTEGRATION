
import click
import os
import json
import pandas as pd
from red_office_google_integration.spreadsheets.sheets import SpreadSheet
from red_office_google_integration.src.utils import handle_exception
"""
# CLI Module

This module provides a command-line interface (CLI) for interacting with Google Spreadsheets. It allows you to perform various actions such as retrieving data, updating values, and appending data to a spreadsheet.

## Commands

- `get_data`: Retrieves data from a specified range in a Google Sheets spreadsheet. `py main.py spreadsheet get-data`
- `get_batch_data`: Retrieves data from multiple specified ranges in a Google Sheets spreadsheet. `py main.py spreadsheet get-batch-data`
- `update_values`: Updates values in a specified range in a Google Sheets spreadsheet. `py main.py spreadsheet update-values`
- `batch_update_values`: Updates values in multiple specified ranges in a Google Sheets spreadsheet. `py main.py spreadsheet batch-update-values`
- `append_data`: Appends values to a specified range in a Google Sheets spreadsheet. `py main.py spreadsheet append-data`


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
        Retrieves data from a specified range in a Google Sheets spreadsheet.

        Args:
            payload (str): Path to a JSON file or a JSON string containing the request payload.
            output (str): Path to the output file where the retrieved data will be saved.

        Returns:
            None
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
        Retrieves data from multiple specified ranges in a Google Sheets spreadsheet.

        Args:
            payload (str): Path to a JSON file or a JSON string containing the request payload.
            output (str): Path to the output file where the retrieved data will be saved.

        Returns:
            None
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
        Updates values in a specified range in a Google Sheets spreadsheet.

        Args:
            payload (str): Path to a JSON file or a JSON string containing the request payload.

        Returns:
            None
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
    """
        Updates values in multiple specified ranges in a Google Sheets spreadsheet.

        Args:
            payload (str): Path to a JSON file or a JSON string containing the request payload.

        Returns:
            None
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
    """
        Appends values to a specified range in a Google Sheets spreadsheet.

        Args:
            payload (str): Path to a JSON file or a JSON string containing the request payload.

        Returns:
            None
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
    result = spreadsheet.append_data(
        spreadsheetId, range, valueInputOption, values, **optionals)

    print(json.dumps(result, indent=2))


@handle_exception
def save_to_file(data, filename):
    """
    Saves data to a file in CSV or JSON format.

    Args:
        data (dict): The data to be saved.
        filename (str): The path to the file where the data will be saved.

    Returns:
        None
    """
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
