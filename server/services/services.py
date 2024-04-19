from fastapi import FastAPI
from routers.product import product_router



app = FastAPI()
app.include_router(product_router)
