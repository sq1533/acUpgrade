import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from customs.custom import css
#상단 빈칸제거 및 사이드바 제거
st.markdown(css,unsafe_allow_html=True)
url = pd.read_json("C:\\Users\\USER\\ve_1\\acUpgrade\\db\\login.json")["IP"]["IP"]+"/home"

#실시간 알람 불러오기
def H_page():
#실시간 알람 불러오기
    with open('C:\\Users\\USER\\ve_1\\alarmCapture\\db\\info_.json','r',encoding="UTF-8") as f:
        DF = json.load(f)
    with st.expander(label="조회",expanded=False):
        mid = st.text_input("MID조회(입력 후 Enter)")
        look = [i for i in range(len(DF)) if DF[i]['mid']==mid]
        if st.button("조회"):
            if look != []:
                st.write(DF[look[0]]['info'])
                st.write(DF[look[0]]['char'])
            else:
                st.write('존재하지 않는 MID입니다.')
    components.iframe(url,width=650,height=2350)
    with st.sidebar:
        order = pd.read_json('C:\\Users\\USER\\ve_1\\acUpgrade\\db\\order.json',orient='records')
        stoKey = st.selectbox("증권사 이용 핫라인",order.loc[0]["stock"].keys())
        st.write(order.loc[0]["stock"][stoKey])
        svr = st.selectbox("주요 서버 목록",order.loc[1]["server"],index=None)
        st.code(svr)

if __name__ == '__main__':
    H_page()