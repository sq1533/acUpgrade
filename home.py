import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from customs.custom import css
#상단 빈칸제거 및 사이드바 제거
st.markdown(css,unsafe_allow_html=True)
#데이터 불러오기
with open('C:\\Users\\USER\\ve_1\\DB\\3loginInfo.json', 'r', encoding="UTF-8") as f:
    login_DB = json.load(f)
url = pd.Series(login_DB['IP'])['IP']+"/home"
#실시간 알람 불러오기
def H_page():
#실시간 알람 불러오기
    midInfo = pd.read_json('C:\\Users\\USER\\ve_1\\DB\\2midInfo.json',orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = midInfo['mid'].tolist()
    with st.expander(label="조회",expanded=False):
        mid = st.text_input("MID조회(입력 후 Enter)")
        if st.button("조회"):
            if mid in midList:
                st.write(midInfo[midInfo['mid']==mid]['info'].values.replace("<br>","  \n"))
                st.write(midInfo[midInfo['mid']==mid]['char'].values.replace("<br>","  \n"))
            else:
                st.write('존재하지 않는 MID입니다.')
    components.iframe(url,width=650,height=2350)
    with st.sidebar:
        with open('C:\\Users\\USER\\ve_1\\DB\\5sideBar.json','r',encoding="UTF-8") as f:
            order = json.load(f)
        stoKey = st.selectbox("증권사 이용 핫라인",list(order['stock'].keys()))
        st.write(order["stock"][stoKey])
        svr = st.selectbox("주요 서버 목록",order["server"],index=None)
        st.code(svr)

if __name__ == '__main__':
    H_page()