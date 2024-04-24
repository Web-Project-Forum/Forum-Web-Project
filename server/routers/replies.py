from fastapi import APIRouter, Header
from common.responses import BadRequest, NotFound, Unauthorized
from data.models import Reply, Role
from server.common.auth import get_user_or_raise_401
from services import topic_service
from services import reply_service

replies_router = APIRouter(prefix='/replies')

@replies_router.get('/', response_model=list[Reply])
def get_replies(
    
    search: str | None = None
):
    result = reply_service.all(search)

    return result



@replies_router.get('/{id}')
def get_reply_by_id(id: int):
    reply = reply_service.get_by_id(id)

    if not reply:
        return NotFound('Reply with that id doesn\'t exist')

    return reply



@replies_router.post('/', status_code=201)
def create_reply(reply: Reply, x_token: str | None = Header()):
    user = get_user_or_raise_401(x_token)
    if user.role == Role.USER:
         return Unauthorized(content='You are not authoriszed to create category!')
    
    if not topic_service.exists(reply.topics_id):
        return BadRequest(f'Topic {reply.topics_id} does not exist')

    return reply_service.create(reply)
