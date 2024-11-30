import streamlit as st
import pandas as pd

from ex1.prompts.templates import PromptTemplate
from ex1.models.model_manager import ModelManager
from ex1.parsers.parser import OutputParser


def main():
    
    st.title("LangChain Prompt Template Example")

    # Template 정의
    prompt_template = PromptTemplate("$city에서 가장 유명한 관광지는 무엇인가요?")

    # 사용자 입력
    city_name = st.text_input("도시 이름을 입력하세요:")
    
    model = ModelManager()
    
    # 버튼 클릭 시 응답 받기
    if st.button("질문하기"):
        
        if city_name:
            # 프롬프트 생성
            prompt = prompt_template.generate(city=city_name)
            response = model.get_response(prompt)
            
            st.write("응답 (Text 형식):", response)
        
            parsed_df = OutputParser.to_dataframe(response)
            if isinstance(parsed_df, pd.DataFrame):
                st.write("응답 (DataFrame 형식):", parsed_df)
            else:
                st.write("응답을 DataFrame으로 변환 실패:", parsed_df)
        else:
            st.error("도시 이름을 입력해주세요.")

if __name__ == "__main__":
    main()
