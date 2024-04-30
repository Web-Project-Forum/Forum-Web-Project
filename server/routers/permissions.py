from fastapi import APIRouter, Header
from common.auth import is_authenticated, get_user_or_raise_401
from common.responses import Unauthorized, Ok, BadRequest
from data.models import Role, PermissionModel
from services import permission_services, category_service


permissions_router = APIRouter(prefix='/permissions')

@permissions_router.post('/{category_id}/user/{user_id}')
def create_permissions(permissions:PermissionModel, category_id:int, user_id:int, x_token : str | None = Header()):
    if not x_token:
        return Unauthorized(content='You are not authorized!')
    
    if not category_service.exists(category_id):
        return BadRequest(f'Category {category_id} does not exist')
    
    user = get_user_or_raise_401(x_token)

    if user.role == Role.USER:
        return Unauthorized(content='You are not authorized! Only admins can give permissions!')
    
    permission_services.give_all_permissions(permissions, category_id, user_id)

    return Ok(content= 'Permission created!')

#@permissions_router.post('/read/{category_id}/user/{user_id}')
#def create_read_permission(category_id:int, user_id:int, x_token : str | None = Header()):
#    if not x_token:
#        return Unauthorized(content='You are not authorized!')
#    
#    user = get_user_or_raise_401(x_token)
#
#    if user.role == Role.USER:
#        return Unauthorized(content='You are not authorized! Only admins can give permissions!')
#    
#    permission_services.give_read_permission(category_id, user_id)
#
#    return Ok(content= 'Read permission created!')
#
#@permissions_router.post('/write/{category_id}/user/{user_id}')
#def create_write_permissions(category_id:int, user_id:int, x_token : str | None = Header()):
#    if not x_token:
#        return Unauthorized(content='You are not authorized!')
#    
#    user = get_user_or_raise_401(x_token)
#
#    if user.role == Role.USER:
#        return Unauthorized(content='You are not authorized! Only admins can give permissions!')
#    
#    permission_services.give_write_permission(category_id, user_id)
#    
#    return Ok(content= 'Write permission created!')


@permissions_router.put('/{category_id}/user/{user_id}')
def update_permissions(permissions:PermissionModel, category_id:int, user_id:int, x_token : str | None = Header()):
    if not x_token:
        return Unauthorized(content='You are not authorized!')
    
    if not category_service.exists(category_id):
        return BadRequest(f'Category {category_id} does not exist')

    user = get_user_or_raise_401(x_token)

    if user.role == Role.USER:
        return Unauthorized(content='You are not authorized! Only admins can update permissions!')

    permission_services.update_permission(permissions, category_id, user_id)

    return Ok(content= 'Permission updated!')