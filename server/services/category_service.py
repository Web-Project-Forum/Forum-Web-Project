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

def all_non_private(search):
    if search is None:
        data = read_query('select id, name, is_private from categories where is_private=0')
    
    else:
        data = read_query('''select id, name, is_private 
                          from categories 
                          where is_private=0 and name like ?''',(f'%{search}%',))
    
    return (Category.from_query_result(*row) for row in data)

def private(search, user_id:int):
    categories_id = get_private_categories(user_id)
    if search is None:
        data = read_query('''select id, name, is_private 
                          from categories 
                          where is_private = 0
                          or id in (?) ''',tuple(categories_id))

    
    else:
        temp = list(categories_id)
        data = read_query('''select id, name, is_private from categories where (is_private = 0 or id in (?)) and name like ?''', (list(categories_id), (f'%{search}%')))
        
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

def get_private_categories(user_id:int) -> set: 
    data = read_query(
        'SELECT categories_id from permissions where users_id = ?', (user_id,))
    
    return set(i[0] for i in data)
    