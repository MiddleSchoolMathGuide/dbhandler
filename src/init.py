'''
Initialize MongoDB
'''

from hashlib import sha256
import logging
import logging.config
import os
from time import time
import pymongo
import pymongo.collection
import pymongo.database

from .const import DBNAME, MONGO_ADDRESS
from . import ghandler as gh
from .auth import session


def init() -> None:
    '''Load MongoDB'''
    gh.client = pymongo.MongoClient(MONGO_ADDRESS)
    if DBNAME not in gh.client.list_database_names():
        logging.info('Creating database...')
        _create_db_structure()
        logging.info('Database created!')
    gh.db = gh.client[DBNAME]
    session.cleanup_sessions()

    logging.info('MongoDB init done')


def _create_db_structure() -> None:
    db = gh.client.get_database(DBNAME)
    users = db.create_collection('users')
    _ = db.create_collection('session')
    _create_collection_indexes(users=users)

    users.insert_one({
        'username': 'admin',
        'password_hash': sha256(b'admin').hexdigest(),
        'email': None,
        'privilige_level': 'admin',
        'created_at': time(),
        'updated_at': time(),
        'profile': {
            'name': 'Admin',
            'bio': 'Admin of MSMG'
        }
    })


def _create_collection_indexes(users: pymongo.collection.Collection) -> None:
    users.create_index([('username', 1)], unique=True)


def _init_logging() -> None:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    logging.config.fileConfig('config/logger.config.ini')
    logging.info('Logging init done')


if __name__ == '__main__':
    _init_logging()
    init()
