from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv
from typing import Any

load_dotenv()

# Connect to your MongoDB instance
uri = getenv("URI")
client = MongoClient(uri)
database = client['measurements']

def add_trace_route_to_db(traceroute: dict[str, Any]):
    collection = database['traceroute']
    if isinstance(traceroute, list):
        collection.insert_many(traceroute)
    else:
        collection.insert_one(traceroute)

def add_ping_result_to_db(ping: dict[str, Any]):
    collection = database['ping']
    if isinstance(ping, list):
        collection.insert_many(ping)
    else:
        collection.insert_one(ping)

def add_measurements_to_db(measurement: dict[str, Any]):
    collection = database['measurement_ids']
    if isinstance(measurement, list):
        collection.insert_many(measurement)
    else:
        collection.insert_one(measurement)

def get_traceroute_ids():
    collection = database['measurement_ids']
    return collection.distinct("measurement_id", {"type": "traceroute"})

def close_db():
    client.close()


## this is an example of how to update items in a database

# collection = database['measurement_ids']

# update_criteria = {
#     "type":{
#         "$exists": False
#     }
# }

# update_operation = {
#     "$set":{
#         "type": "traceroute"
#     }
# }
# collection.update_many(update_criteria, update_operation)
