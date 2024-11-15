from datetime import datetime

from sqlalchemy.orm import Session
from api.db import schemas, models


def get_application(db: Session, id: int):
    return db.query(models.Application).filter(models.Application.id == id).first()

def get_applications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Application).offset(skip).limit(limit).all()

def create_application(db: Session, application: schemas.ApplicationCreate):
    entity = models.Application(
        name=application.name,
        description=application.description,
        path=application.path,
        original_file_name=application.original_file_name,
        details=application.details,
        uploaded=datetime.now()
    )

    db.add(entity)
    db.commit()
    db.refresh(entity)

    return entity