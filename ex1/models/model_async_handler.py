import asyncio
from typing import Dict, Any, List
from uuid import UUID
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.schema import BaseMessage


class ModelAsyncHandler(AsyncCallbackHandler):
    
    def __init__(self):
        super().__init__()

    async def on_chat_model_start(
        self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], run_id: UUID, **kwargs: Any
    ) -> None:
        """
        모델 시작 시, 호출되는 콜백
        """
        await asyncio.sleep(0.3)
        
    async def on_chat_model_end(
        self, serialized: Dict[str, Any], run_id: UUID, **kwargs: Any
    ) -> None:
        """
        모델 응답 이후, 처리 작업
        """
        pass
# End of ModelAsyncHandler