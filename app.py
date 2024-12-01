import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Optional

from core.utils.message import Message
from ex1.prompts.templates import PromptTemplate
from ex1.models.model_manager import ModelManager
from ex1.parsers.parser import OutputParser
from ex1.utils.bootstrap import add_bootstrap


class LangChainApp:
    """
    App
    """
    
    def __init__(self):
        self.prompt_template = PromptTemplate("$city에서 가장 유명한 관광지는 무엇인가요?")
        self.model = ModelManager()

    def _get_user_input(self) -> None:
        """
        사용자 입력 처리
        """
        st.session_state.city_name = st.text_input(
            "도시 이름을 입력하세요:",
            placeholder="{city}에서 가장 유명한 관광지는 무엇인가요?"
        )

    def _generate_response(self) -> None:
        """
        모델에서 응답메시지 생성
        """
        if st.session_state.city_name:
            
            try:
                prompt = self.prompt_template.generate(city=st.session_state.city_name)
                answer = self.model.get_response(prompt)
                answer_time = int(datetime.now().timestamp())

                # 응답 메시지 생성
                st.session_state.response = Message(
                    time=answer_time,
                    subject=prompt,
                    body=answer.strip()
                )
                st.session_state.generated = True
                st.write("응답이 생성되었습니다.")
            except Exception as e:
                st.error(f"응답 생성 중 오류 발생: {str(e)}")
        else:
            st.error("도시 이름을 입력해주세요.")

    def _display_response(self):
        """
        응답에 대한 형식별 출력 (화면 출력)
        """
        if 'response' in st.session_state and st.session_state.response:
            
            try:
                output_format = st.radio(
                    "응답 형식 선택:",
                    ("JSON", "Text", "DataFrame"),
                    key="output_format",
                    help="응답 형식을 선택하세요.",
                    horizontal=True
                )

                # 응답 형식에 따른 처리
                if output_format == "JSON":
                    parsed_response = OutputParser.to_json(st.session_state.response)
                    st.json(parsed_response)
                elif output_format == "DataFrame":
                    parsed_response = OutputParser.to_dataframe(st.session_state.response)
                    if isinstance(parsed_response, pd.DataFrame):
                        st.dataframe(parsed_response)
                    else:
                        st.write("응답을 DataFrame으로 변환 실패:", parsed_response)
                else:
                    st.text_area("응답 (Text 형식):", OutputParser.to_text(st.session_state.response), height=200)
            except Exception as e:
                st.error(f"응답 표시 중 오류 발생: {str(e)}")
# End of LangChainApp

def initialize_session() -> None:
    """세션 상태 초기화 로직"""
    if "response" not in st.session_state:
        st.session_state.response = None
        
    if "city_name" not in st.session_state:
        st.session_state.city_name = ""
        
    if "generated" not in st.session_state:
        st.session_state.generated = False

def main() -> None:
    st.set_page_config(page_title="LangChain Demo", layout="centered")

    # Bootstrap 적용
    add_bootstrap()
    st.title("LangChain Example")
    initialize_session()

    # 사용자 입력
    app = LangChainApp()
    app._get_user_input()

    # 질문 버튼 클릭 시, 응답 처리
    if st.button("질문하기"):
        app._generate_response()

    # 화면에 응답 출력
    if st.session_state.generated:
        app._display_response()


if __name__ == "__main__":
    main()
