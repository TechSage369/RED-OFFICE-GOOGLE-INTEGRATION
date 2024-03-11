import click
import os
import json
from red_office_google_integration.CLI_handler.calendar.events import event


@click.group()
def command_line_interface():
    pass


@click.group(help="this is test")
def calendar():
    pass


@click.command()
@click.argument('credential', type=click.Path(exists=True, readable=True, resolve_path=True))
@click.option('--key_out', type=click.Path(writable=True, resolve_path=True), help='Output key file path')
def init(credential, key_out):
    click.echo(f"Init: Credential: {credential}, Key Out: {key_out}")


@click.command()
def rmcred():
    click.echo("Removing credentials")


@click.command()
@click.argument('presentkey', type=str)
@click.option('--out', type=click.Path(writable=True, resolve_path=True), help='Output file path')
def change_key(presentkey, out):
    click.echo(f"Change Key: Present Key: {presentkey}, Out: {out}")


calendar.add_command(event)
calendar.add_command(rmcred)

command_line_interface.add_command(calendar)
command_line_interface.add_command(event)
command_line_interface.add_command(change_key)
command_line_interface.add_command(rmcred)


if __name__ == "__main__":
    command_line_interface()
