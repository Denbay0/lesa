from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from .. import models, db, schemas
import os
import uuid

router = APIRouter(prefix="/images", tags=["images"])
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=schemas.ImageUploadRead)
def upload_image(
    file: UploadFile = File(...),
    legal_entity_id: int | None = None,
    session: Session = Depends(db.SessionLocal),
):
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    # сохраняем файл на диск
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(file.file.read())
    # записываем в БД
    img = models.ImageUpload(
        filename=filename,
        content_type=file.content_type,
        legal_entity_id=legal_entity_id,
    )
    session.add(img)
    session.commit()
    session.refresh(img)
    return img
