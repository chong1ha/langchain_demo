from langchain.llms import OpenAI
from core.utils.config import Config


class ModelManager:
    """
    OpenAI 모델 관리 및 프롬프트에 대한 응답 반환
    """

    def __init__(self):
        Config.check_config() 
        self.model = OpenAI(api_key=Config.OPENAI_API_KEY, temperature=0.1)

    def get_response(self, prompt: str) -> str:
        try:
            return self.model.invoke(prompt)
        except Exception as e:
            raise ValueError(f"모델에서 응답을 생성하는 동안 오류 발생: {str(e)}")
# End of ModelManager