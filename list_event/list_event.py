import json
import sys
from modules.events import CalendarEvent


if __name__ == '__main__':
    json_input = sys.stdin.read()
    data = json.loads(json_input)

    calendarId = data['calendarId']
    optional_parameter = data['optional_parameter']

    event = CalendarEvent().list_event(calendarId, optional_parameter)

    print(event.get('nextPageToken'))
    print(json.dumps(event))

# py list_event.py < sample.json
