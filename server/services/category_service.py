from data.database import insert_query, read_query, update_query
from data.models import Category


def all(search):
    if search is None:
        data = read_query('select id, name, is_private, is_locked from categories')
    
    else:
        data = read_query('''select id, name, is_private, is_locked 
                          from categories 
                          where name like ?''',(f'%{search}%',))
    
    return (Category.from_query_result(*row) for row in data)

def all_non_private(search):
    if search is None:
        data = read_query('select id, name, is_private, is_locked from categories where is_private=0')
    
    else:
        data = read_query('''select id, name, is_private , is_locked 
                          from categories 
                          where is_private=0 and name like ?''',(f'%{search}%',))
    
    return (Category.from_query_result(*row) for row in data)

def private(search: str, user_id: int):
    categories_id = get_private_categories(user_id)
    if not categories_id:   # if we pass empty tuple as parametar, occur mariadb.ProgrammingError
        categories_id = (0,)

    if search is None:
        data = read_query('''select id, name, is_private, is_locked
                          from categories 
                          where is_private = 0
                          or id in (?) ''',tuple(categories_id))

    
    else:
        # It does't return the correct data with search-on in python but the same query works in the database
        #data = read_query('''select id, name, is_private 
        #                  from categories 
        #                  where name like ? and(is_private = 0 or id in (?))''', ((f'%{search}%'), tuple(categories_id)))
        
        without_search_data = read_query('''select id, name, is_private, is_locked  
                          from categories 
                          where is_private = 0
                          or id in (?) ''',tuple(categories_id))
        data = []
        for el in without_search_data:
            if search in el[1]:
                data.append(el)
        
    return (Category.from_query_result(*row) for row in data)

def get_by_id(id: int):
    data = read_query('select id, name, is_private, is_locked  from categories where id = ?', (id,))

    return next((Category(id=id, name=name, is_private=is_private, is_locked = is_locked) for id, name, is_private, is_locked in data), None)


def exists(id: int):
    return any(
        read_query(
            'select id, name, is_private from categories where id = ?',
            (id,)))


def create(category: Category):
    generated_id = insert_query(
        'insert into categories(name, is_private) values(?,?)',
        (category.name,category.is_private))

    category.id = generated_id

    return category

def exist_by_name(category:Category):
     return any(
        read_query(
            'select id, name, is_private, is_locked from categories where name = ?',
            (category.name,)))

def delete(category_id):
    update_query('DELETE FROM Categorys WHERE categories_id = ?', (category_id,))
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

def check_if_user_have_access_for_category(user_id:int, category_id:int) -> list: 
    data = read_query(
        '''SELECT categories_id from permissions 
        where users_id = ? and categories_id = ?''', (user_id, category_id))
    
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
    