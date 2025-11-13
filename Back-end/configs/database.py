# -*- coding: utf-8 -*-
import certifi
from pymongo.mongo_client import MongoClient

client = MongoClient(
    'mongodb+srv://doananhtuan77qn_db_user:ZOkB1Xu9RebKeK06@laptrinhmang.prgg2hn.mongodb.net/?appName=lapTrinhMang',
    tlsCAFile=certifi.where()
)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.LapTrinhMang

user_collection = db["Users"]
message_collection = db["Messages"]
dialog_collection = db["Dialogs"]
call_collection = db["Calls"]
