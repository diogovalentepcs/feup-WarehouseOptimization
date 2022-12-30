import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pyasn1.type.univ import Null
import pandas as pd
#from gspread.models import Cell

# Google Spreadsheet Class
class GSH(): 

    ##########################################
    # Default Values
    #########################################
    _SCOPE = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    MODULE_PATH = os.path.abspath(__file__)
    MODULE_DIRECTORY = '/'.join(MODULE_PATH.split('/')[:-1])
    _JSON_GOOGLE_KEY = 'gsheet.json'
    _CLIENT = Null

    #########################################
    # Constructor and Destroyer
    #########################################
    def __init__(self):
        print(f"Initializing Google Spreadheet Connector: {self._JSON_GOOGLE_KEY}")
            # use creds to create a client to interact with the Google Drive API
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.MODULE_DIRECTORY + '/' + self._JSON_GOOGLE_KEY, self._SCOPE)
        self._CLIENT = gspread.authorize(creds)
    
    def __del__(self):
        pass


    def getSheet(self, workbook, worksheet):
        # Find a workbook by name
        spreadsheet = self._CLIENT.open(workbook)
        # Selecting Sheet by name
        sheet = spreadsheet.worksheet(worksheet)
        return sheet

    def generateDataframe(self, workbook, worksheet):
        # Find a workbook by name
        spreadsheet = self._CLIENT.open(workbook)
        # Selecting Sheet by name
        sheet = spreadsheet.worksheet(worksheet)
        all_rows = sheet.get_all_values()
        columns = all_rows.pop(0)
        df = pd.DataFrame(all_rows,columns=columns)
        return df
    
    def updateCell(self, workbook, worksheet, row, column, value):
        sheet = self.getSheet(workbook, worksheet)
        sheet.update_cell(row, column, value)
        return True

    
    def insertHashRow(self, hash ,workbook, worksheet, n_columns):
        # Extract and print all of the values
        sheet = self.getSheet(workbook, worksheet)
        list_of_hashes = sheet.get_all_records()

        # Insert row to last row
        index = len(list_of_hashes) + 2 # Must add header row AND new row
        row = []

        for key in hash.keys():
                row.append(hash[key])

        cells = []
        n_columns += 1
        # Add values to last row (does not insert row, only alters values of empty cells)
        for column in range(1, n_columns):
            cells.append(Cell(row = index, col = column, value = row[column-1]))
        sheet.update_cells(cells) 
        
        # Insert row with values        
        #sheet.insert_row(row, index)

    def insertTest(self):
        row = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        sheet = self.getSheet("SMARTRACE", "00-RollCreation")
        list_of_hashes = sheet.get_all_records()
        index = len(list_of_hashes) + 2
        cells = []
        for column in range(1, 12):
            cells.append(Cell(row = index, col = column, value = row[column-1]))
        sheet.update_cells(cells)
