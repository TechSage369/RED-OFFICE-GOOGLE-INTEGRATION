import json
import sys
from modules.events import CalendarEvent

'''
    sample Data
    ```
    {
    "calendarId": "4892670d0114124bf29efc802349d6fde0810d548285b470fe4009d3ff6a134d@group.calendar.google.com",
    "event_data": {
        "summary": "test created by Nishchal Rai",
        "location": "800 Howard St., San Francisco, CA 94103",
        "description": "lorem6",
        "start": {
            "dateTime": "2024-03-28T09:00:00-07:00",
            "timeZone": "America/Los_Angeles"
        },
        "end": {
            "dateTime": "2024-03-28T17:00:00-07:00",
            "timeZone": "America/Los_Angeles"
        },
        "recurrence": [
            "RRULE:FREQ=DAILY;COUNT=2"
        ],
        "attendees": [
            {
                "email": "techsage369@proton.me"
            }
        ],
        "reminders": {
            "useDefault": false,
            "overrides": [
                {
                    "method": "email",
                    "minutes": 1440
                },
                {
                    "method": "popup",
                    "minutes": 10
                }
            ]
        }
    }
}
    ```

'''

if __name__ == '__main__':
    json_input = sys.stdin.read()
    data = json.loads(json_input)

    calendarId = data['calendarId']
    event_data = data['event_data']

    event = CalendarEvent().create_event(calendarId, event_data)
    print(json.dumps(event))


# py create_event.py < sample.json
