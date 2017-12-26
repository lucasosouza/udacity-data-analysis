#!/usr/bin/env python
# -*- coding: utf-8 -*-
# So, the problem is that the gigantic file is actually not a valid XML, because
# it has several root elements, and XML declarations.
# It is, a matter of fact, a collection of a lot of concatenated XML documents.
# So, one solution would be to split the file into separate documents,
# so that you can process the resulting files as valid XML documents.

import xml.etree.ElementTree as ET
PATENTS = 'patent.data'

def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()

# what do I need to do
# read this gigantic XML file 
# transform it into a lot of bit sized files

def split_file(filename, n=0, divider = '?xml version'):
    # we want you to split the input file into separate files
    # each containing a single patent.
    # As a hint - each patent declaration starts with the same line that was causing the error
    # The new files should be saved with filename in the following format:
    # "{}-{}".format(filename, n) where n is a counter, starting from 0.
    with open(filename, 'rb') as f:
        f_out = None; line = f.readline()
        while line:
            if line.find(divider) != -1:
                if f_out: 
                    f_out.close()
                    n+=1
                f_out = open("{}-{}".format(filename, n), 'wb')
                f_out.write(line)
            else:
                f_out.write(line)
            line = f.readline() #restart     
    f_out.close()
    print "Files splitted with success"

def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print "You have not split the file {} in the correct boundary!".format(fname)
            f.close()
        except:
            print "Could not find file {}. Check if the filename is correct!".format(fname)

test()
