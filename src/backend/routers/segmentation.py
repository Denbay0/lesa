import os
import cv2
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse

from ultralytics import YOLO

from ..db import SessionLocal
from ..models import ImageUpload

# 1. Настройка роутера
router = APIRouter(prefix="/segment", tags=["segment"])

# 2. Доступ к базе

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Путь к папке с загруженными файлами и модели
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "best.pt")

# 4. Загрузка модели (Ultralytics YOLOv8/V9 compatible)
from ultralytics import YOLO
model = YOLO(MODEL_PATH)

@router.post("/{image_id}/file", summary="Сегментировать изображение")
def segment_image(image_id: int, session: Session = Depends(get_db)):
    # 5. Поиск в БД
    img_rec = session.query(ImageUpload).get(image_id)
    if not img_rec:
        raise HTTPException(status_code=404, detail="Image not found")

    input_path = os.path.join(UPLOAD_DIR, img_rec.filename)
    if not os.path.isfile(input_path):
        raise HTTPException(status_code=404, detail="Source file missing")

    # 6. Запуск инференса
    results = model(input_path)
    # Берём первый результат
    r = results[0]

    # 7. Наносим результат на изображение
    annotated = r.plot()  # возвращает numpy ndarray BGR

    # 8. Сохраняем аннотированное изображение
    processed_name = f"seg_{img_rec.filename}"
    processed_path = os.path.join(UPLOAD_DIR, processed_name)
    cv2.imwrite(processed_path, annotated)

    # 9. Отдаём файл
    return FileResponse(
        path=processed_path,
        media_type=img_rec.content_type,
        filename=processed_name
    )


@router.post("/file", summary="Сегментировать загруженный файл без ID")
async def segment_direct(file: UploadFile = File(...)):
    # 1) Сохраним временно на диск (Ultralytics требует путь или np.ndarray)
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # 2) Прогоним модель
    results = model(tmp_path)
    r0 = results[0]

    # 3) Получим изображение с наложенными рамками/маской
    annotated = r0.plot()  # numpy ndarray (BGR)
    os.remove(tmp_path)

    # 4) Сохраним в другой temp-файл для отдачи
    is_success, buffer = cv2.imencode(suffix, annotated)
    if not is_success:
        raise HTTPException(500, "Не удалось закодировать результат")

    return StreamingResponse(
        content=buffer.tobytes(),
        media_type=file.content_type,
        headers={"Content-Disposition": f"attachment; filename=segmented{suffix}"}
    )