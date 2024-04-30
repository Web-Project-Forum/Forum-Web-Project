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


#@users_router.get('/orders', response_model=list[Order])
#def user_info(x_token: str = Header()):
#    user = get_user_or_raise_401(x_token)
#
#    return order_service.get_user_orders(user)


@users_router.post('/register')
def register(data: User):

    if data.email:
        user = users_service.create(data.username, data.password, data.email)
    else:
        return BadRequest(content= 'Email should contain symbol "@" and at least one full stop "."')
    
    return user or BadRequest(f'Username {data.username} is taken.')
