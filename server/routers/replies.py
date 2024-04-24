from fastapi import APIRouter, HTTPException
from common.responses import BadRequest
from data.models import Reply
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
        raise HTTPException(status_code=404, detail="Reply not found!")

    return reply

@replies_router.post('/', status_code=201)
def create_reply(reply: Reply):
    if not topic_service.exist(reply.topics_id):
        return BadRequest(f'Topic {reply.topics_id} does not exist')

    return reply_service.create(reply)
