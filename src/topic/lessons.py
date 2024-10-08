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
    lesson_data.pop('unit_id', None)

    ghandler.db['lessons'].update_one(
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


def get_lessons(id: ObjectId) -> list[dict[str, any]]:
    '''
    Return all the lessons (and underlying data) connected to a unit
    '''
    lessons = list(ghandler.db['lessons'].find({'unit_id': id}))
    lessons.sort(key=lambda x: x.get('index', 0))

    for lesson in lessons:
        lesson['widgets'] = widgets.get_widgets(lesson.get('_id'))

    return lessons


def get_all(unit_id: ObjectId) -> tuple[dict, ...]:
    '''
    Retrieves title and description for all lessons under a unit
    '''

    return tuple(
        document
        for document in ghandler.db['lessons'].find(
            {'unit_id': unit_id}, {'title': 1, 'description': 1, 'index': 1, '_id': 0}
        )
    )


def search(tag: str) -> tuple[dict, ...]:
    '''
    Retrieves lessons based on tag
    '''

    return tuple(
        document
        for document in ghandler.db['lessons'].find(
            {
                '$or': [
                    {'title': {'$regex': tag, '$options': 'i'}},
                    {'description': {'$regex': tag, '$options': 'i'}},
                ]
            },
            {'title': 1, 'description': 1, '_id': 0},
        )
    )
