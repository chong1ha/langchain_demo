import os
import hashlib
import base64
from dotenv import load_dotenv
from langchain.globals import set_llm_cache, set_debug
from langchain_community.cache import InMemoryCache, RedisSemanticCache
from langchain_community.embeddings import OpenAIEmbeddings


# Load
load_dotenv()

class Config:
    """
    애플리케이션 설정 관리
    """
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    REDIS_URL = os.getenv("REDIS_URL", None)
    debug = False
    llm_cache = None
                
    @staticmethod
    def init(use_redis_cache=False):
        """
        전역 설정 초기화
        """
        try:
            Config.check_required_config()
            
            if use_redis_cache and Config.REDIS_URL:
                Config.LLM_CACHE = RedisSemanticCache(
                    redis_url=Config.REDIS_URL, 
                    embedding=OpenAIEmbeddings()
                )
            else:
                Config.LLM_CACHE = InMemoryCache()

            Config.DEBUG = False 

            set_debug(Config.DEBUG)
            set_llm_cache(Config.LLM_CACHE)
            
        except Exception as e:
            raise RuntimeError(f"전역 설정 초기화 실패: {str(e)}")
        
    @classmethod
    def get_debug(cls):
        return cls.debug

    @classmethod
    def get_llm_cache(cls):
        return cls.llm_cache
    
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

def get_cache_key(prompt: str, temperature: float = 0.0, top_p: float = 1.0) -> str:
    """
    캐시 키 생성
    
    :param prompt: 입력 프롬프트
    :param temperature: 모델 출력의 창의성, 무작위성 조정 (확률분포의 분산 조절)
    :param top_p: 누적확률샘플링 기반, 모델이 단어를 선택할 확률 범위 제한
    :return: 캐시 키    
    """
    # 결합 키
    key_data = f"{prompt}-{temperature}-{top_p}"
    
    prompt_bytes = key_data.encode('utf-8')
    hash_object = hashlib.sha256(prompt_bytes)
    
    return base64.urlsafe_b64encode(hash_object.digest()).decode('utf-8')