#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
"""

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}
 

"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    node["pos"] = []
    node["created"] = {}
    node["address"] = {}
    node["node_refs"] = []
    #you should process only 2 types of top level tags: "node" and "way"
    if element.tag == "node" or element.tag == "way" :
        node["type"] = element.tag

        #process subnodes
        for subnode in element.iter():
            if subnode.tag == "tag":
                key = subnode.attrib["k"]
                value = subnode.attrib["v"]
                # tag "k" value contains problematic characters, it should be ignored
                if re.search(problemchars, key): 
                    continue
                # if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
                # if there is a second ":" that separates the type/direction of a street, the tag should be ignored, for example
                elif key[:5] == "addr:" and key[5:].find(":") < 0:
                    node["address"][key[5:]] = value
                # tag "k" value does not start with "addr:", but contains ":", you can process it same as any other tag
                elif key.find(":") > 0:
                    node[key] = value
            # for "way" specifically should be turned into "node_refs": ["305896090", "1719825889"]
            if subnode.tag == "nd" and element.tag == "way": 
                node["node_refs"].append(subnode.attrib["ref"])

        #process attributes
        for key, value in element.attrib.items():
            # attributes for latitude and longitude should be added to a "pos" array, for use in geospacial indexing. 
            # make sure the values inside "pos" array are floats and not strings. 
            if key == "lat":
                node["pos"].insert(0, float(value))
            elif key =="lon":
                node["pos"].insert(1, float(value))
            # attributes in the CREATED array should be added under a key "created" - haven't seen yet
            elif key in CREATED:
                node["created"][key] = value
            # all attributes of "node" and "way" should be turned into regular key/value pairs
            else:
                node[key] = value

        # #test print
        # if len(node["address"]) > 0: 
        #     print node
        node = {k:v for k,v in node.items() if v}
        return node

    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('map.osm', False)
    #pprint.pprint(data)  
    
    correct_first_elem = {
        "id": "261114295", 
        "visible": "true", 
        "type": "node", 
        "pos": [41.9730791, -87.6866303], 
        "created": {
            "changeset": "11129782", 
            "user": "bbmiller", 
            "version": "7", 
            "uid": "451048", 
            "timestamp": "2012-03-28T18:31:23Z"
        }
    }
    assert data[0] == correct_first_elem
    assert data[-1]["address"] == {
                                    "street": "West Lexington St.", 
                                    "housenumber": "1412"
                                      }
    assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369", 
                                    "2199822370", "2199822284", "2199822281"]

if __name__ == "__main__":
    test()