import gspread
from oauth2client.service_account import ServiceAccountCredentials
from helpers import all_in_one
from pprint import pprint

scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
spreadsheet_id = '1B27_j9NDPU3cNlj2HKcrfpJKHkOf-Oi1DbuuQva2gT4'
creds = ServiceAccountCredentials.from_json_keyfile_name('creds_secret.json', scope)

# columns on the spreadsheet
col_controller = 6 #F
col_dram = 8 #H
col_nandtype = 11 #K
col_categories = 15 #O

def brands_and_models():
    gc, sh, ws = auth()
    brands = all_in_one(ws.col_values(1))
    models = all_in_one(ws.col_values(2))

    return brands, models


def auth():
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(spreadsheet_id)
    ws = sh.sheet1
    return (gc, sh, ws)


def lookup(brand, model):
    gc, sh, ws = auth()
    # searches for and finds the cells that match brand and model
    row = -1
    brand_rows = [cell.row for cell in ws.findall(brand)]
    model_rows = [cell.row for cell in ws.findall(model)]
    for num in brand_rows:
        if num in model_rows:
            row = num
    # once the cell is found, get the values from desired cells
    controller = ws.cell(row, col_controller).value
    dram = ws.cell(row, col_dram).value
    nandtype = ws.cell(row, col_nandtype).value
    category = ws.cell(row, col_categories).value

    return controller, dram, nandtype, category
    


