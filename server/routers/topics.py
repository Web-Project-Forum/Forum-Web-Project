from fastapi import APIRouter
from common.responses import BadRequest, NotFound
from data.models import Topic
from services import topic_service
from services import category_service


topics_router = APIRouter(prefix='/topics')


@topics_router.get('/', response_model=list[Topic])
def get_topics(
    sort: str | None = None,
    sort_by: str | None = None,
    search: str | None = None
):
    result = topic_service.all(search)

    if sort and (sort == 'asc' or sort == 'desc'):
        return topic_service.sort(result, reverse=sort == 'desc', attribute=sort_by)
    else:
        return result


@topics_router.get('/{id}')
def get_topic_by_id(id: int):
    Topic = topic_service.get_by_id(id)

    if Topic is None:
        return NotFound()
    else:
        return Topic


@topics_router.post('/', status_code=201)
def create_topic(topic: Topic):
    if not category_service.exists(topic.categories_id):
        return BadRequest('Category {topic.categories_id} does not exist')

    return topic_service.create(topic)


@topics_router.put('/{id}')
def update_topic(id: int, topic: Topic):
    if not category_service.exists(topic.categories_id):
        return BadRequest(f'Category {topic.categories_id} does not exist')

    existing_topic = topic_service.get_by_id(id)
    if existing_topic is None:
        return NotFound()
    else:
        return topic_service.update(existing_topic, topic)
