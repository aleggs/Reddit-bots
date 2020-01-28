import gspread, helpers
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
spreadsheet_id = '1B27_j9NDPU3cNlj2HKcrfpJKHkOf-Oi1DbuuQva2gT4'
creds = ServiceAccountCredentials.from_json_keyfile_name('creds_secret.json', scope)

# Define column locations from spreadsheet
controller_col = 6 #F
dram_col = 8 #H
nand_col = 11 #K
category_col = 15 #O


def auth():
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(spreadsheet_id)
    wks = sh.sheet1
    return (gc, sh, wks)


def brands_and_models():
    gc, sh, wks = auth()
    brands = helpers.all_in_one(wks.col_values(1))
    models = helpers.all_in_one(wks.col_values(2))
    return brands, models


def lookup(brand, model):
    gc, sh, wks = auth()
    # searches for and finds the cells that match brand and model
    row = -1
    brand_rows = [cell.row for cell in wks.findall(brand)]
    model_rows = [cell.row for cell in wks.findall(model)]
    for num in brand_rows:
        if num in model_rows:
            row = num
    # once the cell is found, get the values from desired cells
    controller = wks.cell(row, controller_col).value
    dram = wks.cell(row, dram_col).value
    nandtype = wks.cell(row, nand_col).value
    category = wks.cell(row, category_col).value

    return controller, dram, nandtype, category
    


