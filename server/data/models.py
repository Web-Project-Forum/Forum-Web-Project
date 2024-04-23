from datetime import date
from typing import Annotated
from pydantic import BaseModel, constr, StringConstraints

class Category(BaseModel):
    id:int | None
    name:str
    is_private:int

    @classmethod
    def from_query_result(cls, id, name, is_private):
        return cls(
            id = id,
            name = name,
            is_private = is_private
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
