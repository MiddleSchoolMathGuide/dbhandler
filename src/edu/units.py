'''
Manages units
'''

from bson import ObjectId
from .. import ghandler

from . import lessons


def set(id: str, unit_data: dict[str, any]) -> str:
    '''
    Set fields of a unit
    '''

    lessons_ = unit_data.pop('lessons')
    unit_id = (
        ghandler.db['units']
        .update_one(
            {'_id': unit_data.get('_id') or ObjectId()},
            {'$set': dict({'topic_id': id}, **unit_data)},
            upsert=True
        )
        .upserted_id or unit_data.get('_id')
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


def set_lesson_ids(id: str, lesson_ids: list[str]) -> None:
    '''
    Set lesson ids of a unit
    '''
    ghandler.db['units'].update_one(
        {'_id': id}, {'$set': {'lessons': lesson_ids}}
    )


def get_units(id: str) -> tuple[dict[str, any], ...]:
    '''
    Return all the units (and underlying data) connected to a topic
    '''
    units = tuple(ghandler.db['units'].find({'topic_id': id}))
    for unit in units:
        units[0]['lessons'] = lessons.get_lessons(unit.get('_id'))

    return units
