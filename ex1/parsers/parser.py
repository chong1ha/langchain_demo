import json
import pandas as pd

from io import StringIO
from typing import Union, Optional
from langchain_core.pydantic_v1 import BaseModel


class OutputParser:
    """
    다양한 형식의 응답 처리 및 반환
    (JSON, DataFrame, Text)
    """

    @staticmethod
    def to_json(response: Union[BaseModel, str]) -> Optional[dict]:
        """
        응답을 JSON 형식으로 변환
        """
        if isinstance(response, BaseModel):
            return response.dict()
        
        if isinstance(response, str):
            
            if OutputParser._is_valid_json(response):
                return OutputParser._parse_json(response)
            
            return {"error": "Invalid JSON format."}
        
        return {"error": "Invalid response format. Expected BaseModel or str."}

    @staticmethod
    def _is_valid_json(response: str) -> bool:
        """
        유효한 JSON 형식인지 확인
        
        :param response: JSON 문자열
        :return: 유효한 JSON 형식이면 True
        """
        try:
            json.loads(response)
            return True
        except json.JSONDecodeError:
            return False

    @staticmethod
    def _parse_json(response: str) -> dict:
        """
        str을 파싱하여 Python 딕셔너리로 변환
        
        :param response: JSON 문자열
        :return: 파싱된 JSON 
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse the response as JSON."}

    @staticmethod
    def to_dataframe(response: Union[BaseModel, str]):
        """
        응답을 DataFrame으로 변환
        """
        if isinstance(response, BaseModel):
            return OutputParser._base_model_to_dataframe(response)
        
        if isinstance(response, str):
            return OutputParser._string_to_dataframe(response)

        return {"error": "Invalid response format. Expected BaseModel or str."}

    @staticmethod
    def _base_model_to_dataframe(response: BaseModel) -> pd.DataFrame:
        """
        BaseModel 응답을 DataFrame으로 변환
        """
        data = response.dict()
        data['time'] = response.get_readable_time()  # 시간 변환
        return pd.DataFrame([data])

    @staticmethod
    def _string_to_dataframe(response: str) -> Optional[pd.DataFrame]:
        """
        문자열 응답을 CSV 형식으로 변환하여 DataFrame으로 반환
        """
        try:
            response_io = StringIO(response)
            return pd.read_csv(response_io)
        except Exception as e:
            return {"error": f"Failed to convert response to DataFrame: {str(e)}"}

    @staticmethod
    def to_text(response: Union[BaseModel, str]) -> Optional[str]:
        """
        응답을 plain text 형식으로 변환
        """
        if isinstance(response, BaseModel):
            return response.get_body()
        
        if isinstance(response, str):
            return response
        
        return {"error": "Invalid response format. Expected BaseModel or str."}
# End of OutputParser