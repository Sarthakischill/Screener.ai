import csv
import os
import asyncio
import sqlite3
import pandas as pd
import PyPDF2
from sqlalchemy.orm import sessionmaker
from app.db.database import engine, SessionLocal
from app.models.models import JobDescription, Candidate
from app.agents.jd_summarizer import JDSummarizerAgent
from app.agents.recruiting_agent import RecruitingAgent
from dotenv import load_dotenv

# Load environment variables from .env file if exists
load_dotenv()

# Ensure GEMINI_API_KEY is set
if not os.environ.get("GEMINI_API_KEY"):
    print("Error: GEMINI_API_KEY environment variable is not set.")
    print("Please set the API key in .env file or run with: GEMINI_API_KEY=your_key python import_data.py")
    exit(1)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Initialize agents
jd_summarizer = JDSummarizerAgent()
recruiting_agent = RecruitingAgent()

async def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {str(e)}")
        return ""

async def import_job_descriptions():
    """Import job descriptions from CSV file."""
    try:
        print("Importing job descriptions...")
        
        # Read the CSV file with error handling for encoding issues
        try:
            df = pd.read_csv('job_description.csv', encoding='utf-8')
        except UnicodeDecodeError:
            print("UTF-8 encoding failed, trying with ISO-8859-1...")
            df = pd.read_csv('job_description.csv', encoding='ISO-8859-1')
        
        # Limit the number of job descriptions to process (to avoid hitting API rate limits)
        MAX_JOB_DESCRIPTIONS = 3
        processed_count = 0
        
        # For each job description
        for index, row in df.iterrows():
            # Skip if no title or description
            if pd.isna(row['Job Title']) or pd.isna(row['Job Description']):
                continue
                
            title = row['Job Title']
            description = row['Job Description']
            
            # Check if job description already exists
            existing_jd = session.query(JobDescription).filter(
                JobDescription.title == title,
                JobDescription.description == description
            ).first()
            
            if existing_jd:
                print(f"Job description '{title}' already exists. Skipping.")
                continue
            
            # Analyze job description
            print(f"Analyzing job description: {title}")
            jd_analysis = await jd_summarizer.process(description)
            
            # Create a new job description
            new_jd = JobDescription(
                title=title,
                company="Acme Corp",  # Default company for demo
                description=description,
                required_skills=jd_analysis.get("required_skills", ""),
                required_experience=jd_analysis.get("required_experience", ""),
                required_qualifications=jd_analysis.get("required_qualifications", ""),
                responsibilities=jd_analysis.get("responsibilities", ""),
                summary=jd_analysis.get("summary", "")
            )
            
            # Add to database
            session.add(new_jd)
            session.commit()
            print(f"Imported job description: {title}")
            
            # Increment counter and check limit
            processed_count += 1
            if processed_count >= MAX_JOB_DESCRIPTIONS:
                print(f"Reached limit of {MAX_JOB_DESCRIPTIONS} job descriptions. Stopping import.")
                break
            
    except Exception as e:
        print(f"Error importing job descriptions: {str(e)}")
        session.rollback()

async def import_resumes():
    """Import resumes from PDF files."""
    try:
        print("Importing resumes...")
        
        # Get all PDF files in the CVs1 directory
        cv_dir = "CVs1"
        pdf_files = [f for f in os.listdir(cv_dir) if f.endswith('.pdf')]
        
        # For each PDF file
        for pdf_file in pdf_files:
            # Extract candidate ID from filename
            candidate_id = pdf_file.split('.')[0]
            
            # Check if candidate already exists
            existing_candidate = session.query(Candidate).filter(
                Candidate.name == candidate_id
            ).first()
            
            if existing_candidate:
                print(f"Candidate '{candidate_id}' already exists. Skipping.")
                continue
            
            # Extract text from PDF
            pdf_path = os.path.join(cv_dir, pdf_file)
            resume_text = await extract_text_from_pdf(pdf_path)
            
            if not resume_text:
                print(f"Failed to extract text from {pdf_file}. Skipping.")
                continue
            
            # Extract candidate data
            print(f"Analyzing resume: {candidate_id}")
            candidate_data = await recruiting_agent._extract_candidate_data(resume_text)
            
            # Create a new candidate
            email = f"{candidate_id.lower()}@example.com"  # Generate email for demo
            
            new_candidate = Candidate(
                name=candidate_id,
                email=email,
                education=candidate_data.get("education", ""),
                experience=candidate_data.get("experience", ""),
                skills=candidate_data.get("skills", ""),
                certifications=candidate_data.get("certifications", ""),
                resume_text=resume_text
            )
            
            # Add to database
            session.add(new_candidate)
            session.commit()
            print(f"Imported resume: {candidate_id}")
            
    except Exception as e:
        print(f"Error importing resumes: {str(e)}")
        session.rollback()

async def main():
    # Import job descriptions
    await import_job_descriptions()
    
    # Import resumes
    await import_resumes()
    
    print("Import complete!")

if __name__ == "__main__":
    asyncio.run(main()) 