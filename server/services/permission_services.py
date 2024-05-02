from data.database import insert_query, read_query, update_query
from data.models import PermissionModel

def give_all_permissions(permission:PermissionModel, category_id:int, user_id:int):
    insert_query('insert into permissions(category_id, user_id, write_permission) values(?,?,?)', \
                 (category_id, user_id, True))
    
def give_read_permission(category_id:int, user_id:int):
    insert_query('insert into permissions(category_id, user_id, write_permission) values(?,?,?)', \
                 (category_id, user_id, False))
    


def update_permission(permissions:PermissionModel, category_id:int, user_id:int):
    update_query(
        ''' UPDATE permissions
            SET
            write_permission = ?
            WHERE category_id = ? and user_id = ?
        ''',
        (permissions.write_permission, category_id, user_id))