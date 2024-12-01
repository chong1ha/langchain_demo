from langchain_community.llms import OpenAI
from core.utils.config import Config
from .model_async_handler import ModelAsyncHandler


class ModelManager:
    """
    OpenAI 모델 관리 및 프롬프트에 대한 응답 반환
    """

    def __init__(self):
        Config.check_config() 
        self.model = OpenAI(api_key=Config.OPENAI_API_KEY, temperature=0.1)

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