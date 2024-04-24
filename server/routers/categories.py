from fastapi import APIRouter, Header
from pydantic import BaseModel
from data.models import Category,Topic,Role
from services import topic_service
from services import category_service
from common.responses import NotFound, BadRequest, Ok, Unauthorized
from common.auth import get_user_or_raise_401


class CategoryResponseModel(BaseModel):
    category: Category
    topics: list[Topic]


categories_router = APIRouter(prefix='/categories')


@categories_router.get('/')
def get_catgories(
    sort: str | None = None,
    sort_by: str | None = None,
    search: str | None = None,
    x_token: str | None = Header()
):
    if not x_token:
        data = category_service.all_non_private(search)

    else:
        user = get_user_or_raise_401(x_token)

        if user.role == Role.ADMIN:
            data = category_service.all(search)
        else:
            data = category_service.private(search, user.id)


    if sort and (sort == 'asc' or sort == 'desc'):
        return category_service.sort(data, reverse=sort == 'desc', attribute=sort_by)
    
    return data


#@categories_router.get('/')
#def get_categories():
#    return [    
#        CategoryResponseModel(
#            category=category,
#            topics=topic_service.get_by_category(category.id))  # known (n+1) problem
#        for category in category_service.all()]

@categories_router.get('/{id}')
def get_category_by_id(id: int, x_token: str | None = Header()):

    category = category_service.get_by_id(id)

    if category is None:
        return NotFound('Category with that id doesn\'t exist')
    
    else:
        if category.is_private and not x_token:
            return Unauthorized(content='You are not authoriszed to view this category!')
        
        elif category.is_private and x_token:
            user = get_user_or_raise_401(x_token)

            if user.role == Role.USER:
                if category_service.check_if_user_have_access_for_category(user.id, category.id):
                    pass
                else:
                    return Unauthorized(content='You are not authoriszed to view this category!')

        
        return CategoryResponseModel(
            category=category,
            topics=topic_service.get_by_category(category.id))


@categories_router.post('/')
def create_category(category: Category, x_token: str | None = Header()):
    user = get_user_or_raise_401(x_token)
    if user.role == Role.USER:
         return Unauthorized(content='You are not authoriszed to create category!')
    
    if category_service.exist_by_name(category):
        return BadRequest('Category with that name already exist!')
    
    created_category = category_service.create(category)

    return created_category #ResponseModel(category=created_category, products=[])

@categories_router.put('/{id}')
def update_category(id:int, category:Category, x_token: str | None = Header()):
    user = get_user_or_raise_401(x_token)
    if user.role == Role.USER:
        return Unauthorized(content='You are not authoriszed to update category!')
    
    if not category_service.exists(id):
        return BadRequest(f'Category {id} does not exist')

    existing_category = category_service.get_by_id(id)
    
    return category_service.update(existing_category, category)



@categories_router.delete('/{id}')
def delete_category(id:int, x_token: str | None = Header()):
    user = get_user_or_raise_401(x_token)
    if user.role == Role.USER:
         return Unauthorized(content='You are not authoriszed to delete category!')
    
    category = category_service.get_by_id(id)
    if not category:
        return NotFound('Category with that id doesn\'t exist')
    
    category_service.delete(id)

    return Ok(content= f'Category "{category.name}"  was deleted')


