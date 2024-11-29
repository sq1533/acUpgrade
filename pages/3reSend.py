import time
import pandas as pd
import streamlit as st
from customs.custom import css
#사이드바 제거
st.markdown(css, unsafe_allow_html=True)
#미정산 거래 정보기입
st.header("미정산거래, 팩스 재전송 필요")
textArea,emptyArea = st.columns([2,1],vertical_alignment="bottom")
Date = textArea.text_input(label="수신 일시",value=None,placeholder="MM/DD hh:mm",label_visibility="visible")
emptyArea.empty()
Bank = textArea.text_input(label="원천사",value=None,placeholder="농협",label_visibility="visible")
emptyArea.empty()
Info = textArea.text_input(label="피해자 정보(이름, 금액 등)",value=None,placeholder="홍*동 300000원",label_visibility="visible")
emptyArea.empty()
secter1,secter2 = st.columns([2,1],vertical_alignment="bottom")
signUp = secter1.radio(label="민원등록 여부",options=["등록 완료","등록 미완료(등록 필요)"])
#저장
if secter2.button(label="저장"):
    read = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\6-2reMind.json",orient='records',dtype={'date':str,'bank':str,'info':str,'signUp':str})
    new = pd.DataFrame(data={"date":Date,"bank":Bank,"info":Info,"signUp":signUp},index=[0])
    pd.concat([read,new],ignore_index=True).to_json("C:\\Users\\USER\\ve_1\\DB\\6-2reMind.json",orient='records',force_ascii=False,indent=4)
    with st.spinner('전송중....'):
        time.sleep(1)
    st.success(body="저장완료")