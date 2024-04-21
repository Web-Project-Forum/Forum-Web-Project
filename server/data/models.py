from datetime import date
from pydantic import BaseModel, constr

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

    @classmethod
    def from_query_result(cls, id, title, content, best_reply, locked, categories_id):
        return cls(
            id = id,
            title = title,
            content = content,
            best_reply = best_reply,
            locked = locked,
            categories_id = categories_id)
