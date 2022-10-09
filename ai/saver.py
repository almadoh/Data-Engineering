from pymongo import MongoClient
import pymongo
import json


def connecting_to_mongo():
    # connecting python to mongodb
    CONNECTION_STRING = "mongodb://localhost:27017/"

    # set a client for the connection
    client = MongoClient(CONNECTION_STRING)

    # Create the database, tester is a sample name
    return client['Data_Engineering']


# access the database
dbname = connecting_to_mongo()


def save_to_mongo():
    collection = dbname["all_outputs.jsonl"]
    requesting = []
    with open('all_outputs.jsonl') as file:
        for jsonobj in file:
            myDict = json.loads(jsonobj)
            requesting.append(pymongo.InsertOne(myDict))
    result = collection.bulk_write(requesting)


connecting_to_mongo()
save_to_mongo()
