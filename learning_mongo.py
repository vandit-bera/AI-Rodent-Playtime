from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")
connection = f"mongodb+srv://motional:{password}@cluster0.z4b7ke9.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection)

dbs = client.list_database_names()
print(dbs)
