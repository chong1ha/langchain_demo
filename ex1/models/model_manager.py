from langchain_community.llms import OpenAI
from langchain_community.callbacks import get_openai_callback
from core.utils.config import Config
from .model_async_handler import ModelAsyncHandler
from langchain.globals import set_llm_cache, set_debug
from langchain_community.cache import RedisCache, InMemoryCache, RedisSemanticCache
from langchain.embeddings import OpenAIEmbeddings
from redis import Redis


def init_global_settings(use_redis_cache=False):
    """
    전역 설정 초기화
    """
    try:
        Config.check_required_config()
        
        if use_redis_cache and Config.REDIS_URL:
            # Config.LLM_CACHE = RedisSemanticCache(
            #     redis_url=Config.REDIS_URL, 
            #     embedding=OpenAIEmbeddings()
            # )
            Config.LLM_CACHE = RedisCache(
                redis_= Redis(
                    host="localhost",
                    port=6379,
                    password="redis"
                )
            )
        else:
            Config.LLM_CACHE = InMemoryCache()
    
        set_debug(False)
        set_llm_cache(Config.LLM_CACHE)
    
    except Exception as e:
        raise RuntimeError(e)

init_global_settings(use_redis_cache=True)


class ModelManager:
    """
    OpenAI 모델 관리 및 프롬프트에 대한 응답 반환
    """

    def __init__(self):
        self.model = OpenAI(api_key=Config.OPENAI_API_KEY, temperature=0.0, top_p=1.0, cache=True)
        
    def get_response(
        self, 
        # temperature: 모델 출력의 창의성, 무작위성 조정 (확률분포의 분산 조절)
        # top_p: 누적확률샘플링 기반, 모델이 단어를 선택할 확률 범위 제한
        prompt: str, temperature: float = 0.0, top_p: float = 1.0, 
        mode: str = "sync", batch: bool = False, stream: bool = False, meta_info: bool = False
    ):
        """
        모델 응답 반환
        
        :param prompt: 입력 프롬프트
        :param mode: 'sync' (동기), 'async' (비동기)
        :param batch: True는 배치 처리 
        :param stream: True는 스트리밍 처리
        :param meta_info: True는 응답 + 메타정보
        """
        try:            
            with get_openai_callback() as callback:
                
                if batch:
        
                    if mode == "sync":
                        response = self.get_batch_response_sync([prompt])
                    elif mode == "async":
                        response = self.get_batch_response_async([prompt])
                elif stream:
                    response = self.stream_response_sync(prompt)
                else:
                    if mode == "sync":
                        response = self.get_response_sync(prompt)
                    elif mode == "async":
                        response = self.get_response_async(prompt)
                
                if meta_info:
                    meta = self._get_meta_info(callback)
                    return {"response": response, "meta_info": meta}

                return {"response": response, "meta_info": ""}
        except Exception as e:
            raise ValueError(f"응답 처리 중 오류 발생: {str(e)}")
    
    def _get_meta_info(self, callback) -> dict:
        """
        메타정보 추출
        
        :param callback: OpenAI Callback
        :return: dict
        """
        return {
            "Tokens Used": callback.total_tokens,
            "Prompt Tokens": callback.prompt_tokens,
            "Completion Tokens": callback.completion_tokens,
            "Total Cost (USD)": callback.total_cost,
            "Successful Requests": callback.successful_requests,
        }
        
    def get_response_sync(self, prompt: str) -> str:
        """
        동기식 
        """
        return self._invoke_model(prompt)
        
    async def get_response_async(self, prompt: str) -> str:
        """
        비동기식    
        """
        return await self._invoke_model_async(prompt)
        
    def get_batch_response_sync(self, prompts: list[str]) -> list[str]:
        """
        동기식 배치 처리
        """
        return [self.get_response_sync(prompt) for prompt in prompts]
    
    async def get_batch_response_async(self, prompts: list[str]) -> list[str]:
        """
        비동기식 배치 처리
        """
        return await self._invoke_batch_async(prompts)
        
    def _invoke_model(self, prompt: str) -> str:
        """
        내부, 모델 동기 호출 처리
        """
        try:
            return self.model.invoke(prompt)
        except Exception as e:
            raise ValueError(f"모델 호출 중 오류 발생: {str(e)}")

    async def _invoke_model_async(self, prompt: str) -> str:
        """
        내부, 모델 비동기 호출 처리
        """
        try:
            return await self.model.ainvoke(prompt)
        except Exception as e:
            raise ValueError(f"비동기 모델 호출 중 오류 발생: {str(e)}")
        
    async def _invoke_batch_async(self, prompts: list[str]) -> list[str]:
        """
        내부, 비동기식 배치 호출 처리
        """
        try:
            model_async_handler = ModelAsyncHandler()
            
            return await self.model.abatch(
                inputs=prompts, config={"callbacks": [model_async_handler]}
            )
        except Exception as e:
            raise ValueError(f"비동기 배치 호출 중 오류 발생: {str(e)}")
        
    def stream_response_sync(self, prompt: str) -> None:
        """
        스트리밍 응답을 동기적으로 처리
        """
        try:
            for chunk in self.model.stream_sync(prompt):
                print(chunk, end="", flush=True)
        except Exception as e:
            print(f"\n스트림 처리 중 오류 발생: {str(e)}")
# End of ModelManager