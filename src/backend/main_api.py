# src/backend/main_api.py

from fastapi import FastAPI
from .db import Base, engine
from .routers import legal, images

# (для разработки автоматически создаём таблицы)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FORSET Backend")

# Регистрируем роуты
app.include_router(legal.router)
app.include_router(images.router)
