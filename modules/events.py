from googleapiclient.errors import HttpError, InvalidJsonError
from typing import Any
import sys
from validate_credentials import GoogleCalendarService  # noqa: E203,E402
from log.logger_config import logger  # noqa: E203,E402


def handle_exception(func):
    #  Note: Decorator Function

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HttpError as e:
            res = {'status': e.resp.status, 'message': 'HttpError'}
            logger.error(res)
            return res
        except InvalidJsonError as e:
            res = {'status': 'InvalidJsonError', 'message': e}
            logger.error(res)
            return res
        except TypeError as e:
            res = {'status': 'TypeError', 'message': e}
            logger.error(res)
            return res
        except Exception as e:
            logger.critical(e)
            print({'message': e})
            sys.exit(1)
    return wrapper


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

    def __init__(self):
        self.service = GoogleCalendarService().get_service()

    @handle_exception
    def create_event(self, calendarId: str, event_data: dict[str, Any]):
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

                event = GoogleCalendarService().create_event(calendarId,event_data)


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
        return event

    @handle_exception
    def list_event(self, calendarId: str, optional_parameter: dict) -> list | dict:
        '''
             # List Event

            - calendarId: str
            - payload: dict
                - find more details on [List events](https://developers.google.com/calendar/api/v3/reference/events/list)


            NOTE: 'All the optional Parameter must on dict and send as a parameter to payload excluding evendId'

            ## example without optional_paramater

            event = GoogleCalendarService().list_event(calendarId,{})

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
        # events = events_result.get("items", {})
        return events


if __name__ == '__main__':

    payload = {
        'maxResults': 1
    }
    event = CalendarEvent().list_event(
        'primary', payload)
    print(event)
