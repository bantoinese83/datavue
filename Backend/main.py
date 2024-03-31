from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from src.api import  uploads, insights
from src.database.db import engine, Base

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # React app
    "http://localhost:8000",  # FastAPI server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(uploads.router)
app.include_router(insights.router)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
