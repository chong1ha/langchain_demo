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
        try:
            # 동기식 호출
            return self.model.invoke(prompt)
        except Exception as e:
            raise ValueError(f"모델에서 응답을 생성하는 동안 오류 발생: {str(e)}")
        
    async def get_response_async(self, prompt: str) -> str:
        """
        비동기식    
        """
        try:
            response = await self.model.ainvoke(prompt)
            return response
        except Exception as e:
            raise ValueError(f"모델에서 응답을 생성하는 동안 오류 발생: {str(e)}")
        
    def get_batch_response_sync(self, prompts: list) -> list:
        """
        동기식 배치 처리
        """
        responses = []
        
        for prompt in prompts:
            response = self.get_response_sync(prompt) 
            responses.append(response)
            
        return responses
    
    async def get_batch_response_async(self, prompts: list) -> list:
        """
        비동기식 배치 처리
        """
        try:
            # 여러 비동기 작업, 병렬 실행
            model_async_handler = ModelAsyncHandler()
            
            responses = await self.model.abatch(
                inputs=prompts,
                config={"callbacks": [model_async_handler]}
            )
            
            return responses
        except Exception as e:
            raise ValueError(f"배치 응답을 생성하는 동안 오류 발생: {str(e)}")
# End of ModelManager