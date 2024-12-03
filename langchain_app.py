import streamlit as st
from datetime import datetime
from typing import Optional
from core.utils.message import Message
from ex1.prompts.templates import PromptTemplate
from ex1.models.model_manager import ModelManager
from ex1.parsers.parser import OutputParser

class LangChainApp:
    """
    App
    """
    
    def __init__(self):
        self.prompt_template = PromptTemplate("$city에서 가장 유명한 관광지는 무엇인가요?")
        self.model = ModelManager()

    def get_city_name(self) -> Optional[str]:
        """
        사용자 입력 처리
        """
        city_name = st.text_input(
            "도시 이름을 입력하세요:",
            placeholder="{city}에서 가장 유명한 관광지는 무엇인가요?"
        )
        return city_name

    def generate_response(self, city_name: str) -> Optional[tuple[Message, dict]]:
        """
        모델에서 응답 메시지 생성
        """
        try:
            prompt = self.prompt_template.generate(city=city_name)
            answer = self.model.get_response(
                prompt=prompt,
                mode="sync",
                batch=False,
                stream=False,
                meta_info=True
            )
            
            response = answer["response"].strip()
            meta_info = answer["meta_info"]

            # 응답 메시지 생성
            message = Message(
                time=int(datetime.now().timestamp()),
                subject=prompt,
                body=response
            )
            return message, meta_info
        except Exception as e:
            st.error(f"응답 생성 중 오류 발생: {str(e)}")
            return None

    def display_response(self, response: Message, meta_info: Optional[dict] = None):
        """
        응답에 대한 형식별 출력 (화면 출력)
        """
        try:
            output_format = st.radio(
                "응답 형식 선택:",
                ("JSON", "Text", "DataFrame", "Meta Info"),
                key="output_format",
                help="응답 형식을 선택하세요.",
                horizontal=True
            )

            # 응답 형식에 따른 처리
            parser_map = {
                "JSON": OutputParser.to_json,
                "Text": OutputParser.to_text,
                "DataFrame": OutputParser.to_dataframe
            }

            if output_format == "Meta Info":
                
                if meta_info:
                    st.subheader("메타정보")
                    st.json(meta_info)
                else:
                    st.warning("메타정보가 없습니다.")
            else:
                parsed_response = parser_map[output_format](response)

                if output_format == "DataFrame" and isinstance(parsed_response, pd.DataFrame):
                    st.dataframe(parsed_response)
                elif output_format == "JSON":
                    st.json(parsed_response)
                else:
                    st.text_area("응답 (Text 형식):", parsed_response, height=200)
        except Exception as e:
            st.error(f"응답 표시 중 오류 발생: {str(e)}")
# End of LangChainApp   

def initialize_session() -> None:
    """
    세션 상태 초기화
    """
    if "response" not in st.session_state:
        st.session_state.response = None
        
    if "city_name" not in st.session_state:
        st.session_state.city_name = ""
        
    if "generated" not in st.session_state:
        st.session_state.generated = False
# End of initialize_session