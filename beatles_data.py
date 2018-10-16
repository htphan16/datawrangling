# Your task is to read the input DATAFILE line by line, and for the first 10 lines (not including the header)
# split each line on "," and then for each line, create a dictionary
# where the key is the header title of the field, and the value is the value of that field in the row.
# The function parse_file should return a list of dictionaries,
# each data line in the file being a single list entry.
# Field names and values should not contain extra whitespace, like spaces or newline characters.
# You can use the Python string method strip() to remove the extra whitespace.
# You have to parse only the first 10 data lines in this exercise,
# so the returned list should have 10 entries!
import os
import csv
import pprint as pp
DATADIR = ""
DATAFILE = "beatles-diskography.csv"


def parse_file(datafile):
    f = open(datafile, "r")
    first = f.readline().split(',')
    data = []
    for line in f:
        subdata = {}
        for i in range(len(first)):
            subdata[first[i].strip('\n')] = line.split(',')[i].strip('"').strip(' ').strip('\n')
        data.append(subdata)
    return data


def test():
    # a simple test of your implemetation
    #datafile = os.path.join(DATADIR, DATAFILE)
    d = parse_file("beatles-diskography.csv")
    firstline = {'Title': 'Please Please Me', 'Released': '22 March 1963', 'Label': 'Parlophone(UK)', 'UK Chart Position': '1', 'US Chart Position': '-', 'RIAA Certification': 'Platinum', 'BPI Certification': 'Gold'}
    tenthline = {'Title': '', 'Released': '10 July 1964', 'Label': 'Parlophone(UK)', 'UK Chart Position': '1', 'US Chart Position': '-', 'RIAA Certification': '', 'BPI Certification': 'Gold'}

    assert(d[0] == firstline)
    assert(d[9] == tenthline)

#print(parse_file("beatles-diskography.csv"))
test()

def better_parse_file(datafile):
    data = []
    f = open(datafile, "r")
    r = csv.DictReader(f)
    for line in r:
        data.append(line)
    return data

pp.pprint(parse_file("beatles-diskography.csv"))
pp.pprint(better_parse_file("beatles-diskography.csv"))

