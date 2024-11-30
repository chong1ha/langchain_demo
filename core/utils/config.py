import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    @staticmethod
    def check_config():
        
        if not Config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found in .env file.")
        
        