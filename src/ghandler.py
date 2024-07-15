'''
DBHandler globals
'''

import pymongo
import pymongo.database

client: pymongo.MongoClient | None = None
db: pymongo.database.Database | None = None
