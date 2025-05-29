from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .db import Base

class LegalEntity(Base):
    __tablename__ = "legal_entities"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    inn = Column(String(12), nullable=False, unique=True)
    address = Column(String(512), nullable=False)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ImageUpload(Base):
    __tablename__ = "image_uploads"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(50), nullable=False)
    legal_entity_id = Column(Integer, ForeignKey("legal_entities.id"), nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
