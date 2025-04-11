from app.agents.jd_summarizer import JDSummarizerAgent
from app.agents.recruiting_agent import RecruitingAgent
from app.agents.shortlisting_agent import ShortlistingAgent
from app.agents.interview_scheduler import InterviewSchedulerAgent

class AgentOrchestrator:
    """Orchestrates the workflow between different agents."""
    
    def __init__(self):
        self.jd_summarizer = JDSummarizerAgent()
        self.recruiting_agent = RecruitingAgent()
        self.shortlisting_agent = ShortlistingAgent(threshold=50.0)  # Updated threshold to 50%
        self.interview_scheduler = InterviewSchedulerAgent()
    
    async def process_job_description(self, job_description):
        """Process a job description and extract key information."""
        return await self.jd_summarizer.process(job_description)
    
    async def match_candidate(self, resume_text, job_description_data):
        """Match a candidate with a job description."""
        return await self.recruiting_agent.process(resume_text, job_description_data)
    
    async def shortlist_candidates(self, candidates_with_scores, job_description=None, max_candidates=5):
        """Shortlist candidates based on their match scores."""
        return await self.shortlisting_agent.process(
            candidates_with_scores, 
            job_description,
            max_candidates
        )
    
    async def schedule_interviews(self, shortlisted_candidates, job_description, company_name):
        """Schedule interviews for shortlisted candidates."""
        interviews = []
        for candidate in shortlisted_candidates:
            interview = await self.interview_scheduler.process(
                candidate, 
                job_description,
                company_name
            )
            interviews.append(interview)
        return interviews
    
    async def process_full_workflow(self, job_description, candidates, company_name="Acme Corp"):
        """
        Run the full recruitment workflow:
        1. Summarize job description
        2. Match each candidate
        3. Shortlist candidates
        4. Schedule interviews
        """
        # Step 1: Summarize job description
        print("Step 1: Summarizing job description...")
        jd_data = await self.process_job_description(job_description)
        
        # Step 2: Match each candidate
        print("Step 2: Matching candidates...")
        candidates_with_scores = []
        for candidate in candidates:
            match_result = await self.match_candidate(candidate['resume_text'], jd_data)
            candidates_with_scores.append({
                **candidate,
                **match_result
            })
        
        # Step 3: Shortlist candidates
        print("Step 3: Shortlisting candidates...")
        shortlisted = await self.shortlist_candidates(
            candidates_with_scores, 
            job_description
        )
        
        # Step 4: Schedule interviews
        print("Step 4: Scheduling interviews...")
        interviews = await self.schedule_interviews(
            shortlisted, 
            jd_data,
            company_name
        )
        
        # Return the full results
        return {
            "job_description": jd_data,
            "all_candidates": candidates_with_scores,
            "shortlisted_candidates": shortlisted,
            "interviews": interviews
        } 