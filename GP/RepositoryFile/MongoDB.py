import requests
import json
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDB:
    
    client = None
    
    def __init__(self, username, password):
        connection_string = 'mongodb+srv://' + username + ':' + password + '@sureanalytics.kw6jp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
        client = MongoClient(connection_string)
        self.client = client
        print("connection success")
    
    def Push_JSON(self, platform, user_id, file):
        database = self.client.get_database(platform)
        collection = database[user_id]
        _id = collection.insert_one(file)
        _id = str(_id.inserted_id)
        return _id
        
    def Get_JSON(self, platform, user_id, datafile_id):
        database = self.client.get_database(platform)
        collection = database[user_id]
        file = collection.find_one({"_id": ObjectId(datafile_id)})
        ret_file = pd.DataFrame.from_dict(file)
        ret_file = ret_file.drop(columns={'_id'})
        return ret_file
    

    
    

    

    
    
    
    
    
    
    
    
    