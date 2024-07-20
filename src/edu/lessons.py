'''
Manages lessons
'''

from bson import ObjectId
from .. import ghandler

from . import widgets


def set(id: ObjectId, lesson_data: dict[str, any]) -> str:
    '''
    Set fields in a lesson
    '''

    widgets_ = lesson_data.pop('widgets', [])
    lesson_id = ObjectId(lesson_data.pop('_id', None))
    lesson_data.pop('unit_id')

    ghandler.db['units'].update_one(
        {'_id': lesson_id},
        {'$set': dict({'unit_id': id}, **lesson_data)},
        upsert=True
    )

    widget_ids = []
    for widget in widgets_:
        widget_ids.append(widgets.set(lesson_id, widget))

    set_lesson_ids(lesson_id, widget_ids)
    return lesson_id


def delete(id: str) -> None:
    '''
    Delete a lesson
    '''
    ghandler.db['lessons'].delete_one({'_id': id})


def set_lesson_ids(id: ObjectId, widget_ids: list[str]) -> None:
    '''
    Set widget ids of a lesson
    '''
    ghandler.db['lessons'].update_one(
        {'_id': id}, {'$set': {'widgets': widget_ids}}
    )


def get_lessons(id: ObjectId) -> tuple[dict[str, any], ...]:
    '''
    Return all the lessons (and underlying data) connected to a unit
    '''
    lessons = tuple(ghandler.db['lessons'].find({'unit_id': id}))
    for lesson in lessons:
        lesson['widgets'] = widgets.get_widgets(lesson.get('_id'))

    return lessons
