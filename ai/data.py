from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
database = client["Data_Engineering"]
collection = database["all_outputs.jsonl"]
