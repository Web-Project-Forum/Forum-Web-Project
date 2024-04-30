from data.database import insert_query, read_query, update_query

def give_all_permissions(category_id:int, user_id:int):
    insert_query('insert into permissions(category_id, user_id, read_permission, write_permission) values(?,?,?,?)', \
                 (category_id, user_id, True, True))
    
def give_read_permission(category_id:int, user_id:int):
    insert_query('insert into permissions(category_id, user_id, read_permission, write_permission) values(?,?,?,?)', \
                 (category_id, user_id, True, False))
    
def give_write_permission(category_id:int, user_id:int):
    insert_query('insert into permissions(category_id, user_id, read_permission, write_permission) values(?,?,?,?)', \
                 (category_id, user_id, False, True))