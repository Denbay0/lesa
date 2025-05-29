from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, db

router = APIRouter(prefix="/legal", tags=["legal"])

def get_db():
    db_sess = db.SessionLocal()
    try:
        yield db_sess
    finally:
        db_sess.close()

@router.post("/", response_model=schemas.LegalEntityRead)
def create_legal(entity: schemas.LegalEntityCreate, session: Session = Depends(get_db)):
    # проверим уникальность ИНН
    if session.query(models.LegalEntity).filter_by(inn=entity.inn).first():
        raise HTTPException(status_code=400, detail="Entity with this INN already exists")
    db_obj = models.LegalEntity(**entity.dict())
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
