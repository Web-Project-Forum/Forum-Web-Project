from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from common.responses import BadRequest, NotFound, Unauthorized
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
        return NotFound('Topic with that id doesn\'t exist')
    
    return TopicResponseModel(
        topic= topic,
        replies= reply_service.get_by_topic(topic.id))



@topics_router.post('/', status_code=201)
def create_topic(topic: Topic, x_token: str | None = Header()):
    user = get_user_or_raise_401(x_token)
    if user.role == Role.USER or user.role == Role.ADMIN:
        
        if not category_service.exists(topic.categories_id):
            return BadRequest(f'Category {topic.categories_id} does not exist')

        return topic_service.create(topic)
    
    return Unauthorized(content='You are not authoriszed to create topic!')



@topics_router.put('/{id}/{user_id}')
def update_best_reply(id: int, user_id: int, topic: Topic,  x_token: str | None = Header()):
    user = get_user_or_raise_401(x_token)
    if user.role == Role.USER or user.role == Role.ADMIN:

        existing_topic = topic_service.get_by_id(id)

        if user_id == topic.author_id:
            if existing_topic is None:
                return NotFound()
            
            return topic_service.update_best_reply_id(existing_topic, topic)

        return Unauthorized(content='You are not authoriszed to change the topic!')
    
    return Unauthorized(content='You are not authoriszed to change the topic!')
