from data.models import Topic
from data.database import insert_query, read_query, update_query


def all(search: str = None):
    if search is None:
        data = read_query(
            '''SELECT id, title, content, best_reply, locked, categories_id, users_id
               FROM topics
               ''')
    else:
        data = read_query(
            '''SELECT id, title, content, best_reply, locked, categories_id, users_id
               FROM topics

               WHERE title LIKE ?''', (f'%{search}%',))

    return (Topic.from_query_result(*row) for row in data)


def get_by_id(id: int):
    data = read_query(
        '''SELECT id, title, content, best_reply, locked, categories_id, users_id
            FROM topics

            WHERE id = ?''', (id,))

    return next((Topic.from_query_result(*row) for row in data), None)


def get_many(ids: list[int]):
    ids_joined = ','.join(str(id) for id in ids)
    data = read_query(f'''
            SELECT id, title, content, best_reply, locked, categories_id, users_id
            FROM topics

            WHERE id IN ({ids_joined})''')

    return [Topic.from_query_result(*row) for row in data]


def get_by_category(category_id: int):
    data = read_query(
        '''SELECT id, title, content, best_reply, locked, categories_id, users_id
            FROM topics
            WHERE categories_id = ?''', (category_id,)
             )

    return (Topic.from_query_result(*row) for row in data)


def sort(topics: list[Topic], *, attribute='best_reply', reverse=False):
    if attribute == 'best_reply':
        def sort_fn(p: Topic): return p.best_reply
    elif attribute == 'title':
        def sort_fn(p: Topic): return p.title
    else:
        def sort_fn(p: Topic): return p.id

    return sorted(topics
    , key=sort_fn, reverse=reverse)


def create(Topic: Topic):
    generated_id = insert_query(
        'INSERT INTO topics(title, content, best_reply, locked, categories_id) VALUES(?,?,?,?,?)',
        (Topic.title, Topic.content, Topic.best_reply, Topic.locked, Topic.categories_id
        ))

    Topic.id = generated_id

    return Topic


def update(old: Topic, new: Topic):
    merged = Topic(
        id=old.id,
        title=new.title or old.title,
        content=new.content or old.content,
        best_reply=new.best_reply or old.best_reply,
        locked =new.locked or old.locked,
        categories_id = new.categories_id or old.categories_id
        )

    update_query(
        '''UPDATE topics
         SET
           title = ?, content = ?, best_reply = ?, locked, categories_id
            = ?
           WHERE id = ? 
        ''',
        (merged.title, merged.content, merged.best_reply, \
         merged.locked, merged.categories_id, merged.id))

    return merged
