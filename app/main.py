from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.routes import job_descriptions, candidates, matching
from app.db.database import get_db, engine
from app.models.models import Base

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Screening AI",
    description="A multi-agent AI system for job screening and candidate matching",
    version="0.1.0"
)

# CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(job_descriptions.router)
app.include_router(candidates.router)
app.include_router(matching.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Screening AI API"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint to verify API and database connection."""
    try:
        # Execute a simple query to verify the database connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)} 