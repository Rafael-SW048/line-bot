# from __future__ import print_function
# import pickle
# import os.path
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2 import service_account

from sheetfu import SpreadsheetApp

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'keys.json'


CREDS = None
CREDS = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1OSZXvGldMHw4fgkMMinsAv0L19W_U_8ZmFVVz-DFohw'
# SAMPLE_RANGE_NAME = 'B1:F'

service = SpreadsheetApp(SERVICE_ACCOUNT_FILE)
file = service.open_by_id(spreadsheet_id=SPREADSHEET_ID)
sheat = file.get_sheet_by_name('test-sheet')
result = sheat.get_data_range()
values = result.get_values()
print(values)


# try:
#     service = build('sheets', 'v4', credentials=CREDS)

#     # Call the Sheets API
#     sheet = service.spreadsheets()
#     result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
#                                 range=SAMPLE_RANGE_NAME).execute()
#     values = result.get('values', [])

#     if not values:
#         print('No data found.')

#     else:
#         print(values)
# except HttpError as err:
#     print(err)