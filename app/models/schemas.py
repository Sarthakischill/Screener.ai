from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Job Description Schemas
class JobDescriptionBase(BaseModel):
    title: str
    company: str
    description: str
    required_skills: Optional[str] = None
    required_experience: Optional[str] = None
    required_qualifications: Optional[str] = None
    responsibilities: Optional[str] = None

class JobDescriptionCreate(JobDescriptionBase):
    pass

class JobDescriptionResponse(JobDescriptionBase):
    id: int
    summary: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

# Candidate Schemas
class CandidateBase(BaseModel):
    name: str
    email: str
    education: Optional[str] = None
    experience: Optional[str] = None
    skills: Optional[str] = None
    certifications: Optional[str] = None
    resume_text: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateResponse(CandidateBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Match Schemas
class MatchBase(BaseModel):
    job_id: int
    candidate_id: int
    match_score: float
    is_shortlisted: Optional[bool] = False
    interview_scheduled: Optional[bool] = False
    interview_date: Optional[datetime] = None
    interview_format: Optional[str] = None
    interview_email: Optional[str] = None

class MatchCreate(MatchBase):
    pass

class MatchResponse(MatchBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Enhanced Response Schemas
class CandidateWithMatchResponse(CandidateResponse):
    match_score: float
    is_shortlisted: bool
    interview_scheduled: Optional[bool] = False
    interview_date: Optional[datetime] = None
    interview_format: Optional[str] = None
    interview_email: Optional[str] = None
    
    class Config:
        orm_mode = True

class JobWithCandidatesResponse(JobDescriptionResponse):
    candidates: List[CandidateWithMatchResponse]
    
    class Config:
        orm_mode = True 