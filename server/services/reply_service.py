from data.models import Reply
from data.database import insert_query, read_query

def all(search):
    if search is None:
        data = read_query('''SELECT id, text, best_reply_text, topics_id, best_reply_id, author_id
                          from replies''')
    
    else:
        data = read_query('''select id, text, best_reply_text, topics_id, best_reply_id, author_id 
                          from replies 
                          where text like ?''',(f'%{search}%',))
    
    return (Reply.from_query_result(*row) for row in data)

def get_by_id(id: int):
    data = read_query(
        '''SELECT id, text, best_reply_text, topics_id, best_reply_id, author_id
            FROM replies

            WHERE id = ?''', (id,))

    return next[(Reply.from_query_result(*row) for row in data), None]

def create(reply: Reply):
    generated_id = insert_query(
        'INSERT INTO replies(text, best_reply_text, topics_id, best_reply_id, author_id) VALUES(?,?,?,?,?)',
        (reply.text, reply.best_reply_text, reply.topics_id, reply.best_reply_id, reply.author_id))

    reply.id = generated_id

    return reply