import click
import os
import json
from red_office_google_integration.calendar.events.events import CalendarEvent


@click.group(help="Calendar where you can perform actions on Google Calendar events.")
def calendar():
    pass


@click.command(help="Perform actions on Google Calendar events.")
@click.argument('action', type=click.Choice(['create', 'delete', 'list', 'get']))
@click.argument('payload', type=str, required=True)
@click.option('-o', '--output', type=click.Path(writable=True, resolve_path=True), help='Output directory')
def event(action, payload, output):
    """
    ACTION: The action to perform. Must be one of 'create', 'delete', 'list', 'get'.
    PAYLOAD: Path to a JSON file containing the payload or a JSON string representing the payload.
    Use '--output' to specify an output directory.
    """
    # Load payload from file or string
    if os.path.isfile(payload):
        with open(payload, 'r') as f:
            payload_data = json.load(f)
    else:
        try:
            payload_data = json.loads(payload)
        except json.JSONDecodeError:
            raise click.BadParameter(
                'Payload must be a valid JSON string or a path to a JSON file.')

    # Validate payload
    key = payload_data.get('key')
    calendar_id = payload_data.get('calendarId')
    if not key:
        raise click.ClickException(
            "Key not found! Please specify the key in the payload.")
    if not calendar_id:
        raise click.ClickException(
            "CalendarId not found! Please specify the calendarId in the payload.")

    # Initialize CalendarEvent event
    event = CalendarEvent(key.encode())

    # Perform action based on user input
    if action == 'create':
        if 'event_data' in payload_data:
            event_data = payload_data.get('event_data')
            result = event.create_event(calendar_id, event_data)
        else:
            raise click.ClickException('Event_data not found in the payload.')
    elif action == 'delete':
        if 'eventId' in payload_data:
            optional_parameter = payload_data.get('optional_parameter', {})
            result = event.delete_event(
                calendar_id, payload_data['eventId'], **optional_parameter)
        else:
            raise click.ClickException('EventId not found in the payload.')
    elif action == 'list':
        optional_parameter = payload_data.get('optional_parameter', {})
        result = event.list_event(calendar_id, optional_parameter)
    elif action == 'get':
        if 'eventId' in payload_data:
            optional_parameter = payload_data.get('optional_parameter', {})
            result = event.get_event(
                calendar_id, payload_data['eventId'], **optional_parameter)
        else:
            raise click.ClickException('EventId not found in the payload.')
    else:
        raise click.ClickException('Event operation type not valid!')
    # Output result
    if output:
        with open(output, 'w') as f:
            json.dump(result, f)
        click.echo(json.dumps(result))
    else:
        click.echo(json.dumps(result, indent=2))


calendar.add_command(event)

if __name__ == "__main__":
    calendar()
