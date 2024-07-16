'''
User profile operations
'''

from .. import ghandler


def fetch(username: str | None) -> dict[str, any]:
    '''Fetch user'''
    if username is None:
        return {'ok': False, 'message': 'Username missing from cookies'}

    user = ghandler.db['users'].find_one({'username': username})
    if not user:
        return {'ok': False, 'message': 'User not found'}

    # Hide sensitive fields
    user['_id'] = None
    user['password_hash'] = None

    return {'ok': True, 'message': 'User Found', 'data': user}
