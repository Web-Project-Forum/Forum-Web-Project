from data.database import insert_query, read_query
from data.models import Messages, ConversationsReport, MessageModel
from datetime import datetime

def all(user_id :int):
    data = read_query('''select id, username, role
                        from users
                        where id in (select receiver_id 
                        from messages
                        where sender_id = ?)
                        UNION
                        select id, username, role
                        from users
                        where id in(select DISTINCT sender_id
                        from messages
                        where receiver_id = ?)''', (user_id, user_id,))
    
    return (ConversationsReport.from_query_result(*row) for row in data)


def create(message: MessageModel, user_id:int, receiver_id:id):
    generated_id = insert_query(
        'insert into messages(text, date, sender_id, receiver_id) values(?,?,?,?)',
        (message.text, datetime.now(), user_id, receiver_id))
    m_message = Messages(id=generated_id, text = message.text,date=datetime.now(), sender_id=user_id, receiver_id=receiver_id)
    m_message.date = m_message.date.strftime("%H:%M:%S, %m/%d/%Y")

    return m_message

def get_messages_with(user_id:int, contact_id:int):
    data = read_query('''select id, text, date, sender_id, receiver_id
                      from messages
                      where sender_id = ? and receiver_id = ?
                      UNION
                      select id, text, date, sender_id, receiver_id
                      from messages
                      where sender_id = ? and receiver_id = ?
                      order by date''', (user_id, contact_id, contact_id, user_id))
    
    return (Messages.from_query_result(*row) for row in data)