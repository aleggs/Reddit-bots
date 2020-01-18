import gspread
from oauth2client.service_account import ServiceAccountCredentials
from helpers import all_in_one
from pprint import pprint
scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
spreadsheet_id = '1B27_j9NDPU3cNlj2HKcrfpJKHkOf-Oi1DbuuQva2gT4'
creds = ServiceAccountCredentials.from_json_keyfile_name('creds_secret.json', scope)

col_controller = 6 #F
col_dram = 8 #H
col_nandtype = 11 #K
col_categories = 15 #O


def main():
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(spreadsheet_id)
    wks = sh.sheet1

    brands = wks.col_values(1)
    brands = all_in_one(brands)

    models = wks.col_values(2)
    models = all_in_one(models)

    return (brands, models)

def lookup(brand, model):
    
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(spreadsheet_id)
    wks = sh.sheet1

    row = -1
    brand_rows = [cell.row for cell in wks.findall(brand)]
    model_rows = [cell.row for cell in wks.findall(model)]

    for num in brand_rows:
        if num in model_rows:
            row = num
    controller = wks.cell(row, col_controller).value
    dram = wks.cell(row, col_dram).value
    nandtype = wks.cell(row, col_nandtype).value
    category = wks.cell(row, col_categories).value

    return controller, dram, nandtype, category
    


