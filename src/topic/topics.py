'''
Manages topics
'''

from typing import Any

from bson import ObjectId
import logging

from .. import ghandler

from . import units
from . import utils
from . import widgets


def set(topic_data: dict[str, any]) -> ObjectId:
    '''
    Set fields of a topic
    '''

    units_ = topic_data.pop('units', [])
    topic_id = ObjectId(topic_data.pop('_id', None))

    ghandler.db['topics'].update_one(
        {'_id': topic_id}, {'$set': topic_data}, upsert=True
    )

    unit_ids = []
    for unit in units_:
        unit_ids.append(units.set(topic_id, unit))

    set_unit_ids(topic_id, unit_ids)
    return topic_id


def delete(title: str) -> None:
    '''
    Delete a topic
    '''
    ghandler.db['topics'].delete_one({'title': utils.normalize_title(title)})


def set_unit_ids(id: ObjectId, unit_ids: list[str]) -> None:
    '''
    Set unit ids of a topic
    '''
    ghandler.db['topics'].update_one({'_id': id}, {'$set': {'units': unit_ids}})


def get_units(title: str) -> None:
    pipeline = [{'$match': {'tilte': utils.normalize_title(title)}}]
    return list(ghandler.db['units'].aggregate(pipeline))


def get_id_by_title(title: str) -> ObjectId | None:
    topic = ghandler.db['topics'].find_one({'title': utils.normalize_title(title)})
    return topic.get('_id') if topic else None


def get_topic_by_title(title: str) -> dict[str, str]:
    topic = ghandler.db['topics'].find_one({'title': utils.normalize_title(title)})
    if not topic:
        return {'ok': False, 'msg': 'Topic does not exist', 'data': None}

    topic['units'] = units.get_units(topic.get('_id'))
    return {'ok': True, 'msg': 'Success', 'data': topic}


def get_by_titles(
    topic_title: str, unit_title: str, lesson_title: str
) -> dict[str, Any]:
    topic = ghandler.db['topics'].find_one(
        {'title': utils.normalize_title(topic_title)}
    )
    if not topic:
        logging.info('No topic found with the given title.')
        return {'ok': False, 'msg': 'No topic found with the given title'}

    unit = ghandler.db['units'].find_one(
        {'title': utils.normalize_title(unit_title), 'topic_id': topic['_id']}
    )
    if not unit:
        logging.info('No unit found with the given title and topic_id.')
        return {'ok': False, 'msg': 'No unit found with the given title and topic_id'}

    lesson = ghandler.db['lessons'].find_one(
        {'title': utils.normalize_title(lesson_title), 'unit_id': unit['_id']}
    )

    if not lesson:
        logging.info('No lesson found with the given title and unit_id.')
        return {'ok': False, 'msg': 'No lesson found with the given title and unit_id'}

    topic['units'] = (unit,)
    unit['lessons'] = (lesson,)
    lesson['widgets'] = widgets.get_widgets(lesson['_id'])
    return {
        'ok': True,
        'msg': 'Success',
        'data': topic,
    }


def get_all() -> tuple[dict, ...]:
    '''
    Retrieves title and description for all topics
    '''

    return tuple(
        document
        for document in ghandler.db['topics'].find(
            {}, {'title': 1, 'description': 1, '_id': 0}
        )
    )


def search(tag: str) -> tuple[dict, ...]:
    '''
    Retrieves topics based on tag
    '''

    return tuple(
        document
        for document in ghandler.db['topics'].find(
            {
                '$or': [
                    {'title': {'$regex': tag, '$options': 'i'}},
                    {'description': {'$regex': tag, '$options': 'i'}},
                ]
            },
            {'title': 1, 'description': 1, '_id': 0},
        )
    )
