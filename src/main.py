from fastapi import FastAPI
from .db import Base, engine
from .routers import legal, images

# создаём таблицы (для dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FORSET Backend")

app.include_router(legal.router)
app.include_router(images.router)
