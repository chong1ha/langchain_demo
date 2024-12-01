from langchain_core.pydantic_v1 import BaseModel, Field
from datetime import datetime


class Message(BaseModel):
    """
    Base Message
    """
    
    time: int = Field(..., description="Message create time")
    subject: str = Field(..., description="Message subject")
    body: str = Field(..., description="Message body")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_subject(self) -> str:
        return self.subject

    def get_body(self) -> str:
        return self.body

    def get_readable_time(self) -> str:
        return datetime.fromtimestamp(self.time).strftime('%Y-%m-%d %H:%M:%S')
# End of Message
