from validate_credentials import get_service
from googleapiclient.errors import HttpError
from typing import Any
from log.logger_config import logger
import sys
import os

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (modules package)
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the Python path
sys.path.append(parent_dir)
# Now you can import validate_credentials
from modules.validate_credentials import get_service  # noqa: E203,E402


'''
TODO: 
    - list_event
    - update_event and patch_event
    - documentation
'''


def create_event(calendarId: str, event_data: dict[str, Any]) -> dict[str, Any]:
    '''
    ### Creates a new event on the specified calendar.

    ### Args: 
        `calendarId (str): The ID of the calendar to add the event to.`
        `event_data (dict): A dictionary containing the event data. `

    ### Returns:
        `dict: A dictionary representing the created event.`

    ### Sample event_data:
        get more details on https://developers.google.com/calendar/api/guides/create-events , https://developers.google.com/calendar/api/v3/reference/events
        ```
        event_data = {
                "kind": "calendar#event",
                "etag": etag,
                "id": string,
                "status": string,
                "htmlLink": string,
                "created": datetime,
                "updated": datetime,
                "summary": string,
                "description": string,
                "location": string,
                "colorId": string,
                "creator": {
                    "id": string,
                    "email": string,
                    "displayName": string,
                    "self": boolean
                },
                "organizer": {
                    "id": string,
                    "email": string,
                    "displayName": string,
                    "self": boolean
                },
                "start": {
                    "date": date,
                    "dateTime": datetime,
                    "timeZone": string
                },
                "end": {
                    "date": date,
                    "dateTime": datetime,
                    "timeZone": string
                },
                "endTimeUnspecified": boolean,
                "recurrence": [
                    string
                ],
                "recurringEventId": string,
                "originalStartTime": {
                    "date": date,
                    "dateTime": datetime,
                    "timeZone": string
                },
                "transparency": string,
                "visibility": string,
                "iCalUID": string,
                "sequence": integer,
                "attendees": [
                    {
                    "id": string,
                    "email": string,
                    "displayName": string,
                    "organizer": boolean,
                    "self": boolean,
                    "resource": boolean,
                    "optional": boolean,
                    "responseStatus": string,
                    "comment": string,
                    "additionalGuests": integer
                    }
                ],
                "attendeesOmitted": boolean,
                "extendedProperties": {
                    "private": {
                    (key): string
                    },
                    "shared": {
                    (key): string
                    }
                },
                "hangoutLink": string,
                "conferenceData": {
                    "createRequest": {
                    "requestId": string,
                    "conferenceSolutionKey": {
                        "type": string
                    },
                    "status": {
                        "statusCode": string
                    }
                    },
                    "entryPoints": [
                    {
                        "entryPointType": string,
                        "uri": string,
                        "label": string,
                        "pin": string,
                        "accessCode": string,
                        "meetingCode": string,
                        "passcode": string,
                        "password": string
                    }
                    ],
                    "conferenceSolution": {
                    "key": {
                        "type": string
                    },
                    "name": string,
                    "iconUri": string
                    },
                    "conferenceId": string,
                    "signature": string,
                    "notes": string,
                },
                "gadget": {
                    "type": string,
                    "title": string,
                    "link": string,
                    "iconLink": string,
                    "width": integer,
                    "height": integer,
                    "display": string,
                    "preferences": {
                    (key): string
                    }
                },
                "anyoneCanAddSelf": boolean,
                "guestsCanInviteOthers": boolean,
                "guestsCanModify": boolean,
                "guestsCanSeeOtherGuests": boolean,
                "privateCopy": boolean,
                "locked": boolean,
                "reminders": {
                    "useDefault": boolean,
                    "overrides": [
                    {
                        "method": string,
                        "minutes": integer
                    }
                    ]
                },
                "source": {
                    "url": string,
                    "title": string
                },
                "workingLocationProperties": {
                    "type": string,
                    "homeOffice": (value),
                    "customLocation": {
                    "label": string
                    },
                    "officeLocation": {
                    "buildingId": string,
                    "floorId": string,
                    "floorSectionId": string,
                    "deskId": string,
                    "label": string
                    }
                },
                "outOfOfficeProperties": {
                    "autoDeclineMode": string,
                    "declineMessage": string
                },
                "focusTimeProperties": {
                    "autoDeclineMode": string,
                    "declineMessage": string,
                    "chatStatus": string
                },
                "attachments": [
                    {
                    "fileUrl": string,
                    "title": string,
                    "mimeType": string,
                    "iconLink": string,
                    "fileId": string
                    }
                ],
                "eventType": string
                }
        ```

    '''

    try:
        service = get_service()
        event = service.events().insert(calendarId=calendarId, body=event_data).execute()

        logger.info(f"Success: {event}")
        return event

    except HttpError as e:
        res = {
            'message': 'HttpError',
            'status': e.resp.status
        }
        logger.error(res)
        return res

    except Exception as e:
        logger.critical(e)
        sys.exit(1)


def delete_event(calendarId: str, eventId: str, **kwargs) -> dict:
    '''
    # Deletes Event 

    ### Args: 
        `calendarId (str): The ID of the calendar to delete the event.`
        `eventId (str): Id of event`
    #### **kwargs:
        `sendUpdates: value`
        - Acceptable values are:
            - "all": Notifications are sent to all guests.
            - "externalOnly": Notifications are sent to non-Google Calendar guests only.
            - "none": No notifications are sent. For calendar migration tasks, consider using the

        `sendNotification: bool` Deprecated

    ### Returns:
        `dict: A dictionary representing the created event.`

    '''

    try:
        service = get_service()
        event = service.events().delete(calendarId=calendarId,
                                        eventId=eventId, **kwargs).execute()
        res = {'status': 'Deleted Successfully',
               'message': f'Event with ID {eventId} deleted Successfully.',
               'eventId': eventId}

        logger.warning(res)
        return res

    except HttpError as e:
        res = {'status': "HttpError",
               'status_code': f'{e.resp.status}'}
        logger.error(res)
        return (res)

    except Exception as e:
        logger.critical(e)
        sys.exit(1)


def list_event(payload: dict):
    try:
        service = get_service()
        events_result = service.events().list(**payload).execute()
        events = events_result.get("items", {})
        return events

    except HttpError as e:
        pass
    except Exception as e:
        pass


def update_event():
    pass


if __name__ == '__main__':

    # # Create Event
    # calendarId = "4892670d0114124bf29efc802349d6fde0810d548285b470fe4009d3ff6a134d@group.calendar.google.com"
    # event_data = {
    #     'summary': 'test created by Nishchal Rai',
    #     'location': '800 Howard St., San Francisco, CA 94103',
    #     'description': 'lorem6',
    #     'start': {
    #         'dateTime': '2024-03-28T09:00:00-07:00',
    #         'timeZone': 'America/Los_Angeles',
    #     },
    #     'end': {
    #         'dateTime': '2024-03-28T17:00:00-07:00',
    #         'timeZone': 'America/Los_Angeles',
    #     },
    #     'recurrence': [
    #         'RRULE:FREQ=DAILY;COUNT=2'
    #     ],
    #     'attendees': [
    #         {'email': 'techsage369@proton.me'},
    #     ],
    #     'reminders': {
    #         'useDefault': False,
    #         'overrides': [
    #             {'method': 'email', 'minutes': 24 * 60},
    #             {'method': 'popup', 'minutes': 10},
    #         ],
    #     },
    # }

    # event = create_event(calendarId, event_data)
    # print(event)

    # Delete Event
    # if event['id']:
    #     eventId = event['id']
    #     del_event = delete_event(calendarId, eventId)
    #     print(del_event)

    payload = {
        "calendarId": "primary",
        "timeMin": None,
        "maxResults": 10,
        "singleEvents": True,
        "orderBy": "startTime"
    }

    list_ = list_event(payload)
    print(list_)
