from data.database import insert_query, read_query, update_query
from data.models import Permission

def get_users(category_id):
    data = read_query('''select category_id, user_id, write_permission
                      from permissions
                      where category_id = ?''', (category_id,))
    
    return (Permission.from_query_result(*row) for row in data)

def give_permissions(permission:Permission):
    insert_query('insert into permissions(category_id, user_id, write_permission) values(?,?,?)', \
                 (permission.category_id, permission.user_id, permission.write_permission))
    
    
def update_permission(permissions:Permission, category_id:int, user_id:int):
    update_query(
        ''' UPDATE permissions
            SET
            write_permission = ?
            WHERE category_id = ? and user_id = ?
        ''',
        (permissions.write_permission, category_id, user_id))
    
def delete(category_id:int, user_id:int):
    
    update_query('DELETE FROM permissions WHERE category_id = ? and user_id = ?', (category_id, user_id))