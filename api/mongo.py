from pymongo import MongoClient
from pymongo.server_api import ServerApi
from os import getenv
from dotenv import load_dotenv
load_dotenv()

# Connect to your MongoDB instance
uri = getenv("URI")

def addToDb(json:dict,database:str,collection:str):
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        db = client[database]
        col = db[collection]
        col.insert_one(json)
        print("Pinged your deployment. You successfully pushed to MongoDB!")
    except Exception as e:
        print(e)


