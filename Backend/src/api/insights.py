from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import crud, schemas
from src.database.db import get_db
from src.openai.generate_insights_prompt import generate_insights_prompt
from src.openai.openai_api import generate_insight
from sqlalchemy import text

import pandas as pd

router = APIRouter()


# In src/api/insights.py


@router.post("/insights/", response_model=schemas.InsightInDB)
def create_insight(insight: schemas.InsightCreate, db: Session = Depends(get_db)):
    # Check if upload_id is provided
    if insight.upload_id is None:
        raise HTTPException(status_code=400, detail="upload_id must be provided")

    # Get the upload associated with the insight
    upload = crud.get_upload(db, upload_id=insight.upload_id)
    if upload is None:
        raise HTTPException(status_code=404, detail="Upload not found")

    # Get the data from the corresponding table in the database
    table_name = f'upload_{upload.id}'
    query = text(f"SELECT * FROM {table_name}")
    result = db.execute(query)
    data = [{'col1': row[0], 'col2': row[1], 'col3': row[2], 'col4': row[3], 'col5': row[4]} for row in result]

    # Generate a prompt using the data
    prompt = generate_insights_prompt(data) if data else "Default prompt"

    # Generate insight using OpenAI API or use a placeholder
    insight_text = generate_insight(prompt) if prompt else "Insight text to be updated"

    # Create a new InsightCreate schema with the generated or placeholder insight
    new_insight = schemas.InsightCreate(text=insight_text, upload_id=insight.upload_id)

    return crud.create_insight(db=db, insight=new_insight)


@router.get("/insights/", response_model=List[schemas.InsightInDB])
def read_insights(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    insights = crud.get_insights(db, skip=skip, limit=limit)
    return insights



