from fastapi import APIRouter, Header
from common.responses import NotFound, BadRequest, Unauthorized
from common.auth import get_user_or_raise_401
from data.models import Messages
#from services.message_service import

messages_router = APIRouter(prefix = '/messages')

@messages_router.get('/')
def get_messages(x_token: str | None = Header()):
    if not x_token:
        return Unauthorized('You should have registration!')
    
    
