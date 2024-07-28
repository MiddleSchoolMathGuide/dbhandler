'''
Manages units
'''

from bson import ObjectId
from .. import ghandler

from . import lessons


def set(id: ObjectId, unit_data: dict[str, any]) -> str:
    '''
    Set fields of a unit
    '''

    lessons_ = unit_data.pop('lessons', [])
    unit_id = ObjectId(unit_data.pop('_id', None))
    unit_data.pop('topic_id', None)

    ghandler.db['units'].update_one(
        {'_id': unit_id},
        {'$set': dict({'topic_id': id}, **unit_data)},
        upsert=True
    )

    lesson_ids = []
    for lesson in lessons_:
        lesson_ids.append(lessons.set(unit_id, lesson))

    set_lesson_ids(unit_id, lesson_ids)
    return unit_id


def delete(title: str) -> None:
    '''
    Delete a unit
    '''
    ghandler.db['units'].delete_one({'title': title})


def set_lesson_ids(id: ObjectId, lesson_ids: list[str]) -> None:
    '''
    Set lesson ids of a unit
    '''
    ghandler.db['units'].update_one(
        {'_id': id}, {'$set': {'lessons': lesson_ids}}
    )


def get_units(id: ObjectId) -> list[dict[str, any]]:
    '''
    Return all the units (and underlying data) connected to a topic
    '''

    units = list(ghandler.db['units'].find({'topic_id': id}))
    units.sort(key=lambda x: x.get('index', 0))

    for unit in units:
        unit['lessons'] = lessons.get_lessons(unit.get('_id'))

    return units
