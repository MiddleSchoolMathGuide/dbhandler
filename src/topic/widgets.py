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
    widget_data.pop('lesson_id', None)

    ghandler.db['widgets'].update_one(
        {'_id': widget_id},
        {'$set': dict({'lesson_id': id}, **widget_data)},
        upsert=True
    )

    return widget_id


def get_widgets(id: ObjectId) -> list[dict[str, any]]:
    '''
    Return all the widgets connected to a lesson
    '''
    widgets = list(ghandler.db['widgets'].find({'lesson_id': id}))
    widgets.sort(key=lambda x: x.get('index', 0))
    return widgets
