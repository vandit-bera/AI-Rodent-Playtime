from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv

def connect():
    db_password = os.getenv('MONGO_DB_KEY')

    client = MongoClient(db_password)
    print("Successfully Connected")
    collection = client.main
    return collection.main

db = connect()

# Making a CRUD API

# Create
def write(data):
    if type(data) == None:
        print("No data")
        return
    # for loop to add multiple pieces of data
    if type(data) == list:
        for doc in data:
            db.insert_one(doc)
            return
    db.insert_one(data)

# Read
def read(email):
    if type(email) == None:
        print("No email provided")
        return
    return db.find_one({"email": email})

# Update
def update(email, data, dataType):
    if type(email) == None or type(data) == None:
        print(f"Provide valid data\nEmail: {email} | Data: {data}")
        return
    
    db.update_one({"email": email}, {"$set":{dataType: data}})

# Delete
def delete(email):
    if type(email) == None:
        print("No email provided")
        return
    db.delete_one({"email": email})

object = {
    "name": "Astra",
    "email": "xyz@gmail.com"
}
