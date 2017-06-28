import pymongo
import sys, os
from pprint import pprint

client = pymongo.MongoClient()

db = client.geo

collection = db.airports

pprint(collection.findone())