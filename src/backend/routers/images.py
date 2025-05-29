# src/backend/routers/images.py

import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from .. import models, db, schemas

router = APIRouter(prefix="/images", tags=["images"])

# Делаем путь к upload-папке рядом с backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()

@router.post(
    "/",
    response_model=schemas.ImageUploadRead,
    summary="Загрузить картинку"
)
def upload_image(
    file: UploadFile = File(...),
    legal_entity_id: int | None = None,
    session: Session = Depends(get_db),
):
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Генерируем уникальное имя и сохраняем
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(file.file.read())

    # Пишем метаданные в БД
    img = models.ImageUpload(
        filename=filename,
        content_type=file.content_type,
        legal_entity_id=legal_entity_id,
    )
    session.add(img)
    session.commit()
    session.refresh(img)
    return img

@router.get(
    "/{image_id}/file",
    response_class=FileResponse,
    summary="Скачать картинку по ID"
)
def get_image_file(image_id: int, session: Session = Depends(get_db)):
    img = session.query(models.ImageUpload).get(image_id)
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")

    file_path = os.path.join(UPLOAD_DIR, img.filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File missing on server")

    return FileResponse(
        path=file_path,
        media_type=img.content_type,
        filename=img.filename
    )
