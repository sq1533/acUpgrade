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
    components.iframe(url,width=650,height=3000)
    with st.sidebar:
        svr = st.selectbox("주요 서버 목록",order["server"],index=None)
        st.code(svr)
        stoKey = st.selectbox("핫라인 전파",list(order['hotLine'].keys()))
        line = order["hotLine"][stoKey]
        ment = st.radio("Choose an option",("지연중입니다.","간헐적 지연중입니다.","개시지연중입니다.","정상화 되었습니다."))
        fixed = stoKey+' '+ment
        if st.button("장애전파"):
            if stoKey == "선택":
                st.error("공유될 원천사 정보 없음")
            else:
                clipboard.copy(fixed)
                pd.DataFrame(line).to_json('C:\\Users\\USER\\ve_1\\DB\\4-4hotLine.json',orient='columns',force_ascii=False,indent=4)
                pd.DataFrame({"coochip":"end","enMail":"end","hotline":"start"},index=[0]).to_json('C:\\Users\\USER\\ve_1\\DB\\4-1mailStart.json',orient='records',force_ascii=False,indent=4)
                with st.spinner('구동중입니다.'):
                    time.sleep(4)
                    st.success('핫라인을 확인해주세요.')
        coor = []
        unfixed = st.text_input("핫라인 전파")
        if st.checkbox("카카오페이",value=True):coor.append(230)
        if st.checkbox("쿠팡",value=True):coor.append(278)
        if st.checkbox("카카오모빌리티",value=True):coor.append(341)
        if st.checkbox("네이버페이",value=True):coor.append(392)
        if st.checkbox("카카오 인증서",value=True):coor.append(449)
        if st.checkbox("KT지역화폐",value=True):coor.append(510)
        if st.button("전파"):
            if unfixed == "":
                st.error("공유될 원천사 정보 없음")
            else:
                clipboard.copy(f"{unfixed}")
                pd.DataFrame(coor).to_json('C:\\Users\\USER\\ve_1\\DB\\4-4hotLine.json',orient='columns',force_ascii=False,indent=4)
                pd.DataFrame({"coochip":"end","enMail":"end","hotline":"start"},index=[0]).to_json('C:\\Users\\USER\\ve_1\\DB\\4-1mailStart.json',orient='records',force_ascii=False,indent=4)
                with st.spinner('구동중입니다.'):
                    time.sleep(4)
                    st.success('핫라인을 확인해주세요.')

if __name__ == '__main__':H_page()