from data.database import insert_query, read_query, update_query
from data.models import VoteModel, Vote, VoteUpDownMaps


def create(reply_id:int, user_id:int, vote_model:VoteModel):

    insert_query('insert into votes(replies_id, users_id, vote) values(?,?,?)',\
                 (reply_id, user_id, VoteUpDownMaps.STR_TO_INT[vote_model.vote]))
    
    vote = Vote(replies_id = reply_id, users_id = user_id, vote = VoteUpDownMaps.STR_TO_INT[vote_model.vote], is_changed=False)
    return vote
    

def get_vote(reply_id:int, user_id:int):
    data = read_query('''
                      select replies_id, users_id, vote, is_change
                      from votes
                      where replies_id = ? and users_id = ?''',(reply_id, user_id))
    
    return next((Vote(replies_id=replies_id, users_id=users_id, vote=vote, is_changed = is_changed) \
                  for replies_id, users_id, vote, is_changed in data), None)

def total_vote(reply_id:int):
    data = read_query('''select sum(vote) 
                      from votes
                      where replies_id = ?''', (reply_id,))
    
    return data


def change_vote(old:Vote, new:VoteModel):

    merged = Vote(
        replies_id=old.replies_id,
        users_id=old.users_id ,
        vote=VoteUpDownMaps.STR_TO_INT[new.vote] ,
        is_changed=1,
        )


    update_query(
        '''UPDATE votes
         SET
           replies_id = ?, users_id = ?, vote = ?, is_change = ?
           WHERE replies_id = ? and users_id = ?
        ''',
        (merged.replies_id, merged.users_id, merged.vote, merged.is_changed, old.replies_id, old.users_id))

    return merged

def check_if_user_can_vote(reply_id:int, user_id:int):
    data = read_query('''select c.id 
                    from replies as r
                    join topics as t on r.topics_id = t.id
                    join categories c on t.categories_id = c.id
                    where r.id = ? and 
                    c.id in (
                            select category_id
                            from permissions
                            where user_id = ? 
                            union
                            select id
                            from categories
                            where is_private = 0)
                ''', (reply_id, user_id))
    
    return data
