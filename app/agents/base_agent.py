import os
import google.generativeai as genai
from abc import ABC, abstractmethod
import numpy as np
from dotenv import load_dotenv

class BaseAgent(ABC):
    """Base class for all agents in the multi-agent system."""
    
    def __init__(self, name, description=None):
        self.name = name
        self.description = description or f"{name} Agent"
        
        # Load environment variables from .env file
        load_dotenv()
        
        # Initialize Gemini API
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=api_key)
        self.model_name = "gemini-1.5-flash-latest"  # Use Flash for speed
    
    @abstractmethod
    async def process(self, *args, **kwargs):
        """Process method to be implemented by concrete agents."""
        pass
    
    async def generate_text(self, prompt, system_prompt=None, max_tokens=1000):
        """Generate text using Gemini API."""
        try:
            # Configure the generation config
            generation_config = {
                "temperature": 0.7,
                "max_output_tokens": max_tokens,
                "top_p": 0.95,
                "top_k": 40,
            }
            
            # Get the Gemini model
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=generation_config
            )
            
            # Create chat session if system prompt is provided
            if system_prompt:
                chat = model.start_chat(history=[
                    {"role": "user", "parts": [system_prompt]},
                    {"role": "model", "parts": ["I'll help you with that."]}
                ])
                response = await self._async_send_message(chat, prompt)
            else:
                # One-off generation
                response = await self._async_generate_content(model, prompt)
                
            return response
        except Exception as e:
            print(f"Error generating text: {str(e)}")
            return ""
    
    async def get_embedding(self, text):
        """Get embedding for text using Gemini API."""
        try:
            # Initialize the embedding model
            embedding_model = genai.GenerativeModel("embedding-001")
            
            # Get embedding
            result = embedding_model.embed_content(content=text)
            embedding = result["embedding"]
            
            return embedding
        except Exception as e:
            print(f"Error getting embedding: {str(e)}")
            return []
    
    async def _async_generate_content(self, model, prompt):
        """Helper method to generate content asynchronously."""
        # This is a simple wrapper to make the synchronous API behave asynchronously
        response = model.generate_content(prompt)
        return response.text
    
    async def _async_send_message(self, chat, message):
        """Helper method to send message to chat asynchronously."""
        # This is a simple wrapper to make the synchronous API behave asynchronously
        response = chat.send_message(message)
        return response.text 