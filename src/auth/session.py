'''
Manages session creation and timeout
'''

from datetime import datetime, timedelta

from .. import const, ghandler


def create(user_id: str) -> str:
    '''
    Create a new session for a user

    Warning: Should not be called manually!
    '''

    return ghandler.db['session'].insert_one({
        'user_id': user_id,
        'created_at': datetime.now(),
        'expires_at': datetime.now() + timedelta(seconds=const.TIMEOUT)
    }).inserted_id


def is_expired(session_id: str) -> bool:
    '''
    Checks whether session is expired

    True means session expired
    '''

    session = ghandler.db['session'].find_one({"_id": session_id})
    if not session:
        return True

    if session.get('expires_at') < datetime.now():
        # Delete expired session
        ghandler.db['session'].delete_one({'_id': session_id})
        return True

    return False


def cleanup_sessions() -> None:
    '''Automatically deletes expired sessions'''
    ghandler.db['session'].delete_many({'expires_at': {'$lt': datetime.now()}})
