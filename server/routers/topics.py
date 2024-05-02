from fastapi import APIRouter, Header
from pydantic import BaseModel
from common.responses import BadRequest, InternalServerError, NotFound, Unauthorized
from data.models import Reply, Role, Topic
from services import topic_service, category_service, reply_service
from common.auth import get_user_or_raise_401


topics_router = APIRouter(prefix='/topics')

class TopicResponseModel(BaseModel):
    topic: Topic
    replies: list[Reply]

@topics_router.get('/', response_model=list[Topic])
def get_topics(
    skip: int | None = None,
    take: int |None = None,
    sorting: str | None = None,
    sort_by: str | None = None,
    search: str | None = None):

    result = topic_service.all(search, skip, take)

    if sorting and (sorting == 'asc' or sorting == 'desc'):
        return topic_service.sorting(result, reverse=sorting == 'desc', attribute=sort_by)
    else:
        return result


@topics_router.get('/{id}')
def get_topic_by_id(id: int):
    topic = topic_service.get_by_id(id)

    if not topic:
        return NotFound(f'Topic with the id {id} doesn\'t exist!')
    
    return TopicResponseModel(
        topic= topic,
        replies= reply_service.get_by_topic(topic.id))



@topics_router.post('/', status_code=201)
def create_topic(topic: Topic, x_token: str | None = Header()):

    user = get_user_or_raise_401(x_token)
    if user.role != Role.USER:
        return Unauthorized('You are not authoriszed to create topic!')
    
    if user.id != topic.author_id:
        return BadRequest(f"Author id {topic.author_id} in the topic does not match the id {user.id} of the user!")

    if not category_service.exists(topic.categories_id):
        return BadRequest(f'Category {topic.categories_id} does not exist')

    return topic_service.create(topic)
    

@topics_router.put('/{id}')
def update_best_reply(id: int, topic: Topic,  x_token: str | None = Header()):

    existing_topic = topic_service.get_by_id(id)
    if existing_topic is None:
        return NotFound('Topic with that id doesn\'t exist')
    
    user = get_user_or_raise_401(x_token)
    if user.id != topic.author_id:
        return Unauthorized('You are not authoriszed to change this topic!')
    
    reply = reply_service.get_by_id(topic.best_reply_id)
    if reply.topics_id != topic.id:
        return InternalServerError("Inconsistent data: Topic's best reply does not belong to the topic!")

    return topic_service.update_best_reply_id(existing_topic, topic)
    

