from data.database import insert_query, read_query
from data.models import Role, User, Key
from mariadb import IntegrityError
from datetime import datetime, timezone, timedelta
import jwt
from hashlib import sha256


_EXP_TIME_TOKEN = 2

def _hash_password(password: str):

    return sha256(password.encode('utf-8')).hexdigest()


def find_by_username(username: str) -> User | None:
    data = read_query(
        'SELECT id, username, password, role, email FROM users WHERE username = ?',
        (username,))

    return next((User.from_query_result(*row) for row in data), None)


def try_login(username: str, password: str) -> User | None:
    user = find_by_username(username)

    hashed_password = _hash_password(password)

    return user if user and user.password == hashed_password else None


def create(username: str, password: str, email) -> User | None:
    
    hashed_password = _hash_password(password)

    try:
        generated_id = insert_query(
            'INSERT INTO users(username, password, role, email) VALUES (?,?,?,?)',
            (username, hashed_password, Role.USER, email))

        return User(id=generated_id, username=username, password='xxxxxxxxx', role=Role.USER,email=email)

    except IntegrityError:
        # mariadb raises this error when a constraint is violated
        # in that case we have duplicate usernames
        return None


def create_token(user: User) -> str:

    load = {"id":user.id,
           "username":user.username,
           "role":user.role,
           "iat": datetime.now(tz=timezone.utc),
           "exp":(datetime.now(tz=timezone.utc) + timedelta(hours=_EXP_TIME_TOKEN))
            }
    encoded = jwt.encode(payload = load, key = Key.KEY, algorithm="HS256")
   
    return encoded


def is_authenticated(token: str) -> bool:
    try:
        decoded = jwt.decode(token, Key.KEY, algorithms=["HS256"])
    
    except jwt.ExpiredSignatureError:
        return False

    return any(read_query(
        'SELECT 1 FROM users where id = ? and username = ?',
        (decoded['id'], decoded['username'])))


def from_token(token: str) -> User | None:
    try:
        decoded = jwt.decode(token, Key.KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return False
    
    return find_by_username(decoded['username'])