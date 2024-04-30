from data.models import Topic
from data.database import insert_query, read_query, update_query



def all(search: str = None, offset: int = 0, limit: int = 2):
    if search is None:
        data = read_query(
            '''SELECT id, title, content, locked, categories_id, author_id, best_reply_id
               FROM topics''')
#               LIMIT ?, ?''', (offset, limit))
    else:
        data = read_query(
            '''SELECT id, title, content, locked, categories_id, author_id, best_reply_id
               WHERE title LIKE ?''', (f'%{search}%'))
#               LIMIT ?, ?''', (f'%{search}%', offset, limit))

    return [Topic.from_query_result(*row) for row in data]



def get_by_id(id: int):
    data = read_query(
        '''SELECT id, title, content, locked, categories_id, author_id, best_reply_id
            FROM topics

            WHERE id = ?''', (id,))

    return next((Topic.from_query_result(*row) for row in data), None)



def get_many(ids: list[int]):
    ids_joined = ','.join(str(id) for id in ids)
    data = read_query(f'''
            SELECT id, title, content, locked, categories_id, author_id, best_reply_id
            FROM topics

            WHERE id IN ({ids_joined})''')

    return [Topic.from_query_result(*row) for row in data]



def get_by_category(category_id: int):
    data = read_query(
        '''SELECT id, title, content, locked, categories_id, author_id, best_reply_id
            FROM topics
            WHERE categories_id = ?''', (category_id,)
             )

    return (Topic.from_query_result(*row) for row in data)



def sorting(topics: list[Topic], *, attribute='best_reply', reverse=False):
    if attribute == 'best_reply':
        def sort_fn(p: Topic): return p.best_reply
    elif attribute == 'title':
        def sort_fn(p: Topic): return p.title
    else:
        def sort_fn(p: Topic): return p.id

    return sorted(topics
    , key=sort_fn, reverse=reverse)




#def create(topic: Topic):
#    generated_id = insert_query(
#        'INSERT INTO topics(title, content, locked, categories_id, author_id, best_reply_id) VALUES(?,?,?,?,?,?)',
#        (topic.title, topic.content, topic.locked, topic.categories_id, topic.author_id, topic.best_reply_id))
#
#    topic.id = generated_id
#
#    return topic
def create(topic: Topic):
    # Check if best_reply_id is None and handle accordingly
    if topic.best_reply_id is None:
        query = 'INSERT INTO topics(title, content, locked, categories_id, author_id) VALUES(?,?,?,?,?)'
        params = (topic.title, topic.content, topic.locked, topic.categories_id, topic.author_id)
    else:
        query = 'INSERT INTO topics(title, content, locked, categories_id, author_id, best_reply_id) VALUES(?,?,?,?,?,?)'
        params = (topic.title, topic.content, topic.locked, topic.categories_id, topic.author_id, topic.best_reply_id)

    generated_id = insert_query(query, params)

    topic.id = generated_id

    return topic


def exists(id: int):
    return any(
        read_query(
            '''SELECT id, title, content, locked, categories_id, author_id, best_reply_id 
            from topics where id = ?''',
            (id,)))



def update(old: Topic, new: Topic):
    merged = Topic(
        id = old.id,
        title = new.title or old.title,
        content = new.content or old.content,
        locked = new.locked or old.locked,
        categories_id = new.categories_id or old.categories_id,
        author_id = new.author_id or old.author_id,
        best_reply_id = new.best_reply or old.best_reply
        )

    update_query(
        '''UPDATE topics
         SET
           title = ?, content = ?, locked = ?, categories_id = ?, author_id = ?, best_reply_id = ? 
           WHERE id = ? 
        ''',
        (merged.title, merged.content, merged.locked, merged.categories_id, merged.author_id, merged.best_reply_id, merged.id))

    return merged
