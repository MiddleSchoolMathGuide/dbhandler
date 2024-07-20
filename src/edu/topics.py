'''
Manages topics
'''

from bson import ObjectId
from .. import ghandler

from . import units


def set(topic_data: dict[str, any]) -> str:
    '''
    Set fields of a topic
    '''

    units_ = topic_data.pop('units')
    topic_id = (
        ghandler.db['topics']
        .update_one(
            {'_id': topic_data.get('_id') or ObjectId()},
            {'$set': topic_data},
            upsert=True
        )
        .upserted_id or topic_data.get('_id')
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
    ghandler.db['topics'].delete_one({'title': title})


def set_unit_ids(id: str, units_ids: list[str]) -> None:
    '''
    Set unit ids of a topic
    '''
    ghandler.db['topics'].update_one(
        {'_id': id}, {'$set': {'units': units_ids}}
    )


def get_units(title: str) -> None:
    pipeline = [{'$match': {'tilte': title}}]
    return list(ghandler.db['units'].aggregate(pipeline))


def get_topic(title: str) -> dict[str, str]:
    topic = ghandler.db['topics'].find_one({'title': title})
    if not topic:
        return {'ok': False, 'msg': 'Topic does not exist', 'data': None}

    topic['units'] = units.get_units(topic.get('_id'))
    return {'ok': True, 'msg': 'Success', 'data': topic}
