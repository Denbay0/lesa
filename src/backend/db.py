# src/backend/db.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Получаем абсолютный путь к папке backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Склеиваем путь до файла database.db внутри backend
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")

# SQLite URL с указанием пути
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Для SQLite нужен дополнительный аргумент
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
