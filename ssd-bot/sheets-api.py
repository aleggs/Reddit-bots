from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
from helper_functions import *


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

spreadsheet_id = '1B27_j9NDPU3cNlj2HKcrfpJKHkOf-Oi1DbuuQva2gT4'
g_range = 'Master List!A:S'

def main():
    
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

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    
    # gets the values from "Brands" column (column A) and filters out duplicates
    brands = sheet.values().get(spreadsheetId = spreadsheet_id, range = 'A2:A190').execute()
    brands = remove_dupes(flatten(brands['values']))
    brand_filter = list_to_alnum(brands)


    # result = sheet.values().get(spreadsheetId=spreadsheet_id).execute()
    # values = result.get('values', [])

    # if not values:
    #     print('No data found.')
    # else:
    #     print('Name, Major:')
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         print('%s, %s' % (row[0], row[4]))

if __name__ == '__main__':
    main()


# brands = service.spreadsheet().values().get('A')