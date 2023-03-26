import os
import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
SERVICE_ACCOUNT_FILE = 'spreadsheet-keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1gKEYX9yz3uabZu73AB1gxyDW6bhISGSX1ARS3R0R5wE'

try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range='Sheet1!A1:XFD1048576').execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            sys.exit(1)

        file_path = 'vault_data.txt'

        # check if the file exists
        if os.path.isfile(file_path):
            # delete the file
            os.remove(file_path)

        for row in values[1:]:
            ts=row[0]+' '+row[1]
            with open('vault_data.txt', 'a') as f:
                f.write(ts)
                f.write('\n')
       
except HttpError as err:
        print(err)




