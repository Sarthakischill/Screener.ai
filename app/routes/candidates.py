from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.models import Candidate
from app.models.schemas import CandidateCreate, CandidateResponse
from app.agents.recruiting_agent import RecruitingAgent

router = APIRouter(
    prefix="/candidates",
    tags=["candidates"],
)

# Initialize the recruiting agent
recruiting_agent = RecruitingAgent()

@router.post("/", response_model=CandidateResponse)
async def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    """Create a new candidate."""
    
    # Check if candidate with same email already exists
    db_candidate = db.query(Candidate).filter(Candidate.email == candidate.email).first()
    if db_candidate:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create a new candidate object
    db_candidate = Candidate(
        name=candidate.name,
        email=candidate.email,
        education=candidate.education,
        experience=candidate.experience,
        skills=candidate.skills,
        certifications=candidate.certifications,
        resume_text=candidate.resume_text
    )
    
    # Add to database
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    return db_candidate

@router.post("/upload-resume", response_model=CandidateResponse)
async def upload_resume(
    name: str, 
    email: str, 
    resume: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    """Upload a resume and create a candidate."""
    
    # Check if candidate with same email already exists
    db_candidate = db.query(Candidate).filter(Candidate.email == email).first()
    if db_candidate:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Read resume content
    resume_content = await resume.read()
    resume_text = resume_content.decode("utf-8")
    
    # Extract information from resume
    candidate_data = await recruiting_agent._extract_candidate_data(resume_text)
    
    # Create a new candidate object
    db_candidate = Candidate(
        name=name,
        email=email,
        education=candidate_data.get("education", ""),
        experience=candidate_data.get("experience", ""),
        skills=candidate_data.get("skills", ""),
        certifications=candidate_data.get("certifications", ""),
        resume_text=resume_text
    )
    
    # Add to database
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    return db_candidate

@router.get("/", response_model=List[CandidateResponse])
def get_candidates(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all candidates."""
    return db.query(Candidate).offset(skip).limit(limit).all()

@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """Get a specific candidate by ID."""
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate 