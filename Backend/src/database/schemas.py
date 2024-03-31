from datetime import datetime
from pydantic import BaseModel


# Upload Schemas
class UploadBase(BaseModel):
    filename: str


class UploadCreate(UploadBase):
    pass


class UploadUpdate(UploadBase):
    pass


class UploadInDB(UploadBase):
    id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True


# Insight Schemas
class InsightBase(BaseModel):
    text: str


class InsightCreate(BaseModel):
    text: str
    upload_id: int


class InsightUpdate(InsightBase):
    pass


class InsightInDB(InsightBase):
    id: int
    upload_id: int
    created_at: datetime

    class Config:
        from_attributes = True
