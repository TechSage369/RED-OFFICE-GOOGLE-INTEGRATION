## SETUP

1. **Setup Python 3.10:**
   Ensure you have Python 3.10 installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

2. **Clone the Repository:**
   Use the following command to clone the repository:
   ```shell
   git clone https://github.com/TechSage369/RED-OFFICE-GOOGLE-INTEGRATION.git
   ```

3. **Install Poetry:**
   `(if you want to setup without/other virtual environment then, just check pyproject.toml you'll get dependencies there)`
   Poetry is a tool for dependency management and packaging in Python. Install it using pip:
   ``` shell
   pip install poetry
   ```

4. **Configure Virtual Environment:**
   Configure Poetry to create the virtual environment inside your project directory:
   ```shell
   poetry config virtualenvs.in-project true
   ```

5. **Install Dependencies:**
   Use Poetry to install the project dependencies specified in the `pyproject.toml` file:
   ```shell
   poetry install
   ```

6. **Activate the Virtual Environment (Optional):**
   If you want to activate the virtual environment created by Poetry, you can use the following command:
   ```shell
   poetry shell
   ```


# CONFIG Credentials for calendar

please follow this link till credential creation and save to json file

[Python quickstart  |  Google Calendar  |  Google for Developers](https://developers.google.com/calendar/api/quickstart/python)


`After getting credential`

---

## Setup Credentials

To initialize your credentials, provide the credential file name. You will receive the key in the CLI, which you should keep safe for later use as API_KEY.

```bash
py main.py init-cred credential_filename
```

You can also use optional parameters to specify a custom key (e.g., `Lb-9cbIFCUCFcKSrWqRyEvEYuHAOB6pfMLpmHbrdnNA=`) and mention the output file path to save the key. `Fernet key 128-bit base64-encoded `

```bash
py main.py init-cred credential_filename -o outputfilename -k Lb-9cbIFCUCFcKSrWqRyEvEYuHAOB6pfMLpmHbrdnNA
```

Make sure to replace `credential_filename` with the name of your credential file and `outputfilename` with the desired output file path.


## Calendar Events

The following operations are supported for calendar events:
- [Create Event](#create-event)
- [List Event](#list-events)
- [Delete Event](#delete-event)
- [Get Event](#get-event)

### Create Event
To create an event, use the following JSON payload structure:

```json
{
    "key": "YOUR_API_KEY",
    "calendarId": "primary",
    "event_data": {
        "summary": "Event summary",
        "location": "Event location",
        "description": "Event description",
        "start": {
            "dateTime": "Event start date and time",
            "timeZone": "Event time zone"
        },
        "end": {
            "dateTime": "Event end date and time",
            "timeZone": "Event time zone"
        },
        "recurrence": [
            "RRULE:FREQ=DAILY;COUNT=2"
        ],
        "attendees": [
            {
                "email": "attendee_email@example.com"
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



Ensure you replace `"YOUR_API_KEY"` with your actual API key. For more details on available properties and values, refer to the [Events: insert documentation](https://developers.google.com/calendar/api/v3/reference/events/insert).



```json
{
    "key": "Lb-9cbIFCUCFcKSrWqRyEvEYuHAOB6pfMLpmHbrdnNA=",
    "calendarId": "primary",
    "event_data": {
        "summary": "test created by Tech Sage",
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


To create an event using the command line interface (CLI) with the specified syntax, you can use the following example:

```bash
py main.py calendar event create --output output_filename payload_json_file_or_json_string
```

This command will create an event using the payload provided in `payload_json_file_or_json_string` and optionally save the result to `output_filename`. If no output file is specified, the result will be displayed in the terminal.

Here's the command without explicitly mentioning the output file:

```bash
py main.py calendar event create payload_json_file_or_json_string
```

In this case, the result will be displayed in the terminal without saving it to a file.


## List Events

To list events, use the following JSON structure:

```json
{
    "key": "YOUR_API_KEY",
    "calendarId": "YOUR_CALENDAR_ID",
    "optional_parameter": {
        "showDeleted": false
    }
}
```

### Parameters

- `key` (required): Your Google Calendar API key.
- `calendarId` (required): The ID of the calendar from which to retrieve events.
- `optional_parameter` (optional): Additional parameters for listing events. In this example, we use `showDeleted` to specify whether to include deleted events (`true` or `false`).

For more optional parameters, refer to the [Events: list documentation](https://developers.google.com/calendar/api/v3/reference/events/list).

### Example

```bash
py main.py calendar event list payload.json
```


## Delete Event

To delete an event, use the following JSON payload structure:

```json
{
    "key": "Your API key",
    "calendarId": "Your calendar ID",
    "eventId": "Event ID to delete",
    "optional_parameter": {}
}
```

You can include optional parameters as needed. For more details on available parameters, refer to the [Events: delete documentation](https://developers.google.com/calendar/api/v3/reference/events/delete).

### Example Usage

To delete an event using the command line interface (CLI) with the specified syntax, you can use the following example:

```bash
py main.py calendar event delete payload.json
```

This command will delete the event specified in `payload.json`. Make sure to replace `"Your API key"`, `"Your calendar ID"`, and `"Event ID to delete"` with your actual API key, calendar ID, and event ID respectively.



## Get Event

To get an event, use the following JSON payload structure:

```json
{
    "key": "Your API key",
    "calendarId": "Your calendar ID",
    "eventId": "Event ID to retrieve",
    "optional_parameter": {}
}
```

You can include optional parameters as needed. For more details on available parameters, refer to the [Events: get documentation](https://developers.google.com/calendar/api/v3/reference/events/get).

### Example Usage

To get an event using the command line interface (CLI) with the specified syntax, you can use the following example:

```bash
py main.py calendar event get payload.json
```

This command will retrieve the event specified in `payload.json`. Make sure to replace `"Your API key"`, `"Your calendar ID"`, and `"Event ID to retrieve"` with your actual API key, calendar ID, and event ID respectively.
