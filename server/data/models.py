from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, constr, StringConstraints

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
    locked:bool
    categories_id:int
    author_id:int
    best_reply_id:Optional[int]

    @classmethod
    def from_query_result(cls, id, title, content, locked, categories_id, author_id, best_reply_id):
        return cls(
            id = id,
            title = title,
            content = content,
            locked = locked,
            categories_id = categories_id,
            author_id = author_id,
            best_reply_id = best_reply_id)
    

class Role:
    USER = 'user'
    ADMIN = 'admin'

TUsername = Annotated[str, StringConstraints(pattern=r'^\w{2,30}$')]

class User(BaseModel):
    id: int | None
    username: TUsername
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


class LoginData(BaseModel):
    username: TUsername
    password: str

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

class Messages(BaseModel):
    id: int | None
    text: str
    date: datetime
    sender_id: int
    receiver_id:int

    @classmethod
    def from_query_result(cls, id, text, date, sender_id, receiver_id):
        return cls(
            id=id,
            text=text,
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
            username=username,
            role=role)
    
class MessageResponseModel(BaseModel):
    user: User
    messages: list[Messages]