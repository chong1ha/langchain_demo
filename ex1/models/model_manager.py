from langchain_community.llms import OpenAI
from core.utils.config import Config

class ModelManager:

    def __init__(self):
        Config.check_config() 
        self.model = OpenAI(api_key=Config.OPENAI_API_KEY)

    def get_response(self, prompt: str):
        return self.model(prompt)