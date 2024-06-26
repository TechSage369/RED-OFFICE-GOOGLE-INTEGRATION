import click
from red_office_google_integration.CLI_handler.calendar.events import calendar
from red_office_google_integration.CLI_handler.credentials_management_cli.initialize_credentials import init_cred
from red_office_google_integration.CLI_handler.spreadsheet.spreadsheetCLI import spreadsheet
from red_office_google_integration.CLI_handler.gmail.gmail_cli import mail


@click.group()
def command_line_interface():
    pass


command_line_interface.add_command(calendar)
command_line_interface.add_command(init_cred)
command_line_interface.add_command(spreadsheet)
command_line_interface.add_command(mail)
# command_line_interface.add_command(rmcred)


if __name__ == "__main__":
    command_line_interface()
