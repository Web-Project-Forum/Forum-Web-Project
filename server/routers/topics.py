from typing import Optional
from fastapi import APIRouter, Header
from pydantic import BaseModel
from common.responses import BadRequest, Forbidden, NotFound, Unauthorized, Ok
from data.models import Reply, Role, Topic
from services import topic_service, category_service, reply_service
from common.auth import get_user_or_raise_401


topics_router = APIRouter(prefix='/topics')

class TopicResponseModel(BaseModel):
    topic: Topic
    replies: list[Reply]

@topics_router.get('/', response_model=list[Topic], )
def get_topics(
    skip: int | None = 0,
    take: int |None = 5,
    sorting: str | None = None,
    sort_by: str | None = None,
    search: str | None = None,
    x_token: Optional[str] = Header(None)):

    if x_token:
        user = get_user_or_raise_401(x_token)
    
        if user.role == Role.ADMIN:
            result = topic_service.all(search, skip, take)

            if sorting and (sorting == 'asc' or sorting == 'desc'):
                return topic_service.sorting(result, reverse=sorting == 'desc', attribute=sort_by)
            else:
                return result

        elif user.role == Role.USER:
            private_topics = topic_service.all_non_private_for_user(user.id, search, skip, take)

            if sorting and (sorting == 'asc' or sorting == 'desc'):
                return topic_service.sorting(private_topics, reverse=sorting == 'desc', attribute=sort_by)
            else:
                return private_topics
            
    else: 
        all_topics = topic_service.all_non_private(search, skip, take)

        if sorting and (sorting == 'asc' or sorting == 'desc'):
            return topic_service.sorting(all_topics, reverse=sorting == 'desc', attribute=sort_by)
        else:
            return all_topics


@topics_router.get('/{id}')
def get_topic_by_id(id: int, x_token: Optional[str] = Header(None)):
    topic = topic_service.get_by_id(id)
    if not topic:
        return NotFound(f'Topic with id {id} doesn\'t exist!')
    else:
        if x_token:
            user = get_user_or_raise_401(x_token)
    
            if user.role == Role.ADMIN:
                return TopicResponseModel(
                    topic= topic,
                    replies= reply_service.get_by_topic(topic.id))
    
            elif user.role == Role.USER:
                category = category_service.get_by_id(topic.categories_id)
                if category.is_private:
                    data = category_service.check_if_user_have_access_for_category(user.id, topic.categories_id)
                    if data:
                        return TopicResponseModel(
                        topic= topic,
                        replies= reply_service.get_by_topic(topic.id))
                    else:
                        return Forbidden('You don\'t have permisions to view this topic!')
                else:
                    return TopicResponseModel(
                        topic= topic,
                        replies= reply_service.get_by_topic(topic.id))
        else:
            category = category_service.get_by_id(topic.categories_id)
            if not category.is_private:
                return TopicResponseModel(
                    topic= topic,
                    replies= reply_service.get_by_topic(topic.id))
            else:
                return Forbidden(f'Topic with id {id} is private!')

            

@topics_router.post('/', status_code=201)
def create_topic(topic: Topic, x_token: Optional[str] = Header(None)):
    if not x_token:
        return Unauthorized('You should have registration!')
    
    user = get_user_or_raise_401(x_token)
    
    if user.id != topic.author_id:
        return BadRequest(f"Author id {topic.author_id} in the topic does not match the id {user.id} of the user!")

    if not category_service.exists(topic.categories_id):
        return BadRequest(f'Category {topic.categories_id} does not exist!')

    category = category_service.get_by_id(topic.categories_id)
    if category.is_locked:
        return BadRequest(f'Category {topic.categories_id} is locked!')
    
    return topic_service.create(topic)
    

@topics_router.put('/{id}')
def update_best_reply(id: int, topic: Topic,  x_token: Optional[str] = Header(None)):
    if not x_token:
        return Unauthorized('You should have registration!')
    
    existing_topic = topic_service.get_by_id(id)
    if existing_topic is None:
        return NotFound('Topic with that id doesn\'t exist')
    
    user = get_user_or_raise_401(x_token)
    if user.id == topic.author_id:
    
        reply = reply_service.get_by_id(topic.best_reply_id)
        if reply.topics_id != topic.id:
            return BadRequest('Topic\'s best reply does not belong to the topic!')

        return topic_service.update(existing_topic, topic)
    
    elif user.role == Role.ADMIN:
        return topic_service.update(existing_topic, topic)
    
    else:
        return Forbidden("You can not change the topic!")

