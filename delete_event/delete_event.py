import json
import sys
from modules.events import CalendarEvent


if __name__ == '__main__':
    json_input = sys.stdin.read()
    data = json.loads(json_input)

    calendarId = data['calendarId']
    eventId = data['eventId']
    optional_parameter = data['optional_parameter'] if 'optional_parameter' in data else {
    }

    event = CalendarEvent().delete_event(calendarId, eventId, **optional_parameter)
    print(json.dumps(event))


# py delete_event.py < sample.json
