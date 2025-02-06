import os
import pandas
import streamlit as st

#AI_MON simple 알람 타켓
nonePay = [':거래없음',':거래감소',':거래(성공건)없음']
successDown = [':성공율 하락',':비정상환불',':비정상취소']
error = [':동일오류',':오류발생']
upperPay = [':거래급증',':거래(오류)급증']
all = nonePay + successDown + error + upperPay
categorys = {"전체":all,"성공률하락":successDown,"거래감소":nonePay,"Error":error,"거래급증":upperPay}

cols1,cols2,cols3,cols4 = st.columns(spec=4,gap='small',vertical_alignment="center")

startDate = cols1.date_input(label="조회 범위(시작)",format="YYYY-MM-DD")
endDate = cols2.date_input(label="조회 범위(종료)",format="YYYY-MM-DD")
index = cols3.selectbox(label="카테고리",options=categorys.keys())
text = cols4.text_input(label="포함된 단어")

lookupButton = st.button(label="조회")

if lookupButton:
    lookupAlarm = []
    lookupDate = []
    dateRange = pandas.date_range(start=startDate,end=endDate,unit=None).strftime("%y%m%d").tolist()
    for date in dateRange:
        AlarmPath = os.path.join(os.path.dirname(__file__),"..","DB",f"3worksAlarm_{date}.json")
        if os.path.exists(AlarmPath):
            Data = pandas.read_json(AlarmPath,orient="records",dtype={"Alarm":str,"date":str,"check":str})
            alarms = Data["Alarm"].tolist()
            for alarm in alarms:
                if any(i in alarm for i in categorys[index]):
                    if text:
                        if text in alarm:
                            lookupAlarm.append(alarm.replace("<br>",""))
                            lookupDate.append(Data.loc[Data["Alarm"]==alarm,'date'].tolist()[0].split(' ')[0])
                        else:
                            pass
                    else:
                        lookupAlarm.append(alarm.replace("<br>",""))
                        lookupDate.append(Data.loc[Data["Alarm"]==alarm,'date'].tolist()[0].split(' ')[0])
                else:
                    pass
            result = pandas.DataFrame(data={"date":lookupDate,"Alarm":lookupAlarm})
            st.write(result)
        else:
            st.error(f"{date} 알람 파일은 없습니다.")
            break