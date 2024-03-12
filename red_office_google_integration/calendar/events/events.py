from typing import Any
from googleapiclient.discovery import build
from red_office_google_integration.google_service.google_credentials_service import GoogleCalendarService  # noqa: E203,E402
from red_office_google_integration.src.utils import handle_exception
from red_office_google_integration.log.log_handler import logger
from red_office_google_integration.src import setting


class CalendarEvent:
    '''
        # Methods
        - create_event()
        - delete-event()
        - list_event()

        `Example's and details are given within the method`

        TODO: 
        - update_event()
        - patch_event()
    '''

    def __init__(self, key: bytes):
        self.__key = key
        self.service = self.__build_service()

    @handle_exception
    def __build_service(self):
        cred = GoogleCalendarService(
            self.__key, setting.SCOPE_CALENDAR, setting.FILE_NAME_CALENDAR_TOKEN, setting.FILE_NAME_CALENDAR_CREDENTIAL).get_service()
        return build("calendar", "v3", credentials=cred)

    @handle_exception
    def create_event(self, calendarId: str, event_data: dict[str, Any]) -> dict:
        '''
            # Create_event

            - calendarId: str
            - event_data: dict 
                - find more details on [Create events](https://developers.google.com/calendar/api/guides/create-events)

            ## Example:
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

                event = GoogleCalendarService(key).create_event(calendarId,event_data)


            ```


        '''
        event = self.service.events().insert(
            calendarId=calendarId, body=event_data).execute()
        logger.info(f"Success: {event}")
        return event

    @handle_exception
    def delete_event(self, calendarId: str, eventId: str, **kwargs) -> dict:
        '''
            # Delete Event

            - calendarId: str
            - eventId: str
            - optional: dict
                - find more details on [Delete events](https://developers.google.com/calendar/api/v3/reference/events/delete)

            ## example

            event = GoogleCalendarService().delete_event(calendarId,eventId)

            ### Example with Optional query parameters
            ```
            optional_parameter = {
                'sendUpdates' : 'all'
            }
            calendarId = 'primary'
            eventId = 'eventId'

            event = GoogleCalendarService().delete_event(calendarId,eventId,optional_parameter)
            ```


        '''
        event = self.service.events().delete(calendarId=calendarId,
                                             eventId=eventId, **kwargs).execute()
        logger.warning(f'Event with ID {eventId} deleted Successfully.')

        return {'status': 'Deleted', 'event_id': eventId}

    @handle_exception
    def list_event(self, calendarId: str, optional_parameter: dict) -> dict:
        '''
             # List Event

            - calendarId: str
            - payload: dict
                - find more details on [List events](https://developers.google.com/calendar/api/v3/reference/events/list)


            NOTE: 'All the optional Parameter must on dict and send as a parameter to payload excluding evendId'

            ## example without optional_paramater

            event = GoogleCalendarService(key).list_event(calendarId,{})

            ### Example with Optional query parameters
            ```
            optional_parameter = {
                'maxResults': 2,
                .
                .
                .
            }
            calendarId = 'primary'

            event = GoogleCalendarService().list_event(calendarId,optional_parameter)
            ```



        '''
        events = self.service.events().list(
            calendarId=calendarId, **optional_parameter).execute()
        return events

    @handle_exception
    def get_event(self, calendarId: str, eventId: str, **kwargs) -> dict:
        '''

        NOTE: write proper documentation
            # Get Event

            - calendarId: str
            - eventId: str
            - optional: dict
                - find more details on [Events: get | Google Calendar](https://developers.google.com/calendar/api/v3/reference/events/get)

        ## example

            ```
            event = GoogleCalendarService(key).get_event(calendarId,eventId)
            ```



        '''
        event = self.service.events().get(calendarId=calendarId,
                                          eventId=eventId, **kwargs).execute()
        return event


if __name__ == '__main__':

    pass