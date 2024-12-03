import os
from dotenv import load_dotenv


# Load
load_dotenv()

class Config:
    """
    애플리케이션 설정 관리
    """
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    REDIS_URL = os.getenv("REDIS_URL")
    
    @staticmethod
    def check_required_config() -> None:
        """
        환경 변수에 설정된 API 키가 있는지 확인
        
        :raises ValueError: API 키가 .env 파일에 없을 경우, 예외 발생
        """
        if not Config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found in .env file.")
        
        if not Config.REDIS_URL:
            raise ValueError("Redis URL not found in .env file.")
# End of Config