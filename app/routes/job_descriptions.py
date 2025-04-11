from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.models import JobDescription
from app.models.schemas import JobDescriptionCreate, JobDescriptionResponse
from app.agents.jd_summarizer import JDSummarizerAgent

router = APIRouter(
    prefix="/job-descriptions",
    tags=["job-descriptions"],
)

# Initialize the JD summarizer agent
jd_summarizer = JDSummarizerAgent()

@router.post("/", response_model=JobDescriptionResponse)
async def create_job_description(job_desc: JobDescriptionCreate, db: Session = Depends(get_db)):
    """Create a new job description and analyze it."""
    
    # Process the job description with the agent
    jd_analysis = await jd_summarizer.process(job_desc.description)
    
    # Create a new job description object
    db_job_desc = JobDescription(
        title=job_desc.title,
        company=job_desc.company,
        description=job_desc.description,
        required_skills=jd_analysis.get("required_skills", ""),
        required_experience=jd_analysis.get("required_experience", ""),
        required_qualifications=jd_analysis.get("required_qualifications", ""),
        responsibilities=jd_analysis.get("responsibilities", ""),
        summary=jd_analysis.get("summary", "")
    )
    
    # Add to database
    db.add(db_job_desc)
    db.commit()
    db.refresh(db_job_desc)
    
    return db_job_desc

@router.get("/", response_model=List[JobDescriptionResponse])
def get_job_descriptions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all job descriptions."""
    return db.query(JobDescription).offset(skip).limit(limit).all()

@router.get("/{job_id}", response_model=JobDescriptionResponse)
def get_job_description(job_id: int, db: Session = Depends(get_db)):
    """Get a specific job description by ID."""
    db_job_desc = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if db_job_desc is None:
        raise HTTPException(status_code=404, detail="Job description not found")
    return db_job_desc 