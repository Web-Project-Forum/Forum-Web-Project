from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, StringConstraints, field_validator
from re import match
from os import getenv

class Category(BaseModel):
    id:int | None
    name:str
    is_private:int
    is_locked:int

    @classmethod
    def from_query_result(cls, id, name, is_private, is_locked):
        return cls(
            id = id,
            name = name,
            is_private = is_private,
            is_locked = is_locked
        )

class Topic(BaseModel):
    id:int | None
    title:str
    content:str
    best_reply_id:int | None
    locked:bool
    categories_id:int
    author_id:int
    

    @classmethod
    def from_query_result(cls, id, title, content, best_reply_id, locked, categories_id, author_id):
        return cls(
            id = id,
            title = title,
            content = content,
            best_reply_id = best_reply_id,
            locked = locked,
            categories_id = categories_id,
            author_id = author_id)
    

class Role:
    USER = 'user'
    ADMIN = 'admin'

TUsername = Annotated[str, StringConstraints(pattern=r'^\w{2,30}$')]
TEmail = Annotated[str, StringConstraints(pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')]

class User(BaseModel):
    id: int | None
    username: str
    password: str
    role: str
    email:str

    def is_admin(self):
        return self.role == Role.ADMIN

    @classmethod
    def from_query_result(cls, id, username, password, role, email):
        return cls(
            id=id,
            username=username,
            password=password,
            role=role,
            email=email)
    
    @field_validator('username')
    def validate_username(cls, username:str):
        pattern = r'^\w{2,30}$'
        
        return username if match(pattern, username) is not None else False

    
    @field_validator('password')
    def validate_password(cls, password:str):
        pattern = r'^\w{6,30}$'
        
        return password if match(pattern, password) is not None else False
    
    @field_validator('email')
    def validate_email(cls, email:str):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        return email if match(pattern, email) is not None else False


class LoginData(BaseModel):
    username: TUsername
    password: str

class Key:
    KEY = getenv('KEY')


class Reply(BaseModel):
    id: int | None
    text: str
    topics_id: int
    author_id: int

    @classmethod
    def from_query_result(cls, id, text, topics_id, author_id):
        return cls(
            id=id,
            text=text,
            topics_id=topics_id,
            author_id=author_id)


TText = Annotated[str, StringConstraints(pattern=r'^(\w{1,})')]

class MessageModel(BaseModel):
    text: TText

class Messages(BaseModel):
    id: int | None
    text: TText
    date: datetime
    sender_id: int
    receiver_id:int

    @classmethod
    def from_query_result(cls, id, text, date, sender_id, receiver_id):
        return cls(
            id = id,
            text = text,
            date = date,
            sender_id = sender_id,
            receiver_id = receiver_id)
    
class ConversationsReport(BaseModel):
    id:int
    username:str
    role: str

    @classmethod
    def from_query_result(cls, id, username, role):
        return cls(
            id = id,
            username = username,
            role = role)
    
class MessageResponseModel(BaseModel):
    user: User
    messages: list[Messages]


class Permission(BaseModel):
    category_id:int
    user_id:int
    write_permission:bool

    @classmethod
    def from_query_result(cls, category_id, user_id, write_permission):
        return cls(
            category_id = category_id,
            user_id = user_id,
            write_permission = write_permission)

class VoteUpDownMaps:
    INT_TO_STR = {1: 'up', -1: 'down'}
    STR_TO_INT = {'up': 1, 'down': -1,}

class Vote(BaseModel):
    replies_id:int
    users_id:int
    vote:int
    is_changed:bool

    @classmethod
    def from_query_result(cls, replies_id, users_id, vote, is_changed):
        return cls(
            replies_id = replies_id,
            users_id = users_id,
            vote = vote,
            is_changed = is_changed)

class VoteModel(BaseModel):
    vote:Annotated[str, StringConstraints(pattern = '^up|down$')]
   