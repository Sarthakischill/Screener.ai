from app.agents.base_agent import BaseAgent
import numpy as np

class RecruitingAgent(BaseAgent):
    """Agent for extracting data from CVs and matching with job descriptions."""
    
    def __init__(self):
        super().__init__("Recruiting Agent", "CV Data Extraction and Matching Agent")
    
    async def process(self, resume_text, job_description_data):
        """
        Process a candidate's resume and match it with a job description.
        
        Args:
            resume_text: The full text of the candidate's resume
            job_description_data: The processed job description data
            
        Returns:
            dict: A dictionary containing extracted candidate info and match score
        """
        # First, extract key data from the resume
        candidate_data = await self._extract_candidate_data(resume_text)
        
        # Then, calculate match score
        match_score = await self._calculate_match_score(candidate_data, job_description_data)
        
        # Combine the results
        result = {
            **candidate_data,
            "match_score": match_score
        }
        
        return result
    
    async def _extract_candidate_data(self, resume_text):
        """Extract key data from a candidate's resume."""
        system_prompt = """
        You are a resume analyzer. Extract the following information from the resume:
        1. Education history (degrees, institutions, years)
        2. Work experience (positions, companies, years, responsibilities)
        3. Skills (technical skills, soft skills)
        4. Certifications and qualifications
        
        Format your response as JSON with the following structure:
        {
            "education": "education details...",
            "experience": "experience details...",
            "skills": "skill1, skill2, skill3, ...",
            "certifications": "certification1, certification2, ..."
        }
        """
        
        prompt = f"Analyze this resume and extract key information:\n\n{resume_text}"
        
        result = await self.generate_text(prompt, system_prompt)
        
        # In a real implementation, we'd parse the JSON response
        # For this MVP, we'll assume the model returns well-formatted JSON
        try:
            import json
            parsed_result = json.loads(result)
            return parsed_result
        except:
            # Fallback for when the model doesn't return proper JSON
            return {
                "education": "",
                "experience": "",
                "skills": "",
                "certifications": ""
            }
    
    async def _calculate_match_score(self, candidate_data, job_description_data):
        """
        Calculate a match score between candidate and job requirements.
        For MVP, we'll use a simple approach:
        1. Get embeddings for candidate skills and required skills
        2. Calculate cosine similarity
        3. Apply weightings for different factors
        """
        system_prompt = """
        You are a recruiting expert. Calculate a match score (0-100) between a candidate and a job description.
        Consider:
        1. Skills match (50% weight)
        2. Experience match (30% weight)
        3. Education/qualifications match (20% weight)
        
        Return only a numeric score between 0 and 100.
        """
        
        # Prepare prompt with all the data
        prompt = f"""
        JOB REQUIREMENTS:
        Skills: {job_description_data.get('required_skills', '')}
        Experience: {job_description_data.get('required_experience', '')}
        Qualifications: {job_description_data.get('required_qualifications', '')}
        
        CANDIDATE PROFILE:
        Skills: {candidate_data.get('skills', '')}
        Experience: {candidate_data.get('experience', '')}
        Education: {candidate_data.get('education', '')}
        Certifications: {candidate_data.get('certifications', '')}
        
        Calculate match score (0-100):
        """
        
        result = await self.generate_text(prompt, system_prompt)
        
        # Try to extract a numeric score
        try:
            # Clean and extract the number
            score = float(result.strip())
            return min(max(score, 0), 100)  # Ensure score is between 0-100
        except:
            # Fallback score if we can't parse the result
            return 50.0  # Default middle score 