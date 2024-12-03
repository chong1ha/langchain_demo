import streamlit as st
from ex1.utils.bootstrap import add_bootstrap
from langchain_app import LangChainApp, initialize_session

def main() -> None:
    st.set_page_config(page_title="LangChain Demo", layout="centered")

    # Bootstrap 적용
    add_bootstrap()
    st.title("LangChain Example")
    initialize_session()
    
    # 사용자 입력
    app = LangChainApp()
    city_name = app.get_city_name()

    # 질문 버튼 클릭 시, 응답 처리
    if st.button("질문하기"):
        
        if city_name:
            response, meta_info = app.generate_response(city_name)
            
            if response:
                st.session_state.response = response
                st.session_state.meta_info = meta_info
                st.session_state.generated = True
                st.write("응답이 생성되었습니다.")
        else:
            st.error("도시 이름을 입력해주세요.")

    # 화면에 응답 출력
    if st.session_state.generated and st.session_state.response:
        app.display_response(st.session_state.response, st.session_state.get("meta_info"))
        

if __name__ == "__main__":
    main()
