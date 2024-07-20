'''
Manages units
'''

from bson import ObjectId
from .. import ghandler


def set(id: ObjectId, widget_data: dict[str, any]) -> str:
    '''
    Set fields of a widget
    '''

    widget_id = ObjectId(widget_data.pop('_id', None))
    widget_data.pop('lesson_id')

    ghandler.db['widgets'].update_one(
        {'_id': widget_id},
        {'$set': dict({'lesson_id': id}, **widget_data)},
        upsert=True
    )

    return widget_id


def get_widgets(id: ObjectId) -> tuple[dict[str, any], ...]:
    '''
    Return all the widgets connected to a lesson
    '''
    return tuple(ghandler.db['widgets'].find({'lesson_id': id}))
