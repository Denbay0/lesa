# src/backend/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime

class LegalEntityCreate(BaseModel):
    company_name: str
    inn: str
    address: str
    contact_email: EmailStr
    contact_phone: str

class LegalEntityRead(LegalEntityCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ImageUploadRead(BaseModel):
    id: int
    filename: str
    content_type: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
