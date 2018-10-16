"""
Your task is to sucessfully run the exercise to see how pymongo works
and how easy it is to start using it.
You don't actually have to change anything in this exercise,
but you can change the city name in the add_city function if you like.

Your code will be run against a MongoDB instance that we have provided.
If you want to run this code locally on your machine,
you have to install MongoDB (see Instructor comments for link to installation information)
and uncomment the get_db function.
"""
import pandas as pd
import json
import pprint

def add_city(db):
    # Changes to this function will be reflected in the output. 
    # All other functions are for local use only.
    # Try changing the name of the city to be inserted
    db.cities.insert({"name" : "Chicago"})
    
def get_city(db):
    return db.cities.find_one()

def get_db():
    # For local use
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    # 'examples' here is the database name. It will be created if it does not exist.
    db = client.examples
    return db


'''if __name__ == "__main__":
    # For local use
    db = get_db() # uncomment this line if you want to run this locally
    add_city(db)
    for a in db.cities.find():
        pprint.pprint(a)'''

"""
Your task is to complete the 'porsche_query' function and in particular the query
to find all autos where the manufacturer field matches "Porsche".
Please modify only 'porsche_query' function, as only that will be taken into account.

Your code will be run against a MongoDB instance that we have provided.
If you want to run this code locally on your machine,
you have to install MongoDB and download and insert the dataset.
For instructions related to MongoDB setup and datasets please see Course Materials at
the following link:
https://www.udacity.com/wiki/ud032
"""

def porsche_query():
    # Please fill in the query to find all autos manuafactured by Porsche.
    query = {'manufacturer_label': 'Toyota', 'class_label': 'Mid-size car'}
    return query

def porsche_projection():
    # Please fill in the query to find all autos manuafactured by Porsche.
    projection = {'_id': 0, 'name': 1}
    return projection

def process_file_autos(file):
    data = pd.read_csv(file, low_memory=False)
    data_json = json.loads(data.to_json(orient='records'))
    new_data = []
    for row in data_json:
        if 'dbpedia' in row['URI']:
            if row['assembly_label'] == None:
                continue
            else:
                if row['assembly_label'][0] == '{':
                    row['assembly_label'] = row['assembly_label'].strip('{').strip('}').split('|')
                else:
                    continue
                new_data.append(row)
    return new_data

def import_autos(db, file):
    db.autos.insert(process_file_autos(file))

# Do not edit code below this line in the online code editor.
# Code here is for local use on your own computer.
def get_db(db_name):
    # For local use
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def find_porsche(db, query, projection):
    # For local use
    return db.autos.find(query, projection)


'''if __name__ == "__main__":
    # For local use
    db = get_db('examples')
    #db.autos.remove()
    import_autos(db, 'autos.csv')
    query = porsche_query()
    projection = porsche_projection()
    results = find_porsche(db, query, projection)
    for cars in results:
        pprint.pprint(cars)'''

#!/usr/bin/env python
"""
Your task is to write a query that will return all cities
that are founded in 21st century.
Please modify only 'range_query' function, as only that will be taken into account.

Your code will be run against a MongoDB instance that we have provided.
If you want to run this code locally on your machine,
you have to install MongoDB, download and insert the dataset.
For instructions related to MongoDB setup and datasets please see Course Materials.
"""

from datetime import datetime
    
def range_query():
    # Modify the below line with your query.
    # You can use datetime(year, month, day) to specify date in the query
    query = {'year': {'$gte': 2001}}
    return query

def process_file_cities(file):
    data = pd.read_csv(file, low_memory=False)
    data_json = json.loads(data.to_json(orient='records'))
    new_data = []
    for row in data_json:
        if 'dbpedia' in row['URI']:
            if row['foundingDate'] == None:
                row['year'] = None
            else:
                if row['foundingDate'][0] != '{':
                    if '-' in row['foundingDate']:
                        row['year'] = int(row['foundingDate'][0:4])
                    else:
                        row['year'] = int(row['foundingDate'][-4:])
                else:
                    row['year'] = int(row['foundingDate'].split('|')[0].strip('{')[0:4])
                new_data.append(row)
    return new_data

def import_cities(db, file):
    db.cities.insert(process_file_cities(file))

# Do not edit code below this line in the online code editor.
# Code here is for local use on your own computer.
def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.examples
    return db

'''if __name__ == "__main__":
    # For local use
    db = get_db()
    #db.cities.remove()
    #import_cities(db, 'cities.csv')
    query = range_query()
    cities = db.cities.find(query)

    print("Found cities:", cities.count())
    pprint.pprint(cities[0])'''

#!/usr/bin/env python
"""
Your task is to write a query that will return all cars manufactured by
"Ford Motor Company" that are assembled in Germany, United Kingdom, or Japan.
Please modify only 'in_query' function, as only that will be taken into account.

Your code will be run against a MongoDB instance that we have provided.
If you want to run this code locally on your machine,
you have to install MongoDB, download and insert the dataset.
For instructions related to MongoDB setup and datasets please see Course Materials.
"""


def in_query():
    # Modify the below line with your query; try to use the $in operator.
    query = {'manufacturer_label': {'$in': ['Ford Motor Company']}, 'assembly_label': {'$in': ['Germany', 'United Kingdom', 'Japan']}}
    return query


# Do not edit code below this line in the online code editor.
# Code here is for local use on your own computer.
def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.examples
    return db

'''if __name__ == "__main__":
    db = get_db()
    query = in_query()
    autos = db.autos.find(query, {"name":1, "manufacturer_label":1, "assembly_label": 1, "_id":0})
    print("Found autos:", autos.count())
    import pprint
    for a in autos:
        pprint.pprint(a)'''

#!/usr/bin/env python
"""
Your task is to write a query that will return all cars with width dimension
greater than 2.5. Please modify only the 'dot_query' function, as only that
will be taken into account.

Your code will be run against a MongoDB instance that we have provided.
If you want to run this code locally on your machine, you will need to install
MongoDB, download and insert the dataset. For instructions related to MongoDB
setup and datasets, please see the Course Materials.
"""


def dot_query():
    # Edit the line below with your query - try to use dot notation.
    # You can check out example_auto.txt for an example of the document
    # structure in the collection.
    query = {'width': }
    return query

# Do not edit code below this line in the online code editor.
# Code here is for local use on your own computer.
def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.examples
    return db


if __name__ == "__main__":
    db = get_db()
    query = dot_query()
    cars = db.cars.find(query)
    print("Printing first 3 results\n")
    import pprint
    for car in cars[:3]:
        pprint.pprint(car)


