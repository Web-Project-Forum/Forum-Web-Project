from fastapi import APIRouter, Header
from common.auth import is_authenticated, get_user_or_raise_401
from common.responses import Unauthorized, Ok, BadRequest, Forbidden
from data.models import Role, PermissionModel
from services import permission_services, category_service


permissions_router = APIRouter(prefix='/permissions')

@permissions_router.post('/all')
def create_permissions(permissions:PermissionModel, x_token : str | None = Header()):
    if not x_token:
        return Unauthorized(content='You are not authorized!')
    
    if not category_service.exists(permissions.category_id):
        return BadRequest(f'Category {permissions.category_id} does not exist')
    
    user = get_user_or_raise_401(x_token)

    if user.role == Role.USER:
        return Unauthorized(content='You are not authorized! Only admins can give permissions!')
    
    permission_services.give_all_permissions(permissions, permissions.category_id, permissions.user_id)

    return Ok(content= 'Permission created!')

@permissions_router.post('/read')
def create_read_permission(permissions:PermissionModel, x_token : str | None = Header()):
    if not x_token:
        return Unauthorized(content='You are not authorized!')
    
    user = get_user_or_raise_401(x_token)

    if user.role == Role.USER:
        return Forbidden(content='Only admins can give permissions!')
    
    permission_services.give_read_permission(permissions.category_id, permissions.user_id)

    return Ok(content= 'Read permission created!')



@permissions_router.put('/')
def update_permissions(permissions:PermissionModel, x_token : str | None = Header()):
    if not x_token:
        return Unauthorized(content='You are not authorized!')
    
    if not category_service.exists(permissions.category_id):
        return BadRequest(f'Category {permissions.category_id} does not exist')

    user = get_user_or_raise_401(x_token)

    if user.role == Role.USER:
        return Forbidden(content='Only admins can update permissions!')

    permission_services.update_permission(permissions, permissions.category_id, permissions.user_id)

    return Ok(content= 'Permission updated!')