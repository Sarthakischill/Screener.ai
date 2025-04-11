from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Body
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
import logging

from app.db.database import get_db
from app.models.models import JobDescription, Candidate, CandidateMatch
from app.models.schemas import MatchResponse, CandidateWithMatchResponse, JobWithCandidatesResponse
from app.agents.orchestrator import AgentOrchestrator
from sqlalchemy import Column, String, Text

router = APIRouter(
    prefix="/matching",
    tags=["matching"],
)

# Initialize the agent orchestrator
orchestrator = AgentOrchestrator()

class CompanyNameRequest(BaseModel):
    company_name: str = "Acme Corp"

@router.post("/match-candidate/{job_id}/{candidate_id}", response_model=MatchResponse)
async def match_candidate_to_job(
    job_id: int, 
    candidate_id: int, 
    db: Session = Depends(get_db)
):
    """Match a specific candidate to a specific job."""
    
    # Get job description
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    # Get candidate
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Check if match already exists
    existing_match = db.query(CandidateMatch).filter(
        CandidateMatch.job_id == job_id,
        CandidateMatch.candidate_id == candidate_id
    ).first()
    
    if existing_match:
        return existing_match
    
    # Create job description data dictionary
    job_data = {
        "title": job.title,
        "required_skills": job.required_skills,
        "required_experience": job.required_experience,
        "required_qualifications": job.required_qualifications,
        "responsibilities": job.responsibilities
    }
    
    # Process the match
    match_result = await orchestrator.match_candidate(candidate.resume_text, job_data)
    match_score = match_result.get("match_score", 0)
    
    # Create a new match
    db_match = CandidateMatch(
        job_id=job_id,
        candidate_id=candidate_id,
        match_score=match_score,
        is_shortlisted=match_score >= 50.0  # Automatically shortlist if score >= 50%
    )
    
    # Add to database
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    
    return db_match

@router.post("/match-all/{job_id}", response_model=List[MatchResponse])
async def match_all_candidates_to_job(
    job_id: int, 
    db: Session = Depends(get_db)
):
    """Match all candidates to a specific job."""
    
    # Get job description
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    # Get all candidates
    candidates = db.query(Candidate).all()
    if not candidates:
        return []
    
    job_data = {
        "title": job.title,
        "required_skills": job.required_skills,
        "required_experience": job.required_experience,
        "required_qualifications": job.required_qualifications,
        "responsibilities": job.responsibilities
    }
    
    results = []
    
    # Process each candidate
    for candidate in candidates:
        try:
            # Check if match already exists
            existing_match = db.query(CandidateMatch).filter(
                CandidateMatch.job_id == job_id,
                CandidateMatch.candidate_id == candidate.id
            ).first()
            
            if existing_match:
                results.append(existing_match)
                continue
            
            # Process the match
            match_result = await orchestrator.match_candidate(candidate.resume_text, job_data)
            match_score = match_result.get("match_score", 0)
            
            # Create a new match
            db_match = CandidateMatch(
                job_id=job_id,
                candidate_id=candidate.id,
                match_score=match_score,
                is_shortlisted=match_score >= 75.0  # Automatically shortlist if high score
            )
            
            # Add to database
            db.add(db_match)
            db.commit()
            db.refresh(db_match)
            
            results.append(db_match)
        except Exception as e:
            print(f"Error processing candidate {candidate.id}: {str(e)}")
            db.rollback()
    
    return results

@router.get("/job/{job_id}/candidates", response_model=JobWithCandidatesResponse)
def get_job_with_candidates(job_id: int, db: Session = Depends(get_db)):
    """Get a job with all matched candidates."""
    
    # Get job description
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    # Get all matches for this job
    matches = db.query(CandidateMatch).filter(CandidateMatch.job_id == job_id).all()
    
    # Get candidates with match data
    candidates_with_match = []
    for match in matches:
        candidate = db.query(Candidate).filter(Candidate.id == match.candidate_id).first()
        if candidate:
            candidate_dict = {
                "id": candidate.id,
                "name": candidate.name,
                "email": candidate.email,
                "education": candidate.education,
                "experience": candidate.experience,
                "skills": candidate.skills,
                "certifications": candidate.certifications,
                "created_at": candidate.created_at,
                "match_score": match.match_score,
                "is_shortlisted": match.is_shortlisted,
                "interview_scheduled": match.interview_scheduled,
                "interview_date": match.interview_date,
                "interview_format": match.interview_format,
                "interview_email": match.interview_email
            }
            candidates_with_match.append(candidate_dict)
    
    # Create response
    response = {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "description": job.description,
        "required_skills": job.required_skills,
        "required_experience": job.required_experience,
        "required_qualifications": job.required_qualifications,
        "responsibilities": job.responsibilities,
        "summary": job.summary,
        "created_at": job.created_at,
        "candidates": candidates_with_match
    }
    
    return response

@router.post("/shortlist/job/{job_id}", response_model=List[CandidateWithMatchResponse])
async def shortlist_candidates_for_job(job_id: int, db: Session = Depends(get_db)):
    """Shortlist candidates for a job based on match scores."""
    
    # Get job description
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    # Get all matches for this job
    matches = db.query(CandidateMatch).filter(CandidateMatch.job_id == job_id).all()
    
    # Create candidates with scores list
    candidates_with_scores = []
    for match in matches:
        candidate = db.query(Candidate).filter(Candidate.id == match.candidate_id).first()
        if candidate:
            candidate_dict = {
                "id": candidate.id,
                "name": candidate.name,
                "email": candidate.email,
                "education": candidate.education,
                "experience": candidate.experience,
                "skills": candidate.skills,
                "certifications": candidate.certifications,
                "resume_text": candidate.resume_text,
                "created_at": candidate.created_at,
                "match_score": match.match_score,
                "interview_scheduled": match.interview_scheduled,
                "interview_date": match.interview_date,
                "interview_format": match.interview_format,
                "interview_email": match.interview_email
            }
            candidates_with_scores.append(candidate_dict)
    
    # Shortlist candidates
    shortlisted = await orchestrator.shortlist_candidates(
        candidates_with_scores, 
        job.description
    )
    
    # Update database with shortlisted status
    for candidate in shortlisted:
        match = db.query(CandidateMatch).filter(
            CandidateMatch.job_id == job_id,
            CandidateMatch.candidate_id == candidate.get("id")
        ).first()
        
        if match:
            match.is_shortlisted = True
            db.commit()
    
    return shortlisted

@router.post("/schedule-interviews/job/{job_id}", response_model=List[Dict[str, Any]])
async def schedule_interviews(
    job_id: int, 
    request: CompanyNameRequest = Body(...),
    db: Session = Depends(get_db)
):
    """Schedule interviews for shortlisted candidates."""
    
    # Get job description
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    # Get shortlisted candidates
    shortlisted_matches = db.query(CandidateMatch).filter(
        CandidateMatch.job_id == job_id,
        CandidateMatch.is_shortlisted == True,
        CandidateMatch.interview_scheduled == False  # Only unscheduled interviews
    ).all()
    
    # Create shortlisted candidates list
    shortlisted = []
    for match in shortlisted_matches:
        candidate = db.query(Candidate).filter(Candidate.id == match.candidate_id).first()
        if candidate:
            candidate_dict = {
                "id": candidate.id,
                "name": candidate.name,
                "email": candidate.email,
                "education": candidate.education,
                "experience": candidate.experience,
                "skills": candidate.skills,
                "certifications": candidate.certifications,
                "match_score": match.match_score
            }
            shortlisted.append(candidate_dict)
    
    # Schedule interviews
    job_data = {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "description": job.description,
        "required_skills": job.required_skills,
        "required_experience": job.required_experience,
        "required_qualifications": job.required_qualifications
    }
    
    interviews = await orchestrator.schedule_interviews(
        shortlisted, 
        job_data,
        request.company_name
    )
    
    # Update database with interview details
    for interview in interviews:
        match = db.query(CandidateMatch).filter(
            CandidateMatch.job_id == job_id,
            CandidateMatch.candidate_id == interview.get("candidate_id")
        ).first()
        
        if match and interview.get("potential_dates"):
            match.interview_scheduled = True
            match.interview_date = interview.get("potential_dates")[0]  # Use first date as default
            match.interview_format = interview.get("interview_format")
            # Add email content to response
            match.interview_email = interview.get("email_content")
            db.commit()
    
    return interviews

@router.get("/stats/shortlisted")
def get_shortlisted_count(db: Session = Depends(get_db)):
    """Get the count of shortlisted candidates across all jobs."""
    count = db.query(CandidateMatch).filter(CandidateMatch.is_shortlisted == True).count()
    return {"count": count}

@router.get("/stats/interviews")
def get_interviews_count(db: Session = Depends(get_db)):
    """Get the count of scheduled interviews across all jobs."""
    count = db.query(CandidateMatch).filter(CandidateMatch.interview_scheduled == True).count()
    return {"count": count}

async def process_matches_background(job_id, job, candidates):
    """Process matches in the background."""
    # Create a new DB session for the background task
    from app.db.database import SessionLocal
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    db = SessionLocal()
    
    try:
        logger.info(f"Processing matches for job_id={job_id} with {len(candidates)} candidates")
        
        job_data = {
            "title": job.title,
            "required_skills": job.required_skills,
            "required_experience": job.required_experience,
            "required_qualifications": job.required_qualifications,
            "responsibilities": job.responsibilities
        }
        
        for candidate in candidates:
            try:
                # Check if match already exists
                existing_match = db.query(CandidateMatch).filter(
                    CandidateMatch.job_id == job_id,
                    CandidateMatch.candidate_id == candidate.id
                ).first()
                
                if not existing_match:
                    logger.info(f"Processing candidate {candidate.id} for job {job_id}")
                    # Process the match
                    match_result = await orchestrator.match_candidate(candidate.resume_text, job_data)
                    match_score = match_result.get("match_score", 0)
                    
                    # Create a new match
                    db_match = CandidateMatch(
                        job_id=job_id,
                        candidate_id=candidate.id,
                        match_score=match_score,
                        is_shortlisted=match_score >= 50.0  # Lowered threshold to 50%
                    )
                    
                    # Add to database
                    db.add(db_match)
                    db.commit()
                    logger.info(f"Candidate {candidate.id} matched with score {match_score}")
                else:
                    logger.info(f"Match already exists for candidate {candidate.id} and job {job_id}")
            except Exception as e:
                logger.error(f"Error processing candidate {candidate.id}: {str(e)}")
                db.rollback()
    except Exception as e:
        logger.error(f"Error in background processing: {str(e)}")
    finally:
        db.close() 