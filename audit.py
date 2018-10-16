#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a 
SET of the types that can be found in the field. e.g.
{"field1": set([type(float()), type(int()), type(str())]),
 "field2": set([type(str())]),
  ....
}
The type() function returns a type object describing the argument given to the 
function. You can also use examples of objects to create type objects, e.g.
type(1.1) for a float: see the test function below for examples.

Note that the first three rows (after the header row) in the cities.csv file
are not actual data points. The contents of these rows should note be included
when processing data types. Be sure to include functionality in your code to
skip over or detect these rows.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label",
          "isPartOf_label", "areaCode", "populationTotal", "elevation",
          "maximumElevation", "minimumElevation", "populationDensity",
          "wgs84_pos#lat", "wgs84_pos#long", "areaLand", "areaMetro", "areaUrban"]

def audit_file(filename, fields):
    fieldtypes = {}
    for field in fields:
        a = set()
        with open(filename, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'dbpedia' in row['URI']:
                    if row[field] == 'NULL' or row[field] == '':
                        a.add(type(None))
                    elif row[field][0] == '{':
                        a.add(type(list())) 
                    else:
                        try:
                            row[field] = int(row[field])
                            a.add(type(int()))
                        except ValueError:
                            try:
                                row[field] = float(row[field])
                                a.add(type(float()))
                            except ValueError:
                                a.add(type(str()))
        fieldtypes[field] = a

    

    return fieldtypes


'''def test():
    fieldtypes = audit_file(CITIES, FIELDS)
    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type([]), type(None)])
    
if __name__ == "__main__":
    test()'''


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up.

Since in the previous quiz you made a decision on which value to keep for the
"areaLand" field, you now know what has to be done.

Finish the function fix_area(). It will receive a string as an input, and it
has to return a float representing the value of the area or None.
You have to change the function fix_area. You can use extra functions if you
like, but changes to process_file will not be taken into account.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'


def fix_area(area):

    if area == 'NULL' or area == '':
        area = None
    elif area[0] == '{':
        area = float(area.strip('}').split('|')[1])
    else:
        try:
            area = float(area)
        except ValueError:
            area = None     
    return area



def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for line in reader:
            if 'dbpedia' in line['URI']:
            # calling your function to fix the area value
                if "areaLand" in line:
                    line["areaLand"] = fix_area(line["areaLand"])
                data.append(line)

    return data


'''def test():
    data = process_file(CITIES)

    print("Printing three example results:")
    for n in range(400,405):
        pprint.pprint(data[n]["areaLand"])

    assert data[3]["areaLand"] == None        
    assert data[400]["areaLand"] == None
    assert data[403]["areaLand"] == 7125060.0
    assert data[404]["areaLand"] == 146394000.0


if __name__ == "__main__":
    test()'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up.

In the previous quiz you recognized that the "name" value can be an array (or
list in Python terms). It would make it easier to process and query the data
later if all values for the name are in a Python list, instead of being
just a string separated with special characters, like now.

Finish the function fix_name(). It will recieve a string as an input, and it
will return a list of all the names. If there is only one name, the list will
have only one item in it; if the name is "NULL", the list should be empty.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import pprint

CITIES = 'cities.csv'


def fix_name(name):

    if name == 'NULL' or name == '':
        name = []
    elif name[0] == '{':
        name = name.strip('{').strip('}').split('|')
    else:
        name = [name]
    return name


def process_file(filename):
    data = []
    with open(filename, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for line in reader:
            if 'dbpedia' in line['URI']:
            # calling your function to fix the area value
                if "name" in line:
                    line["name"] = fix_name(line["name"])
                data.append(line)
        return data


'''def test():
    data = process_file(CITIES)

    print("Printing 20 results:")
    for n in range(20):
        pprint.pprint(data[n]["name"])

    assert data[14]["name"] == ['Laharpur']
    assert data[9]["name"] == ['Kurinjipadi']
    assert data[3]["name"] == ['Kumhari']

if __name__ == "__main__":
    test()'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up.

If you look at the full city data, you will notice that there are couple of
values that seem to provide the same information in different formats: "point"
seems to be the combination of "wgs84_pos#lat" and "wgs84_pos#long". However,
we do not know if that is the case and should check if they are equivalent.

Finish the function check_loc(). It will recieve 3 strings: first, the combined
value of "point" followed by the separate "wgs84_pos#" values. You have to
extract the lat and long values from the "point" argument and compare them to
the "wgs84_pos# values, returning True or False.

Note that you do not have to fix the values, only determine if they are
consistent. To fix them in this case you would need more information. Feel free
to discuss possible strategies for fixing this on the discussion forum.

The rest of the code is just an example on how this function can be used.
Changes to "process_file" function will not be taken into account for grading.
"""
import csv
import pprint

CITIES = 'cities.csv'


def check_loc(point, lat, longi):
    try:
        if point[0] != '{':
            point = point.split(' ')
            if [float(point[0]), float(point[1])] == [float(lat), float(longi)]:
                return True
            else:
                return False
        else:
            if lat[0] != '{' and longi[0] == '{':
                longi1, longi2 = longi.strip('{').strip('}').split('|')
                point1, point2 = point.strip('{').strip('}').split('|')[0].split(' '), point.strip('{').strip('}').split('|')[1].split(' ')
                if ([float(point1[0]), float(point1[1])] == [float(lat), float(longi1)] and [float(point2[0]), float(point2[1])] == [float(lat), float(longi2)]) or ([float(point2[0]), float(point2[1])] == [float(lat), float(longi1)] and [float(point1[0]), float(point1[1])] == [float(lat), float(longi2)]):
                    return True
                else:
                    return False
            
            elif lat[0] == '{' and longi[0] != '{':
                lat1, lat2 = lat.strip('{').strip('}').split('|')
                point1, point2 = point.strip('{').strip('}').split('|')[0].split(' '), point.strip('{').strip('}').split('|')[1].split(' ')
                if ([float(point1[0]), float(point1[1])] == [float(lat1), float(longi)] and [float(point2[0]), float(point2[1])] == [float(lat2), float(longi)]) or ([float(point2[0]), float(point2[1])] == [float(lat1), float(longi)] and [float(point1[0]), float(point1[1])] == [float(lat2), float(longi)]):
                    return True
                else:
                    return False
            elif lat[0] != '{' and longi[0] != '{':
                point1, point2 = point.strip('{').strip('}').split('|')[0].split(' '), point.strip('{').strip('}').split('|')[1].split(' ')
                if [float(point1[0]), float(point1[1])] == [float(lat), float(longi)] or [float(point2[0]), float(point2[1])] == [float(lat), float(longi)]:
                    return True
                else:
                    return False
            else:
                lat1, lat2 = lat.strip('{').strip('}').split('|')
                longi1, longi2 = longi.strip('{').strip('}').split('|')
                point1, point2 = point.strip('{').strip('}').split('|')[0].split(' '), point.strip('{').strip('}').split('|')[1].split(' ')
                if ([float(point1[0]), float(point1[1])] == [float(lat1), float(longi1)] and [float(point2[0]), float(point2[1])] == [float(lat2), float(longi2)]) or ([float(point2[0]), float(point2[1])] == [float(lat1), float(longi1)] and [float(point1[0]), float(point1[1])] == [float(lat2), float(longi2)]):
                    return True
                else:
                    return False
    except ValueError:
        return False


def process_file(filename):
    data = []
    with open(filename, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for line in reader:
            if 'dbpedia' in line['URI']:
            # calling your function to check the location
                result = check_loc(line["point"], line["wgs84_pos#lat"], line["wgs84_pos#long"])
                if not result:
                    print("{}: {} != {} {}".format(line["name"], line["point"], line["wgs84_pos#lat"], line["wgs84_pos#long"]))
                data.append(line)

    return data


def test():
    assert check_loc("33.08 75.28", "33.08", "75.28") == True
    assert check_loc("44.57833333333333 -91.21833333333333", "44.5783", "-91.2183") == False

if __name__ == "__main__":
    test()
