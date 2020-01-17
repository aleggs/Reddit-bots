import gspread
from oauth2client.service_account import ServiceAccountCredentials
from helpers import all_in_one
from pprint import pprint
scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
spreadsheet_id = '1B27_j9NDPU3cNlj2HKcrfpJKHkOf-Oi1DbuuQva2gT4'
creds = ServiceAccountCredentials.from_json_keyfile_name('creds_secret.json', scope)


def main():
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(spreadsheet_id)
    wks = sh.sheet1

    brands = wks.col_values(1)
    brands = all_in_one(brands)

    models = wks.col_values(2)
    models = all_in_one(models)

    print("Completed one loop!")
    return (brands, models)

def lookup_row(brand, model):
    if not brand or not model: # if either does not exist
        print("Error")
        return
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.sheet1

    row = -1
    brand_rows = [cell.row for cell in worksheet.findall(brand)]
    model_rows = [cell.row for cell in worksheet.findall(model)]

    for num in brand_rows:
        if num in model_rows:
            row = num
    
    return row