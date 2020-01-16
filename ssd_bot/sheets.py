# Google's shit
import pickle, os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# my shit
from helpers import all_in_one
import gspread

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

spreadsheet_id = '1B27_j9NDPU3cNlj2HKcrfpJKHkOf-Oi1DbuuQva2gT4'
g_range = 'Master List!A:S'

class Credentials(object):
    def __init__(self, access_token = None):
        self.access_token = access_token
    def refresh(self, http):
        access_token = auth()

def auth():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def main():
    creds = auth()

    # creds = None
    # if os.path.exists('token.pickle'):
    #     with open('token.pickle', 'rb') as token:
    #         creds = pickle.load(token)
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     with open('token.pickle', 'wb') as token:
    #         pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    
    # gets the values from "Brands" column (A) and removes dupes, flattens the list, and removes spaces and special characters
    brands = sheet.values().get(spreadsheetId=spreadsheet_id, range='A2:A250').execute()
    brands = all_in_one(brands['values'])

    # gets the values from "Models" column (B) and removes dupes, flattens the list, and removes spaces and special characters
    models = sheet.values().get(spreadsheetId=spreadsheet_id, range='B2:B250').execute()
    models = all_in_one(models['values'])

    return (brands, models)

if __name__ == '__main__':
    main()


def lookup(brand, model):
    creds = Credentials(auth())
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.sheet1

    cells = worksheet.findall(brand)
    print(cells)
# brands = service.spreadsheet().values().get('A')