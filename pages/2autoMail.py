import time
from datetime import datetime
import pandas as pd
import requests
import json
import streamlit as st

from customs.custom import css
#사이드바 제거
st.markdown(css, unsafe_allow_html=True)
#메일 DB저장
def sendMail():
    requests.post("http://127.0.0.1:8000/email",json.dumps(email))
#DB데이터 불러오기
with open('C:\\Users\\USER\\ve_1\\DB\\4-2mailInfo.json', 'r', encoding='utf-8') as f:
    mailInfo = json.load(f)
coochip = pd.Series(mailInfo["쿠칩"])
cooIndex = pd.Series(mailInfo["쿠칩제목"])
cooRcv = pd.Series(mailInfo["쿠칩수신자"])
recive = pd.Series(mailInfo["수신자"])
servise = pd.Series(mailInfo["서비스"])
bank = pd.Series(mailInfo["원천사"]["은행"])
pg = pd.Series(mailInfo["원천사"]["PG원천사"])
month = pd.Series(mailInfo["월"])
#메일 구분
tab1,tab2 = st.tabs(["영문메일 전송","쿠칩메일 전송"])
with tab1:
    #인증번호 입력
    if st.button(label="영문메일 전송"):
        pd.DataFrame({"coochip":"end","enMail":"start","hotline":"end"},index=[0]).to_json('C:\\Users\\USER\\ve_1\\DB\\4-1mailStart.json',orient='records',force_ascii=False,indent=4)
    #메일 정보 입력
    bady1,empty = st.columns(spec=[1,2],gap="small",vertical_alignment="center")
    st.write("수신자")
    bady2_1,bady2_2,bady2_3,bady2_4 = st.columns(spec=[1,1,1,1],gap="small",vertical_alignment="center")
    st.write("참조자")
    bady2_2 = st.columns(spec=[1],gap="small",vertical_alignment="center")
    bady3,empty = st.columns(spec=[1,1],gap="small",vertical_alignment="center")
    bady4,empty = st.columns(spec=[1,1],gap="small",vertical_alignment="center")
    bady5,empty = st.columns(spec=[1,1],gap="small",vertical_alignment="center")
    bady6,empty = st.columns(spec=[1,1],gap="small",vertical_alignment="center")
    #인증번호
    passN : str = bady1.text_input("pg_info 인증(장애안내)", max_chars=4)
    bady1.empty()
    bady1.empty()
    #메일 수신자 선택
    if bady2_1.checkbox("간편 송금"):adr1 : str = recive["간편송금"]
    else:adr1 : str = ""
    if bady2_2.checkbox("내통장결제"):adr2 : str = recive["내통장결제"]
    else:adr2 : str = ""
    if bady2_3.checkbox("PG"):adr3 : str = recive["PG"]
    else:adr3 : str = ""
    if bady2_4.checkbox("테스트"):adr4 : str = "mnt@hecto.co.kr"
    else:adr4 : str = ""
    adr : str = f"{adr1},{adr2},{adr3},{adr4}"
    if bady2_2.checkbox("참조(해외영업팀, 서비스관리팀)",value=True):subadr : str = "t_291ts@hecto.co.kr, mnt@hecto.co.kr"
    else:subadr : str = ""
    S = []
    O = ""
    #서비스, 원천사 선택
    serv_select = bady3.multiselect("서비스",list(servise.keys()))
    for i in serv_select:
        S.append(servise[i])
    S = " | ".join(S)
    bank_select = bady3.selectbox("은행선택",(list(bank.keys())))
    pg_select = bady3.selectbox("PG선택", (list(pg.keys())))
    if bank_select == "선택":bank_select = ""
    else:
        O = bank[bank_select]
    if pg_select == "선택":pg_select = ""
    else:
        O = pg[pg_select]
    error_DAY1 = str(bady4.date_input("시작 시간",(datetime.now()),format="YYYY-MM-DD"))
    error_DAY = month[error_DAY1.split("-")[1]]+"-"+error_DAY1.split("-")[2]+"-"+error_DAY1.split("-")[0]
    clear_DAY1 = str(bady4.date_input("종료 시간",(datetime.now()),format="YYYY-MM-DD"))
    clear_DAY = month[clear_DAY1.split("-")[1]]+"-"+clear_DAY1.split("-")[2]+"-"+clear_DAY1.split("-")[0]
    error_TIME = str(bady5.text_input("장애 시작 시간","",label_visibility="hidden"))
    clear_TIME = str(bady5.text_input("장애 종료 시간","",label_visibility="hidden"))
    error_MtoS = str(datetime.strptime(error_DAY1,'%Y-%m-%d').strftime("%a"))
    clear_MtoS = str(datetime.strptime(clear_DAY1,'%Y-%m-%d').strftime("%a"))
    if bady6.button(label="장애안내"):
        T = error_DAY+"("+error_MtoS+")"+" "+error_TIME+"~"
        title = "[{s}] {o} Error Notice ({t})".format(s=S,o=O,t=T)
        main = """
Dear valued customers.
Thank you for using Hecto Financial's {s} service.
We are sending you an emergency notice as an error has occurred. Please refer below for the details.

--------------------------------------------------------------------------------------------------------------
- Name of Institution   : {o}
- Impacted Service      : {s}
- Date & Time of Error : {t}
- Details                   : Service not available
--------------------------------------------------------------------------------------------------------------

We will send you an update as soon as the recovery is complete.
Thank you.
""".format(s=S,o=O,t=T)
        email = {
            "passnumber":passN,
            "addr":adr,
            "subaddr":subadr,
            "title":title,
            "main":main
            }
        sendMail()
        with st.spinner('전송중....'):
            time.sleep(10)
        st.success('메일전송 완료')
    bady6.empty()
    if bady6.button(label="정상안내"):
        T = error_DAY+"("+error_MtoS+")"+" "+error_TIME+" ~ "+clear_DAY+"("+clear_MtoS+")"+" "+clear_TIME
        title = "[{s}] {o} Error Recovery Notice ({t})".format(s=S,o=O,t=T)
        main = """
Dear valued customers.
Thank you for using Hecto Financial's {s} service.
We are sending you an emergency notice as an error has occurred. Please refer below for the details.

--------------------------------------------------------------------------------------------------------------
- Name of Institution   : {o}
- Impacted Service      : {s}
- Date & Time of Error : {t}
- Details                   : Service not available
- Result                    : Error recovery completed, service use normalized
--------------------------------------------------------------------------------------------------------------

We apologize for any inconvenience caused.
Thank you.
""".format(s=S,o=O,t=T)
        email = {
            "passnumber":passN,
            "addr":adr,
            "subaddr":subadr,
            "title":title,
            "main":main
            }
        sendMail()
        with st.spinner('전송중....'):
            time.sleep(10)
        st.success('메일전송 완료')
    bady6.empty()
with tab2:
    #인증번호 입력
    if st.button(label="쿠칩메일 전송"):
        pd.DataFrame({"coochip":"start","enMail":"end","hotline":"end"},index=[0]).to_json('C:\\Users\\USER\\ve_1\\DB\\4-1mailStart.json',orient='records',force_ascii=False,indent=4)
    bady1,empty = st.columns(spec=[1,2],gap="small",vertical_alignment="center")
    bady2_1 = st.columns(spec=[1],gap="small",vertical_alignment="center")
    bady2_2 = st.columns(spec=[1],gap="small",vertical_alignment="center")
    passN : str = bady1.text_input("pg_info2 인증번호", max_chars=4)
    bady1.empty()
    bady1.empty()
    select_adr : str = bady2_1.selectbox("수신자",list(cooRcv.keys()))
    adr : str = cooRcv[select_adr]
    if bady2_2.checkbox("참조자(쿠폰사업팀, 서비스관리팀)",value=True):
        subadr : str = "couchip@hecto.co.kr, mnt@hecto.co.kr"
    else:
        subadr : str = ""
    select = st.selectbox("메일 선택",list(coochip.keys()))
    title : str = cooIndex[select]
    main : str = coochip[select]
    email = {
        "passnumber":passN,
        "addr":adr,
        "subaddr":subadr,
        "title":title,
        "main":main
        }
    if st.button(label="전송"):
        sendMail()
        with st.spinner('전송중....'):
            time.sleep(10)
        st.success('메일전송 완료')