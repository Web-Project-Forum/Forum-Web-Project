from data.database import insert_query, read_query, update_query
from data.models import Category


def all(search):
    if search is None:
        data = read_query('select id, name, is_private from categories')
    
    else:
        data = read_query('''select id, name, is_private 
                          from categories 
                          where name like ?''',(f'%{search}%',))
    
    return (Category.from_query_result(*row) for row in data)


def get_by_id(id: int):
    data = read_query('select id, name, is_private from categories where id = ?', (id,))

    return next((Category(id=id, name=name, is_private=is_private) for id, name, is_private in data), None)


#def exists(id: int):
#    return any(
#        read_query(
#            'select id, name, is_private from categories where id = ?',
#            (id,)))


def create(category: Category):
    generated_id = insert_query(
        'insert into categories(name, is_private) values(?,?)',
        (category.name,category.is_private))

    category.id = generated_id

    return category

def exist(category:Category):
     return any(
        read_query(
            'select id, name, is_private from categories where name = ?',
            (category.name,)))

def delete(category_id):
    update_query('DELETE FROM topics WHERE categories_id = ?', (category_id,))
    update_query('DELETE FROM categories WHERE id = ?', (category_id,))

def sort(Categorys: list[Category], *, attribute='', reverse=False):
    if attribute == 'is_private':
        def sort_fn(p: Category): return p.price
    elif attribute == 'name':
        def sort_fn(p: Category): return p.name
    else:
        def sort_fn(p: Category): return p.id

    return sorted(Categorys, key=sort_fn, reverse=reverse)