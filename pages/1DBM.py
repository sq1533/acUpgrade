import requests
import pandas as pd
import json
import streamlit as st
from customs.custom import css
#사이드바 제거
st.markdown(css, unsafe_allow_html=True)
#데이터 불러오기
midInfo = pd.read_json('C:\\Users\\USER\\ve_1\\DB\\2midInfo.json',orient="records",dtype={"mid":str,"info":str,"char":str})
midList = midInfo['mid'].tolist()
#DB수정 API
url = "http://127.0.0.1:8000/mk_info"
url_d = "http://127.0.0.1:8000/mk_info_d"
def create():
    requests.post(url,json.dumps(mk_info))
def change():
    requests.put(url,json.dumps(mk_ch))
def delete():
    requests.post(url_d,json.dumps(mk_d))
tab1,tab2,tab3 = st.tabs(["생성","수정","삭제"])
#생성
with tab1:
    with st.form(key="mk_info"):
        mid: str = st.text_input("mid", max_chars=20)
        info: str = st.text_area("정보")
        char: str = st.text_area("담당자")
        mk_info = {
            "mid":mid,
            "info":info.replace('\n','  \n'),
            "char":char.replace('\n','  \n')
        }
        btn_1 = st.form_submit_button(label="생성")
        if btn_1:
            if mk_info['mid'] not in midList:
                create()
                st.markdown("생성완료")
            else:
                st.markdown("MID가 이미 존재합니다.")
#수정
with tab2:
    mid: str = st.text_input("mid", max_chars=20)
    btn_2 = st.button(label="조회")
    if btn_2:
        if mid not in midList:
            st.markdown("MID가 존재하지 않습니다.")
    with st.form(key="mk_ch"):
        if mid not in midList:
            swap = "수정 전 mid를 조회 해주세요"
        else:
            swap = mid
        mid: str = st.text_input("mid",swap,max_chars=20)
        info: str = st.text_area("정보",midInfo.loc[midInfo['mid']==swap]['info'].tolist()[0].replace("<br>","\n"),height=250)
        char: str = st.text_area("담당자",midInfo.loc[midInfo['mid']==swap]['char'].tolist()[0].replace("<br>","\n"),height=100)
        mk_ch = {
            "mid":mid,
            "info":info.replace('\n','  \n'),
            "char":char.replace('\n','  \n')
        }
        btn_3 = st.form_submit_button(label="수정")
        if btn_3:
            change()
            st.markdown("수정완료")
with tab3:
    with st.form(key="mk_d"):
        mid: str = st.text_input("mid", max_chars=20)
        mk_d = {
            "mid":mid
        }
        btn_4 = st.form_submit_button(label="삭제")
        if btn_4:
            if mk_d['mid'] not in midList:
                st.markdown("MID가 존재하지 않습니다.")
            else:
                delete()
                st.markdown("삭제완료")