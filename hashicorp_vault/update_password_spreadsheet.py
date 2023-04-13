import os.path
import os
import sys
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
load_dotenv()
SPREADSHEET_ID = os.getenv("PASSWORD_SPREADSHEET_ID")
SAMPLE_RANGE_NAME = 'Sheet1!A1:XFD1048576'
creds = None
if os.path.exists('password_sheet_token.json'):
    creds = Credentials.from_authorized_user_file('password_sheet_token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret_oauth.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open('password_sheet_token.json', 'w') as token:
        token.write(creds.to_json())




user_name = sys.argv[1]
user_pass = sys.argv[2]
try:
        service = build('sheets', 'v4', credentials=creds)
        
        values = [
            [user_name, user_pass]
        ]
        request = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption='USER_ENTERED', body={'values': values})
        response = request.execute()
       
except HttpError as err:
        print(err)




