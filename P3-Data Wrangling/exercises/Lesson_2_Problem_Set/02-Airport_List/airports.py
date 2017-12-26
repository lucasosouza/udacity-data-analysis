#!/usr/bin/env python
# -*- coding: utf-8 -*-
# All your changes should be in the 'extract_airports' function
# It should return a list of airport codes, excluding any combinations like "All"

from bs4 import BeautifulSoup
html_page = "options.html"

def extract_airports(page):
    data = []
    with open(page, "r") as html:
        soup = BeautifulSoup(html)
        data = soup.find(id="AirportList").find_all("option")
        data = map(lambda x:x["value"], data)
        data = filter(lambda x:x.find("All")==-1, data)
    return data

def test():
    data = extract_airports(html_page)
    assert len(data) == 15
    assert "ATL" in data
    assert "ABR" in data

test()