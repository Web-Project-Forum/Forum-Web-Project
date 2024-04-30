from data.database import insert_query, read_query, update_query
from data.models import PermissionModel

def give_all_permissions(permission:PermissionModel, category_id:int, user_id:int):
    insert_query('insert into permissions(category_id, user_id, read_permission, write_permission) values(?,?,?,?)', \
                 (category_id, user_id, permission.read_permission, permission.write_permission))
    
#def give_read_permission(category_id:int, user_id:int):
#    insert_query('insert into permissions(category_id, user_id, read_permission, write_permission) values(?,?,?,?)', \
#                 (category_id, user_id, True, False))
#    
#def give_write_permission(category_id:int, user_id:int):
#    insert_query('insert into permissions(category_id, user_id, read_permission, write_permission) values(?,?,?,?)', \
#                 (category_id, user_id, False, True))

def update_permission(permissions:PermissionModel, category_id:int, user_id:int):
    update_query(
        '''UPDATE permissions
         SET
           read_permission = ?, write_permission = ?
           WHERE category_id = ? and user_id = ?
        ''',
        (permissions.read_permission, permissions.write_permission, category_id, user_id))