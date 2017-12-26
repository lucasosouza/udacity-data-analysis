#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.
In the first exercise we want you to audit the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- 'NoneType' if the value is a string "NULL" or an empty string ""
- 'list', if the value starts with "{"
- 'int', if the value can be cast to int
- 'float', if the value can be cast to float, but is not an int
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and the datatypes that can be found in the field.
All the data initially is a string, so you have to do some checks on the values first.

"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal", 
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long", 
          "areaLand", "areaMetro", "areaUrban", "postalCode"]

def audit_file(filename, fields):
    fieldtypes = {}
    #create an empty set for each field type
    for field in FIELDS:
        fieldtypes[field] = set([])
    #open the files with a csv dictreader
    with open(filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        #set conditions
        conditions = [
            (None, "value == 'NULL' or value == ''"), 
            ([], "value[0] == '{'"),
            (1, "int(value)"), 
            (1.0, "float(value)"),
            ('str', "value")
            ]
        #loop through each field and assign the condition
        for idx, row in enumerate(reader):
            if idx<3: continue 
            if idx==3: print sorted(row.keys(), key=lambda x:x[0])
            for field, value in row.iteritems():
                if field == "name": print value
                for type_val, condition in conditions:
                    try:
                        if eval(condition):
                            fieldtypes[field].add(type(type_val))
                            break
                    except: pass

    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
if __name__ == "__main__":
    test()
