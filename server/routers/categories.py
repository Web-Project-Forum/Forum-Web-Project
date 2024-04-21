from fastapi import APIRouter
from pydantic import BaseModel
from data.models import Category,Topic
from services import topic_service
from services import category_service
from common.responses import NotFound, BadRequest, Ok


class CategoryResponseModel(BaseModel):
    category: Category
    topics: list[Topic]


categories_router = APIRouter(prefix='/categories')


@categories_router.get('/')
def get_catgories(
    sort: str | None = None,
    sort_by: str | None = None,
    search: str | None = None
):

    data = category_service.all(search)

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
def get_category_by_id(id: int):
    category = category_service.get_by_id(id)

    if category is None:
        return NotFound('Category with that id doesn\'t exist')
    else:
        return CategoryResponseModel(
            category=category,
            topics=topic_service.get_by_category(category.id))


@categories_router.post('/')
def create_category(category: Category):
    if category_service.exist(category):
        return BadRequest('Category with that name already exist!')
    
    created_category = category_service.create(category)

    return created_category #ResponseModel(category=created_category, products=[])

@categories_router.delete('/{id}')
def delete_category(id:int):
    category = category_service.get_by_id(id)
    if not category:
        return NotFound('Category with that id doesn\'t exist')
    
    category_service.delete(id)

    return Ok(content= f'Category "{category.name}"  was deleted')


