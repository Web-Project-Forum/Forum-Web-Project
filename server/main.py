from fastapi import FastAPI
from routers.categories import categories_router
from routers.topics import topic_router



app = FastAPI()
app.include_router(categories_router)
app.include_router(topic_router)
