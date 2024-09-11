import pymongo
import os

from hashlib import md5
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["freesend"]


users = db["users"]

obj = (md5(os.urandom(64))).hexdigest()

newuser = {"username":"maweeeeeett", "password": "eeeeeeewed", "backend_dir": obj}


users.insert_one(newuser)
os.system("mkdir "+(obj))



