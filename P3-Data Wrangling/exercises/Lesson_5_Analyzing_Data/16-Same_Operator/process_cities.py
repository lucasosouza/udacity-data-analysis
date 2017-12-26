#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zipfile import ZipFile
import csv
from pymongo import MongoClient
import codecs
from pprint import pprint

import sys
print sys.getdefaultencoding()
# reload(sys)
# sys.setdefaultencoding('utf-8')
# print sys.getdefaultencoding()

client = MongoClient('localhost:27017')
db = client['infobox']['cities']
db.drop()

def set_none(x):
	if x == "NULL" or x == ["NULL"]:
		return None
	return x

def parse_array(x):
	if x[0] == "{" and x[-1] == "}":
		return x[1:-1].split("|")
	return [x]

def to_int(x):	
	if x:
		if x[0] == "{": 
			return int(max(parse_array(x))) 
		return int(x)
	return None

def to_float(x):	
	if x and not x=="NULL":
		if x[0] == "{": 
			return float(max(parse_array(x))) 
		return float(x)
	return None

#forcing a conversion to utf-8, ignoring whatever is not recognized
def decode(data):
	convert = lambda x: x.decode('utf-8', 'ignore')
	if type(data) == list: 
		return map(convert, data)
	elif type(data) == str:
		return convert(data)
	else:
		return data


with open('cities.csv', 'rb') as f:
	reader = csv.DictReader(f)
	for idx, row in enumerate(reader):
		if idx < 3: continue
		#if idx < 120 and idx > 100: pprint(row) 
		item = {}
		item['country'] = set_none(row['country'].split("/")[-1])
		item['city'] = set_none(parse_array(row['name'])[0])
		item['latitude'] = to_float(row['wgs84_pos#lat'])
		item['longitude'] = to_float(row['wgs84_pos#long'])
		item['isPartOf'] = set_none(parse_array(row['isPartOf_label']))
		item['population'] = to_int(set_none(row['populationTotal']))
		try:
			db.insert(item)
		except:
			#if item['country'] == 'Brazil': pprint(item)
			item = {k:decode(v) for k,v in item.items()}
			db.insert(item)

#data is not valid utf-8

#zf.extractall()
#with ZipFile("cities.csv.zip", 'r') as zf:
#	zf.extractall	
#with zf.open(zf.namelist()[0]) as f:
#with open(zf.namelist()[0], 'rb') as f:


