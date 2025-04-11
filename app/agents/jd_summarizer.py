from app.agents.base_agent import BaseAgent

class JDSummarizerAgent(BaseAgent):
    """Agent for summarizing job descriptions."""
    
    def __init__(self):
        super().__init__("JD Summarizer", "Job Description Summarizer Agent")
    
    async def process(self, job_description):
        """
        Process a job description to extract key elements.
        
        Args:
            job_description: The full job description text
            
        Returns:
            dict: A dictionary containing extracted information
        """
        system_prompt = """
        You are a job description analyzer. Extract the following information from the job description:
        1. Required skills
        2. Required experience (in years, if mentioned)
        3. Required qualifications (degrees, certifications)
        4. Key job responsibilities
        5. A brief summary of the role (2-3 sentences)
        
        Format your response as JSON with the following structure:
        {
            "required_skills": "skill1, skill2, skill3, ...",
            "required_experience": "X years in...",
            "required_qualifications": "degree1, certification1, ...",
            "responsibilities": "responsibility1, responsibility2, ...",
            "summary": "Brief summary of the role"
        }
        """
        
        prompt = f"Analyze this job description and extract key information:\n\n{job_description}"
        
        result = await self.generate_text(prompt, system_prompt)
        
        # In a real implementation, we'd parse the JSON response
        # For this MVP, we'll assume the model returns well-formatted JSON
        # In production, add error handling and validation here
        
        # Simulate the result parsing for now
        try:
            import json
            parsed_result = json.loads(result)
            return parsed_result
        except:
            # Fallback for when the model doesn't return proper JSON
            return {
                "required_skills": "",
                "required_experience": "",
                "required_qualifications": "",
                "responsibilities": "",
                "summary": "Summary could not be generated."
            } 