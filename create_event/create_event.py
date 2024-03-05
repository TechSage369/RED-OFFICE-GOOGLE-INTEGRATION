import json
import sys
from modules.events import CalendarEvent


if __name__ == '__main__':
    json_input = sys.stdin.read()
    data = json.loads(json_input)

    calendarId = data['calendarId']
    event_data = data['event_data']

    event = CalendarEvent().create_event(calendarId, event_data)
    print(json.dumps(event))


# py create_event.py < sample.json
