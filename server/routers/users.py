from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest
from data.models import LoginData,User
from services import users_service


users_router = APIRouter(prefix='/users')


@users_router.post('/login')
def login(data: LoginData):
    user = users_service.try_login(data.username, data.password)

    if user:
        token = users_service.create_token(user)
        return {'token': token}
    else:
        return BadRequest('Invalid login data')


@users_router.get('/info')
def user_info(x_token: str | None = Header()):
    if  not x_token :
        return BadRequest('No No')
    return get_user_or_raise_401(x_token)


@users_router.post('/register')
def register(data: User):

    if data.email and data.username and data.password:
        user = users_service.create(data.username, data.password, data.email)
    else:
        if not data.email:
            return BadRequest(content= 'Email should contain symbol "@" and at least one full stop "."')
        if not data.username:
            return BadRequest(content= 'Username should be between 2 and 30 symbols.')
        if not data.password:
            return BadRequest(content= 'Password should be between 6 and 30 symbols.')
    
    return user or BadRequest(f'Username {data.username} is taken.')
