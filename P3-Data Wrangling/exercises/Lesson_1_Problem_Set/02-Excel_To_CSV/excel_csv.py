# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.
import xlrd
import os
import csv
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data"
outfile = "2013_Max_Loads.csv"

def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()

def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    headers=['Station','Year','Month','Day','Hour','Max Load']
    data = [headers]
    regions = sheet.row_values(0)[1:-1] #eliminate first and last column
    #create each object and push to data
    for idx, region in enumerate(regions):
        values = sheet.col_values(idx+1, start_rowx=1)
        max_load = max(values)
        max_time = xlrd.xldate_as_tuple(sheet.cell_value(values.index(max_load)+1, 0),0)
        data.append([region,max_time[0],max_time[1],max_time[2],max_time[3],max_load])

    return data

def save_file(data, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f, delimiter="|")
        for row in data:
            writer.writerow(row)
    
def test():
    open_zip(datafile)
    data = parse_file('{0}.xls'.format(datafile))
    save_file(data, outfile)

    ans = {'FAR_WEST': {'Max Load': "2281.2722140000024", 'Year': "2013", "Month": "6", "Day": "26", "Hour": "17"}}
    
    fields = ["Year", "Month", "Day", "Hour", "Max Load"]
    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            st = line["Station"]
            if st == 'FAR_WEST':
                for field in fields:
                    assert ans[st][field] == line[field]

        
test()