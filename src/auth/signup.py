'''
Create new users
'''

from typing import Any
import time

from pymongo import errors

from .. import const, ghandler
from . import login


def new(user_data: dict[str, Any]) -> tuple[dict[str, bool | str], str | None]:
    '''
    Create a new user
    '''

    username = user_data.get('username')
    password_hash = user_data.get('password_hash')
    if not _is_username_valid(username):
        return {'ok': False, 'msg': 'Username is invalid'}, None

    time_created = int(time.time())
    try:
        ghandler.db['users'].insert_one(
            {
                'username': username,
                'email': user_data.get('email'),
                'password_hash': password_hash,
                'privilige_level': const.DEFAULT_PRIVILIGE_LEVEL,
                'created_at': time_created,
                'updated_at': time_created,
                'profile': {
                    'firstname': '',
                    'lastname': '',
                    'bio': ''
                }
            }
        )
    except errors.DuplicateKeyError:
        return {'ok': False, 'msg': f'User "{username}" already exists'}, None

    # Create initial session
    msg, id_ = login.login(username, password_hash)
    if msg.get('ok') is not True:
        return {'ok': False, 'msg': 'Error during auto-login'}, None
    return {'ok': True, 'msg': 'User successfully created'}, id_


def _is_username_valid(username: str) -> bool:
    return username is not None
