# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
import numpy as np

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    max_load = []
    max_time = []
    stations = []
    for col in range(1, sheet.ncols-1):
        stations.append(sheet.cell_value(0, col))
        load = np.max(sheet.col_values(col, start_rowx=1, end_rowx=sheet.nrows+1))
        max_load.append(load)
        for row in range(sheet.nrows):
            if sheet.cell_value(row, col) == max_load[col-1]:
                time = sheet.cell_value(row, 0)
                max_time.append(list(xlrd.xldate_as_tuple(time, 0)))
    
    columns = ['Station', 'Max Load', 'Year', 'Month', 'Day', 'Hour']

    data = []
    for i in range(len(max_load)):
        max_data = [stations[i], max_load[i]] + max_time[i][0:4]
        subdata = {}
        for k in range(len(columns)):
            subdata[columns[k]] = max_data[k]
        data.append(subdata)
    return data

def save_file(data, filename):
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(data[0].keys()))
        writer.writeheader()
        for row in data:
            writer.writerow(row)



def test():
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of)
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)

        
if __name__ == "__main__":
    data = parse_file(datafile)
    print(data)
    save_file(data, outfile)
    test()

