import os.path
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
load_dotenv()
SPREADSHEET_ID = os.getenv("USER_SPREADSHEET_ID")
SAMPLE_RANGE_NAME = 'Sheet1!A1:XFD1048576'
creds = None
if os.path.exists('user_sheet_token.json'):
    creds = Credentials.from_authorized_user_file('user_sheet_token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret_oauth.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open('user_sheet_token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    

    file_path = 'vault_data.txt'
    if os.path.isfile(file_path):
        os.remove(file_path)

    for row in values[1:]:
        data=row[0]+' '+row[1]
        with open('vault_data.txt', 'a') as f:
            f.write(data)
            f.write('\n')
except HttpError as err:
        print(err)


