from data.database import insert_query, read_query, update_query
from data.models import Category


def all(search:str, skip:int, take:int):
    if search is None:
        data = read_query('''select id, name, is_private, is_locked from categories
                          LIMIT ?, ?''', (skip, take))
    
    else:
        data = read_query('''select id, name, is_private, is_locked 
                          from categories 
                          where name like ?
                          LIMIT ?, ?''',(f'%{search}%', skip, take))
    
    return (Category.from_query_result(*row) for row in data)

def all_non_private(search:str, skip:int, take:int):
    if search is None:
        data = read_query('''select id, name, is_private, is_locked 
                          from categories 
                          where is_private=0
                          LIMIT ?, ?''', (skip, take))
    
    else:
        data = read_query('''select id, name, is_private , is_locked 
                          from categories 
                          where is_private=0 and name like ?
                          LIMIT ? ?''',(f'%{search}%', skip, take))
    
    return (Category.from_query_result(*row) for row in data)

def private(search: str, user_id: int, skip:int, take:int):

    if search is None:
        data = read_query('''select id, name, is_private, is_locked
                          from categories 
                          where is_private = 0
                          or id in (SELECT category_id from permissions where user_id = ?) 
                          LIMIT ?, ?''', (user_id, skip, take))

    else:
        data = read_query('''select id, name, is_private, is_locked  
                          from categories 
                          where name like ? and (is_private = 0
                          or id in (SELECT category_id from permissions where user_id = ?))) ''', ((f'%{search}%'), user_id,))

    return (Category.from_query_result(*row) for row in data)

def get_by_id(id: int):
    data = read_query('select id, name, is_private, is_locked  from categories where id = ?', (id,))

    return next((Category(id=id, name=name, is_private=is_private, is_locked = is_locked) for id, name, is_private, is_locked in data), None)


def exists(id: int) -> bool:
    return any(
        read_query(
            'select id, name, is_private from categories where id = ?',
            (id,)))


def create(category: Category):
    generated_id = insert_query(
        'insert into categories(name, is_private, is_locked) values(?,?,?)',
        (category.name,category.is_private, category.is_locked))

    category.id = generated_id

    return category

def exist_by_name(category:Category):
     return any(
        read_query(
            'select id, name, is_private, is_locked from categories where name = ?',
            (category.name,)))

def delete(category_id):
    update_query('DELETE FROM categories WHERE categories_id = ?', (category_id,))
    update_query('DELETE FROM categories WHERE id = ?', (category_id,))

def sorting(Categorys: list[Category], *, attribute='', reverse=False):
    if attribute == 'is_private':
        def sorting_fn(p: Category): return p.price
    elif attribute == 'name':
        def sorting_fn(p: Category): return p.name
    else:
        def sorting_fn(p: Category): return p.id

    return sorted(Categorys, key=sorting_fn, reverse=reverse)

def get_private_categories(user_id:int) -> set: 
    data = read_query(
        'SELECT category_id from permissions where user_id = ?', (user_id,))
    
    return set(i[0] for i in data)

def check_if_user_have_access_for_category(user_id:int, category_id:int) -> list: 
    data = read_query(
        '''SELECT category_id from permissions 
        where user_id = ? and category_id = ?''', (user_id, category_id))
    
    return data

def update(old: Category, new: Category):
    merged = Category(
        id=old.id,
        name=new.name or old.name,
        is_private=new.is_private or old.is_private,
        is_locked=new.is_locked or old.is_locked,
        )

    update_query(
        '''UPDATE Categories
         SET
           name = ?, is_private = ?, is_locked= ?
           WHERE id = ? 
        ''',
        (merged.name, merged.is_private, merged.is_locked, merged.id))

    return merged
    