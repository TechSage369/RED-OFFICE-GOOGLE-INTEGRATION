import click
from red_office_google_integration.CLI_handler.calendar.events import calendar
from red_office_google_integration.CLI_handler.credentials_management_cli.initialize_credentials import init_cred


@click.group()
def command_line_interface():
    pass


command_line_interface.add_command(calendar)
command_line_interface.add_command(init_cred)
# command_line_interface.add_command(rmcred)


if __name__ == "__main__":
    command_line_interface()
