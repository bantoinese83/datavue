import logging
from typing import List

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy import MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from src.database import crud, schemas
from src.database.db import engine, get_db
from src.database.schemas import UploadCreate
from src.models.base import BaseModel, Base

router = APIRouter()

# Initialize a logger
logger = logging.getLogger(__name__)


def create_model(table_name, columns):
    attrs = {
        '__tablename__': table_name,
        '__table_args__': {'extend_existing': True},
    }

    for column_name, column_type in columns.items():
        attrs[column_name] = Column(column_type)

    model = type(table_name, (BaseModel,), attrs)
    return model


def dtype_to_sqltype(dtype):
    """Convert pandas dtype to SQL type."""
    if pd.api.types.is_integer_dtype(dtype):
        return Integer
    elif pd.api.types.is_float_dtype(dtype):
        return Float
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return DateTime
    return String


# Assuming 'engine' is your SQLAlchemy engine
metadata = MetaData()


# No need to bind the engine during MetaData instantiation
def store_in_database(df: pd.DataFrame, upload_id: int):
    try:
        # Infer SQL data types from DataFrame
        columns = {name: dtype_to_sqltype(df[name].dtype) for name in df.columns}

        # Create a new table for the upload
        table_name = f'upload_{upload_id}'
        model = create_model(table_name, columns)

        # Create the table in the database
        Base.metadata.create_all(engine)

        # Insert the data into the table
        with Session(engine) as session:
            for record in df.to_dict(orient='records'):
                instance = model(**record)
                session.add(instance)
            session.commit()
    except Exception as e:
        logger.error(f"Failed to store data in database: {e}")
        raise HTTPException(status_code=500, detail="Failed to store uploaded data")


@router.post("/uploads/", response_model=schemas.UploadInDB)
async def create_upload(upload: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        upload_data = UploadCreate(filename=upload.filename)
        db_upload = crud.create_upload(db, upload_data)  # Store the uploaded file metadata in the database

        df = pd.read_csv(upload.file)  # Read the content of the uploaded file into a pandas DataFrame
        store_in_database(df, db_upload.id)  # Store the DataFrame data in the database

        return db_upload
    except Exception as e:
        logger.error(f"Upload creation failed: {e}")
        raise HTTPException(status_code=500, detail="Upload creation failed")


@router.get("/uploads/", response_model=List[schemas.UploadInDB])
async def read_uploads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        uploads = crud.get_uploads(db, skip=skip, limit=limit)
        return uploads
    except SQLAlchemyError as e:
        logger.error(f"Error reading uploads: {e}")
        raise HTTPException(status_code=500, detail="Error reading uploads")


@router.get("/uploads/{upload_id}/data")
async def get_upload_data(upload_id: int, db: Session = Depends(get_db)):
    # Get the upload associated with the upload_id
    upload = crud.get_upload(db, upload_id=upload_id)
    if upload is None:
        raise HTTPException(status_code=404, detail="Upload not found")

    # Get the data from the corresponding table in the database
    table_name = f'upload_{upload.id}'
    query = text(f"SELECT * FROM {table_name}")
    result = db.execute(query)

    # Convert the result to a pandas DataFrame
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()

    # Convert the DataFrame to a dictionary and return it
    return df.to_dict(orient='records')
