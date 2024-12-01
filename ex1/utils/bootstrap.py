import streamlit as st


def add_bootstrap():
    """
    Streamlit 애플리케이션에 부트스트랩 스타일을 추가,
    라디오 버튼 CSS
    """
    st.markdown("""
        <style>
            /* =======================================
            라디오 버튼 스타일
            ======================================= */
            /* 라디오 버튼 그룹을 수평으로 배치 */
            div[role="radiogroup"] {
                display: flex;
                flex-direction: row;
                gap: 12px;
            }
            
            /* 라디오 버튼이 선택되었을 때, 스타일 */
            input[type="radio"] + div {
                background: #63ADD2 !important;
                color: #FFF;
                border-radius: 38px !important;
                padding: 8px 18px !important;
            }
            
            /* 선택된 라디오 버튼의 스타일 */
            input[type="radio"][tabindex="0"] + div {
                background: #E6FF4D !important;
                color: #17455C !important;
            }
            
            /* 선택된 라디오 버튼 내의 텍스트 색상 */
            input[type="radio"][tabindex="0"] + div p {
                color: #17455C !important;
            }
            
            div[role="radiogroup"] label > div:first-child {
                display: none !important;
            }
            div[role="radiogroup"] label {
                margin-right: 0px !important;
            }
            
            /* =======================================
            일반 버튼 스타일
            ======================================= */
            .stButton > button {
                background-color: #007BFF;  /* 파란색 배경 */
                color: white;               /* 흰색 텍스트 */
                border-radius: 5px;         /* 둥근 테두리 */
                padding: 10px 20px;         /* 버튼에 패딩 추가 */
                border: none;               /* 기본 테두리 제거 */
                font-size: 16px;            /* 폰트 크기 */
                cursor: pointer;           /* 마우스 커서 */
                transition: background-color 0.3s ease;  /* 배경색 변화에 부드러운 전환 효과 추가 */
            }

            /* 버튼에 마우스를 올렸을 때 Style */
            .stButton > button:hover {
                background-color: #0056b3;  /* 배경색 변경 */
                color: white !important;
            }
            /* 버튼 클릭 시 스타일 (active 상태) */
            .stButton > button:active {
                background-color: #004085;
                color: white !important; 
            }

            /* =======================================
            텍스트 입력창 스타일
            ======================================= */
            .stTextInput input {
                border: 1px solid #ccc;  /* 연한 회색 테두리 */
                padding: 10px;            /* 패딩 추가 */
                border-radius: 4px;       /* 둥근 테두리 */
                width: 100%;              /* 가로 너비 100% */
                font-size: 16px;          /* 폰트 크기 */
            }

            /* 텍스트 입력창에 포커스를 주었을 때 스타일 */
            .stTextInput input:focus {
                border-color: #007BFF;     /* 포커스 시 테두리 색상 변경 */
                outline: none;             /* 포커스 테두리 제거 */
            }
        </style>
    """, unsafe_allow_html=True)