from bs4 import BeautifulSoup
import requests
import json

def options(soup, id):
	option_values = []
	carrier_list = soup.find(id=id)
	for option in carrier_list.find_all("option"):
		if "All" not in option["value"]:
			option_values.append(option["value"])
	return option_values

def print_list(label, codes):
	print(label)
	for c in codes:
		print(c)

html_page = "boston_logan_data.htm"

file = open(html_page, "r")
soup = BeautifulSoup(file, "lxml")
carriers = options(soup, "CarrierList")
#print_list("Carriers", carriers)
airports = options(soup, "AirportList")
#print_list("Airport", airports)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Please note that the function "make_request" is provided for your reference only.
# You will not be able to to actually use it from within the Udacity web UI.
# Your task is to process the HTML using BeautifulSoup, extract the hidden
# form field values for "__EVENTVALIDATION" and "__VIEWSTATE" and set the appropriate
# values in the data dictionary.
# All your changes should be in the "extract_data" function


def extract_data(page):
    data = {"eventvalidation": "",
            "viewstate": ""}
    with open(page, "r") as html:
    	soup = BeautifulSoup(html, "lxml")
    	data["eventvalidation"] = soup.find(id = "__EVENTVALIDATION")["value"]
    	data["viewstate"] = soup.find(id = "__VIEWSTATE")["value"]
    	data["carrier"] = carriers
    	data["airport"] = airports
    	
    return data

#print(extract_data(html_page))

def make_request(data):
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]
    airport = data["airport"]
    carrier = data["carrier"]

    r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={"AirportList": airport,
                          "CarrierList": carrier,
                          "Submit": "Submit",
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate
                    })

    return r.text


"""s = requests.Session()
r = s.get("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2")
soup = BeautifulSoup(r.text, "lxml")
viewstate = soup.find(id = "__VIEWSTATE")["value"]
viewstategenerator = soup.find(id = "__VIEWSTATEGENERATOR")["value"]
eventvalidation = soup.find(id = "__EVENTVALIDATION")["value"]

r = s.post("https://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
           data = (
                   ("__EVENTTARGET", ""),
                   ("__EVENTARGUMENT", ""),
                   ("__VIEWSTATE", viewstate),
                   ("__VIEWSTATEGENERATOR",viewstategenerator),
                   ("__EVENTVALIDATION", eventvalidation),
                   ("CarrierList", "DL"),
                   ("AirportList", "ATL"),
                   ("Submit", "Submit")
                  ))

f = open("DL-ATL.html", "w")
f.write(r.text)"""



"""
Let"s assume that you combined the code from the previous 2 exercises with code
from the lesson on how to build requests, and downloaded all the data locally.
The files are in a directory "data", named after the carrier and airport:
"{}-{}.html".format(carrier, airport), for example "FL-ATL.html".

The table with flight info has a table class="dataTDRight". Your task is to
use "process_file()" to extract the flight data from that table as a list of
dictionaries, each dictionary containing relevant data from the file and table
row. This is an example of the data structure you should return:

data = [{"courier": "FL",
         "airport": "ATL",
         "year": 2012,
         "month": 12,
         "flights": {"domestic": 100,
                     "international": 100}
        },
         {"courier": "..."}
]

Note - year, month, and the flight data should be integers.
You should skip the rows that contain the TOTAL data for a year.

There are couple of helper functions to deal with the data files.
Please do not change them for grading purposes.
All your changes should be in the "process_file()" function.

The "data/FL-ATL.html" file in the tab above is only a part of the full data,
covering data through 2003. The test() code will be run on the full table, but
the given file should provide an example of what you will get.
"""

f = "DL-ATL.html"

def process_file(f):
    """
    This function extracts data from the file given as the function argument in
    a list of dictionaries. This is example of the data structure you should
    return:

    data = [{"courier": "FL",
             "airport": "ATL",
             "year": 2012,
             "month": 12,
             "flights": {"domestic": 100,
                         "international": 100}
            },
            {"courier": "..."}
    ]


    Note - year, month, and the flight data should be integers.
    You should skip the rows that contain the TOTAL data for a year.
    """
    data = []
    info = {}
    info["courier"], info["airport"] = f[:6].split("-")
    # Note: create a new dictionary for each entry in the output data list.
    # If you use the info dictionary defined here each element in the list 
    # will be a reference to the same info dictionary.
    html = open(f, "r")
    soup = BeautifulSoup(html, "lxml")
    table_list = soup.find(id="GridView1")
    for table in table_list.find_all("tr"):
    	if table["class"] == ["dataTDRight"]:


    		year, month, domestic, international, total = table.find_all("td")

    		if month.get_text() != "TOTAL":
    			info["courier"], info["airport"] = f[:6].split("-")
    			info["year"] = int(year.get_text())
    			info["month"] = int(month.get_text())
    				
    			info["flights"] = {"domestic": "",
                                   "international": ""}
    			if international.get_text(strip=True) == "" and domestic.get_text(strip=True) == "":
    				info["flights"]["domestic"] = 0
    				info["flights"]["international"] = 0
    			elif domestic.get_text(strip=True) == "" and international.get_text(strip=True) != "":
    				info["flights"]["domestic"] = 0
    				info["flights"]["international"] = international.get_text().strip(",")
    			elif domestic.get_text(strip=True) != "" and international.get_text(strip=True) == "":
    				info["flights"]["domestic"] = int(domestic.get_text().replace(",", ""))
    				info["flights"]["international"] = 0
    			else:
    				info["flights"]["domestic"] = int(domestic.get_text().replace(",", ""))
    				info["flights"]["international"] = int(international.get_text().replace(",", ""))
    			subdata = {"courier": info["courier"],
             				"airport": info["airport"],
             				"year": info["year"],
             				"month": info["month"],
             				"flights": info["flights"]}
    			data.append(subdata)
    return data
    			



print(process_file(f))

def test():
    print("Running a simple test...")
    data = process_file(f)
        
    assert len(data) == 186  # Total number of rows
    for entry in data:
        assert type(entry["year"]) == int
        assert type(entry["month"]) == int
        assert type(entry["flights"]["domestic"]) == int
        assert len(entry["airport"]) == 3
        assert len(entry["courier"]) == 2
    assert data[0]["courier"] == "DL"
    assert data[0]["month"] == 10
    assert data[0]["airport"] == "ATL"
    assert data[0]["flights"] == {'domestic': 16535, 'international': 1357}
    
    print("... success!")

if __name__ == "__main__":
    test()
    