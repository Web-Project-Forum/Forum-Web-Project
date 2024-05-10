from fastapi import APIRouter, Header
from common.responses import NotFound, BadRequest, Unauthorized
from common.auth import get_user_or_raise_401
from data.models import Messages, MessageResponseModel, MessageModel
from services import message_service

messages_router = APIRouter(prefix = '/messages')

@messages_router.get('/')
def get_messages(x_token: str | None = Header()):
    
    if not x_token:
        return Unauthorized('You should have registration!')
    
    user = get_user_or_raise_401(x_token)

    data = message_service.all(user.id)

    return data

@messages_router.get('/{id}')
def get_message_by_id(id:int, x_token: str | None = Header()):

    if not x_token:
        return Unauthorized('You should have registration!')
    
    user = get_user_or_raise_401(x_token)

    return MessageResponseModel(
        user = user,
        messages = message_service.get_messages_with(user.id, id))


@messages_router.post('/{id}')
def send_message_to_user(message:MessageModel, 
                         id:int,
                         x_token:str | None = Header()):
    
    if not x_token:
        return Unauthorized('You should have registration!')
    
    user = get_user_or_raise_401(x_token)

    data = message_service.create(message, user.id, id)

    return data
    





