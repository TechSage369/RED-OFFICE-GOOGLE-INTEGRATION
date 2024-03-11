import click
import os
import json
from red_office_google_integration.calendar.events.events import CalendarEvent
# Events


@click.command(help="""
    Perform actions on Google Calendar events.
    ACTION: The action to perform. Must be one of 'create', 'delete', 'list', 'get'.
    PAYLOAD: Path to a JSON file containing the payload or a JSON string representing the payload.
    Use '--output' to specify an output directory.
               """)
@click.argument('action', type=click.Choice(['create', 'delete', 'list', 'get']))
@click.argument('payload', type=click.Path(exists=True, readable=True, resolve_path=True), required=True)
@click.option('-o', '--output', type=click.Path(writable=True, resolve_path=True), help='Output Directory')
def event(action, payload, output):
    result = None
    # Check if payload is a file path
    if os.path.isfile(payload):
        with open(payload, 'r') as f:
            payload_data = json.load(f)
    else:
        try:
            payload_data = json.loads(payload)
        except json.JSONDecodeError:
            raise click.BadParameter(
                'Payload must be a valid JSON string or a path to a JSON file.')

# check args section
    if output:
        if not ('.' in os.path.basename(output)):
            raise click.BadParameter("Output dosen\'t have filename")

    key = payload_data.get('key')
    calendar_id = payload_data.get('calendarId')

    if not key:
        raise click.ClickException(
            "Key not found!. please mention key in args using (--key or -k) or in payload")
    if not calendar_id:
        raise click.ClickException('CalendarId not found!')


# event handler
    service = CalendarEvent(key.encode())

    # create
    if action == 'create':
        if 'event_data' in payload_data:
            event_data = payload_data.get('event_data')
            result = service.create_event(calendar_id, event_data)
        else:
            raise click.ClickException('Even_data not found!.')
    # delete
    elif action == 'delete':
        optional_parameter = payload_data.get('optional_parameter', {})

        if not 'eventId' in payload_data:
            raise click.ClickException('eventId not found')

        result = service.delete_event(
            calendar_id, payload_data['eventId'], **optional_parameter)

    # List
    elif action == 'list':
        optional_parameter = payload_data.get('optional_parameter', {})
        result = service.list_event(calendar_id, optional_parameter)

    # get
    elif action == 'get':
        optional_parameter = payload_data.get('optional_parameter', {})
        if not 'eventId' in payload_data:
            raise click.ClickException('eventId not found')

        result = service.get_event(
            calendar_id, payload_data['eventId'], **optional_parameter)

# output of events
    if output:
        print(json.dumps(result))
        with open(output, 'wb') as f:
            f.write(str(json.dumps(result)).encode())
    else:
        print(json.dumps(result))
