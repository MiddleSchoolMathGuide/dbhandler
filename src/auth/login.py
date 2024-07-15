'''
Manages user login and authentication
'''

from .. import ghandler
from . import session


def login(username: str, password_hash: str) -> tuple[dict, str | None]:
    '''Validate user'''
    user = ghandler.db['users'].find_one({'username': username})
    if not user:
        return {'ok': False, 'message': 'User not found'}, None

    if password_hash != user.get('password_hash'):
        return {'ok': False, 'message': 'Invalid password'}, None

    id_ = session.create(user['_id'])
    return {'ok': True, 'message': 'Authentication successful'}, id_
