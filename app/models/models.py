from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(Text, nullable=True)
    required_experience = Column(Text, nullable=True)
    required_qualifications = Column(Text, nullable=True)
    responsibilities = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    candidates = relationship("CandidateMatch", back_populates="job")


class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    education = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    certifications = Column(Text, nullable=True)
    resume_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    jobs = relationship("CandidateMatch", back_populates="candidate")


class CandidateMatch(Base):
    __tablename__ = "candidate_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    match_score = Column(Float, nullable=False)
    is_shortlisted = Column(Boolean, default=False)
    interview_scheduled = Column(Boolean, default=False)
    interview_date = Column(DateTime, nullable=True)
    interview_format = Column(String(50), nullable=True)
    interview_email = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    job = relationship("JobDescription", back_populates="candidates")
    candidate = relationship("Candidate", back_populates="jobs")

# Initialize the database
def init_db(db_url="sqlite:///./job_screening.db"):
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    return engine 