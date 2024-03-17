
from typing import Any, Literal
from googleapiclient.discovery import build
from red_office_google_integration.google_service.google_credentials_service import GoogleCredentialService  # noqa: E203,E402
from red_office_google_integration.src.utils import handle_exception
from red_office_google_integration.log.log_handler import logger
from red_office_google_integration.src import setting
import json

valueOption = Literal['RAW', 'USER_ENTERED']


class SpreadSheet:
    """
    A class for interacting with Google Sheets API to read, update, and append data.

    Attributes:
    - __key (bytes): The key used for authentication.
    - __service: The Google Sheets service instance.

    Methods:
    - __init__(self, key: bytes): Initializes the SpreadSheet class with the given authentication key.
    - get_data(self, spreadsheetId: str, range: str, **kwargs) -> dict: Retrieves data from a specified range in a Google Sheets spreadsheet.
    - get_batch_data(self, spreadsheetId: str, ranges: list[str], **kwargs) -> dict: Retrieves data from multiple specified ranges in a Google Sheets spreadsheet.
    - update_values(self, spreadsheetId: str, range: str, valueInputOption: str, values: list[list], **kwargs) -> dict: Updates values in a Google Sheet within the specified range.
    - batch_update_values(self, spreadsheet_id: str, valueInputOption, data: list[dict], **kwargs) -> dict: Updates multiple cells in a Google Sheet using a single batch update API call.
    - append_data(self, spreadsheetId: str, range: str, valueInputOption: str, values: list[list], **kwargs) -> dict: Appends values to a Google Sheet starting from the specified range.
    """

    def __init__(self, key: bytes) -> None:
        '''
        Initialize the CalendarEvent class.

        Args:
            key (bytes): The key used for authentication.
        '''
        self.__key = key
        self.__service = self.__build_service()

    @handle_exception
    def __build_service(self):
        '''
        Build and return the Google service.

        Returns:
            (cred): The Google service.
        '''
        cred = GoogleCredentialService(self.__key, setting.SCOPE_SPREADSHEETS,
                                       setting.FILE_NAME_SPREADSHEETS_TOKEN, setting.FILE_NAME_SPREADSHEETS_CREDENTIAL).get_service()
        return build("sheets", "v4",  credentials=cred)

    @handle_exception
    def get_data(self, spreadsheetId: str, range: str, **kwargs):
        """
        Retrieves data from a specified range in a Google Sheets spreadsheet.

        Parameters:
        - spreadsheetId (str): The ID of the spreadsheet to retrieve data from.
        - range (str): The A1 notation or R1C1 notation of the range to retrieve values from. just giving sheet name will return all the data from sheet
        - kwargs: Additional query parameters.

        Query Parameters:
        - majorDimension (enum): The major dimension that results should use.
        For example, if the spreadsheet data in Sheet1 is: A1=1,B1=2,A2=3,B2=4,
        then requesting majorDimension='ROWS' returns [[1,2],[3,4]],
        whereas requesting majorDimension='COLUMNS' returns [[1,3],[2,4]].
        `I don't prefer to use this parameter. We'll use ROW majorDimension for our proejct which is default.`

        - valueRenderOption (enum): How values should be represented in the output.
        The default render option is FORMATTED_VALUE.
        - dateTimeRenderOption (enum): How dates, times, and durations should be represented in the output.
        This is ignored if valueRenderOption is FORMATTED_VALUE.
        The default dateTime render option is SERIAL_NUMBER.

        Returns:
        - dict: A dictionary containing the retrieved values.

        Raises:
        - Exception: If there is an error while retrieving the data.
    """
        return self.__service.spreadsheets().values().get(spreadsheetId=spreadsheetId,
                                                          range=range, **kwargs).execute()

    @handle_exception
    def get_batch_data(self, spreadsheetId: str, ranges: list[str], **kwargs) -> dict:
        """
        Retrieves data from multiple specified ranges in a Google Sheets spreadsheet.

        Parameters:
        - spreadsheetId (str): The ID of the spreadsheet to retrieve data from.
        - ranges (list[str]): A list of A1 notation or R1C1 notation of the ranges to retrieve values from.
        - kwargs: Additional query parameters.

        Query Parameters:
        - majorDimension (enum): The major dimension that results should use.
        For example, if the spreadsheet data in Sheet1 is: A1=1,B1=2,A2=3,B2=4,
        then requesting majorDimension='ROWS' returns [[1,2],[3,4]],
        whereas requesting majorDimension='COLUMNS' returns [[1,3],[2,4]].
        `I don't prefer to use this parameter. We'll use ROW majorDimension for our proejct which is default.`

        - valueRenderOption (enum): How values should be represented in the output.
        The default render option is FORMATTED_VALUE.
        - dateTimeRenderOption (enum): How dates, times, and durations should be represented in the output.
        This is ignored if valueRenderOption is FORMATTED_VALUE.
        The default dateTime render option is SERIAL_NUMBER.

        Returns:
        - dict: A dictionary containing the retrieved values for each range specified.

    """
        return self.__service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId, ranges=ranges, **kwargs).execute()

    @handle_exception
    def update_values(self, spreadsheetId, range: str, valueInputOption: valueOption, values: list[list], **kwargs):
        """
            Updates values in a Google Sheet within the specified range.

            Parameters:
            - spreadsheetId (str): The ID of the spreadsheet.
            - range_ (str): The range of cells to update (A1 notation).
            - valueInputOption (str): How the input data should be interpreted. Possible values are:
                - "RAW": The values will not be parsed and will be stored as-is.
                - "USER_ENTERED": The values will be parsed as if the user typed them into the UI.
            - values (list[list]): A list of lists containing the new values for the cells.
            - kwargs: Additional keyword arguments that can be passed to the update method.

            Returns:
            - dict: A dictionary containing information about the update operation.

            Example:
            ```python
            obj = SpreadSheet(k.encode())
            values = [
                ['New Value 1'],
                ['New Value 2'],
                ['New Value 3']
            ]
            obj.update_values("spreadsheetId", "Sheet1!A1:C3", 'USER_ENTERED', values)
            ```
        """
        body = {
            'values': values
        }
        return self.__service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=range, valueInputOption=valueInputOption, body=body, **kwargs).execute()

    @handle_exception
    def batch_update_values(self, spreadsheet_id: str, valueInputOption: valueOption, data: list[dict], **kwargs) -> dict:
        """
            Updates multiple cells in a Google Sheet using a single batch update API call.

            Parameters:
            - spreadsheet_id (str): The ID of the spreadsheet.
            - valueInputOption (str): How the input data should be interpreted. Possible values are:
                - "RAW": The values will not be parsed and will be stored as-is.
                - "USER_ENTERED": The values will be parsed as if the user typed them into the UI.
            - data (list[dict]): A list of dictionaries containing update details.
                - Each dictionary should have keys:
                    - 'range' (str): The range of the cell to update (A1 notation).
                    - 'values' (list[list]): A list containing the new value for the cell.

            Returns:
            - dict: A dictionary containing the response from the batch update.

            Example:
            ```python
            data = [
                {'range': 'D15', 'values': [[2225]},
                {'range': 'F17:G17', 'values': [['Lorem test', ipsum]]},
                {'range': 'D17:E17', 'values': [['Lorem test', ipsum]]},
            ]
            obj = SpreadSheet(k.encode())
            obj.batch_update_values("spreadsheetId", 'USER_ENTERED', data)
            ```
        """

        body = {"data": data, 'valueInputOption': valueInputOption}

        res = self.__service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body, **kwargs).execute()
        return res

    @handle_exception
    def append_data(self, spreadsheetId: str, range: str, valueInputOption: valueOption, values: list[list], **kwargs) -> dict:
        """
            Appends values to a Google Sheet starting from the specified range.

            Parameters:
            - spreadsheetId (str): The ID of the spreadsheet.
            - range_ (str): The range of cells to append the values to (A1 notation).
            - valueInputOption (str): How the input data should be interpreted. Possible values are:
                - "RAW": The values will not be parsed and will be stored as-is.
                - "USER_ENTERED": The values will be parsed as if the user typed them into the UI.
            - values (list[list]): A list of lists containing the new values to append.
            - kwargs: Additional keyword arguments that can be passed to the append method.

            Returns:
            - dict: A dictionary containing information about the append operation.

            Example:
            ```python
            obj = SpreadSheet(k.encode())
            values = [
                ['New Value 1'],
                ['New Value 2'],
                ['New Value 3']
            ]
            obj.append_data("spreadsheetId", "Sheet1!A1:C3", 'USER_ENTERED', values)
            ```
        """
        body = {'values': values}
        res = self.__service.spreadsheets().values().append(
            spreadsheetId=spreadsheetId, range=range, valueInputOption=valueInputOption, body=body, **kwargs).execute()
        return res


if __name__ == '__main__':
    k = "Lb-9cbIFCUCFcKSrWqRyEvEYuHAOB6pfMLpmHbrdnNA="

    obj = SpreadSheet(k.encode())
    spreadsheetId = '1Q_cYCpmnb1XtCnm7YlCl3ZcpX_GM3IzBZRsLue2dGkc'
# ________________________get_data_tesing_________________________________________________________
    # result = obj.get_data(spreadsheetId,
    #                       'Form Responses 1', majorDimension='ROWS')
    # print(json.dumps(result, indent=2))
# _________________________________________________________________________________________________

# ________________________get_bath_data_testing___________________________________________________
    # ranges = ['Form Responses 1!A2:D7', 'Form Responses 1!E4:F5']

    # result = obj.get_batch_data(
    #     spreadsheetId, ranges)
    # print(json.dumps(result, indent=2))
# ___________________________________________________________________________________________________

# ________________________update_values_testing______________________________________________________
    # valueInputOption = "USER_ENTERED"
    # values = [['Nishchal Rai'], ['Techsage']]
    # result = obj.update_values(spreadsheetId, 'B16', valueInputOption, values)
    # print(json.dumps(result, indent=2))
# _____________________________________________________________________________________________________

# ______________________batch_update_values___________________________________________________________

    # valueInputOption = "USER_ENTERED"
    # data = [
    #     {'range': 'D15', 'values': [[2]]},
    #     {'range': 'F17:G17', 'values': [['Aadithya Sharma', 22]]},
    #     {'range': 'D17:E17', 'values': [['Nishhcal Rai', 22]]},]

    # result = obj.batch_update_values(spreadsheetId, valueInputOption, data)
    # print(json.dumps(result, indent=2))
# ______________________________________________________________________________________________________
# ________________________________________append_data____________________________________________________
    # names = ['Nishchal Rai', 'Aadithya Sharma Dahal', 'Frank Brano Gomes',
    #          'Muhammed Kaif', 'Suraksha Rai', 'Shreya Sharma', 'Vinakay Pradhan', 'Sahitya Gurung']

    # values = [[i] for i in names]

    # result = obj.append_data(
    #     spreadsheetId, 'NameList!A1', 'USER_ENTERED', values)
    # print(json.dumps(result, indent=2))
