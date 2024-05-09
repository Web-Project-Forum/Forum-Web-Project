from mariadb import connect
from mariadb.connections import Connection
from os import getenv


def _get_connection() -> Connection:
    return connect(
        host='localhost',
        user='root',
        password=getenv('PASSWORD_mariadb'),
        port=3306,
        database='webproject',
        autocommit = True
    )


def read_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        
        return list(cursor)


def insert_query(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return cursor.lastrowid


def update_query(sql: str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return cursor.rowcount
