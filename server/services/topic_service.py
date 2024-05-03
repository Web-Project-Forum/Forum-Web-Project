from data.models import Topic
from data.database import insert_query, read_query, update_query



def all(search: str = None, skip: int = None, take: int = None):
    if search is None:
        data = read_query(
            '''SELECT id, title, content, best_reply_id, locked, categories_id, author_id
               FROM topics
               LIMIT ?, ?''', (skip, take))
    else:
        data = read_query(
            '''SELECT id, title, content, best_reply_id, locked, categories_id, author_id
               FROM topics
               WHERE title LIKE ?
               LIMIT ?, ?''', (f'%{search}%', skip, take))

    return [Topic.from_query_result(*row) for row in data]



def get_by_id(id: int):
    data = read_query(
        '''SELECT id, title, content, best_reply_id, locked, categories_id, author_id
            FROM topics

            WHERE id = ?''', (id,))

    return next((Topic.from_query_result(*row) for row in data), None)



def get_many(ids: list[int]):
    ids_joined = ','.join(str(id) for id in ids)
    data = read_query(f'''
            SELECT id, title, content, best_reply_id, locked, categories_id, author_id
            FROM topics

            WHERE id IN ({ids_joined})''')

    return [Topic.from_query_result(*row) for row in data]



def get_by_category(category_id: int):
    data = read_query(
        '''SELECT id, title, content, best_reply_id, locked, categories_id, author_id
            FROM topics
            WHERE categories_id = ?''', (category_id,)
             )

    return (Topic.from_query_result(*row) for row in data)



def sorting(topics: list[Topic], *, attribute='best_reply_id', reverse=False):
    if attribute == 'best_reply_id':
        def sort_fn(p: Topic): return p.best_reply
    elif attribute == 'title':
        def sort_fn(p: Topic): return p.title
    else:
        def sort_fn(p: Topic): return p.id

    return sorted(topics
    , key=sort_fn, reverse=reverse)



def create(topic: Topic):
    generated_id = insert_query(
        'INSERT INTO topics(title, content, best_reply_id, locked, categories_id, author_id) VALUES(?,?,?,?,?,?)',
        (topic.title, topic.content, topic.best_reply_id, topic.locked, topic.categories_id, topic.author_id
        ))

    topic.id = generated_id

    return topic


def exists(id: int):
    return any(
        read_query(
            '''SELECT id, title, content, best_reply_id, locked, categories_id, author_id
                FROM topics 
                WHERE id = ?''', (id,)))



def update_best_reply_id(old: Topic, new: Topic):
    merged = Topic(
        id = old.id,
        title = old.title,
        content = old.content,
        best_reply_id = new.best_reply_id or old.best_reply_id,
        locked = old.locked,
        categories_id = old.categories_id,
        author_id =  old.author_id,
        )

    update_query(
        '''UPDATE topics
         SET
           best_reply_id = ? 
           WHERE id = ? 
        ''',
        (merged.best_reply_id, merged.id))

    return merged


