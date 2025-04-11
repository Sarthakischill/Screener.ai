from app.agents.base_agent import BaseAgent
from datetime import datetime, timedelta
import random

class InterviewSchedulerAgent(BaseAgent):
    """Agent for scheduling interviews with shortlisted candidates."""
    
    def __init__(self):
        super().__init__("Interview Scheduler", "Interview Scheduling Agent")
        # Some predefined interview formats
        self.interview_formats = [
            "Video Call",
            "Phone Interview",
            "In-Person",
            "Technical Assessment"
        ]
    
    async def process(self, candidate, job_description, company_name):
        """
        Process a shortlisted candidate and generate an interview request.
        
        Args:
            candidate: The candidate data
            job_description: The job description
            company_name: The company name
            
        Returns:
            dict: A dictionary with interview details
        """
        # For MVP, we'll simulate generating interview dates
        # In a real application, this would integrate with a calendar API
        
        # Generate some potential dates (next 10 business days)
        potential_dates = self._generate_potential_dates(3)
        
        # Generate personalized email
        email_content = await self._generate_email(
            candidate, 
            job_description, 
            company_name, 
            potential_dates
        )
        
        # Select a random interview format for demo
        interview_format = random.choice(self.interview_formats)
        
        return {
            "candidate_id": candidate.get("id"),
            "candidate_name": candidate.get("name"),
            "candidate_email": candidate.get("email"),
            "potential_dates": potential_dates,
            "interview_format": interview_format,
            "email_content": email_content
        }
    
    def _generate_potential_dates(self, num_dates=3):
        """Generate potential interview dates (weekdays only)."""
        dates = []
        current_date = datetime.now() + timedelta(days=3)  # Start 3 days from now
        
        while len(dates) < num_dates:
            # Skip weekends
            if current_date.weekday() < 5:  # 0-4 are weekdays
                # Generate random time between 9 AM and 4 PM
                hour = random.randint(9, 16)
                minute = random.choice([0, 30])  # 30-minute intervals
                
                interview_datetime = current_date.replace(hour=hour, minute=minute)
                dates.append(interview_datetime)
            
            current_date += timedelta(days=1)
        
        return dates
    
    async def _generate_email(self, candidate, job_description, company_name, potential_dates):
        """Generate a personalized email for the candidate."""
        # Format the dates for the email
        formatted_dates = []
        for date in potential_dates:
            formatted_dates.append(date.strftime("%A, %B %d at %I:%M %p"))
        
        dates_text = ", ".join(formatted_dates[:-1]) + f" or {formatted_dates[-1]}"
        
        system_prompt = """
        You are a professional recruiter. Write a personalized email to invite a candidate for an interview.
        The email should be professional, friendly, and include:
        1. A personalized greeting
        2. Brief mention of their qualifications that impressed you
        3. Information about the role
        4. Suggested interview dates
        5. Next steps
        6. A professional sign-off
        
        Keep the email concise and to the point.
        """
        
        # Get candidate details
        candidate_name = candidate.get("name", "Candidate")
        candidate_skills = candidate.get("skills", "")
        job_title = job_description.get("title", "the position")
        
        prompt = f"""
        Company: {company_name}
        Job Title: {job_title}
        Candidate Name: {candidate_name}
        Candidate Skills: {candidate_skills}
        Potential Interview Dates: {dates_text}
        
        Write a personalized interview invitation email:
        """
        
        email_content = await self.generate_text(prompt, system_prompt)
        return email_content 