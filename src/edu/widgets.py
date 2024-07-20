'''
Manages units
'''

from bson import ObjectId
from .. import ghandler


def set(id: str, widget_data: dict[str, any]) -> str:
    '''
    Set fields of a widget
    '''

    widget_id = (
        ghandler.db['widgets']
        .update_one(
            {'_id': ObjectId(widget_data.get('_id'))},
            {'$set': dict({'lesson_id': id}, **widget_data)},
            upsert=True
        )
        .upserted_id or widget_data.get('_id')
    )

    return widget_id


def get_widgets(id: str) -> tuple[dict[str, any], ...]:
    '''
    Return all the widgets connected to a lesson
    '''
    return tuple(ghandler.db['widgets'].find({'lesson_id': id}))
