#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle
enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))
import os
import sys
sys.path.append('../final_project')
from poi_email_addresses import poiEmails 

#let's do some cleverness 
#what it will consist of?
#convert a dictionary into a np array

import numpy as np
import pandas as pd

data = enron_data.values()
names = enron_data.keys()
for i in range(len(names)): 
	data[i]['name'] = names[i]

df = pd.DataFrame.from_dict(data)
#df.loc[df['name'].str.match(r'SKILLING')]
import pdb;pdb.set_trace()

