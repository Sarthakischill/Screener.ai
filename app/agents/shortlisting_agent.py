from app.agents.base_agent import BaseAgent

class ShortlistingAgent(BaseAgent):
    """Agent for shortlisting candidates."""
    
    def __init__(self, threshold=75.0):
        super().__init__("Shortlisting Agent", "Candidate Shortlisting Agent")
        self.threshold = threshold
    
    async def process(self, candidates_with_scores, job_description=None, max_candidates=5):
        """
        Process candidates and shortlist the top ones.
        
        Args:
            candidates_with_scores: List of candidates with match scores
            job_description: The job description text
            max_candidates: Maximum number of candidates to shortlist
            
        Returns:
            list: A list of shortlisted candidates
        """
        # Sort candidates by score (highest first)
        sorted_candidates = sorted(
            candidates_with_scores, 
            key=lambda x: x.get("match_score", 0), 
            reverse=True
        )
        
        # Simple shortlisting strategy: Get top N candidates above threshold
        shortlisted = []
        for candidate in sorted_candidates:
            if len(shortlisted) >= max_candidates:
                break
                
            match_score = candidate.get("match_score", 0)
            if match_score >= self.threshold:
                # Mark as shortlisted
                candidate["is_shortlisted"] = True
                shortlisted.append(candidate)
        
        # If we don't have enough candidates above threshold, 
        # include the top candidates anyway
        if len(shortlisted) < max_candidates:
            for candidate in sorted_candidates:
                if candidate.get("is_shortlisted"):
                    continue
                    
                if len(shortlisted) >= max_candidates:
                    break
                    
                # Mark as shortlisted
                candidate["is_shortlisted"] = True
                shortlisted.append(candidate)
        
        print(f"Shortlisted {len(shortlisted)} candidates out of {len(candidates_with_scores)}")
        return shortlisted 