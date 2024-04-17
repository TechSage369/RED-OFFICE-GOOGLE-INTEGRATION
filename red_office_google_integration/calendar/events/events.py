'''
    TODO: 
    - unit testing
    
    - optional:
        - Implement update_event()
        - patch_event() methods.
    NOTE:
        Features that can be added:
        - find and replace
        

'''
from typing import Any
from googleapiclient.discovery import build
from red_office_google_integration.google_service.google_credentials_service import GoogleCredentialService  # noqa: E203,E402
from red_office_google_integration.src.utils import handle_exception
from red_office_google_integration.log.log_handler import logger
from red_office_google_integration.src import setting


class CalendarEvent:
    '''
    A class for handling Google Calendar events.

    Methods:
    - create_event()
    - delete_event()
    - list_event()
    - get_event()
    '''

    def __init__(self, key: bytes):
        '''
        Initialize the CalendarEvent class.

        Args:
            key (bytes): The key used for authentication.
        '''
        self.__key = key
        self.service = self.__build_service()

    @handle_exception
    def __build_service(self):
        '''
        Build and return the Google Calendar service.

        Returns:
            (cred): The Google Calendar service.
        '''
        cred = GoogleCredentialService(
            self.__key, setting.SCOPE_CALENDAR, setting.FILE_NAME_CALENDAR_TOKEN, setting.FILE_NAME_CALENDAR_CREDENTIAL).get_service()
        return build("calendar", "v3", credentials=cred)

    @handle_exception
    def create_event(self, calendarId: str, event_data: dict[str, Any]) -> dict:
        '''
            Create a new event in the specified calendar.

            Args:
                calendarId (str): The ID of the calendar in which to create the event.
                event_data (dict): A dictionary containing the details of the event.
                    Find more details on event data format: 
                    [Create events](https://developers.google.com/calendar/api/guides/create-events)

            Returns:
                dict: The created event data.

            Example payload:
                ```
                calendarId = 'primary'
                event_data = {
                    'summary': 'Google I/O 2015',
                    'location': '800 Howard St., San Francisco, CA 94103',
                    'description': 'A chance to hear more about Google developer products.',
                    'start': {
                        'dateTime': '2015-05-28T09:00:00-07:00',
                        'timeZone': 'America/Los_Angeles',
                    },
                    'end': {
                        'dateTime': '2015-05-28T17:00:00-07:00',
                        'timeZone': 'America/Los_Angeles',
                    },
                    'recurrence': [
                        'RRULE:FREQ=DAILY;COUNT=2'
                    ],
                    'attendees': [
                        {'email': 'lpage@example.com'},
                        {'email': 'sbrin@example.com'},
                    ],
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'email', 'minutes': 24 * 60},
                            {'method': 'popup', 'minutes': 10},
                        ],
                    },
                }
                event = CalendarEvent(key)
                data = event.create_event(calendarId, event_data)
                ```

        '''
        event = self.service.events().insert(
            calendarId=calendarId, body=event_data).execute()
        logger.info(f"Success: {event}")
        return event

    @handle_exception
    def delete_event(self, calendarId: str, eventId: str, **kwargs) -> dict:
        '''
        Delete an event from the specified calendar.

        Args:
            calendarId (str): The ID of the calendar from which to delete the event.
            eventId (str): The ID of the event to delete.

        Returns:
            dict: A status message indicating the deletion was successful.

        ## example

            event = GoogleCredentialService().delete_event(calendarId,eventId)

            ### Example with Optional query parameters
            ```
            optional_parameter = {
                'sendUpdates' : 'all'
            }
            calendarId = 'primary'
            eventId = 'eventId'

            event = CalendarEvent(key)
            data = event.delete_event(calendarId,eventId,optional_parameter)
            ```


        '''
        event = self.service.events().delete(calendarId=calendarId,
                                             eventId=eventId, **kwargs).execute()
        logger.warning(f'Event with ID {eventId} deleted Successfully.')

        return {'status': 'Deleted', 'event_id': eventId}

    @handle_exception
    def list_event(self, calendarId: str, optional_parameter: dict) -> dict:
        '''
        List events from the specified calendar.

        Args:
            calendarId (str): The ID of the calendar from which to list events.
            optional_parameter (dict): Optional parameters for listing events. Refer to the
                [Events: list documentation](https://developers.google.com/calendar/api/v3/reference/events/list)
                for details on available parameters.

        Returns:
            dict: The list of events.

        Example:
            ```
            # Example without optional parameters
            event = GoogleCredentialService(key).list_event(calendarId, {})

            # Example with optional query parameters
            optional_parameter = {
                'maxResults': 2,
                # Add more optional parameters as needed
            }
            event = CalendarEvent(key)
            data = event.list_event(calendarId, optional_parameter)
            ```
        '''
        events = self.service.events().list(
            calendarId=calendarId, **optional_parameter).execute()
        return events

    @handle_exception
    def get_event(self, calendarId: str, eventId: str, **kwargs) -> dict:
        '''
        Get details of a specific event from the specified calendar.

        Args:
            calendarId (str): The ID of the calendar containing the event.
            eventId (str): The ID of the event to retrieve.
            **kwargs (**kwarg): Optional keyword arguments for additional parameters. Refer to the
                [Events: get documentation](https://developers.google.com/calendar/api/v3/reference/events/get)
                for details on available parameters.

        Returns:
            (dict): The event details.

        Example:
            ```
            event = CalendarEvent(key)
            data = event.get_event(calendarId, eventId)
            ```
        '''
        event = self.service.events().get(calendarId=calendarId,
                                          eventId=eventId, **kwargs).execute()
        return event


if __name__ == '__main__':

    pass
