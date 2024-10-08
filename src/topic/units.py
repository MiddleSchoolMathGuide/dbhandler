'''
Manages units
'''

from bson import ObjectId
from .. import ghandler

from . import lessons
from . import utils


def get_unit_by_title(title: str) -> dict[str, str]:
    unit = ghandler.db['units'].find_one({'title': utils.normalize_title(title)})
    if not unit:
        return {'ok': False, 'msg': 'Unit does not exist', 'data': None}

    unit['lessons'] = lessons.get_lessons(unit.get('_id'))
    return {'ok': True, 'msg': 'Success', 'data': unit}


def get_id_by_title(topic_id: ObjectId, title: str) -> ObjectId:
    unit = ghandler.db['units'].find_one(
        {'topic_id': topic_id, 'title': utils.normalize_title(title)}
    )
    return unit.get('_id') if unit else None


def set(id: ObjectId, unit_data: dict[str, any]) -> str:
    '''
    Set fields of a unit
    '''

    lessons_ = unit_data.pop('lessons', [])
    unit_id = ObjectId(unit_data.pop('_id', None))
    unit_data.pop('topic_id', None)

    ghandler.db['units'].update_one(
        {'_id': unit_id}, {'$set': dict({'topic_id': id}, **unit_data)}, upsert=True
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
    ghandler.db['units'].delete_one({'title': utils.normalize_title(title)})


def set_lesson_ids(id: ObjectId, lesson_ids: list[str]) -> None:
    '''
    Set lesson ids of a unit
    '''
    ghandler.db['units'].update_one({'_id': id}, {'$set': {'lessons': lesson_ids}})


def get_units(id: ObjectId) -> list[dict[str, any]]:
    '''
    Return all the units (and underlying data) connected to a topic
    '''

    units = list(ghandler.db['units'].find({'topic_id': id}))
    units.sort(key=lambda x: x.get('index', 0))

    for unit in units:
        unit['lessons'] = lessons.get_lessons(unit.get('_id'))

    return units


def get_all(topic_id: ObjectId, include_id: bool = False) -> tuple[dict, ...]:
    '''
    Retrieves title and description for all units under a topic
    '''

    return tuple(
        document
        for document in ghandler.db['units'].find(
            {'topic_id': topic_id}, {'title': 1, 'description': 1, 'index': 1, '_id': include_id}
        )
    )


def search(tag: str) -> tuple[dict, ...]:
    '''
    Retrieves units based on tag
    '''

    return tuple(
        document
        for document in ghandler.db['units'].find(
            {
                '$or': [
                    {'title': {'$regex': tag, '$options': 'i'}},
                    {'description': {'$regex': tag, '$options': 'i'}},
                ]
            },
            {'title': 1, 'description': 1, '_id': 0},
        )
    )
