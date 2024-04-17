# RED-OFFICE-GOOGLE-INTEGRATION
Red-Office-Google-Integration is a comprehensive package designed to simplify integration with Google APIs, specifically Calendar, Sheets, and Gmail. Originally envisioned as three separate packages, the project now offers all functionalities bundled into one, providing users with a seamless experience.

#### Features Overview
- **Calendar**: Create, list, get, and delete events in Google Calendar. Designed for extensibility to accommodate future feature additions.
- **Sheets**:
  - Insert CSV content in a defined range.
  - Replace a defined range with CSV content.
  - Get full worksheet data (and from specified ranges).
  - Replace a single cell.
  - Output data in JSON or CSV format.
- **Gmail**:
  - Get emails by label, recipient, or 'has attachment' status.
  - Archive and label emails by ID.
  - Create draft emails, with the ability to attach files.
  - Download attachments by email ID to a specified path.

#### Usage
The package is designed for ease of use, handling credentials internally. It can be utilized through a single file with a Command Line Interface (CLI), making integration straightforward and efficient.

## Contents

  1. [Setup](#setup)
  2. [Config Credentials](#config-credentials-for-calendar)
  3. [Calendar Events](#calendar-events)
  4. [Google Sheets](#google-sheet)
  5. [Google Mail](#google-mail)
## SETUP

1. **Setup Python 3.10:**
   Ensure you have Python 3.10 installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

2. **Clone the Repository:**
   Use the following command to clone the repository:
   ```shell
   git clone https://github.com/TechSage369/RED-OFFICE-GOOGLE-INTEGRATION.git
   ```

3. **Install Dependencies:**
   ```shell
   pip install -r requirement.txt
   ```
4. **CLI Commands:**
Here's the corrected version of the CLI commands section in Markdown format:

---

## CLI Commands

### List All Commands

To view a list of all available commands, use the `--help`:

### Examples

```shell
py main.py --help
```

### Calendar Commands

To view the available commands for calendar functions, use the following command:

```shell
py main.py calendar --help
```

This will display a list of commands related to calendar functions.

### Mail Commands

To view the available commands for mail functions, use the following command:

```shell
py main.py mail --help
```
This will display a list of commands related to mail functions.

---

# Initialize Credentials

please follow this link till credential creation and save to json file

[Python quickstart  |  Google Calendar  |  Google for Developers](https://developers.google.com/calendar/api/quickstart/python)


`After getting credential`

---

## Setup Credentials

To initialize your credentials, provide the credential file name. You will receive the key in the terminal (also can specify output file[optional]), which you should keep safe for later use as API_KEY.

```bash
py main.py init-cred credential_filename -o outputfilename
```

You can also use optional parameters to specify a custom key (e.g., `Lb-9cbIFCUCFcKSrWqRyEvEYuHAOB6pfMLpmHbrdnNA=`) and mention the output file path to save the key. `Fernet key 128-bit base64-encoded `

```bash
py main.py init-cred credential_filename -o outputfilename -k YOUR_SECRET_KEY
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
    "key": "YOUR_SECTER_KEY",
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
    "key": "YOUR_SECRET_KEY",
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
    "key": "Your SECRET key",
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
    "key": "Your SECRET key",
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

___

# Google Sheet
The following operations are supported for calendar events:
- [Get Data](#get-data)
- [Get Batch Data](#get-batch-data)
- [Update Value](#update-values)
- [Batch Update Values](#batch-update-values)
- [Append Data](#append-data)

### Get Data


This command retrieves data from a specified range in a Google Sheets spreadsheet.

```bash
py main.py spreadsheet get-data [payload] [-o/--output OUTPUT]
```

#### Arguments

- `payload` (str): Path to a JSON file or a valid JSON string containing the following parameters:
  - `key` (str): The Google API key for accessing the spreadsheet.
  - `spreadsheetId` (str): The ID of the Google Sheets spreadsheet.
  - `range` (str): The range of cells to retrieve data from (e.g., "Sheet1!A1:B2").
  - `optionals` (dict, optional): Additional optional parameters for retrieving data, such as `"majorDimension": "ROWS"`.

#### Options

- `-o/--output` (str): Path to the output directory where the retrieved data will be saved (optional).

#### Example Payload

```json
{
    "key": "YOUR_SECRET_KEY",
    "spreadsheetId": "SPREADSHEET",
    "range": "Form Responses 1",
    "optionals": {
        "majorDimension": "ROWS"
    }
}
```

#### Examples

1. Retrieve data from a Google Sheets spreadsheet and print it to the console:

   ```bash
   py main.py spreadsheet get-data payload.json
   ```

2. Retrieve data from a Google Sheets spreadsheet and save it to a file:

   ```bash
   py main.py spreadsheet get-data payload.json -o output_dir
   ```

### Get Batch Data

This command retrieves data from a multiple range in a Google Sheets spreadsheet.

```bash
py main.py spreadsheet get-batch-data [payload] [-o/--output OUTPUT]
```


#### Arguments

- `payload` (str): Path to a JSON file or a valid JSON string containing the following parameters:
  - `key` (str): The Google API key for accessing the spreadsheet.
  - `spreadsheetId` (str): The ID of the Google Sheets spreadsheet.
  - `ranges` (str): The list of range of cells to retrieve data from.
  - `optionals` (dict, optional): Additional optional parameters for retrieving data, such as `"majorDimension": "ROWS"`.

#### Options

- `-o/--output` (str): Path to the output directory where the retrieved data will be saved (optional).

#### Example Payload

```json
{
    "key": "YOUR_SECRET_KEY",
    "spreadsheetId": "SPREADSHEET",
    "ranges": [
        "Form Responses 1!A2:D7",
        "Form Responses 1!E4:F5"
    ],
    "optionals": {
    }
}
```

### Update Values

This command update values to specifed range in spreadsheet.

```bash
py main.py spreadsheet update-values [payload]
```


#### Arguments

- `payload` (str): Path to a JSON file or a valid JSON string containing the following parameters:
  - `key` (str): The Google API key for accessing the spreadsheet.
  - `spreadsheetId` (str): The ID of the Google Sheets spreadsheet.
  - `range` (str): The range of cells to retrieve data from (e.g., "Sheet1!A1:B2").
  - `valueInputOption`: default is `USER_ENTERED`
  - `values `: list of values
  - `optionals` (dict, optional): Additional optional parameters..



#### Example Payload

```json
{
    "key": "YOUR-SECRET-KEY",
    "spreadsheetId": "SPREADSHEET",
    "range": "Form Responses 1!B16",
    "valueInputOption": "USER_ENTERED",
    "values": [
        [
            "Nishchal Rai"
        ],
        [
            "Techsage"
        ]
    ],
    "optionals": {}
}
```


### Batch Update Values

This command update multiple values to multiple range in spreadsheet.

```bash
py main.py spreadsheet batch-update-values [payload]
```


#### Arguments

- `payload` (str): Path to a JSON file or a valid JSON string containing the following parameters:
  - `key` (str): The Google API key for accessing the spreadsheet.
  - `range` (str): The range of cells to retrieve data from (e.g., "Sheet1!A1:B2").
  - `valueInputOption`: default is `USER_ENTERED`
  - `data`: data is list of dict which contains ranges and values
  - `optionals` (dict, optional): Additional optional parameters.



#### Example Payload

```json
{
    "key": "Lb-9cbIFCUCFcKSrWqRyEvEYuHAOB6pfMLpmHbrdnNA=",
    "spreadsheetId": "1Q_cYCpmnb1XtCnm7YlCl3ZcpX_GM3IzBZRsLue2dGkc",
    "valueInputOption": "USER_ENTERED",
    "data": [
        {
            "range": "D15",
            "values": [
                [
                    2
                ]
            ]
        },
        {
            "range": "F17:G17",
            "values": [
                [
                    "Aadithya Sharma",
                    22
                ]
            ]
        },
        {
            "range": "D17:E17",
            "values": [
                [
                    "Nishhcal Rai",
                    22
                ]
            ]
        }
    ],
    "optionals": {}
}
```

### Append Data

This command append data in specified range `It will not replace the existing data, rather it appends to given range. If data already exists,then it will append just below the existing data`

```bash
py main.py spreadsheet append-data [payload]
```


#### Arguments

- `payload` (str): Path to a JSON file or a valid JSON string containing the following parameters:
  - `key` (str): The Google API key for accessing the spreadsheet.
  - `range` (str): The range of cells to retrieve data from (e.g., "Sheet1!A1:B2").
  - `valueInputOption`: default is `USER_ENTERED`
  - `values`: list of values
  - `optionals` (dict, optional): Additional optional parameters.



#### Example Payload

```json
{
    "key": "Lb-9cbIFCUCFcKSrWqRyEvEYuHAOB6pfMLpmHbrdnNA=",
    "spreadsheetId": "1Q_cYCpmnb1XtCnm7YlCl3ZcpX_GM3IzBZRsLue2dGkc",
    "range": "Form Responses 1!A16",
    "valueInputOption": "USER_ENTERED",
    "values": [
        [
            "Nishchal Rai"
        ],
        [
            "Aadithya Sharma Dahal"
        ],
        [
            "Frank Brano Gomes"
        ],
        [
            "Muhammed Kaif"
        ],
        [
            "Suraksha Rai"
        ],
        [
            "Shreya Sharma"
        ],
        [
            "Vinakay Pradhan"
        ],
        [
            "Sahitya Gurung"
        ]
    ],
    "optionals": {}
}
```


## Google Mail

The Google Gmail CLI provides a command-line interface for interacting with Gmail. It allows you to perform various actions such as creating drafts, retrieving emails, downloading attachments, and listing emails based on query parameters. This tool is useful for automating email-related tasks and integrating Gmail functionality into your scripts or workflows.

The following options are supported by google mail:
- [Creade Draft](#create-draft-command)
- [Get mail](#get-email-command)
- [Download Attachment](#download-attachment-command)
- [Get List of Mails](#get-email-list-command)

### Create Draft Command

The `create_draft` command is used to create a draft email in your Gmail account. It takes a payload containing email details and an optional attachment file.

```bash
py main.py mail create_draft [payload] [-a/--attachment ATTACHMENT]
```

- `[payload]`: Path to a JSON file or a valid JSON string containing email details.
- `[-a/--attachment ATTACHMENT]` (optional): Path to an attachment file to include in the email.

Example:
```bash
py main.py mail create_draft payload.json -a attachment.pdf
```
`You can also give multiple attachment path`
```bash
py main.py mail create_draft payload.json -a attachment.pdf -a another.docx
```

Sample Payload:
```json
{
    "key": "Lb-9cbIFCUCFcKSrWqRyEvEYuHAOB6pfMLpmHbrdnNA=",
    "header": {
        "To": "maria123@gmail.com",
        "Subject": "Just sending random message to Maria"
    },
    "body": "<b>Hi Maria How are you? I hope you are well.</b>",
    "subtype": "html"
}
```
`default subtype is plain text`


### Get Email Command

The `get_email` command retrieves an email from your Gmail account based on the provided payload.

```bash
py main.py mail get_email [payload]
```

- `[payload]`: Path to a JSON file or a valid JSON string containing email details.

Example:
```bash
py main.py mail get_email payload.json
```
sample Payload
```json
{
    "key": "Lb-9cbIFCUCFcKSrWqRyEvEYuHAOB6pfMLpmHbrdnNA=",
    "messageId": "18d3a6ee55dcbded",
    "optionals": {}
}
```
### Download Attachment Command

The `download_attachment` command downloads an attachment from a specific email in your Gmail account.

```bash
py main.py mail download_attachment [payload] [-o/--output OUTPUT]
```

- `[payload]`: Path to a JSON file or a valid JSON string containing email details.
- `[-o/--output OUTPUT]`: Path to the output directory where the attachment will be saved.

Example:
```bash
py main.py mail download_attachment payload.json -o output_dir
```

sample payload
```json
{
    "key": "Lb-9cbIFCUCFcKSrWqRyEvEYuHAOB6pfMLpmHbrdnNA=",
    "messageId": "18e2d871a1f36de7"
}
```

### Get Email List Command

The `get_email_list` command lists emails from your Gmail account based on query parameters.

```bash
py main.py mail get_email_list [payload]
```

- `[payload]`: Path to a JSON file or a valid JSON string containing query parameters.

Example:
```bash
py main.py mail get_email_list payload.json
```

sample Payload:
```json
{
    "key": "Lb-9cbIFCUCFcKSrWqRyEvEYuHAOB6pfMLpmHbrdnNA=",
    "query": "has:attachment to:6sigmainstitute@gmail.com",
    "optionals": {}
}
```
---

`NOTE: To get more details on optional you check google api documention for specific action`
