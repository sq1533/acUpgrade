import json
import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from customs.custom import css
import clipboard
#상단 빈칸제거 및 사이드바 제거
st.markdown(css,unsafe_allow_html=True)
#데이터 불러오기
with open('C:\\Users\\USER\\ve_1\\DB\\3loginInfo.json', 'r', encoding="UTF-8") as f:
    login_DB = json.load(f)
with open('C:\\Users\\USER\\ve_1\\DB\\5sideBar.json','r',encoding="UTF-8") as f:
    order = json.load(f)
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
                st.write(midInfo.loc[midInfo['mid']==mid]['info'].tolist()[0].replace("<br>","  \n"))
                st.write(midInfo.loc[midInfo['mid']==mid]['char'].tolist()[0].replace("<br>","  \n"))
            else:
                st.write('존재하지 않는 MID입니다.')
    components.iframe(url,width=650,height=2350)
    with st.sidebar:
        stoKey = st.selectbox("증권사 이용 핫라인",list(order['stock'].keys()))
        st.write(order["stock"][stoKey])
        svr = st.selectbox("주요 서버 목록",order["server"],index=None)
        st.code(svr)
        line = []
        send = st.text_input("핫라인 전파")
        if st.checkbox("카카오페이",value=True):line.append(123)
        if st.checkbox("쿠팡",value=True):line.append(123)
        if st.checkbox("카카오모빌리티",value=True):line.append(123)
        if st.checkbox("네이버페이",value=True):line.append(123)
        if st.checkbox("카카오 인증서",value=True):line.append(123)
        if st.checkbox("KT지역화폐",value=True):line.append(123)
        if st.button("전파"):
            if send == "":
                st.error("공유될 원천사 정보 없음")
            else:
                clipboard.copy(f"{send} 거래지연 발생중입니다.")
                pd.DataFrame(line).to_json('C:\\Users\\USER\\ve_1\\DB\\4-4hotLine.json',orient='columns',force_ascii=False,indent=4)
                pd.DataFrame({"coochip":"end","enMail":"end","hotline":"start"},index=[0]).to_json('C:\\Users\\USER\\ve_1\\DB\\4-1mailStart.json',orient='records',force_ascii=False,indent=4)
                with st.spinner('구동중입니다.'):
                    time.sleep(4)
                    st.success('핫라인을 확인해주세요.')

if __name__ == '__main__':
    H_page()