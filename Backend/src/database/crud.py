from sqlalchemy.orm import Session

from src.database.schemas import UploadCreate, InsightCreate
from src.models.insights import Insight
from src.models.uploads import Upload
from fastapi import HTTPException


# Upload CRUD operations
def get_upload(db: Session, upload_id: int):
    return db.query(Upload).filter(Upload.id == upload_id).first()


def get_uploads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Upload).offset(skip).limit(limit).all()


def create_upload(db: Session, upload: UploadCreate):
    db_upload = Upload(filename=upload.filename)
    db.add(db_upload)
    db.commit()
    db.refresh(db_upload)
    return db_upload


# Insight CRUD operations
def get_insight(db: Session, insight_id: int):
    return db.query(Insight).filter(Insight.id == insight_id).first()


def get_insights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Insight).offset(skip).limit(limit).all()


def create_insight(db: Session, insight: InsightCreate):
    db_insight = Insight(text=insight.text, upload_id=insight.upload_id)
    db.add(db_insight)
    db.commit()
    db.refresh(db_insight)
    return db_insight


def update_insight(db: Session, insight_id: int, insight_update: InsightCreate):
    db_insight = db.query(Insight).filter(Insight.id == insight_id).first()
    if db_insight is None:
        raise HTTPException(status_code=404, detail="Insight not found")
    db_insight.text = insight_update.text
    db.commit()
    db.refresh(db_insight)
    return db_insight
