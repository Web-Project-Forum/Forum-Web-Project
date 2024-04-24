from datetime import date
from typing import Annotated
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
    best_reply:int
    locked:bool
    categories_id:int
    users_id:int

    @classmethod
    def from_query_result(cls, id, title, content, best_reply, locked, categories_id, users_id):
        return cls(
            id = id,
            title = title,
            content = content,
            best_reply = best_reply,
            locked = locked,
            categories_id = categories_id,
            users_id = users_id)
    

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
    best_reply_text: str
    topics_id: int
    best_reply_id: int
    author_id: int

    @classmethod
    def from_query_result(cls, id, text, best_reply_text, topics_id, best_repy_id, author_id):
        return cls(
            id=id,
            text=text,
            best_reply_text=best_reply_text,
            topics_id=topics_id,
            best_repy_id=best_repy_id,
            author_id=author_id)