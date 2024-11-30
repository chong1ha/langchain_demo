import json
import pandas as pd
from io import StringIO

class OutputParser:
    
    @staticmethod
    def to_json(response: str):
        """
        response 를 json으로 변환
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse the response as JSON."}

    @staticmethod
    def to_dataframe(response: str):
        """
        reponse 를 dataframe으로 변환
        """
        try:
            response_io = StringIO(response)
            df = pd.read_csv(response_io)
            return df
        except Exception as e:
            return {"error": f"Failed to convert response to DataFrame. {str(e)}"}

    @staticmethod
    def to_text(response: str):
        """
        response를 plain text로 변환
        """
        return response