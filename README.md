# Google Calendar API for Node-RED

## Description

This project is designed to interact with the Google Calendar API with special consideration for Node-RED. It provides a custom node for Node-RED that allows users to perform various operations, such as adding events, updating events, deleting events, and listing events. The project abstracts internal credential validation to simplify usage for the outer function.

## Setup

1. Go to the Google Calendar API and get credentials. Paste them into the `modules/secrets` directory with the file name `credentials.json`. For more details, refer to [Python quickstart | Google Calendar | Google for Developers](https://developers.google.com/calendar/api/quickstart/python).

## Example

bashCopy code

`py list_event.py < payload.json`

Note: See the samples for proper usage.