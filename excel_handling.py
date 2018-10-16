#Example code
import xlrd
import numpy as np

datafile = "2013_ERCOT_Hourly_Load_Data.xls"


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    data = [[sheet.cell_value(r, col) 
                for col in range(sheet.ncols)] 
                    for r in range(sheet.nrows)] # make a list comprehension of values in the excel file
    
    print("\nList Comprehension")
    print("data[3][2]:", )
    print(data[3][2])

    print("\nCells in a nested loop:"    )
    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            if row == 50:
                print(sheet.cell_value(row, col),)


    ### other useful methods:
    print("\nROWS, COLUMNS, and CELLS:")
    print("Number of rows in the sheet:", ) 
    print(sheet.nrows)
    print("Type of data in cell (row 3, col 2):", )
    print(sheet.cell_type(3, 2))
    print("Value in cell (row 3, col 2):", )
    print(sheet.cell_value(3, 2))
    print("Get a slice of values in column 3, from rows 1-3:")
    print(sheet.col_values(3, start_rowx=1, end_rowx=4))

    print("\nDATES:")
    print("Type of data in cell (row 1, col 0):", )
    print(sheet.cell_type(1, 0))
    exceltime = sheet.cell_value(1, 0)
    print("Time in Excel format:",)
    print(exceltime)
    print("Convert time to a Python datetime tuple, from the Excel float:",)
    print(xlrd.xldate_as_tuple(exceltime, 0))

    return data

data = parse_file(datafile)


"""
Your task is as follows:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format

"""


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    for col in range(sheet.ncols):
        if sheet.cell_value(0, col) == 'COAST':
            coast_values = sheet.col_values(col, start_rowx=1, end_rowx=sheet.nrows+1)
            coast_col = col
    maxvalue = np.max(coast_values)
    minvalue = np.min(coast_values)
    for row in range(sheet.nrows):
        if sheet.cell_value(row, coast_col) == maxvalue:
            maxtime = sheet.cell_value(row, 0)
        if sheet.cell_value(row, coast_col) == minvalue:
            mintime = sheet.cell_value(row, 0)
    

    data = {
            'maxtime': xlrd.xldate_as_tuple(maxtime, 0),
            'maxvalue': maxvalue,
            'mintime': xlrd.xldate_as_tuple(mintime, 0),
            'minvalue': minvalue,
            'avgcoast': np.mean(coast_values)
    }
    return data

def test():
    
    data = parse_file(datafile)

    assert(data['maxtime'] == (2013, 8, 13, 17, 0, 0))
    assert(round(data['maxvalue'], 10) == round(18779.02551, 10))

print(parse_file(datafile))
test()